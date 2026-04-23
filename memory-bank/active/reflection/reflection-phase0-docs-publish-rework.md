---
task_id: phase0-docs-publish-rework
date: 2026-04-23
complexity_level: 2
---

# Reflection: Phase 0 docs-publish rework (mkdocs → properdocs, pip → uv)

## Summary

Two mechanical toolchain substitutions on the already-shipped Phase 0 pipeline — `mkdocs` → `properdocs` and `requirements-docs.txt` + pip → `pyproject.toml` (PEP 735) + `uv`. Both executed exactly to plan; strict-build gate stayed clean across the swap; no design decisions from the original build were reopened.

## Requirements vs Outcome

Every in-scope requirement delivered; nothing dropped, nothing added. All 8 test-plan behaviors verified post-build: PEP 735 fresh install is clean, strict build exits 0 with zero warnings (including the legacy-filename INFO notice the rename was designed to eliminate), no abandonment propaganda in the output, `uv.lock` reproducible under `--frozen`, CI PR-gating and deploy path unchanged, local preview reduced to a two-line recipe, all original Phase 0 behaviors (GH-compat slugifier, footnote rendering, search, `.pages` nav order, working cross-links) preserved.

## Plan Accuracy

Plan was accurate end-to-end: 9 sequential steps, each with a concrete verification gate; no reordering, splitting, or in-flight additions needed. None of the triage branches documented in Step 5 (legacy-config-not-renamed / plugin-naming-wrong / validation-lost-in-translation) were exercised. The challenges section called its shots well — the `uv.lock` churn risk (Challenge #1) and the `setup-uv` major-version pin (Challenge #4) both translated directly into implementation decisions (inline workflow comment + `v5` pin), neither required invention at build time.

Two process details worth naming:

- **Preflight's Step 9 amendment paid for itself.** Preflight promoted four "acceptable historical" residuals (systemPatterns.md L23, .gitignore header, stale docs.yml comment, projectbrief Out-of-Scope bullet) into explicit fixes. All four were operational (present-tense claims about current CI behavior, or misleading labels post-rename), and they'd have been QA findings otherwise. This is the value of a preflight grep-sweep doing honest classification work.
- **Tech validation during plan surfaced the legacy-filename deprecation.** The plan initially read the ProperDocs announcement as "rename is optional" and classified it out-of-scope. Tech validation caught the INFO notice on every build, which turned the rename into Step 1. Doing the validation *during* plan (not deferring it to build) prevented a Preflight-stage rework of the plan.

## Build & QA Observations

Build went clean on first attempt for every step. No iteration, no debugging, no hypothesis-thrashing. The most likely-to-be-risky step on paper — Step 5's strict build against the renamed config with fresh lockfile — was clean on first run; the tech-validation-during-plan work paid off.

QA was clean too — walked seven constraints across 14 committed files, no fixes applied, no deficiencies identified. The residuals triage (memory-bank narrative mentions of `mkdocs.yml` and `requirements-docs.txt`) was the only judgment call; the plan's acceptable-residuals policy made the call trivial.

One operational note: two unrelated `docs/` edits (header renames to `rotten-green.md` and `tautology-theatre.md`) existed in the working tree when `/niko-build` was invoked. Correctly classified as operator-owned out-of-scope and left unstaged. This is the right disposition — the plan explicitly excluded `docs/` — but it's worth flagging that *detecting* those pre-existing changes required a careful `git status` read after `git add -A`; an earlier `git status --short` read would have surfaced them before staging anything.

## Insights

### Technical

- Nothing notable. The swap behaved exactly as the ProperDocs announcement claimed (mkdocs-* plugins work unchanged, config file renames work cleanly, only the CLI command changes). No surprises from either toolchain.

### Process

- **Tech validation during plan is cheaper than tech validation during build.** This is the second Phase 0 task where plan-phase tech validation (running `uv sync`, `properdocs build --strict` against a scratch venv *before* writing the plan) turned a speculative plan into a de-risked one. The original run surfaced the GH-compat slugifier divergence during build; this run surfaced the legacy-filename deprecation during plan. Both would have been noisy mid-build deviations otherwise. Pattern: for toolchain-swap tasks, budget ~10 minutes of scratch-venv tech validation inside the plan phase.
- **`git status --short` before `git add -A`.** A habit of reading `git status --short` *before* any staging step would have surfaced the two unrelated `docs/` working-tree edits before I staged them. Stash-or-triage is cheap; an accidental "all-in-one commit" is not. Not this task's problem (I caught it), but generalizable.

### Million-Dollar Question

If the Phase 0 publishing pipeline had been set up with `uv` + `pyproject.toml` + `properdocs` from day one — rather than `pip` + `requirements-docs.txt` + `mkdocs`, with this swap happening in a second task — the pipeline would have looked identical to what we have now, minus one commit. That's not a redesign; it's the observation that the rework was correct-but-retroactive. The *interesting* counterfactual is whether the original task should have adopted ProperDocs at authorship time. The answer is "probably not" — at the time of the original run, the ProperDocs announcement framed the rename as optional and didn't surface the legacy-filename deprecation INFO as a motivating reason. The rework was reasonable to defer; the cost of deferring was two small edit-and-verify cycles here, which is far less than the cost of a mid-authorship detour would have been.

More broadly, this rework reinforces a pattern already in the SLOBAC playbook: **toolchain choices are revisitable**, and preserving behavior parity under a swap is a quick, well-scoped Level 2 task when the test gate is a build-success one. The strict-mode + validation-anchors config stayed byte-identical through the swap; the gate itself became the parity proof. If a future rework wants to swap (say) `awesome-pages` for a different nav plugin, the same shape applies: preserve plan design-decisions, swap the toolchain surface, let the strict build confirm behavior parity.
