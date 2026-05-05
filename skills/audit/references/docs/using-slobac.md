# Using the SLOBAC audit

The SLOBAC manifesto ships alongside an agentic audit capability: a set of [AgentSkills.io](https://agentskills.io/)-shaped skills that audit a test suite against this manifesto and emit a portable markdown report. This page covers installing, invoking, and troubleshooting the audit.

If you are here to read about what tests should be — not run a tool — you are already in the right place. The manifesto pages ([Principles](principles.md), [Taxonomy](taxonomy/README.md), [Workflows](workflows.md), [Glossary](glossary.md)) stand on their own; no software is required.

## Scope

The audit is **read-only**: it reports findings; it does not modify test code. Applying a recommendation is a separate step (today manual; automated apply is a future capability).

The detection prose in every taxonomy entry is language-neutral, but **Python is the only validated ecosystem** today. The [Polyglot notes](taxonomy/README.md) section in each entry describes the per-language detection surface for future work.

Operators invoke the audit with **explicit slug names** — e.g. `tautology-theatre`, `vacuous-assertion`. Free-text or fuzzy-phrase requests are refused with the supported-slug list. The unscoped wildcard `all` (or an unscoped invocation) resolves to the full supported set.

## Install

The audit ships as a single **plugin** with one registered skill (`audit`). Install the plugin once; the orchestrator dispatches subagents internally from workflow prompts bundled in `references/subagents/`.

### Cursor

1. Open **Cursor Settings → Marketplace** (or your Cursor version's equivalent plugin marketplace UI).
2. Add the marketplace catalog from [`Texarkanine/txrk9-agent-plugins`](https://github.com/Texarkanine/txrk9-agent-plugins) if it is not already configured (that repo publishes `.cursor-plugin/marketplace.json`).
3. Install the **SLOBAC** plugin (`slobac`). Cursor registers the invocation `/slobac-audit` from the `SKILL.md` frontmatter `name` field.

### Claude Code

1. Register the marketplace catalog from [`Texarkanine/txrk9-agent-plugins`](https://github.com/Texarkanine/txrk9-agent-plugins) (see that repo's `.claude-plugin/marketplace.json`).
2. Install the **slobac** plugin from the marketplace. Claude Code namespaces skills as `/plugin-name:folder-name` — with plugin name `slobac` and folder `audit/`, you invoke `/slobac:audit`.

### Legacy: symlink checkout (developers only)

If you are developing SLOBAC from a Git clone and need the pre-marketplace layout, symlink the `skills/audit/` directory into `.cursor/skills/` or `.claude/skills/` exactly as in older revisions of this page. This path is **not** recommended for end users; prefer marketplace install.

### Other harnesses

If your harness supports the AgentSkills.io shape, point its skill loader at the `skills/audit/` directory. The `SKILL.md` frontmatter (`name`, `description`) and the `references/` subtree follow the standard convention; no harness-specific glue is required.

## Invoke

Natural language with an explicit slug or slugs. Examples:

- `"Audit tests/ for tautology-theatre."`
- `"Audit tests/unit/ for naming-lies and vacuous-assertion."`
- `"Audit tests/ for all smells."`
- `"Audit tests/ for all smells — 1M context window."`
- `"Audit src/tests/ and write the report to reports/audit-2026-04.md."`

The skill scopes the audit from the phrasing, orchestrates subagents as needed, and writes `slobac-audit.md` in the current working directory (or the path you provide).

For a list of available slugs, see the [taxonomy catalog](taxonomy/README.md).

### Context window

**For best results, run SLOBAC with your largest available model and context window.** In Cursor, enable MAX mode. In Claude Code, use Opus or Sonnet with the 1M context window. Larger context means fewer batches, richer cross-suite analysis, and better recall on redundancy detection. SLOBAC works at 200K context but shards more aggressively, trading recall on cross-suite smells for safety.

Pass your context window size in the invocation — `"Audit tests/ — 1M context window"` — to skip the one-time question the orchestrator asks when it encounters a large suite without a stated budget.

## Verify your install

The repo ships fixture suites under [`tests/fixtures/audit/`](https://github.com/Texarkanine/slobac/tree/main/tests/fixtures/audit) with documented expected findings. Invoke the skill against a fixture path and compare the emitted `slobac-audit.md` to the fixture's `expected-findings.md`. Phrasing need not be byte-identical — the shape contract is that every expected finding is emitted with its correct smell slug, remediation arm, and a rationale citing the canonical docs entry.

### Per-test smells (batch assessor)

1. `"Audit tests/fixtures/audit/deliverable-fossils/ for deliverable-fossils."` — 4 findings, 1 negative.
2. `"Audit tests/fixtures/audit/naming-lies/ for naming-lies."` — Compare against `expected-findings.md`.
3. `"Audit tests/fixtures/audit/both-smells/ for all smells."` — Exercises scope honoring with mixed smells.
4. `"Audit tests/fixtures/audit/clean/."` — Expect no findings.
5. `"Audit tests/fixtures/audit/tautology-theatre/ for tautology-theatre."` — 2 findings, 1 negative; remediation **delete**.
6. `"Audit tests/fixtures/audit/pseudo-tested/ for pseudo-tested."` — 2 findings, 1 negative.
7. `"Audit tests/fixtures/audit/vacuous-assertion/ for vacuous-assertion."` — 2 findings, 1 negative.
8. `"Audit tests/fixtures/audit/over-specified-mock/ for over-specified-mock."` — 2 findings, 1 negative.
9. `"Audit tests/fixtures/audit/implementation-coupled/ for implementation-coupled."` — 2 findings, 1 negative.
10. `"Audit tests/fixtures/audit/presentation-coupled/ for presentation-coupled."` — 2 findings, 1 negative.
11. `"Audit tests/fixtures/audit/conditional-logic/ for conditional-logic."` — 2 findings, 1 negative.
12. `"Audit tests/fixtures/audit/mystery-guest/ for mystery-guest."` — 2 findings, 1 negative.
13. `"Audit tests/fixtures/audit/rotten-green/ for rotten-green."` — 2 findings, 1 negative.

### Per-file smells (batch assessor)

14. `"Audit tests/fixtures/audit/shared-state/ for shared-state."` — 2 findings, 2 negatives.
15. `"Audit tests/fixtures/audit/monolithic-test-file/ for monolithic-test-file."` — 1 finding, 1 negative.

### Cross-suite smells (cross-suite assessor)

16. `"Audit tests/fixtures/audit/semantic-redundancy/ for semantic-redundancy."` — 1 cross-file redundancy finding, 1 negative.
17. `"Audit tests/fixtures/audit/wrong-level/ for wrong-level."` — 2 findings, 1 negative.

## Troubleshooting

**The skill emits a finding but the rationale is vague.** The canonical entry's *False-positive guards* section exists to prevent this. If the skill cannot cite a specific signal from the entry's *Signals* section, the finding should not have emitted — reconsider. See the [taxonomy entry](taxonomy/README.md) for the slug.

**The skill misses a finding.** Re-read the canonical entry (`taxonomy/<slug>.md`). If the missed case is not covered by any signal, that is a manifesto gap, not a skill bug — raise it as a PR to the canonical entry.

**Cross-suite findings seem wrong.** The cross-suite assessor must perform targeted source reads before confirming. If it is emitting findings based only on behavior-summary clustering, that is a bug — summaries are an index for candidate detection, not evidence.

**The audit launches too many batches.** Provide your context window size in the invocation to avoid conservative sharding at the 200K floor.
