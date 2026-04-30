# Semantic Redundancy

| Slug | Severity | Protects |
|---|---|---|
| `semantic-redundancy` | High | [Necessary](../principles.md#necessary), [Maintainable](../principles.md#maintainable), [Fast](../principles.md#fast) |

## Summary

Two or more tests exercise the same observable behavior with different names, fixtures, or mock styles. One is the [canonical location](../glossary.md#canonical-location); the others should fold into it or be deleted with a named absorber.

## Description

*"You test the same thing (correctly though!) five times, and it belongs in this one specific place of those five."* Tokens differ; the claim is the same. The semantic judgment decomposes into three questions.

**Equivalence** — do these tests verify the same observable behavior? Not the same tokens; different mocks can hide same-behavior tests. **Authority** — which copy is canonical? Pick by: most precise name, smallest fixture surface, strongest assertion, most natural layer. **Justification** — emit a prose reason for every fold or delete so reviewers can trust the move.

Token-level deduplication (jscpd[^jscpd], PMD CPD[^cpd]) catches copy-paste. Embedding-based clustering[^ltm] catches near-duplicates. Neither can decide *which* is canonical, or justify the choice.

This entry respects the [knowledge-DRY governor rule](../principles.md#knowledge-dry-not-syntactic-dry): two tests that *look* similar but guard different knowledge — e.g. a test that intentionally duplicates `STORAGE_KEYS` in-test as a contract check against the production definition — must not be merged.

## Signals

- Adjacent `it`/`test`/`def test_` blocks that call the same SUT entry point with identical arguments, with assertion sets that are subsets of each other.
- Cross-file behavior-sentence clusters with cosine similarity ≥ 0.85 over [describe-before-edit](../principles.md#behavior-articulation-before-change) sentences.
- Two tests cover inverse or parallel operations where one has a strictly weaker oracle.
- Mirrored suites across near-isomorphic components (`plugin-cursor.test.ts` vs `plugin-claude.test.ts`) with identical scenario matrices and only plugin-specific fixtures differing.
- Repeated mock data or shared fixture literals across N tests in the same describe block.

## False-positive guards

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

1. [Describe-before-edit](../principles.md#behavior-articulation-before-change): emit a one-sentence behavior docstring for every test in scope.
2. Cluster sentences by embedding similarity (τ configurable; default 0.85).
3. For each cluster, emit a decision record:
   ```
   keep: path:line — reason
   fold-into-keep: path:line — reason (absorb unique asserts into keep)
   delete: path:line — reason (strict subset)
   ```
4. Mechanical transform: delete the losers, or fold their unique assertions into the canonical; rename the survivor to express the deduped intent.
5. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power). The [mutation kill-set](../glossary.md#mutation-kill-set) must not shrink; lost kills are a veto.
6. Commit per cluster with the decision record in the message body.

For mirrored-component families (plugin A vs plugin B), prefer a parameterized or shared-example transform: extract the scenario matrix once, vary per plugin. Do this only when the mirror is intentional; otherwise the two suites are different products and should stay separate.

## Example

### Before

```typescript
it('parses a valid IR file', async () => {
  const result = await parseIRFile(ws, 'fixtures/typescript.md', opts);
  expect(result.plugins).toHaveLength(2);
  expect(result.plugins[0].id).toBe('cursor');
});

it('returns plugins from IR file', async () => {
  const result = await parseIRFile(ws, 'fixtures/typescript.md', opts);
  expect(result.plugins.length).toBeGreaterThan(0);
});
```

### After

```typescript
it('parses typescript fixture into the expected plugin list', async () => {
  const result = await parseIRFile(ws, 'fixtures/typescript.md', opts);
  expect(result.plugins).toEqual([
    expect.objectContaining({ id: 'cursor' }),
    expect.objectContaining({ id: 'claude' }),
  ]);
});
```

The second test was a strict subset of the first; its name referred to the return shape rather than the behavior. Folded into the first; strengthened the oracle to a structural match rather than a length check. [Mutation kill-set](../glossary.md#mutation-kill-set) unchanged.

## Related modes

- [`deliverable-fossils`](./deliverable-fossils.md) — fossil-named clusters almost always contain redundancy. Run rename first, then this.
- [`vacuous-assertion`](./vacuous-assertion.md) — a cluster's weakest test usually has a vacuous oracle. The dedup step gets to drop it.
- [`monolithic-test-file`](./monolithic-test-file.md) — giant files amplify redundancy because authors don't see what's already there.

## Polyglot notes

Embeddings are language-agnostic; the [describe-before-edit](../principles.md#behavior-articulation-before-change) technique works identically in any runner. The codemod layer is per-language (LibCST, jscodeshift, OpenRewrite, ast-grep) but the decision record is the same shape everywhere.

[^jscpd]: Kucherenko, A. *jscpd* — polyglot copy-paste detector for 150+ formats, ships an `ai` reporter. MIT. <https://github.com/kucherenko/jscpd>.

[^cpd]: PMD Copy-Paste Detector — 30+ languages including JS/TS/Go/Kotlin/Python. <https://pmd.github.io/pmd/pmd_userdocs_cpd.html>.

[^ltm]: Pan, R. et al. (2023). *LTM: Scalable and Black-box Similarity-based Test Suite Minimization based on Language Models*. arXiv:2304.01397. <https://arxiv.org/abs/2304.01397>. CodeBERT embeddings plus a genetic algorithm; 5× faster than the prior ATM method while preserving coverage.
