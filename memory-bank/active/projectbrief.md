# Project Brief: Onboard Remaining 9 Smells

## User Story

The audit orchestration framework (archived 2026-05-03) made 6 of 15 taxonomy smells first-class supported slugs in `slobac-audit`. The remaining 9 — all per-test scope — are still in the manifesto but are not in the SKILL's supported list and have no fixtures proving detection. We want to onboard them so the framework reaches parity with the taxonomy.

## Smells to Onboard

All 9 are **per-test** scope (already verified from the creative-phase classification table in the archived task):

1. `vacuous-assertion`
2. `tautology-theatre`
3. `pseudo-tested`
4. `over-specified-mock`
5. `implementation-coupled`
6. `presentation-coupled`
7. `conditional-logic`
8. `mystery-guest`
9. `rotten-green`

## Requirements

For each of the 9 smells:

1. Add the slug to the **Supported smells** table in `skills/slobac-audit/SKILL.md` (per-test row).
2. Add natural-phrase mappings for the slug in the SKILL's intent-mapping bullets.
3. Verify the taxonomy entry at `skills/slobac-audit/references/docs/taxonomy/<slug>.md` carries the correct `Detection Scope: per-test` header (added uniformly in the prior task — verification only).
4. Create a fixture under `tests/fixtures/audit/<slug>/` with:
   - At least one planted Python test demonstrating the smell.
   - At least one negative-control test that does **not** trigger the smell.
   - An `expected-findings.md` aligned with the report-template conventions used by existing fixtures.
5. Update `tests/fixtures/audit/README.md` if it enumerates fixtures.

## Constraints / Quality Gates

- `properdocs build --strict` must remain green.
- Existing 6-smell behavior must remain unchanged (no regressions in `slobac-audit/SKILL.md` for the already-supported slugs).
- No orchestrator surgery — all 9 are per-test, so the existing batch-assessor routing is sufficient.
- Fixtures may be one-per-smell or combined where natural; either is acceptable.

## Out of Scope

- Apply layer / fix automation.
- Cross-suite extensions (none of the 9 are cross-suite scope).
- Multi-scope combined fixture (noted as a non-blocking advisory in the prior preflight; remains a future enhancement).
