# Project Brief

## User Story

As a SLOBAC maintainer, I want this repository installable via skills.sh (`npx skills` / vercel-labs/skills) so that consumers can discover and install `/slobac-audit` without relying only on the existing Cursor/Claude plugin marketplace path.

## Use-Case(s)

### Use-Case 1

An operator runs `npx skills add Texarkanine/slobac` (or an equivalent listed install command) and gets the `slobac-audit` skill directory with `SKILL.md` and sidecar folders (`references/`, etc.) intact.

### Use-Case 2

A reader of the README / using-slobac docs learns about the skills.sh install path alongside the existing marketplace install instructions.

## Requirements

1. Instrument the repo so skills.sh / `npx skills` can discover and install the published skill(s).
2. Add documentation blurbs for the skills.sh install path where install guidance already lives (or should live for discoverability).
3. Prefer the minimal surface implied by the working model: full skill directories with `SKILL.md` YAML frontmatter; no new packaging/tarball/flatten step.
4. Validate against the claim that skills.sh is a discovery/leaderboard surface whose install path is vercel-labs/skills — adjust only if verification shows a real gap.

## Constraints

1. Do not redesign the skill body or taxonomy layout for this task; the existing `skills/slobac-audit/{SKILL.md,references/,...}` shape is presumed compatible.
2. Do not expand scope into security review of the open registry, symlink-bug workarounds for consumers, or lockfile pinning guidance beyond what is needed for *publishing* this repo.
3. Preserve existing Cursor/Claude plugin marketplace install paths; skills.sh is additive.

## Acceptance Criteria

1. `npx skills add` (or `--list`) against this repo discovers `slobac-audit` with valid `name`/`description` frontmatter.
2. Install docs mention the skills.sh / `npx skills` path.
3. Any JSON/plugin config changes required for discovery are present and consistent with existing plugin manifests.
