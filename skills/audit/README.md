# SLOBAC audit skill

An [AgentSkills.io](https://agentskills.io/)-shaped skill that audits a test suite against the [SLOBAC manifesto](https://texarkanine.github.io/slobac/) and emits a portable markdown report. For install instructions, invocation examples, and troubleshooting, see **[Using the SLOBAC audit](https://texarkanine.github.io/slobac/using-slobac/)** on the published site.

This file is **contributor documentation** — architecture, layout, and smoke-test verification.

## Licensing (standalone bundle)

This skill ships `LICENSES/` and `REUSE.toml` so a marketplace or tarball install is REUSE-valid without the monorepo root. From this directory, run `reuse --root . lint` to verify (nested Git checkouts otherwise lint from the repository root unless `--root` is set).

## Architecture

The audit orchestrator dispatches three subagent workflows from `references/subagents/`:

```
slobac-audit (orchestrator — SKILL.md)
  ├── scout subagent → Suite Manifest (file inventory + sizes + tier conventions)
  ├── batch subagent (×1 or ×N) → Findings + Behavior Summaries
  └── cross-suite subagent → Cross-Suite Findings (if cross-suite smells in scope)
```

Subagent workflows are raw prompt documents (not registered skills). The orchestrator reads `references/subagents/<name>.md` and launches a readonly subagent whose task is that file's content, supplemented with runtime context variables.

**For small suites** (fitting in one context budget): the orchestrator launches 1 scout + 1 batch assessor. Functionally identical to a single-agent audit — the orchestration is invisible.

**For large suites** (exceeding one context budget): the orchestrator partitions files into N batches, launches batch assessors in parallel, merges their behavior summaries, and optionally launches the cross-suite assessor for cross-file smell detection.

The behavior summary — a one-sentence-per-test intermediate representation — is the compression layer between batch assessors and the cross-suite assessor. This implements the manifesto's [describe-before-edit](https://texarkanine.github.io/slobac/principles/#behavior-articulation-before-change) principle as an architectural boundary.

## Layout

```
skills/audit/
├── SKILL.md                              # orchestrator workflow
├── README.md                             # this file
└── references/
    ├── report-template.md                # audit report shape
    ├── behavior-summary-format.md        # IR spec for cross-suite assessor
    ├── suite-manifest-format.md          # scout output spec
    ├── subagents/                        # raw subagent workflow prompts
    │   ├── README.md                     # dispatch contract documentation
    │   ├── scout.md                      # suite enumeration workflow
    │   ├── batch.md                      # per-test + per-file assessment workflow
    │   ├── cross-suite.md                # cross-suite assessment workflow
    │   └── exploration-commands.md       # shell command templates (used by scout)
    └── docs/                             # the full SLOBAC manifesto + published site
        ├── .pages                        # properdocs nav ordering
        ├── index.md                      # site landing page
        ├── principles.md                 # test principles + governor rules
        ├── glossary.md                   # shared terminology + citations
        ├── workflows.md                  # RED-GREEN-MUTATE-KILL-REFACTOR cycle
        ├── using-slobac.md               # install, invoke, troubleshooting (end-user)
        └── taxonomy/
            ├── README.md                 # taxonomy shape SoT + entry catalog
            ├── deliverable-fossils.md    # canonical smell definition
            ├── naming-lies.md            # canonical smell definition
            └── ... (13 more entries)     # canonical smell definitions
```

### Reference convention

All shared references (taxonomy entries, format specs, manifesto docs, subagent workflows) live under `audit/references/`. The orchestrator reads subagent workflows from `references/subagents/` and passes the absolute `references/` path to subagents so they can resolve taxonomy entries and format specs at runtime.

## Smoke test

The repo ships fixture suites under [`tests/fixtures/audit/`](https://github.com/Texarkanine/slobac/tree/main/tests/fixtures/audit) with documented expected findings. Use them to verify the install.

Phrasing of the emitted report need not be byte-identical to `expected-findings.md` — the shape contract is that every expected finding is emitted with its correct smell slug, remediation arm, and a rationale that cites the canonical docs entry. Divergence beyond that is a bug in the skill, not the fixture.

### Per-test smells (batch assessor)

1. **"Audit `tests/fixtures/audit/deliverable-fossils/` for deliverable-fossils."** — 4 findings, 1 negative.
2. **"Audit `tests/fixtures/audit/naming-lies/` for naming-lies."** — Compare against `expected-findings.md`.
3. **"Audit `tests/fixtures/audit/both-smells/` for all smells."** — Exercises scope honoring with mixed smells.
4. **"Audit `tests/fixtures/audit/clean/`."** — Expect no findings.
5. **"Audit `tests/fixtures/audit/tautology-theatre/` for tautology-theatre."** — 2 findings (mock-tautology, mock-of-SUT), 1 negative; remediation **delete**.
6. **"Audit `tests/fixtures/audit/pseudo-tested/` for pseudo-tested."** — 2 findings (no-op SUT replacement survives), 1 negative.
7. **"Audit `tests/fixtures/audit/vacuous-assertion/` for vacuous-assertion."** — 2 findings (`is not None`, truthy field), 1 negative.
8. **"Audit `tests/fixtures/audit/over-specified-mock/` for over-specified-mock."** — 2 findings (over-specified interactions, internal-detail testing), 1 negative.
9. **"Audit `tests/fixtures/audit/implementation-coupled/` for implementation-coupled."** — 2 findings (private dict access, private helper call), 1 negative.
10. **"Audit `tests/fixtures/audit/presentation-coupled/` for presentation-coupled."** — 2 findings (full-string HTML, long `in`-chain), 1 negative.
11. **"Audit `tests/fixtures/audit/conditional-logic/` for conditional-logic."** — 2 findings (`if cond: assert(...)`, `try/except` without trailing `pytest.fail`), 1 negative.
12. **"Audit `tests/fixtures/audit/mystery-guest/` for mystery-guest."** — 2 findings (magic count from external CSV, fixture-coupled magic number), 1 negative.
13. **"Audit `tests/fixtures/audit/rotten-green/` for rotten-green."** — 2 findings (empty body with TODO, `print` instead of assertion), 1 negative.

### Per-file smells (batch assessor)

14. **"Audit `tests/fixtures/audit/shared-state/` for shared-state."** — 2 findings (module-level mutables), 2 negative examples.
15. **"Audit `tests/fixtures/audit/monolithic-test-file/` for monolithic-test-file."** — 1 finding (`test_everything.py`), 1 negative (`test_parser_thorough.py`).

### Cross-suite smells (cross-suite assessor)

16. **"Audit `tests/fixtures/audit/semantic-redundancy/` for semantic-redundancy."** — 1 cross-file redundancy finding, 1 negative (`test_contract_keys.py`).
17. **"Audit `tests/fixtures/audit/wrong-level/` for wrong-level."** — 2 findings (unit with integration behavior, integration with unit behavior), 1 negative (`test_calculator.py`).
