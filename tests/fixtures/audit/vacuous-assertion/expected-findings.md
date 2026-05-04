# Expected findings — `vacuous-assertion` scenario

**Target suite root:** `tests/fixtures/audit/vacuous-assertion/`
**In-scope smells:** `vacuous-assertion`
**Expected finding count:** 2

The two findings exercise the canonical signal from the [`vacuous-assertion`](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/) entry: the SUT runs and the assertion fires, but many interesting wrong answers would still pass. Distinct from `pseudo-tested` (where a no-op SUT replacement passes) — here a *partially-broken* SUT also passes. Fix bias is **strengthen, don't multiply**: one strong check beats three weak ones.

## Findings

### 1. `test_parse_returns_an_invoice` — strengthen with structural equality

- **Location:** `test_invoice_parser.py` → module level
- **Smell:** `vacuous-assertion`
- **Rationale:** The only assertion is `result is not None`. Apply the canonical diagnostic — *"what minimal wrong answer would this still accept?"* — and the answer is: any constructed `Invoice`, including `Invoice("", "", 0, "")`, `Invoice("garbage", "anyone", 1, "XYZ")`, or one with the customer and currency swapped. The oracle accepts every wrong answer that returns *something*.
- **Prescribed remediation:** **Strengthen.** Replace `assert result is not None` with structural equality: `assert result == Invoice(invoice_id="INV-1234", customer="ACME Corp", amount_cents=12550, currency="USD")`. Per the canonical fix-bias preference order (structural equality > matcher-based containment > regex > prefix/length), structural equality is available and should be used. The [mutation kill-set](https://texarkanine.github.io/slobac/glossary/#mutation-kill-set) must increase strictly after the change.
- **Why this isn't a false positive:** This is the canonical signal `assert x is not None` as the only assertion. The test name promises "returns an invoice" but the body verifies merely "returns *something*" — a vastly weaker claim than the parser's actual contract.

### 2. `test_parse_extracts_an_invoice_id` — strengthen with regex or equality

- **Location:** `test_invoice_parser.py` → module level
- **Smell:** `vacuous-assertion`
- **Rationale:** The assertion is `assert result.invoice_id` — a truthiness check. The invoice_id format `INV-\d+` is knowable, so the canonical signal "`expect(x).toBeTruthy()` on a value with a known-knowable format (UUID, URL, date, enum)" applies. A wrong implementation that returned `invoice_id="garbage"` would still pass, as would one that swapped invoice_id and customer fields (since `"ACME Corp"` is also truthy).
- **Prescribed remediation:** **Strengthen.** Replace with `assert result.invoice_id == "INV-1234"` (structural equality on the field) or `assert re.fullmatch(r"INV-\d+", result.invoice_id)` (regex on the format). Equality is preferred per the fix-bias order. Mutation kill-set must increase strictly.
- **Why this isn't a false positive:** Truthiness on a structured-format string is a textbook vacuous oracle. The test name commits to a specific extraction; the body asserts only that *some* string was returned.

## Tests that must NOT be flagged

### `test_parse_extracts_all_four_fields_in_order`

- **Location:** `test_invoice_parser.py` → module level
- **Why not vacuous:** The assertion is full structural equality on all four fields (`invoice_id`, `customer`, `amount_cents`, `currency`). Apply the canonical diagnostic — *"what minimal wrong answer would this still accept?"* — and the answer is: only the exact correct answer. Wrong-delimiter parsing, wrong index ordering, wrong int conversion (`int("12550")` vs `"12550"`), and wrong currency truncation all produce different `Invoice` instances that fail equality.
- **False-positive guard:** Naive detectors that flag any test with a single assertion or any test using `==` on an object will trip here. The semantic question is *"how many wrong answers does this oracle accept?"* — for full structural equality on all output fields, the answer is one (the correct one).

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `vacuous-assertion` and remediation **strengthen** (with the specific replacement assertion named), 1 must not be flagged.
- The fix-bias preference order (structural equality > matcher containment > regex > prefix/length) is load-bearing — a finding that prescribes a regex when structural equality is available is a build-phase bug per the canonical entry.
- Sibling smells (`pseudo-tested`, `presentation-coupled`) are not in scope; cross-pollution shape, if incidentally present, must be scoped out by the audit.
