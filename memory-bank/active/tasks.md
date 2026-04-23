# Task: Phase 0 docs publishing — mkdocs-material to GitHub Pages

* Task ID: phase0-docs-publish
* Complexity: Level 2
* Type: Simple Enhancement (infrastructure / docs scaffolding)

Publish the `docs/` manifesto to GitHub Pages using **mkdocs-material**, built and deployed by a dedicated GitHub Actions workflow via `actions/deploy-pages` (no `gh-pages` branch). Include the `awesome-pages` plugin (nav without stuffing `mkdocs.yml`) and `pymdownx.snippets` (inline source files). Enforce `--strict` at build time so broken cross-links / missing anchors fail CI — the load-bearing integrity gate named in `memory-bank/systemPatterns.md`.

## Test Plan (TDD)

### Behaviors to Verify

- **Build is strict-clean**: running `mkdocs build --strict` locally against the current `docs/` tree → exit 0, no warnings about unrecognized links, missing anchors, or broken `.pages` references.
- **All Phase-0 content is published**: the built `site/` directory contains HTML pages for `index.md`, `principles.md`, `glossary.md`, `workflows.md`, and every `taxonomy/*.md` file (16 files: 15 entries + `taxonomy/README.md` → `taxonomy/index.html`).
- **Navigation exposes the four sections**: the rendered top-level nav shows Home, Principles, Taxonomy (with sub-nav of the 15 entries), Glossary, Workflows — i.e., the sections articulated in `planning/VISION.md` §1.1.
- **Cross-links resolve**: clicking any `../principles.md#anchor` or `../glossary.md#anchor` from any taxonomy entry lands on the correct rendered anchor. (Strict mode proves this at build time.)
- **Footnotes render**: `[^footnote]` syntax in `docs/principles.md`, `docs/glossary.md`, `docs/workflows.md`, `docs/taxonomy/README.md`, `docs/taxonomy/semantic-redundancy.md`, `docs/taxonomy/pseudo-tested.md`, `docs/taxonomy/shared-state.md`, `docs/taxonomy/mystery-guest.md` renders as footnote blocks with backrefs.
- **Search works**: mkdocs-material's built-in search indexes and returns hits for known taxonomy terms (e.g. "tautology", "pseudo-tested").
- **PR builds gate link validity**: on a pull request, the workflow runs `mkdocs build --strict` and does not deploy — a PR that breaks a cross-link fails CI.
- **Push-to-main deploys**: on push to `main`, the workflow builds and deploys to GitHub Pages via `actions/deploy-pages`; the `page_url` output is populated and reachable.

### Edge Cases

- **No link exits `docs/`**: confirmed by audit — every `../` link in `docs/` resolves within `docs/`. If any link later gets added that points to `../planning/` or `../README.md`, strict mode will catch it and force the author to convert to an absolute `https://github.com/...` URL. This is desired behavior, not a regression.
- **`taxonomy/README.md` → `taxonomy/index.html`**: mkdocs-material + awesome-pages treats `README.md` in a subdir as the section index. Intra-tree links like `[../principles.md](../principles.md)` from `taxonomy/README.md` must still resolve after this rewrite. (Verified during local build.)
- **Footnote definitions referenced across sections**: each footnote defined in a file is used only in that file; no cross-file footnote refs (confirmed — `pymdownx.footnotes` handles this fine).
- **`pymdownx.snippets` with `check_paths: true`**: no `--8<--` includes exist in `docs/` today, so this is inert for Phase 0 but correctly configured for later use from Phase 1+.

### Test Infrastructure

- **Framework**: none pre-existing. There is no code to test (project is Markdown-only per `techContext.md`). Verification for this task is **build-success testing**: `mkdocs build --strict` locally + GitHub Actions workflow success.
- **Test location**: N/A. Validation happens in the `build:` job of the Actions workflow and via the local build command.
- **Conventions**: N/A.
- **New test files**: none. The strictness gate is `mkdocs build --strict` in the workflow itself — that's the "test".

## Implementation Plan

Linear and ordered. Each step is a discrete edit-and-verify cycle.

1. **Create `requirements-docs.txt` at repo root** — scoped to docs-build deps so future runtime deps (Phase 1+) live in their own file.
   - Files: `requirements-docs.txt` (new)
   - Contents: `mkdocs`, `mkdocs-material`, `mkdocs-awesome-pages-plugin`, `pymdown-extensions` (provides `pymdownx.snippets`, `pymdownx.superfences`, etc.; `footnotes` ships with base `python-markdown`).
   - Pin to loose-compatible ranges (`~=` on major.minor) for reproducibility without locking out security patches.

2. **Create `docs/index.md`** — the site landing page. Previously a Phase-0 gap: no root README, no existing site index.
   - Files: `docs/index.md` (new)
   - Content: minimal (≈40 lines). One-paragraph framing of what the manifesto is (seeded from `planning/VISION.md` §1.1, rephrased to address the reader of the *site* rather than a project-planning audience). Then a "How to read" section with links to the four top-level docs in recommended order: Principles → Workflows → Taxonomy (with pointer to `taxonomy/README.md` as the curated reading order) → Glossary. No new claims about SLOBAC; this is navigation prose only.
   - Check: existing content in `docs/` should NOT be edited as part of this step; index is additive.

3. **Create `mkdocs.yml` at repo root** — the site configuration.
   - Files: `mkdocs.yml` (new)
   - Site metadata: `site_name: SLOBAC — Suite-Life Of Bobs And Code`, `site_description`, `site_url` (GitHub Pages URL pattern: `https://<user>.github.io/<repo>/`), `repo_url`, `repo_name`, `edit_uri: edit/main/docs/`.
   - `docs_dir: docs`, `site_dir: site` (default, but explicit).
   - `theme: name: material` with: palette with light/dark toggle, navigation features (`navigation.instant`, `navigation.tracking`, `navigation.sections`, `navigation.top`, `toc.follow`), `search.suggest`, `search.highlight`, `content.code.copy`.
   - `plugins:` `search`, `awesome-pages`.
   - `markdown_extensions:` `admonition`, `attr_list`, `md_in_html`, `tables`, `toc` with `permalink: true`, `footnotes`, `pymdownx.details`, `pymdownx.superfences` with mermaid fence format, `pymdownx.tabbed` (arguable for now — include for parity with future entries), `pymdownx.tasklist`, `pymdownx.snippets` with `base_path: ["."]` and `check_paths: true`, `pymdownx.emoji` (material icons), `pymdownx.highlight` with `anchor_linenums: true`.
   - `strict: true` — fails build on broken links, missing anchors, etc. This is the integrity gate.

4. **Local dry-run validate** — install deps in a scratch venv and run `mkdocs build --strict`.
   - Files: none modified; this is a verification step.
   - Expected outcome: clean build. If warnings/errors surface (e.g. link-to-anchor mismatches I didn't catch in the audit), triage:
     - If it's a real broken link → fix the source markdown.
     - If it's a plugin misconfiguration → fix `mkdocs.yml`.
     - If it's a `pymdownx.snippets` path issue → adjust `base_path`.
   - Gate to proceed: `mkdocs build --strict` exits 0.

5. **(Optional, add only if nav ordering is wrong after Step 4)** — add `.pages` files for awesome-pages nav control.
   - Files: `docs/.pages` (maybe), `docs/taxonomy/.pages` (maybe).
   - `docs/.pages` would pin top-level order: `index.md`, `principles.md`, `workflows.md`, `taxonomy`, `glossary.md`.
   - `docs/taxonomy/.pages` would pin entry order (alphabetical by default, which is reasonable; skip unless there's a motivating reason).
   - Defer until Step 4 tells us whether default ordering is acceptable.

6. **Create `.github/workflows/docs.yml`** — the build + deploy pipeline.
   - Files: `.github/workflows/docs.yml` (new)
   - Triggers: `push: branches: [main]`, `pull_request:` (for link-validation gating), `workflow_dispatch:`.
   - Concurrency group `pages` with `cancel-in-progress: false` (production deploys complete).
   - Permissions: `contents: read`, `pages: write`, `id-token: write` (no `contents: write` — we don't push to `gh-pages`).
   - `build:` job (runs on all triggers): checkout (no LFS, no fetch-depth 0), setup-python, pip install `-r requirements-docs.txt`, `mkdocs build --strict`, upload pages artifact.
   - `deploy:` job (skipped on pull_request via `if: github.event_name != 'pull_request'`): needs `build`, environment `github-pages`, `actions/deploy-pages@v4`.
   - Drop from reference workflow: Ruby/Bundler, ImageMagick, mermaid-cli + AppArmor workaround (mkdocs-material renders mermaid client-side), LFS, fetch-depth, LINKCARD env vars, `peaceiris/actions-gh-pages`.

7. **Add a minimal root `README.md`** — not technically required to ship Phase 0, but the repo lacks one entirely and GitHub renders it as the repo landing page. A one-screen README pointing at the published site + the memory-bank setup is a net-positive side effect of this task.
   - Files: `README.md` (new, at repo root)
   - Content: name, one-paragraph pitch (reuse from VISION §1), link to the published docs URL once known, link to `planning/VISION.md` for project context, pointer to `.cursor/rules/` for contributor workflow.
   - Scope check: if this starts feeling like it needs real design, defer it out of this task.

8. **Document operator setup step** — the repo Settings → Pages source must be set to "GitHub Actions" (not "Deploy from a branch"). The workflow cannot set this itself.
   - Files: none modified in-repo. Record in `memory-bank/active/progress.md` as a manual handoff item for the operator. Also mention in the PR description.

## Technology Validation

New dependencies introduced:

- **Python + pip** (workflow-side only — no local Python runtime requirement in `techContext.md` yet; this task adds one for contributors who want to preview the site).
- **mkdocs** (core), **mkdocs-material** (theme), **mkdocs-awesome-pages-plugin** (nav), **pymdown-extensions** (snippets + extras).

Validation plan (executed in Step 4 of the implementation plan above):

1. Create scratch venv: `python -m venv .venv-docs && source .venv-docs/bin/activate`.
2. `pip install -r requirements-docs.txt`.
3. `mkdocs build --strict`.
4. Spot-check `site/index.html` exists, `site/taxonomy/deliverable-fossils/index.html` exists, search index is present in `site/search/search_index.json`.
5. If everything passes, the technology stack is validated. Deactivate and gitignore the venv (add `.venv-docs/` and `site/` to `.gitignore`).

No runtime validation required for `actions/deploy-pages` — it's a first-party GitHub action in active use, and the branch protection / Pages settings are confirmable via repo settings.

## Dependencies

- `mkdocs ~= 1.6`
- `mkdocs-material ~= 9.5`
- `mkdocs-awesome-pages-plugin ~= 2.9`
- `pymdown-extensions ~= 10.7`

(Exact versions pinned when `requirements-docs.txt` is authored; these are anchor ranges, not gospel.)

## Challenges & Mitigations

- **Challenge**: `strict: true` surfaces latent broken cross-links that weren't obvious in raw markdown rendering.
  **Mitigation**: The Grep audit at plan time showed all `../` links resolve within `docs/`. If strict mode surfaces unknown issues at Step 4, fix the source — that's the integrity gate working as designed.

- **Challenge**: No `docs/index.md` today; site has no landing page.
  **Mitigation**: Step 2 creates one. Content is navigation-only (no new manifesto claims), seeded from existing VISION §1.1, low-risk.

- **Challenge**: `awesome-pages` behavior with `README.md` as section index.
  **Mitigation**: Plugin explicitly supports this via its `README` handling; confirmed in its docs. If it misbehaves at Step 4, fall back to renaming `taxonomy/README.md` → `taxonomy/index.md` (but that's a cross-link ripple event and should be avoided).

- **Challenge**: GitHub Pages source toggle is a manual operator step.
  **Mitigation**: Document clearly in Step 8. Without it, the workflow will succeed at build but fail at deploy with a clear error message — low risk of silent failure.

- **Challenge**: Adding Python tooling changes `techContext.md`'s current "Markdown-only project" framing.
  **Mitigation**: Update `techContext.md` during Build phase to reflect the docs-build dependency (keeps memory-bank accurate). This is a minor doc update, not an architectural change — runtime is still Markdown-only; we've just added a docs publishing toolchain.

- **Challenge**: Reference workflow has `contents: write` + `peaceiris/actions-gh-pages` — our pared-down version drops both. Operator may expect symmetry with their existing project.
  **Mitigation**: Surface the divergence explicitly in the PR / reflection — we chose `actions/deploy-pages` because it's the first-party modern path; no `gh-pages` branch needed; less permission surface.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation planned (execution deferred to Build Step 4)
- [ ] Preflight
- [ ] Build
- [ ] QA
