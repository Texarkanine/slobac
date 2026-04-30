# SLOBAC scout skill

A subagent skill dispatched by [`slobac-audit`](../slobac-audit/README.md) to enumerate and measure a test suite before the orchestrator partitions it for batch assessment. The scout is fast, read-only, and never reads file contents deeply — it maps the suite's shape using filesystem operations and lightweight pattern matching.

## Relationship to slobac-audit

The scout is the first step in the audit orchestration pipeline. The orchestrator (`slobac-audit/SKILL.md`) launches the scout as a readonly subagent, receives the Suite Manifest, and uses it to decide how many batch assessors to launch and how to partition files between them.

```
slobac-audit (orchestrator)
  └── slobac-scout → Suite Manifest
      └── slobac-audit uses manifest for partitioning
```

## Cross-skill references

The scout reads:
- `../slobac-audit/references/suite-manifest-format.md` — the output format spec

The scout does NOT read taxonomy entries, the report template, or any other audit-specific content. Its job is measurement, not assessment.

## Invocation

This skill is not invoked directly by operators. It is launched as a subagent by the `slobac-audit` orchestrator. If an operator asks to "scout a suite" or "enumerate tests," direct them to invoke `slobac-audit` instead — the orchestrator handles scout dispatch.
