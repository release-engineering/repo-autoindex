import logging
import os
import datetime
from dataclasses import dataclass
from typing import Type, Optional
from collections.abc import Generator, AsyncGenerator, Iterable

from defusedxml import pulldom
from xml.dom.pulldom import START_ELEMENT, END_ELEMENT, DOMEventStream
from xml.dom.minidom import Element

from .base import Repo, Fetcher, GeneratedIndex, IndexEntry, ICON_PACKAGE, ICON_FOLDER
from .template import TemplateContext
from .tree import treeify

LOG = logging.getLogger("autoindex")


@dataclass
class Package:
    href: str
    time: str
    size: int

    @classmethod
    def from_element(cls, elem: Element) -> "Package":
        return cls(
            href=elem.getElementsByTagName("location")[0].attributes["href"].value,
            # TODO: tolerate some of these being absent or wrong.
            time=elem.getElementsByTagName("time")[0].attributes["file"].value,
            size=elem.getElementsByTagName("size")[0].attributes["package"].value,
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
) -> Generator[Element]:
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
            time = datetime.datetime.utcfromtimestamp(
                float(revision_nodes[0].firstChild.toxml())
            ).isoformat()

        out.append(
            IndexEntry(
                href="repodata/repomd.xml",
                text="repomd.xml",
                time=time,
                size=size,
            )
        )

        data_nodes = list(
            pulldom_elements(
                self.entry_point_content,
                path_matcher=lambda p: p == ["repomd", "data"],
                attr_matcher=lambda attrs: attrs.get("type"),
            )
        )
        data_nodes.sort(key=lambda node: node.attributes["type"].value)

        for node in data_nodes:
            href = node.getElementsByTagName("location")[0].attributes["href"].value
            basename = os.path.basename(href)
            timestamp = node.getElementsByTagName("timestamp")[0].firstChild.toxml()
            time = datetime.datetime.utcfromtimestamp(float(timestamp)).isoformat()
            size = int(node.getElementsByTagName("size")[0].firstChild.toxml())

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

        location = primary_node.getElementsByTagName("location")[0]
        href = location.attributes["href"].value

        primary_url = "/".join([self.base_url, href])
        primary_xml = await self.fetcher(primary_url)

        return sorted(
            [p.index_entry for p in self.__packages_from_primary(primary_xml)],
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
    ) -> Generator[GeneratedIndex, None]:
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
            return

        # it is a yum repo
        return cls(url, repomd_xml, fetcher)
