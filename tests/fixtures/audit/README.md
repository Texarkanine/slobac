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

## Validation mode

Phase 1 validation is **manual**. The operator invokes the audit skill against a fixture path in Cursor or Claude Code, reads the emitted `slobac-audit.md`, and compares it to `expected-findings.md` for that scenario. A scripted eval harness (golden-file or structured-pattern matching) is deliberately deferred to Phase 2 — Phase 1 is proving the shape works, not proving the detection is byte-stable.

## Polyglot note

Fixtures are Python-only. The per-smell augmentation files in `skills/slobac-audit/references/smells/<slug>.md` may describe polyglot detection surface, but the fixtures here are not the place to exercise it. Add ecosystem-specific fixtures when the audit's polyglot claims are being tested in anger — not before.

## Negative examples

Every scenario except `clean/` contains at least one **negative-example** test: a test whose shape would trip a naive detector (e.g. a test named `test_refactor_preserves_behavior` that actually tests refactoring behavior). The audit must not flag these. If it does, the fix goes in the per-smell augmentation file under `skills/slobac-audit/references/smells/`, not in the fixture.
