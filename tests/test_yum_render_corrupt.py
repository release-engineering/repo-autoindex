from typing import Optional
import textwrap

from repo_autoindex import autoindex, ContentError

REPOMD_XML = textwrap.dedent(
    """
    <?xml version="1.0" encoding="UTF-8"?>
    <repomd xmlns="http://linux.duke.edu/metadata/repo" xmlns:rpm="http://linux.duke.edu/metadata/rpm">
    <revision>1657165688</revision>
    <data type="primary">
        <checksum type="sha256">d4888f04f95ac067af4d997d35c6d345cbe398563d777d017a3634c9ed6148cf</checksum>
        <open-checksum type="sha256">6fc4eddd4e9de89246efba3815b8a9dec9dfe168e4fd3104cc792dff908a0f62</open-checksum>
        <location href="repodata/d4888f04f95ac067af4d997d35c6d345cbe398563d777d017a3634c9ed6148cf-primary.xml.gz"/>
        <timestamp>1657165688</timestamp>
        <size>2932</size>
        <open-size>16585</open-size>
    </data>
    <data type="filelists">
        <checksum type="sha256">284769ec79daa9e0a3b0129bb6260cc6271c90c4fe02b43dfa7cdf7635fb803f</checksum>
        <open-checksum type="sha256">72f89223c8b0f6c7a2ee6ed7fbd16ee0bb395ca68260038bb3895265af84c29f</open-checksum>
        <location href="repodata/284769ec79daa9e0a3b0129bb6260cc6271c90c4fe02b43dfa7cdf7635fb803f-filelists.xml.gz"/>
        <timestamp>1657165688</timestamp>
        <size>4621</size>
        <open-size>36911</open-size>
    </data>
    <data type="other">
        <checksum type="sha256">36c2195bbee0c39ee080969abc6fd59d943c3471114cfd43c6e776ac20d7ed21</checksum>
        <open-checksum type="sha256">39f52cf295db14e863abcd7b2eede8e6c5e39ac9b2f194349459d29cd492c90f</open-checksum>
        <location href="repodata/36c2195bbee0c39ee080969abc6fd59d943c3471114cfd43c6e776ac20d7ed21-other.xml.gz"/>
        <timestamp>1657165688</timestamp>
        <size>1408</size>
        <open-size>8432</open-size>
    </data>
    <data type="primary_db">
        <checksum type="sha256">55e6bfd00e889c5c1f9a3c9fb35a660158bc5d975ae082d434f3cf81cc2c0c21</checksum>
        <open-checksum type="sha256">b2692c49d1d98d68e764e29108d8a81a3dfd9e04fa7665115853a029396d118d</open-checksum>
        <location href="repodata/55e6bfd00e889c5c1f9a3c9fb35a660158bc5d975ae082d434f3cf81cc2c0c21-primary.sqlite.bz2"/>
        <timestamp>1657165688</timestamp>
        <size>7609</size>
        <open-size>114688</open-size>
        <database_version>10</database_version>
    </data>
    <data type="filelists_db">
        <checksum type="sha256">de63a509812c37f7736fcef0b79e9c55dfe67a2d77006f74fdc442935103e9e6</checksum>
        <open-checksum type="sha256">40eb5d53fe547c98d470813256c9bfc8a239b13697d8eb824a1485c9e186a0e3</open-checksum>
        <location href="repodata/de63a509812c37f7736fcef0b79e9c55dfe67a2d77006f74fdc442935103e9e6-filelists.sqlite.bz2"/>
        <timestamp>1657165688</timestamp>
        <size>10323</size>
        <open-size>65536</open-size>
        <database_version>10</database_version>
    </data>
    <data type="other_db">
        <checksum type="sha256">9aa39b62df200cb3784dea24092d0c1c686afff0cd0990c2ec7a61afe8896e1c</checksum>
        <open-checksum type="sha256">3e5cefb10ce805b827e12ca3b4839bba873dc9403fd92b60a364bf6f312bd972</open-checksum>
        <location href="repodata/9aa39b62df200cb3784dea24092d0c1c686afff0cd0990c2ec7a61afe8896e1c-other.sqlite.bz2"/>
        <timestamp>1657165688</timestamp>
        <size>2758</size>
        <open-size>32768</open-size>
        <database_version>10</database_version>
    </data>
    </repomd>
"""
).strip()

PRIMARY_XML = textwrap.dedent(
    """
<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="http://linux.duke.edu/metadata/common" xmlns:rpm="http://linux.duke.edu/metadata/rpm" packages="5">
<package type="rpm">
  <name>
"""
).strip()


class StaticFetcher:
    def __init__(self):
        self.content: dict[str, str] = {}

    async def __call__(self, url: str) -> Optional[str]:
        return self.content.get(url)


async def test_corrupt_repodata():
    fetcher = StaticFetcher()

    fetcher.content["https://example.com/repodata/repomd.xml"] = REPOMD_XML
    fetcher.content[
        "https://example.com/repodata/d4888f04f95ac067af4d997d35c6d345cbe398563d777d017a3634c9ed6148cf-primary.xml.gz"
    ] = PRIMARY_XML

    error = None
    try:
        async for _ in autoindex("https://example.com", fetcher=fetcher):
            pass
    except ContentError as exc:
        error = exc

    # It should have raised a ContentError
    assert error

    # It should summarize
    assert "Invalid content found at https://example.com" in str(error)

    # We don't want the test to depend on precise details, but it should have
    # some cause coming from the XML parser
    assert "xml" in error.__cause__.__module__


async def test_missing_primary():
    fetcher = StaticFetcher()

    fetcher.content["https://example.com/repodata/repomd.xml"] = REPOMD_XML

    error = None
    try:
        async for _ in autoindex("https://example.com", fetcher=fetcher):
            pass
    except ContentError as exc:
        error = exc

    # It should have raised a ContentError
    assert error

    # It should state the reason
    assert (
        "missing primary XML at https://example.com/repodata/d4888f04f95ac067af4d997d35c6d345cbe398563d777d017a3634c9ed6148cf-primary.xml.gz"
        in str(error)
    )

    # This one doesn't have a separate cause as it was raised explicitly by our code
    assert not error.__cause__
