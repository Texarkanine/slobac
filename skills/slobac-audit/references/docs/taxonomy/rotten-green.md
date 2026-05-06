# Rotten Green

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `rotten-green` | Low | per-test | [Necessary](../principles/test-qualities.md#necessary), [Granular](../principles/test-qualities.md#granular) |

## Summary

The test reports green but never actually exercises or asserts anything. Empty bodies, TODO stubs that count as passing, dead fixtures declared and never read, debug `console.log` left behind where an assertion was meant to land.

Also known as "dead scaffolding".

## Aliases

- "rotten green"
- "dead scaffolding"
- "empty test body"
- "TODO that passes"
- "print where assertion was intended"
- "console.log instead of assertion"
- "dead fixture never read"
- "test that reports green but verifies nothing"

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

Two over-triggers must be suppressed:

- **Linter-covered cases are out of scope.** `eslint-plugin-jest`'s `expect-expect`, ruff's `PT*` rules, `xunit.analyzers`, `rubocop-rspec`'s `Rspec/NoExpectationExample`, and similar deterministic linters already catch a substantial fraction of empty-body / no-assertion tests. SLOBAC's value here is the *cases the linter cannot see* — assertion-shaped statements that exercise no SUT, fixtures declared but unread elsewhere, debug-`print`/`console.log` in the body where an assertion was intended. Don't double-report what the repo's lint already gates; the audit's contribution is the semantic-judgment subset, not the syntactic subset.
- **Explicit pending markers are the fix, not the smell.** `it.todo(...)`, `xit`, `test.skip(...)`, `@pytest.mark.skip(reason=...)`, `t.Skip(...)`, RSpec `pending(:reason)` — these surface as known gaps in CI reports and explicitly opt out of the "passing" verdict the smell warns about. They are the *prescribed transform* for "stub that was meant to test something." Don't flag tests already using a pending marker with a reason; flag silent-green stubs that report passing while verifying nothing.

## Prescribed Fix

Two transforms, depending on intent:

1. **Dead scaffold, no intent to test.** Delete the file, block, or fixture. Clean and safe; the preservation gate allows coverage to drop here with a named rationale, since the deleted code killed no mutants.
2. **Stub that was meant to test something.** Mark explicitly: either convert to the runner's pending/xit marker (`it.todo(...)`, `xit`, `@pytest.mark.skip`) so it shows as "known gap" in reports, or write the missing assertion using [describe-before-edit](../principles/refactor-qualities.md#behavior-articulation-before-change) to guess intent from the name. If the intent is ambiguous, prefer explicit pending.

Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power). `.todo` / `skip` conversions must include a reason string.

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
- [`pseudo-tested`](./pseudo-tested.md) — SUT runs but no oracle; hard to distinguish from rotten-green without [describe-before-edit](../principles/refactor-qualities.md#behavior-articulation-before-change).
- [`shared-state`](./shared-state.md) — dead shared setup is a rotten-green subcase.

## Polyglot notes

Every runner has a pending/todo marker: `it.todo` / `xit` / `test.skip` / `@pytest.mark.skip` / `pending(:reason)` / `t.Skip` in Go. Adopt the repo's existing convention.
