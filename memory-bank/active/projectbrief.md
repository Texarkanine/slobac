# Project Brief — Phase 1 Audit MVP (two smells)

## User Story

Ship Phase 1 of [`planning/VISION.md`](../../planning/VISION.md) — the audit MVP — as agent customizations that run in both **Cursor** and **Claude Code**. The audit produces a portable report (format TBD) recommending remediations for a chosen subset of the taxonomy; it never touches code.

**Scope: two smells, both built for real:**

1. [`deliverable-fossils`](../../docs/taxonomy/deliverable-fossils.md) — the Phase 1 smell specified in VISION §4. Highest reader-value, syntactic-enough detection signals, two-phase fix (rename → regroup).
2. [`naming-lies`](../../docs/taxonomy/naming-lies.md) — chosen as the second smell specifically because it is close-sibling-but-different-fix-shape to deliverable-fossils. It has a three-way fix branch (rename / strengthen / investigate) vs. the two-phase rename-then-regroup of deliverable-fossils. Any shared structure has to survive both decision shapes or it's the wrong abstraction.

## Requirements

### Functional

- A user in Cursor or Claude Code can invoke the audit and scope it to one, the other, or both smells.
- The audit emits a portable report naming each flagged test, the smell, the rationale, and the prescribed remediation. Portability means a different agent or a human can execute it without rereading the manifesto.
- The audit is read-only — it never modifies test code.

### Design questions (must be resolved; both have creative-phase weight)

1. **Docs ↔ Skill DRY.** The reader-facing taxonomy entry at `docs/taxonomy/<slug>.md` is the canonical prose describing each smell. The Skill may need exactly that prose, or a strict superset (detection heuristics, report templates, decision-tree guidance the manifesto deliberately does not contain). We must resolve whether the taxonomy entry suffices as input, and if not, how the Skill and the docs share a single source of truth. `pymdownx.snippets` (Skill owns the canonical text, docs include it) is one candidate mechanism; others are fair game.
2. **Customization granularity that survives Phase 2.** A monolithic customization with both smells inlined is not acceptable even if it would technically ship — it sets a pattern that will not extend to the full taxonomy. Candidate shape: an ur-skill with per-smell entries under a `references/` subdirectory. Other shapes are fair game. The two-smell scope exists specifically to stress-test whichever shape we pick.

### Portability preference (not a hard spec)

- Prefer customization primitives that are interoperable across Cursor and Claude Code.
- Explicitly avoid harness-specific primitives: e.g. Cursor `.mdc` frontmatter (`alwaysApply`, etc.), Claude Code `hooks.json`, any shape that a second harness cannot ingest.
- "AgentSkills.io-compatible Skill" is one plausible shape; Sub-Agents, Skill+Sub-Agent hybrids, and Plugins are all on the table. The final shape is a creative-phase outcome, not a predetermined target.
- We optimize for incremental shipping, not a day-1 plugin release.

### Creative-phase bar and escape hatch

The bar for creative-phase decisions is **airtight**. If an exploration does not resolve to an airtight answer:

- Do **not** fall back to "report the ambiguity and stop."
- Instead, produce a **research-brief seed document** suitable for handoff to a longer-running research agent, and stop-and-offer that handoff to the operator.
- The operator decides whether to dispatch the research or pivot.

## Out of Scope

- **Apply capability** (VISION Phase 3). This is audit-only.
- **Remaining taxonomy entries** (VISION Phase 2). Only deliverable-fossils and naming-lies.
- **Publishing to any plugin marketplace.** Publication is a later choice; Phase 1 ships as in-repo customizations runnable from a local clone.
- **Harness support beyond Cursor and Claude Code.** Portability is a preference; other harnesses are future work.

## VISION §5 Open Questions Touched by This Task

Phase 1 will likely answer the following as side effects of creative exploration:

- **§5 #1 — Audit output format.** Markdown? JSON? Both? Decides the audit → apply handoff shape.
- **§5 #3 — Subset-selection UX.** How the user says "audit against only these smells."
- **§5 #5 — Skill granularity.** Per-smell / per-fix-shape / per-audit-stage — see "customization granularity" design question above.
- **§5 #6 — Harness target order.** Pre-answered here as "Cursor and Claude Code jointly via portable primitive."

Open questions **not** forced by this task and deferred: #2 (report persistence), #4 (apply guardrail shape), #7 (license), #8 (audit-report artifact name).
