# Project Brief: Align Skill Invocation Name Across Cursor & Claude Code

## User story

After the `slobac-plugin-distribution` work merged, a Claude Code smoke test showed the slash-command UX diverges from Cursor:

- Cursor displays/invokes `/slobac-audit`.
- Claude Code displays the SKILL `name` (`slobac-audit`) but actually invokes via `plugin-name:skill-directory` — historically the directory name appeared after `slobac:` (see current `using-slobac.md` for the post-rename command line).

The operator wants the **token after `/`** to read the same in both harnesses, even at the cost of an awkward doubled prefix in Claude Code. Cross-tool parity is important so the agent (and humans) don't have to remember different invocation strings per platform.

## Requirements

1. **Investigate first.** Confirm there is no Cursor or Claude Code mechanism to achieve true parity (e.g., aliasing, plugin-display-name override, configurable invocation prefix). If something exists, surface it before changing anything.
2. **Rename applied (`git mv`):**
    - Skill directory is now `skills/slobac-audit/`.
    - Keep `name: slobac-audit` in SKILL.md.
3. **Resulting UX (accepted):**
    - Cursor: `/slobac-audit`
    - Claude Code: display `slobac-audit`, invoke `/slobac:slobac-audit`
4. **In-repo references** updated to the new path (including `README.md`, `references/docs/using-slobac.md`, root `REUSE.toml`, `properdocs.yml`, `CONTRIBUTING.md`, memory-bank). Plugin manifests use a `./skills/` glob — no folder string embedded.
5. **Sibling repo `txrk9-agent-plugins`:** README invocation line updated where it referenced the old Claude namespace form.
6. **Verification gates** (mirroring the prior task): `properdocs build --strict`, REUSE lint clean, stale-reference grep clean, operator smoke tests in Cursor and Claude Code.

## Out of scope

- Marketplace re-submission.
- Any change to smell-detection logic or audit workflow content.
