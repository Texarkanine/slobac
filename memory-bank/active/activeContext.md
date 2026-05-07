# Active Context

- **Current Task:** slobac-audit post-release v1 hardening
- **Phase:** BUILD - COMPLETE
- **What Was Done:** All 19 build steps executed in order with TDD discipline.
  - Generator (`slobac_tools/taxonomy_index.py` + `scripts/gen_taxonomy_index.py`)
    built test-first; 22 unit + end-to-end tests cover happy paths, every error
    path, multi-scope round-trip, missing/duplicate-marker detection, and
    idempotency. New `[dependency-groups] dev` with `pytest ~= 8.3` and
    `[tool.pytest.ini_options]` scoping discovery to `tests/python/`.
  - Sentinel-bracketed taxonomy index emitted to both
    `skills/slobac-audit/SKILL.md` (consumed by orchestrator Step 2) and
    `skills/slobac-audit/references/docs/taxonomy/README.md` (human navigation).
    README preamble rewritten to describe the new severity-desc + slug-asc
    ordering. Step 2 of `SKILL.md` rewritten to read the embedded table instead
    of fanning out to per-entry headers.
  - Skill workflow hardening: `SKILL.md` Step 4 gains an output budget
    sub-section with concrete per-richness test-count caps; new Step 6.5 enforces
    the IR-integrity gate before cross-suite dispatch; Step 3 explicitly forbids
    inline orchestrator scouting. `report-template.md` adds a "Suite manifest"
    line and notes the consumed cross-suite richness in the Summary.
    `cross-suite.md` requires the assessor to declare its consumed richness
    tier.
  - Repo `README.md` adds a "Required: a subagent-capable harness" section.
    `CONTRIBUTING.md`'s "After adding an entry" hook redirects to the regen
    command. `memory-bank/techContext.md` carries the exception note clarifying
    that the "no generator" rule applies only to canonical content, not to a
    derived navigation index.
  - CI: new `taxonomy-index-drift` job in `.github/workflows/docs.yaml`
    regenerates and `git diff --exit-code`s both targets, plus runs `pytest`.
    Deploy job now also waits on the drift-check job. Drift-check simulation on
    a side branch confirmed CI would catch a committed hand-edit.
  - All gates green: `uv run pytest` (22 passed), `uv run python
    scripts/gen_taxonomy_index.py` (idempotent on live targets),
    `uv run properdocs build --strict` (clean).
- **Files Modified (paths relative to repo root):**
  - New: `slobac_tools/__init__.py`, `slobac_tools/taxonomy_index.py`,
    `scripts/gen_taxonomy_index.py`, `tests/python/conftest.py`,
    `tests/python/unit/test_{parse_entry,ordering,render,sentinels,end_to_end}.py`,
    `tests/python/fixtures/{valid_single_scope,valid_multi_scope}.md`,
    `tests/python/fixtures/mini_taxonomy/{README,tautology-theatre,deliverable-fossils,conditional-logic,rotten-green}.md`.
  - Modified: `pyproject.toml`, `uv.lock`, `README.md`, `CONTRIBUTING.md`,
    `.github/workflows/docs.yaml`, `memory-bank/techContext.md`,
    `skills/slobac-audit/SKILL.md`,
    `skills/slobac-audit/references/report-template.md`,
    `skills/slobac-audit/references/subagents/cross-suite.md`,
    `skills/slobac-audit/references/docs/taxonomy/README.md`.
- **Deviations from Plan:** Two minor amendments during build, both in step 9:
  (1) the README's link to `CONTRIBUTING.md` was an out-of-docs-root path that
  would have failed `properdocs --strict`; replaced with an inline `uv run`
  command. (2) The README's link to `SKILL.md` was similarly out-of-docs-root;
  rendered as plain text instead. Neither changes contract or function; both
  preserve the doc-site build gate.
- **Next Step:** QA phase — invoke `niko-qa` skill.
