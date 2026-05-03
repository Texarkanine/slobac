# Monolithic Test File

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `monolithic-test-file` | Medium | per-file | [Understandable](../principles.md#understandable), [Maintainable](../principles.md#maintainable) |

## Summary

A single test file mixes multiple behavior domains — parser tests next to integration tests next to regression cases next to contract tests — usually because every new feature accreted into the file of least resistance. Hard to navigate, hard to diff, hard to assign ownership.

## Description

The suite-level analogue of a single test that does too much — a file, not a test, that has outgrown its subject. Often co-occurs with and amplifies [`semantic-redundancy`](./semantic-redundancy.md) (authors don't see what's already there), [`wrong-level`](./wrong-level.md) (levels mix), and [`deliverable-fossils`](./deliverable-fossils.md) (each checklist item got its own `describe` block in the same file).

The semantic judgment: cluster the file's tests by behavior domain ([describe-before-edit](../principles.md#behavior-articulation-before-change) plus embedding clusters), and decide which clusters deserve their own file. This requires naming the behavior domains in a way that matches the *product*, not the *implementation* — the same capability that powers [`deliverable-fossils`](./deliverable-fossils.md).

## Signals

- Test file > 1000 lines or > 50 `it` / `test` blocks.
- File imports from > N unrelated modules (> 5 is a rough threshold).
- Multiple top-level `describe` blocks naming clearly different subjects.
- Mix of mocks plus real clients plus subprocess calls within one file.
- `//`, `#`, or block-comment section headers dividing the file (`// ===== SYNC =====`, `# --- FIXTURES ---`) — an author's tell.
- High duplication score within the file (jscpd, `flay`).

## False-positive guards

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

1. [Describe-before-edit](../principles.md#behavior-articulation-before-change) over every test in the file.
2. Cluster by behavior domain; propose a per-domain target file with a behavior-shaped name.
3. Emit a **split plan**: `original.test.ts` → `{ a.test.ts, b.test.ts, c.test.ts }`, with each destination's test list and the rationale for the grouping.
4. Execute the split via codemod; imports and shared helpers follow.
5. If shared setup warrants it, extract a small `test-support/` module rather than duplicating.
6. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power) plus same total test count plus CI green on each new file.

This move pairs with [`deliverable-fossils`](./deliverable-fossils.md): run the rename pass first so clusters form around product capabilities rather than checklist items.

## Example

### Before

```
tests/test_sync.py (1367 lines)
  ├── class TestSessionParsing (12 tests)
  ├── class TestMessageExtraction (18 tests)
  ├── class TestTrackingDB (9 tests)
  ├── class TestEmbedding (6 tests)
  └── class TestFullSyncEnd2End (4 tests)
```

### After

```
tests/
  test_session_parsing.py      (session-JSONL parsing only)
  test_message_extraction.py   (message extraction + token counting)
  test_tracking_db.py          (tracking DB schema + migrations)
  test_embedding.py            (embedding integration)
  test_sync_e2e.py             (full sync end-to-end)
  _support/fixtures.py         (extracted shared fixtures)
```

One file was mixing five behavior domains. Each is now a behavior-shaped file; shared fixtures moved into `_support/` rather than duplicated. The full-sync e2e is isolated so CI can run it in a separate slow tier.

## Related modes

- [`semantic-redundancy`](./semantic-redundancy.md) — monolithic files hide redundancy; run dedup *after* the split so clusters are per-domain.
- [`wrong-level`](./wrong-level.md) — the e2e extraction in the example is a wrong-level move; often they compose.
- [`deliverable-fossils`](./deliverable-fossils.md) — run the rename first so splitting uses product vocabulary.

## Polyglot notes

The split is universal; the codemod is ecosystem-specific (LibCST, jscodeshift, OpenRewrite, ast-grep). Preserving imports is the only real complication, and every codemod ecosystem has affordances for it.
