# Active Context

- **Current Task:** Expose SLOBAC as Cursor + Claude Code plugin with marketplace entries
- **Phase:** QA (re-run) — IN PROGRESS
- **What Was Done (Build revision):**
  - Phase R1: Created `skills/audit/references/subagents/` with migrated workflow files (scout.md, batch.md, cross-suite.md); `exploration-commands.md` placed at `references/` level alongside other format specs
  - Phase R2: Rewrote orchestrator dispatch in `skills/audit/SKILL.md` — name field `slobac-audit`, subagent steps read raw workflow files and pass absolute `references/` path
  - Phase R3: Deleted `skills/scout/`, `skills/batch/`, `skills/cross-suite/` — RED gate confirmed stale refs in Phase R4 targets
  - Phase R4: Updated `audit/README.md`, `using-slobac.md`, `CONTRIBUTING.md`, `techContext.md`, `systemPatterns.md` — GREEN gate all pass
  - Phase R5: Final verification — properdocs strict, reuse lint (nested + monorepo), stale-ref grep clean
- **QA Findings:**
  - Fixed: `txrk9-agent-plugins/README.md` stale "Ships multiple skills" description → corrected to single-skill architecture
  - Noted: `exploration-commands.md` at `references/` level (plan said `subagents/`) — architecturally sound deviation, scout.md path refs resolve correctly
- **Next Step:** QA verification gates, then report
