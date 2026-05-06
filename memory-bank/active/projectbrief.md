# Project Brief: Align Skill Invocation Name Across Cursor & Claude Code

## User story

After the `slobac-plugin-distribution` work merged, a Claude Code smoke test showed the slash-command UX diverges from Cursor:

- Cursor displays/invokes `/slobac-audit`.
- Claude Code displays the SKILL `name` (`slobac-audit`) but actually invokes via `plugin-name:skill-directory` → `/slobac:audit`.

The operator wants the **token after `/`** to read the same in both harnesses, even at the cost of an awkward doubled prefix in Claude Code. Cross-tool parity is important so the agent (and humans) don't have to remember different invocation strings per platform.

## Requirements

1. **Investigate first.** Confirm there is no Cursor or Claude Code mechanism to achieve true parity (e.g., aliasing, plugin-display-name override, configurable invocation prefix). If something exists, surface it before changing anything.
2. **If no parity mechanism exists, rename:**
    - `skills/audit/` → `skills/slobac-audit/` (`git mv`).
    - Keep `name: slobac-audit` in SKILL.md.
3. **Resulting UX (accepted):**
    - Cursor: `/slobac-audit`
    - Claude Code: display `slobac-audit`, invoke `/slobac:slobac-audit`
4. **Update all in-repo references** to the old `skills/audit/` path:
    - `skills/audit/SKILL.md` self-references (if any), `README.md`, `references/docs/using-slobac.md`
    - Root `REUSE.toml`
    - `properdocs.yml` (`docs_dir`, `edit_uri`)
    - `CONTRIBUTING.md`, repo `README.md`
    - `memory-bank/techContext.md`, `memory-bank/systemPatterns.md`
    - `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json` (if they reference the dir; the `skills` field is a glob today)
5. **Sibling repo `txrk9-agent-plugins`:** update marketplace catalog entries / README if they reference the skill directory.
6. **Verification gates** (mirroring the prior task): `properdocs build --strict`, REUSE lint clean, stale-reference grep clean, operator smoke tests in Cursor and Claude Code.

## Out of scope

- Marketplace re-submission.
- Any change to smell-detection logic or audit workflow content.
