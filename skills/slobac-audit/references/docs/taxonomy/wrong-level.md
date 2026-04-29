# Wrong Level

| Slug | Severity | Protects |
|---|---|---|
| `wrong-level` | Medium | [Fast](../principles.md#fast), [Maintainable](../principles.md#maintainable) |

## Summary

The test is well-written but lives at the wrong [pyramid tier](../glossary.md#test-tier--pyramid-level): a "unit" test running a subprocess, an "integration" test that mocks every dependency, a build smoke colocated with millisecond-scoped assertions.

## Description

Runner conventions tie test location to test tier (`*.unit.test.ts` vs `*.integration.test.ts`, `tests/` vs `tests/integration/`, `@slow` tags, `-tags=integration` build constraints). When a test drifts, it incurs the worst cost of both tiers: slow enough to hurt dev-loop latency, yet not trustworthy enough to count as real integration coverage. The semantic judgment is classifying each test as **unit / component / integration** and comparing the answer to where it currently lives.

Do *not* try to enforce a global layer policy across repos — read the repo's existing conventions first.

## Signals

- A single test file imports both high-level rendering harnesses (`@inquirer/testing`-style) *and* pure computed exports.
- A "unit" test wraps `execSync('npm run build')`, `subprocess.run([...])`, or instantiates a DB client.
- A "unit" test mocks every dependency and asserts on `toHaveBeenCalledWith(...)` — it's actually a contract test, mis-named.
- A spec `send`s to private methods (`described_class.send(:foo, x)`) — should either become a public-API test or extract the private helper as a pure function with its own unit test file. See [`implementation-coupled`](./implementation-coupled.md) for the related reach-through smell.

## False-positive guards

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

1. Classify each test as unit / component / integration via [describe-before-edit](../principles.md#behavior-articulation-before-change) plus the signals above.
2. Split files by level, respecting repo conventions: `foo.test.ts` → `foo.unit.test.ts` + `foo.integration.test.ts`.
3. Apply the runner's markers (`@slow`, `@integration`, `pytest.mark.integration`, `//go:build integration`) so CI can shard correctly.
4. For private-method tests: convert to public-surface coverage, or extract the helper as a pure function. This is the only "refactor for testability" move the taxonomy permits, and only because it also clarifies architecture — see the [no-extract-for-testability governor rule](../principles.md#no-extract-for-testability) for the exception.
5. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power) plus no change in test count plus CI still green at each tier.

## Example

### Before

```typescript
// src/__tests__/page-sizing.test.ts
describe('checkboxSearch page sizing', () => {
  it('calculates dynamic page size', () => {
    expect(calculateDynamicPageSize(80, 24)).toBe(10);
  });

  it('renders the full dropdown', async () => {
    const ui = render(checkboxSearch, { choices: MANY });
    await ui.waitFor(/loaded/);
    expect(ui.lastFrame()).toContain('cursor');
  });
});
```

### After

```typescript
// src/__tests__/page-sizing.unit.test.ts
it('calculates dynamic page size', () => {
  expect(calculateDynamicPageSize(80, 24)).toBe(10);
});

// src/__tests__/page-sizing.integration.test.ts
it('renders the full dropdown', async () => {
  const ui = render(checkboxSearch, { choices: MANY });
  await ui.waitFor(/loaded/);
  expect(ui.lastFrame()).toContain('cursor');
});
```

The pure calculation belongs in the fast unit tier. The render test needs `@inquirer/testing` and takes ~200ms. Split by level; CI shards them independently.

## Related modes

- [`monolithic-test-file`](./monolithic-test-file.md) — level-mixing is one common reason files get monolithic.
- [`implementation-coupled`](./implementation-coupled.md) — private-method tests are often wrong-level *and* implementation-coupled; fix together.

## Polyglot notes

The layer vocabulary is universal; markers differ per runner:

- **Python:** `pytest.mark.integration`, path convention `tests/integration/`.
- **JS/TS:** filename suffix, Vitest `test.concurrent`, Playwright for e2e.
- **Go:** `//go:build integration` build tag, `_integration_test.go` convention.
- **Ruby:** `spec/integration/`, RSpec tags.
- **JVM:** Gradle source sets, Surefire/Failsafe, `@Tag`.
