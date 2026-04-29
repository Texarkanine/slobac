# Active Context

**Current Task:** Phase 1 Audit MVP — `deliverable-fossils` + `naming-lies` as harness-portable agent customizations for Cursor and Claude Code.

**Phase:** REFLECT (second rework) COMPLETE — next phase Archive

## Reflect Summary

Reflection covered the full second-rework lifecycle (Preflight → Build → QA → Reflect). Key observations:

- **Requirements vs Outcome:** All requirements met. 15 entries migrated, snippet wrappers created, false-positive guards promoted/stubbed, augmentation files deleted, SKILL.md rewritten, `properdocs build --strict` passes. S7 was a no-op (first-rework artifacts never committed).
- **Plan accuracy:** The 14-step plan (S1–S14) was accurate as amended by preflight (PF1: S4a for README shape spec, PF2: S1+S2 combined commit). No reordering or splitting needed.
- **Creative phase:** OQ3 Option γ held up perfectly. The calibration discipline (asking "what will the operator's reaction be?") was not stress-tested but remains worth carrying forward.
- **Build/QA:** One trivial QA fix (stale "augmentation file" reference in SKILL.md Constraints). Shell connectivity glitch mid-session caused one phantom commit but no data loss.

### Persistent file reconciliation

- `productContext.md`: fixed stale `references/smells/<slug>.md` reference → `references/docs/taxonomy/<slug>.md`
- `systemPatterns.md`: clean (updated during S11)
- `techContext.md`: clean (updated during S10)

### Key insights

- **Technical:** Snippet-include (`pymdownx.snippets` + `check_paths: true` + `strict: true`) inverts the authoring surface without losing the reader surface. Zero-maintenance sync mechanism — no generator, no CI drift step. Future skills needing canonical content consumed by a rendered site should use this pattern. `git mv` preserves blame history across the inversion.
- **Process:** When multiple creative-phase passes fail at the same architectural boundary, the constraint itself may be wrong — escalate to the operator before the next attempt. Uncommitted build artifacts from a superseded rework are a *feature* (they evaporate cleanly when the workflow's phase-gating prevents the rework from reaching commit).

## Next step

Run `/niko-archive` to create the archive document and finalize the current project.
