"""Mixed-smell tests.

Fixture for the SLOBAC audit's scope-honoring scenario. Contains at least one
test that exhibits both smells simultaneously; the audit must flag it under
each in-scope smell without silently deduplicating the underlying rationale.
"""

from __future__ import annotations


class Config:
    def __init__(self) -> None:
        self._values: dict[str, object] = {}

    def set(self, key: str, value: object) -> None:
        self._values[key] = value

    def get(self, key: str, default: object | None = None) -> object | None:
        return self._values.get(key, default)

    def keys(self) -> list[str]:
        return sorted(self._values.keys())


def _seeded_config() -> Config:
    cfg = Config()
    cfg.set("theme", "dark")
    cfg.set("tab_size", 4)
    return cfg


# --- pure fossil: grouping and title are sprint-shaped; body is a clean    -
#     claim about the get/default contract.                                  -

class TestM2ConfigRefactor:
    def test_get_returns_default_when_key_missing_per_m2_spec(self):
        cfg = _seeded_config()
        assert cfg.get("missing", "fallback") == "fallback"


# --- pure naming-lie: title claims "theme is case-insensitive"; body does  -
#     a plain equality check that depends on the caller passing the exact  -
#     case. Rename path: the body contract is "round-trip a value".        -

def test_theme_setting_is_case_insensitive():
    cfg = _seeded_config()
    cfg.set("theme", "dark")
    assert cfg.get("theme") == "dark"


# --- BOTH smells: ticket prefix in title (fossil) AND title claims ANSI    -
#     color support, body does no color check (naming-lie). Audit must     -
#     flag under each in-scope smell. The two findings share a common      -
#     test location but must not collapse into one generic "this test is   -
#     bad" line — each finding names a distinct remediation.                -

def test_slob_99_uses_cyan_for_error_messages():
    cfg = _seeded_config()
    cfg.set("error_prefix", "ERROR: ")
    assert cfg.get("error_prefix") == "ERROR: "


# --- clean: behavior-encoded name, body verifies the claim directly.       -
#     Audit must NOT flag this under either smell at any scope.             -

def test_keys_returns_entries_in_sorted_order():
    cfg = Config()
    cfg.set("zebra", 1)
    cfg.set("apple", 2)
    cfg.set("mango", 3)
    assert cfg.keys() == ["apple", "mango", "zebra"]
