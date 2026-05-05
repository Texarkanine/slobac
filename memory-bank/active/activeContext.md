# Active Context

- **Current Task:** Expose SLOBAC as Cursor + Claude Code plugin with marketplace entries
- **Phase:** QA — FAIL (routing back to Plan for Cursor namespacing)
- **What Was Done:**
  - Semantic QA: PASS (1 trivial fix to `systemPatterns.md`).
  - Operator smoke test:
    - **Claude Code PASS** — skills resolve as `/slobac:batch`, `/slobac:scout`, `/slobac:audit`.
    - **Cursor FAIL** — skills appear as `/audit`, `/batch`, `/cross-suite` (no `slobac:` prefix; duplicates visible). The SKILL.md `name` field is NOT used as the literal Cursor invocation name.
- **Root Cause:** The plan's namespacing architecture assumed Cursor uses the `name` field in SKILL.md frontmatter as the invocation command. This is incorrect — Cursor's plugin system appears to compose invocations differently (folder name as suffix, plugin name as group/filter, not as a `name:suffix` literal).
- **Next Step:** Return to Plan phase to research Cursor's actual skill resolution mechanism and revise the namespacing approach. Claude Code implementation is correct and should be preserved.
