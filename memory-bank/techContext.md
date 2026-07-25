# Tech Context

SLOBAC's runtime artifact is the **audit skill** at [`skills/slobac-audit/`](../skills/slobac-audit/), an AgentSkills.io-shaped `SKILL.md` + `references/` tree that orchestrates three subagent workflows (scout, batch, cross-suite) bundled at `skills/slobac-audit/references/subagents/` to audit test suites of any size. Supports every smell defined in the manifesto, across three detection scopes (per-test, per-file, cross-suite), with the supported-slug set enumerated structurally from taxonomy entry filenames. The full manifesto lives **inside the skill bundle** at `skills/slobac-audit/references/docs/` — hand-authored, single source of truth. Target harnesses: Cursor and Claude Code (per `planning/VISION.md` §1.2 and §5 open question #6, resolved via the OQ1 creative phase to ur-Skill + per-smell references).

The project also has a **docs publishing toolchain** (Phase 0 deliverable): the manifesto is published to GitHub Pages by `.github/workflows/docs.yaml` using [ProperDocs](https://properdocs.org/) (the actively-maintained continuation of MkDocs 1.x) with the `mkdocs-material` theme, using `--strict` link validation as a CI gate. ProperDocs builds directly from `skills/slobac-audit/references/docs/` (`docs_dir` in `properdocs.yml` points there).

## Audit skill layout and discovery

The canonical source is [`skills/slobac-audit/`](../skills/slobac-audit/). Layout:

- `SKILL.md` — orchestrator workflow: scope parsing, scout dispatch, partitioning, batch dispatch, cross-suite dispatch, report synthesis.
- `references/report-template.md` — report shape.
- `references/behavior-summary-format.md` — intermediate representation spec for cross-suite assessor.
- `references/suite-manifest-format.md` — scout output spec for orchestrator partitioning.
- `references/docs/` — the **full SLOBAC manifesto**: `what-is-slobac.md`, `using-slobac.md`, `.pages`, `principles/` (`test-qualities.md`, `refactor-qualities.md`, `glossary.md`, `workflows.md`), and `taxonomy/` (canonical smell definitions + `README.md` shape SoT). Hand-authored; the SKILL.md workflow reads one taxonomy file per in-scope smell at runtime — no second file, no augmentation layer. ProperDocs builds the published site directly from this directory.

Subagent workflows (`references/subagents/scout.md`, `batch.md`, `cross-suite.md`) are dispatched by the orchestrator as raw task prompts. All shared content (taxonomy, format specs) lives under `references/` — subagents resolve it via the absolute path passed by the orchestrator at runtime.

Per-harness discovery paths are operator-install concerns, not architectural ones. The canonical source stays harness-agnostic; install via **`npx skills add Texarkanine/slobac --skill slobac-audit`** or the [`txrk9-agent-plugins`](https://github.com/Texarkanine/txrk9-agent-plugins) marketplace (see [`using-slobac.md`](../skills/slobac-audit/references/docs/using-slobac.md)).

### Full-manifesto-in-bundle pattern

The entire manifesto lives at `skills/slobac-audit/references/docs/`. `properdocs.yml` `docs_dir` points directly at this directory — no snippet indirection, no wrapper files, no `docs/` directory at repo root. At agent-runtime the skill reads only files inside its own root — invariant #11 (skill-root self-containment) is satisfied architecturally. At build-time properdocs renders the site directly from the same files.

Relative links in canonical files (e.g. `[Understandable](../principles/test-qualities.md#understandable)` inside a taxonomy entry) resolve at their actual filesystem location because properdocs renders from the directory where the files live. No link-path footgun — links work both for the rendered site and for raw-GitHub rendering.

No generator, no CI drift-check, no copy-with-sync discipline. There is one document per smell; forking is structurally impossible. Phase-5 marketplace distribution is trivially supported: the committed layout is the install layout.

**Exception — the slug / severity / detection-scope navigation index** (the table at the top of `skills/slobac-audit/references/docs/taxonomy/README.md` and the same table embedded between `<!-- BEGIN: taxonomy-index -->` sentinels in `skills/slobac-audit/SKILL.md`) **is generated** from each canonical entry's header table by `scripts/gen_taxonomy_index.py`, with a CI drift-check job that fails the PR on staleness (see `.github/workflows/docs.yaml`). The "no generator" rule applies to the manifesto's *canonical content* — per-smell entries, principles, glossary, workflows. The navigation index is a *derived index* of metadata the canonical entries already carry; it is never the source of truth for that metadata, and a contributor edits the per-entry header to change a slug's severity or scope, then runs the regen command. CI catches the drift if they forget. The orchestrator reading the embedded copy in `SKILL.md` (rather than fanning out to every per-entry header at runtime) is the motivating use case; the README copy is downstream of that.

## Audit fixtures

Planted test suites live at [`tests/fixtures/audit/<scenario>/`](../tests/fixtures/audit/) — one directory per scenario. Phase 1 scenarios (`deliverable-fossils/`, `naming-lies/`, `both-smells/`, `clean/`) contain single `.py` files. Orchestration scenarios (`shared-state/`, `monolithic-test-file/`, `semantic-redundancy/`, `wrong-level/`) may contain multiple files and subdirectories to exercise per-file and cross-suite detection scopes. Each scenario contains one or more `.py` files embodying the scenario and an `expected-findings.md` documenting what the audit should emit. The fixtures are **input** to the audit skill — they are never executed by any runner SLOBAC owns. Validation is manual: the operator invokes the skill against a fixture path and compares the emitted `.slobac/audit.md` to `expected-findings.md`. A scripted eval harness is deferred to a future phase.

## Environment Setup

**To read/edit the manifesto:** a Markdown-capable editor is sufficient. The entire manifesto lives at `skills/slobac-audit/references/docs/` — per-smell entries at `taxonomy/<slug>.md`, principles at `principles/test-qualities.md` and `principles/refactor-qualities.md`, glossary at `principles/glossary.md`, workflows at `principles/workflows.md`. There are no wrappers or indirection; this is both the authoring surface and the properdocs build source.

**To preview the built docs site locally:** `uv` (which auto-provisions Python per `pyproject.toml`), then `uv sync --group docs` + `uv run properdocs serve`.

## Build Tools

- **release-please** (automated versioning and changelog). Configured via `release-please-config.json` and `.release-please-manifest.json` at repo root; driven by `googleapis/release-please-action@v4` in `.github/workflows/release-please.yaml`. Uses `release-type: simple` (`version.txt` as canonical, `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json` as sync'd extras). Conventional commits on `main` produce Release PRs; merging a Release PR creates the GitHub release and tag.
- **properdocs + mkdocs-material** (docs site generator; Phase 0 publishing). ProperDocs is a drop-in replacement for MkDocs 1.x by its last active maintainer; the config file, plugin names, and CLI semantics are identical except the command is `properdocs` instead of `mkdocs`.
- **mkdocs-awesome-pages-plugin** (nav ordering via `.pages` files).
- **mkdocs-redirects** (pre-positioned for future rename resilience; empty `redirect_maps` until first taxonomy rename).
- **pymdown-extensions** (snippet-includes via `pymdownx.snippets`, plus the standard mkdocs-material extension stack).

Dependencies are declared in `pyproject.toml` under the PEP 735 `[dependency-groups] docs` group; `uv.lock` pins them for reproducibility. CI uses `uv sync --group docs --frozen` so lock drift must be a PR-reviewable change. No runtime Python is required for the manifesto itself.

The cross-link integrity gate is `properdocs build --strict` combined with `validation.anchors: warn` — every broken markdown cross-reference fails the build. This is the CI-enforced version of the cross-link-drift invariant named in `memory-bank/systemPatterns.md`. PRs are built (but not deployed) so link-drift is caught at review time.

## Testing Process

None yet for functional behavior. When implementation begins, the test target will be the audit/apply capabilities' own behavior against fixture test suites — not the tests of third-party repos.

**REUSE compliance validation (`skills/slobac-audit/` only):** the audit skill bundle is the only subtree with a nested `REUSE.toml`; validate its standalone compliance with `reuse --root . lint` from `skills/slobac-audit/`. The `--root .` flag is mandatory — plain `reuse lint` ascends to the `.git` boundary and lints the full monorepo. The REUSE CLI is not in `pyproject.toml`; install via `pipx install reuse` if needed.

## Authoring Tooling

- **Cursor rules.** Working instructions (TDD discipline, markdown style, git safety, niko memory-bank system, etc.) live in `.cursor/rules/shared/`. These are the canonical source for *how* to work on SLOBAC; do not duplicate them in memory-bank files.
- **Niko memory-bank system.** Project-knowledge capture (this directory) is managed by the niko skills in `.cursor/skills/shared/niko*/`. Entry point is `/niko`.
- **`ai-rizz.skbd`** (project root). A manifest for the [ai-rizz](https://github.com/Texarkanine/.cursor-rules) tool that pulls the shared niko rulesets and the markdown-style rule into this repo's `.cursor/rules/`. Rule updates in this repo should flow through that upstream rather than being edited in place.

## Anticipated Tooling (Phase 1+)

These are referenced by the manifesto and will be **orchestrated**, never reimplemented. Listed here so a future contributor doesn't waste time rediscovering them. Canonical per-ecosystem pointers live in [`glossary.md`](../skills/slobac-audit/references/docs/principles/glossary.md#mutation-testing) and [`planning/research/report.md`](../planning/research/report.md).

- Mutation testing (JVM PIT+Descartes, JS/TS Stryker, Python mutmut/Cosmic Ray, Rust cargo-mutants, Go go-mutesting, .NET Stryker.NET). Required for the preservation-of-regression-detection-power gate.
- Existing test-smell linters — deferred to per-ecosystem tooling, not reimplemented.
- Existing codemod runners — orchestrated by the apply layer if needed, not reimplemented.

## Design System

Docs site chrome (not product UI): ProperDocs / Material tokens live in [`skills/slobac-audit/references/docs/stylesheets/extra.css`](../skills/slobac-audit/references/docs/stylesheets/extra.css), wired from [`properdocs.yaml`](../properdocs.yaml) (`primary`/`accent: custom` + `extra_css`). Warm paper light / ember dark.
