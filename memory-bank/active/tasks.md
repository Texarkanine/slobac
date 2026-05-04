# Tasks — Per-skill LICENSES + REUSE.toml

_Stubs only; expand during Plan/BUILD per Niko level-2 workflow._

- [ ] Define canonical file set per skill (which LICENSES/*.txt copies); copy statically from root `LICENSES/` where needed.
- [ ] Add `skills/<skill>/REUSE.toml` for each of four skills.
- [ ] Add `license:` to each `SKILL.md` front matter.
- [ ] Verify: `cd skills/<name> && reuse lint` for each of the four skills (no automation required).

---

## Preflight findings (2026-05-04)

**Result:** FAIL — do not start `/niko-build` until resolved.

1. **Planning incomplete (blocking)** — `tasks.md` does not yet match the Level 2 output format in `.cursor/skills/shared/niko/references/level2/level2-plan.md` (Task header, Test Plan (TDD), numbered Implementation Plan with file paths, Status checkboxes). `memory-bank/active/activeContext.md` still lists **Phase: PLAN - IN-PROGRESS**.

2. **TDD plan encoding (blocking)** — Per preflight rule: each implementable unit must have explicit ordered substeps that place test/verification before production artifacts. The stub checklist has no per-skill or per-file cycles (e.g. expected failing `reuse lint` → add `LICENSES/` + `REUSE.toml` → passing `reuse lint`). The preamble in `projectbrief.md` does not substitute for per-unit ordering in `tasks.md`.

3. **Test / verification mapping (blocking until encoded in plan)** — `memory-bank/techContext.md` states there is no pytest suite yet. The Level 2 plan must either map acceptance to **`cd skills/<name> && reuse lint`** as the observable verification for each skill (TDD-like: lint fails until bundle is complete) or record the operator decision if another harness is introduced. Until that mapping appears in **Test Plan (TDD)** with concrete steps before file-copy work, preflight treats verification as unspecified.

**Non-blocking / advisory**

- Add a **single** optional CI step or script that runs `reuse lint` from each of the four skill roots after implementation — aligns with acceptance criteria and catches regressions; project brief allows skipping convenience wrappers if manual lint suffices.

**Next step:** Run `/niko-plan` to produce the full Level 2 plan in this file, then re-run `/niko-preflight`.
