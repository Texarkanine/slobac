# `naming-lies` — audit-specific augmentation

This file carries audit-runtime guidance only. The canonical definition of the smell — what it is, why it matters, the signals, the three-way prescribed fix — lives in [`docs/taxonomy/naming-lies.md`](../../../../docs/taxonomy/naming-lies.md) and must be read alongside this file. Nothing here restates the manifesto.

## Invocation-phrase hints

Natural-language phrases that scope an invocation to this smell:

- "naming-lies", "naming lies", "lying names", "lying titles"
- "titles that lie", "docstrings that lie"
- "names that don't match the body", "title/body mismatch"
- "tests whose names overpromise"

When the operator uses any of these, treat the scope as `naming-lies` unless they also name another supported smell, in which case treat it as both.

## Emission hints

Every finding under this smell **must name one of three fix arms** from the manifesto's Prescribed Fix section. The arm is load-bearing — a finding that identifies a mismatch without naming the arm is half a finding. Decision rules, in order:

1. **RENAME** — when the body is a clean, well-scoped claim on its own terms, and the title was aspirational or wrong. Cheapest move; rename-only preserves the call graph trivially.
2. **STRENGTHEN** — when the title captures the real intent and the body under-delivers. Hand off to [`vacuous-assertion`](../../../../docs/taxonomy/vacuous-assertion.md) in the remediation; the actual strengthening is out of Phase-1 scope but the recommendation is in scope. Preservation gate: mutation kill-set delta ≥ 0 after strengthening.
3. **INVESTIGATE** — when both title and body are suspect, or the test's intent cannot be read from the test alone. Recommend [describe-before-edit](../../../../docs/principles.md#behavior-articulation-before-change): the operator (or a downstream agent) must articulate what the test is supposed to prove before any fix. The audit surfaces the ambiguity rather than picking an arm.

When uncertain between RENAME and STRENGTHEN, ask: is the title's claim specific and testable (a derivation rule, an invariant, a bound)? If yes, lean STRENGTHEN — the title is likely the real intent. If the title is a shape claim (styling, color, format) with no specific semantics, lean RENAME — the body's claim is the actual contract.

When the manifesto's Related modes cross-links to a different smell (e.g. `vacuous-assertion` for STRENGTHEN, `rotten-green` when a lie is also missing any assertions at all), cite the related smell in the rationale.

## False-positive guards

Token-level title/body comparison is a first pass. The following over-triggers must be suppressed:

- **Cross-language synonymy.** The title says `deletes`, the body uses `DELETE FROM` in SQL. Title says `waits`, the body uses `time.sleep` or `asyncio.sleep`. Title says `colored`, the body checks CSS class names for `.text-danger`. These are semantic matches even though the surface tokens differ. Rule: before flagging on a missing-token basis, consider whether a sibling ecosystem (SQL, HTTP status codes, CSS classes, shell exit codes, HTTP methods, ANSI codes) carries the semantic equivalent of the title's token.
- **Domain synonymy.** The title uses a product term; the body uses the underlying implementation name. Example: title `test_session_is_expired`, body checks `row["state"] == "TERMINATED"`. The audit must recognize that the product-layer term and the storage-layer term denote the same state. This is the hardest class of false positive; when in doubt, **note the ambiguity in the rationale and lean toward INVESTIGATE** rather than RENAME.
- **Titles that are short-hands.** Pytest, JUnit, and RSpec encourage terse test titles. A title `test_price_math` whose body verifies a specific rounding rule is not lying — it is under-specified. The audit's remediation should be to suggest a more specific name, not flag it as a lie. Distinguish **under-specified** (title leaves room, body is a correct subset of what a fuller title would claim) from **lying** (title claims X, body verifies not-X or unrelated-to-X). Under-specified titles are outside Phase-1 scope.
- **Failure-case tests.** A test titled `rejects_invalid_input` whose body runs the invalid input and asserts an exception was raised is a match, not a lie. Titles that name a **negative** behavior and bodies that verify the negative behavior (via exception, error code, sentinel value) belong to the same semantic class.

## Detection priorities

Within the canonical Signals list, these three are the highest-yield for Phase 1:

1. Title nouns with no surface in the body's assertions (after accounting for synonymy per the false-positive guards).
2. Docstrings that claim a specific derivation rule, invariant, or default value, with assertion bodies that do not verify the claim (common STRENGTHEN trigger).
3. Title adjectives referring to presentation, format, or styling (`color`, `bold`, `cyan`, `indented`, `stripped`) in bodies that do no format-level checking (common RENAME trigger).

## Polyglot note for Phase 1

Trivially polyglot per the manifesto. The token/synonymy-matching discipline is language-neutral. When auditing a non-Python suite, the same rules apply; the ecosystem-specific synonymy tables (SQL keywords, HTTP methods, ANSI codes, CSS properties) are listed in the manifesto entry's Polyglot notes.
