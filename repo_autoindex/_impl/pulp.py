from typing import Optional, Type
from collections.abc import AsyncGenerator
import logging

from .base import Repo, GeneratedIndex, Fetcher, IndexEntry, ICON_OPTICAL, ICON_QCOW
from .template import TemplateContext
from .tree import treeify

LOG = logging.getLogger("repo-autoindex")


class PulpFileRepo(Repo):
    async def render_index(
        self, index_href_suffix: str
    ) -> AsyncGenerator[GeneratedIndex, None]:
        all_entries: list[IndexEntry] = [
            IndexEntry(
                href="PULP_MANIFEST",
                text="PULP_MANIFEST",
                size=str(len(self.entry_point_content)),
            )
        ]

        # PULP_MANIFEST is a series of lines like this:
        # rhel-workstation-7.2-snapshot-2-x86_64-boot.iso,fa687b8f847b5301b6da817fdbe612558aa69c65584ec5781f3feb0c19ff8f24,379584512
        # rhel-workstation-7.3-rc-2-x86_64-dvd.iso,eab749310c95b4751ef9df7d7906ae0b8021c8e0dbc280c3efc8e967d5e60e71,4324327424
        # rhel-workstation-7.3-rc-1-x86_64-dvd.iso,e165919d6977e02e493605dda6a30d2d80c3f16ee3f4c3ab946d256b815dd5db,4323278848
        # rhel-server-7.3-rc-1-x86_64-boot.iso,f760611401fd928c2840eba85a7a80653fe2dc9dc94f3cef8ec1f3e7880d4102,427819008

        for line in sorted(self.entry_point_content.splitlines()):
            components = line.split(",")
            if len(components) != 3:
                LOG.warning("Ignoring bad line in PULP_MANIFEST: %s", line)
                continue
            entry = IndexEntry(
                href=components[0], text=components[0], size=components[2]
            )
            if entry.href.endswith(".iso"):
                entry.icon = ICON_OPTICAL
            elif entry.href.endswith(".qcow2"):
                entry.icon = ICON_QCOW
            all_entries.append(entry)

        ctx = TemplateContext()
        nodes = [treeify(all_entries, index_href_suffix=index_href_suffix)]
        while nodes:
            node = nodes.pop()
            yield GeneratedIndex(
                content=ctx.render_index(index_entries=node.entries),
                relative_dir=node.relative_dir,
            )
            nodes.extend(node.children)

    @classmethod
    async def probe(
        cls: Type["PulpFileRepo"], fetcher: Fetcher, url: str
    ) -> Optional["PulpFileRepo"]:
        manifest_url = f"{url}/PULP_MANIFEST"
        manifest_content = await fetcher(manifest_url)

        if manifest_content is None:
            return None

        return cls(url, manifest_content, fetcher)
