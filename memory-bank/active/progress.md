# Progress — Phase 0 docs publishing (mkdocs-material to GitHub Pages)

Publish the `docs/` manifesto to GitHub Pages using mkdocs-material, built and deployed by a dedicated GitHub Actions workflow (via `actions/deploy-pages`, not a `gh-pages` branch). Include `awesome-pages` and `pymdownx.snippets` plugins. Enforce `strict` link validation at build time to defend the cross-link integrity constraint called out in `systemPatterns.md`.

**Complexity:** Level 2

## Phase Log

- Complexity analysis complete — classified Level 2 (self-contained enhancement, known recipe, no architectural decisions remaining after Option A vs B discussion).
- Plan phase complete — full Level 2 plan written to `tasks.md` (8 behaviors, 8 steps, 4 new deps, 6 challenges). Cross-link audit confirmed no `docs/` link escapes the tree; strict mode will be clean. Flagged two side-effect deliverables: new `docs/index.md` (required — no landing page today) and new root `README.md` (optional — repo has none).

- Preflight phase complete — PASS with one accretive plan amendment: added `mkdocs-redirects` plugin (dep + `mkdocs.yml` config) to pre-position URL stability for future renames. No convention violations, no conflicts, completeness precheck passed.

## Operator Handoff Items (deferred to post-merge)

- **GitHub Pages source toggle**: repo Settings → Pages → Build and deployment → Source must be set to "GitHub Actions". Workflow cannot set this itself. Without it, `deploy:` job fails; `build:` still succeeds so PR-gating still works.
