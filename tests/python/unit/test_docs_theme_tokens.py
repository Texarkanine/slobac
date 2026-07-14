"""Contract tests for the ProperDocs Material creamy/papery theme tokens."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
PROPERDOCS_YAML = REPO_ROOT / "properdocs.yaml"
EXTRA_CSS = (
    REPO_ROOT
    / "skills"
    / "slobac-audit"
    / "references"
    / "docs"
    / "stylesheets"
    / "extra.css"
)

# SLOBAC-original paper/ember tokens (open warm-scale inspired; not Anthropic clones).
LIGHT_BG = "#f6f0e4"
LIGHT_FG = "#1f1a14"
LIGHT_PRIMARY = "#b45309"
LIGHT_ACCENT = "#c2410c"
LIGHT_CODE_BG = "#ebe4d4"
LIGHT_FOOTER_BG = "#2a241c"

DARK_BG = "#1c1914"
DARK_FG = "#f0e6d4"
DARK_PRIMARY = "#f59e0b"
DARK_ACCENT = "#fb923c"
DARK_LINK = "#fb923c"
DARK_CODE_BG = "#2a251c"
DARK_FOOTER_BG = "#12100c"


@pytest.fixture(scope="module")
def properdocs_text() -> str:
    return PROPERDOCS_YAML.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def extra_css_text() -> str:
    assert EXTRA_CSS.is_file(), f"missing theme stylesheet: {EXTRA_CSS}"
    text = EXTRA_CSS.read_text(encoding="utf-8")
    assert text.strip(), "theme stylesheet must not be empty"
    return text


def _scheme_block(css: str, scheme: str) -> str:
    """Return the CSS body for ``[data-md-color-scheme="{scheme}"] { ... }``."""
    needle = f'[data-md-color-scheme="{scheme}"]'
    start = css.find(needle)
    assert start != -1, f"missing scheme selector {needle}"
    brace = css.find("{", start)
    assert brace != -1, f"missing opening brace for {needle}"
    depth = 0
    for i, ch in enumerate(css[brace:], start=brace):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return css[brace + 1 : i]
    raise AssertionError(f"unclosed scheme block for {needle}")


def _assert_var(block: str, name: str, value: str) -> None:
    assert f"{name}:" in block, f"missing {name} in scheme block"
    compact = re.sub(r"\s+", "", block).lower()
    assert f"{name}:{value}".lower() in compact, (
        f"expected {name}: {value} in scheme block"
    )


def test_palette_uses_custom_primary_and_accent(properdocs_text: str) -> None:
    assert re.search(r"^\s*primary:\s*indigo\s*$", properdocs_text, re.M) is None
    assert re.search(r"^\s*accent:\s*indigo\s*$", properdocs_text, re.M) is None
    custom_primary = re.findall(r"^\s*primary:\s*custom\s*$", properdocs_text, re.M)
    custom_accent = re.findall(r"^\s*accent:\s*custom\s*$", properdocs_text, re.M)
    assert len(custom_primary) >= 2
    assert len(custom_accent) >= 2


def test_palette_retains_light_and_dark_toggles(properdocs_text: str) -> None:
    assert re.search(r"^\s*scheme:\s*default\s*$", properdocs_text, re.M)
    assert re.search(r"^\s*scheme:\s*slate\s*$", properdocs_text, re.M)
    assert "toggle:" in properdocs_text
    assert "material/brightness-7" in properdocs_text
    assert "material/brightness-4" in properdocs_text


def test_extra_css_registers_stylesheets_extra(properdocs_text: str) -> None:
    assert "extra_css:" in properdocs_text
    assert "stylesheets/extra.css" in properdocs_text


def test_light_scheme_paper_tokens(extra_css_text: str) -> None:
    block = _scheme_block(extra_css_text, "default")
    _assert_var(block, "--md-default-bg-color", LIGHT_BG)
    _assert_var(block, "--md-default-fg-color", LIGHT_FG)
    _assert_var(block, "--md-primary-fg-color", LIGHT_PRIMARY)
    _assert_var(block, "--md-accent-fg-color", LIGHT_ACCENT)
    _assert_var(block, "--md-code-bg-color", LIGHT_CODE_BG)
    _assert_var(block, "--md-footer-bg-color", LIGHT_FOOTER_BG)


def test_dark_scheme_ember_tokens(extra_css_text: str) -> None:
    block = _scheme_block(extra_css_text, "slate")
    _assert_var(block, "--md-default-bg-color", DARK_BG)
    _assert_var(block, "--md-default-fg-color", DARK_FG)
    _assert_var(block, "--md-primary-fg-color", DARK_PRIMARY)
    _assert_var(block, "--md-accent-fg-color", DARK_ACCENT)
    _assert_var(block, "--md-typeset-a-color", DARK_LINK)
    _assert_var(block, "--md-code-bg-color", DARK_CODE_BG)
    _assert_var(block, "--md-footer-bg-color", DARK_FOOTER_BG)
