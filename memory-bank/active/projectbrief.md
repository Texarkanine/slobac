# Project Brief

## User Story

As a developer who uses Cursor or Claude Code, I want to install SLOBAC from a marketplace so that I can audit test suites without manually cloning the repo or symlinking skills.

## Requirements

### slobac repo

Add plugin manifests to expose the SLOBAC skill bundle as a distributable plugin for both harnesses:

- `.cursor-plugin/plugin.json` — Cursor plugin manifest
- `.claude-plugin/plugin.json` — Claude Code plugin manifest

Both manifests describe the plugin (name, description, version, author) and rely on automatic skill discovery from the existing `skills/` directory tree.

Achieving the `/slobac:audit` invocation name in both harnesses requires:

- Renaming the four skill directories from `slobac-*` to short names (`audit/`, `batch/`, `scout/`, `cross-suite/`) — Claude Code derives the skill suffix from the folder name
- Updating the `name` field in each `SKILL.md` from `slobac-audit` → `slobac:audit` etc. — Cursor uses the SKILL.md frontmatter `name` field as the invocation
- Updating all internal cross-references (relative paths, subagent dispatch names) affected by the renames

### txrk9-agent-plugins repo

Add marketplace catalog files that list the SLOBAC plugin, sourcing it from the `Texarkanine/slobac` GitHub repo:

- `.cursor-plugin/marketplace.json` — Cursor marketplace catalog
- `.claude-plugin/marketplace.json` — Claude Code marketplace catalog

### Out of scope

- Submitting to the official Cursor or Claude Code public marketplaces (that is a follow-on operator action)
- Any changes to the skills' runtime detection logic beyond the rename-driven `SKILL.md` name fields, directory names, and reference-path updates required for marketplace packaging
