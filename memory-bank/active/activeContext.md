# Active Context

**Current Task:** Phase 1 Audit MVP — `deliverable-fossils` + `naming-lies` as harness-portable agent customizations for Cursor and Claude Code.

**Phase:** BUILD (second rework) COMPLETE — next phase QA (autonomous per L3 workflow)

## What Was Done (second rework build)

### Files created

- `skills/slobac-audit/references/docs/taxonomy/*.md` (15 files via `git mv` from `docs/taxonomy/`; Phase-1 entries gained `## False-positive guards` sections; 13 non-Phase-1 entries gained stub guards)
- `docs/taxonomy/<slug>.md` (15 files rewritten as `pymdownx.snippets` wrappers, each containing one `--8<-- ` directive)

### Files modified

- `docs/taxonomy/README.md` — `## False-positive guards` added to the shape spec
- `skills/slobac-audit/SKILL.md` — single-file canonical read (S5a), intra-skill scope-header links (S5b), inline invocation vocabulary migrated from augmentation files (S5c), published-URL governor-rule cite
- `skills/slobac-audit/references/report-template.md` — citation instruction points at intra-skill canonical + published URL for human readers
- `skills/slobac-audit/README.md` — layout tree updated, self-contained-bundle paragraph, absolute GitHub URLs for fixtures, docs-tree-detachment caveat removed
- `memory-bank/techContext.md` — canonical-in-bundle/site-rendered-via-snippet pattern replaces generator-synchronised pattern
- `memory-bank/systemPatterns.md` — structural enforcement wording (S11a), three-deliverables layer authoring surface clarified (S11b), invariant #11 section added with structural enforcement (S11c), canonical-in-bundle authoring model subsection (S11d)
- `memory-bank/active/reflection/reflection-phase-1-audit-mvp.md` — second retraction of insight #2 plus companion retractions

### Files deleted

- `skills/slobac-audit/references/smells/deliverable-fossils.md` (guards → canonical; invocation phrases → SKILL.md; restated content dropped)
- `skills/slobac-audit/references/smells/naming-lies.md` (same treatment)

### Key decisions during build

- **S7 was a no-op.** The first rework's build artifacts (generator script, 15 generated taxonomy copies, CI drift-check step) were never committed — they existed only as uncommitted working-tree changes from the superseded first-rework build, and were discarded at session start via `git checkout -- .` + cleanup. No revert commits needed.
- **False-positive guards content for deliverable-fossils:** migrated `refactor-as-behavior` and `domain vocabulary` guards; dropped `ticket-as-provenance` and `team-specific ticket prefixes` (restated manifesto content per the duplication assessment).
- **False-positive guards content for naming-lies:** migrated all four guards (cross-language synonymy, domain synonymy, under-specified titles, failure-case tests) — all were genuinely unique to the augmentation.

### Integration check results

- `properdocs build --strict`: clean (exit 0, 0.34s). All 15 snippet-include wrappers resolve correctly; `check_paths: true` + `strict: true` verified every target exists.
- B9 (invariant #11 spot-check): `rg '\]\(\.\./\.\./' skills/slobac-audit/` returns zero. No root-escaping links in agent-runtime files.
- B10 (snippet-include rendering): site pages render equivalent content to pre-migration.
- B11 (zero content duplication): no `## Signals`, `## Prescribed Fix`, etc. headers in any `docs/taxonomy/<slug>.md` wrapper.

### Deviations from plan

- None architectural. S7 was a no-op because the first-rework artifacts were never committed. S13 (operator-run harness validation) deferred per plan.

## Next step

QA runs autonomously per L3 workflow Phase Mappings.
