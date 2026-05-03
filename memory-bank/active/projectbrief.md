# Project Brief: Audit Orchestration at Scale

## Summary

Implement the Hybrid Scout + Batch + Cross-Suite audit orchestration architecture designed in `creative-audit-orchestration.md`. Evolve the single-agent `slobac-audit` skill into a multi-agent orchestrator, with three new sibling skills (`slobac-scout`, `slobac-batch`, `slobac-cross-suite`) as proper AgentSkills.io skills.

## Requirements

1. **Three new sibling skills** under `skills/`:
   - `slobac-scout` — enumerates test files, measures chars/lines, emits Suite Manifest
   - `slobac-batch` — reads assigned files, assesses per-test + per-file smells, emits findings + behavior summaries
   - `slobac-cross-suite` — receives behavior summaries, clusters by similarity, targeted source reads, emits cross-suite findings

2. **Evolve `slobac-audit/SKILL.md`** into the orchestrator: scout → partition → batch assess → cross-suite assess → synthesize report. Graceful single-agent degradation for small suites (current behavior is a special case).

3. **Add `detection_scope` metadata** to all 15 taxonomy entry header tables (`per-test`, `per-file`, `cross-suite`).

4. **Minimum smell set proving all three scopes (2 each, 6 total):**
   - Per-test: `deliverable-fossils` + `naming-lies` (existing Phase 1)
   - Per-file: `shared-state` + `monolithic-test-file` (both new)
   - Cross-suite: `semantic-redundancy` + `wrong-level` (both new)

5. **Shared references** in `slobac-audit/references/`: behavior summary format spec, any cross-skill contracts.

6. **Cross-skill reference convention**: skills reach into `slobac-audit/references/` for shared content (manifesto, taxonomy, format specs). No skill reaches into another non-audit sibling (~90% rule — real exceptions raised for review, not discarded on principle).

7. **Partitioning heuristic**: scout measures chars/lines, orchestrator does greedy bin-packing with configurable content budget, auto-tunes summary richness based on suite size vs context budget.

## Source Design

Architecture decision: `memory-bank/active/creative/creative-audit-orchestration.md` (Option D selected).
