---
task_id: onboard-remaining-smells
complexity_level: 2
date: 2026-05-04
status: completed
---

# TASK ARCHIVE: Onboard Remaining 9 Per-Test Smells (and Rework)

## SUMMARY

Promoted nine per-test taxonomy slugs to first-class support in `slobac-audit`, achieving 15-smell parity with the manifesto: nine new fixtures under `tests/fixtures/audit/<slug>/`, SKILL/README/techContext updates, and verification-only checks on existing taxonomy `Detection Scope` headers—no orchestrator surgery. A follow-up **rework** (same task id, Level 2) removed drift-prone duplication from `skills/slobac-audit/SKILL.md`: structural enumeration of supported slugs via `references/docs/taxonomy/` entry files, uniform `## Aliases` sections in all 15 taxonomy entries (human-search discoverability only; orchestrator does not consume them), slug-only invocation contract with refusal of fuzzy phrase requests, harness-neutral subagent instructions at three dispatch sites, and softened lead paragraphs in `slobac-audit/README.md` and `memory-bank/techContext.md`. Post-rework doc follow-up: repo-root `CONTRIBUTING.md` as canonical taxonomy entry-shape SoT; taxonomy README trimmed; `memory-bank/systemPatterns.md` updated to point shape authorship at CONTRIBUTING.

## REQUIREMENTS

**Original**

- For each of nine slugs (`vacuous-assertion`, `tautology-theatre`, `pseudo-tested`, `over-specified-mock`, `implementation-coupled`, `presentation-coupled`, `conditional-logic`, `mystery-guest`, `rotten-green`): add to SKILL supported table (per-test row), add natural-phrase mappings, verify taxonomy entry scope, create fixture with positive + negative control + `expected-findings.md`, update fixtures README if needed.
- `properdocs build --strict` green; no regression for existing six smells; no orchestrator changes for these per-test-only additions.

**Rework (R1 / R2)**

- R1: Drop inline supported-smells table and operator-phrase map from SKILL; enumerate supported set by taxonomy entry file existence; operators invoke by explicit slug; refuse non-slug/fuzzy requests with supported-slug list; whitelist `all` / `everything` / unscoped for bulk-select; migrate phrase content to per-entry `## Aliases` for published-docs discoverability only; update taxonomy README shape SoT; do not reference Aliases in SKILL; mirror lead paragraphs without hardcoded counts; rewrite README scope-and-non-goals bullet for structural enumeration.
- R2: Replace harness-specific dispatch blocks at Steps 3, 5, 7 with single harness-neutral sentences per site.
- Preserve fixtures; no taxonomy detection-scope edits; properdocs green.

## IMPLEMENTATION

**Original build (2026-05-03):** 18 steps (one preflight amendment for `slobac-audit/README.md`): Phase A fixture stubs; Phase B taxonomy verification; Phase C SKILL table + phrase bullets + nine fixtures + README updates; Phase D properdocs and grep/consistency checks. One plan deviation: collapsed SKILL/fixtures-README stub steps into Phase C. Straggler: SKILL frontmatter description still said six smells until step 18.

**Rework build (2026-05-04):** Three commits—Phase A taxonomy `## Aliases` on all 15 entries + README shape SoT; Phase B SKILL slug-only contract + delete table/phrase map + neutral dispatch; Phase C README/techContext lead and scope bullet. Preflight amendment: README line 176 scope bullet; mid-flight contract shift from phrase resolution to slug-only (behaviors B2b/B2c/B4 inverted in plan). Post-formal-phase: `CONTRIBUTING.md`, taxonomy README trim, `systemPatterns.md` pointer.

**Key paths touched (non-exhaustive):** `skills/slobac-audit/SKILL.md`, `skills/slobac-audit/references/docs/taxonomy/*.md`, `skills/slobac-audit/README.md`, `tests/fixtures/audit/**`, `memory-bank/techContext.md`, `memory-bank/productContext.md` (rework reflect), `CONTRIBUTING.md`, `memory-bank/systemPatterns.md`.

## TESTING

- **Original:** `properdocs build --strict`; mechanical consistency; QA PASS (rotten-green missing planted TODO fixed).
- **Rework:** `properdocs build --strict` after Phase A and final; mechanical rg gates (B1–B12 family); fixtures untouched per `git diff`; QA PASS (trivial DRY fix in SKILL Step 2 refusal prose).

## LESSONS LEARNED

- **Technical:** `expected-findings.md` as spec / `test_*.py` as input scales for fixture authoring; mechanical gates do not catch spec–input drift—QA catches it. Post-rework: parallel curated lists of structural data are drift floors; slug-only contract avoids silent miscategorization from fuzzy resolution; uniform taxonomy metadata (e.g. `Detection Scope`, `## Aliases`) keeps rollouts mechanical.
- **Process:** Preflight amendments for missed touchpoints (README) paid off; for docs/fixture work, stubbing non-code artifacts is often low value vs writing final content; detailed behavior enumeration (B-tokens) made mid-flight contract shifts cheap.

## PROCESS IMPROVEMENTS

- Treat explicit per-behavior checklists as infrastructure for contract shifts, not only TDD.
- For fixture tasks, add an explicit “diff spec against planted code” step per fixture or end of batch.

## TECHNICAL IMPROVEMENTS

- Optional: stronger automated check that `expected-findings.md` claims match planted signals (beyond QA).
- Future taxonomy growth: new entry file automatically implies supported slug—no SKILL table edit.

## NEXT STEPS

None for this task. Initialize a new task with `/niko`.

---

## INLINED: Reflection (`reflection-onboard-remaining-smells.md`)

The following is the full reflection document as retained at archive time (original session + rework section).

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

---

## Rework — 2026-05-04

### Summary

Reduced the drift-prone duplication that 15-smell parity introduced into `slobac-audit/SKILL.md`: deleted the inline 15-row supported-slugs table and 15-bullet operator-phrase map, deleted the harness-specific dispatch boilerplate at three subagent-launch sites, migrated the operator-phrase content to a uniform `## Aliases` section in each of the 15 taxonomy entries (audience flipped to human-search discoverability, not orchestrator-runtime input), and rewrote SKILL.md Step 2 to enforce a slug-only invocation contract with structural enumeration of the supported set. Three commits across four plan phases. Build clean; QA caught one trivial DRY duplication and the mid-flight contract shift was the only meaningful plan deviation.

### Requirements vs Outcome

R1 and R2 from the rework brief are both fully delivered, plus an in-flight contract shift that the operator initiated during build prep:

- **R1 — taxonomy delegation**: SKILL.md no longer carries a parallel curated supported-slugs table or operator-phrase map; both surfaces drift-prone. Supported set is now the existence of `references/docs/taxonomy/<slug>.md`. Operator-phrase content survives at the taxonomy entries as `## Aliases` purely for human discoverability — the orchestrator does not consume it.
- **R2 — harness-neutral dispatch**: harness-specific bullet blocks (Cursor `Task`, Claude Code `dispatch_agent`) elided at all three subagent-launch sites. Each site's lead sentence already carried the harness-neutral instruction; the dispatch blocks were pure repetition.
- **In-flight contract shift (R1 amendment)**: mid-rework, the operator clarified that the orchestrator should not perform fuzzy phrase-to-slug resolution at all — operators must invoke by explicit slug, free-text requests are refused with the supported-slug list. This collapsed B4 from "SKILL must reference Aliases for phrase resolution" to "SKILL must NOT reference Aliases" and added B2b (slug-only contract) and B2c (preserved `all`/`everything`/unscoped wildcard). The taxonomy `## Aliases` section's purpose-and-audience documentation in the shape SoT was rewritten to reflect the new audience.

The slobac-audit `README.md` contributor-facing supported-smells table was deliberately preserved per project-brief scope. No fixture changes; no orchestrator surgery; no taxonomy detection-scope edits.

### Plan Accuracy

The plan held shape across one preflight amendment and one mid-flight contract shift:

- **Preflight amendment**: surfaced one missed touchpoint at `slobac-audit/README.md:176` — the "Scope and non-goals" bullet asserted a manually-curated supported-slug table backs slug refusal, which R1 invalidates. Plan step 6 expanded to rewrite the bullet alongside the lead-paragraph soften; B11b added. Sibling skills (`slobac-scout`, `slobac-batch`, `slobac-cross-suite`) confirmed clean by direct grep.
- **Mid-flight contract shift**: operator's mid-build clarification ("operators must ask by slug for minimal ambiguity; aliases are for human discoverability only") inverted B4 and reshaped Phase B step 4. The behaviors were re-enumerated in `tasks.md`; the project brief's R1 was rewritten in place; `progress.md` recorded the shift. The shift did not invalidate any work already done in Phase A — the alias content was migrated verbatim regardless of audience, and only the framing in the shape SoT and the SKILL.md prose differed between the two contracts.
- **No straggler at QA time** beyond one trivial DRY duplication (Step 2 refusal-payload prose restated the supported-set definition); fixed inline.
- **Phase batching held**: Phase A taxonomy rollout in one commit; Phase B SKILL.md surgery in one commit (so the file was never half-rewritten on disk); Phase C mirror cleanup in one commit. The "no half-migrated SKILL.md" mitigation worked exactly as planned.

### Build & QA Observations

**What went smoothly:**

- The 15-entry alias rollout was 15 mechanical `StrReplace` calls anchored on `## Description`. No content authoring; no editorial decisions per entry. Each insertion took less than 30 seconds.
- The SKILL.md surgery was a clean replace-block-with-paragraph + delete-three-bullet-blocks. The reduced surface is roughly 65 fewer lines for substantively the same instruction set.
- `properdocs build --strict` ran twice (post-Phase-A and post-Phase-C) in under 1.5 seconds each — the doc gate is essentially free.

**What QA caught:**

- One trivial DRY duplication in SKILL.md Step 2 — the refusal-payload prose parenthetically restated the supported-set definition given earlier in the same paragraph. Tightened inline. Properdocs rebuilt green.

**What QA notably did NOT catch (good):**

- Zero substantive deficiencies. The mid-flight contract shift could plausibly have created an inconsistency between `tasks.md` behaviors, the SKILL.md prose, the shape SoT, and the alias migration's framing — but the explicit re-enumeration in `tasks.md` immediately after the shift kept all four artifacts coherent.

### Insights

#### Technical

- **A fuzzy phrase-to-slug resolution mechanism is a footgun masquerading as ergonomic affordance.** The pre-rework SKILL.md prose ("Natural phrases map to slugs by meaning, not string match") implicitly delegated the orchestrator to do approximate string matching against a curated alias list — and the failure mode of getting it wrong is *silent miscategorization*: an operator says "find tautology" and the orchestrator picks `tautology-theatre` when the operator meant `vacuous-assertion` (vacuous tautology) or `pseudo-tested` (a stricter mutation-survives variant). The slug-only contract collapses that failure mode to a refusal, which is honest. Friction at the invocation site is preferable to incorrect behavior at the report site.
- **Parallel curated-list mirrors of structural data are lossy at every redundant copy.** SKILL.md's pre-rework supported-smells table was structurally `[entry filename → entry's Detection Scope header]`, recomputed by hand whenever a slug was added. Each manual recomputation is a drift opportunity. Eliminating the mirror eliminates the drift-floor — a future taxonomy entry costs zero SKILL.md edits to be supported.

#### Process

- **Mid-flight contract shifts on Level-2 reworks are cheap when the plan is detailed enough to re-enumerate behaviors.** The slug-only-contract pivot happened during build prep and would normally have been disruptive. It was not, because `tasks.md` had each behavior as a numbered B-token with a precise gate; inverting B4, adding B2b/B2c, and rewriting Step 4 of the implementation plan took about two minutes total. The lesson: TDD-shaped behavior enumeration is also good *contract-shift* infrastructure.
- **"Be disagreeable when necessary" got exercised twice and was wrong once.** I argued in favor of preserving the dedup logic at SKILL.md line 165 against the operator's initial reading; we agreed it stays. I argued in favor of an "Option B" lead-sentence in each `## Aliases` section; the operator rejected it correctly (the docs-site context is sufficient). The score is 1-1: pushing back is right when it surfaces a real consideration, and wrong when it adds friction for a non-decision. The discriminator: is the question "what's the right call" or "do I personally prefer A or B"?

### Million-Dollar Question

If the slug-only invocation contract had been a foundational assumption from the start, the orchestrator's Step 2 would have been a five-line paragraph from day one — "supported set = taxonomy filenames; operators name slugs explicitly; refuse otherwise; `all` is the bulk-select wildcard" — and there would have been no operator-phrase map to migrate, no fuzzy resolution mechanism to dismantle, and no `## Aliases` section to design. The taxonomy entries would still have gained their `## Aliases` section eventually for search discoverability, but as a docs-site enhancement decoupled from the orchestrator. The most-elegant solution is what we now have post-rework — the rework is exactly the cost of having walked through the alternative first. The cleanup was small enough that the path was net cheap, but next time SLOBAC reaches for a vocabulary-resolution layer in any orchestrator, the question to ask first is: "is this a slug-naming contract, or am I about to build a fuzzy-resolution mechanism that I'll regret?"
