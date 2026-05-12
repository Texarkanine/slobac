# Project Brief

## User Story

As a slobac-audit operator, I want the audit's intermediate representation (batch assessor output) to be persisted to disk so that orchestrator context compaction cannot silently destroy batch results and cause confabulated findings.

## Use-Case(s)

### Context compaction survival

A large audit (hundreds of tests, multiple batches) runs across several orchestrator turns. The runtime summarizes the orchestrator's conversation mid-flight. Because batch results currently live only in the orchestrator's volatile context, compaction destroys them. The orchestrator then confabulates behavior-summary tables instead of acknowledging the loss. File-first IR eliminates this failure mode entirely — batch results survive on disk regardless of what happens to the orchestrator's context.

### Post-hoc artifact review

Per-batch artifacts persisted to `.slobac/<run-id>/` remain available after the audit completes, allowing operators to trace findings back to the batch that produced them.

## Requirements

1. Batch assessors write their Findings and Behavior Summaries to `<workdir>/batch-<id>.md`. Their inline response to the orchestrator is metadata only: `{path, row_count, finding_count}`.
2. Cross-suite assessor receives a list of batch file paths (not inlined tables). It reads and merges in its own window. Its output (findings + `Consumed richness` line) stays inline.
3. SKILL.md Steps 6 + 6.5 updated: merge becomes pointer collection; integrity gate becomes deterministic per-file row-count check.
4. Workdir convention: default `.slobac/<run-id>/`, co-located with the eventual report. Support `--workdir` override. Document in SKILL.md Step 3 area.
5. Confabulation guardrail: orchestrator MUST NOT author behavior-summary rows. Missing/unparseable batch files → re-launch, never reconstruct. Add to Constraints section.
6. Rescope scout-level fail-fast: now guards cross-suite's window (`tests × richness_chars < 0.6 × window`), not the orchestrator's. Update Step 4.
7. Update report-template.md: optional `Suite manifest` line can reference workdir path for per-batch artifact traceability.
8. Filesystem-write capability precondition: Step 5 note — subagents must have write access to workdir. Refuse (don't silently fall back to inline) if they can't.

## Constraints

1. No inline-IR fallback path — commit fully to file-first.
2. Workdir kept on both success and failure (operator prunes).
3. Report synthesis stays in the orchestrator (reads only Findings sections from batch files — cheap, deterministic).
4. This is a documentation/contract change to skill files — no runtime code to test in the traditional sense.

## Acceptance Criteria

1. `batch.md` output contract specifies file-first output with metadata-only inline response.
2. `cross-suite.md` input contract specifies file paths, not inlined tables.
3. SKILL.md Steps 6 and 6.5 describe pointer collection and per-file row-count integrity checks.
4. SKILL.md Step 3 area documents workdir convention (`.slobac/<run-id>/`).
5. SKILL.md Constraints section includes the confabulation guardrail.
6. SKILL.md Step 4 fail-fast targets cross-suite's window explicitly.
7. `report-template.md` includes optional workdir reference in Suite manifest line.
8. SKILL.md Step 5 includes filesystem-write precondition.
