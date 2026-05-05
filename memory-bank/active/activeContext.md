# Active Context

- **Current Task:** Expose SLOBAC as Cursor + Claude Code plugin with marketplace entries
- **Phase:** BUILD — COMPLETE (ready for `/niko-qa`)
- **What Was Done:**
  - Renamed `skills/slobac-*` → `skills/{audit,scout,batch,cross-suite}` (`git mv`), updated all four `SKILL.md` frontmatter names to `slobac:*`, path references to `../audit/references/`, and README architecture diagrams.
  - Updated `properdocs.yml`, root `REUSE.toml`, `CONTRIBUTING.md`, repo `README.md`, `skills/audit/references/docs/using-slobac.md` (marketplace install + legacy symlink note), `memory-bank/techContext.md`, `memory-bank/productContext.md`, fixture docs under `tests/fixtures/audit/README.md`.
  - Added `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json` at repo root (`skills` discovery → `./skills/`).
  - Added `Texarkanine/txrk9-agent-plugins` `.cursor-plugin/marketplace.json`, `.claude-plugin/marketplace.json`, and README describing the catalog + SLOBAC plugin.
  - Verification: `uv sync --group docs && uv run properdocs build --strict`; `reuse lint` (repo root); `reuse --root . lint` from `skills/audit/`; `python3 -m json.tool` on all four manifest JSON files.
- **Deviations from plan:** Per-unit stub→RED manifest steps (Steps 19–22 advisory) consolidated — created full JSON directly with syntax validation. `memory-bank/systemPatterns.md` left unchanged (preflight advisory: non-CI); operator may batch-update paths later.
- **Next Step:** Run `/niko-qa` for semantic review.
