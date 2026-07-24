# Active Context

## Current Task: skills-sh-install-surface
**Phase:** BUILD - COMPLETE

## What Was Done
- Added `tests/python/unit/test_skills_sh_surface.py` (RED on docs contract, then GREEN).
- Documented `npx skills add Texarkanine/slobac --skill slobac-audit` in `using-slobac.md` (marketplace path retained as alternate).
- Surfaced install command + skills.sh badge in `README.md`.
- Updated `memory-bank/techContext.md` install paragraph.
- Verified: 28 pytest pass, `properdocs build --strict` pass, `npx skills add . --list` finds `slobac-audit`.

## Files Modified
- `/home/mobaxterm/git/slobac/tests/python/unit/test_skills_sh_surface.py` (new)
- `/home/mobaxterm/git/slobac/skills/slobac-audit/references/docs/using-slobac.md`
- `/home/mobaxterm/git/slobac/README.md`
- `/home/mobaxterm/git/slobac/memory-bank/techContext.md`

## Key Decisions
- No plugin/registry JSON added — CLI discovery already works against `skills/`.
- skills.sh badge included; may show empty until public install telemetry.

## Next Step
- QA phase (automatic).
