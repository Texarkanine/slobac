# Expected findings — `both-smells` scenario

**Target suite root:** `tests/fixtures/audit/both-smells/`
**Suite contents:** 4 tests — 1 pure fossil, 1 pure naming-lie, 1 exhibiting both, 1 clean.

This scenario exercises **scope honoring.** The same suite is audited three times with different scope; findings differ per scope. The audit is correct when each scope emits exactly the findings listed below — no more, no fewer.

## Per-scope expectations

### Scope: `deliverable-fossils` only

**Expected finding count:** 2

1. **`TestM2ConfigRefactor.test_get_returns_default_when_key_missing_per_m2_spec`** — title and class both carry sprint/milestone vocabulary (`M2`, `refactor`, `per m2 spec`). Remediation: rename to `test_get_returns_default_when_key_missing` and move out of the `TestM2ConfigRefactor` grouping into a capability-named container (e.g. `class TestConfigGetWithDefault`).
2. **`test_slob_99_uses_cyan_for_error_messages`** — ticket prefix `SLOB-99`. Remediation: strip the ticket prefix from the title; if the reason-to-exist is a specific regression guard, record the ticket as a code comment.

Naming-lie findings on `test_slob_99_...` and `test_theme_setting_is_case_insensitive` must NOT appear at this scope.

### Scope: `naming-lies` only

**Expected finding count:** 2

1. **`test_theme_setting_is_case_insensitive`** — title claims case-insensitivity; body performs exact-case round-trip. Path: **rename.** Body is a clean round-trip contract.
2. **`test_slob_99_uses_cyan_for_error_messages`** — title claims ANSI color support; body stores and retrieves an error-prefix string with no color handling. Path: **rename.** Body contract is config round-trip; title was aspirational.

Fossil findings on `TestM2ConfigRefactor...` and `test_slob_99_...` must NOT appear at this scope.

### Scope: both (explicit `all` or both smells named)

**Expected finding count:** 4 — *three tests, four findings.* The test `test_slob_99_uses_cyan_for_error_messages` is flagged twice (once per smell) because it exhibits both. Each finding names its distinct remediation:

1. `TestM2ConfigRefactor.test_get_returns_default_when_key_missing_per_m2_spec` — `deliverable-fossils` — rename + regroup.
2. `test_theme_setting_is_case_insensitive` — `naming-lies` — rename.
3. `test_slob_99_uses_cyan_for_error_messages` — `deliverable-fossils` — rename (strip ticket prefix).
4. `test_slob_99_uses_cyan_for_error_messages` — `naming-lies` — rename (body is round-trip, not color).

The two `test_slob_99_...` findings share a test location but have distinct smell slugs, distinct rationale anchors (the ticket prefix vs. the title/body mismatch), and distinct remediations. They must not be silently collapsed. Their coexistence is the "Related modes" cross-link pattern from the manifesto: fossil and naming-lie can co-occur, and each is worth naming.

## Tests that must NOT be flagged at any scope

### `test_keys_returns_values_in_sorted_order`

- **Why not flagged:** Title claims sorted order; body asserts `keys() == ["apple", "mango", "zebra"]` which verifies exactly that. No fossil vocabulary, no title/body mismatch.

## Out-of-scope handling

If the operator invokes with a smell slug the skill does not support in Phase 1 (e.g. `tautology-theatre`), the audit must respond with a clear "not-in-scope for Phase 1" message naming which slugs *are* supported (`deliverable-fossils`, `naming-lies`). It must not silently skip, and it must not emit a partial report implying the requested smell was audited.

## Notes

- This scenario is the scope-honoring integration test (B3 from the test plan).
- The double-flag behavior (same test, two findings) is the principal stress test. A common failure mode is an overly-aggressive dedup that collapses the two findings into "this test is named badly"; the fix is to keep each smell's finding distinct because each prescribes a distinct remediation.
