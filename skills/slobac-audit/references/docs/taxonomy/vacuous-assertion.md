# Vacuous Assertion

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `vacuous-assertion` | High | per-test | [Granular](../principles.md#granular), [Necessary](../principles.md#necessary) |

## Summary

The test *does* assert, and the assertion runs against real SUT output — but the assertion is so weak that many interesting wrong implementations would still pass.

## Description

This is one of three members of the [Tautology Theatre](../glossary.md#tautology-theatre) umbrella, distinguished by *where* the weakness lives:

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

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

1. Identify the real claim via [describe-before-edit](../principles.md#behavior-articulation-before-change).
2. Replace the weak check with the strongest *available* assertion. Prefer in order: structural equality > matcher-based object containment > regex > prefix/length.
3. If the real claim is a side-effect absence, replace `not_to raise_error` with `not_to have_received(:cp)` or equivalent.
4. Collapse `toBeDefined` + subsequent dereference into one matcher: `expect(x).toMatchObject({ foo: 'bar' })`.
5. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power), *stricter* than the default — the [mutation kill-set](../glossary.md#mutation-kill-set) must *increase*, not just stay flat.

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

- [`pseudo-tested`](./pseudo-tested.md), [`tautology-theatre`](./tautology-theatre.md) — adjacent members of the [Tautology Theatre](../glossary.md#tautology-theatre) umbrella.
- [`naming-lies`](./naming-lies.md) — a vacuous body often pairs with a title that over-promises.
- [`presentation-coupled`](./presentation-coupled.md) — the opposite failure mode: assertions too *strong* on the wrong thing.

## Polyglot notes

The list of weak-assertion shapes is per-runner (Jest's `.toBeDefined()`, Pytest's `assert x`, RSpec's `be_truthy`). The detection logic — "what wrong answer still passes?" — is universal. Keep a per-runner shape table and a language-agnostic strengthener prompt.
