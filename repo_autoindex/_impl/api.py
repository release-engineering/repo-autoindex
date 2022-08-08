import gzip
import logging
from collections.abc import AsyncGenerator
from typing import Optional, Type

import aiohttp

from .base import Fetcher, GeneratedIndex, Repo, ContentError, FetcherError
from .yum import YumRepo
from .pulp import PulpFileRepo

LOG = logging.getLogger("repo-autoindex")
REPO_TYPES: list[Type[Repo]] = [YumRepo, PulpFileRepo]


def http_fetcher(session: aiohttp.ClientSession) -> Fetcher:
    async def get_content_with_session(url: str) -> Optional[str]:
        LOG.info("Fetching: %s", url)
        async with session.get(url) as resp:
            if resp.status == 404:
                # This error status means we successfully determined that
                # no content exists
                return None

            # Any other error status is fatal
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


def with_error_handling(fetcher: Fetcher) -> Fetcher:
    # wraps a fetcher such that any raised exceptions are wrapped into FetcherError
    async def new_fetcher(url: str) -> Optional[str]:
        try:
            return await fetcher(url)
        except Exception as exc:
            raise FetcherError from exc

    return new_fetcher


async def autoindex(
    url: str,
    *,
    fetcher: Optional[Fetcher] = None,
    index_href_suffix: str = "",
) -> AsyncGenerator[GeneratedIndex, None]:
    """Generate HTML indexes for a repository.

    Arguments:
        url
            Base URL of repository to be indexed. The function will probe this URL
            for all supported repository types.

        fetcher
            An optional callable to customize the retrieval method for content in the
            repository. Can be omitted to use a basic HTTP(S) fetcher.

            A valid implementation must satisfy this contract:

            - it will be called with the absolute URL of content which may or may not exist
              within the repository (e.g.
              "https://example.com/some-yum-repo/repodata/repomd.xml" when probing a yum
              repository)

            - if the fetcher can determine, without error, that the requested content does not
              exist: it must return ``None``.

            - if the fetcher can retrieve the requested content, it must return the entire
              content at the given URL as a ``str``. This implies that, for example,
              decompressing a compressed file is the responsibility of the fetcher.

            - if the fetcher encounters an exception, it may allow the exception to
              propagate.

        index_href_suffix
            Suffix added onto any links between one generated index and another.

            For example, if the caller intends to save each generated index page as
            autoindex.html, then ``index_href_suffix="autoindex.html"`` should be passed
            so that any links between one index and another will use a correct URL.

            On the other hand, if the caller intends to save each generated index page
            as index.html and serve them via a web server which automatically serves
            files named index.html within each directory, the suffix can be left
            blank.

    Returns:
        An async generator producing zero or more instances of :class:`GeneratedIndex`.

        Zero indexes may be produced if the given URL doesn't represent a repository
        of any supported type.

    Raises:
        :class:`ContentError`
            Raised if indexed content appears to be invalid (for example, a yum repository
            has invalid repodata).

        :class:`Exception`
            Any exception raised by ``fetcher`` will propagate (for example, I/O errors or
            HTTP request failures).
    """
    if fetcher is None:
        async with aiohttp.ClientSession() as session:
            async for page in autoindex(
                url, fetcher=http_fetcher(session), index_href_suffix=index_href_suffix
            ):
                yield page
        return

    while url.endswith("/"):
        url = url[:-1]

    fetcher = with_error_handling(fetcher)

    try:
        for repo_type in REPO_TYPES:
            repo = await repo_type.probe(fetcher, url)
            if repo:
                async for page in repo.render_index(
                    index_href_suffix=index_href_suffix
                ):
                    yield page
    except FetcherError as exc:
        # FetcherErrors are unwrapped to propagate whatever was the original error
        assert exc.__cause__
        raise exc.__cause__ from None
    except ContentError:
        # explicitly raised ContentErrors are allowed to propagate
        raise
    except Exception as exc:
        # Any other errors are treated as a ContentError
        raise ContentError(f"Invalid content found at {url}") from exc
