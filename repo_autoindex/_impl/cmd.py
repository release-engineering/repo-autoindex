import argparse
import asyncio
import logging
import os
from typing import Any

from repo_autoindex import autoindex

LOG = logging.getLogger("repo-autoindex")


async def dump_autoindices(args: argparse.Namespace) -> None:
    index_filename = args.index_filename
    wrote_any = False
    async for index in autoindex(args.url, index_href_suffix=index_filename):
        os.makedirs(index.relative_dir or ".", exist_ok=True)
        output = os.path.join(index.relative_dir or ".", index_filename)
        with open(output, "w") as f:
            f.write(index.content)
        LOG.info("Wrote %s", output)
        wrote_any = True

    if not wrote_any:
        LOG.info("No indexable content found at %s", args.url)


def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate indexes for a repository accessed via HTTP(S)"
    )
    parser.add_argument("url", help="Base URL of repository to be indexed")
    parser.add_argument(
        "--index-filename",
        metavar="FILENAME",
        default="index.html",
        help="Basename of output file(s)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable verbose logging")
    return parser


def entrypoint() -> None:
    parser = argparser()
    p = parser.parse_args()

    kwargs: dict[str, Any] = {"level": logging.DEBUG if p.debug else logging.INFO}
    if not p.debug:
        kwargs["format"] = "%(message)s"

    logging.basicConfig(**kwargs)
    asyncio.run(dump_autoindices(p))
