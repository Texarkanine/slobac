# Expected findings — `presentation-coupled` scenario

**Target suite root:** `tests/fixtures/audit/presentation-coupled/`
**In-scope smells:** `presentation-coupled`
**Expected finding count:** 2

The two findings exercise canonical signals from the [`presentation-coupled`](https://texarkanine.github.io/slobac/taxonomy/presentation-coupled/) entry: full-string equality on rendered HTML, and long `toContain`/`in` chains against the same. The audit is correct only when each finding's prescribed remediation names the **specific parsing layer** (HTML parser, JSON parse, DOM tree) at which the assertion should land.

## Findings

### 1. `test_render_status_html_for_active_user` — parse-and-assert-on-DOM

- **Location:** `test_report_renderer.py` → module level
- **Smell:** `presentation-coupled`
- **Rationale:** The test asserts full-string equality on rendered HTML. The canonical signal `expect(html).toBe('<figure class="..." ...>...<long literal>')` applies. The structural contract is "a status-row div wrapping a status span and a count span"; the cosmetic concerns the test pins include attribute ordering, whitespace between tags, exact class-name strings, ALLCAPS spelling of `ACTIVE`, and self-closing-vs-open tag style. A cosmetic refactor — adding a wrapping element for theming, reordering class attributes for code-style consistency, or pretty-printing the HTML for debug-mode output — breaks this test without changing the visible page.
- **Prescribed remediation:** Parse the HTML and assert on the structural fragment. Per canonical fix step (1), identify the semantic layer — for HTML, that's the parsed DOM. Use `BeautifulSoup` (Python) or `lxml.html` to parse the rendered string, then `assert soup.select_one(".status-row")["data-name"] == "alice"`, `assert soup.select_one(".status-active").text.strip().lower() == "active"`, `assert soup.select_one(".count").text == "5"`. The post-fix test must survive cosmetic reformat of the SUT output (canonical regression-power gate).
- **Why this isn't a false positive:** Full-string equality on HTML is the textbook canonical signal. The test's name promises a behavioral claim ("renders status for active user"); the body verifies a presentational claim (one particular byte-equal HTML rendering).

### 2. `test_render_status_html_includes_active_styling` — parse or delete

- **Location:** `test_report_renderer.py` → module level
- **Smell:** `presentation-coupled`
- **Rationale:** Long `in`-chain (5 substring assertions) against rendered HTML. Each assertion pins a separate cosmetic concern: class-name strings (`status-active`), exact uppercase spelling (`ACTIVE`), literal attribute syntax (`data-name="bob"`), tag-shape (`<span`, `</div>`). The canonical signal "Long `toContain` / `include` chains against rendered terminal output or markdown" applies directly.
- **Prescribed remediation:** Parse with BeautifulSoup; assert on the parsed structural shape (status-active class is present in the DOM, count text equals "3"). Delete the `<span` and `</div>` shape assertions — those are tag-existence claims that any HTML parse would assert structurally. Per fix step (3), if the test is intentionally guarding rendered-presentation contracts (e.g. for a styled UI), keep a single golden-snapshot test marked at a `presentation` tier and use [`wrong-level`](https://texarkanine.github.io/slobac/taxonomy/wrong-level/) tier vocabulary to keep it out of unit-level CI.
- **Why this isn't a false positive:** The number of `in` checks (5) and the cosmetic nature of each (class names, casing, attribute syntax, tag shape) collectively trip the canonical signal. A single `in` check against a non-cosmetic substring would not — the signal is the *chain*.

## Tests that must NOT be flagged

### `test_render_status_json_encodes_name_status_and_count`

- **Location:** `test_report_renderer.py` → module level
- **Why not presentation-coupled:** The test calls `json.loads(rendered)` to parse the SUT output to its semantic layer (a dict), then asserts structural equality on the parsed value. Any cosmetic change in the renderer (key ordering — JSON dict ordering is preserved in Python 3.7+ but irrelevant to `==` on dicts; whitespace; trailing newlines) leaves the test green. The assertion is at the layer where the output has semantic meaning, exactly per canonical fix step (1).
- **False-positive guard:** Naive detectors that flag any test asserting on a renderer's output will trip here. The semantic question per the canonical entry is *"is the assertion at the layer where the output has semantic meaning, or at the raw-string layer?"* — for `json.loads(...) == {...}`, the answer is "semantic layer."

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `presentation-coupled`, 1 must not be flagged.
- The two findings prescribe different post-parse assertions (full-DOM structural for finding 1, scoped `select_one` for finding 2) — both must name the parser library and the specific selectors. Generic "parse the HTML" without a concrete selector is a build-phase bug per the canonical entry's preference for *the* structural fragment that encodes the behavior.
- Sibling smells (`vacuous-assertion`, `mystery-guest`, `over-specified-mock`) are not in scope.
