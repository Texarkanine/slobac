# Task: Align skill invocation name across Cursor & Claude Code

* Task ID: slobac-skill-rename-invocation-parity
* Complexity: Level 2
* Type: Simple enhancement (rename + reference sweep)

Canonical skill path: `skills/slobac-audit/` so the visible invocation token is `slobac-audit` in both harnesses (Cursor `/slobac-audit`, Claude Code `/slobac:slobac-audit`).

**Harness behavior (corrected by operator):**
- **Cursor** uses the **directory name** as the slash command. When the directory was still named with the short token, invocation was unbranded. The SKILL.md `name` field is *not* used by Cursor for the slash command; renaming the directory is what changes the Cursor invocation. The current `name: slobac-audit` was effectively ornamental for Cursor until the directory was aligned.
- **Claude Code** uses `/plugin-name:dir`. Formerly `/slobac:` plus the short directory name; after rename: `/slobac:slobac-audit`.

Investigation confirms no harness-native mechanism produces stricter parity; the doubled prefix in Claude Code is the accepted cost. The build updated the docs build config, the REUSE manifest, the memory bank, and the sibling-repo marketplace README. Drive-by doc fixes: (a) `README.md` no longer links to a removed skill `README.md`; (b) `using-slobac.md` Cursor section documents directory-name–based slash registration.

## Test Plan (TDD)

### Behaviors to Verify

There is no functional unit-test suite (per `techContext.md` "Testing Process: None yet"). Verification gates and smoke tests stand in for tests:

- **Skill discovery (Cursor)**: install the plugin from the local `txrk9-agent-plugins` checkout → `/sl…` autocomplete in Cursor lists `/slobac-audit` (no legacy unbranded token for the old folder name). Operator smoke test.
- **Skill discovery (Claude Code)**: install the plugin → `/sloba…` autocomplete in Claude Code lists `/slobac:slobac-audit` with display name `slobac-audit`. Operator smoke test.
- **`properdocs build --strict`**: passes with no warnings after `docs_dir`/`edit_uri` paths point at `skills/slobac-audit/references/docs/`. CI-style gate run locally.
- **`reuse --root . lint` from `skills/slobac-audit/`**: returns success; no SPDX/license errors. CI-style gate run locally.
- **Stale-reference grep** (`git grep -E 'skills/(audit)\b'` excluding `memory-bank/archive/` and `planning/`): returns no matches. Manual gate.
- **Stale-link grep** (`git grep "skills/.*README"` for the removed README path): returns no matches (the prior-task drive-by fix).
- **Edge — fixtures path untouched**: `git grep "tests/fixtures/audit"` still resolves to the same fixture directory; `tests/fixtures/audit/` is **not** renamed. Confirm by `ls tests/fixtures/audit/`.
- **Edge — report-artifact filename unchanged**: the audit's own output file `slobac-audit.md` (in `SKILL.md` step "write report" and `references/report-template.md`) is the runtime artifact, not the skill name; it stays `slobac-audit.md`. Verify by `git grep "slobac-audit.md"` → only the two intended occurrences.
- **Sibling-repo invocation-line accuracy**: `txrk9-agent-plugins/README.md` plugin row reflects the new Claude-Code invocation `/slobac:slobac-audit`. Manual review.

### Test Infrastructure

- Framework: none (no functional tests). Verification is via `properdocs build --strict`, `reuse lint`, `git grep`, and operator-driven slash-command smoke tests in Cursor and Claude Code.
- Test location: N/A.
- Conventions: follow the prior `slobac-plugin-distribution` task's verification pattern (its archive enumerates the same gates).
- New test files: none.

## Implementation Plan (executed)

1. Investigation — no native parity mechanism found (recorded in preflight / progress).
2. `git mv` of the skill directory to `skills/slobac-audit/` (history-preserving).
3. Root `properdocs.yml` and `REUSE.toml` paths updated to `skills/slobac-audit/references/docs/`.
4. `README.md`, `CONTRIBUTING.md`, `tests/fixtures/audit/README.md` updated.
5. `memory-bank/productContext.md`, `systemPatterns.md`, `techContext.md` updated.
6. `skills/slobac-audit/references/docs/using-slobac.md` — Cursor/Claude invocation documentation corrected.
7. Sibling repo `txrk9-agent-plugins/README.md` — Claude invocation line (separate commit in that repo).
8. Final gate sweep (`properdocs`, `reuse`, greps for legacy path and Claude invocation tokens).
9. Memory-bank ephemerals updated; Build marked complete.

## Technology Validation

No new technology — validation not required. All gates (`properdocs`, `reuse`) are already in use; no new dependencies.

## Dependencies

- `properdocs` (already pinned in `pyproject.toml [dependency-groups] docs`)
- `reuse` CLI (operator-installed via `pipx`, per `techContext.md`)
- Sibling repo `txrk9-agent-plugins` checked out at `/home/mobaxterm/git/txrk9-agent-plugins`
- No code dependencies; this is a rename + docs sweep.

## Challenges & Mitigations

- **Challenge**: The obsolete skill subtree path and unrelated prose tokens (e.g. `tests/fixtures/audit/`, the `slobac-audit.md` report filename, the literal word "audit"). **Mitigation**: anchor searches with regex boundaries; manually inspect each hit; never use `sed -i` blindly.
- **Challenge**: `properdocs build --strict` may surface broken cross-links if any taxonomy file referenced an absolute repo path (it does not — those are relative). **Mitigation**: gate runs after path-touching edits catch breakage early.
- **Challenge**: Two repos must be updated and committed. Marketplace JSON files do **not** reference the folder name (the `skills` field in `.cursor-plugin/plugin.json` is a glob `./skills/`). **Mitigation**: sibling-repo change limited to `README.md` where needed.
- **Challenge**: Harness naming behavior must be smoke-tested by the operator. **Mitigation**: QA gate; if actual invocation differs, treat as QA FAIL and re-plan.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight
- [x] Build
- [ ] QA
