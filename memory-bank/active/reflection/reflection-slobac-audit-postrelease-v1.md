---
task_id: slobac-audit-postrelease-v1
date: 2026-05-07
complexity_level: 2
---

# Reflection: slobac-audit post-release v1 hardening

## Summary

Applied the v1-hardening cut to the `slobac-audit` skill — output budget,
behavior-summary integrity gate, mandatory scout, generated taxonomy index
emitted to two locations with a CI drift-check, repo-level subagent
requirement, and cross-suite richness in the report — driven by failure modes
caught during the first three post-release runs against `ai-rizz`. Built clean
to plan, with one minor in-flight reconciliation between SKILL.md Step 8 and
the new report-template fields caught by QA.

## Requirements vs Outcome

All seven acceptance criteria delivered:
- A1 output budget (SKILL.md Step 4b with concrete per-richness caps),
- A2 IR-integrity gate (new SKILL.md Step 6.5 with retry-or-halt branch),
- A3 mandatory scout + manifest provenance (Step 3 prohibition + Suite manifest
  line in report header),
- A4/B4 generated index dual-emitted to SKILL.md and taxonomy/README.md with
  CI drift-check, CONTRIBUTING.md regen note, and a documented exception in
  techContext.md,
- B5 subagent-required note in the repo README.md,
- C8 cross-suite richness declaration in the report Summary,
- B6 captured as a follow-up rather than implemented (deferred per the original
  decision).

No scope creep, no requirement dropped. The two minor in-flight deviations
(out-of-docs-root link replacements in step 9 to keep `properdocs --strict`
green; a Step 8 / report-template reconciliation caught by QA) preserved
contracts and didn't change scope.

## Plan Accuracy

The plan held up well. 19 steps, 19 executed in order. Test plan covered the
edge cases that actually mattered (multi-scope round-trip, missing-marker
detection, idempotency on real targets). Identified challenges materialised
roughly as predicted — sentinel placement was benign; the `tests/python/`
collision was correctly anticipated and mitigated. The two surprises were
both small:

- **`pythonpath` configuration was missing from the plan.** I'd planned the
  `tests/python/` discovery scoping but not the import path for
  `slobac_tools/`; the first test run failed on `ModuleNotFoundError` and I
  added `pythonpath = ["."]` to the pytest config. One-line fix; could have
  been pre-baked but wasn't blocking.
- **Out-of-docs-root links in the README preamble.** The plan called for a
  link from `taxonomy/README.md` to `CONTRIBUTING.md`, and another to
  `SKILL.md`. Both escape `references/docs/` and fail `properdocs --strict`.
  Replaced with an inline `uv run` command. The plan should have flagged the
  doc-site link constraints; that's a takeaway.

## Build & QA Observations

Build was largely smooth. TDD cycles stayed disciplined — the plan's explicit
"write fixture/test → red → implement → green" sub-ordering (added during
preflight) pulled its weight; in two of the cycles I felt the pull to "just
write the implementation" and the explicit ordering kept me honest.

QA caught one substantive item (Step 8 of SKILL.md hadn't been updated
alongside the new report-template fields). That kind of doc-doc drift is
exactly what semantic review is for; mechanical gates would never have flagged
it. Worth keeping the explicit "documentation alongside code changes"
constraint in the QA checklist.

## Insights

### Technical

- **`properdocs --strict` polices the docs-root boundary aggressively.** Any
  link from a doc-site page to a file outside `references/docs/` (the docs
  root) fails strict-mode build. Mitigation pattern: use inline commands or
  full GitHub URLs; if a *path* must appear, render it as plain text. Worth
  remembering for future doc-bundle work.
- **Sentinel-bracketed generation in two locations is genuinely cheap.** One
  generator function (`replace_between_sentinels`), two `(target_path,
  link_target)` tuples in the entry point, and idempotency falls out of
  comparing pre/post-write text. The drift-check needed only `git diff
  --exit-code` on the two paths. The cost-to-correctness ratio was very good
  for what felt initially like a heavyweight introduction.

### Process

- **The "first post-release real run" is genuinely informative.** Three runs
  against one target with three different models produced three different
  failure modes that no single-author review would have caught: the
  inline-scout shortcut (auto + composer), the truncated-batch silent failure
  (auto), and the missing-subagent assumption (composer). Forcing a
  same-target multi-model exercise *before* declaring v1 stable is a
  defensible pattern to bake into the next release.
- **Doc-doc consistency benefits from QA semantic review.** When a single
  task touches both a workflow (`SKILL.md`) and the contract it implements
  (`report-template.md`), the prose can drift even when the artifacts are
  individually coherent. QA's "documentation alongside code" check caught
  exactly this. Tempting to skip QA on a "mostly docs" change; this
  reinforces that I shouldn't.

### Million-Dollar Question

If the slug → severity → detection-scope index had been a generated
artifact from day one of the manifesto, the per-entry header tables would
have been the only edit-point ever, the audit orchestrator's Step 2 would
have fanned in to a single embedded table from the start (no "read N files
for static metadata" anti-pattern), and the README's "curated reading
order" prose framing — which ended up incompatible with the sort key
contributors actually want — would never have existed. The most elegant
state is what we now have: per-entry headers as canonical metadata, a
generated index downstream, and a CI drift-check enforcing the
relationship. Cheap to run, cheap to extend (e.g. for a future Protects
column), and zero ambient sync cost on the contributor.
