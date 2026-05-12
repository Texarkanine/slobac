---
name: slobac-audit
description: Audit a test suite for common test smells based on the SLOBAC manifesto.
license: "Multiple — see LICENSES/ and REUSE.toml"
enable-model-invocation: false
---

# Test Suite Audit Workflow

## Step 1 — determine the target suite root

The operator names a directory (explicitly or implicitly: "these tests", "my suite", a path in their message). If no target is identifiable, ask for one. Do not audit the whole repo by default; that is almost never what the operator wants and will produce an unreadably long report.

## Step 2 — parse scope

From the operator's request, resolve a list of **in-scope smell slugs** drawn from the supported set.

### Supported slugs and detection scopes

The table below is the orchestrator's authoritative slug → detection-scope index. It is generated from each canonical entry's header table by `scripts/gen_taxonomy_index.py`; a sibling copy lives in [`references/docs/taxonomy/README.md`](./references/docs/taxonomy/README.md) for human navigation. Do not hand-edit the table — edit the canonical entry's header and run the generator.

<!-- BEGIN: taxonomy-index -->
| Slug | Severity | Detection Scope |
|---|---|---|
| [`tautology-theatre`](references/docs/taxonomy/tautology-theatre.md) | Critical | per-test |
| [`deliverable-fossils`](references/docs/taxonomy/deliverable-fossils.md) | High | per-test, cross-suite |
| [`implementation-coupled`](references/docs/taxonomy/implementation-coupled.md) | High | per-test |
| [`over-specified-mock`](references/docs/taxonomy/over-specified-mock.md) | High | per-test |
| [`pseudo-tested`](references/docs/taxonomy/pseudo-tested.md) | High | per-test |
| [`semantic-redundancy`](references/docs/taxonomy/semantic-redundancy.md) | High | cross-suite |
| [`vacuous-assertion`](references/docs/taxonomy/vacuous-assertion.md) | High | per-test |
| [`conditional-logic`](references/docs/taxonomy/conditional-logic.md) | Medium | per-test |
| [`monolithic-test-file`](references/docs/taxonomy/monolithic-test-file.md) | Medium | per-file |
| [`naming-lies`](references/docs/taxonomy/naming-lies.md) | Medium | per-test |
| [`presentation-coupled`](references/docs/taxonomy/presentation-coupled.md) | Medium | per-test |
| [`shared-state`](references/docs/taxonomy/shared-state.md) | Medium | per-file |
| [`wrong-level`](references/docs/taxonomy/wrong-level.md) | Medium | cross-suite |
| [`mystery-guest`](references/docs/taxonomy/mystery-guest.md) | Low | per-test |
| [`rotten-green`](references/docs/taxonomy/rotten-green.md) | Low | per-test |
<!-- END: taxonomy-index -->

**Slug-only invocation contract.** The supported-slug set is exactly the `Slug` column of the table above. Operators must invoke this skill with **explicit slug names** (e.g. `tautology-theatre`, `vacuous-assertion`). Free-text or fuzzy-phrase requests (e.g. "audit my tests for tautology", "find tests that mock the SUT") are **refused**: respond with the supported-slug list and ask the operator to re-invoke with explicit slugs. Do not silently resolve a phrase to a slug. The same refusal applies if the operator names a slug not in the table.

The single exception is the bulk-select wildcard: if the operator's invocation is `all`, `everything`, or unscoped (no slug names at all), resolve to the full supported-slug set. This is the only non-slug input the orchestrator accepts.

**Classify in-scope slugs by detection scope.** Use the `Detection Scope` column of the embedded table above — do **not** read each `<slug>.md`'s header at runtime; the table has already lifted that information. Partition the in-scope slugs into:

- **per-test / per-file set** — slugs whose detection scope contains `per-test` or `per-file`. These go to batch assessors.
- **cross-suite set** — slugs whose detection scope contains `cross-suite`. These go to the cross-suite assessor.

A slug whose detection scope lists multiple values (e.g. `deliverable-fossils` = `per-test, cross-suite`) goes to **both** sets: its per-test detection (Phase A: rename) is handled by batch assessors; its cross-suite detection (Phase B: regroup) is handled by the cross-suite assessor.

## Step 3 — launch scout

Resolve the absolute filesystem path to this skill's `references/` directory (the directory containing `report-template.md`, `behavior-summary-format.md`, `suite-manifest-format.md`, `subagents/`, and `docs/`). This path is passed to all subagents so they can resolve reference files at runtime.

🚨 **The orchestrator MUST NOT enumerate, count, or measure the suite itself.** If you find yourself running `find`, `wc`, `ls`, `Glob`, or any equivalent against the target suite root in this step, **stop and launch the scout instead.** The scout's role is the orchestrator's *evidence base* for partitioning, output budgeting, and report provenance — short-circuiting it produces silently wrong file/char/test counts and downstream miscalibration. (Two of three post-release runs miscounted the suite by either 4 files or ~30k chars when they bypassed the scout; the run that launched it got the counts right.)

Read `references/subagents/scout.md`. Launch a readonly subagent whose task is the content of that file, supplemented with:

- The target directory from Step 1.
- The absolute `references/` path resolved above.
- The content of `references/suite-manifest-format.md` (the output format spec).

The scout will enumerate test files, measure their sizes, detect ecosystem and tier conventions, and return a **Suite Manifest**. The orchestrator copies the scout's headline counts (file count, total chars, total tests) into the report's `Suite manifest` summary line in Step 10 — this is how a reviewer audits whether scout actually ran.

## Step 4 — establish audit workdir

Create a working directory for this audit run's intermediate artifacts (batch result files). The workdir persists on both success and failure so the operator can inspect per-batch artifacts post-hoc.

### Default path

`.slobac/<run-id>/` in the operator's current working directory, where `<run-id>` is an ISO-8601 timestamp at seconds precision (e.g., `2026-05-12T18-30-45`). The `.slobac/` parent directory is created if it does not exist.

### Override

If the operator provided a `--workdir` path in their invocation, use that path instead of the default. Create the directory if it does not exist.

### Precondition

Verify the workdir is writable by creating a small test file and deleting it. If the write fails, **halt with a structured error** — do not fall back to inline IR. The error must name the path and the failure reason so the operator can fix permissions.

## Step 5 — partition and configure batches

Using the Suite Manifest from Step 3:

### 5a. Context budget determination

Determine the content budget per batch:

- If the operator provided a context window size in their invocation (e.g., "1M context window", "using Gemini 2M"), use that as the total context budget.
- If not provided and the suite fits under the conservative floor (200K-token context ≈ 400K chars of source at 60% content allocation), proceed silently at the floor.
- If not provided and the suite exceeds the floor, ask once: "This suite is large enough to require multi-agent sharding. What context window size should I plan against? We recommend the largest available (1M+ tokens) for best results."

Content budget per batch = total context budget × 0.60 (reserve 40% for smell definitions, instructions, and reasoning).

### 5b. Output budget per batch

The 60% content budget governs **input** (file source + smell definitions + instructions). Subagent **output** has its own ceiling — most models cap a single response well below their input window, and the batch assessor's output is dominated by the behavior-summary table whose size scales with test count × richness.

Bound the maximum tests per batch by these per-richness caps so the assessor's output never gets truncated:

| Richness | Approx chars per row | Max tests per batch |
|----------|---------------------|---------------------|
| `full`     | ~400–600 | **~120** |
| `standard` | ~200–350 | **~250** |
| `compact`  | ~80–120  | **~600** |

These caps reserve headroom for the findings section above the table; tune downward if a target model has a notably small output cap.

This guard prevents the truncated-batch failure mode observed in post-release auto-model runs (`full` richness × 379 tests ≈ 190k chars of output in one subagent message → silent table truncation → empty cross-suite findings on suites that obviously contain redundancies).

### 5c. Partition files

If total chars from the Suite Manifest fits in one input content budget **and** total test count fits under the output cap from Step 5b: **1 batch, all files.** This is the small-suite degenerate case — functionally identical to a single-agent audit, but executed via the batch assessor skill for consistency.

If either budget is exceeded: partition files into N batches using greedy bin-packing by character count, with the binding constraint being whichever budget — input chars or output tests — yields **more** batches. Keep files from the same directory together when possible (directory cohesion aids per-file smells like `shared-state`).

### 5d. Compute summary richness

Determine the behavior summary richness level based on total test count vs. the cross-suite assessor's context budget:

| Suite Scale | Approx Tests | Richness Level |
|-------------|-------------|----------------|
| Small-medium | < ~500 | `full` |
| Medium-large | ~500–1500 | `standard` |
| Large-huge | 1500+ | `compact` |

These thresholds are approximate and shift based on average test length. The goal is to keep the merged behavior summary table within the **cross-suite assessor's** context budget — the cross-suite assessor reads and merges all batch files in its own window, so the total merged table size (`tests × richness_chars`) must fit within `0.6 × cross-suite window`. The richness tier downgrades (`full` → `standard` → `compact`) are the mechanism for keeping the merged IR within budget.

If no cross-suite smells are in scope, richness level is irrelevant (summaries won't be consumed by a cross-suite assessor), but batch assessors still produce them for completeness.

## Step 6 — launch batch assessors

Read `references/subagents/batch.md`. For each batch (1 for small suites, N for large suites), launch a subagent whose task is the content of that file, supplemented with:

- The file list for this batch.
- The per-test / per-file smell slugs from Step 2.
- The summary richness level from Step 5d.
- The tier conventions from the Suite Manifest.
- The absolute `references/` path (resolved in Step 3).
- The content of `references/behavior-summary-format.md` (the summary output format spec).
- The workdir path from Step 4.
- The batch ID (e.g., `batch-1`, `batch-2`, …).

Batch assessors must have **write access** to the workdir. They are read-only with respect to the audited codebase, but writing audit artifacts to the workdir is a required capability — not a violation of the read-only constraint. If the runtime environment cannot grant write access (e.g., a strict readonly sandbox with no filesystem exceptions), **halt and tell the operator why** — do not silently fall back to inline output.

For multiple batches, launch them **in parallel** (each as a separate subagent).

### Failure handling

- If a batch assessor returns garbage (unparseable, missing required sections): retry once with the same inputs. If it fails again, skip the batch and note in the report which files were not assessed.
- If a batch assessor times out: skip and note. Do not block the entire audit on one batch.

## Step 7 — collect batch metadata

Collect the metadata returned by each batch assessor: `{path, row_count, finding_count}`. The orchestrator does **not** read the batch result files — the full findings and behavior summaries live on disk, not in the orchestrator's context. The orchestrator works only with pointers and counts.

Build a batch manifest:

| Batch ID | File Path | Row Count | Finding Count |
|----------|-----------|-----------|---------------|
| batch-1  | `<workdir>/batch-1.md` | N | M |
| batch-2  | `<workdir>/batch-2.md` | N | M |
| …        | …         | …         | …             |

## Step 8 — verify behavior-summary integrity

Before any cross-suite work, validate that the batch results on disk actually represent the suite. Compare:

- `total_rows` — sum of `row_count` from all batch metadata entries collected in Step 7.
- `expected_tests` — total `Test count` from the scout's Suite Manifest (Step 3).

Apply this gate:

- `total_rows ≥ expected_tests × 0.95` → proceed to Step 9.
- `0 < total_rows < expected_tests × 0.95` → identify the batch whose missing rows account for the gap and retry **that batch** (idempotent — same file list, same parameters, same workdir path and batch ID so it overwrites the prior file). On a second under-budget result, **halt with a structured error** that names the batch and the gap; do not proceed to cross-suite. Note the gap in the eventual report under "Out-of-scope requests" with an explicit "audit incomplete" line.
- `total_rows == 0` → halt with the same structured error.

This guard prevents the silent-failure mode observed in post-release auto-model runs: a truncated batch produced an incomplete IR; cross-suite ran against the partial data and emitted "no findings" for `semantic-redundancy` on a suite that obviously contains redundancies. **Never feed a partial IR to cross-suite.**

## Step 9 — launch cross-suite assessor (if needed)

If the cross-suite smell set from Step 2 is **non-empty** and the integrity gate from Step 8 passed:

Read `references/subagents/cross-suite.md`. Launch a readonly subagent whose task is the content of that file, supplemented with:

- The list of batch result file paths from the batch manifest (Step 7).
- The cross-suite smell slugs.
- The tier conventions from the Suite Manifest.
- The suite root path.
- The absolute `references/` path (resolved in Step 3).
- The content of `references/behavior-summary-format.md` (so the cross-suite assessor knows the table shape for parsing and merge).

If the cross-suite smell set is **empty**: skip this step entirely. The batch findings are the complete result.

## Step 10 — synthesize report

Merge all findings:
- Batch assessor findings (per-test + per-file smells) — read the Findings sections from each batch result file in the workdir. This is a targeted read of a known section; the full behavior-summary tables in those files are not loaded into the orchestrator's context.
- Cross-suite assessor findings (if Step 9 ran) — returned inline by the cross-suite assessor.

Deduplicate: if the same test appears in both batch and cross-suite findings for the same smell slug, keep the more detailed finding (cross-suite findings typically have richer rationale for cross-suite smells).

Write the report using the shape in [`references/report-template.md`](./references/report-template.md).

- Default path: `./slobac-audit.md` in the operator's current working directory.
- If the operator named a different path, use that.
- If a file already exists at the chosen path, emit at `slobac-audit-2.md`, `slobac-audit-3.md`, … — do not clobber a prior report.
- Populate the `Suite manifest` line in the report header with the scout's headline counts (file count, total chars, total tests). This is the orchestrator's contract for letting a reviewer audit whether scout actually ran.
- Populate the `Workdir` line in the report header with the workdir path from Step 4. This enables tracing findings back to per-batch artifacts.
- Include a "Tests considered but not flagged" section from batch assessor results.
- Include an explicit "No findings for scope `<slug>`" line when a requested in-scope smell produces zero findings.
- In the Summary paragraph, note the orchestration shape per the contract in `references/report-template.md`: how many batch assessors ran, which budget (input chars vs output tests) was binding, whether the Step 8 integrity gate passed cleanly (or required a retry, or halted), and — if the cross-suite assessor ran — the richness tier it declared in its `Consumed richness` line.

## Step 11 — close

Tell the operator where the report was written and which scopes were covered. Do not summarize the findings in chat — the report is the deliverable. If unsupported slugs were requested, remind the operator which were skipped and why.

## Constraints and guards

- **Read-only.** This skill does not modify test code. If the operator asks the skill to apply fixes, that is a future capability that does not exist yet — decline and direct them to treat the report as input to a separate step.
- **Canonical entries are the single source of truth.** The canonical smell definitions in this skill bundle are the manifesto. If a detection feels right but the canonical entry's Signals don't cover it, that is a signal the canonical entry needs extending — stop and surface it as a manifesto gap, do not carry detection content outside the canonical entry.
- **Preserve regression-detection power.** Every prescribed remediation in a finding is bounded by the [preservation-of-regression-detection-power](references/docs/principles/refactor-qualities.md#preservation-of-regression-detection-power) governor rule.
- **Fossil vocabulary is a signal, not a verdict.** The word "refactor" in a title does not make a fossil; a ticket ID in a docstring does not make a fossil. The judgment is whether the vocabulary describes the test's reason-for-existence vs. the behavior it verifies.
- **Naming-lie detection is semantic.** Title/body tokenization is a first pass, not a verdict.
- **Cross-suite findings require targeted source reads.** The cross-suite assessor must read source before confirming a finding — behavior summary clustering alone is insufficient evidence.
- **Batch assessor is the universal audit engine.** There is no separate single-agent code path. Small suites get 1 batch assessor with all files; large suites get N batch assessors with partitions. The degenerate case of 1 batch is the "single-agent" experience.
- **Context budget is conservative by default.** The 200K-token floor with 60% content allocation ensures the audit works on any model. Operators can unlock better results (fewer batches, richer summaries) by specifying a larger context window.
- **Failure is isolated.** A failed batch assessor does not invalidate the entire audit. Note the gap and continue.
- **The orchestrator MUST NOT author behavior-summary rows.** Behavior summaries are produced exclusively by batch assessors and written to disk. The orchestrator collects metadata pointers — it never reads, merges, or reconstructs the summary tables. If a batch result file is missing or unparseable, the orchestrator re-launches that batch; it never reconstructs results from memory or source.
- **No inline-IR fallback path.** All batch results flow through disk files. There is no code path where findings or behavior summaries are passed inline from batch assessors to the orchestrator or from the orchestrator to the cross-suite assessor. If disk writes fail, the audit halts — it does not degrade to inline transfer.
