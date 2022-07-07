import pytest

from repo_autoindex import autoindex


async def fetcher_none(url: str) -> None:
    return None


async def fetcher_error(url: str) -> None:
    raise RuntimeError("simulated error")


async def test_no_repo():
    """If Fetcher finds no content, autoindex should gracefully produce nothing."""

    entries = []
    async for entry in autoindex("https://example.com", fetcher=fetcher_none):
        entries.append(entry)

    # It should not have generated any index, nor raised an error,
    # since the fetcher returned None.
    assert not entries


async def test_error():
    """If Fetcher raises an exception, it should propagate."""

    entries = []

    # It should raise an error
    with pytest.raises(RuntimeError, match="simulated error"):
        async for entry in autoindex("https://example.com", fetcher=fetcher_error):
            entries.append(entry)

    # It should not have generated any index
    assert not entries
