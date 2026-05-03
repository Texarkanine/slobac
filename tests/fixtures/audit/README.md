# Audit fixtures

Test suites planted with known smells. Each subdirectory is **input** to the SLOBAC audit skill — not a test of SLOBAC itself. These files are never executed by any CI SLOBAC owns; their job is to sit still and wait to be audited.

## Convention

Every scenario lives in its own directory under `tests/fixtures/audit/<scenario>/` and contains:

- **One or more `.py` files** embodying the scenario. These are written as pytest-shaped tests so the audit sees realistic shape (fixtures, parametrize, class-based tests, docstrings) — but they are never collected by a runner in this repo. Assertions inside the fixture bodies are illustrative, not load-bearing.
- **`expected-findings.md`** — the ground truth for that scenario. Enumerates every finding the audit should emit (test location, smell slug, expected remediation path, rationale) and flags every negative-example test the audit must *not* flag. Shape mirrors the audit's own report template so a per-scenario comparison is a side-by-side read.

Scenarios in Phase 1:

- `deliverable-fossils/` — tests carrying sprint-history vocabulary; correct fix is rename (and sometimes regroup).
- `naming-lies/` — tests whose titles don't match their assertions; correct fix is one of rename / strengthen / investigate.
- `both-smells/` — mixed suite including at least one test exhibiting both smells; exercises scope honoring.
- `clean/` — behavior-encoded names, body-matching claims; audit should emit no findings.

Scenarios added for orchestration (Phase 2):

- `shared-state/` — module-level mutables shared across tests without per-test reset; exercises per-file detection scope. Includes negative examples using `@pytest.fixture` for isolation and read-only constant access.
- `monolithic-test-file/` — multi-file scenario: one monolith (`test_everything.py`, 54 tests across 6 behavior domains with section headers and mixed imports) and one cohesive large file (`test_parser_thorough.py`, 42 tests all exercising a single parser). Exercises per-file detection scope.
- `semantic-redundancy/` — multi-file scenario exercising cross-suite detection scope. Two files (`test_auth_tokens.py`, `test_session_auth.py`) test the same expired-token rejection behavior at different indirection levels. A third file (`test_contract_keys.py`) contains structurally similar key-checking assertions that guard different contracts (negative example — intentional duplication).
- `wrong-level/` — multi-file, multi-directory scenario exercising cross-suite detection scope. Directory structure encodes tier conventions (`unit/`, `integration/`). Contains both directions of wrong-level: `unit/test_api_client.py` spawns subprocesses and makes real HTTP requests (too low — should be integration), `integration/test_pure_helpers.py` tests pure functions with no external deps (too high — should be unit). `unit/test_calculator.py` is a negative example — correctly placed despite heavy-sounding imports.

## Validation mode

Phase 1 validation is **manual**. The operator invokes the audit skill against a fixture path in Cursor or Claude Code, reads the emitted `slobac-audit.md`, and compares it to `expected-findings.md` for that scenario. A scripted eval harness (golden-file or structured-pattern matching) is deliberately deferred to Phase 2 — Phase 1 is proving the shape works, not proving the detection is byte-stable.

## Polyglot note

Fixtures are Python-only. The canonical smell entries in `skills/slobac-audit/references/docs/taxonomy/<slug>.md` may describe polyglot detection surface, but the fixtures here are not the place to exercise it. Add ecosystem-specific fixtures when the audit's polyglot claims are being tested in anger — not before.

## Negative examples

Every scenario except `clean/` contains at least one **negative-example** test: a test whose shape would trip a naive detector (e.g. a test named `test_refactor_preserves_behavior` that actually tests refactoring behavior). The audit must not flag these. If it does, the fix goes in the canonical smell entry under `skills/slobac-audit/references/docs/taxonomy/`, not in the fixture.
