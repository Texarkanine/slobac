# Prose-Pin

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `prose-pin` | High | per-test | [Maintainable](../principles/test-qualities.md#maintainable), [Necessary](../principles/test-qualities.md#necessary), [Independent of implementation](../principles/test-qualities.md#independent-of-implementation) |

## Summary

The test treats the suite's own committed documentation or agent-skill prose as an oracle — keyword checklists, feature-mention pins, or editorial order — so wording edits fail CI with no product regression.

## Aliases

- "prose pin"
- "documentation-pin"
- "change-detector-on-docs"
- "prose-as-oracle"
- "docs keyword checklist"
- "SKILL.md mention pin"
- "assert phrase in README"
- "feature-mention completeness on docs"

_Audience: human readers landing on this entry from a fuzzy search query. The audit orchestrator does not read this section — it requires explicit slug invocation._

## Description

A specialization of change-detector / Sensitive Equality applied to **committed** markdown and agent-facing skill bodies (`README`, `docs/*.md`, `SKILL.md`, `AGENTS.md`, and cousins). The assertion binds to incidental wording — required phrases, flag mentions, A-before-B order in file bytes — rather than to a behavioral contract. Green means "the strings are still present," not "the documented procedure or shipped flag still works."

The semantic judgment: ask *"would an editorial rewrite that preserves meaning turn this test red with no product change?"* If yes, and the asserted artifact is the repo's own committed prose (not a temp product fixture), the smell fires.

Distinct from [`loose-text-oracle`](./loose-text-oracle.md): that smell targets **runtime-emitted** text (errors, logs, stdout). Distinct from [`presentation-coupled`](./presentation-coupled.md): that smell is over-strong exact/cosmetic presentation of SUT *output*, not committed docs as oracle.

## Signals

- `assert "phrase" in Path("docs/...").read_text()` / `README.md` / committed `SKILL.md` keyword checklists.
- Feature-mention pins after shipping a flag: `assert "--detail raw" in skill_md` as a proxy for "the flag works."
- Order pins on prose: `text.index("step A") < text.index("step B")` in docs or skills.
- Packaging/front-matter checks that only assert non-empty name/description strings without schema validation (weaker sibling — prefer schema/manifest validation instead).

## False-positive guards

- **Architectural fitness-function negative greps.** Forbidden-token scans on agent-facing prose (`assert "uv run" not in skill_text`) with a documented architectural rationale (comment, ArchUnit-style `.because()`, or equivalent) encode a real interface invariant — "the public agent contract must not leak raw internals." Do not flag these as prose-pin; they are the legitimate carve-out. Require the documented rationale — a bare `assert "token" not in text` without architectural framing is still suspect.
- **Prose-as-SUT (temp product I/O).** Tests that write/read a temporary `SKILL.md` / markdown fixture as the SUT's input or output (convert, emit, round-trip) are asserting on product I/O, not on the repo's committed agent prose. Do not flag.
- **Schema / manifest validation.** Front-matter or packaging checks that validate structured fields (required keys, types, length bounds) via a schema or parser are manifest contracts, not keyword checklists. Prefer keeping them; do not prescribe delete.
- **Docs-as-tests / doctest / executable examples.** Suites that *run* code embedded in docs (phmdoctest, pytest-markdown-docs, and cousins) exercise product behavior. That is the healthy inverse of prose-pin — do not flag.
- **Dedicated docs-lint tiers.** Vale / markdownlint / link-checker jobs that validate docs *as docs* outside the unit suite are the prescribed home for surviving prose policy — not a smell when already tiered correctly.

## Prescribed Fix

| Shape | Transform |
|---|---|
| Keyword checklist / feature-mention / order pin on committed docs or skills | **Delete** from the unit suite, or move to a docs-lint tier that does not gate unit CI. |
| "Docs mention flag X" standing in for "flag X works" | Re-ground on a behavioral invocation that exercises the flag and asserts structured output. |
| Vacuous non-empty front-matter string checks | Reframe as schema/manifest validation; keep if structural. |
| Fitness-function forbidden-token scan with documented rationale | **Keep** — not a smell. Optionally back with a behavioral eval that the agent uses the on-path shim. |

Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power). Delete only when the behavioral claim is covered elsewhere (or was never behavioral). Do not "strengthen" a keyword list — that deepens the change-detector.

## Example

### Before

```python
def test_onboarding_doc_mentions_required_phrases():
    text = Path("docs/onboarding.md").read_text()
    assert "install the CLI" in text
    assert "run the smoke check" in text
    assert "report failures upstream" in text
```

### After

```python
# Deleted from the unit suite. Editorial wording is no longer a CI gate.
# If policy requires phrase presence, enforce it in a docs-lint / Vale job.
# If the real claim is "onboarding works," run the documented steps
# (docs-as-tests) and assert on product outcomes — not on file bytes.
```

The original test failed whenever an editor clarified the onboarding copy without changing product behavior. Deleting (or tiering under docs-lint) removes a change-detector that killed no behavioral mutants.

## Related modes

- [`loose-text-oracle`](./loose-text-oracle.md) — cousin on **runtime-emitted** text (errors/logs/stdout); same "string as semantic stand-in" disease, different artifact and fix hierarchy.
- [`presentation-coupled`](./presentation-coupled.md) — over-strong exact/cosmetic presentation of SUT *output*; not committed docs.
- [`vacuous-assertion`](./vacuous-assertion.md) — oracle too weak on real SUT output; prose-pin's oracle is often also weak, but the decisive fact is the *committed-prose* surface.
- [`implementation-coupled`](./implementation-coupled.md) — couples to private code shape; prose-pin couples to private *wording* of public docs.

## Polyglot notes

The surface is language-agnostic: any runner that can `readFile` / `Path.read_text` / `ioutil.ReadFile` a committed `.md` and assert substrings. Agent-skill ecosystems (SKILL.md, AGENTS.md, CLAUDE.md, `.cursorrules`) are the novel 2024–2026 hot path; the same smell applies to classic README/docs keyword checklists in any stack. Prefer docs-lint (Vale, markdownlint) and schema validation (JSON Schema / front-matter parsers) as the polyglot homes for surviving checks.
