# Active Context

## Current Task: Per-skill LICENSES + REUSE.toml instrumentation
**Phase:** BUILD — COMPLETE

## What Was Done

- **Build (2026-05-04):** Added per-skill `LICENSES/` (copies from repo root), `REUSE.toml` (`SPDX-PackageName` per skill; PPL-S default; `slobac-audit` overrides `references/docs/**` → CC-BY-SA-4.0), `BUNDLED-AGPL.md` + REUSE override so **bundled `AGPL-3.0-or-later.txt` is a “used” license** under standalone `reuse --root . lint` (REUSE otherwise reports unused AGPL when only PPL-S tags apply to sources).
- **`SKILL.md`:** Added YAML `license:` to `skills/slobac-batch/`, `skills/slobac-scout/`, `skills/slobac-cross-suite/`, `skills/slobac-audit/` (headline LicenseRef-PPL-S + pointers; audit notes CC-BY-SA for manifesto docs).
- **Docs:** Short **Licensing (standalone bundle)** section in `skills/slobac-audit/README.md`.
- **Harness correction:** `tasks.md` Test Plan / infrastructure updated — nested Git checkouts require **`reuse --root . lint`** at the skill root; plain `reuse lint` ascends to monorepo root.
- **Tooling:** Installed REUSE CLI via `pipx` (`~/.local/bin/reuse`).
- **Verification:** `reuse --root . lint` for all four skill roots (exit 0); `reuse lint` at repo root (exit 0); `uv run properdocs build --strict` (exit 0).

## Next Step

- Run `/niko-qa` following `level2-workflow.md`.
