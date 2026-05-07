"""Tests for slobac_tools.taxonomy_index.replace_between_sentinels."""

from __future__ import annotations

import pytest

from slobac_tools.taxonomy_index import (
    TaxonomyIndexError,
    replace_between_sentinels,
)


_TARGET_TEMPLATE = (
    "# Title\n"
    "\n"
    "Preamble paragraph that must not change.\n"
    "\n"
    "<!-- BEGIN: taxonomy-index -->\n"
    "OLD CONTENT\n"
    "<!-- END: taxonomy-index -->\n"
    "\n"
    "Trailing paragraph that must not change.\n"
)


def test_replace_between_sentinels_replaces_only_bracketed_region() -> None:
    new_content = "| header |\n|---|\n| row |\n"
    output = replace_between_sentinels(_TARGET_TEMPLATE, new_content)
    assert "OLD CONTENT" not in output
    assert "Preamble paragraph that must not change.\n" in output
    assert "Trailing paragraph that must not change.\n" in output
    assert "<!-- BEGIN: taxonomy-index -->" in output
    assert "<!-- END: taxonomy-index -->" in output
    assert "| header |" in output


def test_replace_between_sentinels_idempotent() -> None:
    new_content = "| header |\n|---|\n| row |\n"
    once = replace_between_sentinels(_TARGET_TEMPLATE, new_content)
    twice = replace_between_sentinels(once, new_content)
    assert once == twice


def test_replace_between_sentinels_missing_begin_marker_raises() -> None:
    text = "<!-- END: taxonomy-index -->\n"
    with pytest.raises(TaxonomyIndexError) as exc_info:
        replace_between_sentinels(text, "X")
    assert exc_info.value.field == "marker"


def test_replace_between_sentinels_missing_end_marker_raises() -> None:
    text = "<!-- BEGIN: taxonomy-index -->\n"
    with pytest.raises(TaxonomyIndexError) as exc_info:
        replace_between_sentinels(text, "X")
    assert exc_info.value.field == "marker"


def test_replace_between_sentinels_duplicate_begin_marker_raises() -> None:
    text = (
        "<!-- BEGIN: taxonomy-index -->\nfoo\n<!-- END: taxonomy-index -->\n"
        "<!-- BEGIN: taxonomy-index -->\nbar\n<!-- END: taxonomy-index -->\n"
    )
    with pytest.raises(TaxonomyIndexError) as exc_info:
        replace_between_sentinels(text, "X")
    assert exc_info.value.field == "marker"


def test_replace_between_sentinels_inverted_markers_raises() -> None:
    """
    When END sentinel appears before BEGIN sentinel in the document, the
    function must raise TaxonomyIndexError(field="marker") rather than
    leaking a raw ValueError from str.index().
    """
    text = (
        "<!-- END: taxonomy-index -->\n"
        "content\n"
        "<!-- BEGIN: taxonomy-index -->\n"
    )
    with pytest.raises(TaxonomyIndexError) as exc_info:
        replace_between_sentinels(text, "new content")
    assert exc_info.value.field == "marker"
