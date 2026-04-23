# SLOBAC — product brief (draft)

**Status:** draft v1. Purpose: align on what SLOBAC *is*, who it's for, and what the first shipped thing looks like, before we get technical about implementation.

**Name:** SLOBAC — **S**uite-**L**ife **O**f **B**obs **A**nd **C**ode.

> The joke is that the Bobs from Office Space ask "what would you say you *do* here?" to the tests.
> The suite life refers to test suites.
> The whole construction is a riff on "sweet life of bob and cody," but code is cod-e, the code we wrote.

---

## 1. What SLOBAC is

SLOBAC has three coupled deliverables. They layer: each one is useful on its own, and each subsequent one depends on the previous.

### 1.1 A manifesto

The [`docs/`](../docs/) tree is the manifesto — **what tests should be, what test suites should be, and the taxonomy of how they go wrong.** Users engage with SLOBAC by being educated into this view; a user who doesn't understand why their test is in the catalog will push back on the tool's recommendations for the wrong reasons. Composed of:

- [`docs/principles.md`](../docs/principles.md) — properties of good tests and principles of disciplined test-suite refactoring.
- [`docs/taxonomy/`](../docs/taxonomy/) — the smell catalog: one entry per named failure mode, each with signals, a prescribed fix, and a worked example.
- [`docs/glossary.md`](../docs/glossary.md) — shared terminology.
- [`docs/workflows.md`](../docs/workflows.md) — the cycles (notably RED-GREEN-MUTATE-KILL-REFACTOR) the manifesto assumes.

The manifesto ships as a self-contained read. A user with no intention of ever running the audit capability should still be able to come away with a clearer picture of what their suite should look like.

### 1.2 An audit capability

Given a codebase with tests, SLOBAC audits the suite against the manifesto and produces a portable report of the form:

> *"Test `foo` at `tests/bar.py:42` exhibits the [deliverable-fossils] smell because its name references the gone sprint label `M3-5`; it should be remediated by renaming it to encode the behavior `rejects trailing JSON garbage`."*

Audit is the primary deliverable. It is intentionally **portable**: the output is a human-readable report the user can act on by hand, hand to another agent, ignore, or share on a PR. The audit does not touch the code.

Implementation: prompts for LLMs, packaged as mainstream agentic-coding-harness primitives — **Skills and Sub-Agents.** Any harness that supports those primitives is a valid host.

Scope control: the user chooses which subset of the taxonomy to audit against. Default is the full taxonomy — "tell me everything wrong with my suite" is the usual ask. Scoping down to, say, "just the tautology-theatre and rotten-green smells" is supported.

### 1.3 An apply capability

A thin secondary layer that takes an audit's recommendations and executes them against the codebase, with rigor/guardrails appropriate to the "messing with a test suite" job. Expected to be much lighter than the audit layer — most of the judgment has already been baked into the audit's recommendations; apply mostly needs to mechanically perform the change, verify it did not regress, and land a commit per edit.

Implementation: further Skills/Sub-Agents layered on the audit output. Specific guardrail mechanics are a design question (see §5).

Scope control: the user chooses which subset of the audit to apply. Default is "apply all". It should be equally natural to say "apply only the renames" or "skip the deletions" or "apply smells A and B but not C."

## 2. What SLOBAC is not

- Not a SaaS dashboard.
- Not a linter — repos pick their own.
- Not a mutation engine, codemod runner, or test generator — all mature; if SLOBAC ever calls any, it is as an orchestrated tool, not as an implementation.
- Not a smell-count scoreboard. The EMSE 2023 "Test Smells 20 Years Later" finding is load-bearing: optimizing for raw smell counts is explicitly anti-goal, and already called out as such in [`docs/taxonomy/README.md`](../docs/taxonomy/README.md).
- Not opinionated about *which* agentic harness the user runs. Skills and Sub-Agents are the target packaging; any harness that supports those is valid.

## 3. Who it's for

The primary user is the maintainer of a mature test suite that has accumulated six to sixty months of [deliverable-fossil](../docs/taxonomy/deliverable-fossils.md) drift — tests named per gone checklists, files sized per gone tickets, assertions written per gone acceptance criteria. They do not want a new test generator. They want an adult in the room to walk the existing suite and tell them, in plain English, what's wrong and what to do about it.

Secondary users:

- New joiners trying to read the suite as a spec.
- Tech leads running quarterly suite-health reviews.
- Teams preparing a codebase for handoff.
- Anyone who wants to read the manifesto and self-audit by hand.

## 4. Phased delivery

Each phase is a shippable milestone. A user should be able to stop at phase N and get value without phase N+1.

### Phase 0 — Manifesto

**Ship:** the [`docs/`](../docs/) tree, as-is, as a self-contained reference.

**Value:** a reader can learn the principles, adopt the vocabulary, and audit their own suite by hand. No software required.

### Phase 1 — Audit MVP (one smell)

**Ship:** an audit Skill/Sub-Agent bundle that detects one taxonomy entry and emits a portable recommendation report for it.

**First smell:** [`deliverable-fossils`](../docs/taxonomy/deliverable-fossils.md). It's the highest-visibility, highest-reader-value smell; the audit output ("rename this, because the body verifies Y not X") is self-explanatory; and the detection signals are syntactic enough to prototype quickly.

**Value:** a user installs the bundle, points it at their suite, and gets back a markdown (or similar) report saying which tests are fossils and what each should be renamed to. They can take it anywhere.

### Phase 2 — Audit coverage

**Ship:** audit Skills/Sub-Agents for the remaining taxonomy entries, prioritized by reviewer-value × detection-cost. Expected rough order: tautology-theatre, rotten-green, vacuous-assertion, pseudo-tested, semantic-redundancy, wrong-level, naming-lies, presentation-coupled, over-specified-mock, implementation-coupled, conditional-logic, shared-state, mystery-guest, monolithic-test-file. Order is not load-bearing.

**Value:** full-catalog audit. The user can now get a complete suite-health report against the manifesto.

### Phase 3 — Apply MVP (one smell)

**Ship:** a thin apply layer that consumes Phase 1's audit output and applies the recommended renames with guardrails (per-edit commit, rationale in commit message, verification that the transform didn't break anything).

**First smell:** [`deliverable-fossils`](../docs/taxonomy/deliverable-fossils.md) again — narrowed further to rename-only. This is the safest transform in the catalog (call graph unchanged; only the test identifier changes) and validates the apply pattern on the lowest-risk surface.

**Value:** the user can run audit → apply end-to-end for fossil-named tests.

### Phase 4 — Apply coverage

**Ship:** apply layers for the remaining taxonomy entries, in roughly the order apply-risk allows. Likely order: Critical-severity deletions (tautology-theatre, rotten-green) before rewrites (vacuous-assertion, pseudo-tested) before structural moves (semantic-redundancy, wrong-level, deliverable-fossils Phase B regroup, monolithic-test-file).

**Value:** apply parity with audit. The user can run the full loop for any subset they choose.

### Phase 5 — Distribution polish

**Ship:** packaging for multiple agentic-coding harnesses. Which harnesses, and in what order, is a later decision.

**Value:** SLOBAC is a one-command install in whatever harness the user already runs.

## 5. Open questions

Things that shape Phase 1+ and that we haven't yet decided:

1. **Audit output format.** Markdown report? Structured JSON? Both (markdown for readers, JSON for the apply layer)? This decides the audit-to-apply handoff shape.
2. **Audit report persistence.** Transient chat output, or a committed artifact at e.g. `slobac-audit.md`? The committed-artifact version is more portable and re-reviewable; the transient version is simpler.
3. **Subset-selection UX.** How does the user say "audit against only these five smells"? Skill argument? CLI flag? Naming convention?
4. **Apply guardrail shape.** Per-edit commit is the obvious default; what additional verification does apply perform (re-run tests? coverage check? mutation check? just compile?)? This ties back to the [preservation principle](../docs/principles.md#preservation-of-regression-detection-power) but the specific implementation is open.
5. **Skill granularity.** One Skill per smell, one Skill per fix-shape, or one Skill per audit-stage (scan / triage / recommend)? Leaning per-smell for audit (each smell has distinct detection logic and recommendation template), per-fix-shape for apply (rename, delete, strengthen, split, relocate, annotate are a shared vocabulary).
6. **Harness target order.** Which agentic harness gets first-class packaging in Phase 1? Claude Code Skills are the shape most clearly in the brief; Cursor, Copilot, Cline, Continue, Zed all support adjacent primitives with varying fidelity.
7. **License.** Prior draft proposed AGPL-3.0 on the grounds that the copyleft slot is empty in the research-surveyed prior art. Open until confirmed.
8. **Name for the audit report artifact.** `slobac-audit.md`? Something else? Minor, but the user sees it.

## 6. Success criteria

Per the [principles](../docs/principles.md), none of these are smell counts.

### Manifesto (Phase 0)

- **Reader comprehension.** A user who reads the manifesto end-to-end can correctly classify several real tests from their own suite against the taxonomy. Evaluated by asking them.

### Audit (Phases 1–2)

- **Recommendation precision.** Of the smells the audit flags, what fraction a reviewer accepts as real. (Complement: what fraction are false positives.)
- **Recommendation actionability.** Of the recommendations the audit emits, what fraction a reviewer accepts as the right fix. A correct diagnosis with a wrong remedy is a partial failure.
- **Portability.** Can a user hand the audit report to a different agent (or a human) and have them execute it faithfully without rereading the manifesto? A self-contained report is the goal.

### Apply (Phases 3–4)

- **Preservation.** [Regression-detection power](../docs/principles.md#preservation-of-regression-detection-power) is not reduced — hard gate.
- **Commit review acceptance.** Fraction of per-edit commits that reviewers merge without edits to the rationale paragraph.
- **Round-trip parity.** What the apply layer produces matches what the audit recommended, without drift.

### Anti-signals (do not optimize)

- Raw test count (up or down).
- Coverage percentage (can legitimately drop when tautologies are deleted — [principles § preservation](../docs/principles.md#preservation-of-regression-detection-power) already frames the acceptable case).
- Smell count as a KPI.

## 7. Positioning

SLOBAC is two tools wrapped around a manifesto.

- **The manifesto** is the opinion: here's what tests should be, here's what they become without care, here's what to do about it.
- **The audit** is the portable second opinion: here's what's wrong with *your* suite, specifically, and what each fix would look like.
- **The apply** is the light assistant: here's the audit, executed with rigor.

The audit is the load-bearing piece. The manifesto stands without the audit; the apply does not stand without the audit.
