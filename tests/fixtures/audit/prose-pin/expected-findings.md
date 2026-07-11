# Expected findings — `prose-pin` scenario

**Target suite root:** `tests/fixtures/audit/prose-pin/`
**In-scope smells:** `prose-pin`
**Expected finding count:** 2

The two findings exercise canonical signals from the [`prose-pin`](https://texarkanine.github.io/slobac/taxonomy/prose-pin/) entry: keyword checklists and feature-mention / order pins against the suite's own committed documentation and agent-skill prose. The audit is correct only when each finding's remediation names **delete** or **move to a docs-lint tier** (not "strengthen the substring"), and when both negative controls below stay unflagged.

## Findings

### 1. `test_onboarding_doc_mentions_required_phrases` — delete or docs-lint

- **Location:** `test_docs_oracle.py` → module level
- **Smell:** `prose-pin`
- **Rationale:** The test reads the suite's committed `docs/onboarding.md` and asserts a checklist of phrases (`"install the CLI"`, `"run the smoke check"`, `"report failures upstream"`) via `"phrase" in text`. Green means the wording is still present, not that the onboarding procedure still works. Any editorial rewrite that preserves meaning but changes phrasing fails CI with no product regression. Canonical signal: keyword checklist on committed docs / README / SKILL.md.
- **Prescribed remediation:** **Delete** the unit-suite assertion, or move the check into a dedicated docs-lint / Vale / markdownlint job that does not gate the unit suite. If the real claim is "the procedure works," replace with a behavioral test that *runs* the documented steps (docs-as-tests / executable examples), not a phrase pin. Per the regression-power gate: delete only when mutants/behavior are covered elsewhere; otherwise re-ground on executable behavior.
- **Why this isn't a false positive:** The asserted file is the repo's own committed documentation under `docs/`, not a temp product fixture. The oracle is presence of natural-language phrases, not a schema/front-matter field or a documented architectural fitness-function negative grep.

### 2. `test_skill_mentions_detail_raw_before_format_json` — delete or docs-lint

- **Location:** `test_docs_oracle.py` → module level
- **Smell:** `prose-pin`
- **Rationale:** The test reads committed `skills/demo-wrapper/SKILL.md` and pins both (a) feature-mention completeness (`"--detail raw"` and `"--format json"` must appear) and (b) an order constraint (`"--detail raw"` appears before `"--format json"` in the file bytes). Mentions and editorial order are change-detectors on prose, not proofs that the flags work or that the skill's procedure is correct.
- **Prescribed remediation:** **Delete.** Replace feature-mention pins with a behavioral invocation of the CLI/skill that exercises `--detail raw` / `--format json` and asserts on structured output. Do not keep an order pin on agent-facing prose in the unit suite. Docs-lint may enforce required headings/structure separately if product policy demands it.
- **Why this isn't a false positive:** The path is the suite's own committed skill file. Feature-mention and A-before-B order pins are the stockroom-shaped signals this smell exists to catch.

## Tests that must NOT be flagged

### `test_wrapper_skill_forbids_raw_python_invocation`

- **Location:** `test_docs_oracle.py` → module level
- **Why not prose-pin:** Negative architectural fitness function on agent-facing prose: the test documents (via comment + assertion rationale) that the wrapper `SKILL.md` must not leak raw internals (`uv run`, `PYTHONPATH=`, `python -m`) because the skill body *is* the executable agent contract. Forbidden-token scans with an explicit architectural rationale are the legitimate FP carve-out (ArchUnit-style `.because()` / fitness-function pattern), not keyword checklists.
- **False-positive guard:** Naive detectors that flag every `"token" not in skill_text` will trip here. The semantic question is *"is this asserting required wording / mentions, or encoding a documented architectural invariant that certain tokens must stay absent from the public agent interface?"* — here it is the latter.

### `test_skill_fixture_roundtrip_preserves_name_front_matter`

- **Location:** `test_docs_oracle.py` → module level
- **Why not prose-pin:** Prose-as-SUT: the test writes a temporary `SKILL.md` under a temp directory, runs a (stub) convert/emit helper against that fixture as *product I/O*, and asserts on the emitted bytes. The markdown under test is not the repo's committed agent prose; it is the SUT's input/output surface.
- **False-positive guard:** Naive detectors that flag any assert involving `SKILL.md` path strings or `.md` reads will trip here. The semantic question is *"is the asserted artifact the suite's own committed docs/skills, or a temp fixture standing in for product I/O?"* — here it is temp product I/O.

## Notes

- Scenario contains 4 tests total: 2 must be flagged with `prose-pin`, 2 must not be flagged (fitness-function + prose-as-SUT).
- Remediation for positives is **delete or docs-lint / re-ground on behavior** — never "strengthen the substring list."
- Sibling smells (`presentation-coupled`, `loose-text-oracle`, `vacuous-assertion`) are not in scope for this fixture; do not reclassify the keyword checklist as presentation-coupled or as a runtime text oracle.
