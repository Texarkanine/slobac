# Expected findings — `pseudo-tested` scenario

**Target suite root:** `tests/fixtures/audit/pseudo-tested/`
**In-scope smells:** `pseudo-tested`
**Expected finding count:** 2

The two findings exercise the canonical signal from the [`pseudo-tested`](https://texarkanine.github.io/slobac/taxonomy/pseudo-tested/) entry: the SUT runs, the assertion fires, but a no-op replacement of the SUT body would still pass. The audit is correct only when each finding's prescribed remediation names the **specific assertion to add** that would kill the surviving no-op mutant — not a generic "strengthen the test" recommendation.

## Findings

### 1. `test_normalize_returns_non_empty_string` — strengthen with output-equality

- **Location:** `test_text_normalizer.py` → module level
- **Smell:** `pseudo-tested`
- **Rationale:** The test calls `normalize("Hello, World!  ")` then asserts only `isinstance(result, str)` and `len(result) > 0`. If the SUT body were replaced with `return text` (identity / no-op), the input is already a non-empty string — both assertions pass. The "non-empty" check is a structural-shape oracle that any passthrough satisfies. This is the canonical signal: "test body calls SUT, assigns, then runs only structural shape / type / length checks."
- **Prescribed remediation:** **Strengthen.** Add one assertion comparing `result` to the expected normalized output (`assert result == "hello world"`). Per the canonical entry's preserved-fix gate, the [mutation kill-set](https://texarkanine.github.io/slobac/glossary/#mutation-kill-set) delta must be strictly positive — a `mutmut --simple-mutations` run on `normalize` after the strengthening must show that the previously-surviving identity mutant now dies.
- **Why this isn't a false positive:** The shape-only assertions are the *only* assertions present. The existence of a real SUT call doesn't compensate; what determines pseudo-tested status is whether *the assertion* would tell a no-op apart from the real implementation.

### 2. `test_normalize_preserves_some_letters` — strengthen with output-equality

- **Location:** `test_text_normalizer.py` → module level
- **Smell:** `pseudo-tested`
- **Rationale:** The test asserts `"h" in result.lower() or "H" in result` — an existence check that any identity-passthrough also satisfies (since `"HELLO WORLD"` already contains `"H"`). A no-op `return text` survives. This is the "checks only 'has this key' / 'contains this token'" variant of the canonical signal.
- **Prescribed remediation:** **Strengthen.** Replace the existence check with `assert normalize("HELLO WORLD") == "hello world"`. Mutation kill-set delta must be strictly positive after the change.
- **Why this isn't a false positive:** The `in` check is the only assertion. The disjunction with `"H" in result` is itself diagnostic — the test author hedged the casing because they weren't asserting on the casing transform, which is the very behavior `normalize` claims to perform.

## Tests that must NOT be flagged

### `test_normalize_lowercases_and_strips_trailing_punctuation`

- **Location:** `test_text_normalizer.py` → module level
- **Why not pseudo-tested:** The assertion is `normalize("  Hello, World!  ") == "hello world"` — full output equality. Replace the SUT body with `return text` and the assertion compares `"  Hello, World!  "` to `"hello world"`, which fails. The mutation kill-set is strictly larger than zero for this test against the identity mutant.
- **False-positive guard:** Naive detectors that flag any short test body or any test calling the SUT once will trip here. The semantic question is *"would this test pass under a no-op mutation of the SUT?"* — for this test, answer is no.

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `pseudo-tested` and remediation **strengthen** (with the specific replacement assertion named), 1 must not be flagged.
- The remediation must name the specific assertion — generic "add a stronger check" is insufficient per the canonical entry's "Keep the fix local — one well-placed assertion in the canonical test" guidance.
- Sibling smells (`vacuous-assertion`, `tautology-theatre`, `rotten-green`) are *not* in scope for this fixture; if cross-pollution shape is incidentally present, the audit must scope its findings to `pseudo-tested` only.
