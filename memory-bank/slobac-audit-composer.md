# SLOBAC audit report

- **Scope invoked:** `all` (conditional-logic, deliverable-fossils, implementation-coupled, monolithic-test-file, mystery-guest, naming-lies, over-specified-mock, presentation-coupled, pseudo-tested, rotten-green, semantic-redundancy, shared-state, tautology-theatre, vacuous-assertion, wrong-level)
- **Target suite root:** `tests/` (repository root-relative)
- **Audit date:** 2026-05-06

## Summary

The suite has **three** flagged issues across **two** smells (`rotten-green` twice, `vacuous-assertion` once). Orchestration used **two** readonly batch shards (characters under a **200k-token** assumption with **≈60%** content allowance; greedy partition kept paths lexicographic). **Cross-suite** analysis ran for `semantic-redundancy`, `wrong-level`, and `deliverable-fossils` (Phase B). Behavior summaries used **full** richness. Confirmed tier conventions: `tests/unit/` → unit, `tests/integration/` → integration. **No findings for scope** `conditional-logic`. **No findings for scope** `deliverable-fossils`. **No findings for scope** `implementation-coupled`. **No findings for scope** `monolithic-test-file`. **No findings for scope** `mystery-guest`. **No findings for scope** `naming-lies`. **No findings for scope** `over-specified-mock`. **No findings for scope** `presentation-coupled`. **No findings for scope** `pseudo-tested`. **No findings for scope** `semantic-redundancy`. **No findings for scope** `shared-state`. **No findings for scope** `tautology-theatre`. **No findings for scope** `wrong-level`.

## Findings

### 1. `integration/test_ruleset_commands.test.sh` — `(shunit2 harness; zero registered tests)` — `rotten-green`

- **Location:** `integration/test_ruleset_commands.test.sh` → _(no `test_*` functions registered — `shunit2` reports “Ran 0 tests. OK”)_
- **Smell:** `rotten-green`
- **Rationale:** The file installs integration-style `setUp`/`tearDown`, sources `common.sh`, and loads `shunit2`, yet defines **zero** test functions despite the banner claiming integration coverage for ruleset commands. Runner output is green with no exercised assertions ([Signals: empty body / scaffolding that counts as passing](https://texarkanine.github.io/slobac/taxonomy/rotten-green/), canonical entry `references/docs/taxonomy/rotten-green.md`).
- **Prescribed remediation:** Either delete this file if integration coverage is deliberately deferred solely to unit tests (as comments state), replacing it with an optional doc pointer; or register real CLI-level `test_*` cases that observe ruleset/command behavior distinct from unit coverage (`describe-before-edit` first). If intentional deferral persists, surface it with an explicit skipped/pending convention your runner understands so CI does not show an empty-but-green suite.
- **Why this isn't a false positive:** This is not a linter-flagged jest `expect` gap; shell `shunit2` exited **0** while running **zero** tests — the harness success is orthogonal to verifying product behavior (`rotten-green` false-positive guards target linters already covering empty examples and explicit skips).

### 2. `unit/test_deinit_modes.test.sh` → `test_deinit_local_mode_only` — `rotten-green`

- **Location:** `unit/test_deinit_modes.test.sh` → `test_deinit_local_mode_only`
- **Smell:** `rotten-green`
- **Rationale:** The opening of the body contains exploratory `pwd`, `ls -hal`, `set -x` / `set +x`, which resemble debugging residue rather than deterministic setup or assertions—the same scaffold class warned by dead logging left where an oracle belonged ([signals on debug remnants / dead scaffolding](https://texarkanine.github.io/slobac/taxonomy/rotten-green/), canonical entry `references/docs/taxonomy/rotten-green.md`).
- **Prescribed remediation:** Remove stray logging/xtrace statements; codify intentional setup assertions if directory layout mattered temporarily; keep only steps that stabilize the reproducible precondition for `cmd_init`.
- **Why this isn't a false positive:** The commands do not reinforce the asserted manifest/exclude/post-deinit filesystem state—they only expand trace noise unrelated to `_test intent`, unlike legitimate shell setup that exports paths or verifies fixtures.

### 3. `integration/test_help_and_usage.test.sh` → `test_help_mentions_key_commands` — `vacuous-assertion`

- **Location:** `integration/test_help_and_usage.test.sh` → `test_help_mentions_key_commands`
- **Smell:** `vacuous-assertion`
- **Rationale:** The name promises that help “mentions **key commands**”, but the body accepts help text whenever **any one** substring from `init|add|remove|list|sync|deinit` appears—many degraded help variants that drop most documented commands except a single survivor still satisfy the oracle ([weak-oracle signals](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/), canonical entry `references/docs/taxonomy/vacuous-assertion.md`).
- **Prescribed remediation:** Strengthen toward a structured check: snapshot a golden subset of headings/subcommands (`assert_equals`/`assertTrue` combos, or deterministic line patterns) asserting each primary command documented in the CLI contract—not merely “mentions one keyword”.
- **Why this isn't a false positive:** The false-positive guard for vacuous negatives does not apply—the test explicitly claims affirmative coverage (“mentions **key commands** plural”) while asserting the smallest token presence.

## Tests considered but not flagged

- Duplicate identifiers such as `test_deinit_local_mode_only` in **`unit/test_deinit_modes.test.sh`** versus **`integration/test_cli_deinit.test.sh`** were clustered as potential `semantic-redundancy`, but targeted reading shows materially different seams (`cmd_*` helpers vs full `run_ai_rizz` CLI path, distinct filesystem layout). They protect different adapters, not duplicated knowledge—the overlap is analogous to guarded intentional dual-layer validation per [knowledge-DRY overrides](https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/).
- Numerous **TODO maintenance comments** in `unit/test_hook_based_local_mode.test.sh`/`unit/test_initialization.test.sh` pair with substantive assertions beneath them; audited as incomplete documentation debt but not empty stubs under `rotten-green` / `pseudo-tested`.
- **`tests/common.sh`** centralizes globals with `tearDown()` restoration of `HOME` and tempdirs; reviewed against `shared-state`—lifecycle isolation is deliberate shared harness design, not uncontrolled bleed between tests within a file lacking teardown.
- **Directory-heavy `cmd_init`/`cmd_deinit` helpers** remain under `tests/unit/` by repository convention despite touching git + FS; flagged only when tier semantics clearly contradict observable behavior—the suite consistently treats sourced shell helpers as the unit tier baseline, so **`wrong-level`** was not asserted without sharper mismatch evidence.

## Out-of-scope requests

None.

