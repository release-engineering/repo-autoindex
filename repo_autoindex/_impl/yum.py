import datetime
import logging
import os
from collections.abc import AsyncGenerator, Generator, Iterable
from dataclasses import dataclass
from typing import Optional, Type, Any, TypeVar, NoReturn, overload
from xml.dom.minidom import Element
from xml.dom.pulldom import END_ELEMENT, START_ELEMENT

from defusedxml import pulldom  # type: ignore

from .base import ICON_PACKAGE, Fetcher, GeneratedIndex, IndexEntry, Repo, ContentError
from .template import TemplateContext
from .tree import treeify

LOG = logging.getLogger("autoindex")


def assert_repodata_ok(condition: Any, msg: str):
    if not condition:
        raise ContentError(msg)


def get_tag(elem: Element, name: str) -> Element:
    elems: list[Element] = elem.getElementsByTagName(name)  # type: ignore
    assert_repodata_ok(len(elems) == 1, f"expected exactly one {name} tag")
    return elems[0]


def get_text_tag(elem: Element, name: str) -> str:
    tagnode = get_tag(elem, name)
    child = tagnode.firstChild
    assert_repodata_ok(child, f"missing text {name} tag")
    return str(child.toxml())  # type: ignore


@dataclass
class Package:
    href: str
    time: str
    size: int

    @classmethod
    def from_element(cls, elem: Element) -> "Package":
        return cls(
            href=get_tag(elem, "location").attributes["href"].value,
            time=get_tag(elem, "time").attributes["file"].value,
            size=get_tag(elem, "size").attributes["package"].value,
        )

    @property
    def index_entry(self) -> IndexEntry:
        return IndexEntry(
            icon=ICON_PACKAGE,
            href=self.href,
            text=os.path.basename(self.href),
            time=datetime.datetime.utcfromtimestamp(float(self.time)).isoformat(),
            size=str(self.size),
        )


def pulldom_elements(
    xml_str: str, path_matcher, attr_matcher=lambda _: True
) -> Generator[Element, None, None]:
    stream = pulldom.parseString(xml_str)
    current_path = []
    for event, node in stream:
        if event == START_ELEMENT:
            current_path.append(node.tagName)

            if path_matcher(current_path) and attr_matcher(node.attributes):
                stream.expandNode(node)
                yield node

                # expandNode makes it so that we don't get END_ELEMENT any more
                # for this node, so pop here.
                current_path.pop()

        elif event == END_ELEMENT:
            LOG.debug("leaving element %s", current_path)
            current_path.pop()


class YumRepo(Repo):
    async def render_index(
        self, index_href_suffix: str
    ) -> AsyncGenerator[GeneratedIndex, None]:
        LOG.debug("repomd.xml: %s", self.entry_point_content)

        entries = []
        entries.extend(await self.__repodata_entries())
        entries.extend(await self.__package_entries())

        for page in self.__render_entries(entries, index_href_suffix):
            yield page

    async def __repodata_entries(self) -> list[IndexEntry]:
        out = []

        # There's always an entry for repomd.xml itself...
        size = len(self.entry_point_content)
        time = "-"
        revision_nodes = list(
            pulldom_elements(
                self.entry_point_content,
                path_matcher=lambda p: p == ["repomd", "revision"],
            )
        )
        if len(revision_nodes) == 1:
            timestamp_node = revision_nodes[0].firstChild
            assert_repodata_ok(timestamp_node, "missing timestamp node")
            time = datetime.datetime.utcfromtimestamp(
                int(timestamp_node.toxml())  # type: ignore
            ).isoformat()

        out.append(
            IndexEntry(
                href="repodata/repomd.xml",
                text="repomd.xml",
                time=time,
                size=str(size),
            )
        )

        data_nodes = list(
            pulldom_elements(
                self.entry_point_content,
                path_matcher=lambda p: p == ["repomd", "data"],
                attr_matcher=lambda attrs: attrs.get("type"),
            )
        )
        data_nodes.sort(key=lambda node: str(node.attributes["type"].value))

        for node in data_nodes:
            href = get_tag(node, "location").attributes["href"].value
            basename = os.path.basename(href)
            timestamp = get_text_tag(node, "timestamp")
            time = datetime.datetime.utcfromtimestamp(float(timestamp)).isoformat()
            size = int(get_text_tag(node, "size"))

            out.append(
                IndexEntry(
                    href=href,
                    text=basename,
                    time=time,
                    size=str(size),
                )
            )

        return out

    async def __package_entries(self) -> list[IndexEntry]:

        primary_nodes = list(
            pulldom_elements(
                self.entry_point_content,
                path_matcher=lambda p: p == ["repomd", "data"],
                attr_matcher=lambda attrs: attrs.get("type")
                and attrs["type"].value == "primary",
            )
        )
        assert len(primary_nodes) == 1
        primary_node = primary_nodes[0]

        location = get_tag(primary_node, "location")
        href = location.attributes["href"].value

        primary_url = "/".join([self.base_url, href])
        primary_xml = await self.fetcher(primary_url)

        assert_repodata_ok(primary_xml, f"missing primary XML at {primary_url}")

        return sorted(
            [p.index_entry for p in self.__packages_from_primary(primary_xml)],  # type: ignore
            key=lambda e: e.text,
        )

    def __packages_from_primary(self, primary_xml: str) -> list[Package]:
        LOG.debug("primary xml: %s", primary_xml)

        out = []
        for elem in pulldom_elements(
            primary_xml,
            path_matcher=lambda p: p == ["metadata", "package"],
            attr_matcher=lambda attrs: attrs.get("type")
            and attrs["type"].value == "rpm",
        ):
            pkg = Package.from_element(elem)
            if pkg:
                out.append(pkg)

        return out

    def __render_entries(
        self,
        entries: Iterable[IndexEntry],
        index_href_suffix: str,
    ) -> Generator[GeneratedIndex, None, None]:
        ctx = TemplateContext()
        nodes = [treeify(entries, index_href_suffix=index_href_suffix)]
        while nodes:
            node = nodes.pop()
            yield GeneratedIndex(
                content=ctx.render_index(index_entries=node.entries),
                relative_dir=node.relative_dir,
            )
            nodes.extend(node.children)

    @classmethod
    async def probe(
        cls: Type["YumRepo"],
        fetcher: Fetcher,
        url: str,
    ) -> Optional["YumRepo"]:
        repomd_xml_url = f"{url}/repodata/repomd.xml"
        repomd_xml = await fetcher(repomd_xml_url)

        if repomd_xml is None:
            # not yum repo
            return None

        # it is a yum repo
        return cls(url, repomd_xml, fetcher)
