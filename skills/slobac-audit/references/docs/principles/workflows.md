# Test-Suite Refactor Workflows

Cycles of activity for writing and refactoring code plus its tests. [Principles](./test-qualities.md) describe the goal state; workflows describe sequences of steps to reach it.

## RED-GREEN-MUTATE-KILL-REFACTOR

An extension of the classical TDD cycle (red-green-refactor) with a [mutation-testing](../principles/glossary.md#mutation-testing) gate inserted between green and refactor. This is the workflow the [taxonomy](../taxonomy/README.md) assumes when it talks about refactor safety.

Steps:

1. **RED.** Write a failing test. Confirm it fails for the right reason — not a syntax error, not an import error, but the specific expectation you intend to assert.
2. **GREEN.** Write the minimum production code that makes the test pass. No extra.
3. **MUTATE.** Run mutation testing on the newly touched code. The tool produces a set of [mutants](./glossary.md#mutant) (variants of the code with a single change each) and reports which ones the current suite kills versus which survive.
4. **KILL.** For every surviving mutant that represents a real change in behavior (i.e. is not [equivalent](#equivalent-mutants)), add or strengthen a test that kills it. Return to step 1 if the new test requires additional production code; return to step 3 to confirm the kill. Repeat until all non-equivalent mutants are killed.
5. **REFACTOR.** Only now is it safe to refactor. The [mutation kill-set](./glossary.md#mutation-kill-set) is strong enough that a refactor which accidentally breaks behavior will be caught by at least one test, not fall through into production.

## Why Mutate?

When authoring code from scratch, vanilla TDD "works" to ensure that the specified behavior is implemented by the code; the tests guard the code.

When refactoring a test suite, the test suite can't guard against incorrect changes to itself - the production code becomes the "test suite" and the test suite becomes the system-under-test.

But, you probably had a 1:N relationship between "important production code behavior" and "tests for that behavior." You probably had tests for all sorts of edge cases, input combinations, etc. When you flip the script, each of the 10 tests you might refactor are all guarded by just that one unit of production code. This makes it much easier to break the guarantee that passing tests mean the code works right.

Mutation testing is a way to address this - it creats a bunch of variants (mutants) of your production code and runs the modified test suite against them. You would expect the *same* sets of passing and failing mutants before and after a test suite refactor. If you get *different* sets, that signals that your test suite refactor *changed* what the tests actually cover and that - even if your refactored test suite passes, it's **not** providing the same guarantee it was before.

This is also the principle the [taxonomy](../taxonomy/README.md) leans on when proposing any transform: a rename or dedup is safe precisely when the mutation kill-set cannot regress. See [principles § Preservation of regression-detection power](./refactor-qualities.md#preservation-of-regression-detection-power).

It's possible you'd see a refactored test suite let fewer mutants through - that's good, that would generally mean you improved the test suite! But if you see more mutants survive, or a shift in *which* mutants survive, that's a "fail" signal for a test suite refactor.

### Equivalent mutants

Not every surviving mutant is a real gap. A mutant is **equivalent** when it changes the code in a way that cannot be observed through any input — e.g. replacing `x + 0` with `x`, or flipping `<=` to `<` in a branch that is dead on all reachable inputs. Equivalent mutants cannot be killed by any test and should not be pursued. Identifying them is a semantic judgment that mutation tools cannot make on their own; leaving them as "known survivors" with a comment is the standard practice.
