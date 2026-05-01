> ⚠️ Under active development. Documentation may be aspirational, not factual.

# SLOBAC - The Suite Life of Bobs and Code

![SLOBAC Logo](./docs/img/slobac.jpg)

An agentic skill toolkit for cleaning up software test suites.

## Read the Manifesto

[What tests should be, what test suites should be, and the named ways they go wrong.](https://texarkanine.github.io/slobac/)

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

The manifesto at `skills/slobac-audit/references/docs/` is published to GitHub Pages by [`.github/workflows/docs.yaml`](.github/workflows/docs.yaml). The workflow uses [ProperDocs](https://properdocs.org/) (a drop-in continuation of MkDocs 1.x) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme and strict-mode link validation — a PR that breaks a cross-link fails CI.

**Local preview:**

```bash
uv sync --group docs
uv run properdocs serve
```

**First-time setup** (one-time, by repo admin): repo Settings → Pages → *Source* must be set to **GitHub Actions** (not "Deploy from a branch"). Without this, the `build` job passes but `deploy` fails.

## License

Various licenses apply to different parts of the project. See [`REUSE.toml`](REUSE.toml) for details.

- Skills: [PPL-S](LICENSES/LicenseRef-PPL-S.txt)
- Manifesto/docs: [CC-BY-SA-4.0](LICENSES/CC-BY-SA-4.0.txt)
- Code: [AGPL-3.0-or-later](LICENSES/AGPL-3.0-or-later.txt)
