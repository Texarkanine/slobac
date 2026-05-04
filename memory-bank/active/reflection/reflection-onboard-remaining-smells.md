---
task_id: onboard-remaining-smells
date: 2026-05-03
complexity_level: 2
---

# Reflection: Onboard Remaining 9 Per-Test Smells

## Summary

Promoted 9 per-test taxonomy slugs (`vacuous-assertion`, `tautology-theatre`, `pseudo-tested`, `over-specified-mock`, `implementation-coupled`, `presentation-coupled`, `conditional-logic`, `mystery-guest`, `rotten-green`) to first-class supported status in the `slobac-audit` framework, bringing it to 15-smell parity with the manifesto. Mechanical extension of the architecture delivered in the prior audit-orchestration archive: 9 new fixtures, SKILL/README/techContext updates, no orchestrator surgery. Build and QA both passed with one trivial QA fix.

## Requirements vs Outcome

Every requirement from the project brief was implemented:

- All 9 smells onboarded to the SKILL supported-slug table with `Detection Scope: per-test`.
- All 9 smells gained natural-phrase mapping bullets sourced from their canonical Summary/Description sections.
- All 9 fixtures created at `tests/fixtures/audit/<slug>/`, each with planted positives exercising the canonical signals + a negative control + an `expected-findings.md` mirroring the report-template shape used by existing fixtures.
- `tests/fixtures/audit/README.md`, `skills/slobac-audit/README.md`, and `memory-bank/techContext.md` all promoted to 15-smell parity.
- `properdocs build --strict` remains green.
- Existing 6-smell behavior preserved.

No requirements were dropped, descoped, or reinterpreted. The only addition beyond the original plan was step 15 (`skills/slobac-audit/README.md`), surfaced by preflight as a missed touchpoint and amended into the plan before build began.

## Plan Accuracy

The 18-step plan (17 original + 1 preflight amendment) executed cleanly with one documented deviation and one straggler caught during the final review.

- **Documented deviation**: Phase A steps 2 (SKILL.md TBD-placeholder stub) and 3 (fixtures README placeholder section) were collapsed into Phase C steps 13 and 14. Rationale: TBD placeholders in a runtime instruction document would actively misinform the orchestrator if read during the build window, and the table shape was already established by the existing 6 entries — no interface design to validate. The fixture `.py`/`expected-findings.md` stubs (step 1) were sufficient TDD scaffolding for the spec-input pair pattern.
- **Step-18 straggler**: the SKILL.md YAML frontmatter `description:` field was missed by step 13's body-text edit and still claimed "Supports 6 smells" until grep caught it during step 18. Trivial fix; no rework loop.
- **Per-smell challenges materialized as predicted**: each fixture stayed scoped to its own smell; the "multi-shape smells" risk was managed by exercising one or two shapes per smell (rather than all shapes), as the plan permitted.

## Build & QA Observations

**What went smoothly:**

- The fixture-shape template from `naming-lies/expected-findings.md` translated directly to the 9 new `expected-findings.md` files. Each took ~2-3 minutes of structural composition once the canonical entry was read.
- The SKILL.md table extension was mechanical — 9 row insertions in the established format.
- `properdocs build --strict` was a fast confirmatory gate (1.29s build).

**What was uneventful (good):**

- All 9 taxonomy entries already carried `Detection Scope: per-test` headers from the prior task's uniform metadata rollout — verification only, no edits needed.
- No cross-skill reference paths broke; no manifesto cross-links needed updating.

**What QA caught:**

- One substantive deficiency: `rotten-green/test_metric_collector.py` positive 1 was missing the planted `# TODO: test this` comment that both its surrounding inline docstring and `expected-findings.md` cite as the canonical signal. This was a fixture-content gap — the planted file claimed to demonstrate a signal it did not actually contain. Trivial fix (one-line StrReplace), no rework loop. The QA semantic-review process is precisely the gate that catches this class of error: the mechanical gates (`properdocs build --strict`) cannot detect that a fixture does not match its own spec.

## Insights

### Technical

- **The `expected-findings.md`-as-spec / `test_*.py`-as-input pattern is the right TDD shape for fixture authoring.** The prior task's audit-orchestration archive established this pattern implicitly for the 4 new orchestration fixtures; this task confirmed it scales cleanly to 9 more. Writing the spec first surfaces the canonical signals from the taxonomy entry into the test-author's head before any planted code is written, so the planted code is genuinely an instance of the signals rather than an approximation. The QA finding (missing TODO) is the *exception that proves the rule* — when the spec and the input drift, QA's job is to detect the drift.
- **Spec-input drift is a real failure mode for fixture authoring.** The mechanical gates do not catch it. Future fixture-authoring tasks should consider an explicit "diff the spec against the input" review step at the end of each per-fixture cycle, not just at the end of the whole build.

### Process

- **Preflight earned its keep again on a Level 2 task.** The amendment for `skills/slobac-audit/README.md` (a touchpoint the plan author missed) would have surfaced as either a build-time discovery or — worse — a post-archive inconsistency between the SKILL state and the README state. Surfacing it pre-build was strictly cheaper.
- **The "Phase A stubbing" ritual is over-prescribed for documentation/fixture work.** Stubbing a markdown spec file with a header and then filling it in adds zero validation value compared to writing the final content directly. The deviation taken in this task (collapsing Phase A.2/A.3 into Phase C) was the right move; future plans for similar work should not prescribe stub steps for non-code artifacts in the first place.

### Million-Dollar Question

If 15-smell parity had been a foundational assumption from the start, the architecture would not differ. Each smell's onboarding cost is dominated by the per-fixture authoring effort, which scales linearly and is bounded by the canonical entry's Signals section. The framework's invariants (one-file-per-smell taxonomy, full-manifesto-in-bundle, batch-assessor-as-universal-engine, cross-skill reference convention) all hold at 6 smells, 15 smells, and any future N — the work-per-smell does not compound. The most-elegant solution is what was built: a flat extension of the existing scaffolding, with the only architectural moment being the prior task's decision to make `Detection Scope` a uniform header across all taxonomy entries. That decision pre-paid the cost of every subsequent onboarding, including this one.
