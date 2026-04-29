# Naming Lies

| Slug | Severity | Protects |
|---|---|---|
| `naming-lies` | Medium | [Understandable](../principles.md#understandable), [Well-named](../principles.md#well-named), [Clear failure message](../principles.md#clear-failure-message) |

## Summary

The test title or docstring claims behavior X; the body verifies behavior Y (usually a weaker Y). The reader trusts the name, and the name is wrong.

## Description

Unlike [`deliverable-fossils`](./deliverable-fossils.md) — which is about suite-wide naming shaped by history — this is the per-test variant: a single test whose title promises more than the assertions deliver. LLMs parse natural language; static tools cannot tell that `it('should use cyan/blue styling for descriptions')` doesn't check any ANSI escape code.

The fix is either *rename the test* (cheaper, when the body is already strong) or *strengthen the body* (when the title captured real intent that the assertions under-deliver on). That second path overlaps with [`vacuous-assertion`](./vacuous-assertion.md).

## Signals

- Tokenize the title/docstring; tokenize the assertion lines; find title-nouns with zero surface in the assertion set.
- Title says "color | ANSI | styling | cyan | bold | italic" but the body has no ANSI-regex or theme mock.
- Docstring claims "defaults to zero" but the body never compares to zero.
- Docstring claims a derivation rule ("last path segment of the workspace slug") but the assertion is `len(x) > 0`.
- Title contains `random`, but no distribution or variance check; only prefix and length.

## Prescribed Fix

For each flagged test, the LLM decides among three paths:

- **Body is correct, title lies.** Rename to match the body. Safest move; the preservation gate is trivial (rename only).
- **Title is the real intent, body is weak.** Strengthen assertions (handoff to [`vacuous-assertion`](./vacuous-assertion.md)); rename only if still necessary after.
- **Both are stale.** Investigate with [describe-before-edit](../principles.md#behavior-articulation-before-change); may reveal a [`deliverable-fossil`](./deliverable-fossils.md).

Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power). For rename-only, verify the call graph is unchanged. For strengthen, verify the [mutation kill-set](../glossary.md#mutation-kill-set) delta is ≥ 0.

## Example

### Before

```python
def test_token_counts_default_to_zero():
    conn.execute("INSERT INTO sessions ...")
    row = conn.execute("SELECT token_count FROM sessions").fetchone()
    assert row[0] > 0  # the name said "default to zero"
```

### After — option A, rename to match body

```python
def test_token_count_populated_from_inserted_session():
    conn.execute("INSERT INTO sessions ...")
    row = conn.execute("SELECT token_count FROM sessions").fetchone()
    assert row[0] > 0
```

### After — option B, strengthen body to match title

```python
def test_token_counts_default_to_zero():
    conn.execute("INSERT INTO sessions (id) VALUES ('abc')")  # no token_count provided
    row = conn.execute("SELECT token_count FROM sessions WHERE id = 'abc'").fetchone()
    assert row[0] == 0
```

The body did not verify the claim. The LLM picks option B here because an earlier schema check confirmed `token_count` had a `DEFAULT 0`; the title captured the real contract.

## Related modes

- [`deliverable-fossils`](./deliverable-fossils.md) — suite-wide naming rot; this entry is the per-test variant.
- [`vacuous-assertion`](./vacuous-assertion.md) — when "strengthen the body" is the right response.
- [`rotten-green`](./rotten-green.md) — naming lies where the body contains no assertions at all.

## Polyglot notes

Trivially polyglot. Tokenization plus surface comparison is the same everywhere; ANSI-specific signals are English-language and encoder-agnostic.
