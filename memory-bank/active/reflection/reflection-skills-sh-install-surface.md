---
task_id: skills-sh-install-surface
date: 2026-07-24
complexity_level: 2
---

# Reflection: skills-sh-install-surface

## Summary

Instrumented SLOBAC for skills.sh / `npx skills` install by documenting the already-working Agent Skills directory — no new packaging JSON. Post-reflect polish dropped the badge and the pytest contract layer; the install command in docs is the deliverable.

## Requirements vs Outcome

Delivered: `npx skills add Texarkanine/slobac --skill slobac-audit` in `using-slobac.md` + README; marketplace path preserved; techContext install pointer updated. Dropped: assumed JSON packaging, `skills.sh.json`, skills.sh badge, and `test_skills_sh_surface.py`.

## Plan Accuracy

Plan was accurate after planning smokes proved discovery/install already worked. The plan over-weighted characterization tests and an optional badge; both were removed after review.

## Build & QA Observations

Build/QA were clean for the initial docs + tests. Later ponytail pass correctly deleted tests that only asserted the repo still looked like itself.

## Insights

### Technical
- skills.sh / vercel-labs/skills treats a public repo with `skills/<name>/SKILL.md` as the publish unit; listing on skills.sh is install-telemetry, not a registry manifest you commit.

### Process
- When the task is "instrument for X," smoke the real client before planning config — it can collapse half the imagined surface. Then cut characterization tests that don't lock a change surface.

### Million-Dollar Question

Nothing notable beyond what we shipped: the elegant form was already the committed `skills/slobac-audit/` tree; the missing piece was telling humans that `npx skills add` is a first-class install path.
