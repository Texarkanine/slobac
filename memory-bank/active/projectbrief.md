# Project Brief

## User Story

As a maintainer distributing Agent Skills outside the monorepo (marketplaces, tarballs), I want each skill under `skills/` to ship its own `LICENSES/` texts and scoped `REUSE.toml` so that recipients get SPDX-correct, AGPL-complete attribution without the repo root.

## Use-Case(s)

### Use-Case 1

Someone installs only `slobac-audit` (or another skill) from a marketplace; the folder is the distribution unit and must be REUSE-valid and agentskills-friendly on its own.

### Use-Case 2

Repo-root `REUSE.toml` remains authoritative for the full tree; per-skill configs intentionally duplicate policy for standalone bundles (same pattern as distro packages re-shipping copyright files).

## Requirements

1. Every skill at `skills/*/SKILL.md` has bundled license texts under that skill’s `LICENSES/` using REUSE-required layout and filenames aligned with SPDX identifiers.
2. Every skill has a `REUSE.toml` whose paths are relative to the skill root and mirror repo policy (PPL-S for prompt-shaped payload, CC-BY-SA-4.0 for `slobac-audit` docs subtree, etc.).
3. `SKILL.md` YAML front matter includes a `license:` string that points humans and validators at the bundle (headline = primary license; details in `LICENSES/` + `REUSE.toml`).
4. AGPL-3.0-or-later full text is bundled wherever PPL-S is claimed (PPL-S extends AGPL by reference).
5. **Static only:** commit license texts and `REUSE.toml` in each skill tree (same content as root where applicable). No requirement for Makefile, `pyproject.toml` scripts, or generators unless we later decide hygiene warrants it.

## Constraints

1. Follow [REUSE spec](https://reuse.software/) for `LICENSES/` folder name and license file naming tied to identifiers.
2. Keep redundancy between root and per-skill metadata intentional and documented.
3. Do not claim license on vendored unknown upstream content (use `LicenseRef-NOASSERTION` only if such paths exist inside a skill).
4. **No wrapper scripts by default:** if `cd skills/<name> && reuse lint` passes for each skill, do not add a `reuse` entry to `pyproject.toml` or similar solely for convenience.

## Acceptance Criteria

1. For each skill, `cd skills/<name> && reuse lint` succeeds (that directory is a valid REUSE project root).
2. All four skills (`slobac-audit`, `slobac-batch`, `slobac-cross-suite`, `slobac-scout`) contain `LICENSES/` + `REUSE.toml`; `slobac-audit` additionally licenses `references/docs/**` as CC-BY-SA-4.0 with that text present.
3. Each `SKILL.md` has a `license:` field consistent with the bundled files.
