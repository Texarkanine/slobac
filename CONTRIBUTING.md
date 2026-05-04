# Contributing to SLOBAC

## Adding a taxonomy entry

Taxonomy entries live at `skills/slobac-audit/references/docs/taxonomy/<slug>.md`. Each entry follows a uniform shape — this is the authoritative template.

### Entry shape

```markdown
| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `<slug>` | Critical / High / Medium / Low | per-test / per-file / cross-suite | [Principle](../principles.md#anchor) |

## Summary

One-line TL;DR of the smell.

## Aliases

- "alternate name operators or search engines might use"
- "another common phrase for this smell"

_Audience: human readers landing on this entry from a fuzzy search query. The audit orchestrator does not read this section — it requires explicit slug invocation._

## Description

What the smell is, why it matters, and what semantic judgment is required (i.e. what a linter cannot do).

## Signals

- AST-level or static signal.
- Semantic signal requiring LLM judgment.

## False-positive guards

- **Name for over-trigger class.** Description of the case and the decision rule to suppress it.

## Prescribed Fix

| Shape | Transform |
|---|---|
| Describe the smell shape | The mechanical move |

Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power).

## Example

### Before

\`\`\`<language>
// planted smell
\`\`\`

### After

\`\`\`<language>
// fixed version
\`\`\`

## Related modes

- [`other-slug`](./other-slug.md) — how this smell differs from that one.

## Polyglot notes

What changes across ecosystems for detection and the prescribed transform.
```

### Required fields

Every entry must carry all sections above. Sections with `No audit-specific guards yet` in False-positive guards are stubs — fill them in or leave the stub; do not delete the section heading.

### Severity scale

| Value | Meaning |
|---|---|
| Critical | Usually safe to delete outright — the test kills no mutants |
| High | Real harm; fix is well-defined but needs care |
| Medium | Moderate harm; transform requires reviewer attention |
| Low | Low harm; annotate or split rather than delete |

Severity is a prioritization hint, not a mandate.

### Detection Scope

| Value | Handled by |
|---|---|
| `per-test` | `slobac-batch` assessor |
| `per-file` | `slobac-batch` assessor |
| `cross-suite` | `slobac-cross-suite` assessor |

### After adding an entry

1. Add the slug row to the catalog table in `skills/slobac-audit/references/docs/taxonomy/README.md`.
2. Run `uv run properdocs build --strict` — must stay green.
3. Verify all cross-links in the new entry resolve (`../principles.md#anchor`, `../glossary.md#term`, sibling entries).

## Running the doc-site locally

```bash
uv run properdocs serve
```

The site builds from `skills/slobac-audit/references/docs/`. `properdocs build --strict` is the CI gate — warnings are errors.
