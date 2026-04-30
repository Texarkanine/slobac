# SLOBAC audit skill

An [AgentSkills.io](https://agentskills.io/)-shaped skill that audits a test suite against the [SLOBAC manifesto](https://github.com/Texarkanine/slobac) and emits a portable markdown report. Supports 6 smells across 3 detection scopes, with multi-agent orchestration for suites of any size.

This is the **canonical source** for the skill. The layout is harness-agnostic; the install step per harness is described below.

## Supported Smells

| Slug | Detection Scope | Description |
|------|----------------|-------------|
| `deliverable-fossils` | per-test, cross-suite | Tests named after sprint artifacts, not product behavior |
| `naming-lies` | per-test | Test title claims X; body verifies Y |
| `shared-state` | per-file | Module-level mutables leaked across test boundaries |
| `monolithic-test-file` | per-file | Single file mixing 5+ behavior domains |
| `semantic-redundancy` | cross-suite | Same behavior tested N times across files |
| `wrong-level` | cross-suite | Test at wrong pyramid tier vs. directory convention |

## Architecture

The audit orchestrates three sibling skills as subagents:

```
slobac-audit (orchestrator)
  ├── slobac-scout → Suite Manifest (file inventory + sizes + tier conventions)
  ├── slobac-batch (×1 or ×N) → Findings + Behavior Summaries
  └── slobac-cross-suite → Cross-Suite Findings (if cross-suite smells in scope)
```

**For small suites** (fitting in one context budget): the orchestrator launches 1 scout + 1 batch assessor. Functionally identical to a single-agent audit — the orchestration is invisible.

**For large suites** (exceeding one context budget): the orchestrator partitions files into N batches, launches batch assessors in parallel, merges their behavior summaries, and optionally launches the cross-suite assessor for cross-file smell detection.

The behavior summary — a one-sentence-per-test intermediate representation — is the compression layer between batch assessors and the cross-suite assessor. This implements the manifesto's [describe-before-edit](https://texarkanine.github.io/slobac/principles/#behavior-articulation-before-change) principle as an architectural boundary.

## Layout

```
skills/slobac-audit/
├── SKILL.md                              # orchestrator workflow
├── README.md                             # this file
└── references/
    ├── report-template.md                # audit report shape
    ├── behavior-summary-format.md        # IR spec for cross-suite assessor
    ├── suite-manifest-format.md          # scout output spec
    └── docs/                             # the full SLOBAC manifesto
        ├── .pages                        # properdocs nav ordering
        ├── index.md                      # site landing page
        ├── principles.md                 # test principles + governor rules
        ├── glossary.md                   # shared terminology + citations
        ├── workflows.md                  # RED-GREEN-MUTATE-KILL-REFACTOR cycle
        └── taxonomy/
            ├── README.md                 # taxonomy shape SoT + entry catalog
            ├── deliverable-fossils.md    # canonical smell definition
            ├── naming-lies.md            # canonical smell definition
            └── ... (13 more entries)     # canonical smell definitions

skills/slobac-scout/                      # sibling: suite enumeration
├── SKILL.md
├── README.md
└── references/
    └── exploration-commands.md           # shell command templates

skills/slobac-batch/                      # sibling: per-test + per-file assessment
├── SKILL.md
└── README.md

skills/slobac-cross-suite/                # sibling: cross-suite assessment
├── SKILL.md
└── README.md
```

### Cross-skill reference convention

All shared references (taxonomy entries, format specs, manifesto docs) live in `slobac-audit/references/`. Sibling skills reach in via `../slobac-audit/references/...`. No sibling skill reaches into another sibling — the reference flow is unidirectional into `slobac-audit`.

## Install

The skill is discoverable by any harness that understands an AgentSkills.io-shaped `SKILL.md`. Install the orchestrator (`slobac-audit`) and all three sibling skills so the orchestrator can dispatch them.

### Cursor

Cursor discovers skills under `.cursor/skills/` (repo-level) or `~/.cursor/skills/` (user-level). To make the audit available in the current checkout:

```bash
for skill in slobac-audit slobac-scout slobac-batch slobac-cross-suite; do
  ln -s "$PWD/skills/$skill" ".cursor/skills/$skill"
done
```

To make it available across all projects:

```bash
for skill in slobac-audit slobac-scout slobac-batch slobac-cross-suite; do
  ln -s "$PWD/skills/$skill" "$HOME/.cursor/skills/$skill"
done
```

### Claude Code

Claude Code discovers skills under `.claude/skills/` (repo-level) or `~/.claude/skills/` (user-level). The install pattern mirrors Cursor:

```bash
for skill in slobac-audit slobac-scout slobac-batch slobac-cross-suite; do
  ln -s "$PWD/skills/$skill" ".claude/skills/$skill"
done
```

### Other harnesses

If your harness supports the AgentSkills.io shape, point its skill loader at all four skill directories. The `SKILL.md` frontmatter (`name`, `description`) and the `references/` subtree follow the standard convention; no harness-specific glue is required.

## Invoke

Natural language. Examples:

- "Audit the tests under `src/tests/` for SLOBAC smells."
- "Check `tests/unit/` for naming-lies."
- "Run the SLOBAC audit over this suite for fossils."
- "Which tests have titles that don't match their bodies?"
- "Check `tests/` for shared state and redundant tests."
- "Audit `tests/` for all smells — 1M context window."

The skill scopes the audit from the phrasing, orchestrates subagents as needed, and writes `slobac-audit.md` in the current working directory. Pass a different path explicitly if wanted:

- "Audit `src/tests/` and write the report to `reports/audit-2026-04.md`."

### Context window guidance

**For best results, run SLOBAC with your largest available model and context window.** In Cursor, enable MAX mode. In Claude Code, use Opus or Sonnet with the 1M context window. Larger context means fewer batches, richer cross-suite analysis, and better recall on redundancy detection. SLOBAC will work at 200K context, but will shard more aggressively — trading recall on cross-suite smells for safety.

You can tell the orchestrator your context window size in the invocation: "Audit tests/ — 1M context window." This avoids the one-time question the orchestrator asks when it encounters a large suite without a stated budget.

## Smoke test

The repo ships fixture suites under [`tests/fixtures/audit/`](https://github.com/Texarkanine/slobac/tree/main/tests/fixtures/audit) with documented expected findings. Use them to verify the install:

### Per-test smells (batch assessor)

1. **"Audit `tests/fixtures/audit/deliverable-fossils/` for fossils."** — Compare against `expected-findings.md`. 4 findings, 1 negative example.
2. **"Audit `tests/fixtures/audit/naming-lies/` for naming-lies."** — Compare against `expected-findings.md`.
3. **"Audit `tests/fixtures/audit/both-smells/` for all smells."** — Exercises scope honoring with mixed smells.
4. **"Audit `tests/fixtures/audit/clean/`."** — Expect no findings.

### Per-file smells (batch assessor)

5. **"Audit `tests/fixtures/audit/shared-state/` for shared-state."** — 2 findings (module-level mutables), 2 negative examples.
6. **"Audit `tests/fixtures/audit/monolithic-test-file/` for monolithic files."** — 1 finding (`test_everything.py`), 1 negative (`test_parser_thorough.py`).

### Cross-suite smells (cross-suite assessor)

7. **"Audit `tests/fixtures/audit/semantic-redundancy/` for redundant tests."** — 1 cross-file redundancy finding, 1 negative (`test_contract_keys.py`).
8. **"Audit `tests/fixtures/audit/wrong-level/` for wrong-level."** — 2 findings (unit with integration behavior, integration with unit behavior), 1 negative (`test_calculator.py`).

Phrasing of the emitted report need not be byte-identical to `expected-findings.md` — the shape contract is that every expected finding is emitted with its correct smell slug, remediation arm, and a rationale that cites the canonical docs entry. Divergence beyond that is a bug in the skill, not the fixture.

## Scope and non-goals

- **6 smells supported.** Any request for other smells (`tautology-theatre`, `vacuous-assertion`, etc.) is refused with a clear message — the audit never silently skips a requested smell.
- **The audit is read-only.** It does not modify test code. Applying a recommendation from the report is a separate step (today manual; automated apply is a future capability).
- **Python is the only validated ecosystem.** The detection prose is language-neutral; the manifesto's Polyglot notes describe per-ecosystem detection surface. Validation on JS/TS, Ruby, JVM, etc. is future work.

## Troubleshooting

- **The skill emits a finding but the rationale is vague.** The canonical entry's False-positive guards section exists specifically to prevent this. If the skill cannot cite a specific signal from the Signals section, the finding should not emit — reconsider.
- **The skill misses a finding.** Re-read the canonical entry (`references/docs/taxonomy/<slug>.md`). If the missed case is not covered by any signal, that is a manifesto gap, not a skill bug — raise it as a PR to the canonical entry.
- **Cross-suite findings seem wrong.** The cross-suite assessor must perform targeted source reads before confirming. If it's emitting findings based only on behavior summary clustering, that's a bug — summaries are an index for candidate detection, not evidence.
- **The audit launches too many batches.** Provide your context window size in the invocation to avoid conservative sharding at the 200K floor.
