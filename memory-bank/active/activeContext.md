# Active Context

- **Current Task:** Align skill invocation name across Cursor & Claude Code — skill directory is `skills/slobac-audit/`
- **Phase:** BUILD — COMPLETE (hand off to QA)
- **What Was Done:** Executed Level 2 build: `git mv` skill tree to `skills/slobac-audit/`; updated `properdocs.yml`, `REUSE.toml`, `README.md`, `CONTRIBUTING.md`, `tests/fixtures/audit/README.md`, persistent memory-bank docs (`productContext.md`, `systemPatterns.md`, `techContext.md`), and `skills/slobac-audit/references/docs/using-slobac.md` (Cursor uses directory name; Claude `/slobac:slobac-audit`). Fixed `techContext.md` to drop stale `README.md` link in favor of `using-slobac.md`. Sibling-repo README update remains a separate commit in `txrk9-agent-plugins` (step 7).
- **Next Step:** Invoke `/niko-qa` (Level 2 QA); operator smoke tests for Cursor/Claude autocomplete per `tasks.md` test plan.
