# Mystery Guest

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `mystery-guest` | Low | per-test | [Understandable](../principles/test-qualities.md#understandable), [Clear failure message](../principles/test-qualities.md#clear-failure-message) |

## Summary

A test's meaning depends on external data the reader can't see — a fixture file, a long heredoc, a shared factory — without any inline hint of which part of that data matters. The assertion compares against a magic number or string whose origin requires opening three other files.

## Aliases

- "mystery guest"
- "magic numbers in tests"
- "external fixture file with no summary"
- "fixture-coupled magic numbers"
- "obscure test"
- "heredoc without naming"
- "count == n with no comment"

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

## False-positive guards

External-data signals over-trigger in three shapes the audit must not flag:

- **Inlined derivation cures the magic number.** `assert count == EXPECTED_USER_MSGS + EXPECTED_ASSISTANT_MSGS` (or any expression that *names* the arithmetic) is not mystery-guest — a reader can see why the answer is what it is without leaving the test. Flag only unnamed magic literals (`assert count == 6` with no derivation in scope, no comment, no symbolic constant).
- **Real-world fixtures *are* the input domain.** Parser, codec, schema-validation, and migration tests legitimately read large fixture files because the file *is* the SUT's input contract. The fixture is not a hidden coupling; it is the test subject. Flag only when the *assertion* depends on an unstated property of the file (a magic count, a magic offset); do not flag tests that read a fixture and assert on a specifically-described, comment-summarized property of it.
- **Named factories with descriptive identifiers.** A `let user_with_two_orders = ...` or `make_session(messages=3)` factory call carries the relevant fixture shape in its *name*. The shape is not hidden; the identifier states it. Flag unnamed heredocs, unnamed `let` bindings, and bare `File.read(path)` patterns whose product is never named — not the named-factory pattern, even when the underlying fixture data is large.

## Prescribed Fix

1. [Describe-before-edit](../principles/refactor-qualities.md#behavior-articulation-before-change): identify which fixture property the assertion really depends on.
2. Add a ≤3-line comment stating the relevant fixture shape, not the whole shape.
3. Where an assertion expects a derived count, make the derivation explicit: `expected = USERS + ASSISTANTS` rather than `assert count == 6`.
4. Where heredocs have no name, bind them to a `let` / constant with a name that expresses the fixture's role.
5. Where fixtures are copy-pasted across related repos, note the opportunity for a shared support module — this is a cross-repo refactor, not a per-pass move.
6. Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power). Zero AST changes to assertions; only surrounding comments and constants change.

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
