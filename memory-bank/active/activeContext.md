# Active Context

## Current Task: prose-pin and weak-text-oracle taxonomy smells
**Phase:** BUILD - COMPLETE

## What Was Done
- Added `prose-pin` + `loose-text-oracle` taxonomy entries (High, per-test) with full CONTRIBUTING shape.
- Planted audit fixtures under `tests/fixtures/audit/prose-pin/` and `loose-text-oracle/` (2 positives + 2 negatives each) with `expected-findings.md`.
- Boundary edits: `presentation-coupled` (too-strong vs LTO too-weak), `vacuous-assertion`, `conditional-logic` After prefers typed throw (not message-regex alone).
- Regenerated taxonomy index; count-agnostic wording in `systemPatterns.md` + docs README; fixtures README rows.
- Gates: `properdocs build --strict` green; index `--check` clean; hand-diff 47/47; `pytest` 24 passed.

## Key Decisions During Build
- None beyond creative — built to plan. LTO positive 1 uses `pytest.raises(..., match="timeout")` (canonical signal); typed negative uses `NotFoundError` + supplementary `match="gamma"`.

## Deviations from Plan
- None.

## Next Step
- QA review runs next (`/niko-qa`).
