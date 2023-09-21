import gzip
import logging
from collections.abc import AsyncGenerator, Awaitable, Callable
from typing import Optional, Type, BinaryIO
import tempfile
import io

import aiohttp


from .base import Fetcher, IOFetcher, GeneratedIndex, Repo, ContentError, FetcherError
from .yum import YumRepo
from .pulp import PulpFileRepo
from .kickstart import KickstartRepo

LOG = logging.getLogger("repo-autoindex")
REPO_TYPES: list[Type[Repo]] = [KickstartRepo, YumRepo, PulpFileRepo]


def http_fetcher(session: aiohttp.ClientSession) -> Fetcher:
    async def get_content_with_session(
        url: str,
    ) -> Optional[BinaryIO]:
        LOG.info("Fetching: %s", url)
        async with session.get(url) as resp:
            if resp.status == 404:
                # This error status means we successfully determined that
                # no content exists
                return None

            # Any other error status is fatal
            resp.raise_for_status()

            out: BinaryIO = tempfile.NamedTemporaryFile(prefix="repo-autoindex")  # type: ignore
            async for chunk in resp.content:
                out.write(chunk)
            out.flush()
            out.seek(0)

            # Deal with the non-ideal content negotiation
            # for certain storage backends.
            if url.endswith(".gz") and resp.content_type in (
                "application/x-gzip",
                "application/octet-stream",
            ):
                out = gzip.GzipFile(fileobj=out)  # type: ignore

            return out

    return get_content_with_session


def wrapped_fetcher(fetcher: Fetcher) -> IOFetcher:
    # wraps a fetcher as passed in by the caller into an internal
    # fetcher enforcing certain behaviors:
    #
    # - wraps all exceptions in FetcherError
    #
    # - adapts 'str' outputs into io streams
    #
    async def new_fetcher(url: str) -> Optional[BinaryIO]:
        try:
            out = await fetcher(url)
            if isinstance(out, str):
                out = io.BytesIO(out.encode())
            return out
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

            - if the fetcher can retrieve the requested content, it must return the
              content at the given URL as a file-like object.

              Returning a ``str`` is also possible, but not recommended since it
              requires loading an entire file into memory at once, and some
              repositories contain very large files.

              Note that decompressing compressed files (such as bzipped XML in
              yum repositories) is the responsibility of the fetcher.

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

    fetcher = wrapped_fetcher(fetcher)

    try:
        for repo_type in REPO_TYPES:
            repo = await repo_type.probe(fetcher, url)
            if repo:
                async for page in repo.render_index(
                    index_href_suffix=index_href_suffix
                ):
                    yield page
                break
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
