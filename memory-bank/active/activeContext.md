# Active Context

**Current Task:** Phase 1 Audit MVP — `deliverable-fossils` + `naming-lies` as harness-portable agent customizations for Cursor and Claude Code.

**Phase:** PLAN (third rework) — IN-PROGRESS

## What Triggered This Rework

Pre-merge review of the second-rework artefacts surfaced two remaining seams:

1. SKILL.md Constraints section uses stale pre-inversion language ("audit cites the manifesto; it does not fork it") — architecturally wrong under the canonical-in-bundle model where the skill *is* the manifesto's home.
2. The 15 snippet-include wrappers at `docs/taxonomy/*.md` are pure routing indirection. They exist because `properdocs.yml` has `docs_dir: docs` but the canonical content lives inside the skill. If properdocs points directly at the skill's content, the wrappers evaporate.

Operator's direction: move the entire `docs/` tree into `skills/slobac-audit/references/docs/`, point `properdocs.yml` at it, and delete the now-empty `docs/`. Also includes: the operator's already-made SKILL.md edit (intro removal, heading flattening).

## What This Preserves

- All fixtures and expected-findings files (content unchanged; path references updated)
- The skill workflow (Steps 1–6), detection logic, report template, all unchanged in behavior
- The taxonomy entry shape (all 15 canonical entries untouched in content)
- Invariant #11 (structurally stronger — full manifesto inside the skill root)
- `properdocs build --strict` as the CI integrity gate

## Next Step

Write the implementation plan to `tasks.md`.
