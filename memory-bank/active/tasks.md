# Task: slobac-audit post-release v1 hardening

* Task ID: slobac-audit-postrelease-v1
* Complexity: Level 2
* Type: Simple enhancement (multi-component; doc + tooling + skill workflow)

Apply the v1-hardening cut to the `slobac-audit` skill, motivated by gaps observed in
three post-release runs against `ai-rizz` `tests/`. In scope: A1 (output budget), A2 (IR
integrity check), A3 (mandatory scout + manifest in report), B4 (generated taxonomy
index emitted to both `SKILL.md` and `taxonomy/README.md`, with CI drift-check), B5
(repo `README.md` subagent-requirement note), C8 (cross-suite richness in report),
plus a `techContext.md` amendment documenting the B4 exception. Out of scope: B6
(regex canaries) and C7 (per-subagent telemetry); B6 is logged in `progress.md` as a
follow-up needing creative exploration.

## Test Plan (TDD)

### Behaviors to Verify

**Generator — `scripts/gen_taxonomy_index.py`:**

- *Parse a valid canonical header*: input = a fixture markdown file shaped like a real
  taxonomy entry (header table on line 5) → output = `TaxonomyEntry(slug, severity,
  scopes)` where `scopes` is a list (handles both single-scope `per-test` and
  multi-scope `per-test, cross-suite`).
- *Reject malformed header*: header table missing, columns reordered, severity not in
  `{Critical, High, Medium, Low}`, scope contains a value not in `{per-test, per-file,
  cross-suite}` → raises a typed exception naming the offending file and field. No
  silent skip.
- *Order by severity desc, slug asc*: input = entries in random order → output is
  `[Critical*, High*, Medium*, Low*]` with each tier sorted alphabetically by slug.
- *Render markdown table*: input = ordered entries → output is a 3-column table
  (`Slug | Severity | Detection Scope`), slug column rendered as a relative markdown
  link to `<slug>.md` (the link target depends on the *write target*: README.md uses
  `./<slug>.md`; SKILL.md uses `references/docs/taxonomy/<slug>.md` since it sits
  higher in the tree).
- *Sentinel-bracketed replace*: target file containing
  `<!-- BEGIN: taxonomy-index -->` … `<!-- END: taxonomy-index -->` markers → only the
  region between markers is replaced; surrounding content is byte-identical.
- *Missing-markers error*: target file with no markers, or unbalanced markers, →
  raises a typed exception naming the missing/duplicated marker. No silent append.
- *End-to-end on the live repo*: invoking `python scripts/gen_taxonomy_index.py`
  against the actual `skills/slobac-audit/` produces deterministic output for both
  target files (running twice with no other changes results in zero diff on the second
  run — i.e. the generator is idempotent).

**CI drift-check (smoke):**

- *Drift detected*: a CI run with a hand-edited `taxonomy/<slug>.md` header but
  un-regenerated targets fails the `git diff --exit-code` step with a non-zero exit
  and a clear error message in the job log directing the contributor to run the regen
  command.

**Skill workflow (manual, smoke against the script's own behavior):**

- *Step 2 partition* (orchestrator): an audit invocation that names a mix of per-test,
  per-file, and cross-suite slugs continues to dispatch them to the correct
  subagents — verify by reading the updated SKILL.md prose for partition logic against
  the embedded table.
- *Step 4 partitioning under output budget* (A1): given a manifest with N tests where
  N × richness-chars-per-row exceeds the documented per-batch output cap, the
  partition produces ≥2 batches even if the input fits in one. (Verifiable by reading
  the rule; no runtime test.)
- *Step 6.5 IR integrity gate* (A2): the workflow text encodes a measurable check
  (merged-row-count vs scout test-count, tolerance threshold) and a halt-or-retry
  branch. (Doc-level verification.)
- *Step 3 scout-mandatory wording* (A3): the workflow text explicitly forbids the
  orchestrator from doing scout's work inline.
- *Cross-suite richness in report* (C8): the cross-suite workflow appends a richness
  declaration; report template's Summary section names the richness it consumed.
  (Doc-level verification.)

### Edge Cases

- A taxonomy entry with **multi-scope** detection (`deliverable-fossils.md` →
  `per-test, cross-suite`) round-trips through parse + render without losing either
  scope. The scope column renders as the original comma-joined string.
- A taxonomy entry whose header was edited but no other generator output target was
  edited — drift-check job catches it.
- Empty `taxonomy/` directory (theoretical) — generator emits a table with only header
  + separator rows? Or refuses? Decision: refuse (fail loud), since a SLOBAC repo
  with zero canonical entries is a broken state, not an empty state.
- A `<slug>.md` file that exists but is missing its line-5 header table (e.g. a future
  contributor adds an unrelated `.md` file under `taxonomy/`). Generator must skip
  files that aren't taxonomy entries cleanly. Decision: enumerate via filename
  pattern, then *require* the header table on enumerated files; a malformed header on
  a real entry is an error, but a non-entry markdown file under `taxonomy/` is still
  invalid (we don't have those today and shouldn't introduce one). Treat any
  non-`README.md` markdown file under `taxonomy/` as an entry.

### Test Infrastructure

- **Framework:** `pytest`. Repo currently has no Python test infrastructure; this
  task introduces it for the generator only. Add `pytest` to a new
  `[dependency-groups] dev` group in `pyproject.toml`.
- **Test location:** `tests/python/unit/` (segregated from `tests/fixtures/audit/`,
  which is already in use as audit-skill fixture data, not pytest input).
- **Conventions:** test files named `test_*.py`; import the script as a module via a
  small `sys.path` shim or by giving the script a non-`scripts/`-package import path
  (decision: put the implementation under a top-level `slobac_tools/` package so it
  imports normally, and `scripts/gen_taxonomy_index.py` becomes a thin CLI shim that
  calls into it).
- **New test files:**
  - `tests/python/unit/test_parse_entry.py`
  - `tests/python/unit/test_ordering.py`
  - `tests/python/unit/test_render.py`
  - `tests/python/unit/test_sentinels.py`
  - `tests/python/unit/test_end_to_end.py`
  - `tests/python/conftest.py` (for fixture-path helpers if needed)
  - `tests/python/fixtures/` (small markdown fixtures for parser tests)

## Implementation Plan

Each step is one TDD cycle: write/extend the failing test, implement to pass, refactor.

1. **Bootstrap Python test infrastructure.**
   - Files: `pyproject.toml` (new `[dependency-groups] dev` with `pytest`,
     `[tool.pytest.ini_options]` with `testpaths = ["tests/python"]`),
     `tests/python/__init__.py` *(absent — pytest auto-discovers; do not create)*,
     `tests/python/unit/__init__.py` *(absent for same reason)*.
   - Changes: add the dev group; configure pytest's `testpaths` to scope it to
     `tests/python` so the audit-fixture `tests/fixtures/audit/` directory is not
     swept.
   - Validation: `uv sync --group dev && uv run pytest --collect-only` resolves the
     env and reports zero tests (success).

2. **Stub the generator module with empty implementations + failing test stubs (TDD
   prep).**
   - Files: `slobac_tools/__init__.py`, `slobac_tools/taxonomy_index.py`,
     `scripts/gen_taxonomy_index.py`, `tests/python/unit/test_parse_entry.py`,
     `tests/python/unit/test_ordering.py`, `tests/python/unit/test_render.py`,
     `tests/python/unit/test_sentinels.py`, `tests/python/unit/test_end_to_end.py`.
   - Changes:
     - In `slobac_tools/taxonomy_index.py` declare:
       - `@dataclass class TaxonomyEntry(slug: str, severity: str, scopes: tuple[str, ...])`
       - `class TaxonomyIndexError(ValueError)` with `file_path` + `field` attrs.
       - `def parse_entry(path: Path) -> TaxonomyEntry: raise NotImplementedError`
       - `def order_entries(entries: Iterable[TaxonomyEntry]) -> list[TaxonomyEntry]: raise NotImplementedError`
       - `def render_table(entries: Sequence[TaxonomyEntry], *, link_target: Literal["readme", "skill"]) -> str: raise NotImplementedError`
       - `def replace_between_sentinels(text: str, content: str, *, marker_id: str = "taxonomy-index") -> str: raise NotImplementedError`
       - `def regenerate(taxonomy_dir: Path, targets: Sequence[tuple[Path, Literal["readme","skill"]]]) -> None: raise NotImplementedError`
     - In `scripts/gen_taxonomy_index.py` write a CLI shim with hardcoded paths to
       both target files relative to `Path(__file__).parent.parent`.
     - Test files: pytest stubs (`def test_<behavior>(): pass`) for every behavior
       enumerated in the Test Plan, with docstrings describing the assertion to come.
   - Validation: `uv run pytest --collect-only` reports the expected test count;
     `uv run pytest` runs and all stubs pass (no behavior yet).

3. **TDD: `parse_entry` happy path + multi-scope.**
   - Files: `tests/python/unit/test_parse_entry.py`,
     `tests/python/fixtures/valid_single_scope.md`,
     `tests/python/fixtures/valid_multi_scope.md`,
     `slobac_tools/taxonomy_index.py`.
   - Changes: implement `parse_entry` using a single regex against the line-5 row;
     return `TaxonomyEntry`. Multi-scope split on `,` with `.strip()`.
   - Validation: 2 tests pass.

4. **TDD: `parse_entry` error paths.**
   - Files: same test file + new fixture files for malformed cases (missing line 5,
     wrong-shaped row, unknown severity, unknown scope).
   - Changes: extend `parse_entry` with explicit validation; raise
     `TaxonomyIndexError` with file + field on each malformed case.
   - Validation: 4–6 error-path tests pass.

5. **TDD: `order_entries`.**
   - Files: `tests/python/unit/test_ordering.py`, `slobac_tools/taxonomy_index.py`.
   - Changes: implement with `key=(SEVERITY_ORDER[severity], slug)` where
     `SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}`.
   - Validation: ordering tests pass.

6. **TDD: `render_table` for both link targets.**
   - Files: `tests/python/unit/test_render.py`, `slobac_tools/taxonomy_index.py`.
   - Changes: implement; emits markdown table with `Slug | Severity | Detection
     Scope` header, link target conditional on `link_target` param. Multi-scope
     rendered with the original comma-joined string.
   - Validation: render tests pass.

7. **TDD: `replace_between_sentinels` happy path + missing-markers error.**
   - Files: `tests/python/unit/test_sentinels.py`, `slobac_tools/taxonomy_index.py`.
   - Changes: implement using regex with explicit BEGIN/END marker matching; raise
     `TaxonomyIndexError` if 0 or >1 occurrences of either marker. Preserve
     surrounding whitespace.
   - Validation: sentinel tests pass.

8. **TDD: `regenerate` end-to-end against fixture taxonomy dir.**
   - Files: `tests/python/unit/test_end_to_end.py`,
     `tests/python/fixtures/mini_taxonomy/` (3–4 small entries + a README + a SKILL
     stub with sentinels), `slobac_tools/taxonomy_index.py`.
   - Changes: implement `regenerate` to glob `taxonomy_dir/*.md` excluding
     `README.md`, parse all, order, render per target, write each target via
     `replace_between_sentinels`. Idempotency test: run twice → second run produces
     zero file diff.
   - Validation: end-to-end test passes; idempotency test passes.

9. **Add sentinel markers + initial generated table to the two real targets.**
   - Files: `skills/slobac-audit/references/docs/taxonomy/README.md`,
     `skills/slobac-audit/SKILL.md`.
   - Changes:
     - In `taxonomy/README.md`: replace the existing hand-curated table (lines
       11–27) with `<!-- BEGIN: taxonomy-index -->` / `<!-- END: taxonomy-index -->`
       sentinels around an empty placeholder. Run the generator. Confirm output is
       severity-desc + alpha-asc and column-shape correct.
     - In `SKILL.md`: insert a new short subsection "Supported slugs and detection
       scopes" near the top of Step 2 (before the partition rule), with the
       sentinels and generated table inside.
   - Validation: `git diff` shows the expected table content; `uv run properdocs
     build --strict` stays green (table renders).

10. **Rewrite SKILL.md Step 2 partition rule.**
    - Files: `skills/slobac-audit/SKILL.md`.
    - Changes: remove the "for each in-scope slug, read its `Detection Scope` from
      `<slug>.md`" instruction. Replace with "use the embedded supported-slugs table
      above for the partition; per-slug canonical content is read by the batch /
      cross-suite assessors after partitioning." Note that `taxonomy/README.md`
      contains the same table for human navigation.
    - Validation: re-read Step 2 against test plan's "skill workflow" smoke; no
      regression in the partition contract.

11. **A1 — Output budget in Step 4.**
    - Files: `skills/slobac-audit/SKILL.md`.
    - Changes: extend Step 4a / 4b with an "Output budget" sub-rule. Concrete caps:
      - `full` richness → ~120 tests/batch
      - `standard` → ~250 tests/batch
      - `compact` → ~600 tests/batch
      Whichever of input-budget partitioning or output-budget partitioning yields
      *more* batches is the binding constraint. Add a sentence naming the failure
      mode this prevents (subagent output truncation observed in post-release runs).
    - Validation: re-read Step 4 against the auto-run failure mode.

12. **A2 — IR integrity check (new Step 6.5).**
    - Files: `skills/slobac-audit/SKILL.md`.
    - Changes: insert "Step 6.5 — verify behavior-summary integrity" between Step 6
      (merge) and Step 7 (cross-suite). Specify: count merged behavior-summary rows
      vs the scout's reported test count; if `merged_rows < scout_test_count * 0.95`,
      either retry the implicated batch (idempotent) or halt with a named error.
      Never silently dispatch incomplete IR to cross-suite.
    - Validation: re-read against the auto-run silent-zero-cross-suite-findings
      failure mode.

13. **A3 — Mandatory scout + manifest in report.**
    - Files: `skills/slobac-audit/SKILL.md`, `skills/slobac-audit/references/report-template.md`.
    - Changes:
      - In SKILL.md Step 3 add an explicit prohibition: "the orchestrator MUST NOT
        enumerate or measure the suite itself; if you find yourself running `wc`,
        `find`, or `Glob` against the suite root, stop and launch the scout." Name
        the reasoning (auto-run miscounted at 29 vs actual 33; composer-run
        overcounted by 30k chars).
      - In `report-template.md` add a `Suite manifest` line in the Summary section
        ("scout-reported: N files, M chars, K tests"); the orchestrator copies
        scout's reported numbers into this line so a reader can audit whether scout
        ran.
    - Validation: re-read Step 3 + report-template against the file-count-drift
      failure modes from auto and composer.

14. **C8 — Cross-suite richness in report.**
    - Files: `skills/slobac-audit/references/subagents/cross-suite.md`,
      `skills/slobac-audit/references/report-template.md`.
    - Changes:
      - In `cross-suite.md` Step 5 (emit results) require declaring the consumed
        richness tier of the IR.
      - In `report-template.md` add a one-line note in the Summary section or
        Cross-Suite Findings header naming the richness tier the cross-suite
        assessor consumed (so a `compact`-fed cross-suite pass can be visibly
        downgraded by a reviewer).
    - Validation: re-read against the post-release richness-vs-recall observation.

15. **B5 — Subagent-required note in repo README.md.**
    - Files: `README.md`.
    - Changes: add a "Requirements" or "Prerequisites" section after "Apply It with
      AI" stating that `slobac-audit` requires a harness with subagent-launch
      capability (Cursor and Claude Code by default; composer-2 or similar
      subagent-less harnesses will run incorrectly and should not be used).
    - Validation: read README; confirm the assumption is unmissable for a first-time
      reader.

16. **Update CONTRIBUTING.md regen workflow.**
    - Files: `CONTRIBUTING.md`.
    - Changes: in "After adding an entry" replace step 1 ("Add the slug row to the
      catalog table in `taxonomy/README.md`") with "Run `uv run python
      scripts/gen_taxonomy_index.py` to regenerate the index in both `SKILL.md` and
      `taxonomy/README.md`." Keep the `properdocs build --strict` and cross-link
      verification steps. Also note that editing a slug's `Severity` or `Detection
      Scope` requires re-running the generator.
   - Validation: `CONTRIBUTING.md` reads coherently; cross-reference with the new
     CI drift-check job.

17. **`memory-bank/techContext.md` exception note.**
    - Files: `memory-bank/techContext.md`.
    - Changes: under "Full-manifesto-in-bundle pattern", add a paragraph documenting
      the exception: the navigation index (slug, severity, scope) is generated from
      canonical entry headers and emitted to two locations (SKILL.md and
      taxonomy/README.md) by `scripts/gen_taxonomy_index.py`, with CI drift-check.
      Clarify that the "no generator, no CI drift-check" rule applies to canonical
      manifesto *content* — per-smell entries, principles, glossary, workflows — not
      to a derived navigation index that consumes those entries.
   - Validation: re-read against the "no generator" rule's spirit; ensure the
     exception language preserves the rule's force for canonical content.

18. **CI drift-check job.**
    - Files: `.github/workflows/docs.yaml` (add a parallel `taxonomy-index-drift`
      job adjacent to `build`; keeps related concerns in one workflow file).
    - Changes: new job runs on PR + push:
      1. checkout
      2. setup-uv (same as `build`)
      3. `uv sync --group dev --frozen`
      4. `uv run python scripts/gen_taxonomy_index.py`
      5. `git diff --exit-code skills/slobac-audit/SKILL.md skills/slobac-audit/references/docs/taxonomy/README.md`
      Failure message in the job log instructs the contributor to run the regen
      command locally and commit the result.
    - Validation: locally simulate the drift case (edit a header, don't regen, run
      the script, verify diff is non-empty); revert and confirm clean state has
      empty diff.

19. **Final verification.**
    - Run `uv run pytest` (all green).
    - Run `uv run python scripts/gen_taxonomy_index.py` twice (idempotent — second
      run produces no diff).
    - Run `uv run properdocs build --strict` (still green, links resolve).
    - `git diff` review of all touched files; commit conventional-commit style.

## Technology Validation

Two new dependencies introduced:

- `pytest` (dev group). Industry-standard Python test runner. Verified `uv sync` is
  the project's existing dependency-resolution path. POC: simply add to the dev group
  and confirm `uv run pytest --version` works. No version pin beyond `pytest ~= 8`
  (matching the loose-pin convention from the docs group).
- `scripts/gen_taxonomy_index.py` itself is **stdlib-only** (`pathlib`, `re`,
  `dataclasses`, `argparse`). No new runtime deps; no PEP 723 inline metadata needed
  because uv-managed env from `pyproject.toml` already covers stdlib invocation.

CI: runs on `ubuntu-latest` with the same `astral-sh/setup-uv@v8.0.0` action as the
existing docs build. No new runner image, no new external services.

## Dependencies

- `uv` (already required for docs build)
- `pytest` (new — added to `[dependency-groups] dev`)
- Python ≥ 3.10 (already required by pyproject.toml)

## Challenges & Mitigations

- **Sentinel-region replacement footgun in SKILL.md.** SKILL.md is itself markdown
  rendered to humans + read by orchestrators; sentinel HTML comments must be benign
  in both. *Mitigation:* `<!-- … -->` markdown HTML comments are inert in both
  rendering and orchestrator reading; properdocs strict-build will not warn on them.
  Validation step 9 includes a `properdocs build --strict` run.
- **`tests/python/` collides conceptually with `tests/fixtures/audit/`.** `tests/`
  is already used as an audit-skill fixture root, not a Python test root.
  *Mitigation:* explicit `testpaths = ["tests/python"]` in `[tool.pytest.ini_options]`
  scopes pytest discovery; documented in step 1.
- **Multi-scope rendering ambiguity.** `deliverable-fossils` carries
  `per-test, cross-suite`. *Mitigation:* preserve the original comma-joined string
  byte-for-byte on render; tests guarantee round-trip.
- **CI drift-check vs `release-please`-touched files.** `release-please` rewrites
  `version.txt`, `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json` — none of
  which the generator touches. *Mitigation:* drift-check `git diff --exit-code` is
  scoped to the two specific files we generate; release-please flow is unaffected.
- **`techContext.md` exception risks future-contributor confusion** if phrased
  loosely. *Mitigation:* the exception language explicitly delimits scope to the
  navigation index and explicitly retains the rule's force for canonical content.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [ ] Preflight
- [ ] Build
- [ ] QA
