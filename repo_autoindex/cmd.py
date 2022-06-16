from collections.abc import AsyncGenerator
import logging
import asyncio
import gzip
import os
import argparse

from repo_autoindex import autoindex

LOG = logging.getLogger("autoindex")


async def dump_autoindices(args):
    index_filename = args.index_filename
    async for index in autoindex(args.url, index_href_suffix=index_filename):
        os.makedirs(index.relative_dir or ".", exist_ok=True)
        output = os.path.join(index.relative_dir or ".", index_filename)
        with open(output, "w") as f:
            f.write(index.content)
        LOG.info("Wrote %s", output)


def entrypoint():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--index-filename", default="index.html")
    parser.add_argument("--debug", action="store_true")
    p = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if p.debug else logging.INFO)
    asyncio.run(dump_autoindices(p))
