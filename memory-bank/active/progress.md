# Progress

## Summary

Onboard the 9 remaining per-test taxonomy smells (`vacuous-assertion`, `tautology-theatre`, `pseudo-tested`, `over-specified-mock`, `implementation-coupled`, `presentation-coupled`, `conditional-logic`, `mystery-guest`, `rotten-green`) into the `slobac-audit` framework so it reaches parity with the 15-smell manifesto. Mechanical extension of the architecture delivered in the 2026-05-03 audit-orchestration archive: SKILL supported-slug table, natural-phrase mappings, per-smell fixtures, and `properdocs build --strict` integrity.

**Complexity:** Level 2

## History

- 2026-05-03 — `/niko` re-entry from clean state. Intent clarified and approved. Complexity classified as Level 2.
- 2026-05-03 — COMPLEXITY-ANALYSIS phase complete. Transitioning to Plan phase.
- 2026-05-03 — PLAN phase complete. 17-step plan across 4 phases written to `tasks.md`. Transitioning to Preflight.
- 2026-05-03 — PREFLIGHT phase complete. PASS with 1 amendment (added `skills/slobac-audit/README.md` step → 18 total steps) and 2 advisories. Transitioning to Build.
- 2026-05-03 — BUILD phase complete. 18 steps executed; 9 fixtures created; SKILL.md / fixtures README / skill README / techContext.md all promoted to 15-smell parity. 1 plan deviation (collapsed Phase A.2/A.3 stubs into Phase C). 1 straggler caught and fixed during step 18 (SKILL.md frontmatter). `properdocs build --strict` PASS. Transitioning to QA.
- 2026-05-03 — QA phase complete. PASS. 1 substantive deficiency caught and fixed inline (rotten-green missing planted `# TODO`). All semantic criteria pass. Transitioning to Reflect.
- 2026-05-03 — REFLECT phase complete. Reflection document written. Persistent files reconciled (techContext.md already updated during build; systemPatterns.md / productContext.md not invalidated). Ready for `/niko-archive`.
- 2026-05-04 — REWORK initiated by operator. Post-reflect operator review surfaced two follow-up cleanups against the originally-shipped 15-smell parity:
    - **R1:** the 15-row supported-slugs table and 15-bullet natural-phrase map inlined in `slobac-audit/SKILL.md` are duplicate manifesto content that will drift as the taxonomy grows. Delegate enumeration to taxonomy file existence; move natural-phrase mappings into a uniform per-entry section. Mirror this in lead-paragraph phrasing of `slobac-audit/README.md` and `memory-bank/techContext.md` (drop hardcoded counts).
    - **R2:** harness-specific dispatch examples (`Task` for Cursor, `dispatch_agent` for Claude Code) at three SKILL.md sites name primitives that evolve outside SLOBAC's release cadence with no CI drift gate. Elide in favor of a single harness-neutral instruction at each site; no contributor rationale in SKILL.md.
    - **Not in scope:** Step 8 dedup rule (operator re-read and confirmed it's correctly scoped); no fixture or taxonomy-scope edits; no orchestrator changes.
- 2026-05-04 — REWORK COMPLEXITY-ANALYSIS phase complete. Level 2 retained (mechanical rollout + bounded SKILL.md surgeries; same shape as original task). Transitioning to Plan.
- 2026-05-04 — REWORK PLAN phase complete. 10-step plan across 4 phases (Phase A taxonomy rollout × 3 steps, Phase B SKILL.md surgery × 2 steps batched, Phase C mirror cleanup × 2 steps, Phase D verification × 3 steps) written to `tasks.md`. 15 behaviors enumerated for TDD coverage. Transitioning to Preflight.
- 2026-05-04 — REWORK PREFLIGHT phase: PASS with amendment. Surfaced one missed touchpoint in `slobac-audit/README.md:176` (Scope-and-non-goals bullet asserts manually-curated supported-slug table). Step 6 expanded to rewrite the bullet alongside the lead-paragraph soften; B11b added. Sibling skills (`slobac-scout`, `slobac-batch`, `slobac-cross-suite`) confirmed clean.
- 2026-05-04 — Plan amended pre-build by operator: contract shift. Operators must invoke `/slobac-audit` by **explicit slug** (no fuzzy phrase-to-slug resolution by orchestrator). Operator-phrase migration target is `## Aliases` (renamed from "Natural phrases"; cargo-culted name dropped) and the section's audience flips from orchestrator-runtime to **human-search discoverability** on the published docs site. SKILL.md Step 2 instructs the orchestrator to refuse non-slug requests with the supported-slug list, not to resolve them. A small wildcard whitelist (`all` / `everything` / unscoped) is preserved as bulk-select. tasks.md and projectbrief.md updated; behaviors B2b, B2c added, B4 inverted (SKILL.md must NOT reference Aliases). Transitioning to Build.
- 2026-05-04 — REWORK BUILD phase complete. Three commits across the four plan phases:
    - Phase A (`docs(taxonomy): add ## Aliases section to all 15 entries`) — taxonomy README shape SoT updated; 15 entries each gain a `## Aliases` section with the verbatim phrase content from prior SKILL.md, slug-name prefix dropped. Properdocs `--strict` green.
    - Phase B (`refactor(slobac-audit): slug-only invocation; elide harness-specific dispatch`) — SKILL.md Step 2 rewritten to enforce the slug-only invocation contract with structural-enumeration prose; the 15-row supported-smells table and 15-bullet operator-phrase map both deleted; the `all` / `everything` wildcard preserved as the only non-slug input. Steps 3, 5, 7 lose their harness-specific dispatch bullet blocks (Cursor `Task`, Claude Code `dispatch_agent`); each step's lead sentence already carries the harness-neutral instruction.
    - Phase C (`docs: drop hardcoded smell counts from lead-paragraph mirrors`) — `slobac-audit/README.md` lead paragraph and "Scope and non-goals" bullet rewritten to reflect structural enumeration and the slug-only contract; `memory-bank/techContext.md` lead summary updated similarly. The README's contributor-facing supported-smells table is preserved deliberately.
    - Phase D verification (final properdocs gate green; mechanical-gate audit B1/B3/B4/B5/B8/count-mirrors all clean; B6 spot-checked on `tautology-theatre` and `wrong-level`; B15 fixtures untouched per `git diff --stat` since rework-init).
    Transitioning to QA.
