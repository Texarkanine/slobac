---
name: slobac-batch
description: Assess a batch of test files for per-test and per-file SLOBAC smells, emit findings and behavior summaries. Use when slobac-audit dispatches a batch assessor during orchestrated audit.
---

# Batch Assessor Workflow

This skill is a subagent of the [`slobac-audit`](../slobac-audit/SKILL.md) orchestrator. It receives a list of test files, a set of in-scope smell slugs (per-test and per-file only), a summary richness level, and tier conventions. It reads each file fully, evaluates smells, and emits findings plus behavior summaries.

The batch assessor is the universal audit engine for per-test and per-file smells. For small suites, the orchestrator launches one batch assessor with all files. For large suites, it launches N batch assessors in parallel, each with a partition of files.

## Inputs

The orchestrator provides these in the launch prompt:

- **File list** — paths to the test files this batch is responsible for.
- **In-scope smell slugs** — which per-test and per-file smells to evaluate (drawn from the taxonomy's `per-test` and `per-file` detection scopes).
- **Summary richness level** — `full`, `standard`, or `compact` (controls how much detail goes into the Behavior field of behavior summaries).
- **Tier conventions** — the directory-based tier conventions detected by the scout (e.g., "`unit/` directory → unit tier").
- **Behavior summary format** — the spec to follow (loaded from `../slobac-audit/references/behavior-summary-format.md`).

## Step 1 — load canonical smell definitions

For each slug in the in-scope smell list, read **`../slobac-audit/references/docs/taxonomy/<slug>.md`** (relative to this `SKILL.md`). This is the single source of truth for what the smell is, how to detect it, what the common over-triggers are, and how to fix it. Do not paraphrase, do not substitute.

## Step 2 — load the behavior summary format spec

Read **`../slobac-audit/references/behavior-summary-format.md`** (relative to this `SKILL.md`). This defines the exact shape of the behavior summary table you must produce alongside your findings.

## Step 3 — assess each file

For each file in the assigned file list:

### 3a. Read the file fully

Read the entire file contents. You need the full file to evaluate both per-test and per-file smells.

### 3b. Evaluate per-test smells

For each test function, class, or method in the file:

1. Read the test identifier, any grouping context (class or `describe` equivalent), the docstring if present, and the body's assertions.
2. For each in-scope per-test smell, evaluate whether the test matches the smell's Signals from the canonical entry, refined by the False-positive guards in the same entry.
3. When a candidate match surfaces, formulate the five finding fields:
   - **Location:** file path and test identifier.
   - **Smell:** the slug.
   - **Rationale:** what the test claims vs. what the body verifies, citing the specific Signal that matched. Include a link to the published manifesto URL (`https://texarkanine.github.io/slobac/taxonomy/<slug>/`).
   - **Prescribed remediation:** concrete action per the canonical entry's Prescribed Fix section.
   - **Why this isn't a false positive:** one sentence naming the over-trigger this could be confused for, and why this case isn't it.
4. If any of the five fields cannot be articulated cleanly, the finding is weak — reconsider before emitting.

If a single test exhibits more than one in-scope smell, emit one finding per smell, each with its own remediation.

### 3c. Evaluate per-file smells

For each in-scope per-file smell, evaluate the file as a whole:

- **`shared-state`** — trace mutable bindings at module/class scope. Are there module-level mutable objects (instances, lists, dicts) written by one test and read by another? Are there `before(:suite)` / class-level fixtures that install state without per-test restoration?
- **`monolithic-test-file`** — count behavior domains. Does the file mix 5+ distinct subjects with section-header comments, imports from 5+ unrelated modules, and >50 tests?

Per-file findings follow the same five-field structure as per-test findings, but **Location** references the entire file (or the specific module-level binding for `shared-state`).

### 3d. Build behavior summary row

For each test in the file, emit a behavior summary row per the format spec loaded in Step 2. The richness level (from the orchestrator's input) controls how much detail goes into the **Behavior** field:

- **Full** (~400–600 chars): Behavior sentence + SUT entry points called + assertion targets + fixture shape summary.
- **Standard** (~200–350 chars): Behavior sentence + SUT entry points called + assertion targets.
- **Compact** (~80–120 chars): Behavior sentence only.

The **Tier** field is inferred from the file's directory path using the tier conventions provided by the orchestrator. If no convention applies, use `unknown`.

The **Smells Found** field lists slugs of per-test smells detected for this test (from Step 3b), or `—` if none.

## Step 4 — emit results

Your final message back to the orchestrator contains two sections:

### Findings

All findings from Steps 3b and 3c, in the five-field format. Group by file, ordered by file path then line number.

If no findings were produced for any in-scope smell, include: "No findings for scope `<slug>`."

### Behavior Summaries

The complete behavior summary table for all tests in the batch, in the format defined by the behavior summary format spec. Rows are ordered by file path (lexicographic), then by line number (ascending) within each file.

## Constraints

- **Read-only.** This skill does not modify test code.
- **Per-test and per-file smells only.** Cross-suite smells (`semantic-redundancy`, `wrong-level`, etc.) are handled by the cross-suite assessor, not this skill. If you see cross-suite signals while reading, note them in the Smells Found column of behavior summaries (append `?` for suspected cross-suite smells) but do not emit findings for them.
- **Canonical entries are the single source of truth.** Detection logic comes from the canonical taxonomy entries, not from paraphrased or memorized definitions.
- **Finding quality over quantity.** A weak finding is worse than a missed finding. If any of the five fields cannot be articulated cleanly, reconsider before emitting.
