# Expected findings — `clean` scenario

**Target suite root:** `tests/fixtures/audit/clean/`
**Expected finding count:** 0, at any scope.

Every test in this suite has a behavior-encoded name (the title makes a claim about the product) and a body whose assertions verify that claim. No ticket IDs, no refactor references, no checklist vocabulary. No title/body mismatches.

## Behavior per scope

- **Scope `deliverable-fossils`:** zero findings. Emit a report with "No findings for scope `deliverable-fossils`."
- **Scope `naming-lies`:** zero findings. Emit a report with "No findings for scope `naming-lies`."
- **Scope `all` (or both smells named):** zero findings under each scope; report may combine them into one "No findings" section.

The report must still emit — a "no findings" report is a valid audit outcome, not a silent success. Operator-facing proof of completion matters.

## Why this scenario matters

This is the false-positive gate (B4 from the test plan). A Phase-1 audit that emits one findings report on real tests is only useful if it doesn't emit spurious findings on clean tests. The test bodies here are deliberately short and plain — any finding the audit emits on this fixture is an over-trigger.

## Guard against "everything looks like a nail"

Common over-trigger modes the audit must avoid:

- Flagging `test_preserves_currency_of_operands_in_result` as a naming-lie because "preserves" and "operands" are technical vocabulary. The body verifies what the title says: the currency field of the operands is preserved in the result.
- Flagging `test_rejects_mixed_currencies_with_value_error` as a fossil because the word "rejects" appears. "Rejects" is a behavioral verb, not a fossil marker; the body verifies rejection semantics.
- Flagging the `TestMoneyAddition` grouping as fossil-shaped because it's a class. Class-based grouping by capability is fine; the fossil shape is grouping by *work phase* (e.g. `TestInitialImplementation`, `TestPostRefactor`), not by capability.
