#!/usr/bin/env python3
"""CLI entry point for the SLOBAC taxonomy-index generator.

Run from the repo root:

    uv run python scripts/gen_taxonomy_index.py

Re-emits the slug / severity / detection-scope index between sentinel
markers in two locations:

* ``skills/slobac-audit/SKILL.md``
* ``skills/slobac-audit/references/docs/taxonomy/README.md``

Sole source of truth is the per-entry canonical header table in every
``skills/slobac-audit/references/docs/taxonomy/<slug>.md``.

Idempotent: a second run against an unchanged repo produces zero file diff.
This is what the CI drift-check job relies on.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Make the in-repo `slobac_tools` package importable when running as a script
# without installing the package.
sys.path.insert(0, str(REPO_ROOT))

from slobac_tools.taxonomy_index import regenerate  # noqa: E402


TAXONOMY_DIR = REPO_ROOT / "skills" / "slobac-audit" / "references" / "docs" / "taxonomy"
SKILL_MD = REPO_ROOT / "skills" / "slobac-audit" / "SKILL.md"
TAXONOMY_README = TAXONOMY_DIR / "README.md"


def main() -> int:
    regenerate(
        TAXONOMY_DIR,
        targets=[
            (TAXONOMY_README, "readme"),
            (SKILL_MD, "skill"),
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
