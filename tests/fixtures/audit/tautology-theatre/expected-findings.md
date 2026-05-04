# Expected findings — `tautology-theatre` scenario

**Target suite root:** `tests/fixtures/audit/tautology-theatre/`
**In-scope smells:** `tautology-theatre`
**Expected finding count:** 2

The two findings exercise both canonical shapes named in the [`tautology-theatre`](https://texarkanine.github.io/slobac/taxonomy/tautology-theatre/) entry: **mock tautology** (mock returns X, assert mock returned X) and **mock-of-SUT** (the unit under test has its own method patched). Severity is `Critical` and the prescribed remediation is **delete**, not transform — the audit is correct only when each finding's remediation reads "delete" (with the alternative "rewrite" mentioned only as a contingent path the operator can elect).

## Findings

### 1. `test_charge_returns_true_when_successful` — shape: mock-tautology

- **Location:** `test_payment_processor.py` → module level
- **Smell:** `tautology-theatre`
- **Rationale:** The test creates a `MagicMock`, configures `mock_charger.charge.return_value = True`, calls `mock_charger.charge(...)`, and asserts the result is `True`. The real `PaymentProcessor.charge` is never invoked. Logically `x = True; assert x == True` — the only thing verified is that `MagicMock` works.
- **Prescribed remediation:** **Delete.** No production code is exercised; the test cannot regress regression-detection power because it was killing no mutants. Per the canonical entry's preferred-fix rationale, emit a coverage-gap note if a reviewer believes the underlying behavior (charge succeeds when HTTP returns 200) ought to be covered — do not chain delete + rewrite in this commit.
- **Why this isn't a false positive:** The SUT class `PaymentProcessor` is imported but never constructed in this test. The mock is not standing in for an external collaborator; it *is* the only object the assertion ever touches.

### 2. `test_validate_accepts_positive_amount` — shape: mock-of-SUT

- **Location:** `test_payment_processor.py` → module level
- **Smell:** `tautology-theatre`
- **Rationale:** `PaymentProcessor` is instantiated, but its `validate` method — the very method the test name promises to verify — is patched on the class itself with `return_value=True`. The assertion checks that the patch returned `True`. The real `validate` body (`return amount > 0`) is never executed. This is the canonical "mock the unit under test" shape.
- **Prescribed remediation:** **Delete.** Same rationale as finding 1. The alternative `rewrite` (remove the patch, assert on real `validate(amount=42)` and `validate(amount=-1)` boundary cases) is a separate move per the canonical entry; do not chain.
- **Why this isn't a false positive:** The patched method is on the SUT class, not on a collaborator. The `http_client` MagicMock argument is unused by `validate`; it cannot be the real reason the test passes.

## Tests that must NOT be flagged

### `test_charge_marks_response_ok_when_http_returns_200`

- **Location:** `test_payment_processor.py` → module level
- **Why not a tautology:** The real `PaymentProcessor.charge` body runs end-to-end: it calls `self._http.post(...)`, reads `response["status"]`, builds a result dict, and returns it. The MagicMock stands in for an *external* collaborator (HTTP client), not for the SUT. The assertion `result == {"ok": True, "amount": 100}` verifies the SUT's actual transformation logic (mapping HTTP 200 → `ok: True` and echoing the amount) — none of which the mock controls.
- **False-positive guard:** Naive detectors that flag any test using `MagicMock` will trip here. The semantic question per the canonical entry is *"would this test pass if all production code were deleted?"* — no, because deleting `PaymentProcessor.charge` would leave the mock unused and the assertion's RHS dict unconstructable from the mock alone.

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `tautology-theatre` and remediation **delete**, 1 must not be flagged.
- The remediation arm (delete vs rewrite) is load-bearing — a finding that gets the smell right but suggests rewriting first is a build-phase bug per the canonical entry's "do not chain delete + rewrite" rule.
- The Severity = `Critical` ranking should surface in the report (these are the highest-priority findings to act on, even though only 2 of them).
