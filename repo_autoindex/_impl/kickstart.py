from typing import Optional, Type
from collections.abc import AsyncGenerator
import logging
import configparser
import json
import os

from .base import Repo, GeneratedIndex, Fetcher, IndexEntry, ICON_OPTICAL, ICON_QCOW
from .template import TemplateContext
from .tree import treeify
from .yum import YumRepo

LOG = logging.getLogger("repo-autoindex")


class KickstartRepo(YumRepo):
    def __init__(
        self,
        base_url: str,
        repomd_xml: str,
        extra_files: str,
        treeinfo: str,
        fetcher: Fetcher,
    ):
        super().__init__(base_url, repomd_xml, fetcher)
        self.base_url = base_url
        self.fetcher = fetcher
        self.entry_point_content = repomd_xml
        self.extra_files_content = extra_files
        self.treeinfo_content = treeinfo

    async def render_index(
        self, index_href_suffix: str
    ) -> AsyncGenerator[GeneratedIndex, None]:
        all_entries: list[IndexEntry] = []

        # Parse the treeinfo entry point
        LOG.debug("treeinfo: %s", self.treeinfo_content)
        all_entries.extend(await self._treeinfo_entries())

        # Parse the extra_files.json entry point
        #
        # Legacy kickstart tree repositories do not contain extra_files.json files.
        # If the repo does not contain an extra_files.json, do not attempt to process it.
        if self.extra_files_content:
            LOG.debug("extra_files.json: %s", self.extra_files_content)
            all_entries.extend(await self._extra_files_entries())

        # Parse the yum repo embedded in the kickstart repo
        LOG.debug("repomd.xml: %s", self.entry_point_content)
        all_entries.extend(await super()._repodata_entries())
        all_entries.extend(await super()._package_entries())

        ctx = TemplateContext()
        nodes = [treeify(all_entries, index_href_suffix=index_href_suffix)]
        while nodes:
            node = nodes.pop()
            yield GeneratedIndex(
                content=ctx.render_index(index_entries=node.entries),
                relative_dir=node.relative_dir,
            )
            nodes.extend(node.children)

    async def _treeinfo_entries(self) -> list[IndexEntry]:
        """
        A treeinfo file might look like this:

        [checksums]
        images/boot.iso = sha256:f6be6ec48a4a610e25d591dcf98e1777c4274ed58c583fa64d0aea5b3ecffb18
        images/efiboot.img = sha256:94d5500c4ba266ce77b06aa955d9041eea22129737badc6af56c283dcaec1c29
        images/install.img = sha256:46171146377610cfa0deae157bbcc4ea146b3995c9b0c58d9f261ce404468abe
        images/pxeboot/initrd.img = sha256:e0cd3966097c175d3aaf406a7f8c094374c69504c7be8f08d8084ab9a8812796
        images/pxeboot/vmlinuz = sha256:370db9a3943d4f46dc079dbaeb7e0cc3910dca069f7eede66d3d7d0d5177f684

        [general]
        ; WARNING.0 = This section provides compatibility with pre-productmd treeinfos.
        ; WARNING.1 = Read productmd documentation for details about new format.
        arch = x86_64
        family = Red Hat Enterprise Linux
        name = Red Hat Enterprise Linux 8.0.0
        packagedir = Packages
        platforms = x86_64,xen
        repository = .
        timestamp = 1554367044
        variant = BaseOS
        variants = BaseOS
        version = 8.0.0

        [header]
        type = productmd.treeinfo
        version = 1.2

        [images-x86_64]
        boot.iso = images/boot.iso
        efiboot.img = images/efiboot.img
        initrd = images/pxeboot/initrd.img
        kernel = images/pxeboot/vmlinuz

        [images-xen]
        initrd = images/pxeboot/initrd.img
        kernel = images/pxeboot/vmlinuz

        [release]
        name = Red Hat Enterprise Linux
        short = RHEL
        version = 8.0.0

        [stage2]
        mainimage = images/install.img

        [tree]
        arch = x86_64
        build_timestamp = 1554367044
        platforms = x86_64,xen
        variants = BaseOS

        [variant-BaseOS]
        id = BaseOS
        name = BaseOS
        packages = Packages
        repository = .
        type = variant
        uid = BaseOS
        """
        out: list[IndexEntry] = [
            IndexEntry(
                href="treeinfo",
                text="treeinfo",
                size=str(len(self.treeinfo_content)),
            ),
        ]

        treeinfo = configparser.ConfigParser()
        treeinfo.read_string(self.treeinfo_content)

        for image in treeinfo["checksums"]:
            entry = IndexEntry(
                href=image,
                text=os.path.basename(image),
            )
            if entry.href.endswith(".iso") or entry.href.endswith(".img"):
                entry.icon = ICON_OPTICAL
            out.append(entry)
        return out

    async def _extra_files_entries(self) -> list[IndexEntry]:
        """
        An extra_files.json file might look like this:

        {
            "data": [
                {
                    "checksums": {
                        "md5": "feb4d252ee63634debea654b446e830b",
                        "sha1": "a73fad5aeb5642d1b2108885010c4e7a547a1204",
                        "sha256": "c4117d0e325cde392981626edbd1484c751f0216689a171e4b7547e8800acc21"
                    },
                    "file": "RPM-GPG-KEY-redhat-release",
                    "size": 5134
                },
                {
                    "checksums": {
                        "md5": "3c24137e12ece142a27bbf825c256936",
                        "sha1": "a72daf8585b41529269cdffcca3a0b3d4e2f21cd",
                        "sha256": "3f8644b35db4197e7689d0a034bdef2039d92e330e6b22217abfa6b86a1fc0fa"
                    },
                    "file": "RPM-GPG-KEY-redhat-beta",
                    "size": 1669
                },
                {
                    "checksums": {
                        "md5": "b234ee4d69f5fce4486a80fdaf4a4263",
                        "sha1": "4cc77b90af91e615a64ae04893fdffa7939db84c",
                        "sha256": "8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643"
                    },
                    "file": "GPL",
                    "size": 18092
                },
                {
                    "checksums": {
                        "md5": "0c53898068810a989fa59ca0656bdf24",
                        "sha1": "42d51858642b8a0d10fdf09050266395544ea556",
                        "sha256": "8f833ce3fbcbcb82e47687a890c043332c88350ddabd606201556e14aaf8fcd9"
                    },
                    "file": "EULA",
                    "size": 8154
                }
            ],
            "header": {
                "version": "1.0"
            }
        }
        """
        out: list[IndexEntry] = [
            IndexEntry(
                href="extra_files.json",
                text="extra_files.json",
                size=str(len(self.extra_files_content)),
            ),
        ]

        extra_files = json.loads(self.extra_files_content)
        for extra_file in extra_files["data"]:
            entry = IndexEntry(
                href=extra_file["file"],
                text=extra_file["file"],
                size=extra_file["size"],
            )
            out.append(entry)
        return out

    @classmethod
    async def probe(
        cls: Type["KickstartRepo"], fetcher: Fetcher, url: str
    ) -> Optional["KickstartRepo"]:
        treeinfo_url = f"{url}/treeinfo"
        treeinfo_content = await fetcher(treeinfo_url)
        extra_files_url = f"{url}/extra_files.json"
        extra_files_content = await fetcher(extra_files_url) or ""
        repomd_xml_url = f"{url}/repodata/repomd.xml"
        repomd_xml = await fetcher(repomd_xml_url)

        # Modern versions of kickstart repositories (RHEL-8, 9) contain three entry points:
        # treeinfo, extra_files.json, and repomd.xml. repo-autoindex requires that a kickstart
        # repo contains a treeinfo file and exactly one yum repo located in the root of the
        # kickstart tree repo.
        #
        # Legacy kickstart tree repositories do not contain an extra_files.json file. When
        # repo-autoindex encounters a legacy kickstart tree repository, it will attempt to
        # produce a repo index. The repo index produced by repo-autoindex will not contain the
        # files commonly included in extra_files.json (EULA, GPL, GPG keys).
        if treeinfo_content is None or repomd_xml is None:
            return None

        return cls(url, repomd_xml, extra_files_content, treeinfo_content, fetcher)
