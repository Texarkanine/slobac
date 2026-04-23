# Progress — Phase 0 docs publishing (mkdocs-material to GitHub Pages)

Publish the `docs/` manifesto to GitHub Pages using mkdocs-material, built and deployed by a dedicated GitHub Actions workflow (via `actions/deploy-pages`, not a `gh-pages` branch). Include `awesome-pages` and `pymdownx.snippets` plugins. Enforce `strict` link validation at build time to defend the cross-link integrity constraint called out in `systemPatterns.md`.

**Complexity:** Level 2

## Phase Log

- Complexity analysis complete — classified Level 2 (self-contained enhancement, known recipe, no architectural decisions remaining after Option A vs B discussion).
- Plan phase complete — full Level 2 plan written to `tasks.md` (8 behaviors, 8 steps, 4 new deps, 6 challenges). Cross-link audit confirmed no `docs/` link escapes the tree; strict mode will be clean. Flagged two side-effect deliverables: new `docs/index.md` (required — no landing page today) and new root `README.md` (optional — repo has none).

- Preflight phase complete — PASS with one accretive plan amendment: added `mkdocs-redirects` plugin (dep + `mkdocs.yml` config) to pre-position URL stability for future renames. No convention violations, no conflicts, completeness precheck passed.
- Build phase complete — PASS. All 8 steps executed; `mkdocs build --strict` exits clean locally. Three mid-build deviations (GitHub-compat slugifier, explicit `validation:` block, `DISABLE_MKDOCS_2_WARNING` env var, conditional `.pages` activated for reading-order nav) all documented in `tasks.md` Build Notes. Side-effect files added per plan: `.gitignore`, minimal root `README.md`, `techContext.md` update reflecting docs toolchain.
- QA phase complete — PASS. Two trivial fixes: YAGNI trim of 9 unused `markdown_extensions` + doc update to `systemPatterns.md` acknowledging the strict-mode CI gate. Post-fix strict build remains clean. All 8 plan behaviors verified. No substantive deficiencies, no regressions.
- Reflect phase complete — `reflection/reflection-phase0-docs-publish.md` written. Two technical insights (mkdocs strict vs validation; GH vs python-markdown slug divergence), one process insight (plan-as-contract re: dep expansion), one million-dollar finding (day-1 CI gate would have caught three latent cross-link bugs shipped in initial manifesto commit). Persistent files reconciled.

## REFLECT COMPLETE (superseded — see Rework below)

Task was ready for archival at this point, then operator initiated rework.

## Rework initiated

Operator's feedback:

1. **Switch `mkdocs` → `properdocs`** per the [ProperDocs #33 discussion](https://github.com/orgs/ProperDocs/discussions/33). ProperDocs is a drop-in continuation of MkDocs 1.x by the last active MkDocs maintainer (`oprypin`); original MkDocs is abandoned and the owner plans to reuse the name for an incompatible v2 that will break every existing plugin/theme. Switching now removes that time-bomb. Per the announcement:
    - Plugins keep their `mkdocs-*` names — no renames needed.
    - Config file can stay as `mkdocs.yml` (rename to `properdocs.yml` is optional).
    - Command goes `mkdocs build` → `properdocs build`.
    - `DISABLE_MKDOCS_2_WARNING` env var likely becomes unnecessary: on `properdocs`, the abandonment warning stops firing; and on non-mkdocs forks, mkdocs-material's own Zensical warning also stops firing. Validate at build-time.
    - Note on env var rename: ProperDocs v1.6.7 changed the env var name (the old name is now `NO_MKDOCS_2_WARNING`); worth checking the release notes if the silencer is still needed for some reason.
2. **Switch `requirements-docs.txt` → `pyproject.toml` with `uv`**. Use PEP 735 `[dependency-groups]` (clean fit — this is not a publishable package, just a docs-build toolchain). Replace pip with uv both locally and in CI. Commit `uv.lock` for reproducibility.

Neither change reopens any of the design decisions settled in the original build (mkdocs-material + awesome-pages + redirects + pymdownx.snippets + GH-compat slugifier + strict-mode link validation + PR-gating + Actions deploy-pages). They are a toolchain swap.

**Complexity:** Level 2

## Rework — Phase Log

- Rework initiated. Stale ephemerals cleared (tasks.md, activeContext.md, `.preflight-status`, `.qa-validation-status`). Reflection preserved. Operator had partially pre-swapped `mkdocs → properdocs` in the working tree before invoking rework; that WIP was swept into the `chore: initiating rework on phase0-docs-publish` commit as the rework's starting state.
- Complexity re-classified: Level 2 (two self-contained infra swaps, known recipes, no architectural decisions).
- Plan phase complete — Level 2 plan in `tasks.md`. 8 behaviors, 9 steps, 5 challenges. Tech validation executed inline: uv 0.8.22 + properdocs 1.6.7 clean on current tree; properdocs 1.6.7 *does* emit a legacy-filename deprecation INFO (contradicts my earlier read of the ProperDocs announcement), so the plan now renames `mkdocs.yml` → `properdocs.yml` as Step 1. Abandonment notices confirmed absent under properdocs, validating the pre-rework drop of `DISABLE_MKDOCS_2_WARNING`.
- Preflight phase complete — PASS with Step 9 amended. Grep-sweep turned up three *operational* residuals the plan had initially classified as "acceptable historical" and one cross-doc inconsistency: (1) `systemPatterns.md` line 23's present-tense `mkdocs build --strict` claim about current CI behavior; (2) `.gitignore`'s `# mkdocs build output` header; (3) the `docs.yml` line 42 comment asserting "config file stays mkdocs.yml" (contradicts Step 1's rename); (4) `projectbrief.md`'s Rework — Out of Scope bullet saying the rename should be skipped "unless there's a motivating reason" (superseded — Step 1 renames with the legacy-filename deprecation INFO as the motivating reason). All four are promoted to explicit fixes in Step 9. No convention violations, no implementation conflicts, no missing dependency-impact edges, no completeness gaps.
- Build phase complete — PASS. All 9 plan steps executed in order; no deviations, no triage branches. `mkdocs.yml` → `properdocs.yml` (rename, content byte-identical), `pyproject.toml` created with PEP 735 `[dependency-groups] docs` + minimal `[project]` stub, `uv.lock` generated (35 packages, committed), `requirements-docs.txt` deleted, workflow swapped to setup-uv@v5 + `uv sync --frozen` + `uv run properdocs build --strict`, README local-preview rewritten to two-line uv idiom, `techContext.md` updated, and all four preflight-amended operational stragglers fixed (`systemPatterns.md` present-tense claim, `.gitignore` header comment, stale `docs.yml` comment, superseded `projectbrief.md` Out-of-Scope bullet). Post-edit strict build re-ran clean (exit 0, zero warnings, no legacy-filename notice, no abandonment propaganda); `uv sync --group docs --frozen` idempotent. Behavior parity with pre-rework tree confirmed.
- QA phase complete — PASS. Clean — no fixes applied. Walked the seven semantic constraints (KISS, DRY, YAGNI, Completeness, Regression, Integrity, Documentation) across the 14 committed files; all eight test-plan behaviors verified; all residual `mkdocs` / `requirements-docs.txt` references classified as memory-bank historical narrative or literal package names (acceptable per plan Step 9). No operational path references either. Two unstaged docs/ edits in the working tree are operator-owned, out-of-scope, and deliberately excluded from the build commit.

## Operator Handoff Items (deferred to post-merge)

- **GitHub Pages source toggle**: repo Settings → Pages → Build and deployment → Source must be set to "GitHub Actions". Workflow cannot set this itself. Without it, `deploy:` job fails; `build:` still succeeds so PR-gating still works.
