# Project Brief: Author False-Positive Guards Across Taxonomy

## User Story

As a maintainer of the SLOBAC audit reference, I want every smell doc in `skills/slobac-audit/references/docs/taxonomy/` to carry a populated `## False-positive guards` section — sourced from `planning/research/` — so the taxonomy provides a uniform, evidence-backed baseline of guards instead of stub placeholders on most files.

## Scope

Author the `## False-positive guards` section for the 13 taxonomy files that currently carry the placeholder `No audit-specific guards yet; Phase-2 per-smell work will author these.`:

- `conditional-logic.md`
- `implementation-coupled.md`
- `monolithic-test-file.md`
- `mystery-guest.md`
- `over-specified-mock.md`
- `presentation-coupled.md`
- `pseudo-tested.md`
- `rotten-green.md`
- `semantic-redundancy.md`
- `shared-state.md`
- `tautology-theatre.md`
- `vacuous-assertion.md`
- `wrong-level.md`

Already authored (out of scope, do not modify):

- `naming-lies.md`
- `deliverable-fossils.md`

## Source Material

`planning/research/` — synthesis report (`report.md`) plus per-model findings (`FINDINGS-CLAUDE.md`, `FINDINGS-CODEX.md`, `FINDINGS-COMPOSER.md`, `FINDINGS-GEMINI.md`, `FINDINGS-GROK.md`).

## Quality Constraints

- **Concise.** These are foundational, human-read references. Bias toward few sharp guards over a long checklist.
- **Evidenced.** Only include guards supported by the research corpus; don't invent or pad from intuition.
- **Don't elide.** If research clearly supports a guard, it must appear — terseness is not an excuse to drop a real false-positive class.
- **Per-smell scoping.** Each guard belongs to a specific smell's false-positive surface, not a generic disclaimer.
- **Style match.** Follow the existing form in `naming-lies.md` and `deliverable-fossils.md`.

## Out of Scope

- Rewriting the two already-authored sections.
- Touching other sections of the smell docs.
- Expanding the taxonomy itself.
