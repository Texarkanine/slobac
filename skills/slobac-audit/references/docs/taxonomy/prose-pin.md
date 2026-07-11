# Prose-Pin

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `prose-pin` | High | per-test | [Maintainable](../principles/test-qualities.md#maintainable), [Necessary](../principles/test-qualities.md#necessary), [Independent of implementation](../principles/test-qualities.md#independent-of-implementation) |

## Summary

The test treats the suite's own committed documentation or other prose as an oracle — keyword checklists, feature-mention pins, or editorial order — so wording edits fail CI with no product regression.

## Aliases

- "prose pin"
- "documentation-pin"
- "change-detector-on-docs"
- "prose-as-oracle"
- "docs keyword checklist"
- "SKILL.md mention pin"
- "assert phrase in README"
- "feature-mention completeness on docs"

## Description

A specialization of change-detector tests[^change-detector] and Sensitive Equality[^sensitive-equality] applied to **committed prose** — any checked-in natural-language artifact the suite treats as an oracle. That includes but is not limited to READMEs, `docs/**`, HTML/help pages, changelogs, packaging blurbs, and agent-facing skill bodies (`SKILL.md`, `AGENTS.md`, `CLAUDE.md`, and cousins).

The assertion binds to incidental wording — required phrases, feature mentions, A-before-B order in file bytes — rather than to a behavioral contract. Green means "the strings are still present," not "the documented procedure works" or "the shipped flag works." Token presence in committed prose is an unanchored proxy for product meaning: editorial rewrites and feature-mention checklists fail CI with no product change, and they never verified the product in the first place.

The semantic judgment: ask *"would an editorial rewrite that preserves meaning turn this test red with no product change?"* and *"did this assert ever encode a behavioral contract, or only that wording exists?"* If the artifact is the repo's own committed prose (not a temp product fixture) and the answer to either is damning, the smell fires.

Distinct from [`loose-text-oracle`](./loose-text-oracle.md): that smell targets **runtime-emitted** text (errors, logs, stdout). Distinct from [`presentation-coupled`](./presentation-coupled.md): that smell is over-strong exact/cosmetic presentation of SUT *output*, not committed prose as oracle.

## Signals

- `assert "phrase" in Path("docs/...").read_text()` / `README.md` / committed HTML / other checked-in prose keyword checklists.
- Feature-mention pins after shipping a flag: `assert "--detail raw" in skill_md` (or README / help page) as a proxy for "the flag works."
- Order pins on prose: `text.index("step A") < text.index("step B")` in docs, skills, or help pages.
- Packaging/front-matter checks that only assert non-empty name/description strings without schema validation (weaker sibling — prefer schema/manifest validation instead).

## False-positive guards

- **Architectural fitness-function negative greps.** Forbidden-token scans on committed public-facing prose (`assert "uv run" not in skill_text`, banned phrases in agent wrappers or published docs) with a documented architectural rationale (comment, ArchUnit-style `.because()`, or equivalent)[^fitness] encode a real interface invariant. Do not flag these as prose-pin; they are the legitimate carve-out. Require the documented rationale — a bare `assert "token" not in text` without architectural framing is still suspect.
- **Prose-as-SUT (temp product I/O).** Tests that write/read a temporary markdown / HTML / `SKILL.md` fixture as the SUT's input or output (convert, emit, round-trip) are asserting on product I/O, not on the repo's committed prose. Do not flag.
- **Schema / manifest validation.** Front-matter or packaging checks that validate structured fields (required keys, types, length bounds) via a schema or parser are manifest contracts, not keyword checklists. Prefer keeping them; do not prescribe delete.
- **Docs-as-tests / doctest / executable examples.** Suites that *run* code embedded in docs (phmdoctest, pytest-markdown-docs, and cousins) exercise product behavior. That is the healthy inverse of prose-pin — do not flag.
- **Dedicated docs-lint tiers.** Vale / markdownlint / link-checker jobs that validate docs *as docs* outside the unit suite are the prescribed home for surviving prose policy — not a smell when already tiered correctly.

## Prescribed Fix

| Shape | Transform |
|---|---|
| Keyword checklist / feature-mention / order pin on committed prose | **Delete.** Presence of wording was never a behavioral contract — "the flag is mentioned" does not mean the flag works. |
| A real product claim still needed ("flag X works", "onboarding works") | Re-ground on a behavioral invocation / docs-as-tests that exercises the product and asserts structured outcomes — do not keep the prose pin beside it. |
| Policy still wants wording / terminology checks | Move to a docs-lint tier (Vale, markdownlint) that does not gate the unit suite. |
| Vacuous non-empty front-matter string checks | Reframe as schema/manifest validation; keep if structural. |
| Fitness-function forbidden-token scan with documented rationale | **Keep** — not a smell. Optionally back with a behavioral eval of the real interface. |

Disposition order (strongest first):

1. **Delete** — the assert never locked product behavior (keyword / mention / order pins)
2. **Re-ground** — replace with a behavioral or docs-as-tests check of the real claim
3. **Tier** — move surviving prose policy to docs-lint, out of unit CI
4. **Keep** — only fitness-function negatives and schema/manifest validation with explicit rationale

Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power). Do not "strengthen" a keyword list — that deepens the change-detector. Deleting a mention pin does not drop regression power it never had.

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

The original test failed whenever an editor clarified the onboarding copy without changing product behavior — and green never meant the procedure worked. Deleting (or tiering under docs-lint) removes a change-detector that killed no behavioral mutants.

## Related modes

- [`loose-text-oracle`](./loose-text-oracle.md) — cousin on **runtime-emitted** text (errors/logs/stdout); same "string as semantic stand-in" disease, different artifact kind (process output vs committed prose).
- [`presentation-coupled`](./presentation-coupled.md) — over-strong exact/cosmetic presentation of SUT *output*; not committed prose.
- [`vacuous-assertion`](./vacuous-assertion.md) — oracle too weak on real SUT output; prose-pin's decisive fact is the *committed-prose* surface.
- [`implementation-coupled`](./implementation-coupled.md) — couples to private code shape; prose-pin couples to incidental *wording* of public docs.

## Polyglot notes

The surface is language-agnostic: any runner that can `readFile` / `Path.read_text` / `ioutil.ReadFile` a committed prose artifact and assert substrings. Classic forms are README / docs / HTML help keyword checklists in any stack. Agent-skill ecosystems (`SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`) are a 2024–2026 hot path — one class of committed prose, not a separate smell. Prefer docs-lint (Vale, markdownlint) and schema validation (JSON Schema / front-matter parsers) as the polyglot homes for surviving checks.

[^change-detector]: Google Testing Blog (2015). *Testing on the Toilet: Change-Detector Tests Considered Harmful*. Also *Software Engineering at Google*, ch. 13. A documentation-pin fails when wording changes regardless of whether product behavior changed — the change-detector symptom applied to committed prose.

[^sensitive-equality]: van Deursen, A., Moonen, L., van den Bergh, A., & Kok, G. (2001). *Refactoring Test Code*. Also Meszaros, G. *xUnit Test Patterns* — "Sensitive Equality" / Fragile Test. Coupling a test to an incidental string representation; prose-pin generalizes that from `toString()` output to committed file bytes. <http://xunitpatterns.com/Sensitive%20Equality.html>.

[^fitness]: Ford, N., Parsons, R., & Kua, P. *Building Evolutionary Architectures* (O'Reilly). Architectural fitness functions provide an objective integrity assessment of architectural characteristics — the framing for legitimate forbidden-token scans on public-facing prose (ArchUnit-style negative rules).
