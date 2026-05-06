# Test-Suite Refactor Qualities

What a disciplined *refactor* of an existing test suite may do. Graded against a proposed change, not against a test.

## Behavior articulation before change

Before proposing any change to a test, the change-maker (human or agent) must first state, in one sentence, what the test is supposed to verify — as a claim about the product, not a claim about the code. The articulated behavior is the basis for every subsequent rename, consolidation, relocation, or deletion judgment; without it, changes drift toward shape-preserving rather than behavior-preserving moves.

The technique is borrowed from ChatTester,[^chattester] which showed that forcing an LLM to state intent *before* writing test code materially reduces vacuous assertions. The same discipline applies retroactively: state what a pre-existing test claims to protect before you touch it.

## Preservation of regression-detection power

A refactor of the test suite must not reduce the suite's ability to detect regressions. This is stricter than "the tests still pass" — the tests that remain after the refactor must still catch the same real bugs the tests before the refactor would have caught.

In practice this is measured by some combination of:

- line/branch coverage (necessary but insufficient),
- mutation score (stronger — see [mutation testing](./glossary.md#mutation-testing)),
- the specific set of mutants the suite kills (strongest).

A transform that shrinks any of these without a named absorber in the rationale is disallowed. The specific validator pipeline used to check this is an implementation choice; the principle is the constraint.

If a test is clearly identified as a regression test - especially if it has a reference to a ticket or ticketing system - the threshold for changing it at all is higher than a "normal" test. Someone very intentionally wanted this specific regression test, as a result of a specific incident!

## Governor rules

Hard restrictions on what a disciplined test-suite refactor may do. Inspired by citypaul's refactoring skill[^citypaul-refactoring] and general practice. Violating any of them is an automatic veto.

### Knowledge-DRY, not syntactic DRY

DRY means *knowledge*, not *code*. Two tests that look similar but guard different product concerns must not be merged. The merge question is always "do these encode the same knowledge about the product?", never "do these share tokens?".

### No extract-for-testability

Do not extract production code purely so tests become easier to write. Split production code for readability or genuine concern-separation; never for test convenience. The one exception the [taxonomy](../taxonomy/README.md) permits is extracting a provably cohesive helper that *also* clarifies architecture (see [`implementation-coupled`](../taxonomy/implementation-coupled.md)).

### No speculative code

Do not add tests, abstractions, or extraction points "in case we need them later". Every change must serve a concrete current need with a concrete current rationale.

### Commit-before-refactor

The working-but-ugly state must be committed before any refactor begins. If the refactor goes wrong, `git reset` is the recovery path — not memory.

## Cross-reference to taxonomy entries

Each [taxonomy](../taxonomy/README.md) entry names the principle(s) it protects at the top of its page. When you see `**Protects:** [Maintainable](../principles/test-qualities.md#maintainable)`, this is the section being referenced.

[^chattester]: Yuan, Z. et al. (2023). *No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation* (ChatTester). arXiv:2305.04207. <https://arxiv.org/abs/2305.04207>. The describe-before-test framing appears as Section 4.2 ("Intention Description").

[^citypaul-refactoring]: citypaul, *refactoring* skill for Claude Code. <https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/refactoring/SKILL.md>.
