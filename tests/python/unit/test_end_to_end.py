"""End-to-end tests for slobac_tools.taxonomy_index.regenerate."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from slobac_tools.taxonomy_index import TaxonomyIndexError, regenerate


def _stage_mini_taxonomy(fixtures_dir: Path, tmp_path: Path) -> tuple[Path, Path, Path]:
    """Copy the mini_taxonomy fixture into tmp_path so we can mutate it.

    Returns ``(taxonomy_dir, readme_target, skill_target)``.
    """
    src = fixtures_dir / "mini_taxonomy"
    taxonomy_dir = tmp_path / "taxonomy"
    shutil.copytree(src, taxonomy_dir)

    skill_target = tmp_path / "SKILL.md"
    skill_target.write_text(
        "# Skill\n"
        "\n"
        "Preamble.\n"
        "\n"
        "<!-- BEGIN: taxonomy-index -->\n"
        "<!-- END: taxonomy-index -->\n"
        "\n"
        "Trailing.\n"
    )

    readme_target = taxonomy_dir / "README.md"
    return taxonomy_dir, readme_target, skill_target


def test_regenerate_writes_both_targets(fixtures_dir: Path, tmp_path: Path) -> None:
    taxonomy_dir, readme_target, skill_target = _stage_mini_taxonomy(
        fixtures_dir, tmp_path
    )
    regenerate(
        taxonomy_dir,
        targets=[(readme_target, "readme"), (skill_target, "skill")],
    )

    readme_text = readme_target.read_text()
    skill_text = skill_target.read_text()

    # Severity-desc + alpha order: Critical(tautology), High(deliverable), Medium(conditional), Low(rotten).
    for target_text in (readme_text, skill_text):
        ttp = target_text.find("tautology-theatre")
        df = target_text.find("deliverable-fossils")
        cl = target_text.find("conditional-logic")
        rg = target_text.find("rotten-green")
        assert -1 < ttp < df < cl < rg

    assert "[`tautology-theatre`](./tautology-theatre.md)" in readme_text
    assert (
        "[`tautology-theatre`](references/docs/taxonomy/tautology-theatre.md)"
        in skill_text
    )

    # Surrounding prose must survive untouched.
    assert "Trailing prose that must not change." in readme_text
    assert "Trailing.\n" in skill_text


def test_regenerate_is_idempotent(fixtures_dir: Path, tmp_path: Path) -> None:
    taxonomy_dir, readme_target, skill_target = _stage_mini_taxonomy(
        fixtures_dir, tmp_path
    )
    regenerate(
        taxonomy_dir,
        targets=[(readme_target, "readme"), (skill_target, "skill")],
    )
    first_readme = readme_target.read_text()
    first_skill = skill_target.read_text()

    regenerate(
        taxonomy_dir,
        targets=[(readme_target, "readme"), (skill_target, "skill")],
    )
    assert readme_target.read_text() == first_readme
    assert skill_target.read_text() == first_skill


def test_regenerate_skips_readme_in_taxonomy_dir(
    fixtures_dir: Path, tmp_path: Path
) -> None:
    taxonomy_dir, readme_target, skill_target = _stage_mini_taxonomy(
        fixtures_dir, tmp_path
    )
    regenerate(
        taxonomy_dir,
        targets=[(readme_target, "readme"), (skill_target, "skill")],
    )
    # README.md is *both* target and member of taxonomy_dir; verify the
    # generator didn't try to parse it as an entry (which would have raised
    # TaxonomyIndexError because README.md has no canonical header table)
    # AND didn't emit a row linking to README.md.
    text = readme_target.read_text()
    assert "[`README`]" not in text
    assert "[`readme`]" not in text


def test_regenerate_raises_on_unparseable_entry_file(
    fixtures_dir: Path, tmp_path: Path
) -> None:
    taxonomy_dir, readme_target, skill_target = _stage_mini_taxonomy(
        fixtures_dir, tmp_path
    )
    (taxonomy_dir / "broken-entry.md").write_text("# Broken\n\nNo header table.\n")
    with pytest.raises(TaxonomyIndexError):
        regenerate(
            taxonomy_dir,
            targets=[(readme_target, "readme"), (skill_target, "skill")],
        )
