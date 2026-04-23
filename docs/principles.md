# Testing principles

The test-design principles the [taxonomy](./taxonomy/README.md) ties back to. Each entry is anchor-linkable so taxonomy files can cite it directly. External sources are footnoted so this document stands on its own.

Two kinds of principles appear here:

1. **Properties of good tests** — what a *finished* test should look like. Graded against an individual test on its own merits.
2. **Principles of test-suite refactoring** — what a disciplined *refactor* of an existing test suite may do. Graded against a proposed change, not against a test.

## Properties of good tests

### Farley's 8

Dave Farley's framing of what makes a test worth having.[^farley] Each property here is what a test *should* be; the taxonomy names the ways real tests fail to hit the mark.

#### Understandable

A reader new to the codebase should be able to tell what the test proves without opening five other files. The test name shouts what it tests; the body reads as arrange-act-assert; fixtures are named or summarized.

#### Maintainable

Changing the system under test in a behavior-preserving way should not break the test. Tests that pin incidental formatting, private-method shapes, or mock-call ordering fail this property.

#### Repeatable

The test produces the same answer every time, in any environment, on any day. Time, RNG, network, filesystem, and execution order are all controlled.

#### Atomic

The test stands alone. It does not depend on a prior test having run, a shared mutable fixture being in a particular state, or any other cross-test ordering.

#### Necessary

The test adds a perspective no other test already covers. Two tests that verify the same observable behavior by different routes fail this property; one of them is redundant.

#### Granular

The test verifies one outcome. When it fails, a reader knows exactly what broke. A test that asserts five unrelated properties fails this property.

#### Fast

The test runs quickly enough to be worth running after every small edit. "Fast" is tier-relative: unit tests run in single-digit milliseconds; integration tests can be seconds.

#### Simple

The test's own cyclomatic complexity is ~1. No `if` branches, no loops hiding assertions, no try/catch compensating for a weak oracle.

### Greg Wright's additions

Greg Wright's *Ten Properties of Good Unit Tests* (first eight)[^wright] overlaps substantially with Farley's. Wright's *Independent*, *At least one assertion*, *Consistent*, and *Fast* are covered by Farley's Atomic / Repeatable / Granular / Fast. Three of Wright's axes name things Farley does not call out explicitly, and they earn their own entries here:

#### Well-named

The test's identifier encodes its claim. `it('should work')` and `test_1` fail this property. Farley's Understandable is about the test body; this property is about the name on its own.

#### Independent of implementation

Tests verify *what* the code does, not *how*. Classically described as black-box vs white-box testing: a black-box test only knows the interface; a white-box test also knows the internal structure. Black-box is the default; white-box testing should be rare, intentional, and well-documented as to why it was necessary. Farley's Maintainable is close but sits one level higher.

#### Clear failure message

When the test fails, the message should point a reader toward the real cause. `expected 6, got 5` is worse than `expected 6 messages (3 user + 3 assistant), got 5`.

## Principles of test-suite refactoring

The properties above describe what a test should *be*. These principles constrain what a disciplined refactor of an existing test suite may *do*.

### Behavior articulation before change

Before proposing any change to a test, the change-maker (human or agent) must first state, in one sentence, what the test is supposed to verify — as a claim about the product, not a claim about the code. The articulated behavior is the basis for every subsequent rename, consolidation, relocation, or deletion judgment; without it, changes drift toward shape-preserving rather than behavior-preserving moves.

The technique is borrowed from ChatTester,[^chattester] which showed that forcing an LLM to state intent *before* writing test code materially reduces vacuous assertions. The same discipline applies retroactively: state what a pre-existing test claims to protect before you touch it.

### Preservation of regression-detection power

A refactor of the test suite must not reduce the suite's ability to detect regressions. This is stricter than "the tests still pass" — the tests that remain after the refactor must still catch the same real bugs the tests before the refactor would have caught.

In practice this is measured by some combination of:

- line/branch coverage (necessary but insufficient),
- mutation score (stronger — see [mutation testing](./glossary.md#mutation-testing)),
- the specific set of mutants the suite kills (strongest).

A transform that shrinks any of these without a named absorber in the rationale is disallowed. The specific validator pipeline used to check this is an implementation choice; the principle is the constraint.

If a test is clearly identified as a regression test - especially if it has a reference to a ticket or ticketing system - the threshold for changing it at all is higher than a "normal" test. Someone very intentionally wanted this specific regression test, as a result of a specific incident!

### Governor rules

Hard restrictions on what a disciplined test-suite refactor may do. Inspired by citypaul's refactoring skill[^citypaul-refactoring] and general practice. Violating any of them is an automatic veto.

#### Knowledge-DRY, not syntactic DRY

DRY means *knowledge*, not *code*. Two tests that look similar but guard different product concerns must not be merged. The merge question is always "do these encode the same knowledge about the product?", never "do these share tokens?".

#### No extract-for-testability

Do not extract production code purely so tests become easier to write. Split production code for readability or genuine concern-separation; never for test convenience. The one exception the [taxonomy](./taxonomy/README.md) permits is extracting a provably cohesive helper that *also* clarifies architecture (see [`implementation-coupled`](./taxonomy/implementation-coupled.md)).

#### No speculative code

Do not add tests, abstractions, or extraction points "in case we need them later". Every change must serve a concrete current need with a concrete current rationale.

#### Commit-before-refactor

The working-but-ugly state must be committed before any refactor begins. If the refactor goes wrong, `git reset` is the recovery path — not memory.

## Cross-reference to taxonomy entries

Each [taxonomy](./taxonomy/README.md) entry names the principle(s) it protects at the top of its page. When you see `**Protects:** [Maintainable](../principles.md#maintainable)`, this is the section being referenced.

[^farley]: Dave Farley, originally as an eight-tweet thread summarizing his view of good tests. Captured and extended in citypaul's `test-design-reviewer` skill: <https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/test-design-reviewer/SKILL.md>. Farley's own writing: Farley, D. (2021). *Modern Software Engineering*, Addison-Wesley; and talks at <https://www.youtube.com/@ContinuousDelivery>.

[^wright]: Wright, G. *Ten Properties of Good Unit Tests*. Medium, 2021. <https://medium.com/@gregwright_1301/ten-properties-of-good-unit-tests-3bbd49222754>. This document uses his first eight; the remaining two (*First*/TDD and *documents the code*) are folded into other entries.

[^chattester]: Yuan, Z. et al. (2023). *No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation* (ChatTester). arXiv:2305.04207. <https://arxiv.org/abs/2305.04207>. The describe-before-test framing appears as Section 4.2 ("Intention Description").

[^citypaul-refactoring]: citypaul, *refactoring* skill for Claude Code. <https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/refactoring/SKILL.md>.
