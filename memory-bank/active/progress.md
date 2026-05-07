# Progress: slobac-audit post-release v1 hardening

**Complexity:** Level 2

## Summary

Apply the v1-hardening cut (A1, A2, A3, B4, B5, C8) to the `slobac-audit` skill,
motivated by gaps observed in three post-release runs (default/auto, composer-2,
claude-opus-4-7) against `ai-rizz`'s `tests/` suite. Out of scope: B6 (regex canaries,
deferred pending creative exploration), C7 (extra orchestration provenance), and any
inline-fallback subagent workflow.

## Phase log

- 2026-05-07: COMPLEXITY-ANALYSIS — Level 2 determined.
- 2026-05-07: PLAN — Complete. 19 TDD steps; `pytest` introduced; generator script
  + sentinel-bracketed dual-target embed; CI drift-check; `techContext.md` exception
  documented.

## Follow-ups (not in this task)

- **B6 — regex / grep "canary" hints for cheap smell signals.** Polyglot enumeration is
  intractable and explicit pattern lists risk constraining the agent's reasoning
  (`assertTrue(true)` vs `assert true` vs Lisp shapes etc.). Deferred for creative-phase
  exploration of how to *suggest* hotspot detection without narrowing the agent's
  qualitative pass. Motivating evidence: 2/3 post-release runs missed the literal
  `assertTrue "..." true` in `tests/unit/test_list_display.test.sh:87`.
- **Subagent-less inline fallback (rejected for now).** If composer-class harnesses
  become a more common audit caller, revisit whether a documented degraded mode is
  better than the current "use a different harness" stance.
