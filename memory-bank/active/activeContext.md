# Active Context

**Current Task:** Phase 1 Audit MVP — `deliverable-fossils` + `naming-lies` as harness-portable agent customizations for Cursor and Claude Code.

**Phase:** PLAN (second rework) COMPLETE — next phase Preflight (operator-gated per L3 workflow)

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

## Rework plan summary (post-creative)

OQ2-redux resolved to **Option E**: generator + drift-check CI gate, two-directory skill layout. `docs/taxonomy/<slug>.md` stays canonical; `scripts/sync-taxonomy.py` (new, stdlib-only Python) regenerates `skills/slobac-audit/references/taxonomy/<slug>.md` as verbatim copies with "do not hand-edit" headers; a CI job runs `--check` mode on PRs and fails on drift. The hand-authored `skills/slobac-audit/references/smells/<slug>.md` files survive in their original role (audit-specific augmentation only). SKILL.md's per-smell workflow reads both files — both inside the skill root.

**Rework implementation steps (R1–R11):** R1 authors the generator; R2 produces the 15 taxonomy copies (all of the manifesto, for Phase-2 readiness even though only two smells are active); R3 adds the CI drift-gate; R4–R6 rewrite SKILL.md, the augmentation files, and the README; R7–R8 update memory-bank `techContext.md` and `systemPatterns.md`; R9 is the operator-run manual validation re-execution; R10 is the one-time invariant #11 spot-check; R11 amends reflection insight #2 to retract the misplaced "high confidence" claim.

**Calibration-debt from the failed prior OQ2:** explicitly carried into the creative doc and tasks.md Challenges section. The next SLOBAC architectural claim should be treated with extra scrutiny until a few more decisions land cleanly.

## Preflight outcome (rework)

**PASS with amendments.** The plan's R4/R5/R6 undercounted cross-root references inside `skills/slobac-audit/**`; a grep surfaced six additional locations the plan did not name. Amendments applied inline: R4 split 4-way, R5 split 3-way, R5a added, R6 split 4-way, R1 and R10 clarified. All cross-root references are now covered. Three advisories not applied (scripts-dir convention, CI-job placement latitude, smells-manifest as Phase-2 entry-point candidate). Full report in `.preflight-status`.

## Build outcome (rework)

**PASS.** All 11 authored rework steps executed:

- **R1–R2** — `scripts/sync-taxonomy.py` authored (stdlib-only; no `pyproject.toml` deps added). Two modes: default (write outputs) and `--check` (diff against committed). Generator ran clean and produced 15 verbatim taxonomy copies under `skills/slobac-audit/references/taxonomy/` with a fixed "GENERATED FILE — do not hand-edit" header naming the source path and regeneration command.
- **R3** — CI drift-check step added to `.github/workflows/docs.yaml` build job (PF4 advisory applied: colocated to reuse the bootstrapped `uv` env). Runs on every PR build per the existing `docs.yaml` triggers.
- **R4** — SKILL.md: workflow step (4a) now reads `references/taxonomy/<slug>.md` + `references/smells/<slug>.md`, both inside the skill root; scope header (4b) intra-skill links; governor-rule cite (4c) rewritten to published URL (`https://texarkanine.github.io/slobac/principles/#preservation-of-regression-detection-power`); catch-all (4d) confirmed clean via rg.
- **R5** — both per-smell augmentation files: preamble rewrites (5a) point at the sibling generated taxonomy file; intra-manifesto cross-refs (5b, `semantic-redundancy` from fossils, `vacuous-assertion` from naming-lies) rewritten as `../taxonomy/<slug>.md` (both exist after R2's full-manifesto walk); principle ref (5c, `behavior-articulation-before-change` from naming-lies) rewritten to a published URL.
- **R5a** — `references/report-template.md` rationale instruction now cites `references/taxonomy/<slug>.md` for the agent-facing citation and instructs the agent to emit a published `https://texarkanine.github.io/slobac/taxonomy/<slug>/` URL in the report for human readers.
- **R6** — `skills/slobac-audit/README.md`: scope links (6a) become `https://texarkanine.github.io/slobac/taxonomy/<slug>/`; runtime-reads paragraph (6b) replaced by a self-contained-bundle paragraph describing the generator + CI gate and updated with a new `references/taxonomy/` row in the layout tree; the user-level-install caveat paragraphs are now "no caveats"; fixture links (6c) become absolute GitHub URLs; the obsolete "skill cannot find docs/taxonomy/<slug>.md" paragraph (6d) deleted and replaced by a drift-gate troubleshooting entry.
- **R7** — `memory-bank/techContext.md`: "Canonical-docs-referenced-from-skill pattern" section replaced by "Generator-synchronised skill-bundle pattern"; generator behavior and CI-gate mechanism documented; the new `references/taxonomy/` directory added to the layout description.
- **R8** — `memory-bank/systemPatterns.md`: invariant #11 (Skill-root self-containment) added as a dedicated section codifying both the constraint and the post-rework discipline that produced it. The opening "How This System Works" paragraph rewritten: manifesto-independence is now described as procedural (generator + CI gate), not structural, with an explicit pointer to the techContext pattern name.
- **R10** — structural spot-check: `rg '\]\(\.\./\.\./' skills/slobac-audit/` returns zero; SKILL.md / report-template / augmentation files / README have zero cross-root markdown links; the only `../principles.md#...` / `../glossary.md#...` references live inside generated `references/taxonomy/*.md` files and are inert verbatim content per the R1 link-handling policy, explicitly excluded from invariant-#11 enforcement.
- **R11** — reflection insight #2 retracted inline with a calibration note; Summary section and Cross-Phase Analysis insight #2 also updated with companion retractions; other reflection insights preserved.
- **R9** — operator-run harness validation deferred per plan; not a ship gate.

**Deviations from plan:** none. PF4's "add to existing docs job vs parallel job" choice resolved in favor of same-job co-location (uv cache reuse). PF3 (scripts-dir convention) and PF5 (smells-manifest) remain unapplied per preflight; not blocking.

**Artefacts created or modified during build:**

- NEW: `scripts/sync-taxonomy.py` (stdlib-only generator + drift-check)
- NEW: `skills/slobac-audit/references/taxonomy/*.md` (15 generated files, one per manifesto entry)
- MOD: `.github/workflows/docs.yaml` (drift-check step added)
- MOD: `skills/slobac-audit/SKILL.md` (4 edits per R4)
- MOD: `skills/slobac-audit/references/report-template.md` (R5a)
- MOD: `skills/slobac-audit/references/smells/deliverable-fossils.md` (R5a + R5b)
- MOD: `skills/slobac-audit/references/smells/naming-lies.md` (R5a + R5b + R5c)
- MOD: `skills/slobac-audit/README.md` (R6a–R6d plus install-caveat paragraphs)
- MOD: `memory-bank/techContext.md` (R7)
- MOD: `memory-bank/systemPatterns.md` (R8 + invariant-#11 section)
- MOD: `memory-bank/active/reflection/reflection-phase-1-audit-mvp.md` (R11 + companion retractions)

## Second Rework Context (post-build-2 re-entry)

The shipped Option-E architecture from the first rework (generator + drift-check CI gate; generated `references/taxonomy/*.md` verbatim copies; hand-authored `references/smells/*.md` augmentation files) was rejected by the operator post-build on two load-bearing objections:

1. Committing generated code is itself architecturally a smell — even with a drift-gate, the bundle carries derivative content and the "remember to regenerate before commit" ritual is exactly the kind of out-of-band discipline that silently rots.
2. The augmentation files are ~35–60% restatement of the manifesto entries. An editor updating the manifesto has no structural prompt to open the augmentation file, so the restated content silently drifts.

**Root cause (shared):** the first rework's creative phase (OQ2-redux) preserved the premise that `docs/taxonomy/*.md` is the authoring source of truth *while* satisfying invariant #11. The only way to satisfy both is copy-with-sync-discipline. Option E was a competent instance; the pattern itself is the problem.

**Operator's corrective direction:** invert canonicality. Skill bundle holds the canonical taxonomy; `docs/taxonomy/*.md` becomes a thin `pymdownx.snippets`-include wrapper. Explicit new constraint: **nobody reads `docs/*.md` directly** — the rendered properdocs site is the reader surface. This eliminates the original OQ2 objection that had previously killed snippet-based options.

## Second Rework Plan Summary (post-creative)

**OQ3 resolved to Option γ — definitional canonical + discursive wrapper.** The canonical (`skills/slobac-audit/references/docs/taxonomy/<slug>.md`, 15 files) carries every section of the smell's definition: Summary, Description, Signals, **False-positive guards** (new first-class section, promoted from the augmentation files), Prescribed Fix, Example, Related modes, Polyglot notes. The wrapper (`docs/taxonomy/<slug>.md`) is usually just a snippet-include directive; optional reader-framing prose can wrap the snippet when an author consciously wants it. For Phase-1 scope (2 smells), all wrappers are bare. For the 13 non-Phase-1 smells, canonical content migrates verbatim via `git mv`; a stub False-positive guards section is added to each with a "Phase-2 per-smell work will author these" marker. Augmentation files are **deleted**; guards migrate to canonical, invocation phrases migrate to SKILL.md, restated manifesto content is dropped. See [`creative/creative-canonical-entry-shape.md`](./creative/creative-canonical-entry-shape.md).

**Second-rework implementation steps (S1–S14):** S1 `git mv` migration of 15 manifesto entries to new canonical path; S2 thin snippet-include wrappers at `docs/taxonomy/*.md`; S3 Phase-1 false-positive-guards promotion; S4 stub guards for 13 non-Phase-1 entries; S5 SKILL.md workflow + scope-parsing rewrite (inline invocation vocabulary migrated from augmentation files); S6 delete `references/smells/`; S7 delete `scripts/sync-taxonomy.py` + generated `references/taxonomy/*` + CI drift-check step; S8 report-template path update; S9 README rewrites; S10–S11 memory-bank techContext + systemPatterns updates (invariant #3 wording revision; invariant #11 now structurally enforced; new "Canonical-in-bundle" pattern); S12 reflection second-retraction note; S13 operator-run harness validation; S14 `properdocs build --strict` gate.

**Recurring-calibration debt:** this is the third OQ2 pass. Each prior decision met its enumerated constraints and missed a later-surfaced one. Creative doc flags this explicitly and recommends a Phase-2 creative-phase discipline hedge: "what will the operator's first reaction to the shipped artefact be, and can we surface that objection now?" as a checklist item before declaring high confidence.

## Artefact impact (second rework)

- **DELETE:** `scripts/sync-taxonomy.py`, `skills/slobac-audit/references/taxonomy/*.md` (15 files), `skills/slobac-audit/references/smells/*.md` (2 files), `.github/workflows/docs.yaml` drift-check step.
- **NEW:** `skills/slobac-audit/references/docs/taxonomy/*.md` (15 files via `git mv` from `docs/taxonomy/`; Phase-1 entries gain `## False-positive guards` sections).
- **REWRITE:** `docs/taxonomy/*.md` (15 files → thin snippet-include wrappers).
- **MOD:** `skills/slobac-audit/SKILL.md` (workflow single-file read; inline invocation vocabulary); `skills/slobac-audit/references/report-template.md` (path update); `skills/slobac-audit/README.md` (layout, runtime paragraph, drift-gate troubleshooting removed); `memory-bank/techContext.md` (new "Canonical-in-bundle" pattern); `memory-bank/systemPatterns.md` (invariant #3 wording; invariant #11 clarified; new authoring-model subsection); `memory-bank/active/reflection/reflection-phase-1-audit-mvp.md` (second-retraction note).

## Next step

Preflight (second rework) runs per operator invocation per L3 workflow.

PLAN PHASE (second rework) — PASS; awaiting operator input to enter Preflight
