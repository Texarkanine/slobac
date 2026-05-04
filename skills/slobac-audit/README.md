# SLOBAC audit skill

An [AgentSkills.io](https://agentskills.io/)-shaped skill that audits a test suite against the [SLOBAC manifesto](https://texarkanine.github.io/slobac/) and emits a portable markdown report. For install instructions, invocation examples, and troubleshooting, see **[Using the SLOBAC audit](https://texarkanine.github.io/slobac/using-slobac/)** on the published site.

This file is **contributor documentation** — architecture, layout, and smoke-test verification.

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
