# Project Brief: Onboard Remaining 9 Smells

## User Story

The audit orchestration framework (archived 2026-05-03) made 6 of 15 taxonomy smells first-class supported slugs in `slobac-audit`. The remaining 9 — all per-test scope — are still in the manifesto but are not in the SKILL's supported list and have no fixtures proving detection. We want to onboard them so the framework reaches parity with the taxonomy.

## Smells to Onboard

All 9 are **per-test** scope (already verified from the creative-phase classification table in the archived task):

1. `vacuous-assertion`
2. `tautology-theatre`
3. `pseudo-tested`
4. `over-specified-mock`
5. `implementation-coupled`
6. `presentation-coupled`
7. `conditional-logic`
8. `mystery-guest`
9. `rotten-green`

## Requirements

For each of the 9 smells:

1. Add the slug to the **Supported smells** table in `skills/slobac-audit/SKILL.md` (per-test row).
2. Add natural-phrase mappings for the slug in the SKILL's intent-mapping bullets.
3. Verify the taxonomy entry at `skills/slobac-audit/references/docs/taxonomy/<slug>.md` carries the correct `Detection Scope: per-test` header (added uniformly in the prior task — verification only).
4. Create a fixture under `tests/fixtures/audit/<slug>/` with:
   - At least one planted Python test demonstrating the smell.
   - At least one negative-control test that does **not** trigger the smell.
   - An `expected-findings.md` aligned with the report-template conventions used by existing fixtures.
5. Update `tests/fixtures/audit/README.md` if it enumerates fixtures.

## Constraints / Quality Gates

- `properdocs build --strict` must remain green.
- Existing 6-smell behavior must remain unchanged (no regressions in `slobac-audit/SKILL.md` for the already-supported slugs).
- No orchestrator surgery — all 9 are per-test, so the existing batch-assessor routing is sufficient.
- Fixtures may be one-per-smell or combined where natural; either is acceptable.

## Out of Scope

- Apply layer / fix automation.
- Cross-suite extensions (none of the 9 are cross-suite scope).
- Multi-scope combined fixture (noted as a non-blocking advisory in the prior preflight; remains a future enhancement).

---

## Rework — 2026-05-04

The original implementation reached 15-smell parity but did so by **inlining manifesto content into `skills/slobac-audit/SKILL.md`**: a 15-row supported-slugs table and a 15-bullet natural-phrase map. With every taxonomy addition, this surface compounds — and the fan-out of "supported slugs" already spans SKILL.md, both READMEs, and `techContext.md`. Two follow-up cleanups surfaced in post-reflect operator review:

### Rework requirement R1 — delegate slug enumeration and operator vocabulary to per-entry taxonomy content

The set of supported slugs is now **structurally** the set of files at `references/docs/taxonomy/*.md` (excluding `README.md`). The duplicate enumeration in SKILL.md is purely a mirror that drifts.

- Drop the `Supported smells (N)` table from `skills/slobac-audit/SKILL.md` Step 2. Replace with an instruction that the supported set is enumerated by the existence of `references/docs/taxonomy/<slug>.md`; refuse any slug whose entry does not exist.
- Move the natural-phrase mapping out of SKILL.md and into each taxonomy entry as a uniform `## Natural phrases` (or equivalent) section. Update `references/docs/taxonomy/README.md` shape SoT to require the new section. SKILL.md Step 2 instructs the agent to resolve operator phrasing by reading each entry's `Summary` + `Natural phrases` sections.
- Detection-scope partitioning logic continues to read each entry's header `Detection Scope` field — that part already worked structurally and only the mirror table goes away.
- The human-facing supported-smells table in `skills/slobac-audit/README.md` is **not** in scope to delete — that's contributor documentation, not agent instructions, and a human-readable mirror is legitimate there. But its lead-paragraph count line must stop saying a specific number — replace `"Supports all 15 manifesto smells"` with phrasing equivalent to `"supports every smell defined in the manifesto"`. Same logic for `memory-bank/techContext.md`'s lead summary.

### Rework requirement R2 — elide harness-specific dispatch examples

`SKILL.md` currently names `Task` (Cursor) and `dispatch_agent` (Claude Code) at three dispatch sites (Step 3 scout, Step 5 batch, Step 7 cross-suite). Harness primitives evolve outside SLOBAC's release cadence; SLOBAC has no CI gate that would catch drift; agents reading the SKILL already know their own subagent primitive without prompting.

- At each of the three dispatch sites, replace the Cursor / Claude Code / Other harnesses bullet block with a single uniform sentence that instructs the agent to launch a readonly subagent with the named skill, providing the listed inputs.
- The replacement is **agent-facing instruction only** — no contributor rationale, no meta-note explaining why the harness names were dropped. SKILL.md is for agents; rationale belongs in `slobac-audit/README.md` or commit messages.

### Rework non-requirements

- The Step 8 dedup rule at SKILL.md line 165 is **fine as-is** — operator clarified after re-reading that the rule is correctly scoped to "same smell slug" and only fires for `deliverable-fossils` (the only slug with both per-test and cross-suite scope). No change.
- No fixture changes. No taxonomy detection-scope edits. No orchestrator-architecture changes.

### Quality gates for rework

- `properdocs build --strict` remains green.
- Operator-invocation flow unchanged — operator phrasing still resolves to the same slugs as before this rework.
- All 15 taxonomy entries gain the new Natural phrases section uniformly, mirroring the prior task's `Detection Scope` rollout shape.
- Existing fixtures and existing 9-smell onboarding work from the original implementation are preserved without modification.
