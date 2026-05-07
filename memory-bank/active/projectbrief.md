# Project Brief: slobac-audit post-release v1 hardening

## Context

The `slobac-audit` skill had its first "real" post-release exercise: three runs against the
`ai-rizz` test suite (`tests/`, 33 files, ~389k chars, ~377 tests) using three different
models (default/auto, composer-2, claude-opus-4-7). Cross-run comparison plus warehouse
forensics on the parent sessions revealed material correctness gaps in two of the three
runs, several skill-workflow contracts that operators silently violated, and one piece of
wasted per-run work the skill bundle could pre-bake.

See `memory-bank/slobac-audit-{auto,composer,opus}.md` for the three reports and
`memory-bank/slobac-audit-{auto,composer,opus}-ai-rizz.md` for the chat exports.

## Story

As a `slobac-audit` skill operator, I want the skill to fail loud (or not at all) on the
failure modes the post-release runs exposed, and to stop wasting work on things the
skill bundle already knows, so that audits I trigger are reliably as correct as the
opus run was — regardless of which model executes the orchestrator.

## Acceptance criteria

1. **Output budget (A1)**: The orchestrator step on partitioning explicitly budgets
   subagent **output** size in addition to input. Per-richness test-count caps are
   documented as concrete numbers, and the Step 4 partitioning rule cites the binding
   budget (whichever is smaller).
2. **IR integrity check (A2)**: Between the merge step and the cross-suite step, the
   orchestrator validates that the merged behavior-summary table covers the suite's
   tests within a stated tolerance, and either retries the affected batch or halts with
   a clear message instead of silently feeding incomplete IR to cross-suite.
3. **Mandatory scout (A3)**: The skill text forbids the orchestrator from enumerating /
   measuring the suite itself; the suite manifest is named in the report header so a
   reader can audit whether scout actually ran.
4. **Generated taxonomy index (B4)**:
   - A Python script under `pyproject.toml` parses every
     `skills/slobac-audit/references/docs/taxonomy/<slug>.md` (excluding `README.md`),
     reads the canonical header table at the top of the file, and (re)generates the
     index table currently maintained by hand in
     `skills/slobac-audit/references/docs/taxonomy/README.md` (lines ~11–27 today).
   - The script lives where `pyproject.toml` can run it via `uv run` / a script entry.
   - `SKILL.md` Step 2 points at `taxonomy/README.md` for the supported-slug list +
     detection scopes — replacing the inline 15-file fan-out.
   - CI runs a drift check (regenerate, diff against committed) and fails the PR on
     drift.
   - `CONTRIBUTING.md` (or equivalent) documents "after editing a taxonomy entry, run
     <command> to regenerate".
   - **Open question for Plan phase:** how to handle the README index's `Core move`
     column, which is hand-curated and has no source in the per-entry header today.
     Candidates: (a) generator preserves that column on regen; (b) add `Core move` to
     each per-entry canonical header (true single-source-of-truth, leaning toward this);
     (c) keep README index hand-maintained, generate a minimal separate scope index for
     the orchestrator. Pick during Plan.
5. **Subagent assumption documented (B5)**: The required-environment assumption
   (subagent-capable harness) is called out in the project-level `README.md`. No
   pointer from `SKILL.md` to the repo README — the skill bundle ships independently of
   the repo, so any such pointer would dangle once installed.
6. **Cross-suite richness in report (C8)**: The cross-suite assessor declares the
   richness tier of the IR it consumed; the report renders that declaration in the
   relevant findings section so a reviewer can downgrade their confidence on a
   `compact`-fed cross-suite pass.
7. **B6 captured as future work**: The deferred regex-canary idea is recorded under
   "Follow-ups" in `progress.md` (and/or a tracking file) so it isn't lost.

## Explicit non-goals

- **B6 (regex canaries)**: Deferred pending creative exploration on polyglot signal
  hinting without constraining agent reasoning.
- **B5 inline-fallback workflow**: We do *not* add a degraded subagent-less code path.
  Operators in subagent-less harnesses are told to use a different harness.
- **C7 orchestration provenance beyond manifest**: The manifest reference in the report
  (from A3) is the only provenance addition; no per-subagent ID/size telemetry block.
- No changes to the smell taxonomy itself.
- No changes to the audit's findings shape (still five fields).

## Stakeholders

Operator (the skill caller) and skill maintainer (CI drift check + CONTRIBUTING note are
for them).
