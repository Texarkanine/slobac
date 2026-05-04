# Active Context

## Current Task: Per-skill LICENSES + REUSE.toml instrumentation
**Phase:** PREFLIGHT — FAIL (complete Level 2 plan in `tasks.md`, then re-run preflight)

## What Was Done

- Classified task as **Level 2** (scoped enhancement across four skill folders: add bundled licenses + per-unit REUSE config + SKILL front matter; no new runtime architecture).
- Reviewed planning export `planning/Claude-Licensing skills with PPL-S on agentskills.io.md` and current repo `REUSE.toml`, canonical `/LICENSES/`, and `skills/*/SKILL.md` layout (none of the skills currently ship local `LICENSES/` or `license:` front matter).
- **Decision:** static committed `LICENSES/` + `REUSE.toml` per skill; **no** Makefile/pyproject reuse helper unless we discover a need. Verification = `cd skills/<name> && reuse lint` per skill.
- **Preflight (2026-05-04):** FAILED — `tasks.md` still stub-only (not Level 2 plan format); missing Test Plan (TDD) and per-unit test-before-artifact ordering; see `tasks.md` Preflight findings and `memory-bank/active/.preflight-status`.

## Next Step

- Run `/niko-plan` to expand `memory-bank/active/tasks.md` per `level2-plan.md` (behaviors, `reuse lint` verification mapping, ordered implementation steps). Then re-run `/niko-preflight` before `/niko-build`.
