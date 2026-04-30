# Rotten Green

| Slug | Severity | Protects |
|---|---|---|
| `rotten-green` | Low | [Necessary](../principles.md#necessary), [Granular](../principles.md#granular) |

## Summary

The test reports green but never actually exercises or asserts anything. Empty bodies, TODO stubs that count as passing, dead fixtures declared and never read, debug `console.log` left behind where an assertion was meant to land.

Also known as "dead scaffolding".

## Description

Covered in spirit by [`vacuous-assertion`](./vacuous-assertion.md), [`pseudo-tested`](./pseudo-tested.md), and [`shared-state`](./shared-state.md), but worth a separate entry because the signal is **syntactic and extremely cheap** — no semantic reasoning required for detection, only for the fix-vs-delete decision.

## Signals

- Empty `it()` / `test()` body with only `// TODO` that still counts as passing.
- `let(:doc)` / fixture declared and never referenced.
- Fixture directories (`fixtures/to-claude/`, `fixtures/to-cursor/`) referenced by path but never read.
- `console.log('done!', res)` / `print(result)` left in the test body where an assertion was intended.
- Variables computed and discarded (`const toDir = ...` never used).
- Linter `expect-expect` / `@typescript-eslint/no-unused-vars` flagging the case.

## False-positive guards

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

Two transforms, depending on intent:

1. **Dead scaffold, no intent to test.** Delete the file, block, or fixture. Clean and safe; the preservation gate allows coverage to drop here with a named rationale, since the deleted code killed no mutants.
2. **Stub that was meant to test something.** Mark explicitly: either convert to the runner's pending/xit marker (`it.todo(...)`, `xit`, `@pytest.mark.skip`) so it shows as "known gap" in reports, or write the missing assertion using [describe-before-edit](../principles.md#behavior-articulation-before-change) to guess intent from the name. If the intent is ambiguous, prefer explicit pending.

Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power). `.todo` / `skip` conversions must include a reason string.

## Example

### Before

```javascript
describe('MempoolApiClient', () => {
  it('handles network errors', () => {
    // TODO: test this
  });

  it('retries on 429', () => {
    const client = new MempoolApiClient();
    const res = client.fetch('/block/tip');
    console.log('done!', res);
  });
});
```

### After

```javascript
describe('MempoolApiClient', () => {
  it.todo('handles network errors by surfacing a typed exception');

  it('retries on 429 with exponential backoff', async () => {
    const fetchMock = jest.fn()
      .mockResolvedValueOnce({ ok: false, status: 429 })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ height: 1 }) });
    const client = new MempoolApiClient({ fetch: fetchMock });
    const res = await client.fetch('/block/tip');
    expect(res.height).toBe(1);
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
```

The first test is now explicitly pending — it surfaces as TODO in CI reports instead of a silent green. The second test had a `console.log` where the assertion belonged; the actual retry assertion is now present.

## Related modes

- [`vacuous-assertion`](./vacuous-assertion.md) — adjacent; rotten-green has *no* assertion, vacuous has a weak one.
- [`pseudo-tested`](./pseudo-tested.md) — SUT runs but no oracle; hard to distinguish from rotten-green without [describe-before-edit](../principles.md#behavior-articulation-before-change).
- [`shared-state`](./shared-state.md) — dead shared setup is a rotten-green subcase.

## Polyglot notes

Every runner has a pending/todo marker: `it.todo` / `xit` / `test.skip` / `@pytest.mark.skip` / `pending(:reason)` / `t.Skip` in Go. Adopt the repo's existing convention.
