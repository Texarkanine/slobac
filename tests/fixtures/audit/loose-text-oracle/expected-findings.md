# Expected findings — `loose-text-oracle` scenario

**Target suite root:** `tests/fixtures/audit/loose-text-oracle/`
**In-scope smells:** `loose-text-oracle`
**Expected finding count:** 2

The two findings exercise canonical signals from the [`loose-text-oracle`](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/) entry: underdetermined substring/regex asserts on runtime-emitted errors and logs where the opposite meaning would also match. The audit is correct only when remediation prefers **typed error / structured code / structured log fields**, and when both negative controls below stay unflagged. Do **not** reclassify these as `presentation-coupled` (that smell is over-strong cosmetic presentation, not underdetermined meaning).

## Findings

### 1. `test_fetch_raises_on_timeout` — prefer typed error / code

- **Location:** `test_runtime_text.py` → module level
- **Smell:** `loose-text-oracle`
- **Rationale:** The sole oracle for *which* failure occurred is `pytest.raises(RuntimeError, match="timeout")` / message substring `"timeout"`. The phrase underdetermines meaning: a wrong implementation that raises `RuntimeError("timeout disabled; proceeding")` or `RuntimeError("no timeout configured")` still matches. Opposite-polarity messages that contain the token pass. Canonical signal: ambiguous err-message substring/regex as the primary (or only) oracle for failure identity.
- **Prescribed remediation:** Assert on a typed error and/or stable machine code first (`raises(TimeoutError)` / `err.code == "ETIMEDOUT"` / `errors.Is`). Message match may remain only as a *supplementary* check that a dynamic datum appears (e.g. the offending URL), never as the identifier of which failure occurred.
- **Why this isn't a false positive:** `"timeout"` is deliberately ambiguous; the test comment notes the opposite meaning would also match. This is not a full golden diagnostic snapshot, and not a typed primary oracle.

### 2. `test_process_logs_success` — prefer structured log fields

- **Location:** `test_runtime_text.py` → module level
- **Smell:** `loose-text-oracle`
- **Rationale:** The oracle is `assert "success" in caplog.text` (or equivalent stdout/log-line substring). The token `"success"` underdetermines the claimed outcome: `"operation success: false"`, `"no success path taken"`, or a partial failure that still prints the word would keep the test green. Canonical signal: ambiguous log/stdout phrase as the semantic claim.
- **Prescribed remediation:** Assert on structured log/event fields (event name, level, bound context) via the emitter's capture API, or assert on the resulting state change. If the rendered line *is* the product, switch to an explicit golden/approval snapshot of the full diagnostic — not a lone substring.
- **Why this isn't a false positive:** The planted phrase is ambiguous by design; this is not presentation-coupled's long cosmetic HTML `in`-chain (B9 boundary — that shape stays in the `presentation-coupled` fixture).

## Tests that must NOT be flagged

### `test_fetch_raises_typed_not_found_with_optional_param_name`

- **Location:** `test_runtime_text.py` → module level
- **Why not loose-text-oracle:** Primary oracle is typed (`raises(NotFoundError)` / equivalent). An optional supplementary `match=` / message check only verifies that a dynamic datum (the missing resource name) appears in the human message — the Go Wiki carve-out. Type/code identifies *which* failure; the substring does not.
- **False-positive guard:** Naive detectors that flag every `raises(..., match=)` will trip here. The semantic question is *"is the message match the primary identifier of the failure, or a supplementary datum check beside type/code?"* — here it is supplementary.

### `test_cli_help_golden_matches_full_diagnostic`

- **Location:** `test_runtime_text.py` → module level
- **Why not loose-text-oracle:** The emitted text *is* the product: full CLI help / diagnostic golden equality (approval-style). The presentation contract is explicit and whole, not a lone underdetermined substring pretending to encode meaning.
- **False-positive guard:** Do not flag golden/full-snapshot presentation contracts where message text is the specified deliverable. (A `presentation-coupled` / `wrong-level` review of whether the golden belongs in unit CI is out of scope for this fixture.)

## Notes

- Scenario contains 4 tests total: 2 must be flagged with `loose-text-oracle`, 2 must not be flagged (typed+supplementary; text-is-product golden).
- Remediation hierarchy is load-bearing: typed/code > structured log fields > golden full text > substring. A finding that only says "tighten the regex" without climbing the hierarchy is a build-phase bug.
- Boundary (B9): long cosmetic HTML `in`-chains remain `presentation-coupled` territory — this fixture plants *ambiguous meaning* tokens (`"timeout"`, `"success"`), not cosmetic tag/class chains.
- Sibling smells (`presentation-coupled`, `vacuous-assertion`, `prose-pin`) are not in scope for flagging here.
