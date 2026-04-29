# SLOBAC audit skill

An [AgentSkills.io](https://agentskills.io/)-shaped skill that audits a test suite against the [SLOBAC manifesto](https://github.com/Texarkanine/slobac) and emits a portable markdown report. Phase 1 covers two smells: [`deliverable-fossils`](https://texarkanine.github.io/slobac/taxonomy/deliverable-fossils/) and [`naming-lies`](https://texarkanine.github.io/slobac/taxonomy/naming-lies/).

This is the **canonical source** for the skill. The layout is harness-agnostic; the install step per harness is described below.

## Layout

```
skills/slobac-audit/
├── SKILL.md                              # ur-workflow (primitive-agnostic prose)
├── README.md                             # this file
└── references/
    ├── report-template.md                # audit report shape
    └── docs/
        └── taxonomy/
            ├── deliverable-fossils.md    # canonical smell definition (Phase 1)
            ├── naming-lies.md            # canonical smell definition (Phase 1)
            └── ... (13 more entries)     # canonical smell definitions (Phase 2+)
```

The canonical smell definitions live in `references/docs/taxonomy/<slug>.md` — hand-authored, single source of truth. The rendered SLOBAC site ([properdocs](https://texarkanine.github.io/slobac/)) consumes these files via `pymdownx.snippets` at build time. The skill reads the same files at agent-runtime; no generator, no drift-check, no external paths, no network fetches, no harness-cwd assumptions. The skill bundle is fully self-contained and installable anywhere.

## Install

The skill is discoverable by any harness that understands an AgentSkills.io-shaped `SKILL.md`. In practice that means copying or symlinking this directory into the harness's skill-discovery path.

### Cursor

Cursor discovers skills under `.cursor/skills/` (repo-level) or `~/.cursor/skills/` (user-level). To make the audit available in the current checkout:

```bash
ln -s "$PWD/skills/slobac-audit" .cursor/skills/slobac-audit
```

To make it available across all projects:

```bash
ln -s "$PWD/skills/slobac-audit" ~/.cursor/skills/slobac-audit
```

### Claude Code

Claude Code discovers skills under `.claude/skills/` (repo-level) or `~/.claude/skills/` (user-level). The install pattern mirrors Cursor:

```bash
ln -s "$PWD/skills/slobac-audit" .claude/skills/slobac-audit
```

### Other harnesses

If your harness supports the AgentSkills.io shape, point its skill loader at this directory. The `SKILL.md` frontmatter (`name`, `description`) and the `references/` subtree follow the standard convention; no harness-specific glue is required.

## Invoke

Natural language. Examples:

- "Audit the tests under `src/tests/` for SLOBAC smells."
- "Check `tests/unit/` for naming-lies."
- "Run the SLOBAC audit over this suite for fossils."
- "Which tests have titles that don't match their bodies?"

The skill scopes the audit from the phrasing, reads the target suite, and writes `slobac-audit.md` in the current working directory. Pass a different path explicitly if wanted:

- "Audit `src/tests/` and write the report to `reports/audit-2026-04.md`."

## Smoke test

The repo ships fixture suites under [`tests/fixtures/audit/`](https://github.com/Texarkanine/slobac/tree/main/tests/fixtures/audit) with documented expected findings. Use them to verify the install:

1. In Cursor or Claude Code, run: **"Audit `tests/fixtures/audit/deliverable-fossils/` for fossils."**
2. Compare the emitted `slobac-audit.md` against [`tests/fixtures/audit/deliverable-fossils/expected-findings.md`](https://github.com/Texarkanine/slobac/blob/main/tests/fixtures/audit/deliverable-fossils/expected-findings.md).
3. Every flagged test in the expected file should appear in the audit report with a matching remediation arm. The negative-example test (`test_refactor_preserving_rename_does_not_change_lookup_results`) must not be flagged.

Repeat with `tests/fixtures/audit/naming-lies/`, `tests/fixtures/audit/both-smells/` (exercise scope), and `tests/fixtures/audit/clean/` (expect no findings) to cover the full Phase-1 behavior matrix.

Phrasing of the emitted report need not be byte-identical to `expected-findings.md` — the shape contract is that every expected finding is emitted with its correct smell slug, remediation arm, and a rationale that cites the canonical docs entry. Divergence beyond that is a bug in the skill, not the fixture.

## Scope and non-goals

- **Phase 1 supports two smells.** Any request for other smells (`tautology-theatre`, `vacuous-assertion`, etc.) is refused with a clear message — the audit never silently skips a requested smell.
- **The audit is read-only.** It does not modify test code. Applying a recommendation from the report is a separate step (today manual; Phase 3 is the automated apply capability that does not exist yet).
- **Python is the only validated ecosystem.** The detection prose is language-neutral; the manifesto's Polyglot notes describe per-ecosystem detection surface. Validation on JS/TS, Ruby, JVM, etc. is Phase-2+ work.

## Troubleshooting

- **The skill emits a finding but the rationale is vague ("this test has fossil-shaped vocabulary").** The canonical entry's False-positive guards section exists specifically to prevent this. If the skill cannot cite a specific signal from the Signals section, the finding should not emit — reconsider.
- **The skill misses a finding.** Re-read the canonical entry (`references/docs/taxonomy/<slug>.md`). If the missed case is not covered by any signal, that is a manifesto gap, not a skill bug — raise it as a PR to the canonical entry.
