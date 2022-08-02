from repo_autoindex._impl.template import TemplateContext
from repo_autoindex._impl.base import IndexEntry


def test_long_string_elision():
    """Entries with a very long name will trigger elision."""
    ctx = TemplateContext(max_text_length=6)

    rendered = ctx.render_index(
        index_entries=[
            IndexEntry(href="href1", text="123456"),
            IndexEntry(href="some longer href", text="1234567"),
        ]
    )

    # Text which fits in the limit should be left alone
    assert '<a href="href1">123456</a>' in rendered

    # Text which exceeds the limit should trigger elision (but href should
    # still be left alone)
    assert '<a href="some longer href">123...</a>' in rendered
