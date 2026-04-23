# The SLOBAC manifesto

Welcome. This is the manifesto for **SLOBAC** — *Suite-Life Of Bobs And Code* — a point of view about what tests should be, what test suites should be, and the named ways both go wrong.

The manifesto ships as a **self-contained read**. No software is required to use it. A reader who finishes these pages should be able to audit their own test suite by hand and classify real tests against the named failure modes. Whether SLOBAC later ships an audit capability on top of this manifesto is a separate question — the manifesto stands on its own.

## How to read the manifesto

Roughly in this order, though every page cross-links the others:

- **[Principles](principles.md)** — what a test *should* be, and the bounds a disciplined test-suite refactor must respect. This is the vocabulary every other page cites.
- **[Workflows](workflows.md)** — the RED-GREEN-MUTATE-KILL-REFACTOR cycle that the taxonomy's prescribed fixes assume. Short, but load-bearing — fix steps reference it by name.
- **[Taxonomy](taxonomy/README.md)** — the catalog of named failure modes, one entry per smell. Start with `taxonomy/README.md` for the curated reading order across the 15 entries; each entry is a standalone page you can jump to directly.
- **[Glossary](glossary.md)** — definitions and citations for terms the other pages rely on (mutation testing, kill-sets, tautology theatre, canonical location, etc.).

## What this is not

- Not a linter. Where existing ecosystem tools already lint syntactically, SLOBAC defers.
- Not a mutation engine, codemod runner, or test generator — those are mature; SLOBAC orchestrates them, never reimplements.
- Not a smell-count scoreboard. Optimizing for raw smell counts is an explicit anti-goal ([Panichella et al., *Test Smells 20 Years Later*, EMSE 2023](https://link.springer.com/article/10.1007/s10664-022-10207-5)).

Ready? Start with **[Principles](principles.md)**.
