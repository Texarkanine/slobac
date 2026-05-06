# Progress

## Summary

Align the single registered SLOBAC skill directory (`skills/slobac-audit/`) so that the token displayed/invoked in both Cursor (`/slobac-audit`) and Claude Code (display `slobac-audit`, invocation `/slobac:slobac-audit`) reads the same. Investigation ruled out a harness-native parity shortcut.

**Complexity:** Level 2

## Log

- Complexity analysis complete; Level 2 determined.
- Plan complete; investigation confirms no harness-native parity mechanism. Plan adopted the directory name `slobac-audit` plus drive-by doc fixes (stale `README.md` link; `using-slobac.md` misattribution of Cursor slash-command source).
- **Operator correction recorded:** Cursor uses the directory name for slash commands, not the SKILL.md `name` field (the prior archive recorded this incorrectly). Before the rename, the Cursor slash token matched the short directory name, not the frontmatter display name. Aligning the directory name to `slobac-audit` brands the Cursor command.
- Plan phase exited; entering Preflight.
- Preflight PASS with one plan amendment: step 4 file list extended to include `tests/fixtures/audit/README.md` (two stale taxonomy-path prose references on lines 44 & 48 surfaced by searching for the pre-rename `skills/` + short folder name path; not previously enumerated). Confirmed `.cursor-plugin/plugin.json` (uses glob `./skills/`) and `.claude-plugin/plugin.json` (no skills field — auto-discovers) need no change. `.github/workflows/`, `pyproject.toml`, and orchestrator `SKILL.md` under the skill tree are rename-safe (relative `references/...` paths only). Sibling-repo touchpoint confirmed as `txrk9-agent-plugins/README.md` only.
- **Build complete:** `git mv` to `skills/slobac-audit/`; `properdocs.yml` + root `REUSE.toml` + repo docs + memory-bank persistent files + `using-slobac.md` updated; `txrk9-agent-plugins/README.md` invocation line updated in sibling checkout. Gates: `properdocs build --strict`, `reuse --root . lint` from `skills/slobac-audit/`, path greps (see `tasks.md`). Ready for QA / operator smoke tests.
