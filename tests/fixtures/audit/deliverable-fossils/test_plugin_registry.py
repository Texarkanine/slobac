"""Plugin registry tests.

Fixture for the SLOBAC audit's `deliverable-fossils` scenario. These tests are not
executed by any runner; they are read by the audit skill as if they were a real
suite carrying sprint-shaped naming rot.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Plugin:
    id: str
    name: str


class PluginEngine:
    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        self._plugins[plugin.id] = plugin

    def get_plugin(self, plugin_id: str) -> Plugin | None:
        return self._plugins.get(plugin_id)

    def list_plugins(self) -> list[Plugin]:
        return list(self._plugins.values())


def _seed() -> PluginEngine:
    engine = PluginEngine()
    engine.register(Plugin(id="cursor", name="Cursor"))
    engine.register(Plugin(id="claude-code", name="Claude Code"))
    return engine


# --- fossil: describe/it history, grouping names a refactor -----------------

class TestSourceTrackingRefactor:
    """Grouping references a long-gone refactor rather than a product capability."""

    def test_should_return_the_plugin_via_get_plugin_after_source_tracking_refactor(self):
        engine = _seed()
        plugin = engine.get_plugin("cursor")
        assert plugin is not None
        assert plugin.id == "cursor"

    def test_ms4_checklist_item_3_plugin_exposes_name(self):
        engine = _seed()
        plugin = engine.get_plugin("cursor")
        assert plugin is not None
        assert plugin.name == "Cursor"


# --- fossil: ticket ID in the title, unrelated to the behavior --------------

def test_slob_42_list_plugins_returns_registered_entries():
    engine = _seed()
    plugins = engine.list_plugins()
    ids = {p.id for p in plugins}
    assert ids == {"cursor", "claude-code"}


# --- fossil: AC identifier in the docstring, body is a registry contract ---

def test_register_is_idempotent():
    """Satisfies AC-7 of the registry spike: repeated registration does not dup."""
    engine = _seed()
    engine.register(Plugin(id="cursor", name="Cursor"))
    plugins = [p for p in engine.list_plugins() if p.id == "cursor"]
    assert len(plugins) == 1


# --- negative example: the word "refactor" appears, but the body genuinely  -
#     verifies a refactor-safety property (call-graph preservation under a    -
#     renaming transform). The audit must not flag this.                     -

def test_refactor_preserving_rename_does_not_change_lookup_results():
    """Rename-only refactors must not change call-graph semantics; guards that claim."""
    engine = _seed()
    before = engine.get_plugin("cursor")

    original_id = "cursor"
    renamed_id = original_id  # simulates the identity-refactor case
    after = engine.get_plugin(renamed_id)

    assert before == after
