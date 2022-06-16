from collections.abc import Iterable
from dataclasses import replace
import os

import jinja2

from .base import IndexEntry

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


class TemplateContext:
    def __init__(self):
        self.env = jinja2.Environment(
            autoescape=True, loader=jinja2.FileSystemLoader(TEMPLATE_DIR)
        )
        # low number is for testing - increase it later
        self.max_text_length = 200

    def render_index(
        self,
        title: str = "repository index",
        header: str = "",
        footer: str = "",
        index_entries: Iterable[IndexEntry] = (),
    ) -> str:
        return self.env.get_template("index.html.j2").render(
            title=title,
            header=header,
            footer=footer,
            index_entries=self.__with_padded_text(index_entries),
        )

    def __with_padded_text(self, entries: Iterable[IndexEntry]) -> Iterable[IndexEntry]:
        max_len = 0
        for entry in entries:
            entry_len = min(len(entry.text), self.max_text_length)
            max_len = max(entry_len, max_len)

        out = []
        for entry in entries:
            if len(entry.text) >= (self.max_text_length - 3):
                entry = replace(entry, text=entry.text[:-3] + "...")

            # pad right so they all have the same length
            padcount = max_len - len(entry.text)
            entry = replace(entry, padding=" " * padcount)
            out.append(entry)

        return out
