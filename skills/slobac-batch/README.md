# SLOBAC batch assessor skill

A subagent skill dispatched by [`slobac-audit`](../slobac-audit/README.md) to deeply read a batch of test files and assess them for per-test and per-file SLOBAC smells. The batch assessor is the universal audit engine — for small suites, one assessor handles all files; for large suites, multiple assessors run in parallel on different file partitions.

## Relationship to slobac-audit

The batch assessor is the core detection engine in the audit orchestration pipeline. The orchestrator (`slobac-audit/SKILL.md`) launches one or more batch assessors after the scout has mapped the suite. Each batch assessor receives a partition of files, reads them deeply, and returns findings plus behavior summaries.

```
slobac-audit (orchestrator)
  ├── slobac-scout → Suite Manifest
  ├── slobac-batch (×1 for small suites) → Findings + Behavior Summaries
  └── slobac-batch (×N for large suites) → Findings + Behavior Summaries
```

## Cross-skill references

The batch assessor reads:
- `../slobac-audit/references/docs/taxonomy/<slug>.md` — canonical smell definitions for each in-scope smell
- `../slobac-audit/references/behavior-summary-format.md` — the output format spec for behavior summaries

The batch assessor does NOT read the report template (the orchestrator handles report assembly) or the suite manifest format (that's the scout's concern).

## Invocation

This skill is not invoked directly by operators. It is launched as a subagent by the `slobac-audit` orchestrator. If an operator asks to "batch assess" or "assess these files," direct them to invoke `slobac-audit` instead — the orchestrator handles batch dispatch, partitioning, and result merging.
