# Loose-Text-Oracle

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `loose-text-oracle` | High | per-test | [Maintainable](../principles/test-qualities.md#maintainable), [Independent of implementation](../principles/test-qualities.md#independent-of-implementation) |

## Summary

The test uses an underdetermined substring or regex on runtime-emitted text — error messages, log lines, stdout/stderr — as the primary oracle for meaning, so opposite-polarity text that happens to contain the token still passes.

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

_Audience: human readers landing on this entry from a fuzzy search query. The audit orchestrator does not read this section — it requires explicit slug invocation._

## Description

The missing middle between [`presentation-coupled`](./presentation-coupled.md) (oracle too *strong* on presentation) and [`vacuous-assertion`](./vacuous-assertion.md) (effectively no check): there *is* an assertion on free text, but it underdetermines the semantic claim. `expect(err.message).toContain("timeout")`, `pytest.raises(..., match="timeout")`, `assert "success" in caplog.text` — each can stay green when the emitted text means the opposite of what the test name claims.

The semantic judgment: ask *"would text with the opposite meaning still match this substring/regex?"* If yes, and the match is the primary (or only) identifier of which behavior/failure occurred, the smell fires.

Distinct from [`prose-pin`](./prose-pin.md): that smell asserts on **committed** docs/skills file bytes, not process output. Distinct from presentation-coupled: long cosmetic HTML/`toContain` chains pin formatting accidents; this smell pins *underdetermined meaning* with a short ambiguous token.

Industry grounding: Go's "error strings are not part of the API," Node.js `ERR_` codes (messages are not the stable contract), Barr et al.'s partial-oracle vocabulary.

## Signals

- `pytest.raises(T, match="ambiguous")` / `toThrow(/timeout/)` / `err.message.includes("…")` as the *sole* oracle for which failure occurred.
- `assert "success" in caplog.text` / stdout/stderr substring where the token underdetermines outcome.
- Regex/message match identifying error *kind* rather than verifying a dynamic datum beside a typed primary oracle.
- Community shape: tests that would still pass if the SUT printed `"no timeout configured"` or `"operation success: false"`.

## False-positive guards

- **Typed / coded primary oracle with supplementary datum match.** `raises(NotFoundError, match="gamma")` where the type/code identifies the failure and the match only checks that a dynamic parameter name appears (Go Wiki carve-out) is legitimate. Flag only when the message match *is* the identifier of which failure occurred.
- **Text is the product.** Compiler/CLI/linter diagnostics, formatter output, and intentional UX copy verified via full golden/approval/snapshot files are explicit presentation contracts — not lone underdetermined substrings. Do not flag whole-output goldens where the rendered text is the specified deliverable.
- **i18n / message-key checks.** Asserting that the correct catalog key or locale entry is selected is a localization contract, not a loose meaning pin on free English.
- **Structured assert after parse.** Parsing a log line or message into fields and asserting on those fields is the prescribed fix shape — do not flag the cured form.
- **Vacuous `toThrow()` with no argument.** That extreme is closer to [`vacuous-assertion`](./vacuous-assertion.md) / rotten paths; escalate there when there is effectively no check. This entry is for *present but underdetermined* text matches.

## Prescribed Fix

| Shape | Transform |
|---|---|
| Message substring/regex as sole failure identity | Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class). |
| Log-line / stdout phrase as outcome claim | Assert structured log/event fields (event name, level, bound context), or assert the resulting state change. |
| Need to lock rendered diagnostics | Switch to an explicit golden/approval snapshot of the *full* output, reviewed as a presentation contract. |
| Dynamic datum in a human message | Keep message match only as *supplementary* beside type/code (parameter name appears). |

Hierarchy (strongest first): typed error + code → structured log/event fields → behavioral state change → full golden text → substring/regex (last resort, supplementary only).

Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power). Climbing the hierarchy must not drop mutants the old substring happened to kill; prefer typed oracles that kill *more* wrong answers, including opposite-polarity messages.

## Example

### Before

```python
def test_fetch_raises_on_timeout():
    # Opposite meaning that would also match: RuntimeError("timeout disabled").
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

The original oracle accepted any `RuntimeError` whose message happened to contain `"timeout"`, including opposite-polarity wording. The fixed form identifies the failure by type and structured fields; human message text is no longer the API.

## Related modes

- [`presentation-coupled`](./presentation-coupled.md) — too *strong* on exact/cosmetic presentation of SUT output; this entry is too *weak* / underdetermined on free text.
- [`vacuous-assertion`](./vacuous-assertion.md) — effectively no semantic check; loose-text-oracle still asserts, but underdetermines meaning.
- [`prose-pin`](./prose-pin.md) — committed docs/skills as oracle; different artifact kind, different fix (delete/docs-lint vs typed error).
- [`conditional-logic`](./conditional-logic.md) — `try/except` without fail often pairs with message asserts; after moving to a throw matcher, prefer type/code over `match=` as the semantic oracle.

## Polyglot notes

- **Python:** prefer custom exception classes / `pytest.raises(T)` without relying on `match=`; structlog / pytest-structlog for log fields.
- **JS/TS:** prefer `err.code` / custom error subclasses over `toThrow(/msg/)`; eslint-plugin-jest `require-to-throw-message` only kills the vacuous end — still require type/code beside any message.
- **Go:** `errors.Is` / `errors.As` and typed error values; Go Wiki permits string compare only for properties like parameter-name inclusion.
- **Ruby:** `raise_error(SomeError)` with typed class; avoid message-only `raise_error(/msg/)`.
- **Rust:** match error enums; for diagnostics that *are* the product, use UI/`trybuild` golden files rather than substring asserts.
