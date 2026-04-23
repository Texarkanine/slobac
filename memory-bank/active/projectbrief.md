# Project Brief: Phase 0 Docs Publishing — mkdocs-material to GitHub Pages

## User Story

As a SLOBAC reader (and, later, an audit-report recipient), I want the `docs/` manifesto published at a stable, navigable, searchable URL so that the Phase 0 value proposition ("a self-contained read") is deliverable as a real URL I can share — and so that future audit reports can cite manifesto sections by link without relying on raw github.com markdown rendering.

## Scope

Ship a Phase 0 docs site built from `docs/` with mkdocs-material, deployed to GitHub Pages via a dedicated GitHub Actions workflow (no `gh-pages` branch — use `actions/deploy-pages`).

### In Scope

- `mkdocs.yml` at repo root configuring mkdocs-material to build from `docs/`.
- Python dependency declaration for the build (mkdocs, mkdocs-material, plus plugins below).
- Plugins: at minimum `awesome-pages` (for nav control without stuffing `mkdocs.yml`) and `pymdownx.snippets` (for inlining source files into docs pages).
- `.github/workflows/docs.yml` — pared-down from the user's reference Jekyll workflow: checkout, Python setup, install deps, `mkdocs build --strict`, upload Pages artifact, deploy via `actions/deploy-pages`.
- `strict: true` (or `mkdocs build --strict`) so the build fails on broken cross-links / missing anchors — this is the load-bearing integrity gate called out in `memory-bank/systemPatterns.md`.
- Repo README touch-up if helpful (badge / link to published site).

### Out of Scope

- Migrating Phase 0 content itself — `docs/` stays as-is.
- `gh-pages` branch approach (we chose Actions deploy-pages explicitly).
- Custom domain, analytics, or theming beyond mkdocs-material defaults.
- The Phase 0 → Phase 1 transition (audit capability) — that's a separate future task.

## Success Criteria

- Running `mkdocs build --strict` locally succeeds against the current `docs/` tree with zero broken-link warnings. (If it surfaces real broken cross-links, fix them as part of this task — that's the gate doing its job.)
- Pushing to `main` triggers the workflow, which builds the site and deploys to GitHub Pages without manual intervention.
- The published site has working navigation, working search, and working internal links for all existing taxonomy/principles/glossary/workflows content.
- A user can visit the published URL and read the manifesto end-to-end without needing to open the repo.

## Design Decisions Already Made (from clarification conversation)

- **Option B chosen** (mkdocs-material + Actions workflow) over Option A (GitHub Pages built-in pointing at `/docs`). Rationale: `strict` link validation at CI time defends the single most damaging failure mode the project has (cross-link drift in `docs/`), and Phase 1+ audit portability wants URL-citeable manifesto pages.
- **Actions `deploy-pages` deploy**, not a `gh-pages` branch. The `gh-pages` branch pattern is legacy; modern GitHub Pages deploys from the workflow artifact directly.
- **Plugins**: `awesome-pages` + `pymdownx.snippets` requested explicitly by operator.

## Rework — toolchain swap

After the original task reached REFLECT COMPLETE, operator initiated a rework to swap the docs-build toolchain. No design decisions from the original scope are reopened; the goals, plugins, workflow structure, GH-compat slugifier, strict-mode gate, PR-gating, and deploy path are unchanged. Two swaps only:

### Rework Scope

1. **`mkdocs` → `properdocs`**. ProperDocs is a drop-in continuation of MkDocs 1.x maintained by `oprypin` (the last active MkDocs maintainer before original abandonment). Per [Discussion #33](https://github.com/orgs/ProperDocs/discussions/33): plugins keep `mkdocs-*` names, `mkdocs.yml` can keep its filename, only the command changes to `properdocs build`. Rationale: original MkDocs is abandoned and the owner plans to reuse the name for an incompatible v2 that will break every plugin/theme — switching to ProperDocs now removes that time-bomb and keeps the same dep surface.
2. **`requirements-docs.txt` → `pyproject.toml` with `uv`**. Declare docs-build deps under PEP 735 `[dependency-groups]`. Local preview and CI both use `uv sync --group docs` + `uv run properdocs build --strict`. `uv.lock` is committed for reproducibility.

### Rework Expected Side-Effects

- `DISABLE_MKDOCS_2_WARNING=true` env var in the workflow likely becomes unnecessary (both the ProperDocs abandonment notice and mkdocs-material's Zensical notice stop firing on ProperDocs per upstream changes). Validate at build-time; drop the env var if silent.
- `techContext.md` toolchain paragraph needs updating: s/mkdocs/properdocs/ and s/pip/uv/.
- `README.md` local-preview instructions change from `pip install -r` to `uv sync --group docs` + `uv run properdocs serve`.

### Rework — Out of Scope

- Changing plugin selection, theme, slugifier, strict/validation config, nav ordering (`.pages`), landing page content, deploy target, or anything in `docs/` itself.

Note: renaming `mkdocs.yml` → `properdocs.yml` was initially classified out-of-scope (per the announcement it was optional), but moved into scope during plan's tech validation after `properdocs 1.6.7` was observed emitting a legacy-filename deprecation INFO notice on every build. The rename is now Step 1 of the plan.
