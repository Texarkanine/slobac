# SLOBAC audit report

- **Scope invoked:** `all` (full taxonomy: 15 supported slugs)
- **Target suite root:** `tests/`
- **Audit date:** 2026-05-06

## Summary

This audit examined **29** shell/shunit2 files (`*.test.sh`) under `tests/` (~379 `test_*()` functions, ~389k characters total). **Ten** finding blocks were recorded across five smell types: **rotten-green** (three locations), **naming-lies** (two tests), **conditional-logic** (three tests), **vacuous-assertion** (one test), **deliverable-fossils** (one file-level comment). Cross-suite analysis produced **no** confirmed findings.

Orchestration: **one** batch assessor run (suite fits one partition at the declared **200k-token** window with ~**60%** content allocation ≈ **400k** character budget); **cross-suite** assessor **ran**; behavior-summary richness was requested at **`full`** for the batch engine (the batch subagent truncated the merged IR table in chat output; clustering for cross-suite still used explicit duplicate-name review and targeted reads). Summary richness tier for behavior IR was **`full`** by plan (< ~500 tests).

Explicit **no findings** lines for requested scopes that produced **zero** findings anywhere in this audit:

- No findings for scope **`semantic-redundancy`**.
- No findings for scope **`wrong-level`**.
- No findings for scope **`pseudo-tested`**.
- No findings for scope **`tautology-theatre`**.
- No findings for scope **`over-specified-mock`**.
- No findings for scope **`implementation-coupled`**.
- No findings for scope **`presentation-coupled`**.
- No findings for scope **`mystery-guest`**.
- No findings for scope **`shared-state`**.
- No findings for scope **`monolithic-test-file`**.

## Findings

### 1. `integration/test_ruleset_commands.test.sh` (file) — `rotten-green`

- **Location:** `integration/test_ruleset_commands.test.sh` → *(no `test_*` functions; harness + comments only)*
- **Smell:** `rotten-green`
- **Rationale:** The file loads `common.sh` and `shunit2`, defines `setUp`/`tearDown`, and documents that coverage lives in unit tests, but it defines **no** `test_*()` bodies. The runner can report success while **no** behavior is exercised or asserted—matching the canonical signal for empty / dead scaffolding versus explicit skip/pending mechanisms. See [rotten-green](https://texarkanine.github.io/slobac/taxonomy/rotten-green/).
- **Prescribed remediation:** Delete the file if integration coverage is intentionally deferred, **or** add real `test_*` functions that invoke the public CLI and assert observable outcomes; if work is intentionally deferred, use the runner’s explicit pending/skip mechanism with a stated reason instead of a silent empty suite.
- **Why this isn't a false positive:** This is not an explicitly skipped test suite; it is a passing file with zero test functions—distinct from a declared `skip`/`todo` that preserves honesty about coverage.

### 2. `integration/test_cli_add_remove.test.sh` → `test_add_nonexistent_rule_fails` — `naming-lies`

- **Location:** `integration/test_cli_add_remove.test.sh` → `test_add_nonexistent_rule_fails`
- **Smell:** `naming-lies`
- **Rationale:** The identifier claims **`fails`**, while comments and assertions document **success** (exit code **0**) with warning text and no manifest mutation—the title does not match what the body verifies (Signal: title/doc claims X, assertions prove Y). See [naming-lies](https://texarkanine.github.io/slobac/taxonomy/naming-lies/).
- **Prescribed remediation:** Rename the test and/or adjust claims to match the contract under test (graceful handling with warning and exit **0**), or change expectations if the product contract is actually non-zero exit—then align assertions.
- **Why this isn't a false positive:** This is not benign synonymy across domains; “fails” vs asserted exit **0** is a direct contradiction.

### 3. `integration/test_cli_init.test.sh` → `test_init_mode_defaults` — `naming-lies`

- **Location:** `integration/test_cli_init.test.sh` → `test_init_mode_defaults`
- **Smell:** `naming-lies`
- **Rationale:** Comments claim **local** default behavior while stdin supplies **`commit`** via `printf`, and assertions only check **`0 $?`** without establishing which mode was selected—documentation-level claims are not carried by the oracle set (Signal: title/comment vs assertion mismatch). See [naming-lies](https://texarkanine.github.io/slobac/taxonomy/naming-lies/).
- **Prescribed remediation:** Rename comments/test scope to match the stdin-driven interaction, assert on resulting manifests/paths for the intended mode, or change stdin to exercise the default-mode path the comment describes.
- **Why this isn't a false positive:** Under-specified titles are acceptable when the body is a strict subset of a broader claim; here the comment makes a **specific mode-default** claim that the stdin choice and assertions do not substantiate.

### 4. `integration/test_cli_add_remove.test.sh` → `test_add_rule_with_invalid_repository` — `conditional-logic`

- **Location:** `integration/test_cli_add_remove.test.sh` → `test_add_rule_with_invalid_repository`
- **Smell:** `conditional-logic`
- **Rationale:** Assertions live under `if [ $exit_code -ne 0 ]; then … fi`; if the command **succeeds** unexpectedly, the test may pass **without** asserting the failure contract (Signal: asymmetric branches where one path lacks a decisive oracle). See [conditional-logic](https://texarkanine.github.io/slobac/taxonomy/conditional-logic/).
- **Prescribed remediation:** Split into pinned-success vs pinned-failure tests, or assert unconditionally on the outcome contract for both exit-code outcomes.
- **Why this isn't a false positive:** This is not the symmetric parameterized pattern where **both** branches carry equivalent assertions.

### 5. `integration/test_cli_add_remove.test.sh` → `test_add_rule_dual_mode_requires_mode` — `conditional-logic`

- **Location:** `integration/test_cli_add_remove.test.sh` → `test_add_rule_dual_mode_requires_mode`
- **Smell:** `conditional-logic`
- **Rationale:** The body branches on multiple outcomes (`COMMAND_FAILED`, nested `if`/`elif`) with uneven oracle strength across paths—candidate signal for branching-heavy tests where not every path gets an equivalent assertion (Signals in canonical entry for branching / cyclomatic complexity in tests). See [conditional-logic](https://texarkanine.github.io/slobac/taxonomy/conditional-logic/).
- **Prescribed remediation:** Split into separate tests with deterministic fixtures—one for ambiguous-mode failure messages, one for smart-default success—each with unconditional assertions on its contract.
- **Why this isn't a false positive:** Not a single-table parameterized case with symmetric assertions on each row.

### 6. `unit/test_deinit_modes.test.sh` → `test_deinit_partial_cleanup_on_error` — `conditional-logic`

- **Location:** `unit/test_deinit_modes.test.sh` → `test_deinit_partial_cleanup_on_error`
- **Smell:** `conditional-logic`
- **Rationale:** The test mixes `if`/`fi` setup with nested filesystem branches—some paths skip setup—combined with pipeline patterns that weaken branch predictability (canonical signals for conditional structure obscuring the oracle). See [conditional-logic](https://texarkanine.github.io/slobac/taxonomy/conditional-logic/).
- **Prescribed remediation:** Split scenarios so each test has one precondition shape and one decisive outcome assertion.
- **Why this isn't a false positive:** The structure couples multiple execution shapes without pinning a single observable contract per branch.

### 7. `unit/test_deinit_modes.test.sh` → `test_deinit_partial_cleanup_on_error` — `vacuous-assertion`

- **Location:** `unit/test_deinit_modes.test.sh` → `test_deinit_partial_cleanup_on_error`
- **Smell:** `vacuous-assertion`
- **Rationale:** Uses `echo "$output" | grep -q … || true`, which **cannot fail** the pipeline—so the check does not discriminate pass vs fail outcomes (weak / vacuous oracle). See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Remove `|| true` from assertion pipelines; assert concrete stderr/exit-code contracts, or use explicit `skip` when behavior is genuinely optional.
- **Why this isn't a false positive:** `|| true` explicitly defeats grep’s failure signal—it is not a flake-mitigation pattern with an alternate oracle.

### 8. `unit/test_conflict_resolution.test.sh` → `test_migrate_rule_local_to_commit` — `rotten-green`

- **Location:** `unit/test_conflict_resolution.test.sh` → `test_migrate_rule_local_to_commit`
- **Smell:** `rotten-green`
- **Rationale:** Multiple `ls -hal` invocations appear in the test body without participating in assertions—debug listing scaffolding rather than behavioral oracles (canonical signals for dead/exploration noise). See [rotten-green](https://texarkanine.github.io/slobac/taxonomy/rotten-green/).
- **Prescribed remediation:** Remove listing commands; if directory inspection is part of the contract, replace with asserts on the specific paths that matter.
- **Why this isn't a false positive:** The listings are not referenced by assertions and read as leftover diagnostics, not intentional coverage.

### 9. `unit/test_deinit_modes.test.sh` → `test_deinit_local_mode_only` — `rotten-green`

- **Location:** `unit/test_deinit_modes.test.sh` → `test_deinit_local_mode_only`
- **Smell:** `rotten-green`
- **Rationale:** Contains `pwd`, `ls -hal`, and `set -x` / `set +x` around setup—diagnostic noise not tied to assertions (same canonical signal class). See [rotten-green](https://texarkanine.github.io/slobac/taxonomy/rotten-green/).
- **Prescribed remediation:** Strip exploratory commands from the test body; keep only SUT calls and assertions (or gate tracing behind an explicit debug flag outside CI).
- **Why this isn't a false positive:** These commands do not encode product behavior and match typical leftover scaffolding.

### 10. `unit/test_cache_isolation.test.sh` (file header comment) — `deliverable-fossils`

- **Location:** `unit/test_cache_isolation.test.sh` → *(file-level header comment, lines 3–7)*
- **Smell:** `deliverable-fossils`
- **Rationale:** The live comment frames work as **“Phase 7 bug fixes”**—schedule/deliverable vocabulary rather than durable **product behavior** vocabulary for what global vs repo cache invariants are under test (canonical Phase A signal: sprint/release-shaped framing on the spec surface). See [deliverable-fossils](https://texarkanine.github.io/slobac/taxonomy/deliverable-fossils/).
- **Prescribed remediation:** Rewrite the header to behavior-first language (what cache/repo invariants are enforced); keep ticket/phase history in commit messages, not the active test spec surface.
- **Why this isn't a false positive:** “Phase 7” is schedule language, not user-visible capability language from the SUT contract.

## Tests considered but not flagged

- **CLI glyph / `list` output tests** across integration and unit suites: asserting rendered Unicode markers and names appears appropriate where terminal output **is** the contract for this tool—**presentation-coupled** false-positive guards apply.
- **Substring / grep-heavy env-var and help tests**: weaker in the abstract, but here they anchor env override and help semantics without a concrete counterexample mutant—left unflagged for **vacuous-assertion**.
- **Symmetric branch coverage** (e.g. help tests where **both** branches fail the suite on miss): treated as parameterized-style symmetry—not **conditional-logic**.
- **Integration vs unit tests sharing names** (e.g. `test_deinit_local_mode_only` in `integration/test_cli_deinit.test.sh` vs `unit/test_deinit_modes.test.sh`): targeted comparison shows **different seams**—full CLI/`run_ai_rizz` vs sourced `cmd_*` functions—not redundant observables for **semantic-redundancy**.
- **`integration/test_ruleset_commands.test.sh` vs `unit/test_ruleset_commands.test.sh`**: empty integration stub vs substantive unit file—flagged under **rotten-green** for the empty file, not treated as duplicate coverage.

## Out-of-scope requests

None.
