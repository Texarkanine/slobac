# SLOBAC audit report

- **Scope invoked:** `all` (resolved to: `conditional-logic`, `deliverable-fossils`, `implementation-coupled`, `monolithic-test-file`, `mystery-guest`, `naming-lies`, `over-specified-mock`, `presentation-coupled`, `pseudo-tested`, `rotten-green`, `semantic-redundancy`, `shared-state`, `tautology-theatre`, `vacuous-assertion`, `wrong-level`)
- **Target suite root:** `tests/`
- **Audit date:** 2026-05-06

## Summary

Audited 33 shell test files (377 tests, ~389K chars; ecosystem: shell+shunit2; tiers: `unit/`, `integration/`) using a 1M-token context window. Orchestration: 1 batch assessor (suite fit a single batch), `full` summary richness, then 1 cross-suite assessor over the merged behavior summary table. Total findings: **17**, broken down as follows.

- `conditional-logic`: 1
- `monolithic-test-file`: 1
- `naming-lies`: 2
- `rotten-green`: 2
- `semantic-redundancy`: 7
- `tautology-theatre`: 1
- `vacuous-assertion`: 3
- No findings for scope `deliverable-fossils` (Phase A — rename detection from batch).
- No findings for scope `deliverable-fossils` (Phase B — regrouping from cross-suite assessor).
- No findings for scope `implementation-coupled`.
- No findings for scope `mystery-guest`.
- No findings for scope `over-specified-mock`.
- No findings for scope `presentation-coupled`.
- No findings for scope `pseudo-tested`.
- No findings for scope `shared-state`.
- No findings for scope `wrong-level`.

The largest single locus is the cross-tier duplication between `tests/integration/test_cli_init.test.sh` and `tests/unit/test_initialization.test.sh` (4 of the 7 semantic-redundancy findings), and a glyph-rendering 3×3 matrix duplicated between `tests/integration/test_cli_list_sync.test.sh` and `tests/unit/test_rule_management.test.sh`. The largest single-file weakness is `tests/integration/test_help_and_usage.test.sh`, which carries 2 vacuous-assertion findings and 1 naming-lies finding (3 of its 5 tests). The most dangerous individual finding is the `assertTrue ... true` tautology in `tests/unit/test_list_display.test.sh:87` — it cannot fail.

## Findings

### 1. `tests/integration/test_cli_add_remove.test.sh:310` — `conditional-logic`

- **Location:** `integration/test_cli_add_remove.test.sh` → `test_add_rule_with_invalid_repository`
- **Smell:** `conditional-logic`
- **Rationale:** The body wraps `cmd_add_rule` with `|| echo "ADD_FAILED"` and then guards every assertion behind `if [ $exit_code -ne 0 ]; then assert_output_contains ...; fi`. On the success branch the test silently passes with no assertion at all — an asymmetric `if` shape (one arm asserts, the other returns silently). See <https://texarkanine.github.io/slobac/taxonomy/conditional-logic/>.
- **Prescribed remediation:** Remove the branch and assert unconditionally on the contract: invalid-URL inputs MUST exit non-zero AND emit a recognizable repository error. Pin the precondition by truly corrupting the manifest as the setup already does, then `assertNotEquals 0 "$exit_code"` plus a single `assert_output_contains` for the error vocabulary.
- **Why this isn't a false positive:** Not the symmetric parameterized-table pattern — only the failure arm asserts; the success arm returns silently with no assertion, exactly the asymmetric shape the smell targets.

### 2. `tests/integration/test_cli_init.test.sh:232` — `vacuous-assertion`

- **Location:** `integration/test_cli_init.test.sh` → `test_init_mode_defaults`
- **Smell:** `vacuous-assertion`
- **Rationale:** Title and inline comment claim the test exercises mode defaulting ("should prompt and set default"), but the body's only oracle is `assertEquals 0 $?`. Any non-zero failure of the prompt path or any wrong default selection still passes the test as long as exit is 0 — the strongest wrong implementation (silently picking the opposite mode, or no mode) still passes. See <https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/>.
- **Prescribed remediation:** Strengthen the body. After piping `commit` into `init`, assert that `ai-rizz.skbd` exists (commit chosen) AND `ai-rizz.local.skbd` does not — i.e., a positive structural check on which mode was actually created, not just exit code.
- **Why this isn't a false positive:** Not a side-effect-absence contract (which is the documented over-trigger) — the contract is a positive observable (which mode got created) that the test simply omits to verify.

### 3. `tests/integration/test_cli_init.test.sh:232` — `naming-lies`

- **Location:** `integration/test_cli_init.test.sh` → `test_init_mode_defaults`
- **Smell:** `naming-lies`
- **Rationale:** The identifier `test_init_mode_defaults` claims behavior about *which* mode the prompt defaults to, while the body verifies only command success. Title-noun "defaults" has zero surface in the assertion set. See <https://texarkanine.github.io/slobac/taxonomy/naming-lies/>.
- **Prescribed remediation:** Either rename to `test_init_with_piped_mode_input_succeeds` (rename to match body) or strengthen the body to verify the defaulted mode (preferred; pairs with the `vacuous-assertion` finding above).
- **Why this isn't a false positive:** Not under-specified — the title makes a specific claim about a default that the body simply does not exercise; this is the title-overpromises shape, not the terse-title shape.

### 4. `tests/integration/test_help_and_usage.test.sh:28` — `vacuous-assertion`

- **Location:** `integration/test_help_and_usage.test.sh` → `test_help_command_shows_content`
- **Smell:** `vacuous-assertion`
- **Rationale:** The oracle is two extremely loose disjunctive substring matches (`Usage|usage|USAGE` and `command|Command|COMMAND`) plus a non-null assertion on the entire help blob. A SUT that printed the single byte `usage command` would pass; many interesting wrong implementations (truncated help, misspelled commands, missing flags) survive. The test even labels itself "very loose checks". See <https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/>.
- **Prescribed remediation:** Replace with a structural matcher: assert that the help text contains a stable contract surface — e.g., the six top-level command names enumerated together, plus a known flag like `--local`. The presentation tests for help should pin a contract, not just word presence.
- **Why this isn't a false positive:** Not a side-effect-absence contract and not a TS/Python type-narrowing two-stage pattern; it is a real return-value oracle deliberately chosen weak.

### 5. `tests/integration/test_help_and_usage.test.sh:46` — `vacuous-assertion`

- **Location:** `integration/test_help_and_usage.test.sh` → `test_no_arguments_shows_usage`
- **Smell:** `vacuous-assertion`
- **Rationale:** Same shape as the above — a single very-broad `Usage|usage|USAGE|help|Help|HELP` disjunction plus `assertNotNull` on the whole output. A no-op SUT that just printed "help" would pass. See <https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/>.
- **Prescribed remediation:** After running `ai-rizz` with no args, assert exit code is non-zero AND that the output enumerates the actual command list (collapse with `test_help_command_shows_content` if both can share one structural matcher).
- **Why this isn't a false positive:** Not the documented-side-effect-absence pattern — the contract here is the rendered usage block; the test simply doesn't check enough of it.

### 6. `tests/integration/test_help_and_usage.test.sh:97` — `naming-lies`

- **Location:** `integration/test_help_and_usage.test.sh` → `test_help_works_from_any_directory`
- **Smell:** `naming-lies`
- **Rationale:** Title claims behavior "from any directory" (a quantifier — every directory). The body picks exactly one directory (`./subdir`) and runs `ai-rizz help` once. The "any-directory" claim is unprovable from one sample; the body verifies "help works from one subdirectory", not the universal claim. See <https://texarkanine.github.io/slobac/taxonomy/naming-lies/>.
- **Prescribed remediation:** Rename to `test_help_works_from_subdirectory` to match the body's actual scope. If the universal claim is the real intent, parameterize over a representative set (project root, subdir, deep subdir, sibling tree) and assert success in each.
- **Why this isn't a false positive:** Not a domain-synonym confusion — "any directory" is a clear universal-quantifier claim that one observation cannot establish.

### 7. `tests/unit/test_deinit_modes.test.sh:196` — `rotten-green`

- **Location:** `unit/test_deinit_modes.test.sh` → `test_deinit_partial_cleanup_on_error`
- **Smell:** `rotten-green`
- **Rationale:** The test makes the manifest read-only, runs `cmd_deinit --local`, and the body's only would-be oracle is `echo "$output" | grep -q "error\|permission\|failed" || true` — the trailing `|| true` swallows the grep's exit code so the assertion is dead scaffolding. There are no other assertions in the test (the chmod 644 lines are cleanup). The function reports green regardless of whether deinit produced any error message at all. See <https://texarkanine.github.io/slobac/taxonomy/rotten-green/>.
- **Prescribed remediation:** If the contract is "graceful error", replace the dead grep with a real assertion: capture exit code AND assert the readable error vocabulary unconditionally, plus assert that the manifest still exists (not partially deleted). If the test was a stub, convert to `# TODO`/skip with a reason.
- **Why this isn't a false positive:** Not linter-covered (shellcheck doesn't flag `|| true` swallowing assertions), and there is no runner-native skip marker in use; this is a silent-green stub with assertion-shaped statements that verify nothing.

### 8. `tests/unit/test_error_handling.test.sh:251` — `rotten-green`

- **Location:** `unit/test_error_handling.test.sh` → `test_graceful_empty_repository`
- **Smell:** `rotten-green`
- **Rationale:** After setting up an empty repo and running `cmd_init` and `cmd_list`, the test's only oracle is `echo "$output" | grep -q "No rules available\|empty\|found" || true` — the `|| true` makes the assertion non-binding, and the comment even labels it "May show empty state". No other assertion follows. The body executes the SUT but reports green regardless of output content. See <https://texarkanine.github.io/slobac/taxonomy/rotten-green/>.
- **Prescribed remediation:** Decide the contract. Either (a) `cmd_list` against an empty repo emits a specific empty-state line — assert it unconditionally, drop the `|| true`; or (b) the contract is just "does not crash" — replace the dead grep with `assertEquals 0 $?` so at least the exit-code contract is pinned.
- **Why this isn't a false positive:** Not a documented side-effect-absence contract (`cmd_list` has a positive return: a printed listing), and not under runner-native skip.

### 9. `tests/unit/test_list_display.test.sh:87` — `tautology-theatre`

- **Location:** `unit/test_list_display.test.sh` → `test_list_handles_empty_commands_directory`
- **Smell:** `tautology-theatre` (trivial-tautology variant)
- **Rationale:** The final oracle is literally `assertTrue "commands/ should be shown" true` — a built-in tautology that cannot fail. Per the canonical entry's signal list, `assertTrue(true)` is the trivial-tautology variant. The earlier `grep -q "commands"` is guarded with `|| fail` so that line does verify presence, but the explicit `assertTrue true` adds zero coverage and the comment block above it ("This is a bit tricky to test precisely…") shows the author abandoned the empty-directory check. See <https://texarkanine.github.io/slobac/taxonomy/tautology-theatre/>.
- **Prescribed remediation:** Delete the `assertTrue ... true` line; if the empty-commands behavior is part of the contract, replace it with an actual structural check — e.g., parse the list output, locate the `test-empty` ruleset block, and assert that no file lines appear under its `commands/` subtree.
- **Why this isn't a false positive:** Not a one-off framework-bootstrap smoke test (this file has many real tests); not a boundary-fake feeding a real SUT — it is exactly the trivial-tautology `assertTrue(true)` shape called out in the signals.

### 10. `tests/unit/test_ruleset_commands.test.sh` (whole file) — `monolithic-test-file`

- **Location:** `unit/test_ruleset_commands.test.sh` (711 lines, 21 tests)
- **Smell:** `monolithic-test-file`
- **Rationale:** The file is dissected by author-supplied section-header comments into five clearly distinct subjects: (1) "UNIFIED COMMAND HANDLING TESTS (.md files in ruleset root)" lines 30–188, (2) "MIGRATION TESTS" for old flat-command cleanup lines 190–310, (3) "DETECTION AND VALIDATION TESTS" for cross-mode ruleset addition lines 312–407, (4) "COMMAND COPYING TESTS" for symlink/auto-create behavior lines 409–555, and (5) "REMOVE RULESET MODE FLAG TESTS" for `cmd_remove_ruleset` flag-parsing bugs lines 557–706. Sections 1–4 concern `cmd_add_ruleset` deployment semantics; section 5 concerns `cmd_remove_ruleset` argument-order parsing — a different SUT and a different concern. The section-header-comment signal plus the imports/SUT divergence between sections meet the smell's mixed-domain criterion. See <https://texarkanine.github.io/slobac/taxonomy/monolithic-test-file/>.
- **Prescribed remediation:** Describe-before-edit each test, then split into per-domain files: `test_ruleset_command_handling.test.sh` (sections 1, 4), `test_ruleset_command_migration.test.sh` (section 2), `test_ruleset_mode_validation.test.sh` (section 3), `test_remove_ruleset_flag_parsing.test.sh` (section 5). Use `tests/_support/` for any shared `create_*` helpers.
- **Why this isn't a false positive:** Not a co-location-by-convention ecosystem (shell + shunit2 has no enforced one-file-per-package idiom), and not a single-domain parameterized file — section 5 verifies a different command's flag parser whose only relation to sections 1–4 is the word "ruleset".

### 11. `test_init_local_mode_creates_proper_structure` + `test_init_commit_mode_creates_proper_structure` ↔ `test_init_local_mode_only` + `test_init_commit_mode_only` — `semantic-redundancy`

- **Location:** `integration/test_cli_init.test.sh:29 test_init_local_mode_creates_proper_structure` and `integration/test_cli_init.test.sh:53 test_init_commit_mode_creates_proper_structure` ↔ `unit/test_initialization.test.sh:34 test_init_local_mode_only` and `unit/test_initialization.test.sh:57 test_init_commit_mode_only`
- **Smell:** `semantic-redundancy`
- **Rationale:** Each pair verifies the same observable: after `init --local` (resp. `--commit`), the corresponding manifest+subdir exist, the opposite-mode artifacts do not, the pre-commit hook with `BEGIN ai-rizz hook` exists (local) or git-tracking is correct (commit). The integration variants invoke via `run_ai_rizz` (subprocess) and the unit variants via the sourced `cmd_init`, but both call the same shell function against the same temp-dir fixture and assert on the same on-disk artifacts. The unit variants' assertion sets are a strict subset of the integration variants', which add manifest-header byte-equality. Matches Signals "Mirrored suites … with identical scenario matrices" and "assertion sets that are subsets of each other". See <https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/>.
- **Prescribed remediation:** Keep the two integration tests as canonical — they exercise the user-visible CLI surface, carry the strictest oracle (4-field manifest header byte-equality plus `assert_git_tracks` for commit), and use the smallest fixture (`setup_integration_test`). Fold the unit `is_mode_active` boolean checks into the integration tests as additional asserts, then delete `test_init_local_mode_only` and `test_init_commit_mode_only`.
- **Why this isn't a false positive:** Not "mirrored components are intentional duplication" — `ai-rizz` is one product, not two implementations of a shared contract; the unit/integration split here is tier depth, not a separate deliverable whose regression must be caught independently.

### 12. `test_init_twice_same_mode_idempotent` (integration ↔ unit) — `semantic-redundancy`

- **Location:** `integration/test_cli_init.test.sh:128 test_init_twice_same_mode_idempotent` ↔ `unit/test_initialization.test.sh:116 test_init_twice_same_mode_idempotent`
- **Smell:** `semantic-redundancy`
- **Rationale:** Identical test name across files, identical SUT (`init --local` invoked twice), identical observable (post-second-invocation: local manifest+dir still exist, commit mode still absent). Integration adds the hook-marker check; unit adds an `is_mode_active commit = false` check. Subset relation across an across-file behavior-sentence cluster — matches the Signal "Cross-file behavior-sentence clusters" plus "assertion sets that are subsets of each other". See <https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/>.
- **Prescribed remediation:** Keep the integration test as canonical (stronger oracle, exercises the user-visible CLI). Fold the unit's `is_mode_active commit = false` assertion into it; delete the unit copy.
- **Why this isn't a false positive:** Not "same surface, different business concept" — the one-sentence behavior summaries are identical (idempotent re-init preserves single-mode state), not divergent domain rules.

### 13. `test_init_different_modes_creates_dual_mode` (integration ↔ unit) — `semantic-redundancy`

- **Location:** `integration/test_cli_init.test.sh:153 test_init_different_modes_creates_dual_mode` ↔ `unit/test_initialization.test.sh:161 test_init_different_modes_creates_dual_mode`
- **Smell:** `semantic-redundancy`
- **Rationale:** Identical test name, identical setup (init `--local` then `--commit`), identical observable (both manifests + both subdirs exist; both modes report active). Integration asserts hook-marker presence + `assert_git_tracks`; unit asserts `is_mode_active local && is_mode_active commit`. Strict subset relation; matches the "behavior-sentence cluster" + "subset assertion set" Signals. See <https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/>.
- **Prescribed remediation:** Keep the integration test as canonical (broader oracle, user-facing surface). Fold the unit's `is_mode_active` dual-mode check into it as an additional assertion; delete the unit copy.
- **Why this isn't a false positive:** Not "contract-duplication of production constants" — neither test re-states a production constant; they assert on side effects of the same call sequence.

### 14. `test_init_requires_mode_selection` ↔ `test_init_requires_mode_flag` — `semantic-redundancy`

- **Location:** `integration/test_cli_init.test.sh:77 test_init_requires_mode_selection` ↔ `unit/test_initialization.test.sh:73 test_init_requires_mode_flag`
- **Smell:** `semantic-redundancy`
- **Rationale:** Both feed empty stdin to a no-mode-flag `init` invocation against the same source-repo+target-dir fixture and assert the captured output matches the loose alternation `mode|local|commit|choose|select`. Identical SUT shape, identical oracle vocabulary — matches the Signal "two tests cover … parallel operations where one has a strictly weaker oracle" (the unit version drops the integration's `ERROR_OCCURRED` branch). See <https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/>.
- **Prescribed remediation:** Keep the integration test as canonical — the user-visible CLI prompt is exactly what this loose oracle is meant to capture, and the integration version handles both the prompt branch and the failure branch. Delete the unit copy.
- **Why this isn't a false positive:** Not "domain vocabulary that looks like fossil/duplicate vocabulary" — the matched substring `mode|local|commit|choose|select` is the literal prompt the SUT renders, and both tests are pinning that single rendering, not two different prompts that coincidentally share words.

### 15. `test_init_invalid_repository_url` ↔ `test_error_source_repo_unavailable` — `semantic-redundancy`

- **Location:** `integration/test_cli_init.test.sh:114 test_init_invalid_repository_url` ↔ `unit/test_error_handling.test.sh:146 test_error_source_repo_unavailable`
- **Smell:** `semantic-redundancy`
- **Rationale:** Both invoke `init invalid://nonexistent[.repo] --local`, capture output, and assert (a) the command fails and (b) no local manifest is created. Integration uses the sentinel `COMMAND_FAILED`; unit uses a slightly broader `repository|clone|fetch|unavailable|ERROR_OCCURRED` substring. Same SUT, same negative file-presence oracle, same failure observable. Matches "Adjacent … blocks that call the same SUT entry point with identical arguments, with assertion sets that are subsets of each other". See <https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/>.
- **Prescribed remediation:** Keep the integration test as canonical — it lives in the file dedicated to CLI init behavior and matches the user-facing failure shape. Delete the unit copy; if the broader vocabulary alternation is felt to add coverage, fold it into the integration test as an additional `assert_output_contains` line.
- **Why this isn't a false positive:** Not "mirrored components" — there is one `cmd_init` URL-validation path, not two implementations whose contracts must be independently regression-guarded; the unit/integration tier difference is not protecting different knowledge.

### 16. Glyph-rendering 3×3 matrix (integration ↔ unit) — `semantic-redundancy`

- **Location:** `integration/test_cli_list_sync.test.sh:34 test_list_shows_correct_glyphs_local_only`, `integration/test_cli_list_sync.test.sh:59 test_list_shows_correct_glyphs_commit_only`, `integration/test_cli_list_sync.test.sh:84 test_list_shows_correct_glyphs_dual_mode` ↔ `unit/test_rule_management.test.sh:33 test_list_local_mode_only_glyphs`, `unit/test_rule_management.test.sh:49 test_list_commit_mode_only_glyphs`, `unit/test_rule_management.test.sh:64 test_list_dual_mode_all_glyphs`
- **Smell:** `semantic-redundancy`
- **Rationale:** A 3×3 matrix duplicated across tiers. The local-only triple verifies `◐ rule1`, `○ rule2`, never `●`; the commit-only triple flips local/committed glyphs; the dual triple shows all three glyphs across rule1/rule2/rule3. Same fixtures (rules added in the relevant mode), same SUT (`cmd_list` rendering output), same glyph-vocabulary oracles. Matches the Signal "Mirrored suites across near-isomorphic components … with identical scenario matrices and only … fixtures differing" — here the only difference is invocation depth, not knowledge under guard. See <https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/>.
- **Prescribed remediation:** Keep the integration triple as canonical — it asserts on user-visible CLI list output, which is the actual deliverable of `cmd_list`. Delete the three unit-side glyph tests. Other unit tests in `test_rule_management.test.sh` (rule removal, manifest cleanup) are not redundant and should remain.
- **Why this isn't a false positive:** Not the "parameterized matrix is intentional coverage" guard — the matrix collision is across files, not within one file's parameterized rows; collapsing the unit triple does not lose any per-tier-product contract because both tiers exercise the same single rendering function.

### 17. No-git-repo failure pairs (commit + local) duplicated across two unit files — `semantic-redundancy`

- **Location:** `unit/test_error_handling.test.sh:90 test_error_git_repo_required_for_commit_mode` and `unit/test_error_handling.test.sh:105 test_local_mode_requires_git` ↔ `unit/test_global_only_context.test.sh:136 test_commit_init_fails_outside_git_repo` and `unit/test_global_only_context.test.sh:121 test_local_init_fails_outside_git_repo`
- **Smell:** `semantic-redundancy`
- **Rationale:** Both pairs (commit and local) verify that `cmd_init --commit` (resp. `--local`) outside a git repo exits non-zero and emits output containing `git` (case-insensitive). Identical SUT (`rm -rf .git` then `cmd_init` — or for `test_global_only_context.test.sh`, the file's setUp constructs a non-git cwd, which is equivalent), identical oracle (non-zero exit + `grep -qi git`). Two cross-file paraphrases of the same one-sentence behavior summary. Matches "Cross-file behavior-sentence clusters" with the local and commit cases each duplicated. See <https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/>.
- **Prescribed remediation:** Keep the `test_error_handling.test.sh` versions as canonical — that file's stated purpose is to consolidate `cmd_init` error paths, the no-git-repo error is a generic init concern not specific to global mode, and those tests already sit beside the broader error-handling coverage. Delete `test_local_init_fails_outside_git_repo` and `test_commit_init_fails_outside_git_repo` from `test_global_only_context.test.sh`; the file's `test_global_init_works_outside_git_repo` already provides the only non-redundant contrast that file's mission requires (global succeeds without git).
- **Why this isn't a false positive:** Not "knowledge-DRY contract guard" — neither pair re-states a production constant or guards drift between test and production; both tests are observing the same single behavior of `cmd_init` (it errors when `.git` is absent), so merging does not lose any independently-protected knowledge.

## Tests considered but not flagged

- `unit/test_sync_operations.test.sh:199` `test_sync_handles_missing_manifests` — exhibits the same `grep ... || true` non-binding-assertion shape as findings 7 and 8 and was tagged `rotten-green?` in the behavior summaries, but the batch assessor declined to promote it pending a closer read of whether any later oracle exists. The test as written is a strong rotten-green candidate; recommend manual review before the next audit pass.
- The mode-symmetric three-up clusters (`test_command_modes.test.sh`, `test_command_sync.test.sh`, `test_command_entity_detection.test.sh`, `test_skill_sync.test.sh`, `test_mode_transition_warnings.test.sh`, `test_cache_isolation.test.sh`) all looked like cross-file `semantic-redundancy` candidates from the behavior summary, but on targeted source reads each triple is an intentional matrix verifying the per-mode dispatch contract — different fixtures (`MOCK_REPO_DIR` vs `GLOBAL_*`), and the routing knowledge under guard would degrade if collapsed. The parameterized-rows guard from the canonical entry applies.
- The within-file `test_deinit_modes.test.sh:75` (`test_deinit_requires_mode_selection`) and `test_deinit_modes.test.sh:236` (`test_deinit_interactive_mode_selection`) pair was a strong candidate but the cross-suite assessor's targeted read found enough divergence in setup state (dual-mode-with-rules vs. dual-mode-bare) to defer. Recommend the maintainer collapse the pair manually if the divergence is incidental rather than intentional.
- Author debug residue exists in three unit tests (`test_conflict_resolution.test.sh:29` repeated `ls -hal`; `test_deinit_modes.test.sh:28` `pwd`/`ls -hal`/`set -x`; `test_deinit_modes.test.sh:75` stray `echo "cmd_init ..."`). This is hygiene noise, not a SLOBAC smell — the tests still have real assertions — but worth cleaning up.
- `tests/integration/test_ruleset_commands.test.sh` contains zero `test_*` functions (only `setUp`/`tearDown` plus a comment block deferring command coverage to the unit tests). Not a smell finding under the in-scope set, but the file is dead weight in its current form — either delete it or move the deferred coverage in.

## Out-of-scope requests

None. The operator invoked the wildcard `all`, which resolves to the full supported-slug set; every requested slug was audited.
