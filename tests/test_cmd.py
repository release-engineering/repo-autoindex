import pathlib
import asyncio
import logging
from collections.abc import Callable, Awaitable

import pytest

from aiohttp import web, test_utils

from repo_autoindex._impl.cmd import entrypoint


THIS_DIR = pathlib.Path(__file__).parent


class CommandTester:
    def __init__(self, monkeypatch: pytest.MonkeyPatch):
        self.monkeypatch = monkeypatch

    async def __call__(self, url: str):
        entrypoint_coro = []

        def fake_run(coro):
            assert asyncio.iscoroutine(coro)
            entrypoint_coro.append(coro)

        self.monkeypatch.setattr("asyncio.run", fake_run)

        app = web.Application()
        app.add_routes([web.static("/", THIS_DIR)])

        async with test_utils.TestServer(app) as server:
            repo_url = server.make_url(url + "//")
            self.monkeypatch.setattr("sys.argv", ["repo-autoindex", str(repo_url)])

            entrypoint()

            assert entrypoint_coro
            await entrypoint_coro[0]


@pytest.fixture
def tester(monkeypatch: pytest.MonkeyPatch) -> CommandTester:
    return CommandTester(monkeypatch)


async def test_command_yum(
    monkeypatch: pytest.MonkeyPatch, tester: CommandTester, tmp_path: pathlib.Path
):
    """Run the repo-autoindex command against a sample yum repo and check the generated index."""
    monkeypatch.chdir(tmp_path)

    await tester("/sample_repo")

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


async def test_command_pulp(
    monkeypatch: pytest.MonkeyPatch, tester: CommandTester, tmp_path: pathlib.Path
):
    """Run the repo-autoindex command against a sample pulp file repo and check the generated index."""
    monkeypatch.chdir(tmp_path)

    await tester("/sample_pulp_repo")

    # It should have written an index file
    index_toplevel = tmp_path.joinpath("index.html")
    assert index_toplevel.exists()

    # Simple sanity check of some expected content
    toplevel = index_toplevel.read_text()

    assert '<a href="file2.qcow2">file2.qcow2</a>' in toplevel


async def test_command_no_content(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    tester: CommandTester,
    caplog: pytest.LogCaptureFixture,
):
    """Run the repo-autoindex command against an empty repo and verify nothing is written."""

    caplog.set_level(logging.INFO)

    monkeypatch.chdir(tmp_path)

    await tester("/some-nonexistent-dir")

    # It should not have written any index.html
    index_toplevel = tmp_path.joinpath("index.html")
    assert not index_toplevel.exists()

    # It should have mentioned that there was no content
    assert "No indexable content found" in caplog.text
