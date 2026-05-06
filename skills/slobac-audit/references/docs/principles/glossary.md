# Glossary

General-purpose terminology used across the [taxonomy](../taxonomy/README.md) and the sibling [principles](./test-qualities.md) and [workflows](./workflows.md) documents. Entries are alphabetical. External sources are footnoted so this document stands alone.

## Canonical location

The file, module, or layer where a given product behavior belongs, independent of where the test for it currently lives. Deciding the canonical location for a cluster of near-duplicate tests is a semantic judgment: there is no deterministic rule, but the usual tiebreakers are (a) the most-public layer, (b) the smallest fixture surface, (c) the most precise test name, and (d) the most natural product-capability framing.

## Describe-before-edit

Before proposing a change to a test, first state in one sentence what the test is supposed to verify. See [principles § Behavior articulation before change](./refactor-qualities.md#behavior-articulation-before-change) for the full definition.

## Descartes

A pluggable engine for [PIT](#pit) (the JVM mutation testing tool) that implements [extreme mutation](#extreme-mutation--pseudo-tested-methods). Descartes replaces a method's body wholesale with `return 0` / `return null` / `return input` and checks whether any test notices. Surviving mutants are evidence of [pseudo-tested](../taxonomy/pseudo-tested.md) code.[^descartes]

## Extreme mutation / pseudo-tested methods

A cheap, high-signal mutation class defined by Niedermayr et al.[^niedermayr] Instead of mutating a single operator or literal, extreme mutation replaces an entire method body with a no-op (`return`, `return null`, `return input`). Niedermayr found a median of 10.1% of methods in studied suites could be replaced with a no-op and still pass every test — those methods are *pseudo-tested*. See the [`pseudo-tested`](../taxonomy/pseudo-tested.md) taxonomy entry and [Descartes](#descartes) / `mutmut --simple-mutations` / `cargo-mutants` for per-ecosystem tooling.

## Mutant

A specific variant of production code produced by a [mutation testing](#mutation-testing) tool. Typically the original code with a single small change: one operator flipped (`+` → `-`), one literal swapped (`0` → `1`), one branch inverted (`<=` → `>`), one statement removed, or — in [extreme mutation](#extreme-mutation--pseudo-tested-methods) — one entire method body replaced with a no-op. A test suite *kills* a mutant when at least one test fails on the mutated code; it *survives* otherwise.

## Mutation

The act of producing a [mutant](#mutant) by applying one mutation operator to production code. The set of operators a tool supports varies — arithmetic flips, boolean flips, conditional-boundary shifts, return-value neutralization, etc. Each operator is chosen because a real bug could plausibly look like the mutation; if no suite catches the mutation, the suite has a genuine gap for that class of bug.

## Mutation kill-set

The set of specific [mutants](#mutant) that the suite currently kills — tracked by mutant ID in whatever [mutation testing](#mutation-testing) tool the project runs. A refactor of the test suite that causes any previously-killed mutant to survive has reduced the suite's regression-detection power, whether or not any test appears to have been weakened. See [principles § Preservation of regression-detection power](./refactor-qualities.md#preservation-of-regression-detection-power).

## Mutation score

The fraction of [mutants](#mutant) the suite kills out of all mutants the tool generated. A single-number summary of [mutation kill-set](#mutation-kill-set) size. Weaker than the full kill-set (two suites with the same score may kill different mutants) but cheap to track over time.

## Mutation testing

A technique for measuring a test suite's regression-detection power by systematically introducing small changes ([mutants](#mutant)) to production code and checking whether any test fails. Any mutant that survives is evidence that *some* plausible bug of that shape would go undetected by the current suite. Mutation testing is more honest than coverage — a line can be covered by a test that would not catch any bug on that line — but also more expensive (every mutant requires a full test run).

Tooling:

- **JVM:** [PIT](#pit), plus [Descartes](#descartes) for extreme mutation.[^pit]
- **JS/TS:** Stryker.[^stryker]
- **Python:** mutmut, Cosmic Ray.
- **Rust:** cargo-mutants.
- **.NET:** Stryker.NET.
- **Go:** go-mutesting, go-gremlins.

## PIT

Pitest, the dominant JVM mutation testing tool.[^pit] Hosts the [Descartes](#descartes) extreme-mutation engine.

## Suite table of contents

A generated artifact that maps product behaviors to the tests that verify them. Useful as a review artifact during reorganization: a reviewer can see "where did `test_foo` go?" without running `git log -S`, and can tell whether the suite covers a given capability by looking it up by behavior name. Produced by [`deliverable-fossils`](../taxonomy/deliverable-fossils.md) and [`semantic-redundancy`](../taxonomy/semantic-redundancy.md) regroup passes.

## SUT (System Under Test)

The specific function, class, module, or service a given test is exercising. A test is said to be *mocking the SUT* when it has stubbed out the very thing it is supposed to be verifying — a classic symptom of [`tautology-theatre`](../taxonomy/tautology-theatre.md).

## Tautology Theatre

Umbrella term for tests that would still pass if all production code were deleted. The diagnostic question is literally *"would this test still pass if I `rm -rf`'d the production directory?"* — if yes, the test is theatre.

The [taxonomy](../taxonomy/README.md) splits Tautology Theatre into three distinct smells distinguished by *where* the weakness lives:

- [`tautology-theatre`](../taxonomy/tautology-theatre.md) — the SUT never runs at all (it is mocked, or the test only operates on mocks).
- [`pseudo-tested`](../taxonomy/pseudo-tested.md) — the SUT runs, but a no-op replacement would still pass.
- [`vacuous-assertion`](../taxonomy/vacuous-assertion.md) — the SUT runs, the assertion fires, but the weakest wrong answer still passes.

## Test level

**Test level** is how much real software sits between the test harness and the narrow behavior you care about — a semantic classification, not a runner label and not a mandate about how many tests to write at each depth.

**Primary split — unit vs integration:** In a **unit** test, the test-time call stack stays **inside** the [SUT](#sut-system-under-test). In an **integration** test, it **deliberately exits** the SUT (real collaborator code, real I/O, real framework plumbing, process boundary, etc.).

**Secondary split** (after you know unit vs integration): **simple unit** vs **component**; **simple integration** vs **functional**. Those names decide where a test belongs relative to repo conventions when you are fixing [`wrong-level`](../taxonomy/wrong-level.md).

For the full matrix (what each level means, CLI vs web examples) and auditor-oriented guidance, see [wrong-level § Classifying test level](../taxonomy/wrong-level.md#classifying-test-level).

[^descartes]: STAMP-project, *pitest-descartes*. <https://github.com/STAMP-project/pitest-descartes>.

[^niedermayr]: Niedermayr, R., Juergens, E., & Wagner, S. (2019). *Will my tests tell me if I break this code?* Empirical Software Engineering, 24(6), 4085–4130. <https://link.springer.com/article/10.1007/s10664-018-9653-2>. The 10.1% pseudo-tested median is Table 3 of the paper.

[^pit]: Coles, H. et al. *PIT Mutation Testing*. <https://pitest.org>.

[^stryker]: Stryker Mutator. <https://stryker-mutator.io>.
