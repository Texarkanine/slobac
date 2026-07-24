---
task_id: skills-sh-install-surface
date: 2026-07-24
complexity_level: 2
---

# Reflection: skills-sh-install-surface

## Summary

Instrumented SLOBAC for skills.sh / `npx skills` install by documenting the already-working Agent Skills directory layout and locking that contract with pytest — no new packaging JSON required.

## Requirements vs Outcome

Delivered: discoverable install (`npx skills add Texarkanine/slobac --skill slobac-audit`), docs in `using-slobac.md` + README (+ badge), marketplace path preserved, techContext install pointer updated. Dropped only the assumed "new JSON config" — verified unnecessary against the live CLI.

## Plan Accuracy

Plan was accurate after planning smokes proved discovery/install already worked. Sequence (tests → docs → README → techContext → gates) held. Main surprise was that the operator's JSON hypothesis was the wrong half of the work.

## Build & QA Observations

Build was clean after one intentional RED on the docs contract. QA only trimmed an overbuilt frontmatter parser down to regex presence checks.

## Insights

### Technical
- skills.sh / vercel-labs/skills treats a public repo with `skills/<name>/SKILL.md` as the publish unit; listing on skills.sh is install-telemetry, not a registry manifest you commit.

### Process
- When the task is "instrument for X," smoke the real client before planning config — it can collapse half the imagined surface.

### Million-Dollar Question

Nothing notable beyond what we shipped: the elegant form was already the committed `skills/slobac-audit/` tree; the missing piece was telling humans (and locking the contract) that `npx skills add` is a first-class install path.
