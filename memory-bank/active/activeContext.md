# Active Context

## Current Task

Author `## False-positive guards` sections for 13 stub taxonomy docs.

## Phase

`REFLECT COMPLETE`

## What Was Done

Authored 2–3 false-positive guards for each of the 13 stub-bearing taxonomy files, drawing on the per-smell evidence index built from `planning/research/` (synthesis report + 5 model-specific FINDINGS files). Each guard is a `- **Name.** Decision rule.` bullet, per-smell scoped, evidenced from the corpus, and matches the form of `naming-lies.md` / `deliverable-fossils.md`. `uv run --group docs properdocs build --strict` passed cleanly with zero warnings, confirming no link or anchor breakage. Editorial cross-pass confirmed uniformity of form, no generic LLM disclaimers, and no elided guard the corpus clearly supported.

### Files modified

- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/semantic-redundancy.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/wrong-level.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/vacuous-assertion.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/pseudo-tested.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/tautology-theatre.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/over-specified-mock.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/implementation-coupled.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/presentation-coupled.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/conditional-logic.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/shared-state.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/mystery-guest.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/rotten-green.md`
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/taxonomy/monolithic-test-file.md`

### Key implementation decisions

- **Two-or-three guards per smell** rather than a fixed count. Some smells (`wrong-level`, `vacuous-assertion`, `pseudo-tested`, `presentation-coupled`, `rotten-green`, `monolithic-test-file`) have a smaller corpus-supported FP surface; padding to three would have violated the "evidenced, don't invent" constraint. Per-plan: ship the strongest set the corpus supports.
- **Citation discipline**: each guard's claim was traceable to a passage in `report.md` or one of the FINDINGS files. The audit rule "no fabricated guards" was honored even when it meant a smell shipped with two guards instead of three.
- **Cross-smell rerouting** (`shared-state` → `rotten-green` for orphan setup) was authored explicitly because the corpus surfaces it as an over-trigger of the shared-state signals.
- **No anchor invention**: the only new internal links cited anchors that already exist (verified by the strict build).

### Deviations from plan

None. Built exactly to plan; the catalog-ordered sub-cycle ran without surprises.

## Next Step

Operator-initiated `/niko-archive` to finalize the task. Reconcile-persistent skipped (no persistent file invalidated by this task).
