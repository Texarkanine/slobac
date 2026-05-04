---
task_id: taxonomy-fp-guards
date: 2026-05-04
complexity_level: 2
---

# Reflection: Author False-Positive Guards Across Taxonomy

## Summary

Authored 2–3 evidenced false-positive guards for each of the 13 stub-bearing taxonomy entries, sourced from `planning/research/` and matching the form of the two pre-existing exemplars. `properdocs build --strict` clean; editorial cross-pass clean. Substantive deliverable succeeded; one git-hygiene mistake of mine flagged for operator decision.

## Requirements vs Outcome

Every requirement satisfied. The user's three constraints — concise, evidenced, don't elide — were the audit-test for each guard and all 13 sections passed. Per-smell scoping was honored (no generic "be careful with LLM judgment" disclaimers). The two-vs-three-guards distribution reflects genuine corpus density rather than padding or trimming. No requirements dropped or added.

## Plan Accuracy

The plan's structure was right and worked as written. Two specific calls landed well:

- **Hoisting the corpus read into Step 1.** The 5 FINDINGS files (1985 lines combined) plus `report.md` were read once, indexed per-smell, then drawn from for each authoring step. Re-reading per smell would have wasted significant token budget and made cross-smell consistency harder.
- **Single sub-cycle described once and referenced 13 times.** Kept the plan ~140 lines instead of the ~600 it would have been if Steps 2–14 each enumerated their own procedure. Made the rigor visible without burying it in repetition.

The identified challenges were the ones that materialized — corpus unevenness was real (CLAUDE supplied most of the per-smell evidence; the smaller findings docs added breadth on a few smells). No surprises in the implementation itself.

## Build & QA Observations

Build was smooth. The hardest editorial decision was the recurring "is this guard a per-smell over-trigger or a generic LLM disclaimer?" question; answering it required cross-checking each candidate guard against that smell's specific *signals* in the entry, which is why I re-read each target file before authoring. That sub-step was worth its time and should be in the canonical procedure for any future stub-fill of this kind.

QA caught one substantive **non-finding** (cross-smell guard overlap on Go/Rust co-location is intentional per the full-bundle pattern) and one substantive **finding I introduced** (commit `0281eda` swept four pre-existing operator-uncommitted SKILL.md edits into my feature commit because I used `git add -A`). The first is acceptable. The second was a procedural error — operator decision pending.

## Insights

### Technical

- **Smell entries in the same neighborhood often share *facts* but use them for different *judgments*.** `wrong-level` and `monolithic-test-file` both cite Go/Rust co-location conventions; `shared-state` and `rotten-green` both touch on dead suite-level setup. Under the manifesto's full-bundle pattern (no snippet indirection), the right move is to restate the fact in each smell's voice rather than cross-link. This is a load-bearing consequence of the authoring model worth recording: redundancy at the *fact* level is acceptable; redundancy at the *judgment* level would be a smell.
- **Corpus density was uneven by smell, but not by author quality — by author *style*.** `FINDINGS-CLAUDE.md` (1085 lines, per-smell evidence with file:line citations and §-anchored taxonomy) was the highest-leverage source per smell; the smaller findings docs were valuable for breadth but rarely contributed unique guards. For future per-smell research authoring, CLAUDE-style line-cited evidence is the contribution shape that pays dividends downstream.

### Process

- **`git add -A` is too sweeping in a working tree that may carry unrelated WIP.** Default to `git add <explicit-paths>` even when the working-tree status looks clean, *especially* when the in-flight task involves files in many directories. The cost of typing 13 paths is much smaller than the cost of conflating unrelated work into a feature commit. This belongs in the project's own git-safety guidance (or my private discipline note), not just in retrospect.
- **The TDD adaptation worked.** `always-tdd.mdc` literally scopes to "code changes." For documentation authoring, the equivalent of "tests get written first" is *the editorial checklist applied during each authoring sub-cycle*. Per-unit ordering is preserved when the checklist is per-guard (don't-elide check, concision check, evidence pointer required) rather than per-section. Future doc-authoring tasks at L2+ should adopt this pattern explicitly rather than hand-waving "TDD doesn't apply."

### Million-Dollar Question

If false-positive guards had been a foundational assumption from the start, the most elegant shape would have been to author them *paired with each Signal* rather than as a separate `## False-positive guards` section. A guard is the inverse-side of a signal — "fire on X, suppress when X has property Y." Co-locating them per-signal (`Signal X. *False-positive when…*.`) would mean an audit assessor evaluating one detection reads one paragraph instead of two sections. The current shape (separate `## Signals` and `## False-positive guards` sections) was inherited and works, but a future major-version reshape of the taxonomy entry could co-locate them. This is a CONTRIBUTING-shape change requiring all 15 entries to update; out of scope for this task, recorded as a possible Phase-3 architectural improvement.
