# FINDINGS-GROK.md: Test Refactoring Research for Texarkanine Repos

## Research Inputs Integrated
- **@randommd/goodtests/farley.md**: Dave Farley's 8 properties (Understandable, Maintainable, Repeatable, Atomic, Necessary, Granular, Fast, Simple - cyclomatic complexity ~1). TDD encourages these.
- **Medium article (first 8 of 10)**: Independent, Well-named, Not coupled to anything, Independent of implementation (test behavior not impl), At least one assertion, Clear failure message, Consistent, Fast.
- **citypaul skills** (from .dotfiles):
  - test-design-reviewer: Implements Farley Score + actionable recs. Closest ancestor.
  - refactoring/SKILL.md: MUTATE before REFACTOR; DRY=Knowledge not Code (merge only if same business concept that changes together); commit working code BEFORE refactoring; no speculative code; extract only for readability/SoC not pure testability; RED-GREEN-MUTATE-KILL-REFACTOR workflow.
- **@randommd/goodtests/report.md**: Comprehensive gap analysis. Emphasizes two-tier (Tier 1 cleanup vs Tier 2 architectural), behavioral smells over syntactic (warns vs. classical test smells per "Test Smells 20 Years Later" paper), polyglot orchestration of existing tools (Stryker/mutmut/PIT, Ruff/eslint/jscpd/ast-grep, etc.), mutation-guided (Niedermayr pseudo-tested methods, Descartes), semantic dedup via embeddings, per-test rationales/changelogs, functional regrouping (novel), filter chains for validation. No existing artifact does the full "LLM does what deterministic tools can't" for thoughtful dedup and reorganization.

**Core Thesis**: LLMs excel at the "dawg, you test the same thing (correctly though!) 5 times, and it belongs in this one specific place" judgment calls. Deterministic tools handle syntax/linting/mutation; LLM layer provides semantic understanding, rationale, behavior clustering.

## Texarkanine Org Repos Analyzed (via explore subagent + targeted reads)
Focused on those with **meaningful test suites** ( >10 test files or dedicated dirs with substance; vitest/jest/bun/pytest/mocha/shell). Key ones:
- **cursor-warehouse** (Python/pytest, tests/test_sync.py ~1367 lines, test_embed.py, test_schema.py, fixtures): Heavy on sync engine, JSONL parsing, DuckDB. One monolithic test file with extensive helpers, fixtures, parameterized cases.
- **claude-code-action** (TS/bun:test, ~10 *.test.ts files e.g. create-prompt.test.ts, url-encoding.test.ts, comment-logic.test.ts): Well-granular per-module tests. Large shared mockGitHubData objects repeated across tests.
- **a16n** (TS/vitest + turbo CI, ~197 test files): Large modern frontend/backend suite.
- **bbill-tracker**, **tab-yeet**, **jsonschema2md** (JS/TS jest/vitest/mocha), **ai-rizz** (shell/shunit2 tests), **cursor-warehouse** (Python).
- Others like action-web-ext, inquirerjs-checkbox-search have smaller suites.

**No code changes made anywhere** - pure read-only analysis + subagent exploration.

## Articulable Failure Modes Observed
Focused on modes that meet **ALL 3 criteria**:
1. **We can SEE they're wrong** (visible in code structure, duplication, naming, assert counts, shared setup, coverage overlap, repeated mocks).
2. **We can figure out how to fix them** (LLM can propose specific rename/split/consolidate/parameterize with rationale; validated via existing tests + mutation).
3. **Suitably general/polyglot** (apply across JS/TS, Python, Go, Java, Shell, Rust - not tied to one framework's syntax; use AST similarity, embeddings, behavioral description).

### High-Priority Polyglot Failure Modes (Ranked by Prevalence/Impact in Texarkanine Suites)
1. **Semantic Duplication of the Same Behavior ("test the same thing 5 times")**
   - **Seen in**: cursor-warehouse (overlapping sync/JSONL parsing cases across test_sync.py helpers and multiple test fns); claude-code-action (similar GitHub context mocking + validation in create-prompt.test.ts, prepare-context.test.ts, trigger-validation.test.ts); a16n likely has repeated component state tests.
   - **Visible**: Repeated mock data, similar assertion patterns on same logic (e.g. encoding, validation, parsing), coverage reports showing same lines hit by multiple tests. jscpd catches syntactic, embeddings/LLM catch semantic.
   - **Why wrong**: Violates Necessary (not a new perspective), Granular, Maintainable, Independent of impl. Duplicates knowledge.
   - **Fix**: Consolidate to canonical test (usually the most behavior-focused one), use parameterized tests or shared test data builders. Prefer lower-level or dedicated behavior test. citypaul DRY=Knowledge: only if same business concept.
   - **Polyglot**: Yes - applies to any test suite. LLM judges "same knowledge" via intent description.

2. **Non-Granular / Multi-Responsibility Tests (Big Ball of Mud Tests)**
   - **Seen in**: cursor-warehouse/test_sync.py (monolithic file with complex helpers, multiple scenarios in single tests or one huge describe); some claude-code-action tests with large setup + multiple expects.
   - **Visible**: High cyclomatic complexity in test (>1), multiple `expect`/`assert` per test, long test bodies, tests doing setup+act+multiple unrelated asserts, shared mutable state.
   - **Why wrong**: Violates Farley's Granular/Simple, Greg's "at least one assertion" (but not too many), Atomic. Hard to diagnose failures (wade through logs).
   - **Fix**: Split into multiple focused tests with single outcome each. Extract common setup to factories/test builders (not shared mutable fixtures). Add descriptive names/docstrings.
   - **Polyglot**: Universal. Detect via AST parse (count asserts/branches), LLM "describe what this test actually verifies".

3. **Vague/Poorly-Named or Impl-Coupled Tests**
   - **Seen in**: Generic names in smaller tests; some tests name after impl steps ("testFunction") vs. behavior ("rejects_trailing_garbage_in_deserialization").
   - **Visible**: Test name doesn't "shout" the property/outcome (Farley Understandable, Greg Well-named). Asserts on internal state/mocks vs. observable behavior.
   - **Why wrong**: Not understandable, coupled to impl (changes break tests), doesn't document code (Greg #9).
   - **Fix**: LLM rewrites names to behavior-focused ("when_lid_opens_printer_stops"), adds per-test docstring describing the *property* verified. Refactor to public contracts.
   - **Polyglot**: Yes. LLM excels at behavior extraction from code/comments.

4. **Overly Complex/Non-Atomic Setup & Coupling**
   - **Seen in**: Repeated large mockGitHubData objects copied across claude-code-action test files; cursor-warehouse complex fixture copying and DB setup shared without full isolation.
   - **Visible**: beforeEach/ fixtures with side effects, tests depending on order or external DB/files, complex setup hiding the "act".
   - **Why wrong**: Violates Atomic, Independent, Repeatable/Consistent, Fast. Not standalone.
   - **Fix**: Per-test factories, immutable test data, explicit mocks per test, in-memory where possible. Use test doubles at data access layer (Greg).
   - **Polyglot**: Core testing principle.

5. **Vacuous / Weak Assertions (Pseudo-tested)**
   - **Seen potentially**: Tests that exercise but don't strongly assert outcomes (e.g. mock verification without result check, or tests that pass even with broken impl). Common in large suites.
   - **Visible**: Via mutation testing (Niedermayr: methods replaceable by no-op/constant and tests still pass). Lack of assertions or only testing happy path.
   - **Why wrong**: No real verification. Violates "at least one assertion", Necessary.
   - **Fix**: Strengthen with specific assertions on outcomes. Use mutation to guide (Meta/TestGen-LLM filter chain style).
   - **Polyglot**: Mutation tools exist per lang (Stryker, mutmut, PIT+Descartes, cargo-mutants); LLM analyzes survivors.

6. **Brittle Tests & Lack of Clear Failure Messages**
   - **Visible**: Tests with cryptic errors, tight coupling to exact strings/formats, no custom messages.
   - **Fix**: Improve messages, test contracts not impl details.

**Other Observed**: Test code itself has duplication (e.g. same helper patterns copied); tests testing framework features vs. app logic; integration tests duplicating unit coverage.

These are **not** classical "test smells" (per 2023 paper warning - poor correlation with pain). These are behavioral/semantic/maintainability issues LLMs can articulate with rationale.

## Brainstorm: Features of a "Test Janitor" System
A system that, **in each pass over a codebase**, makes targeted, safe, progressive improvements. Inspired by report.md's two-tier, citypaul workflow, Farley/Greg properties, and observed modes. **Pure LLM strength**: semantic judgment, rationale, clustering. Orchestrates (doesn't replace) deterministic tools.

### Core Architecture (Per-Pass Design)
- **Pass-Oriented & Scoped**: One failure mode per pass (e.g. Pass 1: Semantic Dedup; Pass 2: Granularity Splitting; Pass 3: Naming & Documentation; Pass 4: Setup Isolation; Pass 5: Mutation Strengthening). Prevents scope creep. Tracks progress via scorecard. Multiple passes compound to functional reorganization.
- **Tiered Analysis**:
  - **Tier 1 (Cleanup - Safe, High-ROI)**: Detect visible wrongs using polyglot signals + LLM. Output per-test Farley/Greg score + specific violations + rationale ("This duplicates validation from X; same knowledge per citypaul").
  - **Tier 2 (Architectural - After Mutation Gate)**: Functional regrouping (cluster by LLM-extracted "behavior verified" using embeddings/similarity, not filenames), suite-as-spec TOC, deeper refactoring.
- **Validation Gates (citypaul + report.md)**: 
  - RED-GREEN (existing tests pass).
  - MUTATE (run Stryker/mutmut/PIT etc. on affected area; kill survivors).
  - Filter chain (compiles, passes N times, no AST dup, coverage/mutation delta >=0, behavior preserved).
  - LLM-judge for equivalent mutants.
  - **NEVER speculative**. Commit baseline before changes.
- **Polyglot Core**:
  - Normalized failure mode catalog (the 6 above + growing from real suites).
  - Wrappers for per-lang tools (Ruff PT rules, eslint-plugin-jest, testifylint, rubocop-rspec, jscpd/ast-grep for dups/rewrites, LibCST/jscodeshift/OpenRewrite for safe edits).
  - LLM does the "polyglot semantic layer" - describe intent in natural language, independent of syntax.
- **Rationale & Human-in-Loop Deliverables** (the moat):
  - Per-change changelog: "Removed duplicate of `test_foo`; merged because tests same edge case (validation of X); new name better matches Farley 'Understandable'; Farley score +2; mutation kill rate improved".
  - Before/after diffs with property mapping.
  - Suite TOC mapping behaviors -> tests.
  - Composite "Test Health Score" tracking across passes.
- **Detection Heuristics (visible + fixable)**:
  - Semantic dup: embeddings + LLM "do these verify same property?"
  - Granularity: AST assert/branch count + LLM summary.
  - Naming: LLM rewrites to match "when X then Y" or Farley style.
  - Use report.md tools (jscpd first for syntactic, then LLM for semantic).
- **Agentic Subagents** (per report.md gap):
  - Inventory/Scorer: reads suite, computes scores, finds candidates.
  - Diagnoser: evidence-based diagnosis tied to specific modes.
  - Proposer: generates minimal, behavior-preserving edits with CoT (UTRefactor style: understand intent → identify smell → plan → rewrite → validate).
  - Validator: runs tests/mutation, rejects if behavior changes.
  - Reporter: generates findings, changelog, updated Farley scores.
- **Novel Differentiators**:
  - **Functional Regrouping**: Move from "per file/module" to "per behavior/spec" over passes. Novel per report.md.
  - **Thoughtful Dedup with Rationale**: Not blind DRY; uses citypaul "same knowledge" heuristic + examples from suite.
  - **Mutation-Guided Test Improvement**: Start with pseudo-tested detection (Descartes style), let LLM strengthen assertions.
  - **No Linter Orchestration**: Trust repo's existing hooks (as per query). Focus exclusively on LLM-unique value.
  - **Iterative Improvement Loop**: Each pass leaves suite strictly better (higher scores, fewer dups, better names), measurable.

### Implementation Sketch (No Code Written)
- MCP server wrapping tools + LLM reasoning.
- Cursor rule / Claude skill bundle (build on citypaul + obra anti-patterns).
- Output format: structured (violations list, proposed edits with rationale, validation results).
- Eval: Use TestGenEval, TaRBench, seeded pseudo-tested datasets, real Texarkanine suites before/after passes.
- License: AGPL to fill gap.

This system would systematically eliminate the observed failure modes across polyglot suites, making tests more like Dave Farley's ideal and Greg's properties, while following citypaul's disciplined workflow. The "janitor" does the curation/refactoring that deterministic tools and current agents don't touch.

**Key Insight from Texarkanine Analysis**: Even "good" suites (like claude-code-action's granular files) have semantic overlap and repeated setup. Monolithic ones (cursor-warehouse) scream for splitting/dedup. LLMs can see the "5 tests for same thing" pattern instantly with context; the system needs to surface it with evidence and safe fix paths.

Research complete. No changes made to any codebase.
