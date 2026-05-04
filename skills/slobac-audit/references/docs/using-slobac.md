# Using the SLOBAC audit

The SLOBAC manifesto ships alongside an agentic audit capability: a set of [AgentSkills.io](https://agentskills.io/)-shaped skills that audit a test suite against this manifesto and emit a portable markdown report. This page covers installing, invoking, and troubleshooting the audit.

If you are here to read about what tests should be — not run a tool — you are already in the right place. The manifesto pages ([Principles](principles.md), [Taxonomy](taxonomy/README.md), [Workflows](workflows.md), [Glossary](glossary.md)) stand on their own; no software is required.

## Scope

The audit is **read-only**: it reports findings; it does not modify test code. Applying a recommendation is a separate step (today manual; automated apply is a future capability).

The detection prose in every taxonomy entry is language-neutral, but **Python is the only validated ecosystem** today. The [Polyglot notes](taxonomy/README.md) section in each entry describes the per-language detection surface for future work.

Operators invoke the audit with **explicit slug names** — e.g. `tautology-theatre`, `vacuous-assertion`. Free-text or fuzzy-phrase requests are refused with the supported-slug list. The unscoped wildcard `all` (or an unscoped invocation) resolves to the full supported set.

## Install

The audit is distributed as four sibling skills. Install all four — the orchestrator (`slobac-audit`) dispatches the others.

### Cursor

Cursor discovers skills under `.cursor/skills/` (repo-level) or `~/.cursor/skills/` (user-level).

```bash
# Repo-level (this checkout only)
for skill in slobac-audit slobac-scout slobac-batch slobac-cross-suite; do
  ln -s "$PWD/skills/$skill" ".cursor/skills/$skill"
done

# User-level (available in all projects)
for skill in slobac-audit slobac-scout slobac-batch slobac-cross-suite; do
  ln -s "$PWD/skills/$skill" "$HOME/.cursor/skills/$skill"
done
```

### Claude Code

Claude Code discovers skills under `.claude/skills/` (repo-level) or `~/.claude/skills/` (user-level). The install pattern mirrors Cursor:

```bash
for skill in slobac-audit slobac-scout slobac-batch slobac-cross-suite; do
  ln -s "$PWD/skills/$skill" ".claude/skills/$skill"
done
```

### Other harnesses

If your harness supports the AgentSkills.io shape, point its skill loader at all four skill directories. The `SKILL.md` frontmatter (`name`, `description`) and the `references/` subtree follow the standard convention; no harness-specific glue is required.

## Invoke

Natural language with an explicit slug or slugs. Examples:

- `"Audit tests/ for tautology-theatre."`
- `"Audit tests/unit/ for naming-lies and vacuous-assertion."`
- `"Audit tests/ for all smells."`
- `"Audit tests/ for all smells — 1M context window."`
- `"Audit src/tests/ and write the report to reports/audit-2026-04.md."`

The skill scopes the audit from the phrasing, orchestrates subagents as needed, and writes `slobac-audit.md` in the current working directory (or the path you provide).

For a list of available slugs, see the [taxonomy catalog](taxonomy/README.md).

### Context window

**For best results, run SLOBAC with your largest available model and context window.** In Cursor, enable MAX mode. In Claude Code, use Opus or Sonnet with the 1M context window. Larger context means fewer batches, richer cross-suite analysis, and better recall on redundancy detection. SLOBAC works at 200K context but shards more aggressively, trading recall on cross-suite smells for safety.

Pass your context window size in the invocation — `"Audit tests/ — 1M context window"` — to skip the one-time question the orchestrator asks when it encounters a large suite without a stated budget.

## Troubleshooting

**The skill emits a finding but the rationale is vague.** The canonical entry's *False-positive guards* section exists to prevent this. If the skill cannot cite a specific signal from the entry's *Signals* section, the finding should not have emitted — reconsider. See the [taxonomy entry](taxonomy/README.md) for the slug.

**The skill misses a finding.** Re-read the canonical entry (`taxonomy/<slug>.md`). If the missed case is not covered by any signal, that is a manifesto gap, not a skill bug — raise it as a PR to the canonical entry.

**Cross-suite findings seem wrong.** The cross-suite assessor must perform targeted source reads before confirming. If it is emitting findings based only on behavior-summary clustering, that is a bug — summaries are an index for candidate detection, not evidence.

**The audit launches too many batches.** Provide your context window size in the invocation to avoid conservative sharding at the 200K floor.
