---
task_id: slobac-skill-rename-invocation-parity
date: 2026-05-06
complexity_level: 2
---

# Reflection: Align Skill Invocation Name Across Cursor & Claude Code

## Summary

Renamed the SLOBAC audit skill directory from the short unbranded token to `skills/slobac-audit/` so the Cursor slash command reads `/slobac-audit`, giving both harnesses the same visible token (at the cost of the accepted doubled-prefix `/slobac:slobac-audit` in Claude Code). All six automated verification gates passed clean; operator smoke tests remain the only pending gate (cannot run until the PR merges).

## Requirements vs Outcome

Every requirement was delivered without descoping or addition. The one wrinkle was a corrected understanding of Cursor's slash-command registration: the SKILL.md `name` field has no effect on the Cursor slash token — the directory name is the sole source. The prior task's archive recorded this incorrectly, and the clarification was captured in `using-slobac.md` and the memory bank as a drive-by fix. This was an improvement over the original plan, not a requirement gap.

## Plan Accuracy

The plan was accurate in sequence, scope, and file list. The only amendment came during preflight: `tests/fixtures/audit/README.md` surfaced two stale taxonomy-path prose references (lines 44 and 48) that the initial plan had not enumerated. Preflight caught this correctly, and a one-line plan amendment was recorded before build began. The originally identified challenges (distinguishing live path references from fixture/archive/prose occurrences; two-repo scope requiring a coordinated commit) were the challenges that actually materialized — no surprises from elsewhere.

## Build & QA Observations

Build was clean from end to end. The `git mv` preserved history correctly; all four grep gates returned zero false negatives after the move. The two-repo coordination (slobac + txrk9-agent-plugins) went smoothly because the sibling touchpoint was isolated to a single README line. QA required zero rework — all automated gates passed on the first run. The one open item is the operator smoke test, which is blocked on the PR merging to a state the plugin harnesses can install.

## Insights

### Technical

- Cursor registers slash commands from the **skill directory name**, not from the `name` field in SKILL.md. The `name` field is purely ornamental for Cursor (it may surface in Claude Code's display, but it has no routing effect). Any future skill directory naming decision must treat the directory name as the user-visible Cursor token — not a metadata field inside the file.

### Process

- The preflight phase earned its keep here: it caught a file (`tests/fixtures/audit/README.md`) that the plan missed because the initial scope definition focused on source files, not fixture documentation. Preflight's grep-then-inspect loop is the right place to surface these stragglers.

### Million-Dollar Question

If directory-based slash registration had been a foundational assumption from the start, the plugin distribution task would have named the directory `skills/slobac-audit/` from day one. The `name` field in SKILL.md would have been treated purely as a human-readable display label with no implied routing semantics. The entire rename task would never have been necessary — the correct token would have been baked in at initial creation, with `using-slobac.md` documenting the directory-name rule from the first commit. Nothing architectural changes; the lesson is simply naming discipline applied one task earlier.
