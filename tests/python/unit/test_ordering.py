"""Tests for slobac_tools.taxonomy_index.order_entries."""

from __future__ import annotations

from slobac_tools.taxonomy_index import TaxonomyEntry, order_entries


def _entry(slug: str, severity: str) -> TaxonomyEntry:
    return TaxonomyEntry(slug=slug, severity=severity, scopes=("per-test",))


def test_order_groups_by_severity_descending() -> None:
    entries = [
        _entry("rotten-green", "Low"),
        _entry("vacuous-assertion", "High"),
        _entry("conditional-logic", "Medium"),
        _entry("tautology-theatre", "Critical"),
    ]
    ordered = order_entries(entries)
    assert [e.severity for e in ordered] == ["Critical", "High", "Medium", "Low"]


def test_order_alphabetical_within_severity() -> None:
    entries = [
        _entry("vacuous-assertion", "High"),
        _entry("deliverable-fossils", "High"),
        _entry("over-specified-mock", "High"),
    ]
    ordered = order_entries(entries)
    assert [e.slug for e in ordered] == [
        "deliverable-fossils",
        "over-specified-mock",
        "vacuous-assertion",
    ]


def test_order_stable_for_already_sorted_input() -> None:
    sorted_entries = [
        _entry("tautology-theatre", "Critical"),
        _entry("deliverable-fossils", "High"),
        _entry("vacuous-assertion", "High"),
        _entry("conditional-logic", "Medium"),
        _entry("rotten-green", "Low"),
    ]
    assert order_entries(sorted_entries) == sorted_entries
