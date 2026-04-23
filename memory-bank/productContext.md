# Product Context

SLOBAC — **S**uite-**L**ife **O**f **B**obs **A**nd **C**ode — is a test-suite audit-and-remediation product for mature codebases. It has three layered deliverables: a **manifesto** (what tests should be and the taxonomy of how they go wrong), an **audit capability** (reports against the manifesto, portable and non-destructive), and an **apply capability** (executes audit recommendations with per-edit-commit rigor).

## Target Audience

**Primary:** Maintainers of mature test suites that have accumulated roughly six to sixty months of drift — tests named per gone sprint labels, tests that didn't break during a refactor but now point off into space, assertions written per gone acceptance criteria. They are not asking for a test generator; they want a disciplined second opinion that walks the existing suite and says, in plain English, what's wrong and what to do about it.

**Secondary:**

- New joiners trying to read an unfamiliar suite as a spec.
- Tech leads running quarterly suite-health reviews.
- Teams preparing a codebase for handoff.
- Practitioners who want to read the manifesto and self-audit by hand (no software required).

## Use Cases

1. **Self-education.** Read the manifesto end-to-end; adopt its vocabulary; audit a personal or team suite by hand. Ships as the `docs/` tree and stands alone as a reference.
2. **Full-suite audit.** Point the audit at a test suite and get back a portable report: per-test, per-smell recommendations with rationale, suitable for hand-execution, hand-off to another agent, a PR comment, or the bin.
3. **Scoped audit.** Run the audit against a chosen subset of the taxonomy (e.g., "only `tautology-theatre` and `rotten-green`") when a full sweep is more than the user wants.
4. **End-to-end remediation.** Hand the audit report to the apply capability, which executes the recommended transforms with guardrails (per-edit commit, rationale in commit message, non-regression verification).
5. **Scoped remediation.** Apply a user-chosen subset of the audit — e.g., "apply all renames, skip the deletions" — without re-running the audit.

## Key Benefits

- **Portability.** The audit output is a human-readable artifact. It is useful whether the user runs the apply capability, hand-executes the recommendations, hands them to another agent, or ignores them.
- **Non-destructive audit.** The audit never touches code. The decision to act always belongs to the user.
- **Semantic judgment, not syntactic counts.** SLOBAC explicitly does not compete with test-smell linters. It targets the subset of test-suite problems where an LLM's semantic judgment beats a linter's pattern-match.
- **Scoping throughout.** Both audit and apply default to "everything," but the user can dial down to any subset of smells at any point.
- **Harness-agnostic.** The target packaging is mainstream agentic-coding-harness primitives (Skills, Sub-Agents). Any host that supports those is a valid deployment.
- **Manifesto is standalone.** Phase 0 ships even if the audit never exists. A reader gets a clearer picture of what a suite should look like without installing anything.

## Success Criteria

Explicitly **not** smell counts. Success is measured per layer:

**Manifesto (Phase 0):**

- *Reader comprehension.* A reader can correctly classify real tests from their own suite against the taxonomy after reading the manifesto.

**Audit (Phases 1–2):**

- *Recommendation precision.* Fraction of flagged smells a reviewer accepts as real (complement: false-positive rate).
- *Recommendation actionability.* Fraction of proposed fixes a reviewer accepts as the right fix. A correct diagnosis with a wrong remedy is a partial failure.
- *Portability.* A user can hand the report to a different agent (or human) and have it executed faithfully without rereading the manifesto.

**Apply (Phases 3–4):**

- *Preservation of regression-detection power.* Hard gate. The suite's ability to catch real bugs must not regress.
- *Commit review acceptance.* Fraction of per-edit commits reviewers merge without edits to the rationale paragraph.
- *Round-trip parity.* Apply's output matches the audit's recommendation without drift.

## Key Constraints

**Scope exclusions (what SLOBAC is not):**

- Not a SaaS dashboard.
- Not a linter. Linting is covered by existing ecosystem tools; SLOBAC defers to whatever linter the repo uses.
- Not a mutation engine, codemod runner, or test generator. These are mature; if SLOBAC ever calls them, it is as an orchestrated tool, never as an implementation.
- Not a smell-count scoreboard. The EMSE 2023 *Test Smells 20 Years Later* finding is load-bearing: optimizing for raw smell counts is an explicit anti-goal.
- Not opinionated about which agentic harness the user runs.

**Anti-signals to actively avoid optimizing:**

- Raw test count (up or down).
- Coverage percentage — it may legitimately drop when tautologies are deleted.
- Smell counts as a KPI.

**Governor rules on any transform (from the manifesto's principles):**

- Knowledge-DRY, not syntactic-DRY.
- No extract-for-testability.
- No speculative code.
- Commit-before-refactor.
- A refactor must not reduce regression-detection power without a named absorber in the rationale.

**Open questions shaping scope** (tracked in `planning/VISION.md` §5, not yet decided): audit output format; report persistence (transient vs committed artifact); subset-selection UX; apply-layer verification depth; Skill granularity (per-smell vs per-fix-shape); first-class harness target; license; name for the audit artifact.
