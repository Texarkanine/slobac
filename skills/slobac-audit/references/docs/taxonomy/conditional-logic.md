# Conditional Test Logic

| Slug | Severity | Protects |
|---|---|---|
| `conditional-logic` | Medium | [Simple](../principles.md#simple), [Granular](../principles.md#granular) |

## Summary

`if X: assert(...)` or `try { sut() } catch(e) { assert(...) }` inside a test body. [Cyclomatic complexity](../principles.md#simple) > 1 means there's at least one path through the test that never reaches an assertion — vacuous by omission.

## Description

Tests with branches have at least one execution path that silently passes without asserting anything. The semantic judgment: decide, per branch, whether the `if` encodes **genuine optionality** (→ split into two tests with explicit preconditions) or is **compensating for an upstream oracle weakness** (→ remove the `if`, pin the precondition in the fixture, assert unconditionally).

Platform-skip branches (`if process.platform === 'win32'`) are a distinct subcase that should use the runner's skip mechanism instead.

## Signals

- AST: `IfStatement` inside a test-function body; the consequent contains `expect` / `assert`; the alternate is absent or contains no assertions.
- `try { sut() } catch (e) { expect(e.message).toBe(...) }` with no `assert.fail('should have thrown')` after the `try`. The catch is conditional on a throw actually happening.
- `if (process.platform === 'win32') return;` — platform skip expressed as body logic, not `it.skip` / `pytest.skip`.
- `if (graphData.edges.length > 0) { expect(...) }` paired with `toBeGreaterThanOrEqual(0)` — passes vacuously on empty input.
- Loops that assert inside but never on the loop's exit condition.

## False-positive guards

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

| Shape | Transform |
|---|---|
| `if (cond) expect(...)` with intended optionality | Split into two tests: one where `cond` is true (fixture pins it), one where `cond` is false (asserts the other branch). |
| `if (cond) expect(...)` compensating for a weak oracle | Fix the fixture so `cond` is guaranteed true; remove the branch; assert unconditionally. |
| `try { sut() } catch (e) { expect(...) }` | Replace with the runner's throw matcher: `expect(() => sut()).toThrow(...)` / `pytest.raises(T, match=...)` / `expect { ... }.to raise_error(T, /msg/)`. |
| Platform skip in body | Convert to `it.skip` / `pytest.mark.skipif` / `//go:build !windows` with a skip reason. |
| Loop without exit assertion | Assert on the collected results after the loop. |

Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power). Test-count delta > 0 is acceptable (splits produce more tests).

## Example

### Before

```javascript
it('parses trailing JSON', () => {
  try {
    parse('{ "a": 1 } garbage');
  } catch (e) {
    expect(e.message).toMatch(/trailing/);
  }
});
```

### After

```javascript
it('rejects trailing garbage after JSON value', () => {
  expect(() => parse('{ "a": 1 } garbage')).toThrow(/trailing/);
});
```

The original test passed silently if `parse` returned normally; the catch block was never reached and no assertion was checked. Moved to a throw matcher that verifies the exception *and* that one was raised.

## Related modes

- [`rotten-green`](./rotten-green.md) — cousin; conditional-logic is "has an assertion but skips it on some paths", rotten-green is "has no assertion at all".
- [`vacuous-assertion`](./vacuous-assertion.md) — `if`-gated weak checks overlap.

## Polyglot notes

Every runner has a throw matcher and a skip mechanism; the transforms are mechanical per-runner lookups. The detection (IfStatement in test body, try-without-fail-after) is AST-level and polyglot via tree-sitter / ast-grep.
