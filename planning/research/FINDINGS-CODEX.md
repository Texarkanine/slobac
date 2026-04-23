# Findings: Polyglot Test Refactoring Failure Modes (Texarkanine Survey)

Date: 2026-04-22  
Scope: pure research, no code changes outside this memo.

## Goal

Identify test-suite failure modes that:

1. are genuinely wrong/suboptimal,
2. are fixable with clear strategy,
3. generalize across languages/frameworks.

Focus is explicitly on LLM-refactorable quality work (not deterministic lint orchestration).

## Inputs used

- `randommd/goodtests/report.md` (prior-art landscape and gap analysis)
- `randommd/goodtests/farley.md` (Dave Farley 8 properties)
- Greg Wright, "Ten Properties of Good Unit Tests" (first 8 properties emphasized)
- citypaul skills:
  - `test-design-reviewer` (Farley scoring + evidence-driven review format)
  - `refactoring` (DRY = knowledge, not code; refactor only when behavior-preserving and useful)
- a4al6a `alf-test-design-reviewer` prior art:
  - two-phase scoring (static signals + semantic review)
  - explicit "tautology theatre" taxonomy (mock tautology, mock-only tests, trivial tautologies, framework tests)
  - mock anti-pattern taxonomy AP1-AP4 (adds operational detection guidance across languages)
- Local workspace repos with `Texarkanine` remotes and nontrivial tests.

## Additional prior-art deltas from a4al6a

The `a4al6a/claude-code-agents` artifact materially strengthens this research in three ways:

1. **Better naming for valueless tests**  
   "Tautology theatre" is a strong umbrella term for tests that can pass independent of production behavior. This cleanly captures a category that generic lint rules miss.

2. **Operational polyglot detection patterns**  
   AP1-AP4 definitions (mock tautology, mock-only, over-specified interactions, testing internal details) include concrete framework-aware heuristics across Java/Python/JS/Go/C#. This is directly reusable in a polyglot pass engine.

3. **Evidence discipline**  
   Per-test-method signal collection and file:line-anchored evidence improve explainability and reviewer trust. This aligns well with the "per-edit rationale layer" requirement in this memo.

## Repos with meaningful test suites (sampled)

Rough test-file signal from local scan:

- `a16n` (~67)
- `jsonschema2md` (~47)
- `inquirerjs-checkbox-search` (~15)
- `bbill-tracker` (~12)
- `tab-yeet` (~10)
- `cursor-warehouse` (~10, with very large modules)
- `claude-code-action` (~10)
- `jekyll-mermaid-prebuild` (~10)
- `jekyll-auto-thumbnails` (~9)
- `jekyll-highlight-cards` (~8)
- `amazon-cpi` (~6)

## Concrete observed issues (cross-language sample)

### JS/TS

- `jsonschema2md/test/api.test.js`
  - Uses weak type assertion (`assert(result === Object(result))`) that says little about behavior.
  - Swallows cleanup failures with `console.log('leaving tmp dir dirty')`, risking hidden state leakage.
- `jsonschema2md/test/testUtils.js`
  - `fuzzy` helper falls back to full-string equality on mismatch; failure diagnostics are confusing and brittle.
- `inquirerjs-checkbox-search/src/__tests__/basic-functionality.test.ts`
  - Heavy `toContain` assertions against full terminal render text; copy/formatting changes break tests for non-behavioral reasons.
- `inquirerjs-checkbox-search/src/__tests__/async-behavior.test.ts`
  - Broad async matcher (`/loading|wait/i`) is under-specified and may pass incidentally.
- `bbill-tracker/test/unit/BitcoinBillDetector.test.js`
  - Dead setup (`mockApiClient`) and spying on SUT internals (`isFeePayment`, `isAmountValid`) increases implementation coupling.
- `tab-yeet/test/lib/formats.test.js`
  - Catalog lock test (`Object.keys(...).toEqual([...])`) is brittle to benign extension.
- `claude-code-action/test/create-prompt.test.ts`
  - Huge in-file fixture object drives many cases; high maintenance drag and noisy diffs.

### Python

- `cursor-warehouse/tests/test_sync.py`
  - Monolithic high-complexity test file; broad blast radius for edits.
  - Magic fixture-coupled counts (example: exact message count tied to fixture line count) are brittle.
  - Imports from `conftest` as if library module, creating tight coupling to pytest test plumbing.
- `amazon-cpi/tests/test_price_extractor.py`
  - Random user-agent test validates only prefix + length; weak oracle can miss regressions.

### Ruby

- `jekyll-mermaid-prebuild/spec/jekyll_mermaid_prebuild/processor_spec.rb`
  - Some assertions are very weak (example: `svgs` not empty) and do not validate structural correctness.
- `jekyll-highlight-cards/spec/jekyll_highlight_cards/expression_evaluator_spec.rb`
  - `allow_nil` examples include potentially redundant/misaligned expectations (title implies branch distinction without meaningful assertion difference).

## Ranked failure-mode taxonomy (wrong + fixable + polyglot)

Each mode includes a detection heuristic and safe refactor play.

1. **Weak Oracle Assertions**
   - Detect: broad regex, non-empty checks, shallow type checks, overly generic contains.
   - Fix: assert invariant-bearing fields/events/outcomes; prefer structured assertions over prose presence.
   - Why polyglot: appears in Jest/Vitest/RSpec/Pytest equally.

2. **Presentation-Coupled Assertions**
   - Detect: long chains of exact/fuzzy string checks on rendered UI/markdown/HTML/log output.
   - Fix: parse to AST/DOM/token model; assert semantic fragments and critical anchors only.
   - Why polyglot: markdown/html/string snapshot brittleness is universal.

3. **Implementation-Coupled Tests**
   - Detect: spying/stubbing SUT private-ish methods, verifying internal calls instead of external outcomes.
   - Fix: move doubles to boundaries (I/O, network, clock), assert behavior through public contract.
   - Why polyglot: mock-heavy anti-pattern spans JS, Ruby, Python, JVM, etc.

4. **Dead/Redundant Test Logic**
   - Detect: unused mocks/fixtures, duplicate setup blocks, two tests proving same fact with different names.
   - Fix: prune dead setup, parameterize repeated scenarios, merge or sharpen case intent.
   - Why polyglot: dead setup and duplicate specs happen in every framework.

5. **Fixture-Coupled Magic Numbers**
   - Detect: exact counts tied to fixture file size/order without explicit semantic reason.
   - Fix: derive expected values from parsed fixture structure or behavior-level checkpoints.
   - Why polyglot: fixture brittleness is language-agnostic.

6. **Isolation/Cleanup Fragility**
   - Detect: best-effort cleanup with swallowed errors, ad hoc temp dirs, global mutable state.
   - Fix: framework temp primitives + fail-fast teardown + deterministic resource ownership.
   - Why polyglot: flaky state leakage is universal.

7. **Monolithic Test Modules**
   - Detect: very large single files mixing parser, integration, regression, contract tests.
   - Fix: split by behavior domain; preserve shared fixtures via helper modules/builders.
   - Why polyglot: maintainability degradation from test sprawl is universal.

8. **Over-Constrained Enumerations**
   - Detect: tests that lock full key sets/order where extensibility is expected.
   - Fix: assert required subset + invariants; separate strict contract tests when API is intentionally closed.
   - Why polyglot: brittle API-shape assertions occur across ecosystems.

9. **Tautology Theatre (explicit category)**
   - Detect: tests whose pass/fail is predetermined by setup and independent of production behavior.
   - Subtypes:
     - mock tautology (configure mock, then assert same mock value),
     - mock-only test (no real SUT exercised),
     - trivial tautology (`assertTrue(true)`, etc.),
     - framework test (asserting framework/language guarantees, not app behavior).
   - Fix: route assertions through real SUT behavior and domain outcomes; remove/replace framework-only checks.
   - Why polyglot: framework-specific syntax differs, but failure semantics are identical.

10. **Over-Specified Interaction Testing**
   - Detect: exact call counts, strict call order assertions, exhaustive interaction locks (`verifyNoMoreInteractions` style), deep captured-argument inspection.
   - Fix: preserve only behavior-relevant collaboration assertions; relax incidental interaction constraints.
   - Why polyglot: this appears in Mockito/Jest/mock/testify/gomock/Moq/NSubstitute families.

## Joined principles (Farley + Wright + citypaul)

Practical merged rubric for LLM refactor passes:

- **Understandable + Well named**: test name must state behavior and failure intent.
- **Maintainable + Not coupled**: assert outcomes, not implementation internals.
- **Repeatable + Consistent + Independent**: deterministic and order-independent.
- **Atomic + Granular + At least one meaningful assertion**: one behavior focus, high-signal oracle.
- **Necessary**: each test adds distinct knowledge (DRY means knowledge, not cosmetic code dedup).
- **Fast**: avoid unnecessary heavy setup and duplicated expensive fixtures.
- **Simple**: minimize control-flow complexity in tests.

## Proposed multi-pass system (LLM-centric, non-linter-centric)

Design objective: each pass must leave suite measurably better while preserving behavior.

### Pass 0 - Inventory and Intent Extraction

- Build a per-test "intent card":
  - behavior statement
  - current assertion strength
  - dependency profile (clock/fs/network/global state)
  - duplication fingerprint (semantic + structural)
- Output: baseline map, no edits.

### Pass 1 - Oracle Strengthening

- Target weak-oracle tests first.
- Rewrite to assert behavior-bearing invariants (domain fields, state transitions, contract outputs).
- Keep test semantics unchanged; only sharpen the oracle.
- Explicitly remove tautology theatre cases first, since they create false confidence and usually have straightforward rewrites.

### Pass 2 - De-couple from Implementation

- Replace SUT-internal spies with boundary doubles.
- Convert call-graph verification into input/output verification.
- Preserve one focused collaborator-verification test only where genuinely required.
- Apply AP3/AP4 detox rules: reduce strict interaction/count/order checks unless they are contract-critical.

### Pass 3 - De-duplicate Knowledge (not syntax)

- Cluster tests by claimed intent (semantic similarity), then detect repeated behavior checks.
- Merge true duplicates; retain one canonical scenario with best naming and diagnostics.
- Keep structurally similar but semantically different tests separate.

### Pass 4 - Determinism and Isolation Hardening

- Remove swallowed cleanup and hidden shared state.
- Move to explicit temp resources and deterministic time/randomness control.
- Ensure failure messages remain precise after isolation changes.

### Pass 5 - Suite Re-organization by Functional Concern

- Re-group tests by user-visible behavior domain rather than file-history/milestone/utility buckets.
- Produce generated "behavior -> tests" TOC and migration rationale.
- This is the differentiator deterministic tools usually cannot do safely.

### Pass 6 - Explainability and Review Layer

- For every edit, emit:
  - why old test was weak/wrong,
  - why new test is better under rubric,
  - why behavior is preserved.
- This keeps human trust high and supports partial acceptance.

## Candidate feature set for each pass

- **Intent extraction engine** (per-test behavior sentence + confidence).
- **Assertion quality scorer** (weak/medium/strong oracle classification).
- **Knowledge-duplication detector** (semantic duplicate groups, not token-only clones).
- **Coupling detector** (internal spy patterns, global patch hotspots).
- **Isolation risk detector** (cleanup swallow, shared temp dirs, implicit state).
- **Tautology theatre detector** (AP1/AP2 + trivial/framework tautologies).
- **Interaction over-spec detector** (AP3/AP4 with per-framework heuristics).
- **Safe refactor templates** (pattern-specific transforms with rollback hooks).
- **Rationale generator** (human-readable per-change explanation).
- **Uncertainty reporter** ("I cannot safely refactor this test without domain clarification").

## What to prioritize first (highest ROI)

1. Weak oracle strengthening.
2. Internal-coupling removal.
3. Knowledge-level deduplication.
4. Isolation hardening.
5. Functional regrouping.

Reason: this order gives immediate correctness/maintainability gains before larger organizational surgery.

## High-value failure modes to productize first

If building an MVP around "wrong + fixable + polyglot", start with:

- weak assertion strengthening,
- internal spy detox,
- duplicate-behavior consolidation,
- swallowed-cleanup and flaky-state fixes,
- fixture magic-number decoupling.

These were repeatedly observable in sampled Texarkanine suites and are not reliably solved by deterministic linters alone.
