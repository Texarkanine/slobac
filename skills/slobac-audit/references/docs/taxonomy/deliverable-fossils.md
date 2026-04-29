# Deliverable Fossils

| Slug | Severity | Protects |
|---|---|---|
| `deliverable-fossils` | High | [Understandable](../principles.md#understandable), [Necessary](../principles.md#necessary), [Well-named](../principles.md#well-named) |

## Summary

Tests whose names, docstrings, or file organization reflect a long-gone development artifact — a sprint checklist, an acceptance-criteria list, a ticket title, or a refactor work-item — rather than the product's behavior. The suite reads like an archaeology of who-did-what-when, not a spec for what the code is supposed to do.

## Description

When a team ships from a design document with a checklist, tests tend to get authored one per checkbox: one `it` block per AC line, file layout shaped like the feature breakdown, names mentioning the refactor/story/ticket that motivated them. This is perfectly fine during the sprint. But six months later the design doc is gone and the tests are still carrying the scaffolding. New readers meet a suite organized by *who did what, when* instead of *what the product guarantees*.

The semantic judgment is threefold. **Intent extraction** — read a test, decide in one sentence what behavior it actually verifies (not what its name claims). **Canonical naming** — propose a new name that shouts the behavior (e.g. "when lid opens, printer stops" rather than "after lid-sensor refactor"). **Canonical grouping** — propose a file and describe-block organization keyed to product capabilities, not work items.

A linter cannot do any of the three. Embedding-based clustering can do some of the grouping in isolation, but without [describe-before-edit](../principles.md#behavior-articulation-before-change) input the clusters are shaped like the code, which is exactly the non-improvement this taxonomy is trying to escape.

## Signals

- Test titles containing: `refactor`, `after X migration`, `per RFC-`, `JIRA-\d+`, `GH-\d+`, `#\d+`, `as of`, `new behavior`, `old behavior`, `bug N`, ticket IDs, sprint/release labels (`M1`, `phase-2`).
- Docstrings or comments citing design-doc section numbers or AC identifiers (`per AC-3`, `satisfies requirement 4.2`).
- File names mirroring the delivery breakdown rather than the code: `feature-x-task-1.test.ts`, `spec_for_pr_512.rb`, `checklist_items_spec.py`.
- `describe` / `context` groupings keyed to work phases rather than product behaviors (`describe('Initial implementation')`, `describe('Post-refactor')`).
- Test names that are verbs in the imperative tense against the developer (`it('should add the new validation after we moved parsing')`) rather than claims against the product (`it('rejects trailing garbage')`).
- Clusters of two or more tests in the same file whose bodies verify the same behavior but whose names reference different checklist items. Often co-occurs with [`semantic-redundancy`](./semantic-redundancy.md).

## Prescribed Fix

A two-phase move. Phase A (rename) is safe and reversible. Phase B (regroup) is the full fix but risks merge conflicts and reviewer confusion if done all at once.

### Phase A — rename per behavior

1. [Describe-before-edit](../principles.md#behavior-articulation-before-change): for each flagged test, emit a one-sentence behavior statement.
2. Propose a new test name that encodes that statement. Style: active voice, a claim about the product, not about the work.
3. Strip fossil vocabulary (ticket IDs, refactor references, milestone markers) unless the *reason* the test exists is "guards a specific regression". If so, cite the bug as a code comment, not in the name.
4. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power). Rename-only must not change the call graph; only the test identifier or description string changes.

### Phase B — regroup per product capability

1. Cluster renamed tests by behavior-sentence embedding similarity.
2. For each cluster, propose a [canonical location](../glossary.md#canonical-location) — a file or `describe` block keyed to a product capability name (e.g. "selection keys", "URL encoding", "auth token refresh").
3. Emit a [suite table of contents](../glossary.md#suite-table-of-contents) diff: behavior → tests, before/after. Reviewers read this to decide whether the regrouping makes sense before any code moves.
4. Execute the moves as a codemod (ast-grep / LibCST / jscodeshift) so imports and fixture references follow.
5. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power) plus identical test count pre/post plus no new cross-file imports that weren't already implicit.

## Example

### Before

```typescript
describe('source tracking refactor', () => {
  it('should return the plugin via getPlugin after source tracking refactor', () => {
    const p = engine.getPlugin('cursor');
    expect(p).toBeDefined();
    expect(p!.id).toBe('cursor');
  });

  it('MS-4 checklist item 3: plugin exposes name', () => {
    const p = engine.getPlugin('cursor');
    expect(p!.name).toBe('Cursor');
  });
});
```

The grouping references a gone refactor. The first title tells you *when* the test was written, not what it proves. The second title points at a dead checklist. Both tests are really about the plugin lookup contract.

### After

```typescript
describe('plugin registry', () => {
  describe('getPlugin(id)', () => {
    it('returns a plugin whose id and name match the registration', () => {
      const p = engine.getPlugin('cursor');
      expect(p).toMatchObject({ id: 'cursor', name: 'Cursor' });
    });
  });
});
```

The rename and regroup express a durable product claim. Two fossil-named tests collapsed into one — this overlap with [`semantic-redundancy`](./semantic-redundancy.md) is common; the rename surfaces redundancy that was hiding under divergent names. A rationale commit for this transform might read:

> Renamed `should return the plugin via getPlugin after source tracking refactor` → `returns a plugin whose id and name match the registration` because the body verifies the registry contract, not the refactor. Folded `MS-4 checklist item 3` into the same assertion: same behavior, weaker oracle. Moved into `plugin registry › getPlugin(id)` group. Mutation kill-set preserved.

## Related modes

- [`naming-lies`](./naming-lies.md) — also renames, but the root cause is a title/body *mismatch* for a single test. Deliverable Fossils is the suite-wide, history-driven variant; naming-lies is the per-test variant.
- [`semantic-redundancy`](./semantic-redundancy.md) — fossil-named tests frequently duplicate each other after rename. Always run both detectors together; rename first, dedupe second.
- [`monolithic-test-file`](./monolithic-test-file.md) — fossil files are often also monolithic because every checklist item accreted into the same file.

## Polyglot notes

Fossil vocabulary is language-agnostic but team-specific. The detector needs a small configurable glossary: the team's ticket prefix (`SLOB-`), common refactor adjectives, release names. Ship sensible defaults.

The rename transform is the same everywhere (string replacement on the test identifier). The regroup transform uses the ecosystem's codemod: ast-grep for polyglot, LibCST for Python, jscodeshift/ts-morph for JS/TS, OpenRewrite for JVM.

RSpec adds an extra lever: `context` blocks can hold the fossil history as a doc comment while the `it` text stays behavior-focused. Use it.
