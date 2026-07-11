# Loose-Text-Oracle

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `loose-text-oracle` | High | per-test | [Maintainable](../principles/test-qualities.md#maintainable), [Independent of implementation](../principles/test-qualities.md#independent-of-implementation) |

## Summary

The test treats a substring or regex on runtime-emitted text — error messages, log lines, stdout/stderr — as locking a specific meaning, but token presence is an unanchored proxy: many distinct emissions that share the token still pass.

## Aliases

- "loose text oracle"
- "weak text oracle"
- "underdetermined text"
- "message pin"
- "error string as API"
- "toContain on err.message"
- "pytest.raises match-only"
- "assert phrase in caplog"
- "partial message oracle"

## Description

The missing middle between [`presentation-coupled`](./presentation-coupled.md) (oracle too *strong* on presentation) and [`vacuous-assertion`](./vacuous-assertion.md) (effectively no check): there *is* an assertion on free text, but the match does not anchor the semantic claim the author thought they locked.

Classic shape — the author meant "too many connections," but wrote `expect(message).toContain("connection")`. All of these stay green:

- `error: too many connections!`
- `error: connection couldn't be established`
- `error: database "connection" not found on host`

Opposite-polarity wording (`"timeout disabled"`, `"operation success: false"`) is the same failure mode, not a separate one: the token is present while the meaning is not the one under test.

The semantic judgment: ask *"which distinct meanings or failure modes would still match this substring/regex?"* If more than the intended claim would pass, and the match is the primary (or only) identifier of which behavior/failure occurred, the smell fires.

Distinct from [`prose-pin`](./prose-pin.md): that smell asserts on **committed** docs/skills file bytes, not process output. Distinct from presentation-coupled: long cosmetic HTML/`toContain` chains pin formatting accidents; this smell pins an *unanchored meaning proxy* with a shared token.

Industry grounding: Go's "error strings are not part of the API,"[^cheney][^go-wiki] Node.js `ERR_` codes (messages are not the stable contract),[^nodejs-err] and Barr et al.'s partial-oracle vocabulary.[^barr]

## Signals

- `pytest.raises(T, match="ambiguous")` / `toThrow(/connection/)` / `err.message.includes("…")` as the *sole* oracle for which failure occurred.
- Shared-token matches where several distinct failures contain the same word (`"connection"`, `"timeout"`, `"success"`).
- `assert "success" in caplog.text` / stdout/stderr substring where the token underdetermines outcome.
- Regex/message match identifying error *kind* rather than verifying a dynamic datum beside a typed primary oracle.
- Community shape: tests that would still pass for an unrelated failure, an opposite-polarity message, or a coincidental token in an otherwise different diagnostic.

## False-positive guards

- **Typed / coded primary oracle with supplementary datum match.** `raises(NotFoundError, match="gamma")` where the type/code identifies the failure and the match only checks that a dynamic parameter name appears (Go Wiki carve-out)[^go-wiki] is legitimate. Flag only when the message match *is* the identifier of which failure occurred.
- **Text is the product.** Compiler/CLI/linter diagnostics, formatter output, and intentional UX copy verified via full golden/approval/snapshot files are explicit presentation contracts — not lone underdetermined substrings. Do not flag whole-output goldens where the rendered text is the specified deliverable.
- **i18n / message-key checks.** Asserting that the correct catalog key or locale entry is selected is a localization contract, not a loose meaning pin on free English.
- **Structured assert after parse.** Parsing a log line or message into fields and asserting on those fields is the prescribed fix shape — do not flag the cured form.
- **Vacuous `toThrow()` with no argument.** That extreme is closer to [`vacuous-assertion`](./vacuous-assertion.md) / [`rotten-green`](./rotten-green.md); escalate there when there is effectively no check. This entry is for *present but unanchored* text matches.

## Prescribed Fix

| Shape | Transform |
|---|---|
| Message substring/regex as sole failure identity | Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class). |
| Log-line / stdout phrase as outcome claim | Assert structured log/event fields (event name, level, bound context), or assert the resulting state change. |
| Need to lock rendered diagnostics | Switch to an explicit golden/approval snapshot of the *full* output, reviewed as a presentation contract. |
| Dynamic datum in a human message | Keep message match only as *supplementary* beside type/code (parameter name appears). |

Preference order (strongest first):

1. Typed error + stable machine code
2. Structured log / event fields
3. Behavioral state change
4. Full golden / approval text (when the rendered output *is* the product)
5. Substring / regex — last resort, and only as a supplementary datum check beside (1)

Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power). Climbing the hierarchy must not drop mutants the old substring happened to kill; prefer typed oracles that reject the unrelated failures the token would have accepted.

## Example

### Before

```python
def test_fetch_raises_on_timeout():
    # Also matches: "timeout disabled", "no timeout configured", …
    with pytest.raises(RuntimeError, match="timeout"):
        fetch("alpha", fail="timeout")
```

### After

```python
def test_fetch_raises_on_timeout():
    with pytest.raises(TimeoutError) as exc_info:
        fetch("alpha", fail="timeout")
    assert exc_info.value.resource == "alpha"  # structured field, not message text
```

The original oracle accepted any `RuntimeError` whose message happened to contain `"timeout"` — including unrelated and opposite-polarity wording. The fixed form identifies the failure by type and structured fields; human message text is no longer the API.

## Related modes

- [`presentation-coupled`](./presentation-coupled.md) — too *strong* on exact/cosmetic presentation of SUT output; this entry is too *weak* / unanchored on free text.
- [`vacuous-assertion`](./vacuous-assertion.md) — effectively no semantic check; loose-text-oracle still asserts, but the match does not lock the claimed meaning.
- [`prose-pin`](./prose-pin.md) — committed docs/skills as oracle; different artifact kind (file bytes vs runtime emission).
- [`conditional-logic`](./conditional-logic.md) — `try/except` without fail often pairs with message asserts on the caught error.
- [`rotten-green`](./rotten-green.md) — no assertion at all; escalate bare `toThrow()` / empty bodies there, not here.

## Polyglot notes

- **Python:** prefer custom exception classes / `pytest.raises(T)` without relying on `match=`; structlog / pytest-structlog for log fields.
- **JS/TS:** prefer `err.code` / custom error subclasses over `toThrow(/msg/)`; eslint-plugin-jest `require-to-throw-message` only kills the vacuous end — still require type/code beside any message.
- **Go:** `errors.Is` / `errors.As` and typed error values; Go Wiki permits string compare only for properties like parameter-name inclusion.[^go-wiki]
- **Ruby:** `raise_error(SomeError)` with typed class; avoid message-only `raise_error(/msg/)`.
- **Rust:** match error enums; for diagnostics that *are* the product, use UI/`trybuild` golden files rather than substring asserts.

[^cheney]: Cheney, D. (2016). *Don't just check errors, handle them gracefully*. <https://dave.cheney.net/2016/04/27/dont-just-check-errors-handle-them-gracefully>. "Comparing the string form of an error is, in my opinion, a code smell."

[^go-wiki]: Go Wiki, *Go Test Comments* — "Error strings." <https://go.dev/wiki/TestComments#error-strings>. Discourages string comparison to identify error *kind*; permits checking that a message includes a dynamic property such as a parameter name.

[^nodejs-err]: Node.js API docs, *Errors* — `error.code`. <https://nodejs.org/api/errors.html#errorcode>. "`error.code` is the most stable way to identify an error… In contrast, `error.message` strings may change between any versions of Node.js."

[^barr]: Barr, E., Harman, M., McMinn, P., Shahbaz, M., & Yoo, S. (2015). *The Oracle Problem in Software Testing: A Survey*. IEEE Transactions on Software Engineering, 41(5), 507–525. <https://doi.org/10.1109/TSE.2014.2372785>. Defines partial oracles as specifying important but incomplete properties of the SUT.
