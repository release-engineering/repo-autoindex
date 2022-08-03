import pathlib
import asyncio

import pytest

from aiohttp import web, test_utils

from repo_autoindex._impl.cmd import entrypoint


THIS_DIR = pathlib.Path(__file__).parent


async def test_command(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path):
    """Run the repo-autoindex command against a sample repo and check the generated index."""

    monkeypatch.chdir(tmp_path)

    entrypoint_coro = []

    def fake_run(coro):
        assert asyncio.iscoroutine(coro)
        entrypoint_coro.append(coro)

    monkeypatch.setattr("asyncio.run", fake_run)

    app = web.Application()
    app.add_routes([web.static("/", THIS_DIR)])

    async with test_utils.TestServer(app) as server:
        repo_url = server.make_url("/sample_repo///")
        monkeypatch.setattr("sys.argv", ["repo-autoindex", str(repo_url)])

        entrypoint()

        assert entrypoint_coro
        await entrypoint_coro[0]

    # It should have written index files reproducing the structure
    index_toplevel = tmp_path.joinpath("index.html")
    index_pkgs = tmp_path.joinpath("pkgs", "index.html")
    index_w = tmp_path.joinpath("pkgs", "w", "index.html")

    assert index_toplevel.exists()
    assert index_pkgs.exists()
    assert index_w.exists()

    # Simple sanity check of some expected content
    toplevel = index_toplevel.read_text()
    pkgs = index_pkgs.read_text()
    w = index_w.read_text()

    assert '<a href="repodata/index.html">repodata/</a>' in toplevel
    assert '<a href="pkgs/index.html">pkgs/</a>' in toplevel

    assert '<a href="w/index.html">w/</a>' in pkgs

    assert '<a href="walrus-5.21-1.noarch.rpm">walrus-5.21-1.noarch.rpm</a>' in w
