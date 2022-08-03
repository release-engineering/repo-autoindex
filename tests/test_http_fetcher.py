import gzip
import pytest
from aiohttp import web
from repo_autoindex._impl.api import http_fetcher


class FakeReader:
    def __init__(self, body: bytes):
        self.body = body

    async def read(self):
        return self.body


class FakeResponse:
    def __init__(self, body: bytes, content_type: str):
        self.body = body
        self.content_type = content_type

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass

    def raise_for_status(self):
        pass

    @property
    def content(self):
        return FakeReader(self.body)


class FakeSession:
    def __init__(self, body: bytes, content_type: str):
        self.body = body
        self.content_type = content_type

    def get(self, url: str) -> FakeResponse:
        return FakeResponse(self.body, self.content_type)


@pytest.mark.parametrize(
    "content_type", ["application/x-gzip", "application/octet-stream"]
)
async def test_http_fetcher_decompresses(content_type: str):
    """http_fetcher will decompress certain responses."""
    text = "some text"
    compressed = gzip.compress(text.encode("utf-8"))

    session = FakeSession(body=compressed, content_type=content_type)
    fetcher = http_fetcher(session)

    response = await fetcher("/some/path.gz")
    assert response == text
