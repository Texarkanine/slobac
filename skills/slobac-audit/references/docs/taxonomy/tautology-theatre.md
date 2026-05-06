# Tautology Theatre

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `tautology-theatre` | Critical | per-test | [Necessary](../principles/test-qualities.md#necessary), [Independent of implementation](../principles/test-qualities.md#independent-of-implementation) |

## Summary

The test doesn't exercise production code at all. The mock was configured to return X; the assertion checks that the mock returned X. The only thing verified is that the mocking library works.

## Aliases

- "tautology"
- "tautology theatre"
- "mock tautology"
- "tests that don't run production code"
- "no SUT call"
- "mock-of-SUT"
- "would-pass-if-prod-deleted"
- "framework test"
- "tests that only verify the mocking library works"

## Description

This entry belongs to the larger [Tautology Theatre](../principles/glossary.md#tautology-theatre) umbrella. Under the diagnostic question *"would this test still pass if all production code were deleted?"*, this is the strictest case: **yes, trivially, because the production code was never called.**

Two distinct shapes fit here:

- **Mock tautology.** Configure a mock to return X; assert the mock returns X; no SUT call between them. Logically `x = 5; assert x == 5`.
- **No production code exercised.** Every object in the test is a mock, or the mock *is* the unit under test (`jest.spyOn(sutInstance, 'method').mockReturnValue(...)`).

Severity is Critical because these tests produce the worst false-confidence signal in the suite *and* have the safest transform: **delete them.** A deleted tautology cannot reduce the [mutation kill-set](../principles/glossary.md#mutation-kill-set) — it was killing no mutants.

## Signals

- Sequence: `mockReturnValue(X)` → `sutStub.method()` → `expect(result).toBe(X)` with no non-mock function call in between.
- `jest.spyOn(sutInstance, 'method').mockReturnValue(...)` in the same file that imports the SUT class — mocking the unit under test.
- All objects in `beforeEach` have a mock factory; no real class constructor is called.
- Python: `@patch.object(sut, '_real_method', return_value=X); assert sut._real_method() == X`.
- Ruby: `allow(obj).to receive(:foo).and_return(X); expect(obj.foo).to eq(X)`.
- Go with gomock: `m.EXPECT().Foo().Return(X); out := m.Foo(); if out != X ...`.
- `assertTrue(true)`, `assertEquals(1, 1)`, `assertNotNull(new Object())` — trivial-tautology variant.
- Assertions on framework guarantees (`assertNotNull(mock(Foo.class))`) rather than app behavior — "framework test" variant.

## False-positive guards

Mock-shaped signals over-trigger in three classes the audit must distinguish:

- **Boundary fake feeding a real SUT transformation.** A test that mocks a network client / clock / random / filesystem to return `X`, then runs the *real* SUT (a parser, formatter, validator, state machine) against `X` and asserts on the SUT's transformation of `X` is not tautology. The mock is a boundary double; the SUT performed real work between the mock setup and the assertion. The smell fires only when the assertion compares to the mock's *configured value* with no SUT transformation in between — `mock.return_value = 5; assert sut_call() == 5` where `sut_call` is just the mock.
- **Spy with side-effect interception, not value replacement.** `jest.spyOn(sut, 'method')` *without* `.mockReturnValue(...)` (and analogues: `spy_on(obj, :method)` without `.and_return`, `mocker.spy(obj, 'method')` in pytest) observes the method's invocations while letting the real implementation run. The spy is a verification tool, not a value source. Flag the mock-of-SUT pattern only when the spy *short-circuits the real implementation* — returning a fixed literal, a stubbed value, or a fake that does not invoke the original method's logic. A `mockImplementation` wrapper that delegates to the original (`(...args) => original(...args)`) still runs real SUT code and is not tautology.
- **Single deliberate framework-bootstrap smoke test.** A lone "the test runner imports the module and hits a trivial public call" smoke test is a defensible suite-bootstrap convention — it catches wiring breakage early without claiming behavior coverage. Flag *clusters* of framework-only assertions (`assertNotNull(mock(Foo.class))` repeated across many files, `assertTrue(true)` blocks scattered through a suite); do not flag the lone bootstrap.

## Prescribed Fix

### Preferred: delete

A tautology test provably verifies nothing; regression-detection power cannot regress because nothing was covered.

1. [Describe-before-edit](../principles/refactor-qualities.md#behavior-articulation-before-change): confirm the test genuinely verifies nothing (two-reader rule — proposer and reviewer must agree).
2. Delete the test; delete its now-orphan fixtures and mocks.
3. If a reviewer believes behavior *should* be covered but isn't, emit a **coverage gap note** to the plan artifact — do not add a new test, since net-new test generation is out of scope for this catalog; hand off to a coverage-generator tool.
4. Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power), with a relaxed coverage rule — coverage may drop if and only if the rationale is "deleted tautology, no lost mutants."

### Alternative: rewrite

If the test clearly *intended* to exercise the SUT, instantiate the real class, remove the mock-of-SUT, and assert on observable output. This is a separate move; do not chain delete + rewrite in one commit.

## Example

### Before

```javascript
it('detects fee payment', () => {
  const detector = new BitcoinBillDetector();
  jest.spyOn(detector, 'isFeePayment').mockReturnValue(false);
  const result = detector.isFeePayment({ amount: 1000 });
  expect(result).toBe(false);
});
```

`isFeePayment` on `detector` is the method supposedly under test, and it's been replaced by a mock. This test verifies that `jest.spyOn` works.

### After — deletion commit

The rationale message reads:

> Deleted. The test mocked `BitcoinBillDetector#isFeePayment` on the detector under test; the assertion verified the mock's return value, not the real method. No mutants were previously killed by this test. Coverage gap recorded in `plan.md#coverage-gaps` for potential test-generation pickup.

## Related modes

- [`pseudo-tested`](./pseudo-tested.md), [`vacuous-assertion`](./vacuous-assertion.md) — siblings in the [Tautology Theatre](../principles/glossary.md#tautology-theatre) umbrella; weaker forms.
- [`over-specified-mock`](./over-specified-mock.md) — different mock-shaped smell where the SUT *does* run but the assertions over-constrain it.
- [`rotten-green`](./rotten-green.md) — covers the trivial-tautology variant (`assertTrue(true)`).

## Polyglot notes

The "mock of the SUT" pattern is universal: `monkeypatch.setattr(self, 'method', ...)` in Python, `instance_double(self.class)` in Ruby, `gomock` on concrete types, NSubstitute on the class under test in .NET. A per-ecosystem signal table is required; the judgment layer is language-agnostic.
