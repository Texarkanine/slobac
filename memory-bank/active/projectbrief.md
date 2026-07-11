# Project Brief

## User Story

As a SLOBAC manifesto / audit maintainer, I want named taxonomy smells that cover (a) tests asserting on committed documentation/agent prose and (b) weak string oracles on runtime-emitted text, so that a blind audit catches both the stockroom corpus cases and the common error/log/stdout message-match shape.

## Use-Case(s)

### Use-Case 1

An auditor runs `/slobac-audit` on a suite containing `assert "--detail raw" in skill_md.read_text()` or `docs/foo.md` keyword checklists. The report flags those tests under a dedicated smell (working name: `prose-pin`) with actionable fix guidance and false-positive guards for legitimate fitness-function greps.

### Use-Case 2

An auditor runs the same skill on a suite full of `expect(err.message).toContain("…")`, `pytest.raises(..., match=…)`, or `assert "timeout" in caplog.text` where the substring underdetermines meaning. Those are flagged (either by a second smell or by an explicitly extended/clarified existing entry) with a typed-error / structured-field remediation hierarchy.

### Use-Case 3

A taxonomy reader skimming related modes can tell `prose-pin` (committed docs) apart from runtime weak-text oracles, and both apart from existing `presentation-coupled` / `vacuous-assertion` / `conditional-logic`.

## Requirements

1. Add one or more new taxonomy entries under `skills/slobac-audit/references/docs/taxonomy/` that uniquely cover the committed-prose-pin mode and the weak runtime text-oracle mode (cardinality and naming settled in creative/plan).
2. Prefer **`prose-pin`** as the slug/name for the committed-documentation smell unless creative analysis finds a stronger coinage that still matches SLOBAC style.
3. Ground signals, examples, and FP guards in: stockroom physical examples; `memory-bank/active/change-detector-tests-markdown.md`; `memory-bank/active/runtime-text-tests-markdown.md`.
4. Match existing SLOBAC taxonomy entry shape and tone (`CONTRIBUTING.md` template; peer entries like `presentation-coupled`, `vacuous-assertion`).
5. Update related-mode cross-links on adjacent smells; regenerate taxonomy index (`scripts/gen_taxonomy_index.py`); keep `SKILL.md` / README index in sync.
6. Add or extend audit fixtures / `expected-findings` as required by project convention so the new smells are exercisable.
7. If style-matching or prior-art detail is blocked on missing information, research (subagent/web) or ask the operator (including Fable deep-research queries).

## Constraints

1. Do not collapse committed-doc pins and runtime emitted-text oracles into one undifferentiated smell without an explicit, documented design decision.
2. Do not weaken or contradict existing smells; clarify boundaries instead (especially `presentation-coupled`, `vacuous-assertion`, `conditional-logic`).
3. Preserve manifesto cross-link integrity; run properdocs/index regeneration gates as required by the project.
4. Forbidden-token / architectural fitness-function greps on agent-facing prose must have an explicit FP guard or legitimate-case carve-out — not blanket “delete.”
5. Remediate stockroom’s own tests is out of scope; taxonomy + SLOBAC audit surfaces only.

## Acceptance Criteria

1. New smell entry(ies) exist with full uniform sections (header table, summary, aliases, description, signals, FP guards, prescribed fix, example, related modes, polyglot notes).
2. A blind reading of the new entries would flag the stockroom prose-pin shapes we identified (with correct disposition for hygiene vs keyword/order/mention pins).
3. The common error/log/stdout weak-substring shape is in scope for detection under the chosen entry(ies).
4. Taxonomy index and orchestrator-consumed table are regenerated and drift-clean.
5. Adjacent smells’ Related modes (and any conditional-logic example guidance that currently normalizes message `match=`) are updated for consistency where needed.
6. Style matches peer entries; creative decisions (slug count, names, severity, detection scope) are recorded in memory-bank creative/plan artifacts.
