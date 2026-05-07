"""Tests for slobac_tools.taxonomy_index.render_table."""

from __future__ import annotations

from slobac_tools.taxonomy_index import TaxonomyEntry, render_table


_ENTRIES = [
    TaxonomyEntry(slug="tautology-theatre", severity="Critical", scopes=("per-test",)),
    TaxonomyEntry(
        slug="deliverable-fossils",
        severity="High",
        scopes=("per-test", "cross-suite"),
    ),
]


def test_render_readme_link_target() -> None:
    output = render_table(_ENTRIES, link_target="readme")
    assert "[`tautology-theatre`](./tautology-theatre.md)" in output
    assert "[`deliverable-fossils`](./deliverable-fossils.md)" in output


def test_render_skill_link_target() -> None:
    output = render_table(_ENTRIES, link_target="skill")
    assert (
        "[`tautology-theatre`](references/docs/taxonomy/tautology-theatre.md)" in output
    )
    assert (
        "[`deliverable-fossils`](references/docs/taxonomy/deliverable-fossils.md)"
        in output
    )


def test_render_multi_scope_preserves_comma_joined_string() -> None:
    output = render_table(_ENTRIES, link_target="readme")
    assert "| per-test, cross-suite |" in output
    assert "| per-test |" in output


def test_render_emits_three_column_table_with_header_and_separator() -> None:
    output = render_table(_ENTRIES, link_target="readme")
    lines = [line for line in output.splitlines() if line.strip()]
    assert lines[0] == "| Slug | Severity | Detection Scope |"
    assert lines[1] == "|---|---|---|"
    assert len(lines) == 2 + len(_ENTRIES)
