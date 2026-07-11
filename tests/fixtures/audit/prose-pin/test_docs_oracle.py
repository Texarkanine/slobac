"""Docs / skill prose oracle tests.

Fixture for the SLOBAC audit's `prose-pin` scenario. Two planted positives
assert on the suite's own committed docs/skills; two negative controls cover
fitness-function greps and prose-as-SUT temp fixtures.
"""

from __future__ import annotations

from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parent
ONBOARDING_DOC = FIXTURE_ROOT / "docs" / "onboarding.md"
WRAPPER_SKILL = FIXTURE_ROOT / "skills" / "demo-wrapper" / "SKILL.md"


# --- positive 1: keyword checklist on committed docs.                       -
#     Green means the phrases still appear in onboarding.md — not that the -
#     documented procedure still works. Editorial rewrites fail CI.        -

def test_onboarding_doc_mentions_required_phrases():
    text = ONBOARDING_DOC.read_text(encoding="utf-8")
    assert "install the CLI" in text
    assert "run the smoke check" in text
    assert "report failures upstream" in text


# --- positive 2: feature-mention + order pin on committed SKILL.md.         -
#     Pins that flags are *mentioned* and that one phrase appears before   -
#     another in the file bytes — change-detectors on prose, not behavior. -

def test_skill_mentions_detail_raw_before_format_json():
    text = WRAPPER_SKILL.read_text(encoding="utf-8")
    assert "--detail raw" in text
    assert "--format json" in text
    assert text.index("--detail raw") < text.index("--format json")


# --- negative control: architectural fitness-function forbidden-token scan. -
#     The wrapper SKILL.md is the agent-executable contract. Leaking raw   -
#     Python invocation tokens into that prose is an interface regression  -
#     (ArchUnit-style negative rule / evolutionary-architecture fitness    -
#     function), not a keyword checklist.                                  -

def test_wrapper_skill_forbids_raw_python_invocation():
    # Architectural invariant: agent-facing wrapper must not expose raw
    # `uv run` / PYTHONPATH / `python -m` invocation — agents must use the
    # on-path shim. Documented fitness function, not a prose keyword pin.
    text = WRAPPER_SKILL.read_text(encoding="utf-8")
    assert "uv run" not in text
    assert "PYTHONPATH=" not in text
    assert "python -m" not in text


# --- negative control: prose-as-SUT (temp skill fixture is product I/O).    -
#     The markdown under test is written into a temp dir and round-tripped -
#     by a convert helper — it is not the repo's committed agent prose.    -

def _emit_skill_front_matter(name: str, description: str) -> str:
    """Minimal SUT stand-in: emit a SKILL.md body from structured fields."""
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        f"# {name}\n"
    )


def test_skill_fixture_roundtrip_preserves_name_front_matter(tmp_path: Path):
    skill_path = tmp_path / "SKILL.md"
    skill_path.write_text(
        _emit_skill_front_matter("temp-skill", "Temporary fixture skill."),
        encoding="utf-8",
    )
    emitted = skill_path.read_text(encoding="utf-8")
    assert emitted.startswith("---\n")
    assert "name: temp-skill" in emitted
    assert "description: Temporary fixture skill." in emitted
