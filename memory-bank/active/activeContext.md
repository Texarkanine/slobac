# Active Context

- **Current Task:** Expose SLOBAC as Cursor + Claude Code plugin with marketplace entries
- **Phase:** PLAN (revision) — COMPLETE
- **What Was Done:**
  - Identified root cause: Cursor registers skills via BOTH folder name AND `name` field. Colon in `name: "slobac:audit"` gets split, producing suffix `audit` that collides with folder name `audit` → duplicates.
  - Evidence: `cursor-warehouse` works because its folders (`cw-recall`) don't match name suffixes (`recall`).
  - Created phased fix plan: Phase R1 tries `name: audit` (matching folder, no collision). If Cursor auto-prefixes with plugin name → `/slobac:audit` achieved. If not → Phase R3 falls back to `name: slobac-audit` (hyphenated, accepts divergence from Claude Code's colon form).
- **Next Step:** `/niko-build` — Phase R1 (4 one-line edits) then operator smoke test.
