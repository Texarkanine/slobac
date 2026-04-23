# FINDINGS — Composer: LLM-native test curation (research)

**Date:** 2026-04-22  
**Scope:** Pure research. No code changes were made. Goal: join prior art (local `report.md`, Farley thread, Greg Wright’s first eight properties, citypaul’s skills, **[a4al6a/claude-code-agents `alf-test-design-reviewer`](https://github.com/a4al6a/claude-code-agents/tree/main/alf-test-design-reviewer)**) with **concrete failure modes** observable in **texarkanine**-linked repositories present under `/home/mobaxterm/Documents/git`, and outline **polyglot** features for a system that improves the suite *per pass* without relying on repo-orchestrated linters (each repo keeps its own deterministic tooling).

**Positioning (user intent):** Deterministic tools already cover hooks, Ruff, eslint rules, etc. The differentiator is **semantic work**: “you test the same thing (correctly) in five places; *this* is the one canonical home, and here’s why.”

---

## 1. How texarkanine repos were identified

Searched for `github.com/texarkanine` / `Texarkanine/` in `package.json`, `go.mod`, `README.md`, `Cargo.toml`, and `pyproject.toml` (workspace-wide, bounded globs). **Not** every such repo in the org is cloned here; the list is **what is present and attributable**.

| Repo (local) | Meaningful test signal | Notes |
|----------------|------------------------|--------|
| **a16n** | **High** — 35+ `*.test.ts` across engine, cli, models, glob-hook, plugins, docs | Monorepo; mirrored patterns across plugins. |
| **inquirerjs-checkbox-search** | **High** — 16 tests under `src/__tests__/` | Vitest; UI/TTY behavior. |
| **ai-rizz** | **High** — 30+ shell tests (`tests/unit`, `tests/integration`) | shunit2-style; large prose headers. |
| **bbill-tracker** | **Medium** — 9 Jest files under `test/unit/` | Domain-heavy mocks. |
| **tab-yeet** | **Medium** — Vitest in `test/` + integration | Extension flow. |
| **jekyll-auto-thumbnails** | **Medium** — 8 RSpec files in `spec/` | Ruby. |
| **cursor-warehouse** | **Lower count, real** — 3 `test_*.py` | Pytest; schema contract tests. |
| **a16n-plugin-cursorrules** | **Lower** — 2 Vitest files | Overlaps conceptually with **a16n** `plugin-cursor` discovery. |

Repos that mention texarkanine in docs but have **negligible automated tests** in-tree (e.g. **jekyll-mermaid-prebuild** — rules/docs only) are noted for org completeness but not used as primary examples.

---

## 2. Prior art synthesis (ground rules for “good”)

### 2.1 Dave Farley (eight properties) — from `farley.md` + citypaul `test-design-reviewer`

Understandable, Maintainable, Repeatable, Atomic, Necessary, Granular, Fast, Simple (thread adds cyclomatic complexity ≈ 1). Citypaul’s skill weights **Understandable** and **Maintainable** highest; **Fast** slightly lower. **TDD/“First”** appears in the skill as an eighth scored axis (not in the original 8-tweet list).

**Implication for automation:** A pass should output **rationale** tied to these axes (not just a single score), so humans can see *why* a merge or move is recommended.

### 2.2 Greg Wright — first eight (Medium)

1. Independent (order, parallel)  
2. Well named  
3. Not coupled to [too much]  
4. Independent of implementation (behaviour)  
5. At least one assertion; one assertion per test as practice  
6. Clear failure message  
7. Consistent (determinism)  
8. Fast  

Aligns with Farley; adds explicit **naming** and **failure message** as first-class. **#4 (behaviour not implementation)** is the bridge to citypaul’s **refactoring** skill: *don’t extract purely for testability* — tests should not force artificial structure if that’s not a product concern.

### 2.3 citypaul `refactoring` / `test-design-reviewer` (fetched 2026-04-22)

- **Refactoring skill:** DRY = **knowledge**, not code; after mutation tests pass, prioritize knowledge duplication, nesting, magic numbers; **do not** extract only to satisfy unit tests. Commit-before-refactor; no speculative code.  
- **Test-design-reviewer:** Farley scorecard + evidence table; fork/explore agent.  

**Implication:** The system’s “dedupe” must distinguish **redundant knowledge** (merge candidates) from **accidental structural similarity** (keep separate) — a **non-linter, semantic** judgment.

### 2.3b a4al6a `alf-test-design-reviewer` — agent-native prior art (operational superset)

Repository: [github.com/a4al6a/claude-code-agents — `alf-test-design-reviewer`](https://github.com/a4al6a/claude-code-agents/tree/main/alf-test-design-reviewer) (companion [`README.md`](https://github.com/a4al6a/claude-code-agents/blob/main/alf-test-design-reviewer/README.md)).

This is the same **Farley 8 + weighted index** line as citypaul’s `test-design-reviewer`, but **specified as a full Claude Code agent** with skills (`farley-properties-and-scoring`, `signal-detection-patterns`), examples (high- vs low-score Java suites), and `docs/` research notes. It is a close **spiritual sibling** to citypaul; citypaul’s skill even attributes an earlier test-design-reviewer to **andlaf-ak/claude-code-agents** — a4al6a’s tree is a **heavier, more mechanized** take in the same family.

**What it adds beyond a short `SKILL.md`:**

| Mechanism | Why it matters for your “LLM pass” product |
|-----------|---------------------------------------------|
| **60/40 static vs LLM** per property | Explicitly separates deterministic **signals** (sleep, I/O, magic numbers, “mega-tests”, mock patterns) from **semantic** judgment (naming, assertion appropriateness, tautology theatre the regex missed). |
| **Per-test-method signals** with file:line evidence | Same **evidence-anchored** bar you want for merge/dedup **rationale**; aggregates to file (P90 for negatives) and suite (LOC-weighted). |
| **Default 5.0 when no signal** | “Unknown ≠ good” — conservative for automation that might otherwise over-score silent suites. |
| **Scale policy** | >50 test files: SHA-256 sampling + always include files with huge method counts; matches **proportional effort** in large monorepos. |
| **Language-aware** pattern tables | Java, Python, JS/TS, Go, C# — aligns with **polyglot** invokers, not one-regex-fits-all. |
| **“Tautology theatre” tax** | Mock tautology, mock-only tests, trivial assertions, framework tests — *would this pass if production were deleted?* Directly encodes **Necessary** / false-confidence detection without shipping TsDetect as KPI. |
| **Mock anti-patterns AP1–AP4** | Over-specified `verify` / `verifyNoMoreInteractions`, ArgumentCaptor rabbit holes, etc. — **Maintainable** + implementation-coupling. |
| **Hygiene vs value** | Explicitly splits **Farley / structural** quality from **mutation / coverage / bug-catch** “test value” — same conceptual split as your Tier-1 **janitor** vs optional mutation in `report.md`. |
| **Optional mutation + flaky (when available)** | Not mandatory; elevates Necessary/Granular when the user *has* Stryker/PIT/etc. or CI history. |
| **Pyramid + property-based mix audit** | Suite-shape narrative beyond single-file review. |
| **Machine-readable JSON schema** | `test-design-reviewer-data.json` in the agent spec for aggregation pipelines. |

**Constraints:** The agent is defined **read-only** (no `Write`/`Edit` in the spec); it **reviews**, not refactors. That matches your split: **this prior art = assessment + evidence**, your differentiator = **per-pass code moves with rationale** (and thoughtful dedup). The a4al6a package does **not** implement suite regrouping, semantic “canonical home of five” merging, or per-edit changelogs — those remain **gaps** (as in `report.md`).

### 2.4 `report.md` (local)

Valuable for **ecosystem inventory** and **filter-chain** / mutation / academic references. The user’s stated direction de-emphasises **orchestrating** every linter; the **rationale layer**, **per-test changelog**, and **behavioural vs syntactic smell** arguments remain the right spine.

---

## 3. Articulable failure modes (texarkanine workspace evidence)

Each mode below is meant to satisfy: **(1) visibly wrong or suboptimal**, **(2) fix path exists**, **(3) polyglot** (not tied to a single framework).

### 3.1 Refactor-tagged or history-laden tests that duplicate an earlier test

**Signal:** A test name references a past refactor (“after X refactor”) while re-asserting behavior already covered (e.g. `getPlugin` still returns the same object fields).

**Example (a16n / `engine.test.ts`):** `it('should return the plugin via getPlugin after source tracking refactor', ...)` re-checks `cursor` id/name similarly to `should get plugin by id` in the same file.

**Why it’s wrong (soft):** The extra test *may* still add confidence if it guards ordering regression, but often it is **Necessary**-redundant: same user-visible behavior, two examples.

**Fix:** Collapse to one spec with a name that states the **invariant**; or keep one “characterization” test if the scenario truly differs (e.g. only fails when registration order changes).

**Polyglot:** Any language; naming and assertion overlap are visible without AST.

---

### 3.2 Mirrored suites across near-isomorphic components (table-driven opportunity)

**Signal:** Two files (e.g. `plugin-cursor` vs `plugin-claude` `discover.test.ts`) repeat the *same* scenario matrix: “basic file”, “multiple files”, “empty project”, “nested paths”, with only plugin-specific fixtures and string literals changed.

**Why it’s not “wrong”:** Each plugin is a separate deliverable; separate tests are defensible.

**Why an LLM pass helps:** **Necessary** and **Maintainable** — when a rule changes (“how we name items from file paths”), **two suites drift**. A system can propose a **shared test matrix** (harness + per-plugin expected snippets) *or* document that divergence is intentional.

**Polyglot:** JUnit parameterized, RSpec shared examples, Vitest `each` — the *refactor* is structural + narrative.

---

### 3.3 Same bug, multiple “bug reproduction” tests (split narrative)

**Signal:** Several tests document different symptom stories (tab vs readline vs spaces) for **one** underlying contract: “selection key must not write into search buffer.”

**Example (inquirerjs / `selection.test.ts`):** `toggle with tab` vs `should not add tab characters to search` vs `readline tab-to-spaces` — all legit; together they can overshoot **Granular** (multiple failures might fire for the same one-line fix).

**Fix:** One **property** or **contract** test (“search buffer invariant under selection keys”) plus optional **regression** cases only where behavior truly branches.

**Polyglot:** Behavioural spec + table of key sequences.

---

### 3.4 Copy-paste domain fixtures (knowledge DRY in data)

**Signal:** Two tests build nearly identical `mockTransaction` / `vin` / `vout` trees and only change txids, then assert the same shape validation.

**Example (bbill-tracker / `BitcoinBillDetector.test.js`):** “create proper BitcoinBillSpend objects” vs “handle … detection correctly” — overlapping structure and expectations (`validateBitcoinBillSpend`, field checks).

**Why tools miss it:** Token dedupers may not flag it; **semantically** it’s the same *scenario* with different labels.

**Fix:** Shared factory (given **citypaul**: extract **knowledge** — “standard bill spend tx shape”) with per-test only the varying assertions.

**Polyglot:** Universal.

---

### 3.5 Schema/contract “big bang” equality

**Signal:** A test asserts that the **full** column set of a table equals a frozen Python `set` (or one huge diff message).

**Example (cursor-warehouse / `test_schema.py`):** `scored_commits` column set equality, harness defaults looped per table.

**Why it’s not incorrect:** Migrations need a source of truth.

**Failure mode for maintenance:** **Granular** at *failure* time — one missing column and the test says “huge set mismatch” rather than “add column X”. **Understandable** for newcomers is weaker unless comments evolve with the schema (they partially do, e.g. `Round 3 RW9`).

**LLM pass:** Suggest **layered** assertions (required columns vs optional vs deprecated) or **changelog** when columns are renamed — semantic documentation of intent.

**Polyglot:** SQL, Protobuf, OpenAPI — same idea.

---

### 3.6 Overlap within one file: discover happy path + “reads correct content”

**Signal:** One test checks discovery returns one item; another uses the *same* fixture to assert `content ===` file read. Both are **correct**; combined they are **Necessary**-adjacent (could be one test with two asserts if the name covers both).

**Example (a16n-plugin-cursorrules / `discover.test.ts`):** `discovers .cursorrules` and `reads correct file content`.

**Fix:** Merge or name so **Granular** is explicit (if split: first = wiring, second = content integrity — then names should say that).

**Polyglot:** General.

---

### 3.7 Integration test coupling to implementation details

**Signal:** An “end-to-end” test hard-codes a **case** or formatting detail (e.g. `tAp` vs `tap`) to match `formatTabs`’ current casing rules, without stating that rule in the name.

**Example (tab-yeet / `extension-flow.test.js`):** `transform then markdown format matches manual pipeline` — expectation encodes a specific case transformation.

**Why it matters (Wright #4, Farley Maintainable):** When formatting rules change, the test looks like a product failure though only **implementation** of title-casing changed.

**Fix:** Name the rule (`markdown link title preserves …`) or assert through a **public** contract.

**Polyglot:** General (snapshots, golden strings, DOM serializations).

---

### 3.8 Shell (or e2e) suites: documentation duplication and scenario overlap

**Signal:** Every file has a 15–20 line header listing “Test Coverage: …” while individual tests are short. **ai-rizz** — `test_sync_operations.test.sh` and siblings.

**Failure mode:** **Understandable** at file level; **Necessary** between files is unclear (multiple tests touching “sync restore after delete” with different setups).

**LLM pass:** Map tests to a **capability map**; flag **two tests that prove the same capability**; suggest fold or cross-reference.

**Polyglot:** Applies to BDD feature files, Cypress specs, etc.

---

### 3.9 RSpec: delegation + return value in one test, then return-only in a second

**Example (jekyll-auto-thumbnails / `generator_spec.rb`):** `imagemagick_available?` — first it asserts delegation + return; second only false path.

**Not wrong;** the pattern sometimes splits **Wright #5** (one main assertion per test) vs **necessary** interaction checks. An LLM can align **naming** with **what would fail** for each (delegation contract vs error path).

---

## 4. Cross-cutting mapping: failure mode → Farley / Wright / citypaul

| Failure mode | Farley (primary) | Wright (first 8) | citypaul echo |
|--------------|------------------|------------------|----------------|
| Refactor-tagged duplicate | Necessary, Granular | #5, #1 | DRY = knowledge |
| Mirrored plugin suites | Maintainable, Necessary | #4 / coupling | — |
| Split bug repros | Granular, Necessary | #6 failure clarity | — |
| Copy-paste fixtures | Necessary | (implicit coupling) | DRY = knowledge |
| Schema set equality | Understandable, Granular | #6 | — |
| Overlapping discover tests | Necessary, Granular | #5 | — |
| E2E case coupling | Maintainable | #4 | Refactor: behaviour |
| Shell header / overlap | Necessary, Understandable | #2, #1 | — |

---

## 5. Brainstorm: system features (per-pass improvement)

Features are phrased so they **do not** require running every repo’s linter; they can use read-only static analysis, embeddings, and **optional** user-invoked local commands.

### 5.1 Tier A — “See it in the text” (LLM-primary)

1. **Duplicate-knowledge report:** Clusters tests that assert the same *invariant* (embedding + name + shared fixture literals); for each cluster, pick a **canonical location** and rationale (Farley Necessary, citypaul DRY = knowledge).  
2. **Invariant extraction:** For a cluster, propose one sentence **“This test protects: …”** (describe-before-test, as in `report.md`’s filter-chain philosophy).  
3. **Name/concern alignment:** Flag tests whose **first assertion** or **data setup** contradicts the `it`/`test` name (Wright #2, Farley Understandable).  
4. **Refactor-historical name detection:** Grep for `refactor`/`bug #`, `JIRA-`, `GH-` in titles; suggest neutral invariant names.  
5. **Mirror-detection** across files (e.g. `discover.test.ts` pairs): same describe-tree shape → “shared matrix” or “documented intentional divergence” template.  
6. **Contract layering for big assertions:** For schema/JSON golden tests, split into **core vs extended** with ordered failure messages (Wright #6).  
7. **Shell/HTML comment audit:** Map headers to actual tests; find orphan documentation lines.

### 5.2 Tier B — “Stronger with optional machines” (user runs locally)

8. **Mutation hook (optional):** If user runs mutation tests, attach **“this assertion never killed a mutant on line L”** to **Tier A** items — aligns with citypaul’s *MUTATE before refactor* and `report.md`’s Niedermayr / pseudo-tested theme — **not** as mandatory orchestration.  
9. **Flaky heuristics without CI:** Suggest `sleep`, `Date.now`, `Math.random` in test bodies (Repeatable / Wright #7) from static read.

### 5.3 Tier C — Output shape (the “moat” from `report.md`)

10. **Per-test change log in prose** — for each edit in a pass: *merged into X because …*, *renamed because …* (reviewability).  
11. **Suite table of contents** — behavior → test mapping (the gap `report.md` calls out as unfilled).  
12. **“Do not extract production code for test-only reasons”** gate — **citypaul**-style — flag suggestions that would push extraction purely for testability.

### 5.4 Anti-goals (per user)

- **Not** a universal linter bundle or “run these 7 CLIs in order.”  
- **Not** optimizing KPIs on classical TsDetect-style smell counts without semantic backing (`report.md` warning).

---

## 6. Polyglot “suitability” checklist

A failure mode is **suitably general** for this system if a reviewer can state it without naming Jest vs pytest:

- It references **invariants**, **naming**, **duplicated scenarios**, **mirrored components**, **documentation drift**, or **regression-narrative sprawl**.  
- The fix is **merge**, **rename**, **shared fixture**, **table-driven matrix**, **layered contract**, or **moved to canonical file** — not “apply rule X from eslint.”

---

## 7. References (external, retrieved or already in repo)

- Dave Farley — thread in `randommd/goodtests/farley.md`; [citypaul test-design-reviewer `SKILL.md`](https://raw.githubusercontent.com/citypaul/.dotfiles/main/claude/.claude/skills/test-design-reviewer/SKILL.md).  
- [citypaul refactoring `SKILL.md`](https://raw.githubusercontent.com/citypaul/.dotfiles/main/claude/.claude/skills/refactoring/SKILL.md).  
- [a4al6a/claude-code-agents — `alf-test-design-reviewer`](https://github.com/a4al6a/claude-code-agents/tree/main/alf-test-design-reviewer) (agent definition, README, `skills/`, `examples/`, `docs/`).  
- Greg Wright — *Ten Properties of Good Unit Tests* (first eight): [Medium](https://medium.com/@gregwright_1301/ten-properties-of-good-unit-tests-3bbd49222754).  
- Local landscape: `randommd/goodtests/report.md`.

---

## 8. Limitations of this pass

- Only repositories **in workspace** and **attributed** to texarkanine were inspectable.  
- No test **execution** was run; conclusions are from **static reading** of samples.  
- Deeper **semantic deduplication** (embeddings over full suite) was not computed — a future pass could do so.

This document is **research for Composer**-style tooling: **articulate, fixable, general** test failures, with **evidence** from this workspace and alignment to Farley, Wright, citypaul, and the user’s no-linter-orchestration stance.
