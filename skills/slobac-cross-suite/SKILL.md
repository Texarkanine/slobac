---
name: slobac-cross-suite
description: Detect cross-suite SLOBAC smells by clustering behavior summaries and performing targeted source reads. Use when slobac-audit dispatches a cross-suite assessor during orchestrated audit.
---

# Cross-Suite Assessor Workflow

This skill is a subagent of the [`slobac-audit`](../slobac-audit/SKILL.md) orchestrator. It receives the merged behavior summaries from all batch assessors, a set of in-scope cross-suite smell slugs, and tier conventions. It clusters summaries, performs targeted source reads, and emits cross-suite findings.

The cross-suite assessor operates on the compressed intermediate representation (behavior summaries) rather than re-reading the full suite. It only reads source code for candidate groups that clustering identifies — a targeted subset, not the full suite.

## Inputs

The orchestrator provides these in the launch prompt:

- **Behavior summaries** — the merged behavior summary table from all batch assessors (per the format in `../slobac-audit/references/behavior-summary-format.md`).
- **In-scope cross-suite smell slugs** — which cross-suite smells to evaluate (drawn from the taxonomy's `cross-suite` detection scope).
- **Tier conventions** — the directory-based tier conventions detected by the scout.
- **Suite root** — the target directory path (for context in findings).

## Step 1 — load canonical smell definitions

For each slug in the in-scope cross-suite smell list, read **`../slobac-audit/references/docs/taxonomy/<slug>.md`** (relative to this `SKILL.md`). This is the single source of truth for what the smell is, how to detect it, and what the common over-triggers are.

## Step 2 — cluster behavior summaries

For each in-scope cross-suite smell, analyze the behavior summary table to identify candidate groups:

### For `semantic-redundancy`

1. Read the **Behavior** field of every summary row.
2. Cluster rows whose behavior descriptions describe the same observable outcome, even if phrased differently or using different fixture shapes. This is LLM judgment over behavior sentences — look for semantic equivalence, not string similarity.
3. A candidate group is ≥2 rows from **different files** whose behaviors describe the same observable. Rows within the same file are not cross-suite redundancy (they may be per-file or per-test smells, already handled by batch assessors).
4. Filter out rows already flagged with smells in the **Smells Found** column unless co-occurrence is relevant.

### For `wrong-level`

1. Read the **Tier** field of every summary row (populated by batch assessors from directory conventions).
2. Compare each row's Tier against signals in the Behavior field:
   - A `unit`-tier test whose behavior mentions subprocess spawn, real HTTP/DB, file I/O, or external service interaction → candidate for wrong-level (too high for unit).
   - An `integration`- or `e2e`-tier test whose behavior describes pure-function computation with no external dependencies → candidate for wrong-level (too low for integration).
3. Rows with `unknown` tier are not candidates (no convention to violate).

### For `deliverable-fossils` (Phase B — regrouping)

1. Read the **Behavior** field to identify tests whose behaviors cluster into product capabilities.
2. Compare the current file grouping against the behavior clusters. If tests that belong to the same product capability are scattered across unrelated files, they are candidates for regrouping.
3. This is a Phase B detection that builds on Phase A (rename, handled by batch assessors). Only flag if regrouping would meaningfully improve suite navigation.

## Step 3 — targeted source reads

For each candidate group identified in Step 2:

1. Use the **File** and **Line** fields from the behavior summaries as pointers.
2. Read only the source of the candidate tests — not the full files, not the full suite. Read enough context around each test (the test function plus its immediate setup/teardown and imports) to confirm or reject the finding.
3. For `semantic-redundancy`: verify that the tests truly exercise the same observable behavior, not just similar-looking code. Check whether the overlap is intentional (contract guard, different knowledge protected) or accidental.
4. For `wrong-level`: verify that the actual test code matches what the behavior summary described. Check imports and function calls to confirm the tier mismatch.

## Step 4 — confirm or reject findings

For each candidate:

- **Confirmed** — the targeted source read validates the smell. Emit a finding.
- **Rejected** — the source read reveals the candidate is a false positive (e.g., similar behavior descriptions but different knowledge being protected, or a "heavy" import that's actually used as a mock). Do not emit.

For confirmed findings, formulate the five finding fields:

- **Location:** file path(s) and test identifier(s) involved in the cross-suite finding.
- **Smell:** the slug.
- **Rationale:** what the cross-suite analysis found, citing the specific Signal from the canonical taxonomy entry. For `semantic-redundancy`, name the behavioral overlap. For `wrong-level`, name the tier mismatch and the evidence. Include a link to the published manifesto URL (`https://texarkanine.github.io/slobac/taxonomy/<slug>/`).
- **Prescribed remediation:** concrete action per the canonical entry's Prescribed Fix. For `semantic-redundancy`, name the canonical location and explain why it's canonical. For `wrong-level`, name the target tier and why.
- **Why this isn't a false positive:** one sentence naming the over-trigger and why this case isn't it.

## Step 5 — emit results

Your final message back to the orchestrator contains:

### Cross-Suite Findings

All confirmed findings from Step 4, in the five-field format. Group by smell slug, then by file path.

If no findings were produced for any in-scope smell, include: "No cross-suite findings for scope `<slug>`."

## Constraints

- **Read-only.** This skill does not modify test code.
- **Cross-suite smells only.** Per-test and per-file smells are handled by batch assessors. Do not emit findings for per-test or per-file smells even if you notice them during targeted reads.
- **Summaries enable candidate detection, not full findings.** Always perform targeted source reads before confirming a finding. Do not emit findings based solely on behavior summary clustering — the summaries are an index for candidate identification, not evidence sufficient for a finding.
- **Canonical entries are the single source of truth.** Detection logic comes from the canonical taxonomy entries, not from paraphrased or memorized definitions.
- **Finding quality over quantity.** Cross-suite findings are high-stakes (they often recommend deleting or relocating tests). Every finding must be defensible. If the targeted read leaves doubt, reject the candidate.
