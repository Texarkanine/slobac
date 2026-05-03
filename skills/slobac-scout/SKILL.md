---
name: slobac-scout
description: Enumerate and measure a test suite's files, emit a Suite Manifest for the audit orchestrator. Use when slobac-audit dispatches a scout to map the suite before partitioning.
---

# Test Suite Scout Workflow

This skill is a subagent of the [`slobac-audit`](../slobac-audit/SKILL.md) orchestrator. It receives a target directory, enumerates all test files, measures their size, and emits a Suite Manifest that the orchestrator uses for partitioning decisions. The scout does not read file contents deeply — it uses filesystem operations and lightweight pattern matching only.

## Inputs

The orchestrator provides these in the launch prompt:

- **Target directory** — the suite root to scan.
- **Suite manifest format** — the spec to follow (loaded from `../slobac-audit/references/suite-manifest-format.md`).

## Step 1 — load the manifest format spec

Read **`../slobac-audit/references/suite-manifest-format.md`** (relative to this `SKILL.md`). This defines the exact shape of the output you must produce. Do not deviate from the field contracts or table structure defined there.

## Step 2 — load exploration command templates

Read **`references/exploration-commands.md`** (relative to this `SKILL.md`). This contains ready-made shell command templates for efficient test-suite exploration across ecosystems. Adapt the commands to the target suite's ecosystem rather than reinventing the wheel.

## Step 3 — detect ecosystem

Examine the target directory for file extensions and framework markers:

| Signal | Ecosystem |
|--------|-----------|
| `.py` files + `conftest.py` or `pytest` imports | Python (pytest) |
| `.py` files + `unittest` imports, no pytest | Python (unittest) |
| `.test.ts` / `.spec.ts` files + `jest.config.*` | TypeScript (jest) |
| `.test.ts` / `.spec.ts` files + `vitest.config.*` | TypeScript (vitest) |
| `.test.js` / `.spec.js` files + `jest.config.*` | JavaScript (jest) |
| `_test.go` files | Go (testing) |
| `_spec.rb` files + `spec_helper.rb` | Ruby (rspec) |
| `_test.rb` files or `test_*.rb` files | Ruby (minitest) |
| `*Test.java` / `*Test.kt` files | JVM (JUnit) |
| `_test.rs` files or `tests/` directory with `.rs` | Rust (cargo test) |
| Mixed signals | Mixed |
| No recognizable pattern | Unknown |

Use file extension discovery first (fastest), then check for framework config files if ambiguous.

## Step 4 — enumerate test files

Using the ecosystem-appropriate patterns from the exploration commands reference, enumerate all test files under the target directory. Exclude common non-test directories: `node_modules/`, `__pycache__/`, `.git/`, `vendor/`, `target/`, `build/`, `dist/`.

## Step 5 — measure each file

For each test file discovered:

1. **Line count** — `wc -l` equivalent.
2. **Character count** — `wc -c` equivalent (byte count for ASCII-dominant source).
3. **Test count** — approximate count using ecosystem-appropriate patterns:
   - Python: `def test_` or `async def test_` at any indentation, plus methods in classes that inherit from `unittest.TestCase`
   - JS/TS: `it(`, `test(`, `it.each(`, `test.each(`
   - Go: `func Test`
   - Ruby (rspec): `it `, `specify `
   - Ruby (minitest): `def test_`
   - JVM: `@Test` annotations
   - Rust: `#[test]` attributes

These counts are approximate (pattern-based, not AST-parsed). The scout's job is measurement, not precision parsing.

## Step 6 — detect tier conventions

Scan the directory structure for common tier conventions:

- `unit/` → unit tier
- `integration/` → integration tier
- `e2e/` or `end-to-end/` → e2e tier
- `smoke/` → smoke tier
- `contract/` → contract tier
- `functional/` → integration tier (common alias)

Record each convention with its evidence (how many files live under that directory). If no directory-based conventions are detected, note that explicitly.

## Step 7 — compute totals and emit manifest

Sum the per-file measurements into totals. Emit the Suite Manifest in the exact shape defined by the manifest format spec (loaded in Step 1).

The output is your final message back to the orchestrator. It should contain only the Suite Manifest — no commentary, no recommendations, no analysis. The orchestrator makes all partitioning decisions.
