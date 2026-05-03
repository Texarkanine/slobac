# SLOBAC cross-suite assessor skill

A subagent skill dispatched by [`slobac-audit`](../slobac-audit/README.md) to detect cross-suite SLOBAC smells by clustering behavior summaries from batch assessors and performing targeted source reads. Handles smells that cannot be detected from any single file in isolation — they require comparing tests across files or understanding suite-wide conventions.

## Relationship to slobac-audit

The cross-suite assessor is the final detection step in the audit orchestration pipeline. The orchestrator (`slobac-audit/SKILL.md`) launches it after all batch assessors have returned, passing it the merged behavior summaries and the list of cross-suite smell slugs. The cross-suite assessor clusters summaries, reads targeted source, and returns confirmed findings.

```
slobac-audit (orchestrator)
  ├── slobac-scout → Suite Manifest
  ├── slobac-batch (×N) → Findings + Behavior Summaries
  └── slobac-cross-suite → Cross-Suite Findings
      (receives merged behavior summaries from all batch assessors)
```

## Cross-skill references

The cross-suite assessor reads:
- `../slobac-audit/references/docs/taxonomy/<slug>.md` — canonical smell definitions for each in-scope cross-suite smell

The cross-suite assessor does NOT read the behavior summary format spec (the summaries are already formatted by batch assessors and passed as input), the report template (the orchestrator handles report assembly), or the suite manifest format (that's the scout's concern).

## Invocation

This skill is not invoked directly by operators. It is launched as a subagent by the `slobac-audit` orchestrator. If an operator asks about cross-suite smells, direct them to invoke `slobac-audit` instead — the orchestrator handles cross-suite dispatch and result merging.
