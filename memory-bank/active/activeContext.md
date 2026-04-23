# Active Context

**Current Task:** Phase 1 Audit MVP — `deliverable-fossils` + `naming-lies` as harness-portable agent customizations for Cursor and Claude Code.

**Phase:** PLAN (re-entered post-reflect; rework in progress)

## Rework In Progress

The operator surfaced a portability defect after Reflect: the shipped skill references `docs/taxonomy/<slug>.md` via paths that cross its own root directory (`../../../../docs/...` from inside `skills/slobac-audit/references/smells/*.md`, and the SKILL.md "read docs at runtime" step). AgentSkills.io skills are self-contained — their runtime root is wherever they're installed (`~/.claude/skills/slobac-audit/` on an external machine, a user-level Cursor install, etc.) — so the cross-root reference breaks on every real install.

OQ2's creative decision (Option D: docs canonical, skill reads both files at runtime) is invalidated. A new invariant (**#11 Skill-root self-containment**) has been codified in tasks.md so the constraint isn't missed again. OQ2-redux is open; creative phase pending. Affected implementation steps: 7 (SKILL.md workflow), 8–9 (per-smell augmentation files), 11 (README language), 13 (techContext pattern). Preserved: OQ1, all fixtures, the report template, the five-field per-finding invariant, the invocation UX.

## What Was Done (cumulative, including pre-rework)

- Complexity analysis: Level 3 (Intermediate Feature).
- Plan phase: component analysis, invariant checklist, TDD test plan, 14-step implementation plan, challenges, technology validation note, all in [`tasks.md`](./tasks.md).
- Creative phases: OQ1 (ur-Skill + per-smell references) and OQ2 (docs canonical; skill carries augmentation only; agent reads both files). Both high confidence.
- Preflight: PASS with two implementation amendments applied inline (report default path; always-present augmentation file) and one advisory raised (report versioning).
- Build: all plan steps executed except step 10 (marked unneeded at plan time) and step 14 (conditional pivot; not triggered — the manifesto's Signals sections were sufficient for both Phase-1 smells without extension).

## Build artefacts — files created

### Audit skill (canonical source)

- `skills/slobac-audit/SKILL.md` — ur-workflow (primitive-agnostic prose). Scope parsing with Phase-1-only supported slugs (`deliverable-fossils`, `naming-lies`), explicit out-of-scope refusal, per-smell two-file read, detection loop, report emission, read-only guard.
- `skills/slobac-audit/README.md` — operator-facing install + smoke-test instructions.
- `skills/slobac-audit/references/report-template.md` — audit report shape: top-level sections (Summary, Findings, Tests considered but not flagged, Out-of-scope requests) + per-finding five-field shape (Location, Smell, Rationale, Prescribed remediation, Why this isn't a false positive).
- `skills/slobac-audit/references/smells/deliverable-fossils.md` — audit-specific augmentation: invocation phrases, emission hints (rename encodes behavior not fossil label; Phase-A vs Phase-B decision), false-positive guards (refactor-in-body, ticket-as-provenance, domain vocabulary collisions).
- `skills/slobac-audit/references/smells/naming-lies.md` — audit-specific augmentation: invocation phrases, three-arm decision rules (RENAME / STRENGTHEN / INVESTIGATE), false-positive guards (cross-language synonymy, domain synonymy, under-specified titles, failure-case tests).

### Fixture suites

- `tests/fixtures/audit/README.md` — fixture convention.
- `tests/fixtures/audit/deliverable-fossils/test_plugin_registry.py` + `expected-findings.md` — 5 tests, 4 expected flags, 1 negative example (refactor-safety body).
- `tests/fixtures/audit/naming-lies/test_session_lifecycle.py` + `expected-findings.md` — 4 tests, 3 expected flags (one per fix arm: RENAME, STRENGTHEN, INVESTIGATE), 1 negative example (cross-language synonymy: `deletes` ↔ `DELETE FROM`).
- `tests/fixtures/audit/both-smells/test_mixed.py` + `expected-findings.md` — 4 tests exercising scope; one test exhibits both smells and must emit two findings under scope `all`.
- `tests/fixtures/audit/clean/test_example.py` + `expected-findings.md` — 3 tests with zero expected findings; false-positive gate.

### Documentation updates

- `README.md` (repo root) — added Audit capability section linking to the skill README and fixtures.
- `memory-bank/techContext.md` — documented the skill layout, canonical-docs-referenced-from-skill pattern, and fixture directory.

## Key implementation decisions during build (not in creative docs)

- **Report clobber-avoidance.** If `slobac-audit.md` already exists at the chosen path, emit at `slobac-audit-2.md`, `-3.md`, etc. rather than overwriting a prior report. Prevents silent loss of an earlier audit and is cheap in the template.
- **Finding-level five-field invariant.** The report template codifies that every finding carries all five fields (Location, Smell, Rationale, Prescribed remediation, Why this isn't a false positive). A finding missing any field is structurally invalid. This is the build-phase translation of the preflight-raised "machine-consistent enough for a future JSON extraction" requirement.
- **Cross-language synonymy as a named false-positive class.** The naming-lies augmentation names cross-language synonymy (English-verb ↔ SQL-keyword, etc.) explicitly because token-level matching alone will over-trigger. Corresponding negative example (`test_closing_a_session_deletes_its_row`) is planted in the naming-lies fixture to stress-test the guard.
- **Fossil vocabulary as signal-not-verdict.** The deliverable-fossils augmentation codifies that words like `refactor` and ticket IDs are signals, not verdicts. Corresponding negative example (`test_refactor_preserving_rename_does_not_change_lookup_results`) tests whether the audit distinguishes "refactor in title, refactor property in body" from "refactor in title, unrelated body."

## Deviations from plan

- None architectural. Step 14 (mid-build taxonomy-entry extension) was conditional and not triggered — the manifesto's existing Signals sections for both `deliverable-fossils` and `naming-lies` were sufficient to back the Phase-1 detection prose.
- Step 10 (tech validation) was pre-marked as unneeded at plan time; build did not revisit.
- Step 12 (manual validation in each harness) is operator-driven; the plan explicitly states it is not a gate to ship but a gate to declare behaviorally correct. Deferred to the operator.

## Integration check results

- **`properdocs build --strict`:** clean. No broken cross-links in `docs/`. Build step did not touch `docs/`; invariant preserved.
- **Python fixture parse check:** all 4 fixture files parse as valid Python 3.
- **Link-depth audit:** all relative links from new markdown files (`skills/**`, `tests/fixtures/audit/**`) to `docs/taxonomy/<slug>.md` and `docs/principles.md` resolved correctly after fixing four initially-incorrect links in the fixture `expected-findings.md` files.

## QA outcome

PASS with one trivial fix (removed preflight-advisory `Skill version` field that was scope-crept into the report template). Full report in [`.qa-validation-status`](./.qa-validation-status).

## Reflection outcome

Written to [`reflection/reflection-phase-1-audit-mvp.md`](./reflection/reflection-phase-1-audit-mvp.md). Key insights: prompt-artifact TDD worked (fixture-first discipline reshaped augmentation prose); the five-field per-finding invariant is the report's quality lever; structural enforcement of manifesto-independence (OQ2) made QA's DRY check collapse to one line; "preflight advisory not applied" is an ambiguous state that leaked scope during build and was caught by QA.

Persistent memory-bank files reconciled: `systemPatterns.md` updated to reflect that the project is no longer "pre-code, docs-only"; `productContext.md` open-questions paragraph updated to reflect Phase-1 resolutions. `techContext.md` was already updated during build (Step 13).

## Next step

**Creative phase for OQ2-redux.** The rework hinges on how the skill carries (or synthesises) canonical content it can no longer read from outside its own root. Candidates span a generator + drift-check CI gate (Option E), a role-split operational playbook with hand-authored overlap (Option H), a vendored copy with manual sync discipline (Option K), and runtime network fetch (Option J). Given that the previous OQ2 creative pass missed the skill-root self-containment constraint, OQ2-redux should go through creative with an airtight bar rather than being pre-answered at plan time.

PLAN PHASE (rework) — creative pending for OQ2-redux
