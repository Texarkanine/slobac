# Mystery Guest

| Slug | Severity | Protects |
|---|---|---|
| `mystery-guest` | Low | [Understandable](../principles.md#understandable), [Clear failure message](../principles.md#clear-failure-message) |

## Summary

A test's meaning depends on external data the reader can't see — a fixture file, a long heredoc, a shared factory — without any inline hint of which part of that data matters. The assertion compares against a magic number or string whose origin requires opening three other files.

## Description

A classical xUnit test smell,[^xunit-patterns] still relevant. Covers two variants:

- **Classical mystery guest** — `File.read('fixture.jsonl')` then `assert len(rows) == 6` with no hint *why* 6.
- **Fixture-coupled magic numbers** — exact counts tied to fixture file size or order, brittle to any fixture edit.

The semantic judgment: summarize in one sentence the *relevant* shape of the fixture for this assertion — not the whole shape — and surface that as a comment or derived constant.

This is the lowest-risk, highest-readability entry in the catalog; the transform adds documentation and never changes assertions.

## Signals

- `assert count == <n>` with no adjacent comment and `<n>` not derived from anything named in the test.
- `File.read(path)` / `fs.readFileSync(path)` followed by assertions with no inline fixture summary.
- Long `<<~HEREDOC` blocks as `let` inputs with no naming.
- Test imports a fixture module but shadows part of its contents silently.
- Magic constant (`6`, `"abc123"`) compared against parsed fixture output.

## Prescribed Fix

1. [Describe-before-edit](../principles.md#behavior-articulation-before-change): identify which fixture property the assertion really depends on.
2. Add a ≤3-line comment stating the relevant fixture shape, not the whole shape.
3. Where an assertion expects a derived count, make the derivation explicit: `expected = USERS + ASSISTANTS` rather than `assert count == 6`.
4. Where heredocs have no name, bind them to a `let` / constant with a name that expresses the fixture's role.
5. Where fixtures are copy-pasted across related repos, note the opportunity for a shared support module — this is a cross-repo refactor, not a per-pass move.
6. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power). Zero AST changes to assertions; only surrounding comments and constants change.

## Example

### Before

```python
def test_parses_cursor_session_rollout(tmp_path):
    shutil.copytree(FIXTURES / 'cursor-rollout', tmp_path, dirs_exist_ok=True)
    rows = sync(tmp_path)
    assert len(rows) == 6
```

### After

```python
def test_parses_cursor_session_rollout(tmp_path):
    # Fixture shape: 3 user + 3 assistant messages across 2 sessions.
    # `sync` returns one row per message.
    shutil.copytree(FIXTURES / 'cursor-rollout', tmp_path, dirs_exist_ok=True)
    rows = sync(tmp_path)
    EXPECTED_USER_MSGS = 3
    EXPECTED_ASSISTANT_MSGS = 3
    assert len(rows) == EXPECTED_USER_MSGS + EXPECTED_ASSISTANT_MSGS
```

A reader can now see why `6` is the right answer without opening the fixture. A new contributor editing the fixture would edit the constants, not chase a magic number.

## Related modes

- [`shared-state`](./shared-state.md) — shared fixtures are often also mystery guests.
- [`presentation-coupled`](./presentation-coupled.md) — both pin on incidental details of an external artifact.

## Polyglot notes

Universal. The mechanical transform is language-agnostic (comment insertion plus symbolic constant naming).

[^xunit-patterns]: The "Mystery Guest" name comes from Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code* (Addison-Wesley, 2007). See the online catalog at <http://xunitpatterns.com/Obscure%20Test.html#Mystery%20Guest>.
