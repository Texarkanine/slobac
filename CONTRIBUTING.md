# Contributing to SLOBAC

## Adding a taxonomy entry

Taxonomy entries live at `skills/audit/references/docs/taxonomy/<slug>.md`. Each entry follows a uniform shape — this is the authoritative template.

### Entry shape

~~~markdown
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

```<language>
// planted smell
```

### After

```<language>
// fixed version
```

## Related modes

- [`other-slug`](./other-slug.md) — how this smell differs from that one.

## Polyglot notes

What changes across ecosystems for detection and the prescribed transform.
~~~

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
| `per-test` | batch assessor (dispatched from `skills/audit/references/subagents/batch.md`) |
| `per-file` | batch assessor (dispatched from `skills/audit/references/subagents/batch.md`) |
| `cross-suite` | cross-suite assessor (dispatched from `skills/audit/references/subagents/cross-suite.md`) |

### After adding an entry

1. Add the slug row to the catalog table in `skills/audit/references/docs/taxonomy/README.md`.
2. Run `uv run properdocs build --strict` — must stay green.
3. Verify all cross-links in the new entry resolve (`../principles.md#anchor`, `../glossary.md#term`, sibling entries).

## Skill architecture

The audit orchestrator (`skills/audit/SKILL.md`) dispatches three subagent workflows:

```
slobac-audit (orchestrator — SKILL.md)
  ├── scout    → Suite Manifest (file inventory + sizes + tier conventions)
  ├── batch    → Findings + Behavior Summaries (×1 or ×N in parallel)
  └── cross-suite → Cross-Suite Findings (if cross-suite smells in scope)
```

Subagent workflows are **raw prompt documents** at `skills/audit/references/subagents/`, not registered skills. The orchestrator reads each file and launches a readonly subagent whose task is that file's content, supplemented with runtime context variables (target directory, absolute `references/` path, format specs).

All shared references (taxonomy entries, format specs, subagent workflows) live under `skills/audit/references/`. No `../` escapes — the skill is self-contained for standalone/marketplace installs.

## REUSE compliance

`skills/audit/` is the only subtree with its own `REUSE.toml` (it carries two licenses: PPL-S for the skill payload and CC-BY-SA-4.0 for `references/docs/**`). Validate its standalone compliance with:

```bash
reuse --root . lint   # run from skills/audit/
```

The `--root .` flag is mandatory — omitting it causes `reuse` to ascend to the `.git` boundary and lint the full monorepo instead.

## Running the doc-site locally

```bash
uv run properdocs serve
```

The site builds from `skills/audit/references/docs/`. `properdocs build --strict` is the CI gate — warnings are errors.
