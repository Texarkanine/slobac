---
task_id: slobac-skill-rename-invocation-parity
complexity_level: 2
date: 2026-05-06
status: completed
---

# TASK ARCHIVE: Align Skill Invocation Name Across Cursor & Claude Code

## SUMMARY

Renamed the audit skill tree to `skills/slobac-audit/` (history-preserving `git mv`) so the visible invocation token matches across harnesses: Cursor `/slobac-audit`, Claude Code display `slobac-audit` with invocation `/slobac:slobac-audit` (doubled prefix accepted). Root docs, `properdocs.yml`, `REUSE.toml`, memory-bank persistents, `using-slobac.md`, and sibling `txrk9-agent-plugins/README.md` were updated. Investigation confirmed no harness-native shortcut for stricter parity.

## REQUIREMENTS

- Investigate harness mechanisms for parity; document if none exist.
- Apply `git mv` to `skills/slobac-audit/`; keep `name: slobac-audit` in SKILL.md.
- Target UX: Cursor `/slobac-audit`; Claude Code `/slobac:slobac-audit`.
- Sweep in-repo references; plugin manifests use `./skills/` glob (no embedded folder string).
- Update sibling marketplace README invocation line.
- Gates: `properdocs build --strict`, REUSE lint, stale-reference greps, operator smoke tests (Cursor + Claude Code).

## IMPLEMENTATION

- **`git mv`** of skill directory to `skills/slobac-audit/`.
- **Config / compliance:** `properdocs.yml`, root `REUSE.toml` paths → `skills/slobac-audit/references/docs/`.
- **Docs:** `README.md`, `CONTRIBUTING.md`, `tests/fixtures/audit/README.md` (preflight catch for stale path prose), `skills/slobac-audit/references/docs/using-slobac.md` (Cursor slash command = directory name, not SKILL.md `name`).
- **Memory bank (persistent):** `productContext.md`, `systemPatterns.md`, `techContext.md` updated during build.
- **Sibling repo:** `txrk9-agent-plugins/README.md` invocation line (separate commit in that checkout).
- **Explicit non-changes:** `tests/fixtures/audit/` directory name unchanged; runtime report artifact `slobac-audit.md` unchanged.

## TESTING

- **Automated:** `properdocs build --strict` (0), `reuse --root . lint` from skill tree (30/30), `git grep` gates for legacy `skills/(audit)` path and removed README links — all clean before archive. `/niko-qa` semantic review passed with no trivial fixes.
- **Operator:** Smoke tests in Cursor (`/slobac-audit`) and Claude Code (`/slobac:slobac-audit`) — **completed successfully** per operator at archive time (post-merge / install).

## LESSONS LEARNED

- **Cursor** registers the slash command from the **skill directory name**, not `SKILL.md` `name`. Treat directory naming as the user-visible Cursor token; `name` is display/orchestration metadata, not routing for Cursor.
- **Preflight** caught `tests/fixtures/audit/README.md` stale references that the initial plan file list missed — grep-then-inspect during preflight is the right safety net for stragglers.

## PROCESS IMPROVEMENTS

- When adding or renaming skills, document **directory name = Cursor slash token** in planning and in `using-slobac.md` (or equivalent) from the first change, to avoid a follow-up rename task.

## TECHNICAL IMPROVEMENTS

- None beyond naming discipline above; no smell-detection or audit logic changes.

## NEXT STEPS

- None for this task. Ongoing: keep marketplace / install docs aligned if the skill path or harness behavior changes again.

---

## Inlined reflection (ephemeral collapsed)

_Source: reflection `reflection-slobac-skill-rename-invocation-parity.md` — deleted during archive._

**Requirements vs outcome:** All requirements met. Operator correction improved docs: SKILL.md `name` does not drive Cursor slash token; prior archive was wrong on that point — fixed in `using-slobac.md` and memory bank.

**Plan accuracy:** Sequence and scope held. Only amendment: preflight added `tests/fixtures/audit/README.md` to the touch list (stale taxonomy path prose).

**Build & QA:** `git_mv` preserved history; greps clean; two-repo change isolated to sibling README line; QA first-pass clean on automated gates.

**Million-dollar question:** If the distribution task had named the directory `slobac-audit` initially, this rename task would have been unnecessary — lesson is naming discipline one task earlier, not an architecture gap.
