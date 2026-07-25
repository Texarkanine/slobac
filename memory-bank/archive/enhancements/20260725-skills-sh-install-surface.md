---
task_id: skills-sh-install-surface
complexity_level: 2
date: 2026-07-25
status: completed
---

# TASK ARCHIVE: skills.sh / npx skills Install Surface

## SUMMARY

Documented SLOBAC as installable via skills.sh / `npx skills` (vercel-labs/skills). Planning smokes showed discovery and full-directory install already worked against `skills/slobac-audit/` — no new packaging JSON. Deliverable is the install command in `using-slobac.md` + README (marketplace path kept additive) and a surgical `techContext.md` install pointer. Post-reflect polish removed an empty skills.sh badge and deleted characterization pytest that only locked already-true layout/docs strings.

## REQUIREMENTS

- Make the repo discoverable/installable via skills.sh / `npx skills` with minimal surface.
- Document the skills.sh install path where install guidance already lives; keep Cursor/Claude marketplace path.
- Prefer full skill directories with `SKILL.md` frontmatter; no new packaging/tarball/flatten step.
- Do not redesign the skill body or taxonomy layout.

## IMPLEMENTATION

- **Docs:** `skills/slobac-audit/references/docs/using-slobac.md` — `npx skills add Texarkanine/slobac --skill slobac-audit` plus marketplace one-liner alternate.
- **README:** concrete `npx skills add` under "Apply It with AI" (skills.sh badge added then removed when empty pending telemetry).
- **Memory bank (persistent):** `techContext.md` install paragraph mentions skills.sh alongside marketplace.
- **Explicit non-changes:** no `.cursor-plugin` / `.claude-plugin` skills arrays, no `skills.sh.json`, no SKILL.md body/taxonomy edits — CLI already discovers via standard `skills/` scan.
- **Post-reflect cut:** deleted `tests/python/unit/test_skills_sh_surface.py` (frontmatter/layout/docs prose-pin characterization).

## TESTING

- **Planning smoke:** `npx skills add . --list` → only `slobac-audit`; `--copy` install preserved `references/` / taxonomy.
- **Build/QA:** full pytest suite green (28 with contract tests; later suite after deletion); `uv run properdocs build --strict` green; `/niko-qa` PASS.
- **Post-polish:** docs-only surface; no automated lock on the install string.

## LESSONS LEARNED

- skills.sh / vercel-labs/skills treats a public repo with `skills/<name>/SKILL.md` as the publish unit; listing on skills.sh is install-telemetry, not a committed registry manifest.
- When the task is "instrument for X," smoke the real client before planning config — it can collapse half the imagined surface.
- Characterization tests that assert the repo still looks like itself rarely earn their keep; cut them once the real change surface is docs-only.

## PROCESS IMPROVEMENTS

- For discovery/install tasks, run the consumer CLI (`npx skills add --list` / `--copy`) in planning before drafting packaging JSON or contract tests.

## TECHNICAL IMPROVEMENTS

- None. The elegant form was already the committed `skills/slobac-audit/` tree; humans needed the install command documented.

## NEXT STEPS

- Optional: seed skills.sh leaderboard/telemetry with a public `npx skills add Texarkanine/slobac` once desired; badge can return then.
- Merge PR #35 (`docs/skills-sh-install-surface`) when ready.

---

## Inlined reflection (ephemeral collapsed)

_Source: `reflection-skills-sh-install-surface.md` — deleted during archive._

**Requirements vs outcome:** Delivered install command in using-slobac + README; marketplace preserved; techContext updated. Dropped assumed JSON packaging, `skills.sh.json`, skills.sh badge, and `test_skills_sh_surface.py`.

**Plan accuracy:** Accurate after planning smokes proved discovery/install already worked. Plan over-weighted characterization tests and an optional badge; both removed after review.

**Build & QA:** Clean for initial docs + tests. Later ponytail pass correctly deleted tests that only asserted the repo still looked like itself.

**Million-dollar question:** Nothing notable beyond what shipped — the missing piece was telling humans that `npx skills add` is a first-class install path.
