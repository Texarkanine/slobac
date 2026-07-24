"""Contract tests for skills.sh / ``npx skills`` install surface.

Locks the Agent Skills discovery shape (SKILL.md frontmatter + sidecar dirs)
and the documented ``npx skills add`` install path in using-slobac.md, while
preserving the existing marketplace install path.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = REPO_ROOT / "skills" / "slobac-audit"
SKILL_MD = SKILL_ROOT / "SKILL.md"
USING_SLOBAC = SKILL_ROOT / "references" / "docs" / "using-slobac.md"


def _parse_simple_frontmatter(text: str) -> dict[str, str]:
    """Parse top-level scalar YAML keys from a SKILL.md frontmatter block.

    Only handles the flat ``key: value`` / folded ``key: >`` shapes this repo
    uses. Not a general YAML parser.
    """
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("SKILL.md frontmatter is not closed")
    block = text[4:end]
    fields: dict[str, str] = {}
    current_key: str | None = None
    current_parts: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_parts
        if current_key is None:
            return
        fields[current_key] = " ".join(part.strip() for part in current_parts).strip()
        current_key = None
        current_parts = []

    for line in block.splitlines():
        if not line.strip():
            continue
        if current_key is not None and (line.startswith(" ") or line.startswith("\t")):
            current_parts.append(line.strip())
            continue
        flush()
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest in {">", "|"}:
            current_key = key
            current_parts = []
        else:
            fields[key] = rest.strip("\"'")
    flush()
    return fields


def test_skill_frontmatter_has_name_and_description() -> None:
    """B1: SKILL.md YAML frontmatter exposes non-empty name and description."""
    fields = _parse_simple_frontmatter(SKILL_MD.read_text(encoding="utf-8"))
    assert fields.get("name"), "SKILL.md frontmatter missing non-empty name"
    assert fields.get("description"), "SKILL.md frontmatter missing non-empty description"


def test_skill_root_ships_references_and_licenses() -> None:
    """B2: skill root includes references/ and LICENSES/ for full-dir installs."""
    assert SKILL_MD.is_file()
    assert (SKILL_ROOT / "references").is_dir()
    assert (SKILL_ROOT / "LICENSES").is_dir()


def test_using_slobac_documents_npx_skills_add() -> None:
    """B3: using-slobac.md documents npx skills add for Texarkanine/slobac."""
    text = USING_SLOBAC.read_text(encoding="utf-8")
    assert "npx skills add" in text
    assert "Texarkanine/slobac" in text


def test_using_slobac_preserves_marketplace_install_path() -> None:
    """Edge: using-slobac.md still documents the txrk9-agent-plugins path."""
    text = USING_SLOBAC.read_text(encoding="utf-8")
    assert "txrk9-agent-plugins" in text
