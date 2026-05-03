# Expected findings — `monolithic-test-file` scenario

**Target suite root:** `tests/fixtures/audit/monolithic-test-file/`
**In-scope smells:** `monolithic-test-file`
**Expected finding count:** 1

Shape mirrors the audit report template. Each finding below must appear in the emitted `slobac-audit.md` with equivalent content; phrasing need not be byte-identical, but the test location, smell slug, remediation path, and rationale anchor must match.

## Findings

### 1. `test_everything.py` — monolithic test file mixing 6 behavior domains

- **Location:** `test_everything.py` (entire file)
- **Smell:** `monolithic-test-file`
- **Rationale:** The file contains 54 tests across 6 distinct behavior domains (authentication, database operations, API routing, email notifications, file sync, billing), organized under comment section headers (`# === AUTH ===`, `# === DATABASE ===`, etc.) with imports from 6+ unrelated modules. See [monolithic-test-file](https://texarkanine.github.io/slobac/taxonomy/monolithic-test-file/) signals — ">50 tests, multiple top-level classes with different subjects, comment section headers, imports from 5+ unrelated modules."
- **Prescribed remediation:** Split by behavior domain into separate files: `test_auth.py`, `test_database.py`, `test_api_routing.py`, `test_email.py`, `test_file_sync.py`, `test_billing.py`. Each file gets the imports relevant to its domain only. Section-header comments become unnecessary when the file boundary carries the domain. Shared helpers (if any) move to a `conftest.py` or helpers module.
- **Why this isn't a false positive:** The file exhibits all structural signals: multiple domains, section headers as navigation crutches, mixed imports, and >50 tests. The comment headers themselves are evidence that the author felt the file needed internal navigation — a sign the file has outgrown a single file.

## Tests that must NOT be flagged

### `test_parser_thorough.py` — large but single-domain

- **Location:** `test_parser_thorough.py` (entire file)
- **Why not monolithic:** The file is large (40+ tests) but all tests exercise a single subject: a JSON-like parser. Every test class and function targets the same `Parser` type. There are no section-header comments because the file doesn't need internal navigation — it's all about one thing. Imports are focused on the parser module and standard library only.
- **False-positive guard:** See the [monolithic-test-file](https://texarkanine.github.io/slobac/taxonomy/monolithic-test-file/) canonical entry's False-positive guards section — size alone is not the signal; behavioral diversity is. A file with 100 tests that all exercise the same parser is thorough, not monolithic.

## Notes

- This is a multi-file scenario: one monolith (positive) and one cohesive large file (negative). The audit must evaluate per-file structure, not just per-test.
- The monolith's 54 tests use minimal stub bodies (`pass` or trivial assertions) — the structural signals (domains, headers, imports) are what matter, not the test logic.
- The cohesive file's 42 tests also use stub bodies but maintain single-domain focus throughout.
