# Wrong Level

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `wrong-level` | Medium | cross-suite | [Fast](../principles/test-qualities.md#fast), [Maintainable](../principles/test-qualities.md#maintainable) |

## Summary

The test is well-written but lives at the wrong [test level](../principles/glossary.md#test-level): a "unit" test running a subprocess, an "integration" test that mocks every dependency, a build smoke colocated with millisecond-scoped assertions.

## Aliases

- "wrong level"
- "unit test doing integration"
- "integration test that's really unit"

## Description

Runner conventions tie test location to test level (`*.unit.test.ts` vs `*.integration.test.ts`, `tests/` vs `tests/integration/`, `@slow` tags, `-tags=integration` build constraints). When a test drifts, it incurs the worst cost of both levels: slow enough to hurt dev-loop latency, yet not trustworthy enough to count as real integration coverage. The semantic judgment is classifying each test per [Classifying test level](#classifying-test-level) and comparing the answer to where it currently lives.

Do *not* try to enforce a global layer policy across repos — read the repo's existing conventions first.

## Classifying test level

Use this section to decide **what ran** (unit vs integration, then the four named levels) before comparing that judgment to the repo's markers (directory, filename, tags), not the other way around.

**Primary split — unit vs integration:** In a **unit** test, the test-time call stack stays **inside** the SUT. In an **integration** test, it **deliberately exits** the SUT. Everything else is secondary but still matters for relocation — pick unit/integration first, then refine.

**Secondary split** within each family — simple vs. component, simple integration vs. functional — matters just as much for picking the right bucket once unit/integration is settled.

### Unit tests

The test-time call stack stays inside the SUT.

| Level | What it tests | CLI example | Web app example |
|---|---|---|---|
| **Simple unit** | Pure function. No I/O, no fixtures beyond arguments. | A helper used by the CLI. | A helper used by the controller. |
| **Component** | Module under test, with mocks/fakes/dummies isolating external deps. | Function that would make an HTTP request, with the request mocked. | Controller invoked directly; Model and View mocked. |

### Integration tests

The test-time call stack deliberately exits the SUT.

| Level | What it tests | CLI example | Web app example |
|---|---|---|---|
| **Simple integration** | SUT calls into code outside its own module or package, for real. | Function that makes an actual HTTP request. | Framework binds the controller; the framework's request-handling code calls through to it. |
| **Functional** | Software runs "for real"; the test is a harness invoking it the way a user would. | Compiled CLI binary invoked with arguments (and maybe a real HTTP request happens). | Web app started; real HTTP request sent to `localhost` over the machine's networking stack. |

**Depth:** A **low** test level sits close to the code under assertion — little more than arguments and return values. A **high** test level pulls in a thick stack: subprocess or HTTP to `localhost`, kernel and runtime scheduling, framework dispatch, then finally the slice of product code you care about. That vertical distance is what people informally call “pyramid height” or “how high up the stack.”

**Intersections:** Wrong level often shows up beside other smells (e.g. [`monolithic-test-file`](./monolithic-test-file.md), [`implementation-coupled`](./implementation-coupled.md)). Classify level first; then decide whether the fix is relocation, split, or a narrower companion smell.

## Signals

- A single test file imports both high-level rendering harnesses (`@inquirer/testing`-style) *and* pure computed exports.
- A "unit" test wraps `execSync('npm run build')`, `subprocess.run([...])`, or instantiates a DB client.
- A "unit" test mocks every dependency and asserts on `toHaveBeenCalledWith(...)` — it's actually a contract test, mis-named.
- A spec `send`s to private methods (`described_class.send(:foo, x)`) — should either become a public-API test or extract the private helper as a pure function with its own unit test file. See [`implementation-coupled`](./implementation-coupled.md) for the related reach-through smell.

## False-positive guards

Level signals are repo-conditional and over-trigger when applied as if they were universal:

- **The repo's existing layer convention is authoritative.** Before flagging a test for living at the wrong level, read the repo's tier conventions: directory layout (`tests/integration/`), filename suffixes (`*.unit.test.ts`, `*_integration_test.go`), runner markers (`pytest.mark.integration`, `@Tag("slow")`), and build constraints (`//go:build integration`). If the test sits in a tier the repo treats as appropriate for the test's content, do not flag — even if a different repo would file it differently. The signal is mismatch between a test's content and its repo's stated tier, not mismatch with an idealized pyramid.
- **Co-location-by-convention single-file ecosystems.** Some ecosystems place all tier coverage for a unit in one file by design — Go's `package_test.go` adjacent to `package.go`, Rust's `#[cfg(test)] mod tests` — and the build system shards via tags or build constraints. Flag only when the colocation incurs the cost the smell warns about (slow tests blocking the dev-loop tier), not when the colocation is the ecosystem's idiomatic shape and the cost is already mitigated by the runner.

## Prescribed Fix

1. Classify each test per [Classifying test level](#classifying-test-level) plus [describe-before-edit](../principles/refactor-qualities.md#behavior-articulation-before-change) and the [signals](#signals) above.
2. Split files by level, respecting repo conventions: `foo.test.ts` → `foo.unit.test.ts` + `foo.integration.test.ts`.
3. Apply the runner's markers (`@slow`, `@integration`, `pytest.mark.integration`, `//go:build integration`) so CI can shard correctly.
4. For private-method tests: convert to public-surface coverage, or extract the helper as a pure function. This is the only "refactor for testability" move the taxonomy permits, and only because it also clarifies architecture — see the [no-extract-for-testability governor rule](../principles/refactor-qualities.md#no-extract-for-testability) for the exception.
5. Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power) plus no change in test count plus CI still green at each tier.

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

The pure calculation belongs at the fast **simple unit** level. The render test needs `@inquirer/testing` and takes ~200ms. Split by level; CI shards them independently.

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
