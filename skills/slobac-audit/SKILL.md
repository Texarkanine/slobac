---
name: slobac-audit
description: Audit a test suite for SLOBAC manifesto smells and emit a portable markdown report. Supports 6 smells across 3 detection scopes (per-test, per-file, cross-suite). Orchestrates scout, batch, and cross-suite subagents for suites of any size. Use when a human asks for a smell audit of test code, a review of test names/assertions against the behavior they claim to protect, or a SLOBAC report.
---

# Test Suite Audit Workflow

## Step 1 — determine the target suite root

The operator names a directory (explicitly or implicitly: "these tests", "my suite", a path in their message). If no target is identifiable, ask for one. Do not audit the whole repo by default; that is almost never what the operator wants and will produce an unreadably long report.

## Step 2 — parse scope

From the operator's request, resolve a list of **in-scope smell slugs** drawn from the supported set:

**Supported smells (6):**

| Slug | Detection Scope |
|------|----------------|
| `deliverable-fossils` | per-test, cross-suite |
| `naming-lies` | per-test |
| `shared-state` | per-file |
| `monolithic-test-file` | per-file |
| `semantic-redundancy` | cross-suite |
| `wrong-level` | cross-suite |

Natural phrases map to slugs by meaning, not string match. Map operator intent to slugs:

- `deliverable-fossils` — "fossils", "deliverable fossils", "fossil tests", "stale names", "dead names", "sprint-shaped tests", "checklist tests", "checklist-shaped", "one test per AC", "tests named after tickets", "ticket-id vocabulary", "names that describe who wrote them, not what they prove", "sprint-vocab tests"
- `naming-lies` — "naming-lies", "naming lies", "lying names", "lying titles", "titles that lie", "docstrings that lie", "names that don't match the body", "title/body mismatch", "tests whose names overpromise"
- `shared-state` — "shared state", "order dependence", "order-dependent", "leaked state", "module-level mutables", "test isolation", "state leaking between tests"
- `monolithic-test-file` — "monolithic", "god test file", "test file too large", "mixed domains in one file", "test file needs splitting"
- `semantic-redundancy` — "redundant tests", "duplicate tests", "same behavior tested twice", "redundancy", "overlapping tests"
- `wrong-level` — "wrong level", "wrong tier", "wrong pyramid level", "unit test doing integration", "integration test that's really unit"
- "audit everything", "all smells", unscoped — resolve to the full supported set.

If the operator names a smell not in the supported set (e.g., `tautology-theatre`, `vacuous-assertion`, any other taxonomy slug), **refuse that slug**. Acknowledge it by name, state it is not yet supported, list the supported slugs, and proceed with only the supported slugs from the operator's request. Do not audit the out-of-scope slug anyway; do not silently drop it.

**Classify in-scope slugs by detection scope.** For each in-scope slug, read its `Detection Scope` from `references/docs/taxonomy/<slug>.md` (the header table). Partition into:

- **per-test / per-file set** — slugs with detection scope `per-test` or `per-file`. These go to batch assessors.
- **cross-suite set** — slugs with detection scope `cross-suite`. These go to the cross-suite assessor.

Note: `deliverable-fossils` has both `per-test` and `cross-suite` scopes. Its per-test detection (Phase A: rename) goes to batch assessors; its cross-suite detection (Phase B: regroup) goes to the cross-suite assessor.

## Step 3 — launch scout

Launch a readonly subagent with the `slobac-scout` skill. Provide:

- The target directory from Step 1.
- Instruct it to read `../slobac-audit/references/suite-manifest-format.md` for the output format.

The scout will enumerate test files, measure their sizes, detect ecosystem and tier conventions, and return a **Suite Manifest**.

**Harness-specific dispatch:**
- **Cursor:** Use the `Task` tool with `subagent_type: "generalPurpose"`, `readonly: true`. Pass the scout skill's SKILL.md content or instruct the subagent to read it.
- **Claude Code:** Use `dispatch_agent` with the scout prompt.
- **Other harnesses:** Use whatever subagent-launch primitive is available. The scout needs only filesystem read access.

## Step 4 — partition and configure batches

Using the Suite Manifest from Step 3:

### 4a. Context budget determination

Determine the content budget per batch:

- If the operator provided a context window size in their invocation (e.g., "1M context window", "using Gemini 2M"), use that as the total context budget.
- If not provided and the suite fits under the conservative floor (200K-token context ≈ 400K chars of source at 60% content allocation), proceed silently at the floor.
- If not provided and the suite exceeds the floor, ask once: "This suite is large enough to require multi-agent sharding. What context window size should I plan against? We recommend the largest available (1M+ tokens) for best results."

Content budget per batch = total context budget × 0.60 (reserve 40% for smell definitions, instructions, and reasoning).

### 4b. Partition files

If total chars from the Suite Manifest fits in one content budget: **1 batch, all files.** This is the small-suite degenerate case — functionally identical to a single-agent audit, but executed via the batch assessor skill for consistency.

If total chars exceeds one content budget: partition files into N batches using greedy bin-packing by character count. Keep files from the same directory together when possible (directory cohesion aids per-file smells like `shared-state`).

### 4c. Compute summary richness

Determine the behavior summary richness level based on total test count vs. the cross-suite assessor's context budget:

| Suite Scale | Approx Tests | Richness Level |
|-------------|-------------|----------------|
| Small-medium | < ~500 | `full` |
| Medium-large | ~500–1500 | `standard` |
| Large-huge | 1500+ | `compact` |

These thresholds are approximate and shift based on average test length. The goal is to keep the merged behavior summary table within the cross-suite assessor's context budget.

If no cross-suite smells are in scope, richness level is irrelevant (summaries won't be consumed by a cross-suite assessor), but batch assessors still produce them for completeness.

## Step 5 — launch batch assessors

For each batch (1 for small suites, N for large suites), launch a readonly subagent with the `slobac-batch` skill. Provide:

- The file list for this batch.
- The per-test / per-file smell slugs from Step 2.
- The summary richness level from Step 4c.
- The tier conventions from the Suite Manifest.
- Instruct it to read `../slobac-audit/references/behavior-summary-format.md` for the summary output format.
- Instruct it to read `../slobac-audit/references/docs/taxonomy/<slug>.md` for each in-scope smell.

For multiple batches, launch them **in parallel** (each as a separate subagent).

**Harness-specific dispatch:**
- **Cursor:** Use the `Task` tool with `subagent_type: "generalPurpose"`, `readonly: true`, `run_in_background: true` for parallel batches.
- **Claude Code:** Use `dispatch_agent` for each batch.

### Failure handling

- If a batch assessor returns garbage (unparseable, missing required sections): retry once with the same inputs. If it fails again, skip the batch and note in the report which files were not assessed.
- If a batch assessor times out: skip and note. Do not block the entire audit on one batch.

## Step 6 — collect and merge batch results

Collect findings and behavior summaries from all batch assessors.

- **Merge findings** — concatenate findings from all batches. There should be no duplicates (each file is assigned to exactly one batch).
- **Merge behavior summaries** — concatenate summary tables from all batches and re-sort by file path (lexicographic), then line number (ascending). If duplicate rows appear (same File + Line), keep the first and log a warning.

## Step 7 — launch cross-suite assessor (if needed)

If the cross-suite smell set from Step 2 is **non-empty**:

Launch a readonly subagent with the `slobac-cross-suite` skill. Provide:

- The merged behavior summary table from Step 6.
- The cross-suite smell slugs.
- The tier conventions from the Suite Manifest.
- The suite root path.
- Instruct it to read `../slobac-audit/references/docs/taxonomy/<slug>.md` for each in-scope cross-suite smell.

If the cross-suite smell set is **empty**: skip this step entirely. The batch findings are the complete result.

**Harness-specific dispatch:**
- **Cursor:** Use the `Task` tool with `subagent_type: "generalPurpose"`, `readonly: true`.
- **Claude Code:** Use `dispatch_agent`.

## Step 8 — synthesize report

Merge all findings:
- Batch assessor findings (per-test + per-file smells).
- Cross-suite assessor findings (if Step 7 ran).

Deduplicate: if the same test appears in both batch and cross-suite findings for the same smell slug, keep the more detailed finding (cross-suite findings typically have richer rationale for cross-suite smells).

Write the report using the shape in [`references/report-template.md`](./references/report-template.md).

- Default path: `./slobac-audit.md` in the operator's current working directory.
- If the operator named a different path, use that.
- If a file already exists at the chosen path, emit at `slobac-audit-2.md`, `slobac-audit-3.md`, … — do not clobber a prior report.
- Include a "Tests considered but not flagged" section from batch assessor results.
- Include an explicit "No findings for scope `<slug>`" line when a requested in-scope smell produces zero findings.
- In the Summary section, note the orchestration metadata: how many batch assessors were launched, whether cross-suite analysis ran, and the summary richness level used.

## Step 9 — close

Tell the operator where the report was written and which scopes were covered. Do not summarize the findings in chat — the report is the deliverable. If unsupported slugs were requested, remind the operator which were skipped and why.

## Constraints and guards

- **Read-only.** This skill does not modify test code. If the operator asks the skill to apply fixes, that is a future capability that does not exist yet — decline and direct them to treat the report as input to a separate step.
- **Canonical entries are the single source of truth.** The canonical smell definitions in this skill bundle are the manifesto. If a detection feels right but the canonical entry's Signals don't cover it, that is a signal the canonical entry needs extending — stop and surface it as a manifesto gap, do not carry detection content outside the canonical entry.
- **Preserve regression-detection power.** Every prescribed remediation in a finding is bounded by the [preservation-of-regression-detection-power](references/docs/principles.md#preservation-of-regression-detection-power) governor rule.
- **Fossil vocabulary is a signal, not a verdict.** The word "refactor" in a title does not make a fossil; a ticket ID in a docstring does not make a fossil. The judgment is whether the vocabulary describes the test's reason-for-existence vs. the behavior it verifies.
- **Naming-lie detection is semantic.** Title/body tokenization is a first pass, not a verdict.
- **Cross-suite findings require targeted source reads.** The cross-suite assessor must read source before confirming a finding — behavior summary clustering alone is insufficient evidence.
- **Batch assessor is the universal audit engine.** There is no separate single-agent code path. Small suites get 1 batch assessor with all files; large suites get N batch assessors with partitions. The degenerate case of 1 batch is the "single-agent" experience.
- **Context budget is conservative by default.** The 200K-token floor with 60% content allocation ensures the audit works on any model. Operators can unlock better results (fewer batches, richer summaries) by specifying a larger context window.
- **Failure is isolated.** A failed batch assessor does not invalidate the entire audit. Note the gap and continue.
