---
task_id: file-first-ir
complexity_level: 3
date: 2026-05-13
status: completed
---

# TASK ARCHIVE: file-first-ir

## SUMMARY

The slobac-audit skill’s intermediate representation was changed from inline (batch findings and behavior summaries living only in the orchestrator’s volatile context) to **file-first**: each batch assessor writes Findings and Behavior Summaries to `<workdir>/batch-<id>.md` and returns metadata only `{path, row_count, finding_count}`. The orchestrator collects pointers and runs a per-file row-count integrity gate. The cross-suite assessor receives a list of batch file paths, reads and merges behavior summaries in its own window, and continues to emit inline cross-suite findings. This removes the failure mode where orchestrator context compaction destroys inline batch results and the orchestrator confabulates replacement tables.

Default workdir: `.slobac/<run-id>/` in the operator’s cwd, with optional `--workdir` override. Workdir is retained on both success and failure. Report synthesis remains in the orchestrator; report template gains an optional workdir reference for traceability.

## REQUIREMENTS

From the project brief (all satisfied):

1. Batch assessors write to `<workdir>/batch-<id>.md`; inline response is metadata only.
2. Cross-suite assessor receives file paths (not inlined tables); reads and merges in its own window; cross-suite output stays inline.
3. SKILL.md Steps 6 and 6.5: pointer collection and deterministic per-file row-count integrity gate.
4. Workdir convention documented (default `.slobac/<run-id>/`, `--workdir` override).
5. Confabulation guardrail: orchestrator MUST NOT author behavior-summary rows; missing/unparseable batch files → re-launch batch, never reconstruct from memory or source.
6. Scout-level fail-fast rescoped to guard the **cross-suite** window (`tests × richness_chars < 0.6 × window`), not the orchestrator’s.
7. `report-template.md`: optional workdir reference on Suite manifest line.
8. Filesystem-write precondition in Step 5: subagents must have write access to workdir; refuse if not guaranteed.

**Constraints honored:** No inline-IR fallback; workdir kept on success and failure; changes limited to markdown contracts in the skill bundle (no traditional automated tests for these files).

## IMPLEMENTATION

**Approach:** Ten-step plan executed in order: batch output contract → cross-suite input contract → behavior-summary merge semantics → orchestrator workdir and Steps 4–6.5 → constraints → report template → cross-file consistency review.

**Key files touched** (all under `skills/slobac-audit/` unless noted):

| File | Change |
|------|--------|
| `references/subagents/batch.md` | File-first Step 4: write `<workdir>/batch-<id>.md`, return `{path, row_count, finding_count}`; workdir input; clarify read-only means codebase only, not workdir. |
| `references/subagents/cross-suite.md` | Inputs: batch result file paths; read files, extract behavior summaries, merge/re-sort; clustering references self-merged table. |
| `references/behavior-summary-format.md` | Merge semantics and consumption: cross-suite owns merge from disk, not orchestrator. |
| `SKILL.md` | Step 3 area: `.slobac/<run-id>/`, run-id, `--workdir`; Step 4: cross-suite window for fail-fast; Step 5: write precondition, pass workdir; Step 6/6.5: pointer collection + per-file integrity; Constraints: no orchestrator-authored rows, no inline fallback; batch launch wording (write access to workdir); Step 8: populate Workdir in report header. |
| `references/report-template.md` | Optional workdir in header / Suite manifest for artifact traceability. |

**Data flow (after):** Batch *i* → writes `batch-i.md` → orchestrator holds metadata only → cross-suite gets path list → reads files → merge → findings. Orchestrator no longer holds full IR for batches in context.

**Design decisions (from planning / build):**

- Workdir path: `.slobac/<run-id>/`; run-id e.g. ISO-8601 with seconds to avoid collisions.
- **Readonly clarification:** The batch assessor remains read-only with respect to the **audited codebase**; writes to the audit workdir are required. Batch assessor is no longer described as a “readonly subagent” in the sense that blocked workdir writes.
- Cross-suite context risk for large suites mitigated by existing Step 4 richness / window guard targeting cross-suite’s window.

**Creative phase:** None executed — approach was clear from the bug report and intent clarification. (No creative folder; no options/rationale document to inline.)

## TESTING

- **Automated:** N/A — skill workflow definitions are markdown contracts without a project test harness for them.
- **Preflight:** PASS (seven checks); TDD encoding noted as structural/cross-file consistency for these artifacts.
- **QA:** PASS — all eight acceptance criteria verified against the edited files; KISS/DRY/YAGNI, completeness, regression, integrity, documentation checks passed; no post-QA fixes required.
- **Manual:** Invoking the skill against `tests/fixtures/audit/` was noted as out-of-scope in the task plan; not performed as part of this closure.

## LESSONS LEARNED

- **Technical:** A single word (“readonly”) had bundled two meanings — do not mutate the repo under audit vs. run in a read-only sandbox. File-first IR forced splitting these explicitly. **Recommendation:** When a constraint spans multiple concerns, spell out each concern so a change to one cannot silently invalidate the other.
- **Process:** Preflight’s upfront call that markdown contracts have no automated tests avoided a futile search for test hooks; the dedicated cross-file consistency review (plan Step 10) caught minor stale phrasing (“orchestrator handed you”) and ensured Step 8 populated the Workdir line — consequences of the contract flip rather than gaps in the numbered steps.
- **Plan quality:** Component analysis and dependency mapping before edits turned a potentially iterative “fix reference, discover break” loop into a single-pass implementation with a short QA tail.

## PROCESS IMPROVEMENTS

None surfaced as mandatory changes. The existing L3 sequence (plan → preflight → build → QA → reflect → archive) fit this documentation-only change set well.

## TECHNICAL IMPROVEMENTS

Optional follow-ups (not committed as part of this task):

- If the team wants stronger guarantees later, consider lightweight lint or CI checks that skill cross-references resolve and required sections exist (without executing the audit).

## NEXT STEPS

None. Task complete; memory bank ephemeral state cleared for the next `/niko` session.
