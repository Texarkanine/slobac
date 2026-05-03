"""Engine state tests.

Fixture for the SLOBAC audit's `shared-state` scenario. These tests are not
executed by any runner; they are read by the audit skill as if they were a real
suite leaking mutable state across test boundaries.
"""

from __future__ import annotations

import pytest

ENGINE_NAME = "turbo-v2"
_engine = Engine()
_results: list[str] = []


class Engine:
    def __init__(self) -> None:
        self._items: dict[str, str] = {}

    def add(self, key: str, value: str) -> None:
        self._items[key] = value

    def remove(self, key: str) -> None:
        self._items.pop(key, None)

    def get(self, key: str) -> str | None:
        return self._items.get(key)

    def count(self) -> int:
        return len(self._items)

    @property
    def name(self) -> str:
        return ENGINE_NAME


# --- shared-state: module-level Engine mutated by multiple tests -------------

def test_add_item_persists():
    _engine.add("alpha", "first")
    _results.append("added alpha")
    assert _engine.get("alpha") == "first"


def test_remove_item_clears_entry():
    # Depends on test_add_item_persists having run first
    _engine.remove("alpha")
    assert _engine.get("alpha") is None


def test_count_reflects_additions():
    _engine.add("beta", "second")
    _engine.add("gamma", "third")
    _results.append("added beta and gamma")
    assert _engine.count() >= 2


# --- shared-state: module-level list that accumulates across tests -----------

def test_results_accumulate():
    # Only passes if earlier tests appended to _results
    assert len(_results) > 0


# --- negative example: per-test fixture creates a fresh Engine ---------------

@pytest.fixture
def fresh_engine() -> Engine:
    engine = Engine()
    engine.add("seed", "value")
    return engine


def test_isolated_operation(fresh_engine: Engine):
    """Uses a per-test fixture — no shared mutable state."""
    fresh_engine.add("local", "data")
    assert fresh_engine.count() == 2
    assert fresh_engine.get("local") == "data"


# --- negative example: reads module-level constant, does not mutate ----------

def test_read_only_access():
    """Reads ENGINE_NAME (a constant) but touches no mutable shared state."""
    assert ENGINE_NAME == "turbo-v2"
