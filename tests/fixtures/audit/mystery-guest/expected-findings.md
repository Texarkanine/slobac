# Expected findings — `mystery-guest` scenario

**Target suite root:** `tests/fixtures/audit/mystery-guest/`
**In-scope smells:** `mystery-guest`
**Expected finding count:** 2

The two findings exercise both canonical variants from the [`mystery-guest`](https://texarkanine.github.io/slobac/taxonomy/mystery-guest/) entry: classical mystery guest (external fixture file with no inline summary) and fixture-coupled magic numbers (counts derived from fixture state but written as bare integers). Severity is `Low` and the transform adds documentation only — assertions are not changed. Per the canonical regression-power gate: "Zero AST changes to assertions; only surrounding comments and constants change."

## Findings

### 1. `test_import_orders_returns_all_rows` — annotate fixture shape

- **Location:** `test_csv_importer.py` → module level
- **Smell:** `mystery-guest`
- **Rationale:** The test reads `orders.csv` via `import_orders(FIXTURE_FILE)` and asserts `len(orders) == 6`. Canonical signal "`File.read(path)` / `fs.readFileSync(path)` followed by assertions with no inline fixture summary" plus "`assert count == <n>` with no adjacent comment and `<n>` not derived from anything named in the test" — both fire. A reader cannot tell why 6 is the right answer without opening the CSV.
- **Prescribed remediation:** Per canonical fix step (2), add a ≤3-line comment stating the relevant fixture shape: e.g. `# Fixture shape: 6 order rows across 3 customers (alice, bob, carol) and 3 statuses (paid, pending, refunded).` Per fix step (3), keep the assertion shape but make the count derivable: `EXPECTED_ORDER_ROWS = 6  # rows in orders.csv`. Zero AST changes to the assertion itself; only surrounding comments and a named constant.
- **Why this isn't a false positive:** The test reads an external fixture file and asserts on a magic count derived from its size. There is no inline hint of the fixture's shape, no named constant for 6, and no comment.

### 2. `test_count_paid_returns_four` — annotate derivation

- **Location:** `test_csv_importer.py` → module level
- **Smell:** `mystery-guest`
- **Rationale:** Asserts `count_paid(orders) == 4` — a magic number tied to the exact distribution of `status` values in `orders.csv`. The canonical signal "Magic constant (`6`, `"abc123"`) compared against parsed fixture output" applies, with the additional fragility that editing the fixture (e.g. changing one paid to refunded) silently breaks the test in a way that gives the next reader no diagnostic context.
- **Prescribed remediation:** Per canonical fix step (3), make the derivation explicit: `EXPECTED_PAID_ORDERS = 4  # rows in orders.csv where status == "paid" (1001, 1002, 1004, 1005)`. Or, equivalently, derive the constant from the fixture content: `expected = sum(1 for o in import_orders(FIXTURE_FILE) if o["status"] == "paid")` — but this couples the test to the SUT's exact filtering shape, so the named-constant variant is preferred per the canonical fix bias toward documentation over computation.
- **Why this isn't a false positive:** The number 4 is derived from fixture state but appears as a bare integer with no naming, no comment, and no derivation. A future contributor editing the fixture has no way to see what 4 corresponds to without re-counting the rows.

## Tests that must NOT be flagged

### `test_count_paid_counts_only_paid_status`

- **Location:** `test_csv_importer.py` → module level
- **Why not a mystery guest:** The fixture is inline (a literal list-of-dicts), the relevant shape is *visible* to the reader, and the expectation `EXPECTED_PAID_ROWS` is derived symbolically from the fixture rather than asserted as a magic number. Per the canonical entry's diagnostic — "summarize in one sentence the *relevant* shape of the fixture for this assertion" — the test does this implicitly via inline data plus derived constant.
- **False-positive guard:** Naive detectors that flag any test using a list-of-dicts as fixture data, or any test computing an expectation from a comprehension, will trip here. The semantic question per the canonical entry is *"does the meaning of this test depend on external data the reader can't see?"* — for inline data, the answer is no.

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `mystery-guest`, 1 must not be flagged.
- The fixture also includes a non-test file: `orders.csv`. The audit must not treat data files as test files.
- The remediation is documentation-only — a finding that prescribes changing the assertion (e.g. "replace `len(orders) == 6` with `len(orders) > 0`") is a build-phase bug per the canonical regression-power gate.
- Sibling smells (`shared-state`, `presentation-coupled`) are not in scope; the canonical entry notes the relationship to `shared-state` (shared fixtures often also are mystery guests), but this fixture has no shared state — `FIXTURE_FILE` is a read-only path constant.
