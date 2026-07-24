"""Contract tests for skills.sh / ``npx skills`` install surface.

Locks the Agent Skills discovery shape (SKILL.md frontmatter + sidecar dirs)
and the documented ``npx skills add`` install path in using-slobac.md, while
preserving the existing marketplace install path.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = REPO_ROOT / "skills" / "slobac-audit"
SKILL_MD = SKILL_ROOT / "SKILL.md"
USING_SLOBAC = SKILL_ROOT / "references" / "docs" / "using-slobac.md"


def test_skill_frontmatter_has_name_and_description() -> None:
    """B1: SKILL.md YAML frontmatter exposes non-empty name and description."""
    text = SKILL_MD.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    assert re.search(r"(?m)^name:\s*\S", text), "SKILL.md frontmatter missing non-empty name"
    assert re.search(
        r"(?m)^description:\s*\S", text
    ), "SKILL.md frontmatter missing non-empty description"


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
