---
task_id: slobac-plugin-distribution
complexity_level: 3
date: 2026-05-05
status: completed
---

# TASK ARCHIVE: Expose SLOBAC as Cursor + Claude Code Plugin

## SUMMARY

SLOBAC is distributable as a **single-skill** plugin for Cursor and Claude Code via plugin manifests in the `slobac` repo and marketplace catalog entries in `txrk9-agent-plugins`. Users install from the marketplace instead of cloning and symlinking skills.

The work proceeded in **two builds**. The first implementation renamed skill directories to short names (`audit`, `scout`, `batch`, `cross-suite`), set SKILL.md `name` values to the `slobac:*` form, added `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json`, updated documentation and REUSE/properdocs paths, and added Cursor and Claude marketplace JSON files in `txrk9-agent-plugins`. **QA failed** on an operator smoke test in Cursor: invocation naming did not match the plan’s assumptions (colons, plugin prefix).

A **plan revision** adopted a **single-skill architecture**: the orchestrator remains `skills/audit/` as the only registered skill; former subagent SKILL bodies were folded into `skills/audit/references/subagents/` (`scout.md`, `batch.md`, `cross-suite.md`) as **raw workflow prompts** dispatched by the orchestrator (Task/Agent tools), not separate registered skills. The orchestrator SKILL.md uses `name: slobac-audit` for Cursor (hyphen form after platform normalization). Claude Code continues to resolve `plugin-name:folder-name` as `/slobac:audit`. Sibling skill directories `skills/scout/`, `skills/batch/`, and `skills/cross-suite/` were removed after migration.

## REQUIREMENTS

- **Plugin manifests (`slobac`):** `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json` with metadata and skill discovery from `skills/`.
- **Marketplace catalogs (`txrk9-agent-plugins`):** `.cursor-plugin/marketplace.json` and `.claude-plugin/marketplace.json` listing the `slobac` plugin with GitHub source `Texarkanine/slobac`.
- **Single discoverable skill per harness:** one picker entry; subagent workflows are internal reference documents, not user-facing skills.
- **Invocation targets:** Cursor → `/slobac-audit` (SKILL `name` behavior); Claude Code → `/slobac:audit`.
- **Documentation:** `using-slobac.md`, READMEs, CONTRIBUTING, memory bank (`techContext`, `systemPatterns`) aligned with install and layout.
- **Compliance:** `properdocs` strict build and REUSE lint remain green; SPDX/report naming conventions preserved where specified (e.g. output artifact `slobac-audit.md`, `SPDX-PackageName` where applicable).
- **Explicitly out of scope:** submitting to official public marketplaces (operator follow-up); changes to core smell-detection logic.

## IMPLEMENTATION

### First build (multi-skill, later superseded)

- Renamed `skills/slobac-*` directories to `skills/audit`, `skills/scout`, `skills/batch`, `skills/cross-suite` (`git mv`).
- Updated all four SKILL.md files, READMEs, `properdocs.yml` (`docs_dir` / `edit_uri`), root `REUSE.toml` paths, `CONTRIBUTING.md`, repo `README.md`, and `skills/audit/references/docs/using-slobac.md` for marketplace-oriented install instructions.
- Added plugin JSON manifests at repo root under `.cursor-plugin/` and `.claude-plugin/`.
- In `txrk9-agent-plugins`, added marketplace catalogs and updated `README.md` for the marketplace description.

### Revision (single-skill, final shape)

- Created `skills/audit/references/subagents/` and migrated content from the three sibling skills into `scout.md`, `batch.md`, `cross-suite.md` (workflow text for raw subagent prompts; paths adjusted relative to `references/`).
- Relocated `exploration-commands.md` under `skills/audit/references/` (accepted deviation from an earlier plan line that said `subagents/`; references resolve correctly).
- Rewrote `skills/audit/SKILL.md`: `name: slobac-audit`; dispatch steps instruct reading `references/subagents/*.md` and launching readonly subagents with that content plus context (including an absolute `references/` path for taxonomy and format files).
- Removed `skills/scout/`, `skills/batch/`, `skills/cross-suite/` from the tree.
- Updated `skills/audit/README.md`, `using-slobac.md`, CONTRIBUTING (detection-scope table without separate subagent skill names), `memory-bank/techContext.md`, and `memory-bank/systemPatterns.md`.
- **Unchanged by revision:** plugin manifest locations and `skills` path; `txrk9-agent-plugins` catalog structure; `properdocs.yml` docs root still under `skills/audit/references/docs`.

### Creative phase

No formal creative-phase documents were produced; the `memory-bank/active/creative/` directory was empty. Architecture choices for the revision were made during **plan revision** using QA evidence (Cursor naming) and UX goals (single picker entry).

## TESTING

- **CI-style gates:** `uv run properdocs build --strict` from repo root; `reuse --root . lint` from `skills/audit/` (and monorepo reuse where applicable per task log).
- **Stale-reference grep:** searches for old skill paths and removed `slobac:*` subagent invocations — clean outside ephemeral planning/active paths after revision.
- **Preflight:** three preflight passes across plan versions caught gaps including missing `properdocs.yml` / root `REUSE.toml` / `CONTRIBUTING.md` / `README.md` updates and TDD gate ordering (baseline RED/GREEN sequencing).
- **QA:** First QA failed on **operator Cursor smoke test** (actual invocation names). Second QA passed after README fix in `txrk9-agent-plugins` for single-skill wording; one accepted deviation noted for `exploration-commands.md` placement.

## LESSONS LEARNED

- **Cursor plugin naming is poorly documented and behaviorally opaque:** colons in SKILL `name` are normalized (e.g. to hyphens), and the plugin name is not necessarily prefixed the way the original plan assumed. **Empirical smoke tests** in the target harness are mandatory for distribution work—not optional polish.
- **Single-skill + reference-backed subagent workflows** avoids duplicate picker entries and cross-harness registration quirks; the orchestrator owns the dispatch contract.
- **Preflight paid off:** seven concrete gaps across three runs that would have broken CI or left stale docs—especially sequencing so `properdocs.yml` is updated before gates that run properdocs.
- **After a major architecture revision, re-audit every “no change needed” item** from the prior plan (e.g. sibling-repo READMEs); stale assumptions caused a trivial but real QA fix in `txrk9-agent-plugins/README.md`.

## PROCESS IMPROVEMENTS

- Treat **operator smoke tests** for Cursor/Claude install and slash-command resolution as **blocking QA**, not post-hoc verification, when the task depends on platform integration behavior.
- When the plan changes structurally, **re-run a repo-wide consistency pass** (README, marketplace repo, docs) even if those paths were unchanged in the revision delta.
- Continue **TDD-style sequencing** (baseline green, intentional red where valuable, then green) for rename-heavy work; deferring all checks to the end was explicitly flagged and corrected twice in preflight.

## TECHNICAL IMPROVEMENTS

- Consider a short **`references/subagents/README.md`** for contributors documenting that these files are orchestrator-dispatched workflows, not registered skills, and what context the orchestrator passes (recommended during preflight as optional; not required for completion).

## NEXT STEPS

- **Operator:** Optionally submit the plugin to official Cursor and Claude Code public marketplaces when ready (explicitly out of scope for this task).
- **None** required in-repo for task closure; memory bank ephemeral files are cleared after this archive.
