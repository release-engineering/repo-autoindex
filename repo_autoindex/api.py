import logging
import gzip
from collections.abc import AsyncGenerator

import aiohttp

from .base import Fetcher, GeneratedIndex
from .yum import YumRepo

LOG = logging.getLogger("repo-autoindex")
REPO_TYPES = [YumRepo]


def http_fetcher(session: aiohttp.ClientSession) -> Fetcher:
    async def get_content_with_session(url: str) -> str:
        LOG.info("Fetching: %s", url)
        async with session.get(url) as resp:
            resp.raise_for_status()

            # Deal with the non-ideal content negotiation
            # for certain storage backends.
            if url.endswith(".gz") and resp.content_type in (
                "application/x-gzip",
                "application/octet-stream",
            ):
                compressed = await resp.content.read()
                uncomp = gzip.decompress(compressed)
                return uncomp.decode("utf-8")

            return await resp.text()

    return get_content_with_session


async def autoindex(
    url: str,
    *,
    fetcher: Fetcher = None,
    index_href_suffix: str = "",
) -> AsyncGenerator[GeneratedIndex, None]:
    if fetcher is None:
        async with aiohttp.ClientSession() as session:
            async for page in autoindex(
                url, fetcher=http_fetcher(session), index_href_suffix=index_href_suffix
            ):
                yield page
        return

    while url.endswith("/"):
        url = url[:-1]

    for repo_type in REPO_TYPES:
        repo = await repo_type.probe(fetcher, url)
        if repo:
            async for page in repo.render_index(index_href_suffix=index_href_suffix):
                yield page
