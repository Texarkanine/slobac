---
task_id: phase0-docs-publish-rework
complexity_level: 2
date: 2026-04-23
status: completed
---

# TASK ARCHIVE: Phase 0 docs publishing rework (ProperDocs + uv)

## SUMMARY

After the initial Phase 0 “manifesto to GitHub Pages” pipeline was completed and reflected on, a **rework** swapped the docs-build **tooling only**—no design reversals: same plugins, theme, strict/validation config, GH-compatible slugifier, PR-gating, and `actions/deploy-pages` path.

Two mechanical substitutions: **MkDocs → ProperDocs** (CLI + `properdocs.yml` config name to drop the legacy-filename build INFO) and **pip + `requirements-docs.txt` → uv + `pyproject.toml` (PEP 735 `[dependency-groups] docs`) + committed `uv.lock`**. CI uses `astral-sh/setup-uv@v5`, `uv sync --group docs --frozen`, and `uv run properdocs build --strict`. All nine plan steps executed on first try; Build and QA both clean; no deviations from the written plan.

## REQUIREMENTS

- Keep shipped site behavior equivalent to the pre-rework tree (strict build as the gate).
- Preserve: awesome-pages, redirects, pymdownx, Material theme, slugifier, `validation:` + `strict`, PR `build` gate, `main` deploy.
- Use ProperDocs; rename config to `properdocs.yml` ( motivated by per-build legacy-filename INFO in properdocs 1.6.7).
- Use uv for local and CI; lockfile reproducible with `--frozen`.
- Update `README`, `techContext`, and operational stragglers in `systemPatterns`, `projectbrief`, `.gitignore`, workflow (per preflight).

## IMPLEMENTATION

| Area | Change |
|------|--------|
| Config | `mkdocs.yml` → `properdocs.yml` (rename, identical content) |
| Deps | `pyproject.toml` — minimal `[project]` stub, `[dependency-groups] docs`, `[tool.uv] required-version >= 0.5`; `requirements-docs.txt` removed; `uv.lock` committed |
| CI | `.github/workflows/docs.yaml`— `setup-uv`, `uv sync --group docs --frozen`, `uv run properdocs build --strict` |
| Docs for humans | `README` local preview two-liner; `techContext` env + build-tool lines |
| Integrity docs | `systemPatterns` CI line → `properdocs build --strict`; `.gitignore` comment; `projectbrief` rework out-of-scope note updated |
| Niko ephemerals | `tasks` Build/QA/Reflect notes; `reflection-phase0-docs-publish-rework` (inlined below) |

Post-merge: GitHub **Settings → Pages** must use **GitHub Actions** as source (operator handoff; workflow cannot set it).

## TESTING

- `uv run properdocs build --strict` — exit 0, no warnings, no legacy-filename INFO, no abandonment “switch to X” notices; full `docs/` tree built.
- `uv sync --group docs --frozen` idempotent.
- Niko **QA** phase: seven constraints (KISS, DRY, YAGNI, Completeness, Regression, Integrity, Documentation) — **PASS**, no code fixes.

## LESSONS LEARNED

*Inlined from `reflection-phase0-docs-publish-rework`.*

**Technical:** Nothing novel from the swap itself; behavior matched the ProperDocs announcement (mkdocs-* plugin names unchanged; CLI-only change).

**Process (high value):**

- **Tech validation during plan (scratch venv) is cheaper than during build.** Plan-phase runs of `uv sync` and `properdocs build --strict` caught the **legacy-filename INFO** and moved **rename to `properdocs.yml`** from “optional / out of scope” into Step 1—avoiding a plan rewrite at preflight.
- **Preflight grep with honest “operational vs historical” classification** caught four stragglers (e.g. present-tense `mkdocs build` in `systemPatterns`, stale workflow comment, `projectbrief` out-of-scope bullet) that would have been QA noise if left for later.
- **Toolchain swaps** stay well-scoped when the **test gate** is a single strict build; config stayed byte-equivalent in semantics so parity was the build itself.

**Million-dollar (reflection):** If the repo had used uv + properdocs from day one, the end state would look like today with one fewer pass—acceptable deferred rework. Broader point: **strict + validation-anchors** stayed identical across the swap, so the gate was the parity proof.

**Operational note:** Unrelated `docs/` edits in the worktree (e.g. taxonomy H1 tweaks) are easy to catch with `git status --short` *before* `git add -A`.

## PROCESS IMPROVEMENTS

- For future **toolchain-swap** tasks, budget a short **plan-phase** scratch-venv validation.
- Habit: **`git status` before wide staging** when multiple concurrent edits are possible.

## TECHNICAL IMPROVEMENTS

- Optional: `tool.uv.package = false` if a `[build-system]` is ever added; without one, current uv does not install the root project (docs-only stub `[project]`). Not required for the rework outcome.

## NEXT STEPS

- **None** for this task. (Ongoing: ensure GitHub Pages source is GitHub Actions when using this workflow.)

## RELATED: Prior reflection (initial Phase 0 publish, same session)

*The file `memory-bank/active/reflection/reflection-phase0-docs-publish.md` is deleted in this archive step; a condensed account follows.*

The **first** Phase 0 task added mkdocs-material + GitHub Actions + `actions/deploy-pages`, `mkdocs-redirects` (preflight amendment), GitHub-compatible **`pymdownx.slugs.slugify`**, and explicit **`validation.anchors: warn`** alongside `strict: true` (strict alone does not fail on missing anchors by default in older mkdocs). QA trimmed over-expanded `markdown_extensions` and aligned `systemPatterns` with the new CI gate. A key technical takeaway: **strict mode and comprehensive link/anchor validation are not the same**—both configs are needed. Another: **GitHub vs default python-markdown slugs** differ; matching GitHub in mkdocs material preserves “reads the same on github.com and the site.” Process: **plan-as-contract**—do not grow dependency/extension lists without amending the plan.
