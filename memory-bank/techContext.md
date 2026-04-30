# Tech Context

SLOBAC's runtime artifact is the **audit skill** at [`skills/slobac-audit/`](../skills/slobac-audit/), an AgentSkills.io-shaped `SKILL.md` + `references/` tree that orchestrates three sibling skills ([`slobac-scout`](../skills/slobac-scout/), [`slobac-batch`](../skills/slobac-batch/), [`slobac-cross-suite`](../skills/slobac-cross-suite/)) to audit test suites of any size. Supports 6 smells across 3 detection scopes: per-test (`deliverable-fossils`, `naming-lies`), per-file (`shared-state`, `monolithic-test-file`), and cross-suite (`semantic-redundancy`, `wrong-level`). The full manifesto lives **inside the skill bundle** at `skills/slobac-audit/references/docs/` — hand-authored, single source of truth. Target harnesses: Cursor and Claude Code (per `planning/VISION.md` §1.2 and §5 open question #6, resolved via the OQ1 creative phase to ur-Skill + per-smell references).

The project also has a **docs publishing toolchain** (Phase 0 deliverable): the manifesto is published to GitHub Pages by `.github/workflows/docs.yaml` using [ProperDocs](https://properdocs.org/) (the actively-maintained continuation of MkDocs 1.x) with the `mkdocs-material` theme, using `--strict` link validation as a CI gate. ProperDocs builds directly from `skills/slobac-audit/references/docs/` (`docs_dir` in `properdocs.yml` points there).

## Audit skill layout and discovery

The canonical source is [`skills/slobac-audit/`](../skills/slobac-audit/). Layout:

- `SKILL.md` — orchestrator workflow: scope parsing, scout dispatch, partitioning, batch dispatch, cross-suite dispatch, report synthesis.
- `references/report-template.md` — report shape.
- `references/behavior-summary-format.md` — intermediate representation spec for cross-suite assessor.
- `references/suite-manifest-format.md` — scout output spec for orchestrator partitioning.
- `references/docs/` — the **full SLOBAC manifesto**: `index.md`, `principles.md`, `glossary.md`, `workflows.md`, `.pages`, and `taxonomy/` (15 canonical smell definitions + `README.md` shape SoT). Hand-authored; the SKILL.md workflow reads one taxonomy file per in-scope smell at runtime — no second file, no augmentation layer. ProperDocs builds the published site directly from this directory.

Sibling skills (`skills/slobac-scout/`, `skills/slobac-batch/`, `skills/slobac-cross-suite/`) are subagents dispatched by the orchestrator. They reach into `slobac-audit/references/` for shared content via `../slobac-audit/references/...`.

Per-harness discovery paths are operator-install concerns, not architectural ones. The canonical source stays harness-agnostic; install via symlink (`.cursor/skills/slobac-audit`, `.claude/skills/slobac-audit`) per the smoke-test in [`skills/slobac-audit/README.md`](../skills/slobac-audit/README.md).

### Full-manifesto-in-bundle pattern

The entire manifesto lives at `skills/slobac-audit/references/docs/`. `properdocs.yml` `docs_dir` points directly at this directory — no snippet indirection, no wrapper files, no `docs/` directory at repo root. At agent-runtime the skill reads only files inside its own root — invariant #11 (skill-root self-containment) is satisfied architecturally. At build-time properdocs renders the site directly from the same files.

Relative links in canonical files (e.g. `[Understandable](../principles.md#understandable)` inside a taxonomy entry) resolve at their actual filesystem location because properdocs renders from the directory where the files live. No link-path footgun — links work both for the rendered site and for raw-GitHub rendering.

No generator, no CI drift-check, no copy-with-sync discipline. There is one document per smell; forking is structurally impossible. Phase-5 marketplace distribution is trivially supported: the committed layout is the install layout.

## Audit fixtures

Planted test suites live at [`tests/fixtures/audit/<scenario>/`](../tests/fixtures/audit/) — one directory per scenario. Phase 1 scenarios (`deliverable-fossils/`, `naming-lies/`, `both-smells/`, `clean/`) contain single `.py` files. Orchestration scenarios (`shared-state/`, `monolithic-test-file/`, `semantic-redundancy/`, `wrong-level/`) may contain multiple files and subdirectories to exercise per-file and cross-suite detection scopes. Each scenario contains one or more `.py` files embodying the scenario and an `expected-findings.md` documenting what the audit should emit. The fixtures are **input** to the audit skill — they are never executed by any runner SLOBAC owns. Validation is manual: the operator invokes the skill against a fixture path and compares the emitted `slobac-audit.md` to `expected-findings.md`. A scripted eval harness is deferred to a future phase.

## Environment Setup

**To read/edit the manifesto:** a Markdown-capable editor is sufficient. The entire manifesto lives at `skills/slobac-audit/references/docs/` — per-smell entries at `taxonomy/<slug>.md`, principles at `principles.md`, glossary at `glossary.md`, workflows at `workflows.md`. There are no wrappers or indirection; this is both the authoring surface and the properdocs build source.

**To preview the built docs site locally:** `uv` (which auto-provisions Python per `pyproject.toml`), then `uv sync --group docs` + `uv run properdocs serve`.

## Build Tools

- **properdocs + mkdocs-material** (docs site generator; Phase 0 publishing). ProperDocs is a drop-in replacement for MkDocs 1.x by its last active maintainer; the config file, plugin names, and CLI semantics are identical except the command is `properdocs` instead of `mkdocs`.
- **mkdocs-awesome-pages-plugin** (nav ordering via `.pages` files).
- **mkdocs-redirects** (pre-positioned for future rename resilience; empty `redirect_maps` until first taxonomy rename).
- **pymdown-extensions** (snippet-includes via `pymdownx.snippets`, plus the standard mkdocs-material extension stack).

Dependencies are declared in `pyproject.toml` under the PEP 735 `[dependency-groups] docs` group; `uv.lock` pins them for reproducibility. CI uses `uv sync --group docs --frozen` so lock drift must be a PR-reviewable change. No runtime Python is required for the manifesto itself.

The cross-link integrity gate is `properdocs build --strict` combined with `validation.anchors: warn` — every broken markdown cross-reference fails the build. This is the CI-enforced version of the cross-link-drift invariant named in `memory-bank/systemPatterns.md`. PRs are built (but not deployed) so link-drift is caught at review time.

## Testing Process

None yet. There is no code to test. When implementation begins, the test target will be the audit/apply capabilities' own behavior against fixture test suites — not the tests of third-party repos.

## Authoring Tooling

- **Cursor rules.** Working instructions (TDD discipline, markdown style, git safety, niko memory-bank system, etc.) live in `.cursor/rules/shared/`. These are the canonical source for *how* to work on SLOBAC; do not duplicate them in memory-bank files.
- **Niko memory-bank system.** Project-knowledge capture (this directory) is managed by the niko skills in `.cursor/skills/shared/niko*/`. Entry point is `/niko`.
- **`ai-rizz.skbd`** (project root). A manifest for the [ai-rizz](https://github.com/Texarkanine/.cursor-rules) tool that pulls the shared niko rulesets and the markdown-style rule into this repo's `.cursor/rules/`. Rule updates in this repo should flow through that upstream rather than being edited in place.

## Anticipated Tooling (Phase 1+)

These are referenced by the manifesto and will be **orchestrated**, never reimplemented. Listed here so a future contributor doesn't waste time rediscovering them. Canonical per-ecosystem pointers live in [`glossary.md`](../skills/slobac-audit/references/docs/glossary.md#mutation-testing) and [`planning/research/report.md`](../planning/research/report.md).

- Mutation testing (JVM PIT+Descartes, JS/TS Stryker, Python mutmut/Cosmic Ray, Rust cargo-mutants, Go go-mutesting, .NET Stryker.NET). Required for the preservation-of-regression-detection-power gate.
- Existing test-smell linters — deferred to per-ecosystem tooling, not reimplemented.
- Existing codemod runners — orchestrated by the apply layer if needed, not reimplemented.

## Design System

N/A. SLOBAC has no user-facing UI. The audit output is plain text (format TBD per `planning/VISION.md` §5 open question #1).
