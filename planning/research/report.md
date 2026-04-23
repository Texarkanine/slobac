# The test-suite janitor gap is real, build it

**Bottom line up front:** the niche you've described — two-tier, polyglot, agent-native, behavior-preserving test-suite cleanup + improvement — is **substantially empty**. Five agent-native artifacts come close to Tier 1, none do Tier 2 architecturally, none are polyglot, none reorganize by functional concern, and the AGPL slot is vacant. The CLI "hands" (mutation, smells, linters, codemods) are mature per-ecosystem. The academic literature hands you three usable architectural patterns and one urgent warning. **Compose, don't buy.** Details and links below.

---

## 1. Agent-native prior art — five things, one gap

Almost every test-flavored Claude Code skill / Cursor rule / Copilot instruction is **test-generation** (write new tests) or **TDD discipline** (red-green-refactor), not curation of an existing suite. The handful that touch quality:

- **[obra/superpowers — `testing-anti-patterns`](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/testing-anti-patterns.md)** (Claude Code skill, MIT, 152k★, v5.0.7 Mar 2026). Prescriptive "Iron Law" checklist: no asserting-that-mocks-exist, no test-only prod methods, no over-mocking. **Tier 1 rule vocabulary worth stealing verbatim.** It's a reference doc, not an autonomous cleaner.
- **[citypaul/.dotfiles — `test-design-reviewer`](https://github.com/citypaul/.dotfiles/tree/main/claude/.claude/skills/test-design-reviewer)** (also at [skills.rest](https://skills.rest/skill/test-design-reviewer)). Implements Dave Farley's 8 properties of good tests with a "Farley Score" and actionable recommendations. **The single closest spiritual ancestor to your Tier 1.** Personal dotfiles, not a polished plugin.
- **[citypaul/.dotfiles — `refactoring` skill](https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/refactoring/SKILL.md)**. Explicit "DRY = Knowledge, not Code; don't extract purely for testability." **Directly ratifies your thoughtful-dedup stance.** Read it end-to-end before you write your own spec.
- **[citypaul/.dotfiles — RED-GREEN-MUTATE-KILL-REFACTOR planning](https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/planning/SKILL.md)**. Mutation-before-refactor = verified test strength as a gate. Clean architectural model for "behavior preservation, bug-surfacing as bonus."
- **[jazzberry-ai/python-testing-mcp](https://github.com/jazzberry-ai/python-testing-mcp)** (MCP server). AST mutation + AI analysis + coverage in one server. The only FLOSS MCP doing mutation-aware test-quality analysis. Small, Gemini-coupled, unpolished, but a reasonable embryo.

Adjacent-but-not-yours: **[github/awesome-copilot — testing-automation collection](https://github.com/github/awesome-copilot/blob/main/collections/testing-automation.md)** has a "refactor while tests stay green" prompt (closest cross-harness behavior-preservation prior art). **[CircleCI MCP `find_flaky_tests`](https://github.com/CircleCI-Public/mcp-server-circleci)** is the canonical flaky-agent UX — but SaaS-coupled, so you'll want to remember it as a *reference shape*, not a dependency.

**Subagents / slash commands:** [wshobson/agents](https://github.com/wshobson/agents) (27.9k★), [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) (13k★), [vijaythecoder/awesome-claude-agents](https://github.com/vijaythecoder/awesome-claude-agents), [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) — all ship `test-automator` / `qa-expert` / `test-writer` agents. Every one is **test generation or execution, not suite curation.** Zero two-tier-separated cleanup subagents exist.

**Cursor rules:** [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) and [sanjeed5/awesome-cursor-rules-mdc](https://github.com/sanjeed5/awesome-cursor-rules-mdc) contain pytest/jest/vitest/playwright style rules; none target refactoring an existing suite. [cursor.directory](https://cursor.directory) same story.

**Cline / Windsurf / Aider / Continue / Zed:** surveyed [cline/prompts](https://github.com/cline/prompts), [kinopeee/windsurfrules](https://github.com/kinopeee/windsurfrules), [Aider-AI/conventions](https://github.com/Aider-AI/conventions), [continuedev/awesome-rules](https://github.com/continuedev/awesome-rules), [zed.dev/docs/ai/rules](https://zed.dev/docs/ai/rules) — generation-biased, nothing test-cleanup-specific.

## 2. Prompt libraries: a wasteland with three usable fragments

The major open-source prompt collections ([f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts), [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide), [ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts), [abilzerian/LLM-Prompt-Library](https://github.com/abilzerian/LLM-Prompt-Library), [anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook), LangSmith Hub) contain **zero** dedicated test-refactoring/test-smell/test-curation prompts. Test-tagged entries are either "write me a unit test" one-liners or "evaluate this LLM output" rubrics. Only three genuinely useful pieces of prior art exist:

- **[OpenAI Cookbook — `Unit_test_writing_using_a_multi-step_prompt`](https://github.com/openai/openai-cookbook/blob/main/examples/Unit_test_writing_using_a_multi-step_prompt.ipynb)**. Explain → Plan → Execute with AST validation. The chain structure re-targets trivially from generation to curation.
- **[testmigrator/testsmellrefactoring (UTRefactor)](https://github.com/testmigrator/testsmellrefactoring)** — FSE 2025 replication package. Smell-KB-as-RAG + DSL refactoring rules + CoT walkthrough + multi-smell checkpointing. 89% smell reduction on 879 Java tests. **This is the closest architectural template in the wild.** No license declared, treat as inspiration.
- **[craftvscruft/chatgpt-refactoring-prompts (Ray Myers)](https://github.com/craftvscruft/chatgpt-refactoring-prompts)** — Apache-2.0. Letter-grade + named-smells + bounded action vocabulary output format for code refactoring. Substitute test smells (Assertion Roulette, Mystery Guest, Eager Test, Rotten Green) and you have a Tier 1 output schema.

Honorable mention: [mwinteringham/llm-prompts-for-testing](https://github.com/mwinteringham/llm-prompts-for-testing) (CC-BY-SA, companion to Winteringham's Manning book) — practitioner templates, loose but human.

## 3. The CLI toolchain — mature hands, no brain

You don't need to write any of this; you need to orchestrate it. The stack per ecosystem:

### Mutation testing — the honest signal for "tests that don't assert"

| Lang | Tool | License | Notes |
|---|---|---|---|
| JS/TS | [**Stryker**](https://github.com/stryker-mutator/stryker-js) | Apache-2.0 | Jest/Vitest/Mocha runners; `--since` incremental; JSON reporter |
| Python | [**mutmut**](https://github.com/boxed/mutmut) | BSD-3 | Simple AST mutations, coverage-filtered; an [MCP wrapper already exists](https://github.com/wdm0006/mutmut-mcp) |
| Python | [Cosmic Ray](https://github.com/sixty-north/cosmic-ray) | MIT | SQLite sessions, pluggable — heavier, more configurable |
| JVM | [**PIT / Pitest**](https://pitest.org/) + [**Descartes engine**](https://github.com/STAMP-project/pitest-descartes) | Apache-2.0 | Industry standard; Descartes does cheap extreme mutation ("pseudo-tested methods") |
| Rust | [**cargo-mutants**](https://github.com/sourcefrog/cargo-mutants) | MIT | `--in-diff` for incremental |
| Go | [avito-tech/go-mutesting](https://github.com/avito-tech/go-mutesting), [go-gremlins](https://github.com/go-gremlins/gremlins) | MIT | Ecosystem weak; zimmski fork abandoned |
| Ruby | [Mutant](https://github.com/mbj/mutant) | **⚠️ commercial for non-OSS** ($30–90/dev/mo) | No FLOSS equivalent |
| .NET | [Stryker.NET](https://github.com/stryker-mutator/stryker-net) | Apache-2.0 | Same family as JS |
| C/C++ | [Mull](https://github.com/mull-project/mull) | MIT | LLVM-IR level |

**Niedermayr's pseudo-tested methods** (methods where `return null`/`0` breaks nothing) are the cheapest, most honest Tier 1 signal for "this code has no real assertions." Descartes implements it on JVM. [Paper (EMSE 2019)](https://link.springer.com/article/10.1007/s10664-018-9653-2), [Descartes](https://github.com/STAMP-project/pitest-descartes). Port the idea everywhere.

### Test smell detectors

- Java: [**tsDetect**](https://github.com/TestSmells/TestSmellDetector) (19 smells, 96% precision) + [JNose](https://github.com/arieslab/jnose) (adds coverage). Both MIT, academic pedigree, low velocity.
- Python: [**PyNose**](https://github.com/JetBrains-Research/PyNose) (17 smells, unittest-biased, awkward CLI); [pytest-smell](https://pypi.org/project/pytest-smell/) (thin, single-author).
- JS/TS: **no standalone smell detector exists** — ESLint plugins cover ~40 overlapping rules.
- Warning: the [**Test Smells 20 Years Later**](https://link.springer.com/article/10.1007/s10664-022-10207-5) paper (EMSE 2023) demonstrates the classical TsDetect catalog correlates poorly with real maintenance pain. **Do not ship a Tier 1 tool whose KPI is "reduce TsDetect warnings."** Build around behavioral/semantic validity (does it assert, does it fail for the right reason).

### Linters — your first line of fake-assertion detection

All FLOSS, all emit JSON, all trivially agent-wrappable:

- **JS/TS:** [eslint-plugin-jest](https://github.com/jest-community/eslint-plugin-jest) (`expect-expect`, `no-conditional-expect`, `no-identical-title`, `valid-expect`, `no-standalone-expect`), [@vitest/eslint-plugin](https://github.com/vitest-dev/eslint-plugin-vitest), [eslint-plugin-testing-library](https://github.com/testing-library/eslint-plugin-testing-library), [eslint-plugin-playwright](https://github.com/playwright-community/eslint-plugin-playwright), [eslint-plugin-cypress](https://github.com/cypress-io/eslint-plugin-cypress), [eslint-plugin-mocha](https://github.com/lo1tuma/eslint-plugin-mocha).
- **Python:** [**Ruff** with `PT` + `B` + `S` + `SIM`](https://docs.astral.sh/ruff/rules/#flake8-pytest-style-pt) — industry standard, orders of magnitude faster than flake8; [flake8-pytest-style](https://github.com/m-burst/flake8-pytest-style) is the origin (some rules controversial, see [ruff#8796](https://github.com/astral-sh/ruff/issues/8796)).
- **Go:** [**golangci-lint**](https://golangci-lint.run/) bundling [testifylint](https://github.com/Antonboom/testifylint) (`useless-assert`, `bool-compare`, `require-error`), [paralleltest](https://github.com/kunwardeep/paralleltest), [tparallel](https://github.com/moricho/tparallel), `thelper`, `testpackage`, `usetesting`.
- **Ruby:** [rubocop-rspec](https://github.com/rubocop/rubocop-rspec) (~90 cops: `ExampleLength`, `MultipleExpectations`, `NestedGroups`, `NamedSubject`, `ContextWording`, `ExampleWording`), [rubocop-minitest](https://github.com/rubocop/rubocop-minitest).
- **Rust:** [Clippy](https://github.com/rust-lang/rust-clippy) — `assertions_on_constants`, `bool_assert_comparison`, `assertions_on_result_states`. Incidental coverage; [Dylint](https://blog.trailofbits.com/2021/11/09/write-rust-lints-without-forking-clippy/) for custom.
- **.NET:** [xunit.analyzers](https://github.com/xunit/xunit.analyzers), [NUnit.Analyzers](https://github.com/nunit/nunit.analyzers).
- **JVM legacy:** [PMD Best Practices](https://pmd.github.io/pmd/pmd_userdocs_cpd.html) (`JUnitTestsShouldIncludeAssert`, `UnnecessaryBooleanAssertion`).

### Duplicate / structural rewrite / dead-code

- **Duplicates:** [**jscpd**](https://github.com/kucherenko/jscpd) (polyglot, 150+ formats, ships an `ai` reporter), [**PMD CPD**](https://pmd.github.io/pmd/pmd_userdocs_cpd.html) (30+ languages including JS/TS/Go/Kotlin/Python), [dupl](https://github.com/mibk/dupl) (Go, AST), [flay](https://github.com/seattlerb/flay) (Ruby, AST). All token/AST-level, none semantic — you fill that gap with embeddings (see LTM, §5).
- **Codemods:** [**ast-grep**](https://github.com/ast-grep/ast-grep) (tree-sitter, 50+ langs) for pattern rewrites; [**jscodeshift**](https://github.com/facebook/jscodeshift) / [**ts-morph**](https://github.com/dsherret/ts-morph) for JS/TS with type info; [**LibCST**](https://github.com/Instagram/LibCST) for Python (preserves whitespace/comments, unlike stdlib `ast`); [**OpenRewrite**](https://github.com/openrewrite/rewrite) + [rewrite-testing-frameworks](https://github.com/openrewrite/rewrite-testing-frameworks) for JVM (has `JUnit4to5Migration`, `AssertJ`, `Mockito1to3Migration`, `CleanupAssertions` recipes ready); [comby](https://comby.dev/) polyglot structural. Ready-made test migrations: [jest-codemods](https://github.com/skovhus/jest-codemods), [@vitest/codemod](https://vitest.dev/), [unittest2pytest](https://github.com/pytest-dev/unittest2pytest).
- **Dead code:** [knip](https://github.com/webpro-nl/knip) (JS/TS, replaces ts-prune), [vulture](https://github.com/jendrikseipp/vulture) (Python, noisy on fixtures), [deadcode](https://pkg.go.dev/golang.org/x/tools/cmd/deadcode) (Go), [staticcheck U1000](https://staticcheck.dev/), [cargo-udeps](https://github.com/est31/cargo-udeps), [debride](https://github.com/seattlerb/debride) (Ruby). **"Test that never covers new code" has no drop-in tool anywhere** — you build it from per-test coverage contexts (`coverage.py --context=test`, JaCoCo sessionid, Jest `--coverage` per-test).

### Flaky detection

[pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures) with `--fail-on-flaky`, [pytest-flakefinder](https://github.com/dropbox/pytest-flakefinder), [pytest-randomly](https://github.com/pytest-dev/pytest-randomly), `jest.retryTimes({logErrorsBeforeRetry})`, [Vitest retry](https://vitest.dev/config/#retry), [Playwright traces on retry](https://playwright.dev/docs/test-retries), [Gradle test-retry plugin](https://github.com/gradle/test-retry-gradle-plugin) with `failOnPassedAfterRetry=true`, [gotestsum --rerun-fails](https://github.com/gotestyourself/gotestsum), [cargo nextest retries](https://nexte.st/docs/features/retries/), [NonDex](https://github.com/TestingResearchIllinois/NonDex) / [iDFlakies](https://github.com/TestingResearchIllinois/idflakies) for order-dependency. [DeFlaker](https://www.deflaker.org/) (ICSE 2018) does differential-coverage-based detection without reruns — JVM, academic, last active ~2019 but the idea is the best cheap-detector in the field.

## 4. Academic and industry: three templates, one warning, one gold-standard benchmark

Only a handful of papers matter for building this thing; most of the 2023–25 arXiv torrent is generate-tests-from-scratch noise. The core:

- **[Alshahwan et al., TestGen-LLM at Meta (FSE 2024)](https://arxiv.org/abs/2402.09171)** — the **filter-chain-as-hallucination-firewall**: compiles → passes N times → not duplicate (AST) → coverage delta ≥ 1 → human review. 73% acceptance at testathons. **Copy this pipeline. It's table stakes for Tier 2.** Open-source reimplementation: [**qodo-ai/qodo-cover**](https://github.com/qodo-ai/qodo-cover) (AGPL-3.0, unmaintained, replaced by [qodo-ci](https://github.com/qodo-ai/qodo-ci)). BYOK LLM — still local-runnable.
- **[Foster / Harman et al., Mutation-Guided Test Generation at Meta — ACH (FSE 2025)](https://arxiv.org/abs/2501.12862)** — concern-specific mutants → LLM writes tests that kill them → LLM-judge filters equivalent mutants (0.79 precision baseline, 0.95 with preprocessing). Directly answers your "LLM + mutation for assertion strengthening" use case. Closed-source.
- **[Gao et al., UTRefactor (FSE 2025)](https://arxiv.org/abs/2409.16739)** — the Tier 1 CoT: understand intent → identify smell → plan transform → rewrite → validate. Smell-KB + DSL rules as RAG. 89% smell reduction on 879 Java tests. [Repo](https://github.com/testmigrator/testsmellrefactoring).
- **[Jain & Le Goues, TestForge (arXiv 2503.14713)](https://arxiv.org/abs/2503.14713)** — agentic tool-call loop with 25-iter cap at $0.63/file. [OpenHands integration](https://github.com/CMU-pasta/TestGenEval-OpenHands). Best published agentic scaffold.
- **[Pizzorno & Berger, CoverUp (PACM SE 2025)](https://arxiv.org/abs/2403.16218)** — [plasma-umass/coverup](https://github.com/plasma-umass/coverup), `pip install coverup`. Best open Python reference implementation. Copy its tool-calling interface verbatim.

Required warning: **[Panichella et al., "Test Smells 20 Years Later" (EMSE 2023)](https://link.springer.com/article/10.1007/s10664-022-10207-5)** — the classical smell catalog is mostly noise; machine-generated tests score *better* on smell detectors while being semantically worse. Don't build your Tier 1 KPIs on TsDetect.

Required baseline: **[Niedermayr et al., pseudo-tested methods (EMSE 2019)](https://link.springer.com/article/10.1007/s10664-018-9653-2)** — median 10.1% of methods can be replaced with no-op and pass all tests. Run Descartes before you run a single LLM token.

Second tier worth skimming: [ChatTester](https://arxiv.org/abs/2305.04207) (describe-before-test reduces vacuous assertions), [MuTAP](https://arxiv.org/abs/2308.16557) and [MutGen](https://arxiv.org/abs/2506.02954) (mutation-feedback prompts), [LTM](https://arxiv.org/abs/2304.01397) (embedding-based test suite minimization — CodeBERT + GA, 5× faster than ATM, **drop-in for Tier 1 semantic dedup**), [TaRGET + TaRBench](https://arxiv.org/abs/2401.06765) (45k broken-test repair benchmark — your maintenance eval), [TestGenEval](https://arxiv.org/abs/2410.00752) (68k tests, 11 Python repos — your coverage eval), [FlakyGuard](https://arxiv.org/abs/2511.14002) (Uber Go monorepo, 47.6% repair success), [FlakyDoctor](https://arxiv.org/abs/2404.09398) (neuro-symbolic), [Lucas et al. 2024 on LLM smell detection](https://arxiv.org/abs/2407.19261) (GPT-4 detects 21/30 smells across 7 languages — your cross-language shortcut), [Diffusion of Test Smells in LLM-Generated Tests](https://arxiv.org/abs/2410.10628) (Assertion Roulette and Magic Number dominate LLM output).

Industry writeups that matter: [Google *Flaky Tests at Google* (Micco 2016)](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html), [Google *State of Mutation Testing at Google* (ICSE-SEIP 2018)](https://research.google/pubs/state-of-mutation-testing-at-google/) (diff-scoped mutation surfaced as code-review signals — operational model you want), [Dropbox *Athena* (2021)](https://dropbox.tech/infrastructure/athena-our-automated-build-health-management-system) (watch-and-act reference architecture), [Shopify *Unreasonable Effectiveness of Test Retries* (2023)](https://shopify.engineering/unreasonable-effectiveness-test-retries-android-monorepo-case-study), [Fowler *Eradicating Non-Determinism in Tests*](https://martinfowler.com/articles/nonDeterminism.html) (still the best short essay). [Diffblue Cover](https://www.diffblue.com/) is closed-source, Java-only, RL-based — prior art; not something you can use. [Cognition Devin](https://cognition.ai/blog) posts are marketing.

## 5. Comparison table — the shortlist that matters to you

| Artifact | Harness | Scope | Tier | License | Maint. | Verdict for your use case |
|---|---|---|---|---|---|---|
| [obra/superpowers `testing-anti-patterns`](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/testing-anti-patterns.md) | Claude Code skill | Prescriptive rules | 1 | MIT | Very active (152k★) | **Steal the rule vocabulary.** Interop, don't compete. |
| [citypaul `test-design-reviewer`](https://github.com/citypaul/.dotfiles/tree/main/claude/.claude/skills/test-design-reviewer) | Claude Code skill | Farley's 8 properties | 1 | MIT (implicit) | Active, personal | **Closest spiritual ancestor.** Adapt; don't depend. |
| [citypaul `refactoring` skill](https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/refactoring/SKILL.md) | Claude Code skill | Anti-DRY-dogma | 1/2 | MIT | Active | **Validates your thoughtful-dedup stance.** |
| [citypaul RED-GREEN-MUTATE-KILL](https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/planning/SKILL.md) | Claude Code skill | Mutation-before-refactor | 1→2 bridge | MIT | Active | **Use as your gate architecture.** |
| [jazzberry-ai/python-testing-mcp](https://github.com/jazzberry-ai/python-testing-mcp) | MCP server | Python mutation + AI | 1/2 | MIT | Low | Embryo; wrap or supersede |
| [awesome-copilot testing-automation](https://github.com/github/awesome-copilot/blob/main/collections/testing-automation.md) | Copilot | "Refactor while green" prompt | 1 | MIT | Active | Closest Copilot reference for behavior preservation |
| [testmigrator UTRefactor](https://github.com/testmigrator/testsmellrefactoring) | Academic repo | Java smell refactor CoT | 1 | none | Stale | **Architectural template — copy the CoT.** |
| [qodo-ai/qodo-cover](https://github.com/qodo-ai/qodo-cover) | CLI | TestGen-LLM clone | 2 | AGPL-3.0 | **Unmaintained** | Cannibalize filter-chain code, don't build on |
| [plasma-umass/CoverUp](https://github.com/plasma-umass/coverup) | CLI | Python coverage-guided gen | 2 | Apache-2.0 | Active | Best Python reference for tool-call interface |
| [Stryker / Stryker.NET / Stryker4s](https://stryker-mutator.io/) | CLI | Mutation JS/TS/.NET/Scala | 1 | Apache-2.0 | Very active | **Invoke directly.** |
| [mutmut](https://github.com/boxed/mutmut) + [mutmut-mcp](https://github.com/wdm0006/mutmut-mcp) | CLI + MCP | Python mutation | 1 | BSD-3/? | Active | **Invoke directly.** Already has an MCP wrapper. |
| [PIT](https://pitest.org/) + [Descartes](https://github.com/STAMP-project/pitest-descartes) | CLI | JVM mutation + pseudo-tested | 1 | Apache-2.0 | Active | **Your Niedermayr detector for JVM.** |
| [cargo-mutants](https://github.com/sourcefrog/cargo-mutants) | CLI | Rust mutation | 1 | MIT | Active | Rust story solved |
| [Ruff PT rules](https://docs.astral.sh/ruff/rules/#flake8-pytest-style-pt) | CLI | Python test lints | 1 | MIT | Very active | **Top Python linter.** |
| [eslint-plugin-jest](https://github.com/jest-community/eslint-plugin-jest) + siblings | CLI | JS/TS test lints | 1/2 | MIT | Very active | **Top JS linter.** `expect-expect` catches fake assertions. |
| [testifylint](https://github.com/Antonboom/testifylint) (via [golangci-lint](https://golangci-lint.run/)) | CLI | Go test lints | 1 | MIT | Active | **Top Go linter.** `useless-assert`, `bool-compare`. |
| [rubocop-rspec](https://github.com/rubocop/rubocop-rspec) | CLI | Ruby | 1/2 | MIT | Active | Ruby story solved |
| [tsDetect](https://github.com/TestSmells/TestSmellDetector) / [JNose](https://github.com/arieslab/jnose) | CLI | Java smells | 1 | MIT | Stagnant | Use cautiously; smells ≠ maintenance pain |
| [jscpd](https://github.com/kucherenko/jscpd) | CLI | Polyglot dup | 1 | MIT | Active | **First-pass dedup; AI reporter built in.** |
| [ast-grep](https://github.com/ast-grep/ast-grep) | CLI | Polyglot rewrite | 1 | MIT | Very active | **Your polyglot codemod hammer.** |
| [OpenRewrite rewrite-testing-frameworks](https://github.com/openrewrite/rewrite-testing-frameworks) | Maven/Gradle | JVM test migrations | 1/2 | Apache-2.0 | Very active | **Ready-made JUnit4→5, AssertJ recipes.** |
| [LibCST](https://github.com/Instagram/LibCST) | Library | Python codemod | 1/2 | MIT | Active | **Your Python codemod hammer.** |
| [jest-codemods](https://github.com/skovhus/jest-codemods) / [@vitest/codemod](https://vitest.dev/) / [unittest2pytest](https://github.com/pytest-dev/unittest2pytest) | CLI | Test migrations | 2 | MIT | Active | Bolt-on migrations |
| [pytest-randomly](https://github.com/pytest-dev/pytest-randomly) + [flakefinder](https://github.com/dropbox/pytest-flakefinder) | CLI | Python flaky | 1 | MIT/Apache | Active | Pair them for order-pollution + bulk multiplication |
| [Playwright traces on retry](https://playwright.dev/docs/trace-viewer-intro) | CLI | E2E root-causing | 1/2 | Apache-2.0 | Very active | Feed trace.zip to LLM |
| [knip](https://github.com/webpro-nl/knip) / [vulture](https://github.com/jendrikseipp/vulture) / [deadcode](https://pkg.go.dev/golang.org/x/tools/cmd/deadcode) | CLI | Dead code/exports | 1 | ISC/MIT/BSD | Active | **Not "dead test" detectors** — fill that gap yourself |
| [CircleCI MCP `find_flaky_tests`](https://github.com/CircleCI-Public/mcp-server-circleci) | MCP | Flaky UX | 1 | various | Active | SaaS-coupled. Reference UX only. |
| Mutant (Ruby) | CLI | Ruby mutation | 1 | **⚠️ commercial** | Active | Avoid for closed-source work; no FLOSS Ruby equivalent |

## 6. Gap analysis — what's missing, what to build

Eight things the existing prior art demonstrably **does not** cover, ranked by how much of your differentiator they are:

1. **Two-tier separation (cleanup vs. architectural improvement) as a first-class abstraction.** Zero existing artifacts. obra's anti-patterns is Tier 1, citypaul's refactoring is Tier 2-ish, but nothing is structured around the tier split. This is your load-bearing design choice.
2. **Functional regrouping / suite-as-spec reorganization.** Nobody does this — not academic, not industry, not agent-native. The closest is Airbnb's pyramid-rebalancing blog. A deliverable that outputs a reorganized suite with a table-of-contents mapping behaviors → tests is genuinely novel.
3. **Behavioral smells over syntactic smells.** The "Test Smells 20 Years Later" paper is a warning shot: TsDetect-style rules are weak proxies. Descartes-style pseudo-tested detection, "test passes under `return true` and `return false`", "assert never reached in any execution", "setup >> act >> assert ratio inverted" are the honest signals nobody has packaged.
4. **Polyglot coverage with a unified output model.** Every existing artifact is single-language. You'd be the first to ship one tool with per-ecosystem invokers (Ruff/Stryker/mutmut/PIT/Descartes/golangci-lint/rubocop-rspec/cargo-mutants/Stryker.NET) and a normalized smell/mutation report the agent reads.
5. **Semantic deduplication with rationale.** LTM (black-box minimization via embeddings) and jscpd/CPD (token-level) are the poles; nobody does LLM-guided "these two tests are semantically the same; merge, prefer the better-named, here's why" with a human-readable changelog. This is where thoughtful-dedup actually lives.
6. **Vacuous-assertion report in prose.** Niedermayr's pseudo-tested methods are 10 years old and under-integrated. A Tier 1 feature that runs Descartes/extreme-mutation and emits "this test pretends to verify X but only exercises Y" in plain English is a clear differentiator.
7. **Per-test changelog as a deliverable.** Every tool outputs new code. None output a per-test rationale ("removed: duplicate of `TestFoo::bar`; renamed: `test_1` → `deserialization_rejects_trailing_garbage` because that's what the assertion actually checks"). Meta's 73% acceptance comes from reviewable surface — yours can be higher with rationale.
8. **AGPL slot.** Every test-cleanup-adjacent artifact in this survey is MIT, Apache-2.0, or closed/commercial. There's no copyleft test-curation tool anywhere. Going AGPL is uncontested positioning.

### The composition recipe

You don't need to write a mutation engine, a linter, or a codemod runner. You need the orchestrator and the rationale layer. Build this:

- **Filter chain** (Alshahwan/TestGen-LLM): compile → pass ×N → not-AST-duplicate → coverage+mutation delta ≥ 0 → emit rationale. Non-negotiable gate for every agent-proposed edit.
- **Tier 1 pipeline**: `jscpd` (duplicates) + per-language linter (`ruff`/`eslint-plugin-jest`/`testifylint`/`rubocop-rspec`/`clippy`/`xunit.analyzers`) + Descartes/extreme-mutation (pseudo-tested) + `pytest-randomly`/jest-shuffle (order pollution). LLM proposes rename/regroup/dedup/assertion-fix; codemod via `ast-grep` (polyglot) or `LibCST`/`jscodeshift`/`OpenRewrite` (language-specific).
- **Tier 2 pipeline**: full mutation (`Stryker`/`mutmut`/`PIT`/`cargo-mutants`) → surviving mutants → LLM assertion strengthening (MuTAP/ACH pattern) with equivalent-mutant LLM-judge → validated via filter chain. Migration recipes (`jest-codemods`, `OpenRewrite JUnit4to5Migration`, `unittest2pytest`) available as opt-in.
- **CoT scaffold** (UTRefactor): understand intent → identify smell/weakness → plan transform → rewrite → validate. Each step its own validator.
- **Describe-before-test** (ChatTester): before any edit, force the LLM to write what the test is *supposed* to verify. Store as a per-test docstring. This is also your functional-grouping key.
- **Functional grouping heuristic**: cluster by LLM-extracted "behavior verified" docstring (embedding similarity) rather than filename or milestone. Output is a reorganized suite with a generated TOC.
- **Rationale layer**: per-edit changelog in prose. This is the moat.
- **Agent harness**: ship as (a) Claude Code skill + subagents bundle, (b) MCP server wrapping all CLI invokers, (c) Cursor rules file, (d) Copilot custom instructions. The "install-anywhere" play — the MCP server is the load-bearing one; the rest are thin adapters.
- **Evaluate on** TestGenEval + TaRBench + your own Niedermayr-style pseudo-tested seeded dataset. Don't trust Defects4J alone — it's overfit.

### What you don't build

- A mutation engine. Use existing ones.
- A linter. Use existing ones.
- A codemod runner. Use `ast-grep` / `LibCST` / `jscodeshift` / `OpenRewrite` / `comby`.
- A coverage tool. Use `coverage.py --context=test` / JaCoCo sessions / Jest per-test.
- A SaaS dashboard. The entire point.

### Sardonic closing

The literature is mostly people generating tests from scratch for Defects4J so they can publish a 2% coverage bump. The agent ecosystem is mostly people shipping `test-automator` subagents that re-derive "use describe/it". The commercial space is Diffblue — Java-only, RL-based, closed — and Qodo's cover-agent, whose repo literally says "no longer maintained." The smell catalog everyone cites is, per the best-run empirical study, uncorrelated with maintenance pain. And nobody, anywhere, reorganizes a milestone-sorted suite into a functional spec.

You have a clear gap, a clean composition recipe, a defensible license slot, and four papers' worth of architecture to steal. Build it.
