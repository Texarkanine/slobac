---
task_id: phase-1-audit-mvp
date: 2026-04-23
complexity_level: 3
---

# Reflection: Phase 1 Audit MVP (`deliverable-fossils` + `naming-lies`)

## Summary

Shipped a harness-portable audit skill at `skills/slobac-audit/` covering the two Phase-1 smells, plus four fixture scenarios with expected-findings documentation. The ur-Skill + per-smell references shape held up through both fix-shape stress tests (two-phase for fossils, three-way for naming-lies). ~~Manifesto-independence was preserved structurally: zero manifesto copy in the skill tree.~~ *Amended (second rework): under the canonical-in-bundle architecture, the skill bundle IS the manifesto's authoring surface. Manifesto-independence is now structurally enforced by construction — there is one document per smell, and forking is impossible.*

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

~~**OQ2 (docs canonical; skill carries augmentation only) held up cleanly.**~~ *Retracted (first rework): the "high confidence" rating was misplaced. OQ2's creative phase conflated filesystem co-location (the files live in the same tree in this repo) with runtime co-location (the path is reachable from the skill's install root). The former held; the latter did not. Invariant #11 (skill-root self-containment) was codified as a result.* *Retracted again (second rework): the OQ2-redux (Option E: generator + CI drift-gate) decision was itself invalidated — the operator rejected committed generated content and augmentation-file drift as architecturally a smell. The recurring failure mode — each creative phase satisfies its enumerated constraints and misses a later-surfaced one — is calibration-bearing and flagged for Phase-2 creative-phase discipline. The final architecture (OQ3, Option γ: canonical-in-bundle, site-rendered-via-snippet) resolves all three passes' concerns: invariant #11 is satisfied structurally, no generated content, no augmentation-file drift, and manifesto-independence holds by construction.*

No friction points from the OQ1 creative decision surfaced during build.

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

2. ~~**OQ2 creative decision → QA DRY check was trivial.**~~ *Retracted (second rework): the original observation remains locally true for the initial build, but the architecture it described (no copy in the skill tree) was invalid under the runtime-root constraint. The second rework's canonical-in-bundle architecture achieves a stronger form of the same property: there is literally one document per smell, no copy, no drift surface, and no QA work to validate coherence.*

3. **Preflight advisory that was "not applied" → QA scope-creep catch.** The `Skill version` field was raised in preflight as "consider this; costs 1 line; not applied because operator didn't flag §5 #2." During build, "not applied" did not feel equivalent to "forbidden" — the line was easy to slip in. QA caught it. This is a latent weakness of the "advisory raised but not applied" pattern, noted under Insights → Process.

## Insights

### Technical

- **Prompt-artifact TDD is real and worth doing.** Writing expected findings before writing the detection prose reshapes the detection prose. Worth codifying the fixture-expected-findings convention for Phase 2's 13 additional smells rather than leaving it as ad-hoc per-smell practice.
- **The five-field per-finding invariant is the quality lever.** Location + smell slug + rationale + remediation + false-positive guard. The single most important of the five is the false-positive guard — it forces the audit to show its work and gives the reader a disagreement handle without re-running the audit.
- **Structural enforcement beats procedural enforcement whenever it's available.** ~~OQ2's "no manifesto copy in skill tree" is the cleanest example in this task.~~ *Amended (second rework): the canonical-in-bundle architecture is the real example — there is one document per smell, the skill reads it, the site renders it. Structural enforcement went through three iterations (OQ2 → OQ2-redux → OQ3) before landing on an architecture where the invariant holds by construction rather than by discipline.*

### Process

- **"Advisory not applied" is an ambiguous state.** A preflight advisory raised but not applied is a footgun during build: the line between "nice idea, low cost, why not include it" and "operator explicitly deferred, build must not include it" is easy to blur under build-phase momentum. Two possible fixes for future tasks:
  1. Preflight either applies an advisory or rejects it. No middle state.
  2. Unapplied advisories are recorded in `tasks.md` under a "Forbidden during build absent operator approval" section, which build must explicitly check.
  The former is cleaner but may over-collapse the advisory pattern's value. The latter is more bureaucratic but preserves the "raise but defer" affordance. Worth raising with the operator on the next L3 cycle.
- **Niko's phase-mapping ritual (progress update + pre-phase commit) is load-bearing when multiple phase boundaries are crossed in one session.** This task crossed build → QA → reflect in a single operator-driven session; the explicit commit between phases is what keeps the memory bank auditable rather than a smear of uncommitted state.

---

## Second Rework Addendum (2026-04-29)

### Requirements vs Outcome (second rework)

The second rework's scope was narrow and precise: invert canonicality so the skill bundle holds the canonical taxonomy, and `docs/taxonomy/*.md` becomes snippet-include wrappers. Every requirement was met:

- 15 manifesto entries migrated via `git mv` (preserving git history) to `skills/slobac-audit/references/docs/taxonomy/`.
- 15 `pymdownx.snippets` wrappers created at `docs/taxonomy/`.
- False-positive guards promoted from augmentation files into canonical entries (Phase-1 smells) or stubbed (non-Phase-1 smells).
- Augmentation files deleted; invocation vocabulary inlined into SKILL.md; restated manifesto content dropped.
- `properdocs build --strict` passes under the new layout.
- No generator, no CI drift-check, no committed derived content.

No requirements were dropped or reinterpreted. S7 (delete first-rework generator artifacts) was a no-op because those artifacts were never committed — they existed as uncommitted working-tree changes from the superseded first rework and were discarded at session start.

### Plan Accuracy (second rework)

The 14-step plan (S1–S14) was accurate. PF2's amendment (combine S1+S2 into a single commit) correctly prevented a broken intermediate state. PF1's amendment (S4a for README shape spec) correctly caught a completeness gap. No steps needed reordering or splitting beyond the preflight amendments.

One non-obvious moment: the first attempt at S4 (scripting the 13-file stub insertion) silently succeeded on file writes but crashed on a print statement, then a re-run doubled the insertions. Caught and fixed immediately. The lesson: when scripting multi-file edits in a loop, verify the file state after the loop completes, not just the script's exit code.

### Creative Phase Review (second rework)

OQ3 (Option γ — definitional canonical + discursive wrapper) held up perfectly. The operator's framing ("there might not be ANY wrapping" + "tight description") mapped cleanly to the empty-wrapper-as-default + canonical-carries-everything design. The calibration note ("what will the operator's first reaction to the shipped artefact be?") was not stress-tested this time — the architecture is simple enough that no hidden constraint is likely to surface, but the discipline is worth carrying forward.

### Build & QA Observations (second rework)

**Went smoothly:**

- The `git mv` + wrapper approach is mechanically simple and fully reversible. The combined commit (PF2) was the right call — no broken intermediate state.
- `properdocs build --strict` with `check_paths: true` is an excellent structural integrity gate for snippet-include layouts. It caught nothing (because the implementation was correct), but it *would* catch a typo in any wrapper path.

**Iterated on:**

- Shell connectivity glitch mid-session (commands returning empty output with 0ms duration). Worked around by retrying after a brief pause. One phantom commit (the S10+S11+S12 memory-bank commit) appeared to succeed but was actually lost; re-committed successfully after the glitch resolved.

**QA caught:** one stale "augmentation file" reference in SKILL.md's Constraints section. Trivial fix. The same class of issue as the original QA's scope-creep catch — stale language from a superseded architecture surviving into the shipped artifact.

### Cross-Phase Analysis (second rework)

1. **Preflight amendments → build correctness.** PF2 (combine S1+S2) prevented what would have been a broken intermediate commit. PF1 (S4a) ensured the README shape spec stayed in sync with the new section. Both are pure preflight wins — issues that would have required post-hoc fixup if not caught.

2. **Three-pass calibration debt → disciplined creative phase.** The OQ3 creative doc explicitly carries the calibration note from three prior passes. This is the first decision that shipped without a post-build rejection. Whether that's because the architecture is genuinely simpler (likely) or because the calibration discipline is working (possible), the pattern is worth continuing.

### Insights (second rework)

#### Technical

- **Snippet-include inverts the authoring surface without losing the reader surface.** The key insight from this rework is that `pymdownx.snippets` + `check_paths: true` + `strict: true` gives structural integrity on the link between canonical and wrapper. It's a zero-maintenance sync mechanism — no generator, no CI step, no "remember to regenerate." Future skills that need to own canonical content consumed by a rendered site should use this pattern.
- **`git mv` preserves history across the inversion.** The 15-file migration kept full git blame for every taxonomy entry. This matters for tracing when a detection signal was added or a guard was authored.

#### Process

- **The "nobody reads raw" operator constraint was a load-bearing unlock.** The original OQ2 (and OQ2-redux) both failed because they preserved the premise that `docs/*.md` must render correctly as raw markdown on github.com. The operator's clarification that the rendered site is the only reader surface eliminated that constraint and opened the snippet-include option that had been structurally killed twice. Lesson: when multiple creative-phase passes fail at the same architectural boundary, the constraint itself may be the wrong constraint — escalate to the operator before the next attempt.
- **Uncommitted first-rework artifacts simplify the second rework.** Because the first rework's build changes were never committed (QA was superseded before it ran), the second rework started from a clean HEAD. No revert commits, no tangled git history. This was accidental (the workflow's phase-gating prevented the first rework from reaching the commit-worthy QA phase), but it's a good outcome. The lesson is that uncommitted build artifacts from a superseded rework are a *feature*, not a hazard — they evaporate cleanly.

---

## Third Rework Note (2026-04-29)

The second rework's snippet-include architecture was correct under its stated constraints and passed QA cleanly. During pre-merge review, two remaining architectural seams were identified: (1) SKILL.md Constraints still used pre-inversion "audit cites the manifesto" language, and (2) the 15 snippet-include wrappers at `docs/taxonomy/*.md` were pure indirection — each file contained a single `--8<--` directive and no content. The wrappers existed solely to bridge properdocs's `docs_dir: docs` expectation with the canonical content living inside the skill.

The corrective action was to complete the inversion: move the **entire** `docs/` tree (principles, glossary, workflows, taxonomy/README, .pages) into `skills/slobac-audit/references/docs/` and point `properdocs.yml` `docs_dir` there. This eliminated the wrappers, the `docs/` directory, and the link-path footgun (canonical files' relative links now resolve at their actual filesystem location). The full manifesto now lives inside the skill root, satisfying invariant #11 for all manifesto content — not just taxonomy entries.

This is not a retraction of the second rework's approach — the snippet-include architecture was correct at the time and would have shipped fine. It is an evolution: once the operator saw that the wrappers added zero content, the simpler architecture (no wrappers, no indirection) was strictly preferable.
