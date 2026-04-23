# Tech Context

SLOBAC's first runtime artifact is the **audit skill** at [`skills/slobac-audit/`](../skills/slobac-audit/), an AgentSkills.io-shaped `SKILL.md` + `references/` tree that covers [`deliverable-fossils`](../docs/taxonomy/deliverable-fossils.md) and [`naming-lies`](../docs/taxonomy/naming-lies.md) in Phase 1. The manifesto at `docs/` remains canonical; the skill carries only audit-specific augmentation and reads smell definitions from `docs/taxonomy/<slug>.md` at agent-runtime. Target harnesses: Cursor and Claude Code (per `planning/VISION.md` §1.2 and §5 open question #6, resolved via the OQ1 creative phase to ur-Skill + per-smell references).

The project also has a **docs publishing toolchain** (Phase 0 deliverable): the `docs/` tree is published to GitHub Pages by `.github/workflows/docs.yaml` using [ProperDocs](https://properdocs.org/) (the actively-maintained continuation of MkDocs 1.x) with the `mkdocs-material` theme, using `--strict` link validation as a CI gate. This is build-only infrastructure — it does not change the "manifesto ships as raw markdown on github.com" property.

## Audit skill layout and discovery

The canonical source is [`skills/slobac-audit/`](../skills/slobac-audit/). Layout:

- `SKILL.md` — ur-workflow: scope parsing, per-smell file loading, detection, report emission.
- `references/report-template.md` — report shape.
- `references/smells/<slug>.md` — audit-specific augmentation per smell. Always present per convention (even if minimal); the SKILL.md workflow reads it unconditionally.

Per-harness discovery paths are operator-install concerns, not architectural ones. The canonical source stays harness-agnostic; install via symlink (`.cursor/skills/slobac-audit`, `.claude/skills/slobac-audit`) per the smoke-test in [`skills/slobac-audit/README.md`](../skills/slobac-audit/README.md).

### Canonical-docs-referenced-from-skill pattern

The skill **never carries a copy** of manifesto content. At runtime it reads:

1. `docs/taxonomy/<slug>.md` for the canonical definition (Summary, Description, Signals, Prescribed Fix, Example, Related modes, Polyglot notes).
2. `skills/slobac-audit/references/smells/<slug>.md` for audit-specific augmentation (invocation hints, emission hints, false-positive guards).

This structurally enforces the manifesto-independence invariant from [`systemPatterns.md`](./systemPatterns.md) — nothing in the skill tree can drift from the manifesto because no copy of the manifesto lives in the skill tree. The tradeoff: the skill needs the `docs/` tree reachable at runtime. Phase 1 and 2 ship in-repo, so co-location is free. Phase 5 marketplace distribution will need to either bundle both trees or synthesize self-contained skill files at release time.

## Audit fixtures

Planted test suites live at [`tests/fixtures/audit/<scenario>/`](../tests/fixtures/audit/) — one directory per scenario (`deliverable-fossils/`, `naming-lies/`, `both-smells/`, `clean/`). Each contains one or more `.py` files embodying the scenario and an `expected-findings.md` documenting what the audit should emit. The fixtures are **input** to the audit skill — they are never executed by any runner SLOBAC owns. Phase-1 validation is manual: the operator invokes the skill against a fixture path and compares the emitted `slobac-audit.md` to `expected-findings.md`. A scripted eval harness is deferred to Phase 2+.

## Environment Setup

**To read/edit the manifesto:** a Markdown-capable editor is sufficient. Anchor-aware preview is helpful because `docs/taxonomy/*.md` entries rely heavily on cross-linked anchors to `docs/principles.md` and `docs/glossary.md`.

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

These are referenced by the manifesto and will be **orchestrated**, never reimplemented. Listed here so a future contributor doesn't waste time rediscovering them. Canonical per-ecosystem pointers live in [`docs/glossary.md`](../docs/glossary.md#mutation-testing) and [`planning/research/report.md`](../planning/research/report.md).

- Mutation testing (JVM PIT+Descartes, JS/TS Stryker, Python mutmut/Cosmic Ray, Rust cargo-mutants, Go go-mutesting, .NET Stryker.NET). Required for the preservation-of-regression-detection-power gate.
- Existing test-smell linters — deferred to per-ecosystem tooling, not reimplemented.
- Existing codemod runners — orchestrated by the apply layer if needed, not reimplemented.

## Design System

N/A. SLOBAC has no user-facing UI. The audit output is plain text (format TBD per `planning/VISION.md` §5 open question #1).
