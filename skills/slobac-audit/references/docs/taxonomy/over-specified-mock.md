# Over-Specified Mock

| Slug | Severity | Protects |
|---|---|---|
| `over-specified-mock` | High | [Maintainable](../principles.md#maintainable), [Independent of implementation](../principles.md#independent-of-implementation) |

## Summary

The test pins exact interaction details — call counts, call order, numeric index into `mock.calls`, `verifyNoMoreInteractions`, `ArgumentCaptor` deep inspection — where the product contract doesn't require them. Internal refactors break the test without breaking any user-visible behavior.

## Description

Two distinct shapes fit here:

- **Over-specified interactions.** Exact call counts, strict ordering, `verifyNoMoreInteractions`, cascades of `mockResolvedValueOnce` that break when internal calls reorder.
- **Testing internal details.** `ArgumentCaptor` deep inspection, `verify(never())` mirroring private branches, assertions on `toHaveBeenCalledWith` pinning production constants (file paths, timeouts, feature flags).

The semantic judgment: read the mock assertion and ask *"if the SUT refactored to call the collaborator differently but produced the same external outcome, would this test still pass?"* If no, it's over-specified.

This is distinct from [`tautology-theatre`](./tautology-theatre.md): there the SUT doesn't run at all; here it runs, but the test asserts on *how* it does its work rather than *what* it does.

## Signals

- Numeric index into `mock.calls[0][N]` for `N ≥ 2`.
- Cascades of `mockResolvedValueOnce(...)` in a specific order.
- `verifyNoMoreInteractions(mock)` / `expect(fn).toHaveBeenCalledTimes(exactN)` for N > 1 when the contract only says "called".
- `toHaveBeenCalledWith("/tmp/github-images", ...)` — production constant baked into the test.
- `ArgumentCaptor<Foo>` followed by field-by-field assertions on the captured argument.
- `have_received(:generate)` tail after a stub block that already asserts on the input.
- Mock-verification duplicating an expectation already inside a stub's callback.

## False-positive guards

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

1. Identify whether the collaboration is contract-relevant (e.g. "must call `paymentClient` exactly once per invoice") or incidental ("happens to call `logger.debug` three times").
2. For contract-relevant interactions: keep one focused assertion, remove the others. Use matcher-based matchers (`expect.anything()`, `expect.stringContaining(...)`) so argument order can change.
3. For incidental interactions: delete the mock assertions entirely; rely on output assertions.
4. Replace ordered `mockResolvedValueOnce` queues with a lookup-keyed fake (`(txid) => fixtures[txid]`).
5. For mock-queues-as-contract: extract a minimal `Fake<Client>` class once per suite; tests reference its observable behavior, not the queue.
6. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power). Tests should now survive an internal refactor of the SUT that preserves the external contract — verify with a targeted codemod that reorders an internal call.

## Example

### Before

```javascript
it('downloads the referenced image', async () => {
  const fetchMock = jest.fn()
    .mockResolvedValueOnce({ ok: true, arrayBuffer: async () => buf1 })
    .mockResolvedValueOnce({ ok: true, arrayBuffer: async () => buf2 });
  await downloadImages(urls, { fetch: fetchMock });
  expect(fetchMock).toHaveBeenCalledTimes(2);
  expect(fetchMock).toHaveBeenNthCalledWith(1, urls[0], { timeout: 5000 });
  expect(fetchMock).toHaveBeenNthCalledWith(2, urls[1], { timeout: 5000 });
  expect(fs.writeFileSync).toHaveBeenCalledWith("/tmp/github-images", buf1);
  expect(fs.writeFileSync).toHaveBeenCalledWith("/tmp/github-images", buf2);
});
```

Locks fetch order; pins the timeout constant; pins the hard-coded tmp dir.

### After

```javascript
it('downloads every referenced image to the configured directory', async () => {
  const byUrl = { [urls[0]]: buf1, [urls[1]]: buf2 };
  const fetchMock = jest.fn(async (u) => ({ ok: true, arrayBuffer: async () => byUrl[u] }));
  const outDir = path.join(tmpdir(), 'slobac-test');
  await downloadImages(urls, { fetch: fetchMock, outDir });
  expect(await fs.readdir(outDir)).toHaveLength(urls.length);
  for (const url of urls) {
    const contents = await fs.readFile(path.join(outDir, basename(url)));
    expect(contents.equals(byUrl[url])).toBe(true);
  }
});
```

Now asserts observable outcome (files written with correct content) and is robust to fetch-order refactors. The `timeout` and `outDir` constants are no longer duplicated here.

## Related modes

- [`tautology-theatre`](./tautology-theatre.md) — related mock-shaped smell where SUT doesn't run.
- [`implementation-coupled`](./implementation-coupled.md) — "testing internal details" often co-occurs with private-API reach-through.
- [`presentation-coupled`](./presentation-coupled.md) — similar root cause (asserting on *how* not *what*) but with rendered text instead of mock interactions.

## Polyglot notes

Appears in every mocking framework: Mockito / JMockit (JVM), Jest / Sinon / Vitest (JS/TS), unittest.mock / pytest-mock (Python), RSpec / minitest-mock (Ruby), gomock / mockery (Go), NSubstitute / Moq (.NET). A per-framework signal table is required; the judgment layer is language-agnostic.
