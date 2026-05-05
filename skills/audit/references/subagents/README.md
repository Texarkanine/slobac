<!-- SPDX-FileCopyrightText: 2025 Texarkanine -->
<!-- SPDX-License-Identifier: LicenseRef-PPL-S -->

# Subagent Workflows

This directory contains raw workflow prompts dispatched by the audit orchestrator (`../../SKILL.md`). **These are not registered skills** — they are reference documents that the orchestrator reads at runtime and passes as task descriptions to readonly subagents.

## Dispatch contract

1. The orchestrator resolves the absolute filesystem path to `references/` (its own skill root + `references/`).
2. It reads the appropriate workflow file (e.g., `subagents/scout.md`).
3. It launches a readonly subagent whose task prompt is the workflow file content, supplemented with runtime context variables (target directory, file lists, smell slugs, etc.).
4. The orchestrator passes the absolute `references/` path as a context variable so the subagent can resolve taxonomy entries and format specs at runtime.

## Files

| File | Role |
|------|------|
| `scout.md` | Enumerates test files, measures sizes, emits a Suite Manifest |
| `batch.md` | Reads test files, evaluates per-test/per-file smells, emits findings + behavior summaries |
| `cross-suite.md` | Clusters behavior summaries, performs targeted reads, emits cross-suite findings |
| `exploration-commands.md` | Shell command templates used by the scout for efficient filesystem exploration |

## Path resolution

Workflow files use **relative paths** (e.g., `../docs/taxonomy/<slug>.md`) for human readability when browsing the repository. At runtime, subagents use the **absolute `references/` path** provided by the orchestrator to resolve these files. The relative paths in the workflow text serve as documentation of the file relationships, not as the runtime resolution mechanism.
