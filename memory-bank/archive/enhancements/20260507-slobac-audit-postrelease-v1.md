---
task_id: slobac-audit-postrelease-v1
complexity_level: 2
date: 2026-05-07
status: completed
---

# TASK ARCHIVE: slobac-audit post-release v1 hardening

## SUMMARY

Applied the v1-hardening cut to the `slobac-audit` skill, driven by failure modes
exposed in the first three post-release runs (default/auto, composer-2,
claude-opus-4-7) against the `ai-rizz` test suite (33 files, ~389k chars, ~377
tests). The work added an output budget, a behavior-summary integrity gate, a
mandatory-scout enforcement, a generated taxonomy index emitted to two locations
with a CI drift-check, a repo-level subagent requirement note, and cross-suite
richness transparency in the report — all motivated by concrete, reproducible
failure modes. All seven acceptance criteria delivered clean to plan.

## REQUIREMENTS

1. **A1 — Output budget**: SKILL.md Step 4b gets per-richness test-count caps
   (`full` ~120, `standard` ~250, `compact` ~600) and a binding-budget rule so
   output truncation (as seen in the auto run) can't silently drop findings.
2. **A2 — IR integrity gate**: A new Step 6.5 between merge and cross-suite
   dispatch checks `merged_rows ≥ scout_test_count × 0.95`, with an explicit
   retry-or-halt branch so the silent zero-findings failure (auto run) is
   structurally impossible.
3. **A3 — Mandatory scout + manifest provenance**: Step 3 of SKILL.md explicitly
   forbids inline enumeration/measurement by the orchestrator; `report-template.md`
   adds a "Suite manifest" line in the Summary section so a reader can audit
   whether scout ran.
4. **B4 — Generated taxonomy index**: A stdlib-only Python generator
   (`slobac_tools/taxonomy_index.py` + `scripts/gen_taxonomy_index.py`) parses
   every `taxonomy/<slug>.md`, sorts entries severity-desc + slug-asc, and emits
   the 3-column index (Slug | Severity | Detection Scope) into sentinel-bracketed
   regions in both `SKILL.md` and `taxonomy/README.md`. CI drift-check
   regenerates and `git diff --exit-code`s both targets. `CONTRIBUTING.md` updated;
   `techContext.md` carries an exception note distinguishing the generated navigation
   index from canonical manifesto content.
5. **B5 — Subagent requirement in README**: repo `README.md` adds a
   "Requirements" section noting that `slobac-audit` requires a subagent-capable
   harness; composer-class harnesses will run incorrectly.
6. **C8 — Cross-suite richness in report**: `cross-suite.md` Step 5 requires
   declaring the consumed richness tier; `report-template.md` renders that
   declaration in the Summary so a `compact`-fed pass can be visibly downgraded.
7. **B6 captured as follow-up**: The deferred regex-canary idea is recorded in
   `progress.md` under "Follow-ups" rather than implemented.

## IMPLEMENTATION

### New code

- `slobac_tools/__init__.py`, `slobac_tools/taxonomy_index.py` — stdlib-only
  generator module. Key types: `TaxonomyEntry` (frozen dataclass), `TaxonomyIndexError`
  (structured `ValueError` with `file_path` + `field` attrs). Key functions:
  `parse_entry`, `order_entries`, `render_table`, `replace_between_sentinels`,
  `regenerate`.
- `scripts/gen_taxonomy_index.py` — thin CLI shim with hardcoded target paths;
  calls `regenerate(...)`.
- `tests/python/` — 24 pytest tests across 5 unit files (`test_parse_entry.py`,
  `test_ordering.py`, `test_render.py`, `test_sentinels.py`, `test_end_to_end.py`)
  plus `conftest.py` and `fixtures/` (fixture taxonomy entries + mini_taxonomy dir).

### Skill workflow changes (`skills/slobac-audit/`)

- **SKILL.md**: Step 2 rewritten to read the embedded slug→scope table instead of
  fanning out to per-entry headers; "Supported slugs and detection scopes" subsection
  added with sentinel-bracketed generated table. Step 3 gains an inline-scout
  prohibition. Step 4b gains the output-budget sub-rule. New Step 6.5 (IR integrity
  gate). Step 8 updated to reference the new report-template Summary fields.
- **references/report-template.md**: "Suite manifest" line added to Summary
  (scout-reported N files, M chars, K tests); cross-suite richness tier note added.
- **references/subagents/cross-suite.md**: Step 5 requires declaring consumed
  richness tier.
- **references/docs/taxonomy/README.md**: hand-curated table replaced with
  sentinel-bracketed generated table; preamble rewritten to describe severity-desc
  + slug-asc ordering.

### Infrastructure

- `pyproject.toml`: new `[dependency-groups] dev` with `pytest ~= 8.3`;
  `[tool.pytest.ini_options]` scoping discovery to `tests/python/` with
  `pythonpath = ["."]`.
- `.github/workflows/reusable-taxonomy-index-check.yml`: new reusable job that
  runs `uv sync --group dev --frozen`, `uv run pytest`, `uv run python
  scripts/gen_taxonomy_index.py`, and `git diff --exit-code` on both generated
  targets.
- `.github/workflows/ci.yml`: calls the new reusable workflow alongside the
  existing docs build.
- `README.md`: "Requirements" section added.
- `CONTRIBUTING.md`: "After adding an entry" hook redirects to the regen command.
- `memory-bank/techContext.md`: exception note clarifying the "no generator"
  rule applies to canonical content, not derived navigation indexes.

### Post-merge PR fixes (on `process-review` branch)

Three CodeRabbit review items from PR #19 applied after the initial commit:
1. Inverted sentinels (`END` before `BEGIN`) leaked a raw `ValueError` instead of
   `TaxonomyIndexError` — wrapped in `try/except ValueError as exc` → `from exc`.
2. Empty taxonomy directory produced a silent empty table — guarded with a
   fail-loud `TaxonomyIndexError` in `regenerate()`.
3. Exception chaining (B904) — `raise TaxonomyIndexError(...) from exc` on the
   inverted-sentinel handler. Each fix was test-first; suite stayed green at 24.

## TESTING

- `uv run pytest tests/python/` — 24 passed (all TDD cycles green; two PR-review
  fixes each added a new test first).
- `uv run python scripts/gen_taxonomy_index.py` run twice — zero diff on second
  run (idempotency confirmed on live targets).
- `uv run properdocs build --strict` — clean (sentinel comments inert in
  doc-site rendering; no out-of-docs-root links).
- Drift-check simulation on a side branch: hand-edited one taxonomy header without
  regenerating; CI job caught the diff with a non-zero exit.
- QA semantic pass: all seven acceptance criteria verified; Step 8 / report-template
  drift caught and reconciled.

## LESSONS LEARNED

- **`properdocs --strict` polices the docs-root boundary aggressively.** Any link
  from a doc-site page to a file outside the docs root fails strict-mode build.
  Pattern: use inline commands or full GitHub URLs; if a path must appear, render
  as plain text.
- **Sentinel-bracketed dual-target generation is cheap.** One `replace_between_sentinels`
  function, two `(target_path, link_target)` tuples in the entry point, and
  idempotency falls out of comparing pre/post-write text. The CI drift-check needed
  only `git diff --exit-code`. Very good cost-to-correctness ratio.
- **The "first post-release real run" is genuinely informative.** Three runs with
  three different models against one target surfaced three orthogonal failure modes
  no single-author review would have found. Same-target multi-model exercise before
  declaring v1 stable is a defensible pattern to bake into future releases.
- **Doc-doc consistency requires semantic QA.** When a task touches both a workflow
  file and the contract it references, prose can drift even when each artifact is
  individually coherent. The Step 8 / report-template drift was exactly this; QA
  caught it; mechanical gates never would have.
- **Explicit per-cycle TDD sub-ordering pays off.** The plan's "write fixture/test →
  red → implement → green" ordering (added during preflight) provided resistance
  against the urge to write the implementation first. Worth keeping in future plans.

## PROCESS IMPROVEMENTS

- **Pre-bake `pythonpath` in any plan that introduces a new importable package under
  the repo root.** The `slobac_tools/` import path failure on first test run was
  predictable; the plan should have included `pythonpath = ["."]` in the pytest
  config step.
- **Flag doc-site link constraints explicitly in any plan step that touches
  `references/docs/`.** The two out-of-docs-root link replacements in step 9 were
  predictable from `properdocs --strict`'s known behavior; flagging this constraint
  in the plan would have avoided in-flight deviations.
- **For future "first post-release exercise" tasks:** consider scheduling a
  same-target multi-model run as an explicit pre-hardening step, not as
  opportunistic evidence after the fact.

## TECHNICAL IMPROVEMENTS

- **B6 — regex/grep canary hints**: polyglot smell-signal enumeration is deferred
  pending creative-phase exploration of how to suggest hotspot detection without
  narrowing the agent's qualitative pass. Motivating evidence: 2/3 post-release
  runs missed the literal `assertTrue "..." true` shell assertion.
- **Subagent-less inline fallback**: not added. If composer-class harnesses become
  a more common audit caller, revisit whether a degraded mode is better than the
  current "use a different harness" stance.
- **Future Protects column in the index**: the generator architecture already
  supports it — `TaxonomyEntry.protects` is parsed but currently dropped at render
  time. Adding a `Protects` column to both output tables is a one-line render
  change + a generator re-run.

## NEXT STEPS

- **B6 (regex canaries)** — deferred; see Technical Improvements above.
- PR #19 (`process-review` → `main`) is pending merge; the three post-merge fixes
  are already committed on the branch.
