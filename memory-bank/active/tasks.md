# Task: Onboard Remaining 9 Per-Test Smells

* Task ID: onboard-remaining-smells
* Complexity: Level 2
* Type: Simple enhancement (mechanical parity work — no architectural change)

Bring the `slobac-audit` framework to taxonomy parity by promoting the 9 still-unsupported smells (`vacuous-assertion`, `tautology-theatre`, `pseudo-tested`, `over-specified-mock`, `implementation-coupled`, `presentation-coupled`, `conditional-logic`, `mystery-guest`, `rotten-green` — all `per-test` detection scope per their existing taxonomy headers) to first-class supported slugs. Each smell gains a fixture under `tests/fixtures/audit/<slug>/`, a row in the `slobac-audit` SKILL's supported-slug table, and a natural-phrase mapping bullet. Existing 6-smell behavior is unchanged; no orchestrator surgery required (all 9 route through the existing per-test batch-assessor path).

## Test Plan (TDD)

### Behaviors to Verify

For each of the 9 smells `<slug>`:

- **B1 — Fixture present**: `tests/fixtures/audit/<slug>/` exists and contains at least one `.py` file with planted positive case(s) and at least one negative-control test → directory listing matches convention.
- **B2 — Expected findings present**: `tests/fixtures/audit/<slug>/expected-findings.md` exists, mirrors the report-template shape used by existing fixtures (header with target/in-scope/count, per-finding location/smell/rationale/remediation/false-positive-guard, "Tests that must NOT be flagged" section) → readable, parseable, and consistent with the canonical taxonomy entry's prescribed fix.
- **B3 — SKILL supported-slug row**: `skills/slobac-audit/SKILL.md` Step 2 supported-smells table contains a row for `<slug>` with `Detection Scope: per-test` → `grep` confirms exactly one row per slug.
- **B4 — SKILL natural-phrase mapping**: `skills/slobac-audit/SKILL.md` Step 2 intent-mapping bullets contain a bullet for `<slug>` enumerating natural-language phrases drawn from the taxonomy entry's vocabulary → `grep` confirms one bullet per slug.

Suite-wide behaviors:

- **B5 — Taxonomy unchanged**: All 9 taxonomy entries already carry `Detection Scope: per-test` (verified inline during planning); no edits to `references/docs/taxonomy/<slug>.md` are required. This is a verification step, not an edit step.
- **B6 — Fixtures README updated**: `tests/fixtures/audit/README.md` enumerates the 9 new scenarios under a new "Scenarios added for taxonomy parity (Phase 3)" subsection.
- **B6b — Skill README updated** *(added by preflight)*: `skills/slobac-audit/README.md` reflects parity — lead-paragraph smell count, supported-smells table, smoke-test fixtures list, and the constraints disclaimer all consistent with the new 15-smell SKILL.md state.
- **B7 — Existing 6-smell rows preserved**: The 6 already-supported slugs (`deliverable-fossils`, `naming-lies`, `shared-state`, `monolithic-test-file`, `semantic-redundancy`, `wrong-level`) remain in the table and intent-map without modification → diff inspection.
- **B8 — properdocs build green**: `uv run properdocs build --strict` succeeds.
- **B9 — Persistent memory bank updated**: `memory-bank/techContext.md` smell count goes from "6 smells across 3 detection scopes" to "15 smells across 3 detection scopes" with the per-test list extended; `memory-bank/systemPatterns.md` evidence count "all 15 existing entries follow the pattern" remains accurate (no change needed).

### Edge Cases

- **Negative controls in every fixture** — every fixture must include at least one test that has the *shape* a naive detector would trip on but is actually clean. This is the false-positive gate, mirrored from existing fixtures (`clean/`, `naming-lies/`, etc.).
- **Multi-shape smells** — `tautology-theatre` (mock-tautology vs no-production-code), `over-specified-mock` (over-spec interactions vs internal-detail testing), `mystery-guest` (classical vs fixture-coupled magic numbers), `conditional-logic` (`if` vs `try/except`), and `rotten-green` (empty body vs dead fixture) each have multiple shapes per their canonical entry. Each fixture must exercise **at least one** shape; exercising all shapes is preferred but not required.
- **Severity-Critical handling** — `tautology-theatre` is `Critical` severity with the prescribed fix being **delete**, not transform. The fixture's `expected-findings.md` must reflect that prescription, not a generic "rewrite" arm.
- **Cross-references between smells** — several entries (e.g. `vacuous-assertion` ↔ `pseudo-tested`, `tautology-theatre` ↔ `pseudo-tested`, `presentation-coupled` ↔ `vacuous-assertion`) cite each other. Each fixture must stay scoped to *its own* smell; if a planted test happens to also exhibit a sibling smell, the `expected-findings.md` notes it but does not require the audit to detect it (single-smell scope is the operator's choice in the invocation).

### Test Infrastructure

- **Framework**: None for fixtures (they are inputs, never executed by SLOBAC's own runners). The mechanical gate is `uv run properdocs build --strict` per `.github/workflows/docs.yaml`.
- **Test location**: `tests/fixtures/audit/<slug>/` per the existing convention documented in `tests/fixtures/audit/README.md`.
- **Conventions**: Each scenario directory contains one or more `.py` files (pytest-shaped but never collected by SLOBAC) and an `expected-findings.md` whose shape mirrors the audit report template. Negative-example tests are mandatory in every scenario except `clean/`.
- **New test files (fixtures)**: 9 new directories, each with one `.py` file and one `expected-findings.md`. No new `.py` files outside `tests/fixtures/audit/`.

## Implementation Plan

The plan is **fixture-first, SKILL-second, verify-third**, mirroring how the 6 already-supported smells were onboarded in the prior task. Each fixture is independent; SKILL.md edits are batched at the end.

### Phase A — Stubbing (TDD prep)

1. **Stub all 9 fixture directories.**
   - Files: `tests/fixtures/audit/<slug>/expected-findings.md` and `tests/fixtures/audit/<slug>/test_<scenario>.py` for each of the 9 slugs.
   - Changes: Create empty files (or minimal headers only) for each. No assertions, no plants yet — this is the "stub all tests with empty bodies" TDD step.

2. **Stub SKILL.md table and natural-phrase entries.**
   - Files: `skills/slobac-audit/SKILL.md`.
   - Changes: Add 9 rows to the supported-smells table and 9 bullets to the natural-phrase intent-mapping list, all with placeholder `TBD` content. This stubs the "interface" the orchestrator exposes to the operator.

3. **Stub `tests/fixtures/audit/README.md` parity section.**
   - Files: `tests/fixtures/audit/README.md`.
   - Changes: Add a new subsection header "Scenarios added for taxonomy parity (Phase 3)" with stub bullets.

### Phase B — Per-smell fill-in (one TDD cycle per smell)

Each step is one TDD cycle: write `expected-findings.md` (the spec / "test"), then plant `test_<scenario>.py` (the input that satisfies the spec). Smells are listed in canonical-entry severity order to keep the highest-impact work first.

4. **`tautology-theatre`** (Critical severity).
   - Files: `tests/fixtures/audit/tautology-theatre/expected-findings.md`, `tests/fixtures/audit/tautology-theatre/test_<scenario>.py`.
   - Changes: At least 2 positive cases (mock-tautology shape + no-production-code shape) + 1 negative control (real SUT call with mock as collaborator). `expected-findings.md` prescribes **delete**, not transform.

5. **`pseudo-tested`** (High).
   - Files: `tests/fixtures/audit/pseudo-tested/expected-findings.md`, `tests/fixtures/audit/pseudo-tested/test_<scenario>.py`.
   - Changes: Positive case where a no-op SUT replacement still passes (e.g. "test_sanitize" asserts `result == input`) + negative control where a no-op replacement would fail (e.g. asserts derived value, not identity).

6. **`vacuous-assertion`** (High).
   - Files: `tests/fixtures/audit/vacuous-assertion/expected-findings.md`, `tests/fixtures/audit/vacuous-assertion/test_<scenario>.py`.
   - Changes: Positive case asserting `result is not None` against a function returning a complex parsed dict + negative control asserting structural equality on the same dict.

7. **`over-specified-mock`** (High).
   - Files: `tests/fixtures/audit/over-specified-mock/expected-findings.md`, `tests/fixtures/audit/over-specified-mock/test_<scenario>.py`.
   - Changes: Positive case using `mock.assert_called_once_with(...)` + exact-arg pinning + call-count assertion + negative control using only outcome-based assertions.

8. **`implementation-coupled`** (High).
   - Files: `tests/fixtures/audit/implementation-coupled/expected-findings.md`, `tests/fixtures/audit/implementation-coupled/test_<scenario>.py`.
   - Changes: Positive case reaching `sut._private_method()` or `sut.__internal_state` + negative control using only public API.

9. **`presentation-coupled`** (Medium).
   - Files: `tests/fixtures/audit/presentation-coupled/expected-findings.md`, `tests/fixtures/audit/presentation-coupled/test_<scenario>.py`.
   - Changes: Positive case asserting full-string equality on rendered HTML/log/markdown + negative control parsing structure (e.g. `json.loads`) and asserting on parsed shape.

10. **`conditional-logic`** (Medium).
    - Files: `tests/fixtures/audit/conditional-logic/expected-findings.md`, `tests/fixtures/audit/conditional-logic/test_<scenario>.py`.
    - Changes: 2 positive cases (`if X: assert(...)` shape + `try/except` without trailing `assert.fail` shape) + negative control using parameterized inputs to express the same intent.

11. **`mystery-guest`** (Low).
    - Files: `tests/fixtures/audit/mystery-guest/expected-findings.md`, `tests/fixtures/audit/mystery-guest/test_<scenario>.py`, `tests/fixtures/audit/mystery-guest/<fixture-data-file>`.
    - Changes: Positive case loading external fixture file then asserting magic count (`len(rows) == 6`) with no inline hint + negative control using inline literal data with derived expectation.

12. **`rotten-green`** (Low).
    - Files: `tests/fixtures/audit/rotten-green/expected-findings.md`, `tests/fixtures/audit/rotten-green/test_<scenario>.py`.
    - Changes: 2 positive cases (empty body with `pass` only + dead fixture declared and never read) + negative control with real assertion on real SUT call.

### Phase C — SKILL.md fill-in

13. **Replace SKILL.md placeholders with real content.**
    - Files: `skills/slobac-audit/SKILL.md`.
    - Changes: For each of the 9 stub rows from step 2, fill in the natural-language phrases derived from each taxonomy entry's vocabulary (`vacuous-assertion` — "weak oracle", "weak assertion", "many wrong answers pass"; `tautology-theatre` — "mock tautology", "no production code", "would-still-pass-with-prod-deleted"; etc.). Confirm the supported-smells table rows have correct `Detection Scope: per-test` per the verified taxonomy headers.

14. **Update `tests/fixtures/audit/README.md` parity section.**
    - Files: `tests/fixtures/audit/README.md`.
    - Changes: Replace the stub bullets from step 3 with a one-line description per fixture in the "Scenarios added for taxonomy parity (Phase 3)" subsection.

15. **Update `skills/slobac-audit/README.md` to reflect parity.** *(amended in by preflight — was a missed touchpoint.)*
    - Files: `skills/slobac-audit/README.md`.
    - Changes:
        - L3 lead paragraph: promote "Supports 6 smells across 3 detection scopes" → "Supports 15 smells across 3 detection scopes".
        - Supported-smells table (currently L11–16): add 9 new rows mirroring the same shape used for the existing 6, keeping rows grouped by detection scope (per-test rows together, then per-file, then cross-suite).
        - Smoke-test fixtures list (currently L139–152): add 9 new smoke-test items (one per new fixture), each citing `tests/fixtures/audit/<slug>/` and a short expected-finding-count summary derived from the new `expected-findings.md`.
        - Constraints disclaimer (currently L158): rewrite from "6 smells supported. Any request for other smells (`tautology-theatre`, `vacuous-assertion`, etc.) is refused…" to a parity-reached statement noting that all 15 taxonomy entries are now first-class supported, and any future taxonomy additions will be onboarded the same way (refusal behavior preserved, but the example slugs change to a generic placeholder rather than slugs that are about to become supported).
        - Example tree (currently L53–54): extend the illustrative `taxonomy/` listing if it visibly under-represents the current set; otherwise leave it (the tree is illustrative, not exhaustive).

16. **Update `memory-bank/techContext.md` smell count.**
    - Files: `memory-bank/techContext.md`.
    - Changes: Promote "6 smells across 3 detection scopes" → "15 smells across 3 detection scopes"; expand the per-test list inline to include all 11 per-test slugs (the existing 2 plus the 9 newly onboarded).

### Phase D — Mechanical verification

17. **`uv run properdocs build --strict`.**
    - Files: none modified.
    - Changes: Verify the docs build remains green. **Note (preflight advisory):** No `references/docs/` files are edited in this plan, so properdocs is a *negative control* gate — it will not exercise the SKILL.md / READMEs / techContext edits directly. Run anyway as a regression safety net.

18. **Manual consistency review.**
    - Files: none modified.
    - Changes:
        - Skim each `expected-findings.md` against its taxonomy entry's "Prescribed fix" section to confirm the prescribed remediation arms match.
        - Skim `slobac-audit/SKILL.md` final state to confirm the 6 already-supported slugs are unchanged in their existing rows and bullets.
        - Skim `slobac-audit/README.md` final state to confirm the smoke-test list and supported-smells table count match the SKILL.md state (single source of truth in SKILL.md; README mirrors).
        - Grep-verify that the count "15" and the count "6" do not coexist in any of the four updated documents — every "6 smells" string must be promoted or removed.

## Technology Validation

No new technology — validation not required. All edits are markdown and Python source; the build/lint gates already in CI cover the changed surface.

## Dependencies

- The 9 taxonomy entries at `skills/slobac-audit/references/docs/taxonomy/<slug>.md` (already exist and already carry `Detection Scope: per-test` headers — verified during planning).
- The audit report template at `skills/slobac-audit/references/report-template.md` (unchanged).
- The fixture convention documented in `tests/fixtures/audit/README.md` (extending, not changing).
- `properdocs` toolchain pinned in `pyproject.toml` / `uv.lock`.

## Challenges & Mitigations

- **Risk of slug-vocabulary drift between SKILL.md and taxonomy entries.** Mitigation: derive natural-phrase mappings directly from each taxonomy entry's Summary + Description sections during step 13; do not invent vocabulary that has no anchor in the manifesto.
- **Risk of false-positive fixtures (planting tests that *also* exhibit a sibling smell).** Mitigation: each fixture's `expected-findings.md` lists only its own smell's findings; if cross-cutting shape is unavoidable, document it explicitly in the "Tests that must NOT be flagged" section as an intentional cross-citation — never silently.
- **Risk of fixture-shape inconsistency across the 9 new scenarios.** Mitigation: copy the structure from `tests/fixtures/audit/naming-lies/expected-findings.md` (which is the most polished existing per-test fixture) as a structural template for each new `expected-findings.md`.
- **Risk that `properdocs build --strict` fails on a new taxonomy cross-link.** Mitigation: no taxonomy file edits are planned; the only manifesto-tree change is the SKILL.md table/intent-map (which lives under `skills/slobac-audit/` but is not a `docs/` file). If the strict build still complains on rendered nav, fix per the existing markdown-style and cross-link conventions in `.cursor/rules/shared/markdown-style.mdc`.
- **Risk of the 9-smell scope masquerading as L3.** Mitigation: re-evaluated explicitly — no new components, no design decisions, no cross-cutting concerns. Each fixture is a paste-and-modify of an existing fixture's shape. The work is wide but shallow. If during build a smell's fixture turns out to require new architectural support (e.g. a new detection-scope variant), STOP and re-level.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight (PASS with 1 amendment + 2 advisories)
- [x] Build (PASS — 18 steps complete; 1 documented deviation; 1 straggler caught and fixed during step 18)
- [x] QA (PASS — 1 substantive deficiency caught and fixed inline: rotten-green fixture's planted `# TODO` comment was missing)

## Preflight Amendments & Advisories

**Amendment (2026-05-03):** Added step 15 — `skills/slobac-audit/README.md` was a missed touchpoint. It mirrors SKILL state (smell count, supported table, smoke-test list, constraints disclaimer) and would have gone stale if not updated. Behavior B6b added to TDD plan. Step renumbering: previous steps 15→16, 16→17, 17→18.

**Advisory 1 — properdocs is a negative-control gate for this task:** Of the four documents this task edits (SKILL.md, two READMEs, techContext.md), zero live under `skills/slobac-audit/references/docs/` (the properdocs `docs_dir`). The strict-build check therefore validates only that nothing else in the manifesto regresses. The actual mechanical gate for *this* task is grep + manual visual review per step 18. Not a blocker — pre-existing to the framework.

**Advisory 2 — multi-scope combined fixture remains deferred:** The prior task's preflight noted absence of a multi-scope combined fixture as a non-blocking advisory. That advisory is unchanged by this task; remains future work and is explicitly out of scope per the project brief.

**Radical-innovation note (advisory only, not adopted):** Once parity is reached, the README.md "constraints disclaimer" L158 example slugs (`tautology-theatre`, `vacuous-assertion`) will be wrong. Step 15 rewrites them to generic placeholders. A more radical move would be to delete the disclaimer entirely on the grounds that "refuse unsupported slugs" is now hypothetical (no slugs are unsupported). Rejected for this task: the refusal behavior is still the contract for *future* taxonomy additions, and removing the disclaimer would make that contract invisible. Re-evaluate if the manifesto stops growing.
