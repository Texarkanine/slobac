# Test-development workflows

Cycles of activity for writing and refactoring code plus its tests. [Principles](./principles.md) describe the goal state; workflows describe sequences of steps to reach it.

## RED-GREEN-MUTATE-KILL-REFACTOR

An extension of the classical TDD cycle (red-green-refactor) with a mutation-testing gate inserted between green and refactor. The cycle appears in citypaul's planning skill[^citypaul-planning] and is the workflow the [taxonomy](./taxonomy/README.md) assumes when it talks about refactor safety.

Steps:

1. **RED.** Write a failing test. Confirm it fails for the right reason — not a syntax error, not an import error, but the specific expectation you intend to assert.
2. **GREEN.** Write the minimum production code that makes the test pass. No extra.
3. **MUTATE.** Run [mutation testing](./glossary.md#mutation-testing) on the newly touched code. The tool produces a set of [mutants](./glossary.md#mutant) (variants of the code with a single change each) and reports which ones the current suite kills versus which survive.
4. **KILL.** For every surviving mutant that represents a real change in behavior (i.e. is not [equivalent](#equivalent-mutants)), add or strengthen a test that kills it. Return to step 1 if the new test requires additional production code; return to step 3 to confirm the kill. Repeat until all non-equivalent mutants are killed.
5. **REFACTOR.** Only now is it safe to refactor. The [mutation kill-set](./glossary.md#mutation-kill-set) is strong enough that a refactor which accidentally breaks behavior will be caught by at least one test, not fall through into production.

### Why the mutate step is load-bearing

Pure TDD's green-refactor step can land a refactor that breaks behavior only observable through mutants the test suite never would have caught in the first place — the tests pass before and after, but the refactor silently introduces a bug. Mutation between green and refactor converts *"my test passes"* into *"the behavior my test claims to protect is actually protected."* Refactor then becomes a sound operation on a suite with known detection power.

This is also the principle the [taxonomy](./taxonomy/README.md) leans on when proposing any transform: a rename or dedup is safe precisely when the mutation kill-set cannot regress. See [principles § Preservation of regression-detection power](./principles.md#preservation-of-regression-detection-power).

### Equivalent mutants

Not every surviving mutant is a real gap. A mutant is **equivalent** when it changes the code in a way that cannot be observed through any input — e.g. replacing `x + 0` with `x`, or flipping `<=` to `<` in a branch that is dead on all reachable inputs. Equivalent mutants cannot be killed by any test and should not be pursued. Identifying them is a semantic judgment that mutation tools cannot make on their own; leaving them as "known survivors" with a comment is the standard practice.

[^citypaul-planning]: citypaul, *planning* skill (RED-GREEN-MUTATE-KILL-REFACTOR). <https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/planning/SKILL.md>.
