# What is SLOBAC?

The **Suite Life of Bobs and Code** is a point of view about what tests should be, what test suites should be, and the named ways both go wrong.

SLOBAC ships several things:

1. A Manifesto: a **self-contained read**. No software is required to use it. A reader who finishes these pages should be able to audit their own test suite by hand and classify real tests against the named failure modes.
    1. [Principles](principles/test-qualities.md) — what a test *should* be, and the bounds a disciplined test-suite refactor must respect.
    2. [Taxonomy](taxonomy/README.md) — a catalog of ways tests and test suites can go wrong.
2. An [Agent Skill](using-slobac.md): Instructions for AI agents to audit a codebases's test suite against the manifesto.

## What This Is Not

- Not a linter. Where existing ecosystem tools already lint syntactically, SLOBAC defers.
- Not a mutation engine, codemod runner, or test generator — those are mature; SLOBAC orchestrates them, never reimplements.
- Not a smell-count scoreboard. Optimizing for raw smell counts is an explicit anti-goal ([Panichella et al., *Test Smells 20 Years Later*, EMSE 2023](https://link.springer.com/article/10.1007/s10664-022-10207-5)).

## How To Start

1. Read the manifesto:
    - **[Principles](principles/test-qualities.md)** — what a test *should* be, and the bounds a disciplined test-suite refactor must respect. This is the vocabulary every other page cites.
    - **[Workflows](principles/workflows.md)** — the RED-GREEN-MUTATE-KILL-REFACTOR cycle that the taxonomy's prescribed fixes assume. You *are* doing [mutation testing](https://en.wikipedia.org/wiki/Mutation_testing), right? No? Ah, well, you can still use SLOBAC, no worries.
    - **[Taxonomy](taxonomy/README.md)** — the catalog of named failure modes, one entry per smell. Start with `taxonomy/README.md` for the curated reading order across the 15 entries; each entry is a standalone page you can jump to directly.
    - **[Glossary](principles/glossary.md)** — definitions and citations for terms the other pages rely on (mutation testing, kill-sets, tautology theatre, canonical location, etc.).
2. Install the audit skill:
    - **[Running the SLOBAC audit](using-slobac.md)** — instructions for installing and invoking the audit skill.
3. Have your AI agents audit your test suite: `/slobac-audit` and it'll walk you through the process.
