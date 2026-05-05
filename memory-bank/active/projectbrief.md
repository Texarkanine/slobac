# Project Brief

## User Story

As a developer who uses Cursor or Claude Code, I want to install SLOBAC from a marketplace so that I can audit test suites without manually cloning the repo or symlinking skills.

## Requirements

### slobac repo

Add plugin manifests to expose the SLOBAC skill bundle as a distributable plugin for both harnesses:

- `.cursor-plugin/plugin.json` — Cursor plugin manifest
- `.claude-plugin/plugin.json` — Claude Code plugin manifest

Both manifests describe the plugin (name, description, version, author) and rely on automatic skill discovery from the existing `skills/` directory tree. No changes to any `SKILL.md` file.

### txrk9-agent-plugins repo

Add marketplace catalog files that list the SLOBAC plugin, sourcing it from the `Texarkanine/slobac` GitHub repo:

- `.cursor-plugin/marketplace.json` — Cursor marketplace catalog
- `.claude-plugin/marketplace.json` — Claude Code marketplace catalog

### Out of scope

- Modifying any `SKILL.md` file in slobac
- Submitting to the official Cursor or Claude Code public marketplaces (that is a follow-on operator action)
- Any changes to the skills' runtime behavior
