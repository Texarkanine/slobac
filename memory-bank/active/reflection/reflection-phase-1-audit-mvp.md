---
task_id: phase-1-audit-mvp
date: 2026-04-23
complexity_level: 3
---

# Reflection: Phase 1 Audit MVP (`deliverable-fossils` + `naming-lies`)

## Summary

Shipped a harness-portable audit skill at `skills/slobac-audit/` covering the two Phase-1 smells, plus four fixture scenarios with expected-findings documentation. The ur-Skill + per-smell references shape held up through both fix-shape stress tests (two-phase for fossils, three-way for naming-lies). Manifesto-independence was preserved structurally: zero manifesto copy in the skill tree.

## Requirements vs Outcome

Every functional requirement from `projectbrief.md` was met:

- **Invocation in Cursor / Claude Code** via AgentSkills.io-shaped `SKILL.md` + `references/` tree — a primitive both harnesses support. Install-path mechanics documented per-harness in `skills/slobac-audit/README.md`.
- **Scoping to one, the other, or both smells** via natural-language parsing in `SKILL.md` Step 2. Out-of-scope slugs refused with a clear message rather than silently skipped.
- **Portable markdown report** with the plan-specified per-finding shape (location, smell slug, rationale, prescribed remediation, false-positive guard).
- **Read-only** — SKILL.md Step 6 and the Constraints section both call it out.
- **Two smells built for real, not stubbed.** Both per-smell augmentation files carry non-trivial content; each fixture scenario has non-trivial expected-findings.

One requirement deferred to the operator, per plan: manual harness-discoverability validation (step 12). The plan explicitly stated this is not a ship gate — the ship gate is "the shape works and it doesn't violate invariants," not "I personally booted both harnesses and ran it."

No requirements dropped or reinterpreted. One requirement added beyond plan (by QA accounting): the "Tests considered but not flagged" section in the report template. Defensible against the plan's false-positive-guard quality attribute, but not explicit; flagged for operator review at archive.

## Plan Accuracy

The 14-step plan was accurate enough that build executed it without re-ordering. Two step notes:

- **Step 10 (tech validation)** was pre-marked unneeded at plan time. Correct call.
- **Step 14 (mid-build taxonomy extension)** was conditional and not triggered. The manifesto's Signals and Prescribed Fix sections for both smells were sufficient at Phase-1 fidelity. This was a genuine-unknown at plan time (the OQ2 analysis flagged "taxonomy entry may be insufficient for detection" as an explicit failure mode) and the conditional branch was the right structural response.

One small build-phase surprise: four `expected-findings.md` files in the fixtures had relative paths that miscounted directory depth (`../../../docs/` instead of `../../../../docs/`). Caught by my own re-scan, not by automated validation. Noted for future fixture-style work but too minor to be a plan-improvement target.

## Creative Phase Review

**OQ1 (ur-Skill + per-smell references) held up cleanly.** The ur-SKILL.md workflow accommodated both fix-shape decision trees (two-phase rename/regroup for fossils; three-way rename/strengthen/investigate for naming-lies) without special-casing either. The mechanism: the ur-workflow describes the *detection loop* generically; per-smell augmentation files carry the *fix-shape decision rules* specific to each smell. Adding a third smell at Phase 2 would be: add an augmentation file, add the slug to the supported-slugs list in SKILL.md Step 2. No architectural changes.

**OQ2 (docs canonical; skill carries augmentation only) held up cleanly.** The structural-enforcement property was load-bearing during QA: there was literally no place in the skill tree where manifesto content could have drifted, because no manifesto content exists in the skill tree. QA's `DRY` check collapsed to a one-line verdict. Option E's generator + drift check would have added a build-time gate QA would have had to verify was healthy.

No friction points from either creative decision surfaced during build.

Sub-Agents-migration path (Option 4 from OQ1 analysis) is still untouched; Phase 1 scope was too small to exercise the prompt-context bloat failure mode that would motivate it. Noted for Phase 2 re-assessment.

## Build & QA Observations

**Went smoothly:**

- Fixture-first TDD order was the right call for a prompt-artifact build. Writing `expected-findings.md` before the SKILL.md workflow prose was forcing function — it surfaced the *specific* false-positive cases (cross-language synonymy, refactor-as-behavior, domain-vocabulary collisions) that needed codifying in the augmentation files. Without the fixtures, the augmentation files would have been aspirational.
- The docs build (`properdocs build --strict`) caught no regressions — the separation-of-trees property held: skill changes don't touch `docs/`, so the strict-link gate is orthogonal to skill correctness.

**Iterated on:**

- Getting the three-way fix arm decision rules crisp in the naming-lies augmentation. The rename / strengthen / investigate distinction is genuinely subjective at the edges; the final shape codifies heuristics ("title is specific and testable → lean strengthen; title is a shape-claim → lean rename; both suspect → investigate") but doesn't fully eliminate judgment. Judged acceptable because the manifesto itself doesn't eliminate the judgment either.
- Relative-link depth in fixture expected-findings files (noted above). Minor.

**QA caught:** one scope-creep (the `Skill version` field implementing a preflight advisory that was explicitly marked "not applied"). Zero substantive issues. Zero re-architecture needs.

## Cross-Phase Analysis

Three causal chains worth recording:

1. **Preflight amendments → build-phase uniformity.** Preflight tightened "augmentation may be absent" to "augmentation file is always present, even if minimal," and pinned the report's default output path. Without those amendments, build would have authored conditional logic in SKILL.md ("if augmentation exists, read it") and would have had to decide the default path on the fly. Amendments converted a future build-phase decision into a structural convention — precisely what preflight is for.

2. **OQ2 creative decision → QA DRY check was trivial.** The decision to structurally enforce manifesto-independence (no manifesto copy in the skill tree) meant QA had no drift to check. Option E (generator + drift check) would have required QA to inspect the generator's output and confirm the CI gate was healthy. Structural enforcement pays off at review time.

3. **Preflight advisory that was "not applied" → QA scope-creep catch.** The `Skill version` field was raised in preflight as "consider this; costs 1 line; not applied because operator didn't flag §5 #2." During build, "not applied" did not feel equivalent to "forbidden" — the line was easy to slip in. QA caught it. This is a latent weakness of the "advisory raised but not applied" pattern, noted under Insights → Process.

## Insights

### Technical

- **Prompt-artifact TDD is real and worth doing.** Writing expected findings before writing the detection prose reshapes the detection prose. Worth codifying the fixture-expected-findings convention for Phase 2's 13 additional smells rather than leaving it as ad-hoc per-smell practice.
- **The five-field per-finding invariant is the quality lever.** Location + smell slug + rationale + remediation + false-positive guard. The single most important of the five is the false-positive guard — it forces the audit to show its work and gives the reader a disagreement handle without re-running the audit.
- **Structural enforcement beats procedural enforcement whenever it's available.** OQ2's "no manifesto copy in skill tree" is the cleanest example in this task: an invariant that cannot be violated because there's nothing to violate.

### Process

- **"Advisory not applied" is an ambiguous state.** A preflight advisory raised but not applied is a footgun during build: the line between "nice idea, low cost, why not include it" and "operator explicitly deferred, build must not include it" is easy to blur under build-phase momentum. Two possible fixes for future tasks:
  1. Preflight either applies an advisory or rejects it. No middle state.
  2. Unapplied advisories are recorded in `tasks.md` under a "Forbidden during build absent operator approval" section, which build must explicitly check.
  The former is cleaner but may over-collapse the advisory pattern's value. The latter is more bureaucratic but preserves the "raise but defer" affordance. Worth raising with the operator on the next L3 cycle.
- **Niko's phase-mapping ritual (progress update + pre-phase commit) is load-bearing when multiple phase boundaries are crossed in one session.** This task crossed build → QA → reflect in a single operator-driven session; the explicit commit between phases is what keeps the memory bank auditable rather than a smear of uncommitted state.
