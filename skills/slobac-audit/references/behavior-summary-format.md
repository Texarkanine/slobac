# Behavior Summary Format

The intermediate representation (IR) emitted by batch assessors and consumed by the cross-suite assessor. Each batch assessor produces one behavior summary table covering all tests in its assigned files.

## Purpose

Behavior summaries compress the "what does each test verify?" question into a structured table. This enables the cross-suite assessor to detect `semantic-redundancy`, `wrong-level`, and other cross-suite smells without re-reading the full source of every test — only performing targeted reads of candidates identified via summary clustering.

The format implements the manifesto's [describe-before-edit](docs/principles.md#behavior-articulation-before-change) principle as a first-class architectural boundary between file-reading agents and cross-suite agents.

## Table Shape

````markdown
## Behavior Summaries

| File | Line | Test ID | Behavior | Tier | Smells Found |
|------|------|---------|----------|------|--------------|
| tests/auth.test.ts | 12 | rejects_expired_token | Rejects request when JWT exp claim is in the past | unit | — |
| tests/auth.test.ts | 28 | test_after_auth_refactor | Returns user object from valid session cookie | unit | deliverable-fossils |
| tests/sync.test.ts | 45 | test_full_sync | Runs end-to-end sync and verifies DB state | integration | wrong-level? |
````

## Field Contracts

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **File** | Relative path | Yes | Path to the test file, relative to the suite root passed to the audit. |
| **Line** | Positive integer | Yes | Line number where the test function/method/block begins. |
| **Test ID** | String | Yes | The test's identifier as it appears in the source — function name, `it`/`test` string, method name. No transformation. |
| **Behavior** | Prose sentence | Yes | One sentence describing what the test actually verifies (not what its name claims). Written in present tense, active voice. Length varies by richness tier. |
| **Tier** | Enum string | Yes | The test's apparent pyramid tier as inferred from directory structure, framework markers, or import patterns. Values: `unit`, `integration`, `e2e`, `smoke`, `contract`, `unknown`. |
| **Smells Found** | Comma-separated slugs | Yes | Per-test and per-file smells detected in this test by the batch assessor. `—` if none. Append `?` to a slug if the assessor suspects but cannot confirm (e.g., `wrong-level?` when tier inference is ambiguous). |

## Richness Tiers

The orchestrator computes a richness level based on suite size vs. the cross-suite assessor's context budget, and passes it to each batch assessor. The richness tier controls how much detail goes into the **Behavior** field — not whether other fields are present (they are always present).

| Tier | When Used | Chars/Summary | Behavior Field Contents |
|------|-----------|---------------|------------------------|
| **Full** | Small-medium suites where budget allows | ~400–600 | Behavior sentence + SUT entry points called + assertion targets + fixture shape summary |
| **Standard** | Medium-large suites | ~200–350 | Behavior sentence + SUT entry points called + assertion targets |
| **Compact** | Large-huge suites | ~80–120 | Behavior sentence only |

The richness tier is advisory, not a hard character limit. Batch assessors should aim for the target range but prioritize accuracy over brevity — a 130-character compact summary that's precise is better than a 90-character one that's vague.

## Ordering

Rows are ordered by file path (lexicographic), then by line number (ascending) within each file. This ensures deterministic output regardless of the batch assessor's internal traversal order.

## Merge Semantics

When the orchestrator collects summaries from multiple batch assessors, it concatenates the tables and re-sorts by the ordering rule above. Duplicate rows (same File + Line) are not expected — the orchestrator's partitioning assigns each file to exactly one batch. If duplicates occur due to an error, the orchestrator keeps the first occurrence and logs a warning.

## Consumption by Cross-Suite Assessor

The cross-suite assessor receives the merged behavior summary table as its primary input. Its workflow:

1. **Cluster** — group rows by semantic similarity of the Behavior field (LLM judgment, not embedding API).
2. **Filter** — identify candidate groups where ≥2 rows from different files describe the same observable behavior.
3. **Targeted read** — for each candidate group, read the source of just those tests (using File + Line as pointers).
4. **Confirm or reject** — with source in hand, determine whether the overlap is real (`semantic-redundancy`) or intentional (contract guard, different knowledge protected).
5. **Tier analysis** — compare each row's Tier field against its actual behavior to detect `wrong-level`.
