---
task_id: prose-pin-weak-text-oracle-smells
date: 2026-07-11
complexity_level: 3
---

# Reflection: prose-pin and weak-text-oracle taxonomy smells

## Summary

Delivered two High/per-test taxonomy smells — `prose-pin` (committed docs/skills as oracle) and `loose-text-oracle` (underdetermined runtime text oracles) — with fixtures, Related-mode boundary edits, and index/docs drift fixes. Build and QA both passed with no plan deviations; one residual count-literal in techContext was caught in QA.

## Requirements vs Outcome

All project-brief acceptance criteria landed: full CONTRIBUTING-shaped entries, stockroom-shaped signals and FP guards (fitness-function + prose-as-SUT; typed+supplementary + text-is-product), runtime weak-substring coverage, regenerated index, adjacent-smell Related modes (including hedged `conditional-logic` After), and fixtures with expected-findings. Nothing descoped; nothing added beyond the preflight amendments (TDD reorder, count-agnostic docs, on-disk fixture prose).

## Plan Accuracy

The amended 11-step plan was accurate end-to-end. Preflight's TDD reorder (expected-findings → plant → taxonomy) was the right encoding for this repo's fixture convention. Challenges that materialized were the ones predicted (PC vs LTO confusion, fitness-function framing) and were handled in fixture comments + taxonomy FP guards — no surprises from elsewhere. The only residual was a third "15" literal in `techContext.md` that preflight had scoped only to systemPatterns + docs README.

## Creative Phase Review

Option B (two smells) held up cleanly in authoring: discriminability and fix hierarchies diverged exactly as designed, and planting ambiguous tokens (`"timeout"`, `"success"`) vs PC's long cosmetic chains made the boundary tangible in fixtures. Naming (`prose-pin` + `loose-text-oracle`) needed no mid-build renegotiation. Fitness-function-as-FP (not a third smell) was the right call — the negative control writes naturally as ArchUnit-style rationale.

## Build & QA Observations

Build was mechanical once creative locked the carve: fixtures and entries wrote in one pass with no iteration. QA was clean on substance; the only finding was documentation count drift in techContext — same class of bug preflight already flagged elsewhere. Manual fixture-vs-expected hand-diff (47 checks) plus properdocs/index/pytest covered the mechanical gates; live `/slobac-audit` against the new fixtures remains operator/QA-manual per project convention (not a build failure mode).

## Cross-Phase Analysis

Creative → Build: the two-axis diagram (oracle strength × artifact kind) translated directly into Signals/FP/Related prose with almost no reinterpretation. Preflight → Build: TDD reorder and on-disk markdown preference prevented the usual "taxonomy first, fixtures as afterthought" skew. Preflight → QA: incomplete enumeration of count-literals left a techContext residue — preflight's amendment class was right, its file list was slightly short. No creative decision created a QA finding.

## Insights

### Technical
- Hardcoded taxonomy cardinality ("all 15 entries") is a latent drift class across persistent docs (`systemPatterns`, `techContext`, manifesto README). When adding smells, grep for count literals project-wide — not only the files named in the plan amendment.

### Process
- For taxonomy-extension tasks, fixture-first TDD (`expected-findings` as failing spec) keeps Signals/Fix honest to planted evidence; creative's Option B sketch was sufficient design detail that build did not need mid-flight redesign.
