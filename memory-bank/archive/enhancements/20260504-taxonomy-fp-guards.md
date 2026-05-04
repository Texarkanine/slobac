---
task_id: taxonomy-fp-guards
complexity_level: 2
date: 2026-05-04
status: completed
---

# TASK ARCHIVE: Author False-Positive Guards Across Taxonomy

## SUMMARY

Populated the `## False-positive guards` section for all 13 taxonomy smell docs that previously carried the Phase-2 placeholder, sourcing concise, per-smell guards from `planning/research/` (synthesis `report.md` plus five model FINDINGS files). Guards match the bullet form and editorial discipline of the existing exemplars `naming-lies.md` and `deliverable-fossils.md`. Mechanical verification: `uv run --group docs properdocs build --strict` passed with zero warnings (no broken anchors or cross-links).

## REQUIREMENTS

- **Uniform taxonomy.** Every listed smell doc carries a real guards section instead of the stub paragraph.
- **Concise, evidenced, don't elide.** Few sharp bullets per smell; only corpus-supported guards; do not drop a false-positive class the research clearly supports.
- **Per-smell scoping.** Each guard addresses over-triggering for that smell's signals, not generic LLM disclaimers.
- **Style match.** Same `- **Name.** Decision rule.` shape as the two pre-authored entries.
- **Out of scope honored.** Did not edit `naming-lies.md`, `deliverable-fossils.md`, or other sections of the smell entries beyond replacing the guards placeholder.

## IMPLEMENTATION

- **Corpus workflow.** Built a per-smell evidence index once from `report.md` and `FINDINGS-CLAUDE.md`, `FINDINGS-CODEX.md`, `FINDINGS-COMPOSER.md`, `FINDINGS-GEMINI.md`, `FINDINGS-GROK.md`, then authored each smell from that index (avoid repeated full corpus reads).
- **Files modified** (13 taxonomy entries under `skills/slobac-audit/references/docs/taxonomy/`): `semantic-redundancy.md`, `wrong-level.md`, `vacuous-assertion.md`, `pseudo-tested.md`, `tautology-theatre.md`, `over-specified-mock.md`, `implementation-coupled.md`, `presentation-coupled.md`, `conditional-logic.md`, `shared-state.md`, `mystery-guest.md`, `rotten-green.md`, `monolithic-test-file.md`.
- **Guard count.** Most smells received 2–3 guards; six smells shipped with 2 guards where the corpus supported only a strong pair—per plan, padding to three would have violated the evidence-only rule. No smell shipped with zero guards.
- **Cross-smell judgment.** Where the same fact appears in multiple smells (e.g. co-location conventions, dead suite setup), facts were restated in each smell's voice under the full-bundle pattern rather than generic cross-links—judgment stays per smell.

## TESTING

- **Mechanical gate:** `uv run --group docs properdocs build --strict` — exit 0, no warnings (link and anchor resolution).
- **Editorial pass:** Second read across all 13 sections for form uniformity, per-smell scoping, no generic disclaimers, and don't-elide after concision edits.

## LESSONS LEARNED

- **Step 1 index.** Hoisting a single per-smell corpus index before authoring avoided re-reading ~2k lines of FINDINGS per smell and kept cross-smell consistency tractable.
- **Plan shape.** One documented sub-cycle referenced for Steps 2–14 kept the plan readable without 13× repetition.
- **Corpus leverage.** `FINDINGS-CLAUDE.md`-style line-cited, per-smell evidence was the highest-leverage input; smaller FINDINGS files added breadth on selected smells.
- **Re-read before author.** For each file, re-reading that smell's Signals before drafting guards reduced "generic LLM disclaimer" slips.

## PROCESS IMPROVEMENTS

- Prefer `git add <explicit paths>` over `git add -A` when the tree may contain unrelated WIP; a prior commit had swept unrelated SKILL.md edits—operator chose to leave history as-is.
- For doc-only L2+ tasks, treat the editorial checklist (evidence pointer, don't-elide, concision) as the TDD analogue to "tests first" when `always-tdd` does not map literally to code.

## TECHNICAL IMPROVEMENTS

- **Possible future shape.** Co-locating each guard with its corresponding Signal (inverse-side of the same detection) could reduce reader hopping; that would be a major taxonomy/CONTRIBUTING reshape—out of scope here.

## NEXT STEPS

None required for this deliverable. Optional follow-up: if the team wants stricter git hygiene on the branch that contained the mixed commit, history cleanup is an operator choice, not a product requirement.
