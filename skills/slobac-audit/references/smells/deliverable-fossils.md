# `deliverable-fossils` — audit-specific augmentation

This file carries audit-runtime guidance only. The canonical definition of the smell — what it is, why it matters, the signals, the prescribed fix — lives in [`docs/taxonomy/deliverable-fossils.md`](../../../../docs/taxonomy/deliverable-fossils.md) and must be read alongside this file. Nothing here restates the manifesto; every line is additive.

## Invocation-phrase hints

Natural-language phrases that scope an invocation to this smell:

- "fossils", "deliverable fossils", "fossil tests"
- "stale names", "dead names", "sprint-shaped tests"
- "checklist tests", "checklist-shaped", "one test per AC"
- "tests named after tickets", "ticket-id vocabulary"
- "names that describe who wrote them, not what they prove"

When the operator uses any of these, treat the scope as `deliverable-fossils` unless they also name another supported smell, in which case treat it as both.

## Emission hints

When emitting a finding, the rename recommendation must encode the **behavior** the test verifies, not the fossil label. Concretely:

- Read the body's assertions and derive a one-sentence behavior statement. Propose a new name from that statement, not from the fossil-laden title.
- If the fossil lives in a `describe` / class grouping rather than the test name, recommend both the rename of the grouping *and* the rename of any in-group tests whose names reference the same history.
- When the manifesto's Prescribed Fix allows a two-phase move (rename, then regroup), emit the remediation scoped to **rename-only** unless the suite already has a clear capability-keyed grouping the test could move into. Phase B (regroup) is the full fix but risks reviewer confusion and merge conflicts; default to naming it as a follow-up, not as the primary remediation.
- When two or more flagged tests in the same file look like they verify the same behavior under different fossil labels, mention the likely [`semantic-redundancy`](../../../../docs/taxonomy/semantic-redundancy.md) overlap in the rationale. Do not attempt to detect redundancy yourself — it is not in Phase-1 scope.

## False-positive guards

Fossil vocabulary is a **signal**, not a **verdict**. The following are common over-triggers — the audit must not flag them:

- **The word `refactor` in a test whose body genuinely tests refactor safety.** Example: `test_refactor_preserves_lookup_semantics` whose body verifies that a rename-only transform does not change the call graph. "Refactor" here is the behavior under test, not the test's reason-for-existence. Rule: before flagging a test with `refactor`/`refactored`/`post-refactor` in the title, check whether the body is *about* a refactor property. If yes, do not flag.
- **Ticket IDs in a test whose body guards that specific regression.** If the body is tightly tied to a specific bug-fix behavior (e.g. asserts a null case that was the bug), the ticket ID may be useful provenance. The manifesto's Prescribed Fix says to move the ticket to a code comment, not to strip it entirely. The audit should recommend this move rather than flagging it as a fossil to rip out.
- **Domain vocabulary that looks like fossil vocabulary.** A test about a legal `checklist` feature, a test about a product's `milestone` entity, a test about version-`M2`-of-the-API-contract — all use fossil-adjacent words as first-class domain terms. Before flagging, check whether the word is product vocabulary (appears in the SUT) or work vocabulary (only appears in the test name). Flag only work vocabulary.
- **Configuration or team-specific ticket prefixes.** The manifesto's Polyglot notes say the fossil glossary is team-specific. Do not assume every `<letters>-<digits>` pattern is a ticket; a test named `test_pr_512_parser` on a project where `PR_512` happens to be a data-file identifier is domain vocabulary, not fossil vocabulary. When uncertain, surface the uncertainty in the rationale and lean toward not flagging.

## Detection priorities

Within the canonical Signals list, these three are the highest-yield for Phase 1:

1. Title vocabulary: `refactor`, `after`, `per`, `ms-N`, `phase-N`, ticket-prefix patterns.
2. Docstrings or comments citing AC identifiers, design-doc section numbers, or sprint references.
3. `describe` / class groupings keyed to work phases rather than product capabilities.

File-name signals (`feature-x-task-1.test.py`, `spec_for_pr_512.rb`) are genuine fossils but are less common in Python fixtures and can be deprioritized unless the target suite's file names are themselves strongly fossil-shaped.

## Polyglot note for Phase 1

The Phase-1 audit is validated only on Python fixtures. The manifesto's Polyglot notes describe the detection surface on JS/TS, Ruby, JVM, and others; detection prose in this augmentation is language-neutral and should apply to any ecosystem the SKILL.md workflow is pointed at. When auditing a non-Python suite, lean on the manifesto's Polyglot notes for the ecosystem-specific fossil conventions (e.g. RSpec `context` blocks as fossil carriers).
