# Task: Author False-Positive Guards Across Taxonomy

* Task ID: taxonomy-fp-guards
* Complexity: Level 2
* Type: Documentation enhancement (manifesto authoring)

Author the `## False-positive guards` section for the 13 taxonomy smell docs that currently carry the placeholder `No audit-specific guards yet; Phase-2 per-smell work will author these.`, sourcing high-confidence guards from `planning/research/` and matching the form already in `naming-lies.md` and `deliverable-fossils.md`. Bias toward concise, evidenced, per-smell guards; do not elide guards the research clearly supports.

## Test Plan (TDD)

> **TDD adaptation note.** This is documentation authoring; there is no executable test target for the *content* of a guard. The "test" of a guard is editorial: it must satisfy a fixed checklist before it's accepted. The mechanical gate is `properdocs build --strict`.

### Behaviors to Verify

For **each** of the 13 edited files, the `## False-positive guards` section must satisfy:

- **Section preserved** — the section heading remains; the placeholder line is replaced (per CONTRIBUTING.md "fill them in or leave the stub; do not delete the section heading").
- **Per-guard form match** — each guard is a `- **Name for over-trigger class.** Description and decision rule.` bullet, matching the shape used in `naming-lies.md` and `deliverable-fossils.md` and prescribed by `CONTRIBUTING.md` §entry-shape.
- **Per-smell scoping** — every guard names a class of false positive **specific to this smell's signals**, not a generic disclaimer (e.g. "be careful with LLM judgment") that would apply to any smell.
- **Evidence-backed** — every guard is traceable to material in `planning/research/` (synthesis report or per-model FINDINGS). For each authored guard, an evidence note exists in the per-smell working index (Step 1 of the implementation plan); guards without corpus support are not authored.
- **Don't-elide check** — guards the corpus clearly supports are not dropped for terseness. The "concise" constraint trims wording, not coverage.
- **No link breakage** — any cross-reference (`../principles.md#anchor`, `../glossary.md#term`, sibling taxonomy entries) resolves; verified by `uv run properdocs build --strict`.

### Edge Cases

- **Thin corpus.** A smell whose corpus material is sparse or low-confidence: the working index is empty/weak. Behavior: do **not** invent guards; record this in the index, surface it to the operator at QA time, and either ship the placeholder unchanged for that smell or ship with a smaller set than peers — explicitly flagged.
- **Cross-smell guards.** Material in the corpus that argues for the same false-positive class across multiple smells (e.g. "LLM-generated tests look smelly by surface metrics but score worse semantically" — Panichella 2023). Behavior: place the guard on each smell where the audit's signals would actually over-trigger; do not promote it to a non-smell-scoped doc.
- **Existing exemplars.** `naming-lies.md` and `deliverable-fossils.md` are out of scope. Behavior: do **not** edit; their form is the calibration target.
- **Anchor drift.** A guard wants to cite a principle/glossary anchor that doesn't exist. Behavior: use plain prose rather than fabricate an anchor; `properdocs build --strict` enforces this.

### Test Infrastructure

- Framework: `uv run properdocs build --strict` (per CONTRIBUTING.md §"After adding an entry"). This is the only mechanical gate; the rest of the verification is the editorial checklist above, executed at QA time against each edited file.
- Test location: not applicable — this is doc-build verification, not unit tests.
- Conventions: section shape per `CONTRIBUTING.md`; tone and bullet form per `naming-lies.md` / `deliverable-fossils.md`.
- New test files: none.

## Implementation Plan

Steps are sequenced so the corpus is read once (Step 1) and then drawn from per-smell (Steps 2–14). Steps 2–14 share an identical sub-cycle — listed once in Step 2 and referenced thereafter — to avoid restating it 13 times.

1. **Build a per-smell evidence index from the research corpus.**
   - Files read: `planning/research/report.md`, `planning/research/FINDINGS-CLAUDE.md`, `planning/research/FINDINGS-CODEX.md`, `planning/research/FINDINGS-COMPOSER.md`, `planning/research/FINDINGS-GEMINI.md`, `planning/research/FINDINGS-GROK.md`.
   - Output: an in-conversation working note (not a checked-in artifact) with one section per smell. Each section holds: bullet list of false-positive classes mentioned in the corpus, with a short evidence pointer (file + topic). If a smell has thin/no corpus support, mark it explicitly.
   - This step exists so Steps 2–14 are corpus-write operations, not corpus-read operations.

2. **Author guards for `semantic-redundancy.md`.** (Sub-cycle, identical for every smell file in Steps 2–14.)
   - Files: `skills/slobac-audit/references/docs/taxonomy/semantic-redundancy.md`.
   - Changes:
     1. Re-read the file so the new section sits alongside the existing Signals and Description content without contradiction.
     2. From the per-smell index entry built in Step 1, draft 1–4 guards. Each guard is one bullet: bolded name + one-to-three-sentence decision rule, in the form of `naming-lies.md` / `deliverable-fossils.md`.
     3. Apply the **don't-elide** check: every corpus-supported false-positive class is represented by a guard.
     4. Apply the **concise** check: tighten wording without dropping classes.
     5. Replace the placeholder paragraph (`No audit-specific guards yet; Phase-2 per-smell work will author these.`) with the authored guard list. Preserve the `## False-positive guards` heading and any intro sentence already present (none, in the stubbed files).
3. **Author guards for `wrong-level.md`.** Apply Step 2's sub-cycle.
4. **Author guards for `vacuous-assertion.md`.** Apply Step 2's sub-cycle.
5. **Author guards for `pseudo-tested.md`.** Apply Step 2's sub-cycle.
6. **Author guards for `tautology-theatre.md`.** Apply Step 2's sub-cycle.
7. **Author guards for `over-specified-mock.md`.** Apply Step 2's sub-cycle.
8. **Author guards for `implementation-coupled.md`.** Apply Step 2's sub-cycle.
9. **Author guards for `presentation-coupled.md`.** Apply Step 2's sub-cycle.
10. **Author guards for `conditional-logic.md`.** Apply Step 2's sub-cycle.
11. **Author guards for `shared-state.md`.** Apply Step 2's sub-cycle.
12. **Author guards for `mystery-guest.md`.** Apply Step 2's sub-cycle.
13. **Author guards for `rotten-green.md`.** Apply Step 2's sub-cycle.
14. **Author guards for `monolithic-test-file.md`.** Apply Step 2's sub-cycle.

   Order rationale: catalog order from `taxonomy/README.md`, skipping the two already-authored entries (`deliverable-fossils`, `naming-lies`). This means the smells-most-dependent-on-semantic-judgment are written first, while the corpus index from Step 1 is freshest.

15. **Run `uv run properdocs build --strict` from the repo root.** Required to pass per CONTRIBUTING.md §"After adding an entry". Any anchor or cross-link warning is a build failure to fix in place before QA.

16. **Editorial cross-pass.** Re-read the 13 edited sections back-to-back. Confirm tone and structure are uniform with `naming-lies.md` and `deliverable-fossils.md`; confirm no guard is a generic LLM disclaimer; confirm the don't-elide check still holds after any concision edits. Adjust in-place.

17. **No code-comment / README updates required.** `CONTRIBUTING.md` already documents the section shape; the `taxonomy/README.md` catalog already lists all 15 smells; nothing about the *task* changes either. (Documentation update step is included per the workflow's "Documentation changes are implementation work" rule and is explicitly empty here, justified.)

## Technology Validation

No new technology — validation not required. `uv` and `properdocs` are already used by CI per `memory-bank/techContext.md` §"Build Tools".

## Dependencies

- Read access to `planning/research/` (already in repo).
- `uv run properdocs build --strict` works locally — verified at Step 15. If `uv` is missing on this machine, fall back to "best-effort visual link verification" (grep for the cited anchors against `principles.md` / `glossary.md`) and flag the missing local gate to the operator.

## Challenges & Mitigations

- **Corpus is uneven across smells.** The synthesis `report.md` is shape-of-the-field, not per-smell guards; per-smell over-trigger material is more likely scattered across the 5 FINDINGS files. **Mitigation**: Step 1 explicitly produces a per-smell index before any authoring; if the index is weak for a smell, that smell ships with fewer guards (or a flagged placeholder), not invented ones.
- **Risk of inventing guards from intuition.** The user's stated constraint is evidenced-only. **Mitigation**: every authored guard carries an evidence pointer in the working index; QA pass cross-checks the pointer against the corpus.
- **Risk of editing into the placeholder text instead of replacing it.** The placeholder is one paragraph with no inline structure; partial edits would leave a malformed section. **Mitigation**: the sub-cycle's step 5 says "replace the placeholder paragraph" explicitly.
- **Risk of breaking cross-links by citing principle/glossary anchors that don't exist.** **Mitigation**: Step 15 runs `properdocs build --strict`; failures are fixed in place. Edge-case row above also says: prefer plain prose over fabricated anchors.
- **Re-level risk.** None expected — there's no architectural decision; the deliverable shape is fully prescribed by the two existing exemplars and CONTRIBUTING.md.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD, doc-adapted)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight
- [x] Build
- [ ] QA

## Build notes

- Step 1 (corpus index) executed in-conversation; per-smell evidence inventory drove every authored guard.
- Steps 2–14: each of the 13 stub sections replaced with 2–3 evidenced, per-smell, concise guards matching the form of `naming-lies.md` and `deliverable-fossils.md`.
- Step 15: `uv run --group docs properdocs build --strict` → exit 0, no warnings.
- Step 16: editorial cross-pass — all 13 sections satisfy form-match, per-smell scoping, evidence-traceability, and don't-elide. No revisions required.
- Step 17: docs-update step intentionally empty (CONTRIBUTING.md and `taxonomy/README.md` already document the section shape and the catalog).
- Deviations from plan: none.
- Distribution: 11 of 13 smells received the planned 2–3 guards; `wrong-level`, `vacuous-assertion`, `pseudo-tested`, `presentation-coupled`, `rotten-green`, and `monolithic-test-file` each ship with 2 (the strongest pair the corpus supports), per the plan's "ship a smaller flagged set rather than pad" rule. No smell shipped with zero — every smell had at least 2 corpus-supported guards once the index was built.
