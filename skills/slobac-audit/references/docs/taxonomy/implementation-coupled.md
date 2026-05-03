# Implementation-Coupled

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `implementation-coupled` | High | per-test | [Maintainable](../principles.md#maintainable), [Independent of implementation](../principles.md#independent-of-implementation) |

## Summary

The test reaches through a public type into a private method, internal field, or undocumented implementation shape. Renaming or refactoring an internal detail breaks the test even when observable behavior is unchanged.

## Description

Distinct from [`over-specified-mock`](./over-specified-mock.md) — that's about over-asserting *interactions*; this is about reaching into *state* or *visibility*.

The semantic judgment: identify whether the accessed field or method is part of the SUT's stable public API. For third-party libraries, this often requires reading the library's published docs.

## Signals

Direct syntactic signals (language-dependent):

- `(x as any).someProp`, `x['_private']`, `x.#field` (TS/JS).
- `described_class.send(:private_method, ...)` (Ruby).
- `_private_method(` or `_PrivateMethod(` in the test body (Python convention).
- `@VisibleForTesting` / `internal` accessors (Kotlin, Java, C#).
- Accessing lowercase fields from an adjacent test file in a different Go package via `unsafe` or test-package-bridge tricks.

Semantic signals:

- Accessors whose names start with `_` or match known-private conventions.
- For third-party libraries: the accessed field doesn't appear in exported types or public docs.
- Python: `sut._internal_dict['some_key']` instead of a public getter.
- Tests calling private helpers via `(sut as any).helper()` and asserting on the helper's return directly.

## False-positive guards

No audit-specific guards yet; Phase-2 per-smell work will author these.

## Prescribed Fix

1. Drive the library's public API instead of reaching for internals (`program.helpInformation()` rather than `(cmd as any).options`).
2. If a private field encodes a real contract:
   - Ask: is the helper cohesive enough to extract as a pure public function? If yes, extract it with its own tiny unit-test file. This is the *only* "refactor-for-testability" move the taxonomy permits, and only because it clarifies architecture — see the [no-extract-for-testability governor rule](../principles.md#no-extract-for-testability).
   - Otherwise, cover the behavior through integration via the public surface.
3. For third-party internal fields: ask the upstream to expose, or encapsulate behind a project-level adapter so the coupling lives in one place.
4. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power). The transform often reveals [`semantic-redundancy`](./semantic-redundancy.md) (private-method tests duplicate public-API tests) — fold in the same pass.

## Example

### Before

```ruby
describe '#html_document?' do
  it 'recognizes .html files' do
    expect(described_class.send(:html_document?, 'foo.html')).to be true
  end
end
```

### After — option A, cover through the public surface

```ruby
describe 'generate' do
  it 'processes .html files but skips .md files' do
    site = build_site(pages: ['foo.html', 'README.md'])
    generator.generate(site)
    expect(generator.processed_paths).to include('foo.html')
    expect(generator.processed_paths).not_to include('README.md')
  end
end
```

### After — option B, extract as a public helper

Taken only when the helper has domain coherence worth publishing.

```ruby
# lib/html_doc_filter.rb
module HtmlDocFilter
  module_function
  def html_document?(path) = path.end_with?('.html', '.htm')
end

# spec/html_doc_filter_spec.rb
describe HtmlDocFilter do
  it '.html_document? recognizes .html and .htm extensions' do
    expect(HtmlDocFilter.html_document?('foo.html')).to be true
    expect(HtmlDocFilter.html_document?('foo.htm')).to be true
    expect(HtmlDocFilter.html_document?('foo.md')).to be false
  end
end
```

Option A covers the behavior through `generate`'s observable effects; no private-method reach-through. Option B is taken only when the helper has domain coherence worth publishing.

## Related modes

- [`over-specified-mock`](./over-specified-mock.md) — the "testing internal details" variant is the mock-shaped version of this smell.
- [`wrong-level`](./wrong-level.md) — private-method tests at the "unit" level often belong at the component level, verifying via the public surface.
- [`tautology-theatre`](./tautology-theatre.md) — `spyOn(sut, 'privateMethod')` combines both smells.

## Polyglot notes

"What counts as private" is per-language:

- **Python:** `_single_leading_underscore` by convention; `__double_leading_underscore` is name-mangled.
- **Ruby:** `private`, `protected`, with `send(:name)` as a bypass.
- **TS/JS:** `private` / `#name` / casts to `any`.
- **Go:** lowercase is package-private; cross-package access requires export.
- **JVM:** `private`, package-private; `@VisibleForTesting` as controlled relaxation.
- **C#:** `internal`, `InternalsVisibleTo` attribute.

Ship a per-language signal table; the judgment layer is language-agnostic.
