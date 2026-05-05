# Active Context

- **Current Task:** Expose SLOBAC as Cursor + Claude Code plugin with marketplace entries
- **Phase:** PLAN (revision 2: single-skill architecture) — COMPLETE
- **What Was Done:**
  - Decided to fold `scout/`, `batch/`, `cross-suite/` into `audit/references/subagents/` (operator-approved)
  - Rationale: (1) eliminates all Cursor naming collisions, (2) removes picker clutter (only audit is user-facing), (3) subagent dispatch via raw prompts is model-agnostic and harness-native
  - Name field resolves to `slobac-audit` (Cursor normalizes colons to hyphens; uses name field verbatim)
  - Claude Code resolves to `slobac:audit` (plugin-name:folder-name; ignores name field)
  - Subagent workflows become reference files; orchestrator reads them and launches raw subagents with dynamic foreground/background
- **Next Step:** `/niko-build` — Phase R1-R5 (create subagent refs, rewrite dispatch, delete siblings, update docs, verify)
