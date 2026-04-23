# Tech Context

SLOBAC is currently a **Markdown-only project**. There is no source code, no build system, no test framework, and no runtime yet. The current artifact is the `docs/` manifesto, with `planning/VISION.md` as the product brief. When implementation begins, the target packaging is **mainstream agentic-coding-harness primitives — Skills and Sub-Agents** (per `planning/VISION.md` §1.2 and §5 open question #6). The specific harness target order is deliberately unresolved.

## Environment Setup

None required to work on the manifesto. A Markdown-capable editor is sufficient. Anchor-aware preview is helpful because `docs/taxonomy/*.md` entries rely heavily on cross-linked anchors to `docs/principles.md` and `docs/glossary.md`.

## Build Tools

None yet. The `docs/` tree is consumed as-is.

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
