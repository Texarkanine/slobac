# Test Qualities

What a *finished* test should look like. Graded against an individual test on its own merits.

## Farley's 8

Dave Farley's framing of what makes a test worth having.[^farley] Each property here is what a test *should* be; the taxonomy names the ways real tests fail to hit the mark.

### Understandable

A reader new to the codebase should be able to tell what the test proves without opening five other files. The test name shouts what it tests; the body reads as arrange-act-assert; fixtures are named or summarized.

### Maintainable

Changing the system under test in a behavior-preserving way should not break the test. Tests that pin incidental formatting, private-method shapes, or mock-call ordering fail this property.

### Repeatable

The test produces the same answer every time, in any environment, on any day. Time, RNG, network, filesystem, and execution order are all controlled.

### Atomic

The test stands alone. It does not depend on a prior test having run, a shared mutable fixture being in a particular state, or any other cross-test ordering.

### Necessary

The test adds a perspective no other test already covers. Two tests that verify the same observable behavior by different routes fail this property; one of them is redundant.

### Granular

The test verifies one outcome. When it fails, a reader knows exactly what broke. A test that asserts five unrelated properties fails this property.

### Fast

The test runs quickly enough to be worth running after every small edit. "Fast" is tier-relative: unit tests run in single-digit milliseconds; integration tests can be seconds.

### Simple

The test's own cyclomatic complexity is ~1. No `if` branches, no loops hiding assertions, no try/catch compensating for a weak oracle.

## Greg Wright's additions

Greg Wright's *Ten Properties of Good Unit Tests* (first eight)[^wright] overlaps substantially with Farley's. Wright's *Independent*, *At least one assertion*, *Consistent*, and *Fast* are covered by Farley's Atomic / Repeatable / Granular / Fast. Three of Wright's axes name things Farley does not call out explicitly, and they earn their own entries here:

### Well-named

The test's identifier encodes its claim. `it('should work')` and `test_1` fail this property. Farley's Understandable is about the test body; this property is about the name on its own.

### Independent of implementation

Tests verify *what* the code does, not *how*. Classically described as black-box vs white-box testing: a black-box test only knows the interface; a white-box test also knows the internal structure. Black-box is the default; white-box testing should be rare, intentional, and well-documented as to why it was necessary. Farley's Maintainable is close but sits one level higher.

### Clear failure message

When the test fails, the message should point a reader toward the real cause. `expected 6, got 5` is worse than `expected 6 messages (3 user + 3 assistant), got 5`.

[^farley]: Dave Farley, originally as an eight-tweet thread summarizing his view of good tests. Captured and extended in citypaul's `test-design-reviewer` skill: <https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/test-design-reviewer/SKILL.md>. Farley's own writing: Farley, D. (2021). *Modern Software Engineering*, Addison-Wesley; and talks at <https://www.youtube.com/@ContinuousDelivery>.

[^wright]: Wright, G. *Ten Properties of Good Unit Tests*. Medium, 2021. <https://medium.com/@gregwright_1301/ten-properties-of-good-unit-tests-3bbd49222754>.
