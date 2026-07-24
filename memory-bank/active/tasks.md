# Task: skills-sh-install-surface

* Task ID: skills-sh-install-surface
* Complexity: Level 2
* Type: simple enhancement

Make SLOBAC's existing `skills/slobac-audit/` package discoverable and documented for install via skills.sh / `npx skills` (vercel-labs/skills). Planning verification already shows discovery and full-directory install work with no new packaging format; remaining work is docs, a small discoverability regression guard, and optional leaderboard badge / install-seed note.

## Test Plan (TDD)

### Behaviors to Verify

- [B1 discoverability frontmatter]: reading `skills/slobac-audit/SKILL.md` → YAML frontmatter contains non-empty `name` and `description` (CLI discovery contract per vercel-labs/skills README).
- [B2 install package shape]: the skill root contains `SKILL.md`, `references/`, and `LICENSES/` → sidecar content required for a useful install is present in-repo (what rides along with `npx skills add`).
- [B3 docs install path]: `skills/slobac-audit/references/docs/using-slobac.md` documents an `npx skills add` install command for this repo → consumers can find the skills.sh path without the marketplace-only path.
- [B4 no niko leak]: `npx skills add <repo> --list` reports only product skills (today: `slobac-audit`), not authoring skills under `.cursor/skills/` → already true empirically; keep as manual/CLI smoke, not a pytest that shells out to npx.
- [Edge marketplace preserved]: after docs edits, `using-slobac.md` still documents the txrk9-agent-plugins marketplace path → additive, not a replacement.
- [Edge properdocs]: `uv run properdocs build --strict` still passes after docs edits → no broken links from new install section.

### Test Infrastructure

- Framework: pytest (`pyproject.toml` `[dependency-groups] dev`, `testpaths = ["tests/python"]`)
- Test location: `tests/python/unit/`
- Conventions: `test_*.py` modules; fixtures via `tests/python/conftest.py`; no network in unit tests
- New test files: `tests/python/unit/test_skills_sh_surface.py`
- Manual/CLI smoke (not CI unit): `npx skills add . --list` and optional `--skill slobac-audit --copy` into a temp dir (already green in planning)

## Implementation Plan

1. **RED — discoverability / layout / docs-contract tests**
   - Files: `tests/python/unit/test_skills_sh_surface.py` (new)
   - Changes: add tests for B1–B3 and Edge marketplace preserved in one module. Assert: (a) SKILL.md frontmatter `name`/`description` non-empty; (b) skill root has `references/` + `LICENSES/`; (c) `using-slobac.md` contains `npx skills add` and `Texarkanine/slobac`; (d) `using-slobac.md` still mentions `txrk9-agent-plugins`. Expect RED on (c) until step 2; (a)(b)(d) may already be green as characterization locks.

### Preflight Amendments

- Marketplace preservation is a required assertion in `test_skills_sh_surface.py`, not docs-only QA.
- Do not add plugin/registry JSON unless a post-docs CLI smoke regresses (none expected).

2. **GREEN — document skills.sh / `npx skills` install path**
   - Files: `skills/slobac-audit/references/docs/using-slobac.md`
   - Changes: expand `## Install` to lead with (or equally present) `npx skills add Texarkanine/slobac` (optionally `--skill slobac-audit`), note that the full skill directory including `references/` is installed, keep marketplace path as an alternate; brief note that skills.sh listing is install-telemetry-driven (no separate publish step)

3. **GREEN — surface install path from repo README**
   - Files: `README.md`
   - Changes: under "Apply It with AI", add a concrete `npx skills add Texarkanine/slobac` command (and link to using-slobac for details); optional skills.sh badge `https://skills.sh/b/Texarkanine/slobac` once wording is settled (badge may be empty/`inaccessible` until a public install seeds telemetry — acceptable)

4. **Align contributor/install context pointers**
   - Files: `memory-bank/techContext.md` (surgical update to install paragraph only)
   - Changes: mention skills.sh / `npx skills add Texarkanine/slobac` as an additive install path alongside the marketplace catalog; do not invent a new packaging story

5. **Verify gates**
   - Files: none (commands)
   - Changes: run new pytest file → full `tests/python` suite → `uv run properdocs build --strict`; re-run `npx skills add . --list` smoke

6. **Explicit non-changes**
   - Files: `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json`, `skills/slobac-audit/SKILL.md` body/taxonomy layout
   - Changes: none required — CLI already discovers `skills/slobac-audit` via standard `skills/` scan; no new registry JSON or tarball step

## Technology Validation

No new technology - validation not required. Existing stack: `npx skills` (external CLI, already smoke-tested against this checkout), pytest, properdocs.

## Dependencies

- Public GitHub source `Texarkanine/slobac` for the documented owner/repo install string
- `npx` available for manual smoke (not a runtime dependency of the repo)

## Challenges & Mitigations

- **Challenge: operator expected a new JSON config, but discovery already works**: Mitigation: document the finding in progress/reflection; ship docs + contract tests instead of inventing unused config.
- **Challenge: skills.sh badge/page empty until telemetry**: Mitigation: docs state there is no publish step; badge is optional/cosmetic; first public `npx skills add` seeds the leaderboard.
- **Challenge: prose-pin smell if tests assert exact marketing copy**: Mitigation: assert presence of the install command substring `npx skills add` + repo identifier, not full paragraph text; keep marketplace path assertion similarly loose.
- **Challenge: npx in CI is slow/networked**: Mitigation: unit tests are filesystem/static only; CLI smoke stays manual/preflight/QA.

## Pre-Mortem

- **Plan failed because we added fake packaging JSON that skills.sh ignores, creating dual sources of truth**: Cut JSON from scope (already covered by Challenge 1 / Implementation step 6); do not add `.claude-plugin` skills arrays unless a real discovery gap appears.
- **Plan failed because docs replaced marketplace install and broke Cursor/Claude plugin users**: Require additive Install section (Edge marketplace preserved).
- **Plan failed because we treated skills.sh listing as a config file problem and never verified CLI behavior**: Already disproven in planning via `--list` and `--copy` smokes; keep those as QA gate.

## Implementation Progress

- [x] Step 1 — RED tests (`test_skills_sh_surface.py`)
- [x] Step 2 — GREEN `using-slobac.md` skills.sh install section
- [x] Step 3 — README install command + skills.sh badge
- [x] Step 4 — `techContext.md` install pointer
- [x] Step 5 — pytest + properdocs + `npx skills --list` smoke
- [x] Step 6 — no plugin JSON changes (confirmed unnecessary)

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA
