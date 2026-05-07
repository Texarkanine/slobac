# Active Context

- **Current Task:** slobac-audit post-release v1 hardening
- **Phase:** PLAN - COMPLETE
- **What Was Done:** Plan written to `tasks.md`. 19 ordered TDD steps covering A1, A2,
  A3, B4 (generator + dual-target embed + CI drift-check), B5, C8, plus a
  `techContext.md` exception note for the new generator. Test infrastructure
  (`pytest` under a new `[dependency-groups] dev`, scoped to `tests/python/`)
  introduced to support the generator's TDD cycle. Generator emits a 3-column table
  (`Slug | Severity | Detection Scope`), severity-desc + slug-asc, between
  sentinel-bracketed regions in both `SKILL.md` and `taxonomy/README.md`.
- **Next Step:** Run preflight (`niko-preflight` skill).
