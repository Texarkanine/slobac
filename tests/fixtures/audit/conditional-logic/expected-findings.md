# Expected findings — `conditional-logic` scenario

**Target suite root:** `tests/fixtures/audit/conditional-logic/`
**In-scope smells:** `conditional-logic`
**Expected finding count:** 2

The two findings exercise both canonical signals from the [`conditional-logic`](https://texarkanine.github.io/slobac/taxonomy/conditional-logic/) entry: `if cond: assert(...)` inside a test body, and `try { sut() } except: assert(...)` without a trailing `pytest.fail("should have raised")`. The audit is correct only when each finding's prescribed remediation matches the canonical Shape→Transform table.

## Findings

### 1. `test_apply_promo_with_save10_reduces_price` — split or remove the branch

- **Location:** `test_promo_calculator.py` → module level
- **Smell:** `conditional-logic`
- **Rationale:** The test body contains `if code: assert result == 90.00`. The canonical AST signal "`IfStatement` inside a test-function body; the consequent contains `expect` / `assert`; the alternate is absent" fires. The condition `code = "SAVE10"` is set in the test body, so the `if` *will* always be entered for this test — but the `if` is dead branching that compensates for nothing. If a future edit changed the local to `code = None`, the test would silently pass without checking anything.
- **Prescribed remediation:** Per the canonical Shape→Transform table, this is the "compensating for a weak oracle" shape — the `if` guards against a precondition that the test itself sets, so the precondition can be pinned in the fixture and the branch removed. Transform: delete the `if code:` wrapper and assert unconditionally `assert result == 90.00`. The cyclomatic complexity of the test body must drop to 1.
- **Why this isn't a false positive:** The `if` is an `IfStatement` inside the test function with no alternate. The test would pass without raising or asserting if the body were edited so `code` evaluated falsy — the textbook silent-pass mode.

### 2. `test_apply_promo_with_unknown_code_raises_value_error` — replace with `pytest.raises`

- **Location:** `test_promo_calculator.py` → module level
- **Smell:** `conditional-logic`
- **Rationale:** The test wraps the SUT call in `try: ... except ValueError as e: assert "MYSTERY" in str(e)` with no `pytest.fail("should have raised")` after the `try`. If `apply_promo` ever stopped raising — e.g. a refactor that silently returned the original price for unknown codes — the `except` block would never execute, no assertion would fire, and the test would pass green. This is exactly the canonical signal "`try { sut() } catch (e) { expect(e.message).toBe(...) }` with no `assert.fail` after the try. The catch is conditional on a throw actually happening."
- **Prescribed remediation:** Per the canonical Shape→Transform table, the transform is the runner's throw matcher: `with pytest.raises(ValueError, match="MYSTERY"): apply_promo(100.00, "MYSTERY")`. This both asserts the exception type/message *and* that one was raised. After the transform, regression-detection power is strictly higher — a refactor that stopped raising would now fail the test instead of passing it silently.
- **Why this isn't a false positive:** The `try` block has no `else` and no trailing `pytest.fail`. The except's assertion fires only on the throw path — the no-throw path is silently green.

## Tests that must NOT be flagged

### `test_apply_promo_returns_expected_price`

- **Location:** `test_promo_calculator.py` → module level
- **Why not conditional-logic:** No `if`, no `try/except`, no loops with internal-only assertions. The cyclomatic complexity of the test body is 1. Each parameterized case asserts unconditionally on the return value — the canonical preferred shape per the entry's transform guidance.
- **False-positive guard:** Naive detectors that flag any test using `pytest.parametrize` (which does, structurally, branch — but at the test-collection layer, not in the test body) will trip here. The semantic question per the canonical entry is *"is there an `IfStatement` or `try/except` inside the test-function body?"* — for parameterized tests, the answer is no; the parameterization is a runner concern, not a body concern.

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `conditional-logic`, 1 must not be flagged.
- The Shape→Transform mapping is load-bearing — finding 1 prescribes "remove the branch", finding 2 prescribes "replace with throw matcher". A finding that prescribes a generic "unconditionally assert" without distinguishing the shape is a build-phase bug.
- Sibling smells (`rotten-green`, `vacuous-assertion`) are not in scope; the canonical entry notes the cousin relationship to `rotten-green` (no assertion at all) but this fixture's positives are firmly within `conditional-logic` (assertion exists, but on a conditional path).
