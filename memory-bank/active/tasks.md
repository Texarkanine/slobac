# Task: Phase 0 docs publishing — rework (properdocs + uv/pyproject.toml)

* Task ID: phase0-docs-publish (rework)
* Complexity: Level 2
* Type: Simple Enhancement (toolchain swap on existing infrastructure)

Swap the docs-build toolchain on the already-shipped Phase 0 pipeline. Two independent substitutions, neither of which reopens any of the design decisions settled in the original run (plugins, theme, slugifier, strict-mode gate, PR-gating, deploy path are unchanged):

1. **`mkdocs` → `properdocs`** (a drop-in continuation of MkDocs 1.x maintained by `oprypin` — the last active pre-abandonment MkDocs maintainer). Config file renames to `properdocs.yml`, command becomes `properdocs build`, plugins retain `mkdocs-*` names.
2. **`requirements-docs.txt` + pip → `pyproject.toml` + `uv`**. Declare docs-build deps under PEP 735 `[dependency-groups]`. Local preview and CI both use `uv sync --group docs` + `uv run properdocs …`. Commit `uv.lock`.

Both swaps are purely mechanical; the shipped site behavior (plugins, slugifier, `--strict` validation, PR gating, `actions/deploy-pages`) is preserved byte-for-byte.

## Test Plan (TDD)

### Behaviors to Verify

- **PEP 735 install is clean from a fresh checkout**: in a freshly-cloned working tree with no existing venv, `uv sync --group docs` exits 0 and materializes the five expected packages (`properdocs`, `mkdocs-material`, `mkdocs-awesome-pages-plugin`, `mkdocs-redirects`, `pymdown-extensions`) plus their transitives.
- **Strict build is clean**: `uv run properdocs build --strict` against the current `docs/` tree exits 0 with **zero** warnings — including the "config file should be renamed" INFO notice, which must be gone post-rename.
- **No abandonment propaganda**: build output contains no "switch to ProperDocs" notice (original MkDocs warning) and no "switch to Zensical" notice (mkdocs-material warning). Validated during plan's tech-validation run. This justifies dropping `DISABLE_MKDOCS_2_WARNING` from the workflow (already dropped in the pre-rework WIP commit).
- **Lockfile reproducibility**: `uv.lock` is present at repo root, committed, and `uv sync --group docs --frozen` in CI succeeds against it without modification.
- **CI PR-gating unchanged**: a PR that breaks a cross-link in `docs/` still fails the `build` job (deploy job skipped on PRs). Strict-mode gate is preserved across the toolchain swap.
- **CI deploy unchanged**: a push to `main` still deploys via `actions/deploy-pages@v4` with `page_url` populated.
- **Local preview still one-shot**: `uv sync --group docs && uv run properdocs serve` is the complete local-preview recipe — no pip, no manual venv activation.
- **All original Phase 0 behaviors preserved**: every behavior from the original task (nav order from `.pages`, GH-compat slugifier, footnote rendering, search working, published site navigable) still holds after the swap. Strict-mode equivalence on the same `docs/` tree is the gate.

### Edge Cases

- **`pyproject.toml` without `[project]`**: PEP 735 allows `[dependency-groups]` as a top-level table without a `[project]` section. Some tools balk. uv does not (verified in tech validation: `uv 0.8.22` installed). Keep the file minimal — no `[project]` section — since SLOBAC is not a publishable package. This also avoids confusion about "what package is this, and is it on PyPI?"
- **Transitional `mkdocs.yml` filename**: after `git mv mkdocs.yml properdocs.yml`, verify no stale references in the workflow (it doesn't reference the filename explicitly — properdocs auto-discovers), in `README.md`, or in memory-bank docs. There is one reference to fix in `techContext.md`.
- **uv.lock cross-platform**: CI and local both run Linux. If a non-Linux contributor ever shows up, they'd regenerate the lock. Out of scope for Phase 0.
- **uv cache key in CI**: `astral-sh/setup-uv` should key on `pyproject.toml` + `uv.lock`. Its default behavior already does this when `enable-cache: true`. No custom key needed.
- **Plugin naming**: the announcement promised mkdocs-* plugins stay named mkdocs-*. Verified against our four plugins: `mkdocs-material`, `mkdocs-awesome-pages-plugin`, `mkdocs-redirects`, `pymdown-extensions`. All resolve unchanged against PyPI.

### Test Infrastructure

- Same as original run: no code tests; verification is **build-success testing** via `properdocs build --strict` (locally + in CI). The strict-mode gate is the "test" — a broken link or a leftover `mkdocs`-era config path fails the build.

## Implementation Plan

Linear and ordered. Each step is a discrete edit-and-verify cycle. Steps 1–4 are local; Step 5 is the local build proof; Steps 6–8 are the CI and docs updates; Step 9 is final housekeeping.

1. **Rename `mkdocs.yml` → `properdocs.yml`** via `git mv`, no content changes.
    - Files: `mkdocs.yml` → `properdocs.yml` (rename only).
    - Why: properdocs 1.6.7 emits an INFO-level deprecation notice on every build when the legacy filename is used ("Support for using this legacy file name as a fallback will eventually be removed"). Renaming makes the notice go away today and pre-positions us against the future removal. Cost is one rename.
    - Verification: `git status` shows rename (not delete+add), `properdocs build --strict` in the pre-existing validation venv no longer prints the notice. (Validation deferred to Step 5 where it's done as part of the proper build.)

2. **Create `pyproject.toml` at repo root** declaring docs-build dependencies via PEP 735.
    - Files: `pyproject.toml` (new).
    - Shape: no `[project]` table (this is not a publishable package). A top-level `[dependency-groups]` table with one group, `docs`, listing the five deps from the current `requirements-docs.txt`. Optionally add `[tool.uv]` with `required-version = ">=0.5"` to declare the uv floor explicitly. A top-level `requires-python = ">=3.10"` under a minimal `[project]` stub *would* give uv a Python version to resolve against — so one of:
        - (a) add a minimal `[project]` with just `name`, `version`, and `requires-python`;
        - (b) skip `[project]` and rely on uv's default Python discovery.
    - **Decision**: take (a) — a minimal `[project]` with `name = "slobac-docs"`, `version = "0"`, `requires-python = ">=3.10"`, and `description = "Docs-build toolchain for the SLOBAC manifesto (not a published package)."`. This is the idiomatic uv project shape and makes `uv sync` behavior unambiguous about which Python to pick. Cost is negligible; benefit is future contributors not guessing.
    - Dependencies under `[dependency-groups] docs = [...]` with the same `~=` pins as the current `requirements-docs.txt`: `properdocs~=1.6`, `mkdocs-material~=9.5`, `mkdocs-awesome-pages-plugin~=2.9`, `mkdocs-redirects~=1.2`, `pymdown-extensions~=10.7`.
    - Header comment in the file should explain: (i) this repo ships the SLOBAC manifesto, not a Python package; (ii) the docs group is the Phase 0 publishing toolchain; (iii) runtime deps for Phase 1+ will land in a separate group or structure when there's actual runtime code.

3. **Delete `requirements-docs.txt`**.
    - Files: `requirements-docs.txt` (delete).
    - Check: grep the repo for any lingering reference to `requirements-docs.txt` and excise. Known references at plan time: `.github/workflows/docs.yml` (the `cache-dependency-path` and the `pip install -r` step) and `README.md` (local preview block). Both are rewritten in Steps 6 and 7 respectively. `techContext.md` also mentions it indirectly — Step 8.

4. **Generate and commit `uv.lock`** by running `uv sync --group docs` locally.
    - Files: `uv.lock` (new, auto-generated).
    - After this, `.venv/` exists locally. `.gitignore` already ignores `.venv/` from the original run; re-verify.
    - Verification: `uv sync --group docs --frozen` re-runs and is idempotent (no lock mutation).

5. **Local strict build proof**: run `uv run properdocs build --strict` in the just-synced venv.
    - Files: none modified (the `site/` artifact is gitignored).
    - Gate to proceed: exit 0, zero warnings, output does not contain the "should be renamed to 'properdocs.yml'" notice, output does not contain any abandonment-notice strings. All 16 docs pages present in `site/`.
    - If something fails here, triage: legacy config path not renamed → fix Step 1; plugin naming wrong in `pyproject.toml` → fix Step 2; validation config lost in translation → should be impossible since `properdocs.yml` is a rename of `mkdocs.yml` with identical contents.

6. **Update `.github/workflows/docs.yml`** — swap Python+pip for uv.
    - Files: `.github/workflows/docs.yml` (modify).
    - Remove: the `actions/setup-python@v5` step; the `pip install -r requirements-docs.txt` step; the `cache-dependency-path: requirements-docs.txt` input.
    - Add: `astral-sh/setup-uv@v5` (pin to v5 — current stable major; v6 at plan time is minor enough we can bump later if needed) with `enable-cache: true` — it auto-keys on `uv.lock` and `pyproject.toml`. No explicit Python step needed; uv auto-provisions per `requires-python`.
    - Add: `uv sync --group docs --frozen` step. `--frozen` makes CI fail if `uv.lock` is out of date vs `pyproject.toml`, which is the desired gate (lock drift must be a PR-reviewable change, not a silent CI-time regeneration).
    - Update: `Build site (strict)` step runs `uv run properdocs build --strict` (already says `properdocs build --strict` — add the `uv run` prefix).
    - Unchanged: triggers, permissions, concurrency, env block (already emptied in pre-rework WIP), upload-pages-artifact, deploy job.

7. **Update `README.md`** — local preview instructions.
    - Files: `README.md` (modify).
    - Current block (post-WIP) uses `python -m venv .venv-docs` + `pip install -r requirements-docs.txt` + `properdocs serve`. Rewrite to the uv idiom: `uv sync --group docs` + `uv run properdocs serve`. Drop the `source .venv-docs/bin/activate` line — `uv run` handles activation implicitly and is the idiomatic uv local-preview command.
    - Also: check for any `requirements-docs.txt` string elsewhere in `README.md`; none expected but grep.

8. **Update `memory-bank/techContext.md`** — reflect the toolchain swap in persistent project context.
    - Files: `memory-bank/techContext.md` (modify).
    - Current state (post-WIP): already references "ProperDocs ... with the `mkdocs-material` theme". Needs two more edits:
        - Environment Setup section — replace `pip install -r requirements-docs.txt` with `uv sync --group docs` + `uv run properdocs serve`. Replace the Python version claim ("Python 3.10+ with pip…") with "`uv` (which auto-provisions Python per `pyproject.toml`)".
        - Build Tools section — rewrite the dependency-declaration line from "Dependencies are declared in `requirements-docs.txt`" to "Dependencies are declared in `pyproject.toml` under the PEP 735 `[dependency-groups] docs` group; `uv.lock` pins them for reproducibility."
    - The rest of that section (CI gate, plugin list, why strict, etc.) is unchanged — the swap does not change any of it.

9. **Grep-sweep for stragglers**: search the repo (excluding `docs/`, `memory-bank/archive/`, `planning/`, `.git/`, `.venv*/`, `site/`, and any markdown authored prior to the original task) for residual references to `mkdocs` (lowercase, command form) and `requirements-docs.txt`.
    - Files: none modified unless the grep turns something up.
    - Known operational fixes (surfaced by preflight grep-sweep — fix these in this step, don't leave them as "acceptable residuals"):
        - `memory-bank/systemPatterns.md` line 23: the sentence "CI runs `mkdocs build --strict` with `validation.anchors: warn`…" is a *present-tense operational* claim about how the CI gate currently works — not a historical log. Update `mkdocs build --strict` → `properdocs build --strict` here.
        - `.gitignore` line 1 comment `# mkdocs build output` labels the `/site/` ignore. The path is unchanged but the label is stale. Update to `# properdocs build output` (or drop the comment — `/site/` is self-explanatory).
        - `.github/workflows/docs.yml` line 42 comment `# properdocs is a drop-in for mkdocs build; config file stays mkdocs.yml.` becomes misleading after Step 1's rename. Either drop the comment (the step name + command make intent clear) or rewrite it to reflect the new filename. Step 6's workflow rewrite should handle this inline.
        - `memory-bank/active/projectbrief.md` Rework — Out of Scope line ("Renaming `mkdocs.yml` to `properdocs.yml` — explicitly optional per the announcement; skip unless there's a motivating reason.") is now superseded — the motivating reason (legacy-filename deprecation INFO) emerged during plan's tech validation and Step 1 renames. Update the bullet to reflect the decision, or move it into scope.
    - Acceptable residuals (truly historical — leave as-is): reflection doc (`memory-bank/active/reflection/reflection-phase0-docs-publish.md`); progress log entries prior to the rework; the README history section (if it mentions the original approach). These are logs of what was true at write time.
    - Unacceptable residuals: any *operational* path (CI, install, run, preview, lint, hooks) still referencing `mkdocs` as a command or `requirements-docs.txt` as a file. Fix in place.

## Challenges

1. **`uv.lock` churn risk in future PRs.** A contributor bumps a dep without running `uv sync` → `pyproject.toml` and `uv.lock` disagree → CI's `--frozen` fails the build. This is *desired* behavior, but must be obvious to readers. Mitigation: one-line comment in the workflow next to `uv sync --group docs --frozen` explaining "if this fails, run `uv sync --group docs` locally and commit the updated `uv.lock`." Cheap, saves a debugging round-trip.

2. **Renaming `mkdocs.yml` → `properdocs.yml` while the git history still references the old name.** Any stored link in e.g. reflection docs, progress logs, or `systemPatterns.md` pointing at `mkdocs.yml` becomes a stale historical reference. Mitigation: accept staleness in *historical* docs (they're a log of what was true at write time) — fix only *operational* references. This maps to Step 9's "acceptable residuals" list.

3. **Behavior parity on the GH-compat slugifier.** `properdocs` is a fork of MkDocs 1.x at the point before abandonment. It consumes `pymdownx.slugs.slugify` identically. Low risk, but the consequences of a silent slug regression would be every cross-reference anchor breaking on the published site. Mitigation: Step 5's strict build doubles as the parity test — the same `docs/` tree that was clean on mkdocs must stay clean on properdocs.

4. **setup-uv major-version bump.** `astral-sh/setup-uv` moves fast; `v5` is stable and widely used; `v6` is current at plan time. Cost of a miss: CI breaks on some obscure input rename. Mitigation: pin to `v5` for this task, leave `v6` adoption to a later maintenance pass. Rationale: minimize scope creep.

5. **PEP 735 is still newish.** Any tooling downstream of uv (IDE integrations, pre-commit, dependabot) may not parse `[dependency-groups]` yet. Mitigation: none needed for Phase 0 — the only consumer in this repo is uv itself. If Dependabot for Python ever gets wired up and can't read the group, that's a future task, not a Phase 0 blocker.

## Technology Validation (done during plan)

The de-risking checkpoints below were executed in the working tree before writing this plan; their outcomes inform Steps 1–5:

- [x] `uv --version` → `uv 0.8.22`. PEP 735 landed in uv 0.5.0, so `[dependency-groups]` is well-supported.
- [x] `uv pip install` of the five pinned deps against a scratch venv succeeds — no dep-resolution conflicts under properdocs 1.6.7.
- [x] `properdocs build --strict` against the current `docs/` + `mkdocs.yml` exits 0. This proves behavior parity with mkdocs is already achieved — renaming the config file is a cosmetic finish.
- [x] `properdocs build` output includes the legacy-filename deprecation INFO notice today. Step 1 eliminates it.
- [x] `properdocs build` output does NOT include any abandonment-switch-to-X notice. Confirms the original `DISABLE_MKDOCS_2_WARNING` env var was correctly dropped in the pre-rework WIP.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete (done inline; see section above)
- [x] Preflight
- [x] Build
- [ ] QA
- [ ] Reflect

## Build Notes

All nine plan steps executed in order, no deviations. Each step's gate was satisfied on first try; no in-plan triage branches were taken.

- **Step 1** — `git mv mkdocs.yml properdocs.yml`. `git status` confirms rename (not delete+add). Content unchanged.
- **Step 2** — `pyproject.toml` created with the decided (a) shape: minimal `[project]` stub + `[dependency-groups] docs` + `[tool.uv] required-version = ">=0.5"`.
- **Step 3** — `requirements-docs.txt` deleted. Confirmed no operational references remain (README, workflow, techContext all rewritten in later steps).
- **Step 4** — `uv sync --group docs` generated `uv.lock` (54 KB). All five declared top-level deps resolved: `properdocs 1.6.7`, `mkdocs-material 9.7.0`, `mkdocs-awesome-pages-plugin 2.10.1`, `mkdocs-redirects 1.2.3`, `pymdown-extensions 10.21.2`, plus 30 transitives. `uv sync --group docs --frozen` idempotent: "Audited 35 packages".
- **Step 5** — `uv run properdocs build --strict` exits 0, zero warnings. Legacy-filename INFO notice absent (Step 1 eliminated it). No "switch to ProperDocs" or "switch to Zensical" notices. Site has 20 content pages + 404.html; all 20 manifesto markdown files built.
- **Step 6** — Workflow rewritten: `actions/setup-python@v5` + pip steps removed; `astral-sh/setup-uv@v5` with `enable-cache: true` added; `uv sync --group docs --frozen` replaces install; `uv run properdocs build --strict` replaces bare command. Stale "config file stays mkdocs.yml" comment removed inline. All other workflow structure (triggers, permissions, concurrency, PR-gating, deploy job) unchanged.
- **Step 7** — README local-preview block rewritten to the uv idiom (two lines: `uv sync --group docs` + `uv run properdocs serve`). Drops explicit venv creation/activation.
- **Step 8** — `techContext.md` Environment Setup and Build Tools sections rewritten for the uv/PEP 735 shape.
- **Step 9** — Grep-sweep done. All four preflight-amended operational residuals fixed:
    - `systemPatterns.md` line 23: `mkdocs build --strict` → `properdocs build --strict`.
    - `.gitignore` line 1: `# mkdocs build output` → `# properdocs build output`.
    - `.github/workflows/docs.yml` stale comment: removed (absorbed into Step 6's rewrite).
    - `projectbrief.md` Rework — Out of Scope bullet: superseded bullet replaced with a note explaining *why* the rename moved into scope.
- Remaining `mkdocs` references across the repo are all either (a) literal package/theme names that keep `mkdocs-*` naming (per the ProperDocs announcement: `mkdocs-material`, `mkdocs-awesome-pages-plugin`, etc.), (b) auto-generated `uv.lock` entries, or (c) historical narrative in memory-bank/active/ rework logs. None are operational paths — classification matches plan Step 9's acceptable-residuals policy.

Post-all-edits, strict build re-ran clean: exit 0, zero warnings, no propaganda notices. Behavior parity with pre-rework tree confirmed.
