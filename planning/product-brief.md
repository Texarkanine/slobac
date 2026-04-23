# SLOBAC — product brief (draft)

**Status:** draft v0. Purpose: align on what SLOBAC *is*, who it's for, and what the
first shipped thing looks like, before we get technical about implementation.

**Name:** SLOBAC — **S**uite-**L**ife **O**f **B**obs **A**nd **C**ode.

> The joke is that the Bobs from Office Space ask "what would you say you do here" to the tests.
> The suite life refers to test suites.
> The whole constructrion is a riff on "sweet life of bob and cody," but code is cod-e, the code we wrote.

---

## 1. What SLOBAC is

**SLOBAC is a collection of agentic-coding-harness customizations** — skills, rules,
subagents, and an MCP server — that the user installs into Claude Code / Cursor /
Copilot / Continue / Cline / Zed, then turns loose on their test suite. Each pass
produces a **small, reviewable set of behavior-preserving edits** plus a **per-edit
prose rationale**.

It is explicitly *not*:

- A SaaS dashboard.
- A linter (repos pick their own).
- A mutation engine, codemod runner, or test generator (all mature; SLOBAC
  orchestrates them).
- A smell-count scoreboard. The research `report.md` and the EMSE 2023 paper make
  the case against TsDetect-shaped KPIs; SLOBAC tracks preserved mutation kills and
  reviewer-accepted edits instead.

It *is*:

- A **catalog** — `docs/taxonomy/` — of articulable, fixable, polyglot test-smell
  classes, each with one prescribed fix shape.
- A set of **skills** (one per taxonomy entry) that encode the detection heuristic,
  the describe-before-edit prompt, and the safe-transform recipe.
- A **validator / filter chain** borrowed from Meta's TestGen-LLM: every proposed
  edit must compile, pass N times, not AST-duplicate an existing test, and not
  regress coverage or mutation kill-set.
- A **rationale layer**: every edit produces a one-paragraph prose commit message
  that is the actual deliverable. Reviewers read rationales; the diff is proof.
- An **MCP server** wrapping ecosystem tools (Stryker, mutmut, PIT, cargo-mutants,
  Ruff, eslint-plugin-jest, rubocop-rspec, testifylint, ast-grep, LibCST,
  jscodeshift) so the skills can act without the user orchestrating every CLI.

## 2. Who it's for

The primary user is a maintainer of a mature test suite that has accumulated six to
sixty months of deliverable-fossil drift — tests named per gone checklists, files
sized per gone tickets, assertions written per gone acceptance criteria. They do not
want a new test generator. They want an adult in the room to walk the existing suite
and propose a diff.

Secondary users: new joiners trying to read the suite as a spec; tech leads running
quarterly suite-health reviews; teams preparing a codebase for handoff.

## 3. What SLOBAC *produces* per pass

Each pass yields three artifacts:

1. **`plan.md`** — findings grouped by taxonomy class, each with locus, proposed
   move, and preservation requirements.
2. **Per-edit commits** — one transform per commit, each with the rationale in the
   commit body. Commits are independently reviewable and revertable.
3. **Suite changelog** — renames/moves/deletions listed so reviewers can answer
   "where did `test_foo` go?" without running `git log -S`.

The rationale layer is the moat. Meta hit 73% acceptance at testathons with a raw
filter chain; SLOBAC aims higher because every proposed change ships with a
reviewable reason in prose.

## 4. Governor rules (non-negotiable)

Inherited from citypaul's refactoring skill, restated as SLOBAC invariants:

1. **Do not extract production code purely for testability.** DRY = knowledge, not
   code. Split SUT code for readability or real concern separation, never for "so we
   can unit test it."
2. **Do not dedupe tests that guard different knowledge.** Two tests that *look*
   similar but cover different requirements are not merged.
3. **Do not invent tests.** A pass that adds tests is a different pass (test
   generation); SLOBAC only improves or deletes existing ones.
4. **Do not reduce mutation kill-set.** Hard gate.
5. **Do not reduce coverage** without naming the absorber in the commit rationale.
6. **Cap edits per pass.** Prefer 10–30 reviewable moves. The next pass continues.

## 5. Phased delivery — each phase is a valuable MVP

Each phase stands on its own as a shippable product. A user should be able to install
phase N and get value without phase N+1.

### Phase 0 — Foundations (infrastructure, not user-facing)

What: the minimal shared spine that every later phase depends on.

- The taxonomy (this repo's `docs/taxonomy/`) as a stable reference.
- The **describe-before-edit** skill — for any test in scope, emit a one-sentence
  behavior docstring. Reusable across every other skill.
- The **filter-chain validator** — compile / pass-N / coverage Δ ≥ 0 / mutation Δ
  ≥ 0, per repo, hooked to whatever tools the repo has.
- The **rationale emitter** — per-edit commit formatter.
- An **MCP server skeleton** that exposes these primitives to the harness.

Value as shipped: a harness skill pack that, when installed, lets the user ask *"what
does this test actually verify?"* and get a reliable one-sentence answer plus a
docstring insert. No transforms yet. Useful on its own as a suite-literacy aid.

### Phase 1 — MVP: Deliverable Fossils (rename only)

What: the user's nominated headline smell, narrowed to its safest transform.

- Detect tests matching `docs/taxonomy/deliverable-fossils.md` signals.
- Propose **renames only** (Phase A of the fix recipe) — no file moves, no
  regrouping.
- Emit a per-test rationale: "Renamed X → Y because body verifies Z, not W."
- Filter chain: rename-only = AST-identical call graph; trivial to gate.

Value as shipped: a user installs SLOBAC, runs a pass, and gets a set of commits
that turn their fossilized test names into behavior statements. Deliverable Fossils
is the right first target because:

- High reader value (suite becomes readable as a spec even without regrouping).
- Lowest-risk transform in the catalog (rename only; call graph untouched).
- Mechanically simple validator.
- Directly exercises the describe-before-edit pipeline Phase 0 shipped.
- Forces us to figure out the "propose a behavior-shaped name" prompt, which every
  later phase reuses.

Scope **excluded** from phase 1 to keep it MVP:

- File moves (Phase B of deliverable-fossils).
- Any other taxonomy entry.
- Mutation-score gating (rename is behavior-preserving by construction).

### Phase 2 — Safe deletions: Tautology Theatre + Rotten Green

What: the highest-severity, lowest-risk transforms in the catalog.

- Detect AP1 / AP2 per `docs/taxonomy/tautology-theatre.md`.
- Detect rotten-green scaffolds per `docs/taxonomy/rotten-green.md`.
- Transform: **delete** (with rationale + coverage-gap note).
- Filter chain: mutation kill-set strictly unchanged (tautologies killed nothing;
  rotten green had no oracle).

Value as shipped: SLOBAC starts removing false-confidence tests with receipts. The
"coverage gap" note becomes a hand-off artifact for any separate test-generation
tooling the user runs.

### Phase 3 — Strengthen assertions: Vacuous + Pseudo-Tested

What: the first *content* edits — not rename, not delete, but actually rewriting
assertions.

- Detect vacuous oracles per `docs/taxonomy/vacuous-assertion.md`.
- Detect pseudo-tested SUTs per `docs/taxonomy/pseudo-tested.md` (LLM conjecture
  first; optional Descartes/mutmut `--simple` confirmation).
- Transform: strengthen the one canonical assertion so at least one previously
  surviving mutant dies.
- Filter chain: mutation kill Δ > 0. Hard pass.

Value as shipped: the suite starts actually catching bugs it previously whitewashed.
First phase where SLOBAC can claim to improve *test value*, not just hygiene.

### Phase 4 — The headline: Semantic Redundancy + Deliverable Fossils Phase B

What: cluster tests by behavior-sentence similarity; pick canonical; fold/delete;
regroup files per product capability.

- Implements `docs/taxonomy/semantic-redundancy.md` in full.
- Finishes the deliverable-fossils Phase B move (file relocation + suite TOC).
- Emits the **suite table-of-contents diff** as a reviewable artifact.
- Filter chain: full (compile, pass-N, AST dedup, coverage Δ ≥ 0, mutation Δ ≥ 0).

Value as shipped: the pitch lands. A long-rotted suite becomes a spec organized by
product behavior, with a generated TOC and rationale-per-move. This is the pass
that earns the "suite-as-spec" framing.

### Phase 5 — Fill the catalog

What: skills for the remaining taxonomy entries.

- `wrong-level` (codemod + runner-marker application).
- `over-specified-mock` (AP3/AP4).
- `implementation-coupled`.
- `conditional-logic`.
- `shared-state`.
- `mystery-guest`.
- `presentation-coupled`.
- `monolithic-test-file` (sequenced after phase 1 + phase 4 so splits use
  product vocabulary).

Value as shipped: full-breadth catalog coverage. Users can dispatch specific smells
on demand.

### Phase 6 — Harness polish and distribution

What: the install-anywhere play.

- Claude Code skill bundle with subagents (`inventory`, `diagnoser`, `proposer`,
  `validator`, `reporter`).
- Cursor rules file (rules + commands).
- Copilot custom instructions.
- Continue / Cline / Zed adapters (thin).
- The MCP server becomes the load-bearing piece; the rest are thin adapters.
- AGPL license (research says this is the empty slot).

Value as shipped: SLOBAC is a one-command install in every major agentic-coding
harness.

## 6. Open composition questions (to refine together)

These are left open for us to decide before phase 2 ships. Capturing so the
next draft pins them.

1. **One skill per smell, or one skill per fix shape?** Leaning "per smell" — the
   describe-before-edit prompt, signals, and rationale template vary meaningfully
   by mode. Fix shapes (rename / delete / strengthen / split / relocate) could be
   shared primitives the skills compose.
2. **Pass composition: N × (1-problem-fixer) or 1 × (N-problem-fixer)?** The
   phased roadmap above assumes the former — each phase adds a skill, each skill
   is runnable alone — which maximizes MVP value per phase. A composite
   "everything" runner is a later convenience, not a load-bearing mode.
3. **Priority queue across skills when multiple apply.** Initial proposal: severity
   × safety. Critical deletions first (tautology), then rename, then strengthen,
   then relocate. Re-evaluate against real-suite results after phase 2.
4. **How much of alf-test-design-reviewer do we absorb as a scoring oracle vs.
   reimplement?** Leaning: consume alf's JSON as a priority queue input when the
   user has it installed; do not require it.
5. **Pair-with vs. replace for adjacent tools.** Assume pair-with. The MCP server
   calls out to Stryker / mutmut / PIT / Ruff / etc.; we do not reimplement.

## 7. Success criteria (per shipped phase)

Per the research docs, none of these are smell counts.

- **Rationale acceptance rate.** % of proposed commits whose rationale paragraph
  survives review unedited.
- **Preserved mutation kill-set.** Hard gate; should be 100%.
- **Per-test behavior-docstring coverage.** Before vs. after, on touched files.
- **Reviewer-claimed suite readability** (qualitative; sample-reviewed).
- **Post-pass time-to-understand** for new joiners: can a stranger to the codebase
  find the test for behavior X in under a minute using the suite TOC? Applies from
  phase 4 onward.

Explicit anti-signals (do *not* optimize these):

- Raw test count (up or down).
- TsDetect-style smell counts.
- Coverage percentage (can legitimately drop when tautologies are deleted).

## 8. Name, license, positioning

- Name: SLOBAC. Acronym honored (`suite-life of bobs and code`); tagline optional
  ("let the bobs go").
- License: AGPL-3.0. Research `report.md` §6 identifies the copyleft slot as
  empty; going AGPL is uncontested positioning and aligns with the composition
  stance (we orchestrate MIT/Apache tools; our value is the rationale layer).
- Positioning: *"compose, don't buy"* — SLOBAC is the brain on top of a mature
  stack of hands.

---

## Appendix: references

- Taxonomy: `docs/taxonomy/`.
- Research: `planning/research/report.md`, `FINDINGS-{CLAUDE,CODEX,COMPOSER,GEMINI,GROK}.md`.
- Governor rules: citypaul's refactoring skill ([DRY = knowledge, not code](https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/refactoring/SKILL.md)).
- Filter chain: Alshahwan et al., *TestGen-LLM at Meta* (FSE 2024).
- Tautology Theatre vocabulary: [a4al6a/alf-test-design-reviewer](https://github.com/a4al6a/claude-code-agents/tree/main/alf-test-design-reviewer).
- RED-GREEN-MUTATE-KILL-REFACTOR: [citypaul's planning skill](https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/planning/SKILL.md).
