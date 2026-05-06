# Decision: Test level vs tier vs pyramid (SLOBAC vocabulary)

## Context

**What:** Pick one canonical name for “where a test sits” in the stack, decide what belongs in the glossary vs in the `wrong-level` smell entry, and clarify whether “pyramid” refers to suite composition (many unit, fewer end-to-end) or to vertical distance from harness to SUT.

**Why it matters:** Auditors and the [`wrong-level`](../../../skills/slobac-audit/references/docs/taxonomy/wrong-level.md) smell need a shared, findable rule. Two names (“tier” and “pyramid level”) plus an unexplained pyramid confuse lookup and misfire false positives when people mix up *portfolio shape* with *per-test depth*.

**Constraints:** Align with smell slug `wrong-level`; keep glossary alphabetical and readable standalone; avoid duplicating huge matrices in two places; preserve repo-conditional false-positive guards in `wrong-level`.

## Options Evaluated

- **A — Canonical “test tier” only:** Matches some industry usage; conflicts with `wrong-level` and scatters “tier” vs “level” across docs.
- **B — Canonical “test level” with “tier” and informal “pyramid level” as aliases:** Aligns slug, glossary, and narrative; one anchor (`#test-level`).
- **C — Retire “pyramid” language entirely:** Reduces confusion but loses a common alias readers search for; keep the word only as explained metaphor.

## Analysis

| Criterion | A (tier only) | B (level + aliases) | C (drop pyramid) |
|-----------|---------------|---------------------|------------------|
| Consistency with `wrong-level` | Weak | Strong | Strong |
| Discoverability for “pyramid” searchers | OK | Strong (alias + explanation) | Weak |
| Glossary vs smell split | Same as B | Glossary = term + splits + pyramid disambiguation; smell = matrix + audit workflow | Same |

**Key insights:**

- The **Mike Cohn-style test pyramid** is about **how many** tests of each kind you want in a healthy suite (fast, narrow tests are numerous; slow, wide tests are few).
- **SLOBAC “level”** is about **how much real stack** sits under the assertion for *this* test (call stack inside vs outside SUT, process boundary, network, etc.). That is a *per-test vertical* notion — related imagery, different question.
- Operational detail (tables, examples) belongs on [`wrong-level`](../../../skills/slobac-audit/references/docs/taxonomy/wrong-level.md) so classifiers land in the right doc when diagnosing the smell; the glossary defines the term once and points there.

## Decision

**Selected:** **B** — canonical **test level**; **test tier** as synonymous alias; **pyramid** kept only as explained vocabulary (portfolio pyramid vs vertical depth), not as a second required term.

**Rationale:** One primary anchor, alignment with the smell slug, and explicit disambiguation so “wrong pyramid” searches still resolve without treating portfolio theory as the classification rule.

**Tradeoff:** Authors must use “test level” in new prose; occasional “tier” in legacy phrases is fine if glossary aliases are visible once.

## Implementation Notes

- Glossary: `## Test level` with short definition, unit/integration rule, secondary split summary, link to `wrong-level#classifying-test-level`, pyramid disambiguation paragraph.
- `wrong-level.md`: new `## Classifying test level` with full tables, stack-depth intuition, intersection note for other smells.
- Replace `#test-tier` with `#test-level`; update taxonomy catalog line and behavior-summary-format wording where it said “pyramid tier.”
