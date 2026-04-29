# Active Context

**Current Task:** Phase 1 Audit MVP — `deliverable-fossils` + `naming-lies` as harness-portable agent customizations for Cursor and Claude Code.

**Phase:** BUILD (third rework) — COMPLETE; next phase QA (auto-transition)

## Build Summary

All 10 implementation steps executed with no deviations from plan:

- **T1:** Atomic move of remaining docs files (`index.md`, `principles.md`, `glossary.md`, `workflows.md`, `taxonomy/README.md`, `.pages`) into `skills/slobac-audit/references/docs/` via `git mv`. Deleted 15 snippet-include wrappers. Updated `properdocs.yml` `docs_dir` and `edit_uri`. Single commit.
- **T2:** SKILL.md Constraints section rewritten (pre-inversion "audit cites the manifesto" → "canonical entries are the single source of truth"). Governor-rule cite changed from published URL to intra-skill path (file is now inside skill root).
- **T3:** Fixture expected-findings updated: `../../../../docs/` relative paths → published URLs. Stale `references/smells/` refs → canonical entry refs. Fixture README stale refs fixed.
- **T4:** Skill README layout expanded with non-taxonomy docs files. Canonical paragraph broadened to full-manifesto-in-bundle.
- **T5:** Repo-root README entry-point links and docs publishing paragraph updated. T5d (PF1 amendment): 14 `../docs/` refs in `planning/VISION.md` → published URLs.
- **T6:** techContext: snippet pattern → full-manifesto-in-bundle pattern. Opening paragraph, skill layout, editing paragraph, anticipated-tooling glossary link all updated.
- **T7:** systemPatterns: opening paragraph, three-deliverables-layer, cross-link refs, authoring-model subsection, invariant #11 section all updated.
- **T8:** Reflection third-rework evolution note added.
- **T9:** `properdocs build --strict` passes clean (B10, B13 verified).
- **T10:** Invariant #11 spot-check passes (zero cross-root escapes in agent-runtime files).

## Files Modified

- `properdocs.yml` — `docs_dir` and `edit_uri` updated
- `skills/slobac-audit/SKILL.md` — Constraints section + governor-rule cite
- `skills/slobac-audit/README.md` — layout + canonical paragraph
- `skills/slobac-audit/references/docs/` — 6 files moved in (git mv)
- `skills/slobac-audit/references/report-template.md` — unchanged (path was already correct)
- `tests/fixtures/audit/deliverable-fossils/expected-findings.md` — path refs updated
- `tests/fixtures/audit/naming-lies/expected-findings.md` — path refs updated
- `tests/fixtures/audit/README.md` — stale refs fixed
- `README.md` — entry-point links + docs publishing section
- `planning/VISION.md` — 14 `../docs/` refs → published URLs
- `memory-bank/techContext.md` — full-manifesto-in-bundle pattern
- `memory-bank/systemPatterns.md` — full rewrite of docs-related sections
- `memory-bank/active/reflection/reflection-phase-1-audit-mvp.md` — third-rework note

## Files Deleted

- 15 snippet-include wrappers at `docs/taxonomy/*.md`
- `docs/` directory (emptied by moves + deletions)

## Next Step

QA review runs automatically per L3 workflow.
