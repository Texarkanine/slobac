---
name: slobac-audit
description: Audit a test suite for SLOBAC manifesto smells and emit a portable markdown report. Phase 1 supports `deliverable-fossils` and `naming-lies`. Use when a human asks for a smell audit of test code, a review of test names/assertions against the behavior they claim to protect, or a SLOBAC report.
---

# Test Suite Audit Workflow

## Step 1 — determine the target suite root

The operator names a directory (explicitly or implicitly: "these tests", "my suite", a path in their message). If no target is identifiable, ask for one. Do not audit the whole repo by default; that is almost never what the operator wants and will produce an unreadably long report.

## Step 2 — parse scope

From the operator's request, resolve a list of **in-scope smell slugs** drawn from the Phase-1 supported set: `{deliverable-fossils, naming-lies}`.

- Natural phrases map to slugs by meaning, not string match. Map operator intent to slugs:
    - `deliverable-fossils` — "fossils", "deliverable fossils", "fossil tests", "stale names", "dead names", "sprint-shaped tests", "checklist tests", "checklist-shaped", "one test per AC", "tests named after tickets", "ticket-id vocabulary", "names that describe who wrote them, not what they prove", "sprint-vocab tests"
    - `naming-lies` — "naming-lies", "naming lies", "lying names", "lying titles", "titles that lie", "docstrings that lie", "names that don't match the body", "title/body mismatch", "tests whose names overpromise"
    - "audit everything", "all smells", unscoped — resolve to the full Phase-1 set.
- If the operator names a smell the Phase-1 skill does not support (e.g. `tautology-theatre`, `vacuous-assertion`, any other taxonomy slug), **refuse that slug**. Acknowledge it by name, state it is not in Phase-1 scope, list the supported slugs, and proceed with only the supported slugs from the operator's request. Do not audit the out-of-scope slug anyway; do not silently drop it.
- If the operator's intent is ambiguous between a supported and unsupported slug, ask rather than guess.

## Step 3 — load per-smell content, for each in-scope smell

For each slug in the resolved scope, read **`references/docs/taxonomy/<slug>.md`** (relative to this `SKILL.md`) — the canonical smell definition. Contains the Summary, Description, Signals, False-positive guards, Prescribed Fix, Example, Related modes, and Polyglot notes. This is the single source of truth for what the smell is, how to detect it, what the common over-triggers are, and how to fix it; do not paraphrase it, do not substitute other definitions.

If a smell's canonical entry turns out to need additional detection content (e.g. a new signal, a missing guard), stop and raise that as a manifesto gap — extend the canonical entry, do not carry detection content outside it.

## Step 4 — walk the target suite and emit candidate findings

For each test file under the target suite root:

1. For each test function, class, or method identified in the file: read the test identifier, any grouping context (class or `describe` equivalent), the docstring if present, and the body's assertions.
2. For each in-scope smell, evaluate whether the test matches the smell's Signals from the canonical entry, refined by the False-positive guards in the same entry. Matching is **semantic**, not keyword: a test mentioning "refactor" is not automatically a fossil; a test whose title nouns don't appear literally in the body is not automatically a naming-lie.
3. When a candidate match surfaces, formulate the five load-bearing pieces that every finding carries:
   - Location: file path and test identifier (function/method name).
   - Rationale: what the test claims vs. what the body verifies, citing the specific Signal that matched.
   - Prescribed remediation: concrete action per the manifesto's Prescribed Fix section, encoded in terms of the test's actual behavior.
   - False-positive guard: one sentence naming the over-trigger this finding could be confused for, and why this case isn't it.
   - Smell slug.
4. If any of the five cannot be articulated cleanly, the finding is weak — reconsider before emitting. A weak finding is worse than a missed finding; weak findings teach the operator to distrust the audit.

If a single test exhibits more than one in-scope smell, emit **one finding per smell**, each with its own remediation. Do not collapse — each smell prescribes a different fix, and the operator needs to see both.

## Step 5 — emit the report

Write the report using the shape in [`references/report-template.md`](./references/report-template.md).

- Default path: `./slobac-audit.md` in the operator's current working directory.
- If the operator named a different path in the invocation, use that path.
- If a file already exists at the chosen path, emit at `slobac-audit-2.md`, `slobac-audit-3.md`, … — do not clobber a prior report.
- Include a "Tests considered but not flagged" section for any test the audit inspected that looked smell-adjacent but cleared on close reading. This is how the audit shows its work; it is also how a reviewer can disagree without re-running.
- Include an explicit "No findings for scope `<slug>`" line when a requested in-scope smell produces zero findings. A zero-finding result is an outcome; silence is not.

## Step 6 — close

Tell the operator where the report was written and which scopes were covered. Do not summarize the findings in chat — the report is the deliverable. If out-of-scope slugs were requested, remind the operator which were skipped and why.

## Constraints and guards

- **Read-only.** This skill does not modify test code. If the operator asks the skill to apply fixes, that is a Phase-3 capability that does not exist yet — decline and direct them to treat the report as input to a separate, manual or future-automated apply step.
- **Canonical entries are the single source of truth.** The canonical smell definitions in this skill bundle are the manifesto. If a detection feels right but the canonical entry's Signals don't cover it, that is a signal the canonical entry needs extending — stop and surface it as a manifesto gap, do not carry detection content outside the canonical entry.
- **Preserve regression-detection power.** Every prescribed remediation in a finding is bounded by the [preservation-of-regression-detection-power](references/docs/principles.md#preservation-of-regression-detection-power) governor rule. A rename-only fix must not change the call graph; a strengthen fix must not shrink the mutation kill-set. If the audit cannot defend a remediation under this gate, reconsider the remediation.
- **Fossil vocabulary is a signal, not a verdict.** The word "refactor" in a title does not make a fossil; a ticket ID in a docstring does not make a fossil. The judgment is whether the vocabulary describes the test's reason-for-existence vs. the behavior it verifies. The canonical entry's False-positive guards section carries the specific over-triggers per smell.
- **Naming-lie detection is semantic.** Title/body tokenization is a first pass, not a verdict. `deletes` in a title matching `DELETE` in the body is a match; `cyan` in a title with no color handling in the body is not. Cross-language synonymy is the common over-trigger, and the canonical entry's False-positive guards section calls it out.
