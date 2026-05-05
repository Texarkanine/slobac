---
task_id: slobac-plugin-distribution
date: 2026-05-05
complexity_level: 3
---

# Reflection: Expose SLOBAC as Cursor + Claude Code Plugin

## Summary

Added plugin manifests and marketplace catalogs to distribute SLOBAC as a single-skill plugin for Cursor and Claude Code. A mid-task architecture revision folded three subagent skills into `audit/references/subagents/` as raw workflow documents after discovering Cursor's actual skill naming behavior contradicted planning assumptions.

## Requirements vs Outcome

All requirements delivered: plugin manifests in both repos, marketplace catalogs in `txrk9-agent-plugins`, single discoverable skill per harness (`/slobac-audit` in Cursor, `/slobac:audit` in Claude Code), and documentation updated end-to-end. No requirements dropped. One requirement was *added* mid-task: the single-skill architecture, which was not in the original brief but emerged from the QA-discovered Cursor naming issue and operator UX observations (subagent skills polluting the command picker).

## Plan Accuracy

The original plan's core assumption — that Cursor uses the SKILL.md `name` field verbatim as the invocation command, including colons — was wrong. Cursor normalizes colons to hyphens and does *not* auto-prefix with the plugin name. This was the single most impactful planning error, invalidating the entire multi-skill `slobac:*` naming strategy and triggering a full architecture revision.

The preflight phase was the plan's strongest asset. Across three runs (two on the original plan, one on the revision), preflight caught 7 concrete gaps: missing `properdocs.yml` update, missing root `REUSE.toml` update, missing `CONTRIBUTING.md` and `README.md` updates, TDD gate sequencing errors (twice — once for the original plan, once for the revision), and the `properdocs.yml` gate unreachability caused by step ordering. Every one of these would have caused a build failure or left stale references in published documentation.

The revision plan was accurate — no build-phase surprises. The only QA finding on the revision was `txrk9-agent-plugins/README.md`, whose stale multi-skill description traced directly to the revision plan's "No change needed" assessment of that repo. The plan should have re-evaluated all prior-build outputs when the architecture changed.

## Creative Phase Review

No formal creative phase was executed. The architecture revision was designed during the plan phase based on empirical evidence from the first build's QA failure. The decision to fold subagent skills into reference documents was sound — it eliminated all naming collisions, command-picker clutter, and cross-harness registration complexity in one structural move.

## Build & QA Observations

**Build 1:** Clean execution against a heavily-preflighted plan. TDD gates (baseline GREEN → deliberate RED → fix → GREEN) worked as designed and caught nothing unexpected — which is the right outcome after thorough preflight.

**QA 1 (FAIL):** The semantic review passed, but the operator smoke test — the only empirical verification of Cursor's actual naming behavior — failed. This is the single most important observation of the task: no amount of documentation research or plan review could have caught this. The Cursor plugin system's naming resolution is not well-documented, and the plan's assumption came from inference, not verification.

**Build 2 (revision):** Clean execution. The single-skill architecture was simpler to implement than the original four-skill layout — fewer files to manage, fewer cross-references, fewer places for names to go wrong.

**QA 2 (PASS):** One trivial fix (stale multi-skill description in `txrk9-agent-plugins/README.md`) and one accepted deviation (`exploration-commands.md` placed at `references/` level instead of `subagents/` — architecturally more consistent, all path references correct).

## Cross-Phase Analysis

The causal chain is clear: **planning research gap → QA failure → architecture revision → clean rebuild**. The plan assumed Cursor naming behavior from documentation inference rather than empirical testing. Preflight couldn't catch this because preflight validates plan *completeness* and *consistency*, not external platform behavior. The only gate that could catch it was the operator smoke test — and it did.

Preflight's consistent value across three runs suggests it is well-calibrated for L3 tasks. Its TDD-encoding checks were particularly effective — the anti-pattern of deferring all verification to the end was caught and corrected twice.

The revision plan's explicit "No change needed" list was a useful structure but created a blind spot: when the architecture changed fundamentally, the list wasn't re-evaluated. The `txrk9-agent-plugins/README.md` stale content was the result.

## Insights

### Technical

- **Cursor plugin naming is opaque.** Cursor normalizes SKILL.md `name` field colons to hyphens and does not auto-prefix with the plugin name. This is not well-documented and can only be verified empirically. Any future work involving Cursor skill naming should include an operator smoke test as a blocking gate, not an optional verification.
- **Single-skill-with-subagent-workflows is a robust distribution pattern.** Raw workflow documents dispatched by the orchestrator avoid all harness-specific skill registration complexity. The orchestrator owns the dispatch contract; subagents don't need to be registered, discovered, or named. This pattern should be the default for multi-agent skills in both Cursor and Claude Code.

### Process

- **Preflight is high-ROI for rename/restructure tasks.** Three runs caught 7 gaps that would have caused build failures or stale documentation. For tasks involving many cross-references and CI gates, preflight pays for itself.
- **"No change needed" lists need re-evaluation after architecture changes.** When a revision fundamentally changes the structure, every prior-build output should be re-audited — not just the files the revision plan explicitly touches. The `txrk9-agent-plugins/README.md` miss was trivial, but in a larger system the same blind spot could be costly.
- **Operator smoke tests are the only gate for platform integration behavior.** Documentation research and plan review cannot substitute for actually installing and invoking in the target harness. For distribution-focused tasks, build an operator smoke test into the plan as a blocking prerequisite for QA completion, not a nice-to-have.
