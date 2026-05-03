# Expected findings — `shared-state` scenario

**Target suite root:** `tests/fixtures/audit/shared-state/`
**In-scope smells:** `shared-state`
**Expected finding count:** 2

Shape mirrors the audit report template. Each finding below must appear in the emitted `slobac-audit.md` with equivalent content; phrasing need not be byte-identical, but the test location, smell slug, remediation path, and rationale anchor must match.

## Findings

### 1. Module-level `Engine` instance shared across tests

- **Location:** `test_engine_state.py` → module level, line ~12 (`_engine = Engine()`)
- **Smell:** `shared-state`
- **Rationale:** A mutable `Engine` instance is created at module scope and mutated by multiple test functions (`test_add_item_persists`, `test_remove_item_clears_entry`, `test_count_reflects_additions`). Tests depend on execution order — `test_remove_item_clears_entry` assumes items added by `test_add_item_persists` are still present. See [shared-state](https://texarkanine.github.io/slobac/taxonomy/shared-state/) signals — "module-level mutable object written by one test, read by another."
- **Prescribed remediation:** Move `Engine()` construction into a `@pytest.fixture` that returns a fresh instance per test. Each test declares the fixture as a parameter and seeds its own starting state. The module-level `_engine` binding is deleted.
- **Why this isn't a false positive:** The binding is mutable (methods called on it modify internal state), and multiple tests both read and write it without any reset mechanism between them.

### 2. Module-level `_results` list accumulated across tests

- **Location:** `test_engine_state.py` → module level, line ~13 (`_results: list[str] = []`)
- **Smell:** `shared-state`
- **Rationale:** A module-level list is appended to by `test_add_item_persists` and `test_count_reflects_additions`, then read by `test_results_accumulate`. The list is never cleared between tests. See [shared-state](https://texarkanine.github.io/slobac/taxonomy/shared-state/) signals — "module-level collection mutated across test boundaries."
- **Prescribed remediation:** Eliminate the module-level `_results` list. Each test that needs to track results should use a local variable or a per-test fixture. If cross-test accumulation was intentional (it shouldn't be), restructure into a single test with multiple assertions.
- **Why this isn't a false positive:** The list grows monotonically across test boundaries with no reset. Test outcomes depend on which tests ran before them.

## Tests that must NOT be flagged

### `test_isolated_operation` (uses `@pytest.fixture` for per-test setup)

- **Location:** `test_engine_state.py` → function `test_isolated_operation`, uses fixture `fresh_engine`
- **Why not shared-state:** The `fresh_engine` fixture creates a new `Engine()` instance per test invocation. The fixture is declared with default scope (`function`), so each test gets its own copy. The test does not touch the module-level `_engine` or `_results`.
- **False-positive guard:** See the [shared-state](https://texarkanine.github.io/slobac/taxonomy/shared-state/) canonical entry's False-positive guards section — per-test fixtures that look shared but use function-scope factory are not the smell.

### `test_read_only_access` (reads module-level constant, does not mutate)

- **Location:** `test_engine_state.py` → function `test_read_only_access`
- **Why not shared-state:** This test reads `ENGINE_NAME` (a module-level string constant) but does not mutate any shared state. Constants shared across tests are not the smell — mutability is the key signal.
- **False-positive guard:** See the [shared-state](https://texarkanine.github.io/slobac/taxonomy/shared-state/) canonical entry — the smell requires mutable bindings leaked across tests, not read-only shared data.

## Notes

- Scenario contains 6 tests total: 3 depend on shared mutable state and trigger findings (though grouped into 2 findings by shared-state root cause), 1 uses per-test fixture isolation (negative), 1 reads a constant (negative), 1 is a legitimate test in the shared-state zone but doesn't itself trigger the smell (it's a victim, not the cause).
- The fixture exercises per-file detection scope: the assessor must see the full file to trace mutable bindings across test boundaries. Per-test analysis alone would miss the cross-test mutation pattern.
