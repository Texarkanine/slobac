# SLOBAC

**Suite-Life Of Bobs And Code** — a manifesto for what tests should be, what test suites should be, and the named ways they go wrong.

The manifesto ships first. An audit capability (built as Skills / Sub-Agents for mainstream agentic-coding harnesses) comes next. An apply capability follows. Each layer is useful on its own; each layer depends on the previous one for correctness.

## Read the manifesto

- 📖 **Published site:** <https://texarkanine.github.io/slobac/> *(after the operator enables GitHub Pages via the Actions source — see [Docs publishing](#docs-publishing) below)*
- 🗂 **Raw markdown:** the [`docs/`](docs/) tree renders cleanly on GitHub — the manifesto is self-contained and does not require the built site.

Entry points:

- [Principles](docs/principles.md) — what a test should be, and the bounds on disciplined suite refactoring.
- [Workflows](docs/workflows.md) — the RED-GREEN-MUTATE-KILL-REFACTOR cycle taxonomy fixes assume.
- [Taxonomy](docs/taxonomy/README.md) — 15 named failure modes with signals, prescribed fixes, and examples.
- [Glossary](docs/glossary.md) — shared terminology and citations.

## Audit capability (Phase 1)

- 🔍 **Audit skill:** [`skills/slobac-audit/`](skills/slobac-audit/) — an AgentSkills.io-shaped skill that audits a test suite for `deliverable-fossils` and `naming-lies`, then emits a portable markdown report. Install and smoke-test instructions in [`skills/slobac-audit/README.md`](skills/slobac-audit/README.md).
- 🧪 **Fixtures:** [`tests/fixtures/audit/`](tests/fixtures/audit/) — planted test suites with documented expected findings. Use them to verify any install, and as worked examples of what the audit considers in- or out-of-scope.

## Project context

- [`planning/VISION.md`](planning/VISION.md) — the product brief: what SLOBAC is, who it's for, the phased delivery plan, and the open questions.
- [`planning/research/`](planning/research/) — prior-art survey backing the positioning.
- [`memory-bank/`](memory-bank/) — project knowledge captured by the [Niko memory-bank system](.cursor/skills/shared/niko/SKILL.md).

## Contributor tooling

Working rules (TDD discipline, markdown style, git safety, the Niko workflow) live in [`.cursor/rules/shared/`](.cursor/rules/shared/). These are authored via [ai-rizz](https://github.com/Texarkanine/.cursor-rules) — rule updates should flow through the upstream manifest at [`ai-rizz.skbd`](ai-rizz.skbd), not through in-place edits.

## Docs publishing

The `docs/` manifesto is published to GitHub Pages by [`.github/workflows/docs.yaml`](.github/workflows/docs.yaml). The workflow uses [ProperDocs](https://properdocs.org/) (a drop-in continuation of MkDocs 1.x) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme and strict-mode link validation — a PR that breaks a cross-link fails CI.

**Local preview:**

```bash
uv sync --group docs
uv run properdocs serve
```

**First-time setup** (one-time, by repo admin): repo Settings → Pages → *Source* must be set to **GitHub Actions** (not "Deploy from a branch"). Without this, the `build` job passes but `deploy` fails.

## License

See [`LICENSE`](LICENSE).
