# Expected findings — `deliverable-fossils` scenario

**Target suite root:** `tests/fixtures/audit/deliverable-fossils/`
**In-scope smells:** `deliverable-fossils`
**Expected finding count:** 4

Shape mirrors the audit report template. Each finding below must appear in the emitted `slobac-audit.md` with equivalent content; phrasing need not be byte-identical, but the test location, smell slug, remediation path, and rationale anchor must match.

## Findings

### 1. `TestSourceTrackingRefactor.test_should_return_the_plugin_via_get_plugin_after_source_tracking_refactor`

- **Location:** `test_plugin_registry.py` → class `TestSourceTrackingRefactor`
- **Smell:** `deliverable-fossils`
- **Rationale:** Test title references a refactor ("source tracking refactor") rather than the behavior it verifies (the plugin registry's `get_plugin(id)` contract). See [deliverable-fossils](https://texarkanine.github.io/slobac/taxonomy/deliverable-fossils/) signals list — "test titles containing `refactor`, `after X migration`".
- **Prescribed remediation:** Rename to encode the behavior the body actually verifies, e.g. `test_get_plugin_returns_registered_plugin_by_id`. Preserve the call graph (rename-only; no body changes).
- **Why this isn't a false positive:** The body asserts the identity of the returned plugin, not any property of the refactor. The refactor vocabulary adds no information about what the test guards.

### 2. `TestSourceTrackingRefactor.test_ms4_checklist_item_3_plugin_exposes_name`

- **Location:** `test_plugin_registry.py` → class `TestSourceTrackingRefactor`
- **Smell:** `deliverable-fossils`
- **Rationale:** Title references a sprint checklist (`MS-4 checklist item 3`) rather than the behavior. Canonical fossil shape.
- **Prescribed remediation:** Rename to express the contract, e.g. `test_get_plugin_returns_plugin_whose_name_matches_registration`. Note under [`semantic-redundancy`](https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/) that finding #1 and #2 verify adjacent properties of the same lookup — a follow-up regroup (Phase B of the prescribed fix) may fold them into one stronger assertion.
- **Why this isn't a false positive:** The checklist reference does not describe what the test proves. The body asserts a name-exposure property.

### 3. `test_slob_42_list_plugins_returns_registered_entries`

- **Location:** `test_plugin_registry.py` → module level
- **Smell:** `deliverable-fossils`
- **Rationale:** Title carries a ticket prefix (`SLOB-42`) that names the reason-for-existence, not the behavior under test.
- **Prescribed remediation:** Rename to `test_list_plugins_returns_registered_entries` (drop the ticket prefix). If the team wants to preserve regression-guard provenance, add the ticket as a code comment above the test — not in the name.
- **Why this isn't a false positive:** `SLOB-42` adds zero behavioral information; the rest of the title already encodes the claim.

### 4. `test_register_is_idempotent`

- **Location:** `test_plugin_registry.py` → module level
- **Smell:** `deliverable-fossils`
- **Rationale:** Docstring cites an acceptance-criterion identifier (`AC-7`) and a delivery artifact ("registry spike"). The *title* is already good; the fossil lives in the docstring.
- **Prescribed remediation:** Rewrite the docstring to describe the behavior ("Registering the same plugin twice leaves the registry with one entry"). Strip the AC reference and the "spike" vocabulary. Title needs no change.
- **Why this isn't a false positive:** The docstring's fossil vocabulary does not survive into the body's assertions; the body is a clean idempotency check.

## Tests that must NOT be flagged

### `test_refactor_preserving_rename_does_not_change_lookup_results`

- **Location:** `test_plugin_registry.py` → module level
- **Why not a fossil:** The title contains the word `refactor`, but the body genuinely verifies a refactor-safety property (that rename-only transforms preserve lookup semantics). The refactor vocabulary here *is* the behavior — dropping it would make the test's intent less clear, not more.
- **False-positive guard:** See the [deliverable-fossils](https://texarkanine.github.io/slobac/taxonomy/deliverable-fossils/) canonical entry's False-positive guards section — the word `refactor` is a signal, not a verdict; the audit must verify the body is *about* history before flagging.

## Notes

- Scenario contains 5 tests total: 4 should be flagged as `deliverable-fossils`, 1 must not. Any deviation (false positive on the negative example, missed finding on any of the 4, or a remediation that encodes the fossil vocabulary rather than the behavior) is a build-phase bug in the audit skill.
- This scenario does not exercise scope (it is single-smell). Scope exercise lives in `both-smells/`.
