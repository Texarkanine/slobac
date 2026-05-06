# Using the SLOBAC audit

The SLOBAC manifesto ships alongside an agentic audit capability: a set of [AgentSkills.io](https://agentskills.io/)-shaped skills that audit a test suite against this manifesto and emit a portable markdown report. This page covers installing, invoking, and troubleshooting the audit.

If you are here to read about what tests should be — not run a tool — you are already in the right place. The manifesto pages ([Principles](principles.md), [Taxonomy](taxonomy/README.md), [Workflows](workflows.md), [Glossary](glossary.md)) stand on their own; no software is required.

## Install

The audit ships as a single **plugin** with one registered skill (`audit`). Install the plugin once; the orchestrator dispatches subagents internally from workflow prompts bundled in `references/subagents/`.

### Cursor

1. Open **Cursor Settings → Marketplace** (or your Cursor version's equivalent plugin marketplace UI).
2. Add the marketplace catalog from [`Texarkanine/txrk9-agent-plugins`](https://github.com/Texarkanine/txrk9-agent-plugins) if it is not already configured (that repo publishes `.cursor-plugin/marketplace.json`).
3. Install the **SLOBAC** plugin (`slobac`). Cursor registers the invocation `/slobac-audit` from the `SKILL.md` frontmatter `name` field.

### Claude Code

1. Register the marketplace catalog from [`Texarkanine/txrk9-agent-plugins`](https://github.com/Texarkanine/txrk9-agent-plugins) (see that repo's `.claude-plugin/marketplace.json`).
2. Install the **slobac** plugin from the marketplace. Claude Code namespaces skills as `/plugin-name:folder-name` — with plugin name `slobac` and folder `audit/`, you invoke `/slobac:audit`.

## Scope

The audit is intended to be **read-only**: it reports findings; it does not modify test code. A report is created that you can feed into your chosen remediation process.

The detection prose in every taxonomy entry is language-neutral, but **Python is the only validated ecosystem** today. The [Polyglot notes](taxonomy/README.md) section in each entry describes the per-language detection surface for future work.

Operators invoke the audit with **explicit slug names** — e.g. `tautology-theatre`, `vacuous-assertion`. Free-text or fuzzy-phrase requests are refused with the supported-slug list. The unscoped wildcard `all` (or an unscoped invocation) resolves to the full supported set.

## Context window

**For best results, run SLOBAC with the most-capable model and largest context window available.** In Cursor, enable MAX mode. In Claude Code, use Opus or Sonnet with the 1M context window. Larger context means fewer batches, richer cross-suite analysis, and better recall on redundancy detection. SLOBAC works at 200K context but shards more aggressively, trading recall on cross-suite smells for safety.

Pass your context window size in the invocation — `"Audit tests/ — 1M context window"` — to skip the one-time question the orchestrator asks when it encounters a large suite without a stated budget.

## TL;DR

You probably want to run `/slobac:audit all - 1M Context window` (after making sure that you've picked a beefy model and actually set that 1M context window).
