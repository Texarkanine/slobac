# Expected findings — `rotten-green` scenario

**Target suite root:** `tests/fixtures/audit/rotten-green/`
**In-scope smells:** `rotten-green`
**Expected finding count:** 2

The two findings exercise canonical signals from the [`rotten-green`](https://texarkanine.github.io/slobac/taxonomy/rotten-green/) entry: empty body with TODO comment, and `print(...)` left in the test body where an assertion was intended. Severity is `Low` and detection is **syntactic and extremely cheap**. The fix-vs-delete decision is the only place semantic reasoning is needed.

## Findings

### 1. `test_record_handles_negative_values` — explicit pending or implement

- **Location:** `test_metric_collector.py` → module level
- **Smell:** `rotten-green`
- **Rationale:** Empty body with only `# TODO: test this` and `pass`. The canonical signal "Empty `it()` / `test()` body with only `// TODO` that still counts as passing" applies directly. The runner reports this as a passing test, hiding the fact that no behavior was verified.
- **Prescribed remediation:** Per canonical fix path (2) "Stub that was meant to test something." The test name suggests an intent (record handles negative values). Two acceptable transforms:
    - **Mark pending:** convert to `@pytest.mark.skip(reason="TODO: verify negative values are recorded as samples")` so the gap surfaces in CI reports as a known TODO instead of a silent green. Per the canonical regression-power gate, the skip *must* include a reason string.
    - **Implement:** apply [describe-before-edit](https://texarkanine.github.io/slobac/principles/#behavior-articulation-before-change) to guess intent from the name — likely "records `-5.0` as a sample and includes it in the average" — and write the assertion. If the intent is ambiguous, prefer explicit pending.
- **Why this isn't a false positive:** Empty body, no assertion, no SUT call, single TODO comment. There is no scenario in which this test verifies anything.

### 2. `test_average_after_three_samples` — replace print with assertion

- **Location:** `test_metric_collector.py` → module level
- **Smell:** `rotten-green`
- **Rationale:** The test calls the SUT (`record` × 3 + `average`), computes `avg`, then calls `print("computed average:", avg)`. The canonical signal "`console.log('done!', res)` / `print(result)` left in the test body where an assertion was intended" applies directly. The test reports green regardless of the SUT's return value — `def average(self): return 999` would still print and pass.
- **Prescribed remediation:** Per canonical fix path (2). The test name is unambiguous (asserts on the average after three samples), so the implementation path is preferred over pending. Replace `print("computed average:", avg)` with `assert avg == 20.0`. The `print` line itself should be removed entirely (debug noise).
- **Why this isn't a false positive:** The SUT runs and produces a value; the value is bound to `avg`; `avg` is consumed only by `print`, never by an assertion. This is exactly the canonical "variable computed and discarded" signal in the `print`-shaped variant.

## Tests that must NOT be flagged

### `test_average_of_three_samples_is_their_arithmetic_mean`

- **Location:** `test_metric_collector.py` → module level
- **Why not rotten-green:** Real SUT call, real assertion (`assert collector.average() == 20.0`). The test would fail if `average` returned anything other than 20.0. There is no `print`, no TODO, no dead variable.
- **False-positive guard:** Naive detectors that flag any short test or any test with a single assertion will trip here. The semantic question per the canonical entry is *"does this test, despite being green, actually exercise and assert anything?"* — for full structural equality on the SUT's return value, the answer is yes.

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `rotten-green`, 1 must not be flagged.
- The fix-vs-delete decision is the load-bearing semantic step. For finding 1, **explicit pending** is acceptable as a stop-gap; for finding 2, the test name is specific enough that **implement the assertion** is preferred. A finding that prescribes deletion for finding 2 (where the test name encodes a real intent) is a build-phase bug per the canonical fix path (2) preference.
- Sibling smells (`vacuous-assertion`, `pseudo-tested`, `shared-state`) are not in scope; the canonical entry notes that `vacuous-assertion` and `pseudo-tested` are adjacent (rotten-green has *no* assertion; the others have weak/insufficient ones), but this fixture's positives are firmly within `rotten-green` (no assertion at all in either positive).
