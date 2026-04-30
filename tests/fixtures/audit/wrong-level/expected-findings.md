# Expected findings — `wrong-level` scenario

**Target suite root:** `tests/fixtures/audit/wrong-level/`
**In-scope smells:** `wrong-level`
**Expected finding count:** 2

Shape mirrors the audit report template. Each finding below must appear in the emitted `slobac-audit.md` with equivalent content; phrasing need not be byte-identical, but the test location, smell slug, remediation path, and rationale anchor must match.

## Findings

### 1. `unit/test_api_client.py` — "unit" directory but integration-level behavior

- **Location:** `unit/test_api_client.py` (entire file, but primarily `test_fetch_users_from_live_endpoint` line ~31 and `test_cli_invocation_returns_output` line ~42)
- **Smell:** `wrong-level`
- **Rationale:** The file lives under `unit/` but contains tests that spawn a subprocess (`subprocess.run`) and perform real HTTP requests (`urllib.request.urlopen`). These are integration-level behaviors: they depend on external processes, network availability, and system state. See [wrong-level](https://texarkanine.github.io/slobac/taxonomy/wrong-level/) signals — "a 'unit' test that spawns a subprocess or uses real network/database dependencies."
- **Prescribed remediation:** Relocate `test_fetch_users_from_live_endpoint` and `test_cli_invocation_returns_output` to `integration/test_api_client.py`. If the file's remaining tests (which do use mocks correctly) should stay in `unit/`, split the file. The directory tier convention (`unit/` = no external deps) must be honored for the test pyramid to be meaningful.
- **Why this isn't a false positive:** The tests perform real I/O (subprocess spawn, HTTP request) that cannot execute in isolation. These are not mocked or stubbed — the code literally calls `subprocess.run()` and `urllib.request.urlopen()`.

### 2. `integration/test_pure_helpers.py` — "integration" directory but pure-function unit tests

- **Location:** `integration/test_pure_helpers.py` (entire file)
- **Smell:** `wrong-level`
- **Rationale:** The file lives under `integration/` but every test is a pure-function unit test: `add`, `clamp`, `slugify`, `parse_bool`. No external dependencies, no I/O, no fixtures beyond the function arguments. See [wrong-level](https://texarkanine.github.io/slobac/taxonomy/wrong-level/) signals — "an 'integration' test that mocks every dependency" (in this case, there are no dependencies to mock because the functions are pure).
- **Prescribed remediation:** Relocate to `unit/test_pure_helpers.py`. These tests run in milliseconds and have zero external dependencies — they belong at the unit tier. Placing them in `integration/` inflates the integration suite's run time reporting and makes the pyramid shape misleading.
- **Why this isn't a false positive:** Every test calls a pure function with literal arguments and asserts the return value. No test constructs any fixture, mock, connection, or external resource.

## Tests that must NOT be flagged

### `unit/test_calculator.py` — pure unit test, correctly placed

- **Location:** `unit/test_calculator.py` (entire file)
- **Why not wrong-level:** The file is in `unit/` and contains only pure-function tests. The imports include `math` and `decimal` — modules that look "heavy" but are standard library with no I/O. Every test creates a `Calculator` instance, calls a method with literal arguments, and asserts the result. No mocks, no fixtures beyond the instance, no external state.
- **False-positive guard:** See the [wrong-level](https://texarkanine.github.io/slobac/taxonomy/wrong-level/) canonical entry's False-positive guards section — "heavy-sounding imports that are actually pure computation (e.g., `math`, `decimal`, `numpy` for array ops) are not signals of integration-level behavior."

## Notes

- This is a multi-file, multi-directory scenario exercising cross-suite detection scope. The assessor must understand the tier convention (`unit/` vs `integration/`) and compare each test's actual behavior against its tier placement.
- The scenario includes both directions of wrong-level: too-high (unit dir with integration behavior) and too-low (integration dir with unit behavior).
- `unit/test_calculator.py` is the negative example — correctly placed despite importing computation-heavy-sounding modules.
