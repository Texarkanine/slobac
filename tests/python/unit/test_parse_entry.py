"""Tests for slobac_tools.taxonomy_index.parse_entry.

Covers happy paths (single + multi scope) and the structured-error contract
for each documented malformed-input case.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from slobac_tools.taxonomy_index import (
    TaxonomyEntry,
    TaxonomyIndexError,
    parse_entry,
)


def test_parse_entry_single_scope(fixtures_dir: Path) -> None:
    entry = parse_entry(fixtures_dir / "valid_single_scope.md")
    assert entry == TaxonomyEntry(
        slug="naming-lies",
        severity="Medium",
        scopes=("per-test",),
    )


def test_parse_entry_multi_scope(fixtures_dir: Path) -> None:
    entry = parse_entry(fixtures_dir / "valid_multi_scope.md")
    assert entry == TaxonomyEntry(
        slug="deliverable-fossils",
        severity="High",
        scopes=("per-test", "cross-suite"),
    )


def test_parse_entry_missing_header_table(tmp_path: Path) -> None:
    f = tmp_path / "broken.md"
    f.write_text("# Just a heading\n\nNo header table here.\n")
    with pytest.raises(TaxonomyIndexError) as exc_info:
        parse_entry(f)
    assert exc_info.value.field == "header"
    assert exc_info.value.file_path == f


def test_parse_entry_unknown_severity(tmp_path: Path) -> None:
    f = tmp_path / "bad-sev.md"
    f.write_text(
        "# Bad Severity\n\n"
        "| Slug | Severity | Detection Scope | Protects |\n"
        "|---|---|---|---|\n"
        "| `bad-sev` | Spicy | per-test | [Understandable](x.md) |\n"
    )
    with pytest.raises(TaxonomyIndexError) as exc_info:
        parse_entry(f)
    assert exc_info.value.field == "severity"


def test_parse_entry_unknown_scope(tmp_path: Path) -> None:
    f = tmp_path / "bad-scope.md"
    f.write_text(
        "# Bad Scope\n\n"
        "| Slug | Severity | Detection Scope | Protects |\n"
        "|---|---|---|---|\n"
        "| `bad-scope` | Medium | per-galaxy | [Understandable](x.md) |\n"
    )
    with pytest.raises(TaxonomyIndexError) as exc_info:
        parse_entry(f)
    assert exc_info.value.field == "scope"


def test_parse_entry_wrong_shape_row(tmp_path: Path) -> None:
    f = tmp_path / "bad-shape.md"
    f.write_text(
        "# Bad Shape\n\n"
        "| Slug | Severity | Detection Scope | Protects |\n"
        "|---|---|---|---|\n"
        "| `bad-shape` | Medium | per-test |\n"
    )
    with pytest.raises(TaxonomyIndexError) as exc_info:
        parse_entry(f)
    assert exc_info.value.field == "header"
