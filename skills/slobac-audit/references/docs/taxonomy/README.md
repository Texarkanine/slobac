# Test-smell taxonomy

A curated, polyglot catalog of test-suite failure modes that are **seeable, fixable, and language-independent** — the subset of test-suite problems where an LLM's semantic judgment beats a linter's syntactic one.

The taxonomy is foundational. It names smells, describes how to see them, and prescribes how to fix them. It does *not* describe any particular tool.

## The catalog

Ordered by **severity descending** (Critical → High → Medium → Low), then alphabetical by slug within each severity tier. The table is generated from each entry's canonical header by `scripts/gen_taxonomy_index.py`; a sibling copy lives at the top of `skills/slobac-audit/SKILL.md` where the audit orchestrator consumes it. Do not hand-edit the table — edit the canonical entry's header and run `uv run python scripts/gen_taxonomy_index.py` from the repo root.

<!-- BEGIN: taxonomy-index -->
| Slug | Severity | Detection Scope |
|---|---|---|
| [`tautology-theatre`](./tautology-theatre.md) | Critical | per-test |
| [`deliverable-fossils`](./deliverable-fossils.md) | High | per-test, cross-suite |
| [`implementation-coupled`](./implementation-coupled.md) | High | per-test |
| [`loose-text-oracle`](./loose-text-oracle.md) | High | per-test |
| [`over-specified-mock`](./over-specified-mock.md) | High | per-test |
| [`prose-pin`](./prose-pin.md) | High | per-test |
| [`pseudo-tested`](./pseudo-tested.md) | High | per-test |
| [`semantic-redundancy`](./semantic-redundancy.md) | High | cross-suite |
| [`vacuous-assertion`](./vacuous-assertion.md) | High | per-test |
| [`conditional-logic`](./conditional-logic.md) | Medium | per-test |
| [`monolithic-test-file`](./monolithic-test-file.md) | Medium | per-file |
| [`naming-lies`](./naming-lies.md) | Medium | per-test |
| [`presentation-coupled`](./presentation-coupled.md) | Medium | per-test |
| [`shared-state`](./shared-state.md) | Medium | per-file |
| [`wrong-level`](./wrong-level.md) | Medium | cross-suite |
| [`mystery-guest`](./mystery-guest.md) | Low | per-test |
| [`rotten-green`](./rotten-green.md) | Low | per-test |
<!-- END: taxonomy-index -->

**Severity** is a relative-harm/safety hint: how bad the smell is for the suite, weighted by how safe the canonical fix is. Critical smells can usually be deleted outright because they were killing no mutants. Lower severities need transforms and correspondingly more reviewer attention. No severity is a mandate to act; it is input to prioritization.

## Non-goals

These are covered by existing tooling. Where a linter, mutation tool, or codemod runner already does the work *deterministically*, this taxonomy defers.

- Syntactic smell counts ([TsDetect](https://github.com/TestSmells/TSDetect)-style scoreboards). The EMSE 2023 follow-up study[^testsmells20] found classical smell counts uncorrelated with maintenance pain, and that machine-generated tests actually score *better* on smell detectors while being semantically worse. Optimizing for smell counts is an explicit anti-goal.
- Net-new test generation (handled by tools like CoverUp[^coverup]).
- Framework migrations (handled by jest-codemods, OpenRewrite, unittest2pytest, and similar).
- Flaky *detection* (handled by DeFlaker, `pytest-rerunfailures`, test-retry plugins). This catalog names flakiness root causes when they surface as [`shared-state`](./shared-state.md) or [`conditional-logic`](./conditional-logic.md); detection itself is out of scope.

## Governor rules

Every prescribed fix in the catalog is bounded by the [governor rules in principles](../principles/refactor-qualities.md#governor-rules): knowledge-DRY not syntactic-DRY, no extract-for-testability, no speculative code, commit-before-refactor. And by the broader principle that a refactor must [preserve regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power).

[^testsmells20]: Panichella, A. et al. (2023). *Test Smells 20 Years Later: a Large-Scale Study*. Empirical Software Engineering, 28(4). <https://link.springer.com/article/10.1007/s10664-022-10207-5>. Concludes that classical smell catalogs correlate poorly with real maintenance pain, and warns specifically against optimizing smell counts as a KPI.

[^coverup]: Pizzorno, J. & Berger, E. (2025). *CoverUp: Effective High-Coverage Test Generation for Python*. PACM SE 2025. <https://arxiv.org/abs/2403.16218>. Reference implementation: <https://github.com/plasma-umass/coverup>.
