# Suite Manifest Format

The structured output emitted by the scout agent and consumed by the orchestrator. The manifest describes the shape and size of a test suite without reading any file's contents.

## Purpose

The suite manifest provides the orchestrator with the measurements needed to make partitioning decisions: how many files, how large each is, how many tests each contains, and what tier conventions (directory structure) the suite uses. The scout gathers this data using filesystem operations and lightweight pattern matching — it never reads file contents deeply.

## Manifest Shape

````markdown
## Suite Manifest

**Suite root:** `tests/`
**Ecosystem:** Python (pytest)
**Total files:** 47
**Total tests:** 823
**Total lines:** 18,204
**Total chars:** 612,480

### Tier Conventions

| Convention | Evidence |
|------------|----------|
| `unit/` directory → unit tier | 31 files in `tests/unit/` |
| `integration/` directory → integration tier | 12 files in `tests/integration/` |
| `e2e/` directory → e2e tier | 4 files in `tests/e2e/` |

### Per-File Inventory

| File | Lines | Chars | Tests | Inferred Tier |
|------|-------|-------|-------|---------------|
| tests/unit/test_auth.py | 245 | 8,120 | 12 | unit |
| tests/unit/test_parser.py | 892 | 31,450 | 48 | unit |
| tests/integration/test_api.py | 340 | 11,200 | 8 | integration |
| ... | ... | ... | ... | ... |
````

## Field Contracts

### Top-Level Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **Suite root** | Relative path | Yes | The directory passed to the scout, relative to the workspace root. |
| **Ecosystem** | String | Yes | Detected test ecosystem: `Python (pytest)`, `Python (unittest)`, `JavaScript (jest)`, `TypeScript (vitest)`, `Go (testing)`, `Ruby (rspec)`, `Ruby (minitest)`, `JVM (JUnit)`, `JVM (TestNG)`, `Rust (cargo test)`, `Mixed`, `Unknown`. |
| **Total files** | Positive integer | Yes | Count of test files discovered. |
| **Total tests** | Positive integer | Yes | Sum of test function/method/block counts across all files. Approximate — the scout uses pattern matching (e.g., `def test_`, `it(`, `func Test`), not AST parsing. |
| **Total lines** | Positive integer | Yes | Sum of line counts across all test files. |
| **Total chars** | Positive integer | Yes | Sum of character counts (bytes for ASCII-dominant source) across all test files. This is the primary input to the orchestrator's partitioning heuristic. |

### Tier Conventions Table

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **Convention** | Prose | Yes | The rule the scout inferred (e.g., "`unit/` directory → unit tier"). |
| **Evidence** | Prose | Yes | What the scout observed to support the convention (e.g., "31 files in `tests/unit/`"). |

The tier conventions table may be empty if the suite uses no discoverable directory-based tier structure. In that case, the scout emits: "No directory-based tier conventions detected. Tier inference will rely on import patterns and framework markers during batch assessment."

### Per-File Inventory Table

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **File** | Relative path | Yes | Path to the test file, relative to the suite root. |
| **Lines** | Positive integer | Yes | Line count (`wc -l` equivalent). |
| **Chars** | Positive integer | Yes | Character/byte count (`wc -c` equivalent). |
| **Tests** | Positive integer | Yes | Approximate test count from pattern matching. |
| **Inferred Tier** | Enum string | Yes | Tier inferred from directory-based conventions. Values: `unit`, `integration`, `e2e`, `smoke`, `contract`, `unknown`. |

## Ordering

Per-file inventory rows are ordered by file path (lexicographic). This ensures deterministic output.

## Consumption by Orchestrator

The orchestrator uses the manifest to:

1. **Decide sharding** — compare Total chars against the content budget (derived from the context window size). If the suite fits in one batch, launch a single batch assessor with all files.
2. **Partition** — if sharding is needed, use greedy bin-packing by Chars, keeping files from the same directory together when possible (directory cohesion aids per-file smell detection).
3. **Compute summary richness** — derive the richness tier for behavior summaries from Total tests vs. the cross-suite assessor's context budget (see `behavior-summary-format.md`).
4. **Pass tier conventions** — forward the tier conventions table to batch assessors so they can populate the Tier field in behavior summaries, and to the cross-suite assessor for `wrong-level` detection.
