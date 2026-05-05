# Project Brief

## User Story

As a developer who uses Cursor or Claude Code, I want to install SLOBAC from a marketplace so that I can audit test suites without manually cloning the repo or symlinking skills.

## Requirements

### slobac repo

Add plugin manifests and restructure the skill layout so SLOBAC presents as a single discoverable skill per harness:

- `.cursor-plugin/plugin.json` — Cursor plugin manifest
- `.claude-plugin/plugin.json` — Claude Code plugin manifest

Both manifests describe the plugin (name, description, version, author) and rely on automatic skill discovery from the `skills/` directory tree.

#### Single-skill architecture

The three subagent skills (`scout/`, `batch/`, `cross-suite/`) are folded into `audit/references/subagents/` as raw workflow documents. Only `audit/` remains as a registered skill. This eliminates user-facing clutter (one picker entry, not four) and avoids Cursor's colon→hyphen normalization issue with `name` fields.

Invocation names:

| Harness | Mechanism | Invocation |
|---------|-----------|------------|
| Cursor | SKILL.md `name` field | `/slobac-audit` |
| Claude Code | `plugin-name:folder-name` | `/slobac:audit` |

This requires:

- Migrating `skills/scout/SKILL.md`, `skills/batch/SKILL.md`, `skills/cross-suite/SKILL.md` bodies into `skills/audit/references/subagents/`
- Rewriting the orchestrator's dispatch in `skills/audit/SKILL.md` to use raw subagent prompts instead of skill invocations
- Updating the `name` field from `slobac:audit` → `slobac-audit`
- Deleting the three sibling skill directories
- Updating all documentation (README, CONTRIBUTING, using-slobac, memory bank) to reflect the single-skill layout

### txrk9-agent-plugins repo

Add marketplace catalog files that list the SLOBAC plugin, sourcing it from the `Texarkanine/slobac` GitHub repo:

- `.cursor-plugin/marketplace.json` — Cursor marketplace catalog
- `.claude-plugin/marketplace.json` — Claude Code marketplace catalog

### Out of scope

- Submitting to the official Cursor or Claude Code public marketplaces (that is a follow-on operator action)
- Changes to the skills' runtime detection logic (smell definitions, signals, false-positive guards, prescribed fixes)
