# Research Findings: LLM-Driven Test Suite Curation

## Overview
This document synthesizes research on automated test suite curation, combining academic literature (`report.md`), industry practices (Dave Farley's 8 properties, `citypaul`'s refactoring skills), and an analysis of existing test suites in the `texarkanine` organization. The goal is to identify articulable, polyglot failure modes in test suites that an LLM-based system can reliably detect and fix, without making any code changes during this research phase.

## Articulable Failure Modes (The "Bad" Patterns)

### 1. Testing Implementation Details (The "Private Method" Trap)
**The Problem:** Tests are coupled to the internal implementation rather than the public behavior. If the implementation changes, the test breaks, even if the external behavior remains correct.
**Evidence:** In `amazon-cpi/tests/test_price_extractor.py`, tests directly invoke and assert on private methods like `_build_product_url`, `_get_random_user_agent`, and `_extract_price_from_text`.
**Why it's wrong:** Violates Farley's Property #4 (Independent of the implementation). It makes refactoring impossible without breaking tests.
**How to fix it:** An LLM can identify tests calling private/internal methods, trace those methods to their public callers, and rewrite the test to assert the same logical outcome via the public API.

### 2. Trivial / Vacuous Testing (The "Speculative" Test)
**The Problem:** Tests that verify language features, trivial getters/setters, or simple string manipulations that carry no business logic weight.
**Evidence:** In `amazon-cpi/tests/test_lib.py`, there are four separate tests for a trivial `process_greeting` function (testing custom message, default message, empty string, and whitespace).
**Why it's wrong:** Violates Farley's Property #5 (Necessary) and the `refactoring` skill's rule against speculative code. It clutters the suite and dilutes the value of real tests.
**How to fix it:** An LLM can use mutation testing (like Niedermayr's pseudo-tested methods) to prove the assertions are weak or trivial, and then consolidate them into a single parameterized test or delete them entirely if they test language features.

### 3. Mystery Guest / Setup Obscurity
**The Problem:** The test relies on complex, implicit setup (like nested `let` blocks or global fixtures) that obscures *what* is actually being tested.
**Evidence:** In `jekyll-mermaid-prebuild/spec/jekyll_mermaid_prebuild/processor_spec.rb`, the tests rely on multiple nested `let` blocks (`config`, `generator`, `site_data`, `site`, `cache_dir`) and a `before` block that stubs out multiple methods and writes to the filesystem.
**Why it's wrong:** Violates Farley's Property #1 (Understandable) and #9 (Simple - cyclomatic complexity of 1). The reader cannot see the cause and effect within the test body.
**How to fix it:** An LLM can inline the relevant setup directly into the test (or a clear factory method), replacing the implicit magic with explicit, readable Arrange-Act-Assert blocks.

### 4. Brittle String/HTML Assertions
**The Problem:** Asserting on exact string matches or HTML structures rather than semantic meaning.
**Evidence:** In `processor_spec.rb`, the test asserts `expect(result).to include("<figure class=\"mermaid-diagram\">")`. If the class name changes or a newline is added, the test fails.
**Why it's wrong:** Violates Farley's Property #2 (Maintainable).
**How to fix it:** An LLM can rewrite string-matching assertions to use semantic parsers (e.g., parsing the HTML and asserting on the node structure) or regexes that ignore whitespace.

### 5. Semantic Duplication (The "Copy-Paste" Test)
**The Problem:** Multiple tests verify the exact same behavior but are written slightly differently or test identical equivalence classes.
**Evidence:** Mentioned in `report.md` (LTM embedding-based minimization). Often seen when developers copy-paste a test to change one variable without realizing they are testing the same path.
**Why it's wrong:** Violates the `refactoring` skill's "DRY = Knowledge, Not Code" principle. It increases suite execution time (violating Farley's "Fast") without increasing confidence.
**How to fix it:** An LLM can cluster tests by their semantic intent (using embeddings), identify duplicates, and merge them, providing a clear rationale ("Merged Test A and Test B because both verify the null-input boundary condition").

### 6. Tautology Theatre (The "Self-Fulfilling Prophecy")
**The Problem:** Tests whose outcome is predetermined by their own setup, independent of production code. This includes *Mock Tautologies* (configuring a mock to return X, then asserting it returns X), *Mock-Only Tests* (no real classes instantiated), *Trivial Tautologies* (`assertTrue(true)`), and *Framework Tests* (verifying that the mocking library works).
**Evidence:** Identified as a core anti-pattern in `a4al6a/claude-code-agents/alf-test-design-reviewer`. These tests provide zero verification of production behavior but create false confidence in test coverage.
**Why it's wrong:** Violates Farley's Property #5 (Necessary) and #2 (Maintainable). It's pure theatre.
**How to fix it:** An LLM can statically detect these patterns (e.g., matching mock setup directly to assertions) and either delete the test or rewrite it to instantiate and exercise the actual production class.

### 7. Over-Specified Mock Interactions
**The Problem:** Tests that verify exact invocation counts, strict call ordering, or use `verifyNoMoreInteractions` when the business logic doesn't strictly require it.
**Evidence:** Highlighted in `alf-test-design-reviewer` as a mock interaction anti-pattern.
**Why it's wrong:** Violates Farley's Property #4 (Independent of the implementation). It makes the test hyper-brittle to any internal refactoring.
**How to fix it:** An LLM can relax the assertions to verify state outcomes rather than interaction histories, or reduce strict ordering/count verifications to simple "was called" checks where appropriate.

## Proposed System Features

Based on the research and failure modes, a polyglot, LLM-driven test refactoring system should include:

1. **Two-Tier Architecture:**
   - **Tier 1 (Cleanup):** Fast, deterministic passes using linters, AST deduplication, and LLM-driven consolidation of trivial/duplicate tests.
   - **Tier 2 (Architectural):** Mutation-guided assertion strengthening. Run a mutation engine, feed surviving mutants to the LLM, and have it rewrite tests to kill them.

2. **The "Filter-Chain" Firewall:**
   - Never commit a test change blindly. The system must verify: `compiles -> passes N times (flaky check) -> coverage delta >= 0 -> mutation score delta >= 0`.

3. **Behavioral Extraction & Regrouping:**
   - Before modifying a test, force the LLM to write a docstring explaining *what* the test verifies (Describe-before-test).
   - Use these descriptions to regroup the test suite functionally, rather than by file or milestone.

4. **Per-Test Rationale Changelog:**
   - The system must output a prose explanation for every change (e.g., "Deleted `test_empty_string` because it was a duplicate equivalence class of `test_whitespace`"). This builds trust and enables human review.

5. **Two-Phase Scoring & Evidence Anchoring:**
   - As seen in `alf-test-design-reviewer`, the system should score tests using a blend of static signal detection (deterministic) and LLM semantic assessment (controlled).
   - Every score or proposed change must cite specific code locations (file:line) and signal counts. A score without evidence is a guess.

6. **Separation of Test-Value and Test-Hygiene:**
   - The system must distinguish between *hygiene* (structural quality, naming, setup complexity) and *value* (mutation score, bug-catch history). A suite of well-written tests that don't catch bugs is just hygienic theatre.