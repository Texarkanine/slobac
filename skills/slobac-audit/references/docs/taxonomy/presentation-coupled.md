# Presentation-Coupled

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `presentation-coupled` | Medium | per-test | [Maintainable](../principles/test-qualities.md#maintainable), [Independent of implementation](../principles/test-qualities.md#independent-of-implementation) |

## Summary

The test asserts on the exact rendered presentation of an output — a terminal string, HTML fragment, markdown, JSON with ordered keys, log message — when the real contract is about *semantics*. Any cosmetic formatting change breaks the test.

## Aliases

- "presentation coupled"
- "rendered-string equality"
- "golden-string snapshot"
- "long toContain chains"
- "raw HTML assertions"
- "asserts on formatting not semantics"
- "string match on structured output"

## Description

The converse of [`vacuous-assertion`](./vacuous-assertion.md): the oracle is too *strong* in the wrong dimension. Long `toContain` chains over rendered output, full-string equality on prose, HTML with a specific class name — any of these couple the test to rendering accidents rather than the behavior they were trying to describe.

The semantic judgment: identify the layer at which the output has semantic meaning and assert there (parsed HTML node, DOM tree, structured log event, AST, JSON after normalization) rather than at the raw-string layer.

Distinct from [`loose-text-oracle`](./loose-text-oracle.md): that smell is the other failure on free text — an underdetermined substring/regex that is too *weak* to lock meaning (opposite-polarity text still matches). Presentation-coupled is over-strong cosmetic/exact presentation; do not dump every string assert into this entry.

Distinct from [`over-specified-mock`](./over-specified-mock.md): presentation coupling is about over-asserting the *output* of a real SUT; over-spec is about over-asserting the *interactions* with collaborators.

## Signals

- Long `toContain` / `include` chains against rendered terminal output or markdown.
- `expect(html).toBe('<figure class="mermaid-diagram">...<long literal>')`.
- Golden-string snapshots updated every time formatting changes, with reviewers rubber-stamping the diff.
- Assertions on HTML strings that could use a parser (cheerio, Nokogiri, BeautifulSoup, `jsdom`).
- Assertions on structured data via string matching instead of parsing (`assert "status: ok" in resp.text` where `resp.json()` is available).
- Heavy prose fixtures asserted whole, where only one field is load-bearing.

## False-positive guards

String-equality signals over-trigger when rendering itself is the deliverable:

- **The presentation IS the contract.** Tests for code formatters, syntax highlighters, ANSI styling libraries, JSON pretty-printers, markdown renderers, terminal UIs, or any SUT whose deliverable *is* the rendered string MUST assert on the rendered output character-by-character — that's the public contract, and a parsed-AST assertion would lose the formatting fidelity the SUT exists to produce. Flag presentation coupling only when the SUT's contract is *semantic* (a calculator that incidentally returns formatted text, an API that emits JSON which happens to be human-readable) and the test pins formatting accidents that aren't part of the contract.
- **Snapshot tests for visual regression with a semantic sibling.** A snapshot or golden-file assertion paired with a sibling test that asserts the parsed structure is a deliberate two-axis guard: structure for behavior, snapshot for reviewer visual diff. The pair is not over-coupled — each axis catches what the other can't. Flag snapshot-only tests that stand alone with no semantic sibling, where any whitespace edit silently demands a snapshot update with no behavior question asked.

## Prescribed Fix

1. Identify the semantic layer: DOM tree, parsed JSON, AST, normalized-whitespace canonical form.
2. Parse the output; assert on the structural fragment that encodes the behavior.
3. For intentionally-rendered output (docs, UI copy), keep golden-snapshot tests but mark them explicitly as `presentation` tests at a separate tier — they should not block unit-level CI. (See [`wrong-level`](./wrong-level.md) for the tiering vocabulary.)
4. For terminal / log output, assert on a structured event shape when the emitter supports it; otherwise extract via regex with a normalized matcher.
5. Gate: [preservation of regression-detection power](../principles/refactor-qualities.md#preservation-of-regression-detection-power). The test should survive a cosmetic reformat of the SUT output.

## Example

### Before

```ruby
it 'renders mermaid diagrams as figures' do
  result = processor.render(input)
  expect(result).to include('<figure class="mermaid-diagram">')
  expect(result).to include('<img src="./cache/')
  expect(result).to include('alt="diagram"')
  expect(result).to include('</figure>')
end
```

### After

```ruby
it 'renders mermaid diagrams as figures with a cached image reference' do
  html = Nokogiri::HTML.fragment(processor.render(input))
  figure = html.at_css('figure.mermaid-diagram')
  expect(figure).not_to be_nil
  img = figure.at_css('img')
  expect(img['src']).to match(%r{\A\./cache/[0-9a-f]+\.svg\z})
  expect(img['alt']).to be_present
end
```

The original test broke on whitespace, attribute-order, and wrapping changes. The new test asserts the structural contract (a figure wrapping an img with a cached path) and tolerates cosmetic rendering edits.

## Related modes

- [`vacuous-assertion`](./vacuous-assertion.md) — opposite failure (too weak where this one is too narrow).
- [`loose-text-oracle`](./loose-text-oracle.md) — underdetermined meaning on free text (too weak); this entry is over-strong cosmetic/exact presentation.
- [`over-specified-mock`](./over-specified-mock.md) — adjacent over-assertion mode, but interaction-flavored.
- [`mystery-guest`](./mystery-guest.md) — presentation-coupled tests often include giant fixture strings with no summary of what matters.
- [`prose-pin`](./prose-pin.md) — committed docs/skills as oracle; different artifact kind.

## Polyglot notes

Every ecosystem has a semantic-parse alternative:

- **HTML:** cheerio / jsdom / Nokogiri / BeautifulSoup / HtmlAgilityPack.
- **Markdown:** remark / commonmark-java / markdown-it AST.
- **JSON:** native parsers with normalized comparison.
- **Terminal output:** strip-ansi plus pattern matching; structured logs where the emitter allows.
- **SQL:** parsers exist, but usually a round-trip to DB is the honest test.
