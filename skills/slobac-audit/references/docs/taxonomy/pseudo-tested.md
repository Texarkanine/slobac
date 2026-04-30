# Pseudo-Tested

| Slug | Severity | Protects |
|---|---|---|
| `pseudo-tested` | High | [Necessary](../principles.md#necessary), [Granular](../principles.md#granular) |

## Summary

Replace the SUT body with `return;` / `return null` / `return input` — every test still passes. The SUT *runs*, the test *asserts*, but the assertion could not tell a working implementation from a no-op one.

## Description

This is the [extreme-mutation / pseudo-tested-methods](../glossary.md#extreme-mutation--pseudo-tested-methods) smell: methods whose bodies can be replaced with a no-op without any test noticing. Niedermayr et al.[^niedermayr] measured a median of 10.1% of methods in studied Java suites being pseudo-tested — a cheap, high-signal mutation class (often run via [Descartes](../glossary.md#descartes) on JVM, `mutmut --simple-mutations` on Python, `cargo-mutants` on Rust, or Stryker's block-statement mutator on JS/TS).

This entry is the mutation-adjacent sibling of [`vacuous-assertion`](./vacuous-assertion.md). The [Tautology Theatre](../glossary.md#tautology-theatre) operational test — "would this test still pass if all production code were deleted?" — has `pseudo-tested` as a strict subset ("would it still pass if production code were no-opped?").

A reader can *conjecture* without running a mutator: "if `short_digest` returned `''`, would any existing test fail?" Read the suite, answer yes/no, and add the missing assertion. A real mutation run later confirms.

## Signals

- Test body calls SUT, assigns to `_`, then runs only structural shape / type / length checks.
- Assertions after the SUT call check only "non-empty" or "has this key".
- SUT return value is never compared to an expected value.
- A file-touching SUT is tested by checking a file exists, not its content.
- Confirmatory cross-check: run [Descartes](../glossary.md#descartes) / `mutmut --simple-mutations` / equivalent; any surviving no-op mutant is evidence for this mode.

## False-positive guards

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

1. For the canonical test in the cluster, identify the SUT's actual output contract.
2. Add the one assertion that would fail under `return default`: compare to an expected value, parse the output and assert on its shape, hash the file content, etc.
3. Keep the fix local — one well-placed assertion in the canonical test, not N across N tests.
4. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power), *stricter* than the default — at least one previously-surviving no-op mutant now dies. [Mutation kill-set](../glossary.md#mutation-kill-set) delta must be strictly positive.

## Example

### Before

```python
def test_corrupt_tracking_db_graceful_skip(tmp_path):
    corrupt_db = tmp_path / "tracking.db"
    corrupt_db.write_bytes(b"garbage")
    sync_tracking_db(corrupt_db)  # should skip without raising
```

`sync_tracking_db` could be `def sync_tracking_db(_): pass` and this test still passes. The "graceful skip" contract is asserted only by the absence of an exception.

### After

```python
def test_corrupt_tracking_db_logged_and_marked_skipped(tmp_path, caplog):
    corrupt_db = tmp_path / "tracking.db"
    corrupt_db.write_bytes(b"garbage")
    result = sync_tracking_db(corrupt_db)
    assert result.status == "skipped"
    assert result.reason == "corrupt_db"
    assert any("tracking.db" in rec.message for rec in caplog.records)
```

Now `pass` fails (`result` is `None`; attribute access raises). A no-op mutation dies. The "graceful skip" contract is now encoded as a positive return plus a log line.

## Related modes

- [`vacuous-assertion`](./vacuous-assertion.md) — same family; asserts *something*, but insufficient.
- [`tautology-theatre`](./tautology-theatre.md) — SUT never runs at all.
- [`rotten-green`](./rotten-green.md) — SUT call with zero assertions; hard to distinguish from pseudo-tested without [describe-before-edit](../principles.md#behavior-articulation-before-change).

## Polyglot notes

Every ecosystem has at least one extreme-mutation driver:

- **JVM:** [Descartes](../glossary.md#descartes) engine for PIT.
- **Python:** `mutmut --simple-mutations`, Cosmic Ray.
- **Rust:** `cargo-mutants`.
- **JS/TS/.NET:** Stryker's block-statement mutator.
- **Go:** `go-mutesting`, go-gremlins.

A reader's cheap conjecture pass works without any of them; full confirmation benefits from the tool.

[^niedermayr]: Niedermayr, R., Juergens, E., & Wagner, S. (2019). *Will my tests tell me if I break this code?* Empirical Software Engineering, 24(6), 4085–4130. <https://link.springer.com/article/10.1007/s10664-018-9653-2>. The 10.1% pseudo-tested median appears in Table 3 of the paper.
