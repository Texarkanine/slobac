# Vacuous Assertion

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `vacuous-assertion` | High | per-test | [Granular](../principles/test-qualities.md#granular), [Necessary](../principles/test-qualities.md#necessary) |

## Summary

The test *does* assert, and the assertion runs against real SUT output — but the assertion is so weak that many interesting wrong implementations would still pass.

## Aliases

- "vacuous assertion"
- "weak oracle"
- "weak assertion"
- "assertion too weak"
- "many wrong answers pass"
- "is-not-none assertions"
- "truthiness check"
- "structural-only check"
- "not-empty as the only check"

## Description

This is one of three members of the [Tautology Theatre](../principles/glossary.md#tautology-theatre) umbrella, distinguished by *where* the weakness lives:

- [`tautology-theatre`](./tautology-theatre.md) — SUT never runs at all.
- [`pseudo-tested`](./pseudo-tested.md) — SUT runs, but a no-op replacement would still pass.
- **this entry (`vacuous-assertion`)** — SUT runs, the assertion fires, but the weakest wrong answer still passes.

The semantic judgment: read the assertion against the SUT and ask *"what minimal wrong answer would this still accept?"* If many interesting wrong answers pass, the oracle is vacuous. Linters catch some cases (`expect-expect`, Ruff's `S*` rules, `bool-compare`) but miss domain-specific weakness because they do not understand the type of the return value.

Fix bias: **strengthen, don't multiply.** One strong check beats three weak ones.

## Signals

- `expect(x).toBeDefined()` immediately followed by `x!.y.z` — the dereference is the real assertion; the `toBeDefined` is dead weight.
- `expect(x).toBeTruthy()` on a value with a known-knowable format (UUID, URL, date, enum).
- `assert x is not None` or `assert len(x) > 0` as the *only* assertion.
- `expect(obj).toBeInstanceOf(Array)` / `be_a(String)` where an exact value is knowable.
- `assert(result === Object(result))` — an identity check that any object passes.
- `assert.ok(file.isFile())` plus `assert.notStrictEqual(file.size, 0)` — an empty content with a non-empty file still passes.
- `expect { ... }.not_to raise_error` as the whole `it` body when the real claim is "does not *do* Y" (a side-effect absence).
- `assert "12" in out` as the only check on multi-line structured output.

## False-positive guards

Two over-triggers must be suppressed:

- **Side-effect absence is the documented contract.** When the SUT's contract is "this function swallows errors by design," "this listener performs no I/O on the no-op input," or "this idempotent retry has no effect on the second call," `expect { ... }.not_to raise_error` (or `assert no_calls_to(boundary)`, etc.) is the *correct* assertion of that absence — there is no positive return or state to compare against. The smell fires only when the docstring or test name claims a *positive* behavior (a return value, a state mutation, an emitted event) that the assertion does not verify. Pair the negative-existence check with a positive assertion only when the contract has both halves; do not flag a test whose contract is the negative half alone.
- **Two-stage assertions where the first stage is required language narrowing.** `expect(x).toBeDefined()` followed by `x!.foo === 'bar'` is collapsible into `toMatchObject({ foo: 'bar' })` per the fix recipe. But `assert response is not None` followed by a deep destructure of `response.json()` is sometimes the only shape the *language* allows — TypeScript non-null narrowing, Python `Optional` checks, mypy's `--strict` mode, Kotlin platform-types — where the first-stage check exists to satisfy the type checker and the second-stage destructure is the real oracle. The first-stage check is dead weight; the test as a whole is not vacuous. Flag only when the second-stage assertion is itself weak.

## Prescribed Fix

1. Identify the real claim via [describe-before-edit](../principles/refactor-qualities.md#behavior-articulation-before-change).
2. Replace the weak check with the strongest *available* assertion. Prefer in order: structural equality > matcher-based object containment > regex > prefix/length.
3. If the real claim is a side-effect absence, replace `not_to raise_error` with `not_to have_received(:cp)` or equivalent.
4. Collapse `toBeDefined` + subsequent dereference into one matcher: `expect(x).toMatchObject({ foo: 'bar' })`.
5. Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power), *stricter* than the default — the [mutation kill-set](../principles/glossary.md#mutation-kill-set) must *increase*, not just stay flat.

## Example

### Before

```typescript
it('discovers plugin descriptions', async () => {
  const result = await discover(ws);
  expect(result).toBeDefined();
  expect(result.description).toBeTruthy();
});
```

### After

```typescript
it('describes each plugin with a non-empty single-paragraph summary', async () => {
  const result = await discover(ws);
  expect(result).toMatchObject({
    id: 'cursor',
    description: expect.stringMatching(/^[A-Z][\s\S]{10,}\.$/),
  });
});
```

The original assertions would pass for `{}` or `{ description: ' ' }`. Strengthened to a structural match plus a minimum-shape regex. Two mutants that previously survived (`return {}` and `return { description: ' ' }`) are now killed.

## Related modes

- [`pseudo-tested`](./pseudo-tested.md), [`tautology-theatre`](./tautology-theatre.md) — adjacent members of the [Tautology Theatre](../principles/glossary.md#tautology-theatre) umbrella.
- [`naming-lies`](./naming-lies.md) — a vacuous body often pairs with a title that over-promises.
- [`presentation-coupled`](./presentation-coupled.md) — the opposite failure mode: assertions too *strong* on the wrong thing.
- [`loose-text-oracle`](./loose-text-oracle.md) — present but underdetermined text match on runtime emissions; not "effectively no check," but still fails to lock meaning.

## Polyglot notes

The list of weak-assertion shapes is per-runner (Jest's `.toBeDefined()`, Pytest's `assert x`, RSpec's `be_truthy`). The detection logic — "what wrong answer still passes?" — is universal. Keep a per-runner shape table and a language-agnostic strengthener prompt.
