# Test-smell taxonomy

A curated, polyglot catalog of test-suite failure modes that are **seeable, fixable, and language-independent** — the subset of test-suite problems where an LLM's semantic judgment beats a linter's syntactic one.

The taxonomy is foundational. It names smells, describes how to see them, and prescribes how to fix them. It does *not* describe any particular tool.

## Companion documents

Two sibling documents carry the shared context. Every taxonomy entry cross-links to them rather than re-explaining:

- [`../principles.md`](../principles.md) — the test-design principles each smell violates (Farley's 8, Greg Wright's three additions, plus the refactoring principles that constrain how fixes may be applied). Anchored per principle.
- [`../glossary.md`](../glossary.md) — general-purpose term definitions (mutation testing, mutation kill-set, tautology theatre, canonical location, etc.) with citations. Anchored per term.

See also [`../workflows.md`](../workflows.md) for the RED-GREEN-MUTATE-KILL-REFACTOR cycle that underlies "refactor is only safe with known detection power".

## How to read an entry

Every taxonomy file follows the same shape:

- **Header table** — slug, severity, detection scope (`per-test`, `per-file`, or `cross-suite` — which agent type handles detection), and the [principles](../principles.md) the smell violates.
- **Summary** — one-line TL;DR.
- **Description** — what the smell is, why it matters, and what semantic judgment is required (i.e. what a linter cannot do).
- **Signals** — concrete detection heuristics, static and semantic.
- **False-positive guards** — common over-triggers and why they aren't the smell. Calibrates both human readers and agent consumers against pattern-matching false positives.
- **Prescribed Fix** — the mechanical move and the preservation gate the transform must clear.
- **Example** — a "before / after" mock in some representative language.
- **Related** — how this mode differs from adjacent ones.
- **Polyglot notes** — what changes across ecosystems. Every entry is expected to be polyglot; this section documents the per-language surface the detector and codemod need to handle.

## The catalog

Ordered roughly by how much semantic reasoning the required judgment demands. Higher-numbered entries lean on mechanical signals; lower-numbered entries need reasoning a linter cannot do.

| # | Slug | Core move | Severity | Detection Scope |
|---|---|---|---|---|
| 1 | [`deliverable-fossils`](./deliverable-fossils.md) | rename + regroup per product behavior | High | per-test, cross-suite |
| 2 | [`semantic-redundancy`](./semantic-redundancy.md) | cluster, pick canonical, fold/delete the rest | High | cross-suite |
| 3 | [`wrong-level`](./wrong-level.md) | relocate to correct pyramid tier | Medium | cross-suite |
| 4 | [`naming-lies`](./naming-lies.md) | rename test or strengthen body to match the claim | Medium | per-test |
| 5 | [`vacuous-assertion`](./vacuous-assertion.md) | strengthen the oracle | High | per-test |
| 6 | [`pseudo-tested`](./pseudo-tested.md) | add assertion that kills the no-op mutant | High | per-test |
| 7 | [`tautology-theatre`](./tautology-theatre.md) | delete or rewrite to exercise real SUT | Critical | per-test |
| 8 | [`over-specified-mock`](./over-specified-mock.md) | relax to behavior-relevant interaction only | High | per-test |
| 9 | [`implementation-coupled`](./implementation-coupled.md) | drive through public API instead | High | per-test |
| 10 | [`presentation-coupled`](./presentation-coupled.md) | parse then assert semantics, not formatting | Medium | per-test |
| 11 | [`conditional-logic`](./conditional-logic.md) | split or pin the precondition | Medium | per-test |
| 12 | [`shared-state`](./shared-state.md) | move setup to per-test factory / restore globals | Medium | per-file |
| 13 | [`mystery-guest`](./mystery-guest.md) | inline a 1–3 line summary of relevant fixture shape | Low | per-test |
| 14 | [`rotten-green`](./rotten-green.md) | delete the empty/dead scaffold or add the missing assertion | Low | per-test |
| 15 | [`monolithic-test-file`](./monolithic-test-file.md) | split file by behavior domain | Medium | per-file |

**Severity** is a relative-harm/safety hint: how bad the smell is for the suite, weighted by how safe the canonical fix is. Critical smells can usually be deleted outright because they were killing no mutants. Lower severities need transforms and correspondingly more reviewer attention. No severity is a mandate to act; it is input to prioritization.

## Non-goals (what the catalog is not for)

These are covered by existing tooling. Where a linter, mutation tool, or codemod runner already does the work deterministically, this taxonomy defers.

- Syntactic smell counts (TsDetect-style scoreboards). The EMSE 2023 follow-up study[^testsmells20] found classical smell counts uncorrelated with maintenance pain, and that machine-generated tests actually score *better* on smell detectors while being semantically worse. Optimizing for smell counts is an explicit anti-goal.
- Net-new test generation (handled by tools like CoverUp[^coverup]).
- Framework migrations (handled by jest-codemods, OpenRewrite, unittest2pytest, and similar).
- Flaky *detection* (handled by DeFlaker, `pytest-rerunfailures`, test-retry plugins). This catalog names flakiness root causes when they surface as [`shared-state`](./shared-state.md) or [`conditional-logic`](./conditional-logic.md); detection itself is out of scope.

## Governor rules

Every prescribed fix in the catalog is bounded by the [governor rules in principles](../principles.md#governor-rules): knowledge-DRY not syntactic-DRY, no extract-for-testability, no speculative code, commit-before-refactor. And by the broader principle that a refactor must [preserve regression-detection power](../principles.md#preservation-of-regression-detection-power).

[^testsmells20]: Panichella, A. et al. (2023). *Test Smells 20 Years Later: a Large-Scale Study*. Empirical Software Engineering, 28(4). <https://link.springer.com/article/10.1007/s10664-022-10207-5>. Concludes that classical smell catalogs correlate poorly with real maintenance pain, and warns specifically against optimizing smell counts as a KPI.

[^coverup]: Pizzorno, J. & Berger, E. (2025). *CoverUp: Effective High-Coverage Test Generation for Python*. PACM SE 2025. <https://arxiv.org/abs/2403.16218>. Reference implementation: <https://github.com/plasma-umass/coverup>.
