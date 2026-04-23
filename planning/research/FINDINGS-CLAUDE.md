# FINDINGS-CLAUDE.md — the LLM-uniquely-fixable test anti-pattern set

*Pure research. No code was changed. Findings synthesized from*
*`report.md`, `farley.md`, citypaul's `test-design-reviewer` and `refactoring`*
*skills, Greg Wright's "Ten Properties" (first 8), `a4al6a/alf-test-design-reviewer`,*
*and a direct audit of eleven `texarkanine`-owned repos with meaningful*
*test suites.*

---

## 1. Premise & scope

### The thing we are **not** building

- **Not a linter.** `eslint-plugin-jest`, `ruff PT`, `testifylint`,
  `rubocop-rspec`, `xunit.analyzers`, Clippy, etc., already cover everything
  that can be expressed as "this token-level pattern is wrong."
- **Not a mutation testing driver.** Stryker / mutmut / PIT+Descartes /
  cargo-mutants / Mull already tell you "no test noticed when I broke this
  branch." We assume the repo has (or will hook up) what it cares about.
- **Not a smell-catalog scoreboard.** The *Test Smells 20 Years Later* (EMSE
  2023) warning applies: TsDetect-style numeric counts correlate poorly with
  maintenance pain. A Farley score, unmodified, is a rating artifact, not a
  plan.
- **Not a test generator.** TestGen-LLM / CoverUp / ChatTester already do this.

### The thing we **are** building

A loop-callable "pass" that an LLM performs over an existing test suite.
Each pass produces **a small, reviewable set of behavior-preserving edits**
plus **a per-edit prose rationale**, driven by classes of failure that meet
all three of the user's criteria:

1. **Seeable** — an LLM reading the suite can point at the problem and name
   it, with a concrete signal, not vibes.
2. **Fixable** — the transformation to fix it is mechanical or nearly so,
   and a validator (compile, tests-still-pass, no coverage loss, no
   mutation-score loss) can gate it.
3. **Polyglot** — the same detection heuristic and fix recipe transfers
   across Python/JS/TS/Go/Ruby/Rust/Java/C# with at most superficial
   re-skinning.

### The user's north-star phrasing

> "dawg, you test the same thing (correctly though!) 5 times, and it
> belongs in this one specific place of those five, for reason…"

That sentence decomposes into four LLM-native judgments that no
deterministic tool can make:

- **Equivalence** — are these tests exercising the same observable behavior
  (not the same tokens)?
- **Locality** — which file/module/level is the *right* home for that
  behavior, given the rest of the suite's organization?
- **Authority** — which of the N existing copies is the "canonical" one
  (best name, smallest fixture surface, strongest assertions)?
- **Justification** — *why* here, not there.

Every proposed taxonomy entry below must preserve at least one of those
four as its core move; otherwise it's table-stakes linting and we leave
it to the linters.

---

## 2. What the inspiration corpus already gives us

### Dave Farley (8 props) + Greg Wright (first 8)

Treat these as the **evaluation rubric**, not the action list. Important
collapse: Farley's *Atomic* ≈ Wright's *Independent* + *Consistent*;
Farley's *Necessary* ≈ Wright's #4 *Independent of Implementation*. The
genuinely distinct axes to keep are:

| Axis | Short form | Action implication |
|---|---|---|
| Understandable | "shout what it tests" | fix naming lies, strip Mystery Guest |
| Maintainable | "easy to change the code under test" | weaken coupling to internals |
| Repeatable | "same answer every time" | kill time/RNG/order/fs deps |
| Atomic | "stand alone" | kill shared state, inter-test deps |
| Necessary | "different perspective from other tests" | **dedup & regroup** — the main ask |
| Granular | "one outcome per test" | split Eager / Assertion Roulette |
| Fast | "runs after tiny edits" | demote build-smoke out of unit tier |
| Simple | "cyclomatic 1" | kill conditional-test-logic |

### citypaul's contributions

- `test-design-reviewer`: reviews against Farley's 8 with a weighted score.
  **Good for "is this suite any good?" — wrong shape for "make it one step
  better."**
- `refactoring`: **"DRY = knowledge, not code. Don't extract purely for
  testability."** This is the governor on deduping; it rules out a large
  class of bad LLM moves.
- `planning` (RED-GREEN-MUTATE-KILL-REFACTOR): **mutation strength as the
  commit-gate before structural refactor.** This is exactly the safety
  architecture we want to inherit — mutation survival as a prerequisite,
  not as the deliverable.

### `alf-test-design-reviewer` — the closest rival, still a reviewer

[`a4al6a/claude-code-agents/alf-test-design-reviewer`](https://github.com/a4al6a/claude-code-agents/tree/main/alf-test-design-reviewer)
is a substantially more developed descendant of citypaul's skill.
Everything below is worth adopting *verbatim* where it fits; the
critical point is that alf, like its predecessor, still *rates* the
suite. It emits a Farley Index and a set of worst offenders; it does
not emit a plan, it does not propose behavior-preserving edits with
per-edit rationale, it does not do semantic redundancy clustering, and
it does not relocate tests. The transform/review split stands.

**Pieces to steal wholesale:**

- **Tautology Theatre as a unifying rubric.** alf names the category
  and gives it the operational test — *"Would this test still pass
  if all production code were deleted?"* That single question unifies
  this document's §4.3 (vacuous), §4.4 (pseudo-tested), and §4.7
  (verifies-the-mock) under one reader-visible concept. The four
  subtypes alf specifies are:
  - **Mock Tautology** — configure a mock to return X, assert the
    mock returns X, with no SUT call between them. Logically
    `x = 5; assert x == 5`.
  - **Mock-Only Test** — every object in the test is a mock; the test
    exercises only the mocking framework.
  - **Trivial Tautology** — `assertTrue(true)`, `assertEquals(1, 1)`,
    `assertNotNull(new Object())`.
  - **Framework Test** — asserts on language/framework behavior, not
    application behavior (`assertNotNull(mock(Foo.class))`).

- **Mock Anti-Patterns AP1–AP4**, with severity grades:
  - **AP1 Mock Tautology** (Critical) — as above.
  - **AP2 No Production Code Exercised** (Critical) — no real class
    instantiated.
  - **AP3 Over-Specified Interactions** (High) — exact call counts,
    strict ordering, `verifyNoMoreInteractions`, numeric indices into
    `mock.calls[N]`.
  - **AP4 Testing Internal Details** (High) — `ArgumentCaptor` deep
    inspection, `verify(never())` mirroring private branches, type
    assertions.

  This crystallizes this document's §4.7 into four named, severity-graded
  shapes. Adopt the names; adopt the severities.

- **Per-method granularity with LOC-weighted aggregation** (means for
  positives, P90 for negatives). The P90-for-negatives move is subtle
  and correct: worst offenders must surface through aggregation, not
  be smoothed away.

- **60/40 static/LLM blend** per property. alf's position is that
  static detection carries more signal (60%) than LLM assessment (40%)
  except for T (First/TDD), where LLM is more reliable. This is
  directly applicable to our detection heuristics in §4; **adopt as
  the default when a pass needs to score before acting**, but note
  that our primary deliverable is edits, not scores.

- **Conservative 5.0 base score** for no-signal properties — "no
  signal ≠ good," a small but real discipline that prevents the false
  green-light failure mode.

- **Language-aware framework detection before signal scanning.** Don't
  run Java patterns on Python. alf's `signal-detection-patterns` skill
  covers nine mocking frameworks across five languages; we should
  consume or redistribute that skill directly rather than re-deriving
  per-ecosystem signals.

- **Deterministic SHA-256 sampling** past a threshold (alf uses 30% at
  >50 files). Solves the "repeatable analysis" problem without running
  on the whole suite every time.

- **Hygiene-vs-Value split.** alf separates test-hygiene (structural
  quality, the classical Farley 8) from test-value (mutation score,
  bug-catch history). A suite can be hygienic theater. Name-check this
  distinction in any user-facing output.

- **Test-pyramid shape audit** and **property-based vs example-based
  mix audit.** Both are one-shot scans with clear prescriptive
  outputs; they compose cheaply with our §4.2 Wrong-Level work.

**Where alf stops and our doc goes further:**

- No semantic-equivalence clustering. alf can't tell you "these five
  tests verify the same behavior; keep this one because X." That's
  our §4.1 and the headline ask.
- No wrong-location detection. alf has a pyramid-shape audit, but
  doesn't say "this test belongs in `foo.integration.test.ts`, not
  `foo.test.ts`, because Y." That's our §4.2.
- No edit proposals. alf outputs Farley Index + recommendations in
  prose; it does not emit mechanical transforms, does not run a
  mutation-kill gate, does not produce per-edit commits with rationale.
- No describe-before-edit CoT scaffold. alf scores; it doesn't force
  the LLM to state the test's intended behavior as a prerequisite for
  touching it.
- No citypaul-governor codification. alf's recommendations can easily
  propose "extract for testability" moves; our doc explicitly forbids
  that class.

### The gap this document fills

`test-design-reviewer` and `alf-test-design-reviewer` *rate*. We need
a system that *transforms*, one pass at a time, with each edit
justified in prose and gated by objective preservation checks.

alf's Tautology Theatre framing and AP1–AP4 taxonomy are the cleanest
published detection vocabulary; we adopt them and extend past the
reviewer/transformer line.

---

## 3. The texarkanine corpus — what actually goes wrong

Surveyed 11 qualifying repos (TS/JS, Ruby/RSpec, Python/pytest): `a16n`,
`claude-code-action`, `inquirerjs-checkbox-search`, `bbill-tracker`,
`tab-yeet`, `nervouscsstem`, `jsonschema2md`, `jekyll-mermaid-prebuild`,
`jekyll-auto-thumbnails`, `jekyll-highlight-cards`, `cursor-warehouse`.

Every concrete failure mode we found is cited with `repo/file:line` so
this document can be re-walked later. The taxonomy below is sorted by
**how LLM-native the required judgment is** — #1 is the thing no tool can
do, #10 is close to what linters already catch and we note it only for
completeness.

---

## 4. Taxonomy — ten articulable failure modes, each L/D/F/P-scored

*Each entry has:*
*Name · LLM-native move · Detection heuristic · Fix recipe · Polyglot notes · Evidence citations*

---

### 4.1 — **Semantic Redundancy, Canonicalize-and-Delete**

*The headline ask. "These 2–5 tests exercise the same observable
behavior; one is the best home; the others can merge into it, or be
deleted with a rationale."*

**LLM-native move.** Cluster tests by a *describe-the-behavior-in-one-sentence*
prompt (ChatTester-style describe-before-test, applied retroactively), then
cluster sentences by embedding similarity, then reason about which cluster
member has (a) the most precise name, (b) the smallest fixture surface,
(c) the strongest assertion, (d) the most natural layer. Keep that one.
Delete or fold the rest with an explicit "because X, not Y" paragraph.

**Detection heuristic.**

1. *Intra-file*: adjacent `it`/`test`/`def test_` blocks that call the same
   SUT entry point with identical arguments, with assertion sets that
   are subsets of each other.
2. *Intra-suite*: semantic clusters of behavior-sentences (cosine sim ≥ τ
   over a CodeBERT/embedding model, applied to the LLM-generated intent
   docstring, not the test body). **Use embedding, not AST, because
   different mocks can hide same-behavior tests.**
3. *Cross-file asymmetric-strength pairs*: when two tests cover inverse /
   parallel operations and one has a strictly weaker oracle, either
   canonicalize toward the stronger, or split the weaker pair into a named
   gap.

**Fix recipe.**

- Emit a **decision record** per cluster: `keep: path:line (reason)`,
  `fold-into-keep: path:line (reason)`, `delete: path:line (reason)`.
- Mechanical transforms: delete the test, move the test to the canonical
  file, rename to express the deduplicated intent, or absorb the weaker
  test's unique assertion into the canonical body.
- Gate: total mutation score and per-mutant kill set **must not shrink**
  after the edit. Lost coverage = veto.

**Polyglot?** Yes. Embeddings are language-agnostic; the docstring-first
prompt works identically in any test runner; the mutation gate plugs the
per-ecosystem tool. This is the single most polyglot move in the taxonomy.

**Evidence.**

- `a16n/packages/plugin-a16n/test/parse.test.ts:51-69` — two `it` blocks
  both call `parseIRFile(ws, 'parse-fileRule/typescript.md', ...)`; the
  second is a strict subset of the first.
- `a16n/packages/engine/test/engine.test.ts:231-263` — asymmetric
  strength: cursor→claude reads file contents; claude→cursor only checks
  `files.length > 0`.
- `jsonschema2md/test/api.test.js` + `test/testintegration.test.js` —
  both paths cover "process fixtures → README exists" against the same
  `tmp` tree; either the API test can be narrowed or the integration
  test is the sole oracle.
- Jekyll-gem cross-repo: `jekyll-mermaid-prebuild/spec/jekyll_mermaid_prebuild/digest_calculator_spec.rb:5-35`
  is a structural copy of `jekyll-auto-thumbnails/spec/digest_calculator_spec.rb:5-54`
  — same test arc (shape / stable / divergent) with cosmetic API drift.
- Within `jekyll-highlight-cards`: `linkcard_tag_spec.rb:11-22` vs
  `polaroid_tag_spec.rb:10-22` — same setup with drifted accessor
  (`instance_variable_set` vs public writer). One canonical `before`.

---

### 4.2 — **Wrong-Level / Wrong-Location**

*The "it belongs in this one specific place" half of the ask. Distinct
from 4.1 because the test itself may be fine — it just lives in the
wrong layer.*

**LLM-native move.** Decide, per test, whether it is *unit* (pure
function, small surface), *component* (module-with-fakes), or
*integration* (real adapter + temp dir + process boundary). Compare to
where it lives and where its siblings live.

**Detection heuristic.**

- A single test file imports both `@inquirer/testing`-style rendering
  harnesses *and* pure computed exports.
- A unit-flavored test wraps `execSync('npm run build')` or
  `subprocess.run([...])`.
- A "unit" test mocks every dependency and then asserts on
  `toHaveBeenCalledWith(...)` argv shape — that's a *contract* test,
  mis-named.
- A spec file `send`s to private methods (`described_class.send(:foo, x)`)
  — that's either "should be public," "should move to a per-unit spec
  for the pure helper," or "should be deleted and covered via integration."

**Fix recipe.**

- Split the file by level (`foo.test.ts` → `foo.unit.test.ts` +
  `foo.integration.test.ts`). If the runner already has markers (`@slow`,
  `@integration`, `-tags=integration`), apply those too.
- Move build-smokes out of the unit tier (separate CI job, or mark
  `slow`).
- Convert `send(:private_method, ...)` to (a) invocation through the
  public surface, or (b) extraction of the private helper as a pure
  function with its own tiny unit test file. (This is the *only*
  refactoring-for-testability move we allow, and only because it also
  clarifies architecture.)

**Polyglot?** Yes. The layer vocabulary is universal; the markers differ
per runner and are easily looked up. *Do not* try to enforce a global
layer policy — read the existing conventions in the repo first.

**Evidence.**

- `inquirerjs-checkbox-search/src/__tests__/page-sizing.test.ts:6-165`
  — `render(checkboxSearch, ...)` (integration) nested next to a
  `describe('calculateDynamicPageSize')` unit block.
- `nervouscsstem/test/foundation.test.mjs:25-35` — `describe('Build
  smoke tests')` runs `execSync('npm run build')` inside the unit file.
- `jekyll-auto-thumbnails/spec/hooks_spec.rb:115-123` — `described_class.send(:html_document?, ...)`
  on a private predicate.

---

### 4.3 — **Vacuous / Assertion-Shaped-Like-Nothing**

*The test asserts, but the assertion could not distinguish a working
implementation from a broken one.*

*Adopt alf's **Tautology Theatre** framing here: would this test still
pass if all production code were deleted? If yes, it's theatre. This
entry covers the "technically runs SUT but asserts nothing meaningful"
subset; for the "never touches SUT at all" subset, see §4.7 (AP1
Mock Tautology) and §4.4 (pseudo-tested).*

**LLM-native move.** Reading the assertion against the SUT, ask "what
minimal wrong answer would this still accept?" If many interesting wrong
answers pass, the assertion is vacuous. The LLM is better at this than
static tools because it understands the domain of the return value.

**Detection heuristic.**

- `expect(x).toBeDefined()` immediately followed by `x!.y.z` — the
  dereference is the real assertion; the first line is dead weight.
- `expect(x).toBeTruthy()` on a value with known format (UUID, URL, date,
  enum).
- `assert result is not None` or `assert len(x) > 0` as the *only*
  assertion.
- `expect(obj).toBeInstanceOf(Array)` or `be_a(String)` where an exact
  value is knowable.
- `assert(result === Object(result))` — an identity check that passes
  for any object.
- `assert.ok(file.isFile())` + `assert.notStrictEqual(file.size, 0)` —
  non-empty, wrong-content passes.
- `expect { ... }.not_to raise_error` as the whole `it` body, when the
  real claim is "does not *do* Y" (a side-effect absence).
- `expect(match).not_to be_nil` as the gate before using `match[2]`.

**Fix recipe — *strengthen, don't multiply*.** Prefer the one strongest
check. Concretely:

- Collapse `toBeDefined` + `x!.foo === 'bar'` to `expect(x).toEqual(expect.objectContaining({ foo: 'bar' }))`
  or `toMatchObject({ foo: 'bar' })`.
- Replace "non-empty file" with a parse-and-assert-shape, or a
  normalized-content comparison to a fixture.
- Replace `.not_to raise_error` with `.not_to have_received(:cp)` /
  absence-of-side-effect check, which is what the docstring said.
- Replace `assert "12" in out` with full-string or regex equality.

**Polyglot?** Yes. The *list of weak assertion shapes* is per-runner, but
the detection logic ("weakest-test-that-still-distinguishes") is the same
everywhere.

**Evidence.**

- `a16n/packages/plugin-claude/test/discover.test.ts:94-100` — `toBeDefined`
  then immediate `.description`.
- `inquirerjs-checkbox-search/src/__tests__/descriptions.test.ts:71-74`
  — `toBeTruthy` on `find(...)`.
- `jsonschema2md/test/api.test.js:51-52` — `assert(result === Object(result))`.
- `cursor-warehouse/tests/test_sync.py:221-231` — `test_string_content_handled`
  asserts only `len(rows) > 0`.
- `cursor-warehouse/tests/test_sync.py:1340-1356` — ISO8601 test uses
  `"12" in out`.
- `jekyll-mermaid-prebuild/spec/.../hooks_spec.rb:72-90` —
  `.not_to raise_error` as sole assertion for "does nothing."

---

### 4.4 — **Pseudo-Tested / Null-Op Survivor**

*A close cousin of §4.3, but the signal is behavioral: replace the SUT
body with `return;` / `return null` / `return input` — no test fails.
This is Niedermayr's extreme mutation, used as a cheap LLM-visible
signal.*

*This is the mutation-adjacent sibling of alf's Tautology Theatre.
alf's operational test ("would it pass if prod code were deleted?") is
a strict-superset of this one ("would it pass if prod code were
no-opped?"); Niedermayr adds the cheap mechanization.*

**LLM-native move.** The LLM can *conjecture* without running the
mutator: "if `short_digest` returned `''`, would any existing test
fail?" Read the suite, answer yes/no, and (a) add the missing assertion
to the canonical test, (b) mark this as a mutation-score candidate for
the automated pass to confirm.

**Detection heuristic.**

- The LLM generates the null-op mutants itself for the top N public
  methods and simulates which tests would catch each (cheap, no
  runtime cost). This is cross-checked by whatever real mutation tool
  the repo uses on Tier-2 passes.
- Heuristic shortcut: test body calls SUT, assigns to `_`, then only
  runs structural shape/type/length checks.

**Fix recipe.** Strengthen the canonical test's oracle (see §4.3's fix
recipe) so at least one null-op mutant is killed. Keep the fix local —
don't add N mutant-killers across N tests if one well-placed assertion
in the canonical location suffices.

**Polyglot?** Yes. Every ecosystem has at least one extreme-mutation tool
or can be nudged with a 10-line "replace body with `return default`"
codemod.

**Evidence.**

- `cursor-warehouse/tests/test_sync.py:844-861` — `test_corrupt_tracking_db_graceful_skip`
  has no post-call assertion; `sync_tracking_db` could be a no-op and
  this test still passes.
- `a16n/packages/engine/test/engine.test.ts:260-263` — emitter could
  write empty files; test only checks directory is non-empty.
- `jekyll-mermaid-prebuild/spec/.../processor_spec.rb:70-75` — `svgs`
  emitter could return a single junk entry; test only checks
  non-empty.

---

### 4.5 — **Naming Lies / Docstring Drift**

*Test title claims X; body verifies Y.*

**LLM-native move.** LLMs parse natural language. Static tools cannot
tell that `it('should use cyan/blue styling for descriptions')`
doesn't check ANSI escape codes. An LLM can.

**Detection heuristic.**

- Tokenize the test title/docstring; tokenize the assertion lines;
  look for title-nouns that have zero surface in the assertion set.
- If the title contains `color | ANSI | styling | cyan | bold | italic`
  but the body has no ANSI-regex or theme mock — flag.
- If the docstring claims "defaults to zero" but the body never compares
  to zero — flag.
- If the docstring claims a derivation rule ("last path segment of the
  workspace slug") but the assertion is `len(row[0]) > 0` — flag.

**Fix recipe.** Either *rename the test* to describe what it actually
does (usually the cheaper fix if the body is already strong), or
*strengthen the body* to match the title (if the body is weak — overlaps
with §4.3).

**Polyglot?** Yes. Trivially.

**Evidence.**

- `inquirerjs-checkbox-search/src/__tests__/descriptions.test.ts:56-66`
  — `should use cyan/blue styling` asserts only `toContain('Red fruit')`.
- `cursor-warehouse/tests/test_sync.py:250-260` — `test_token_counts_default_to_zero`
  asserts only `row[0] > 0` on a count query.
- `amazon-cpi/tests/test_price_extractor.py:24-28` —
  `test_get_random_user_agent` checks prefix + length only; "random"
  never verified.
- `cursor-warehouse/tests/test_sync.py:626-648` — docstring claims
  derivation from workspace-slug's last segment; asserts only
  non-empty.

---

### 4.6 — **Conditional Test Logic**

*`if X: assert(...)` inside a test body. Farley-Simple-≠-1.*

**LLM-native move.** Decide, per branch, whether the `if` encodes
genuine optionality (→ split into two tests with preconditions) or
is compensating for an upstream oracle weakness (→ remove the `if`,
pin the precondition in the fixture, assert unconditionally).

**Detection heuristic.**

- AST: `IfStatement` inside a `CallExpression` whose callee matches
  the test-function regex for the runner; consequent contains `expect`
  / `assert`; alternate absent or contains no assertions.
- `try { sut() } catch(e) { assert(e.message === ...) }` without an
  `assert.fail('should have thrown')` after the `try`. The catch is
  conditional on the throw actually happening.
- `if (process.platform === 'win32') return;` — platform skip expressed
  as body logic, not `it.skip` / `pytest.skip`.

**Fix recipe.**

- `if (condition) expect(...)` → either split, or fix the scenario so
  the condition is guaranteed.
- `try/catch` → `expect(...).toThrow(...)` / `pytest.raises` /
  `expect { ... }.to raise_error(... /msg/)`.
- Platform branches → runner-native skip with a reason string that will
  show in test output.

**Polyglot?** Yes.

**Evidence.**

- `claude-code-action/test/prepare-context.test.ts:56-69` — big block of
  `if (result.eventData.eventName === "issue_comment") { expect... }`.
- `bbill-tracker/test/unit/GraphVisualization.test.js:110-119` — `if
  (graphData.edges.length > 0) { ... }`; combined with
  `toBeGreaterThanOrEqual(0)` the test passes vacuously on empty graph.
- `jsonschema2md/test/api.test.js:143-151` — `try { sut() } catch {
  assert.strictEqual(e.message, ...) }` with no `assert.fail` after
  `try`.
- `jsonschema2md/test/api.test.js:154-168` — `if (process.platform ===
  'win32') return;` inside an `it` body.

---

### 4.7 — **Verifies-the-Mock, Not the Behavior**

*Mock setup is the test. The SUT could be stubbed to noop and it still
passes.*

*This entry maps directly onto alf's AP1–AP4. Use alf's names in
user-facing output:*

- *Configure-then-assert-same-mock-with-no-SUT-in-between → **AP1
  Mock Tautology** (Critical).*
- *All-objects-are-mocks → **AP2 No Production Code Exercised**
  (Critical).*
- *Numeric `mock.calls[0][N]` indices, strict ordering,
  `verifyNoMoreInteractions`, ordered `mockResolvedValueOnce` queues
  → **AP3 Over-Specified Interactions** (High).*
- *`ArgumentCaptor` deep inspection, `verify(never())` mirroring
  production branches, `toHaveBeenCalledWith` pinning magic
  constants → **AP4 Testing Internal Details** (High).*

**LLM-native move.** For each mock assertion, ask: "if the SUT were
deleted and only the mock setup remained, what would fail?" The amount
of work the SUT is shown to do is the test's real strength.

**Detection heuristic.**

- `jest.spyOn(sutInstance, 'method').mockReturnValue(...)` within the
  same test file that imports that class — **mocking the unit under
  test**. Nearly always wrong.
- Numeric index into `mock.calls[0][N]` for `N ≥ 2` — brittle
  signature-shape coupling.
- Cascades of `mockResolvedValueOnce(...)` where reordering internal
  calls breaks the test but doesn't change observable behavior.
- Mock-verification tail that duplicates an expectation already inside
  a stub's callback (`have_received(:generate)` after `allow(generator).to
  receive(:generate) do |src| expect(src).to include(...) end`).
- Assertions on `toHaveBeenCalledWith("/tmp/github-images", ...)` — the
  path is a production constant baked into the test.

**Fix recipe.**

- Replace `spyOn(sut, 'method')` with a fixture that makes `method`
  return the desired value naturally.
- Replace index-into-`calls` with matcher-based `toHaveBeenCalledWith(
  expect.anything(), expect.stringContaining('5000'), ...)` so
  argument order can change.
- Replace ordered `mockResolvedValueOnce` queues with a lookup-keyed
  fake (`(txid) => fixtures[txid]`).
- For mock-queues-as-contract: extract a minimal `Fake<Client>` class
  once per suite; tests reference its behavior, not the queue.

**Polyglot?** Yes. The "mock of the SUT" pattern is universal
(monkeypatch `self.method` in Python, `instance_double(self.class)` in
Ruby, `gomock` on concrete types, etc.).

**Evidence.**

- `bbill-tracker/test/unit/BitcoinBillDetector.test.js:40-48` —
  `jest.spyOn(detector, 'isFeePayment').mockReturnValue(false)` inside
  the detector's own test file.
- `bbill-tracker/test/unit/TransactionChainTraverser.test.js:543-548`
  — `cacheCall[2]`, `cacheCall[3]` positional index into mock calls.
- `bbill-tracker/test/unit/TransactionChainTraverser.test.js:17-42`
  — paired `mockResolvedValueOnce` calls that must match production
  call order.
- `jekyll-mermaid-prebuild/spec/.../processor_spec.rb:127-150` —
  `have_received(:generate)` tail after a stub block that already
  asserts on `source`.
- `claude-code-action/test/image-downloader.test.ts:68-72` —
  `toHaveBeenCalledWith("/tmp/github-images", ...)`.

---

### 4.8 — **Brittle-to-Internal-Rename / Third-Party-Internal Coupling**

*The test reaches through a public type into a private or undocumented
implementation shape.*

**LLM-native move.** Identify whether the accessed field is part of the
stable public API of the library / module in question. Libraries have
docs; the LLM has read them.

**Detection heuristic.**

- `(x as any).someProp`, `x['_private']`, `x.#field`, `described_class.send(:private_method, ...)`
  — direct syntactic signals.
- Accessors whose names start with `_` or match known-private
  conventions in the ecosystem.
- For third-party libraries: the field doesn't appear in the library's
  exported types / public docs. (LLM can check.)

**Fix recipe.**

- Drive the library's public API instead (`program.helpInformation()`
  instead of `(cmd as any).options`).
- If the private field encodes a real contract, ask the upstream
  library to expose it, or encapsulate behind a helper in the project
  so the coupling lives in one place.

**Polyglot?** Yes, with one caveat: *what counts as "private"* is a
per-language convention the LLM must know (Ruby visibility vs Python
`_` vs TS `private` vs Go uppercase-vs-lowercase export).

**Evidence.**

- `a16n/packages/cli/test/create-program.test.ts:15-18` — `(cmd as
  any).options` to read Commander internals.
- `claude-code-action/test/mockContext.ts:37-38` and
  `test/data-formatter.test.ts:35-36` — `{} as any` /
  `{} as GitHubFile` casts that silently turn type errors into test
  problems.
- `jekyll-auto-thumbnails/spec/hooks_spec.rb:115-123` —
  `described_class.send(:html_document?, ...)`.

---

### 4.9 — **Shared State / Order Dependence**

*Farley-Atomic violated via module-level mutables, fixture leaks, and
implicit ordering between describes.*

**LLM-native move.** Trace write/read reachability of each mutable
top-level binding across the suite. An LLM reading the imports + the
`before`/`beforeEach`/`beforeAll`/`before(:suite)` blocks can build
this graph quickly; a linter has to solve scope-aware data flow.

**Detection heuristic.**

- File-level `let` / `const` bound to a `new SUT()`, `new Engine()`,
  `createClient()` — used by many `it` blocks with no `beforeEach`
  factory.
- `@temp_dir` created in `before(:suite)` and read in test bodies
  (worse: created and *never* read — genuine dead setup).
- `let css = ''` written in one `describe`, read in another, with
  `if (!css) { rebuild }` lazy-init — execution-order-dependent.
- `sys.path.insert(0, ...)` / `NODE_PATH` mutation in `conftest` that
  a sibling test file *also* performs for a different reason.
- Global mutable stubs (`console.warn = ...`) installed in a setup file
  with no per-test restore.

**Fix recipe.**

- Move setup into `beforeEach`/factory; accept the tiny perf cost.
- Delete genuinely unused shared setup (dead `@temp_dir`, unused
  `let(:doc)`).
- Install-and-restore patterns (`jest.spyOn(console, 'warn')` with
  `afterEach`) instead of mutating globals permanently.
- Collapse duplicate `sys.path` inserts into one `conftest`.

**Polyglot?** Yes.

**Evidence.**

- `a16n/packages/cli/test/integration/integration.test.ts:25-26` —
  `const engine = new A16nEngine(...)` at module scope.
- `nervouscsstem/test/foundation.test.mjs:23, 37-40, 79-85` — `let
  css = ''` at module level, lazy-populated across describes.
- `jekyll-auto-thumbnails/spec/spec_helper.rb:29-36` — `@temp_dir`
  created in `before(:suite)`, **read nowhere in `spec/`**.
- `cursor-warehouse/tests/conftest.py:8-12` vs `tests/test_embed.py:6-7`
  — `sys.path` inserted in two places.
- `bbill-tracker/test/setupTests.js:13-22` — global `console.warn`
  replacement without per-test restore.

---

### 4.10 — **Mystery Guest / Under-Documented Fixture**

*The test body's meaning lives in an external file. Without opening
that file, the reader cannot tell what's being verified.*

**LLM-native move.** When a test reads a fixture, the LLM can (a)
summarize the fixture's relevant shape in one sentence, (b) emit that
sentence as an inline comment or a `let`/`const` docstring at the
assertion site, without moving the fixture.

**Detection heuristic.**

- Test body: `FIXTURES_DIR / "X.jsonl"` then `assert count == 6` with
  no hint *why* 6.
- `<<~MARKDOWN ... 500 chars ...` heredoc as `let` input with no name
  explaining the relevant feature.
- `File.read(...)` with no inline comment about what part of the file
  matters.

**Fix recipe.**

- Add a ≤3-line comment stating the relevant fixture shape, not the
  whole shape.
- Where fixtures are copy-paste shared across repos (Jekyll-gem
  family), extract a tiny support file; otherwise leave files alone.
- Where assertion expects a derived magic number (`6 == 3 users + 3
  assistants`), express the derivation inline: `expected = USERS +
  ASSISTANTS`.

**Polyglot?** Yes. This is one of the lowest-risk, highest-understandability
moves in the taxonomy.

**Evidence.**

- `cursor-warehouse/tests/test_sync.py:113-120` — `assert msg_count == 6`
  with `# 3 user + 3 assistant messages` as the only hint; applied
  across many tests referencing the same fixture.
- `jekyll-mermaid-prebuild/spec/.../processor_spec.rb:19-32` — long
  inline heredoc in `let` with no name.

---

### 4.11 — **Rotten Green & Dead Scaffolding** *(bonus)*

*Test reports green without actually exercising anything.*

Already covered in spirit by 4.3/4.4/4.9, but worth separating because
the signal is syntactic and extremely cheap:

- Empty `it()` / `test()` bodies with only `// TODO` comments that
  still count as passing tests (linter `expect-expect` catches some).
- `let(:doc)` / fixtures declared and never referenced.
- Integration fixture dirs (`to-claude/`, `to-cursor/`) that the test
  never reads (`toDir` computed and dropped).
- `console.log('done!', res)` left in test bodies — signal the author
  stopped iterating before landing a real assertion.

**Evidence.** `bbill-tracker/test/unit/MempoolApiClient.test.js:16-35`,
`jekyll-auto-thumbnails/spec/hooks_spec.rb:14`,
`a16n/packages/cli/test/integration/integration.test.ts:99-104` (unused
`toDir`), `jsonschema2md/test/testintegration.test.js:66-70` (debug
`console.log`).

**Polyglot? Yes** — trivially.

---

## 5. What an LLM "pass" looks like

A pass over one repo produces a **plan artifact** and a **change set**,
not one monolithic PR. The plan is itself reviewable and mergeable
independently of the edits.

### Inputs

1. Repo working tree.
2. Existing linter / mutation / coverage results if present (read-only;
   we don't invoke them ourselves per the user's constraint).
3. A heuristic-selected subset of ≤ N test files (default 5–10), scored
   by a cheap bait: files with the most weak-assertion patterns + the
   most `let`/`const` sharing + the most fixture references. Avoid
   operating over the whole suite in one pass — this is the entire
   point of iterating.

### The pass itself (CoT, not hidden)

Adopt UTRefactor's five-step chain, adapted, with alf's static/LLM
blend driving step 3:

1. **Describe-before-edit** — for each test in scope, generate a
   one-sentence behavior docstring. Store as a machine-readable side
   table and also insert as a docblock. *This step alone resolves many
   naming-lies without any transform.*
2. **Cluster** — embed those sentences; cluster. Each cluster is a
   candidate for §4.1 work.
3. **Identify failure modes** — walk the 10-entry taxonomy above per
   test (not per cluster). For each entry, run **static detection
   first** (alf's `signal-detection-patterns` per language), **then
   LLM semantic assessment**, blended 60/40 static/LLM except for
   failure modes that are primarily semantic (§4.1 Redundancy, §4.2
   Wrong-Location, §4.5 Naming Lies, §4.10 Mystery Guest — blend
   40/60 or pure-LLM). Run the **Tautology Theatre gate** from alf
   explicitly: "would this test still pass if all production code
   were deleted?" Tag AP1–AP4 with Critical/High severities.
   Output: `{file:line, mode, severity, static_score, llm_score,
   proposed_move}`.
4. **Plan** — for each finding, emit a **plan entry**:
   ```
   finding: <taxonomy id>
   locus: <file:line range>
   move: delete | fold-into | rename | strengthen-assertion | split | move-layer | replace-mock | add-fixture-comment
   target: <file:line, if move=fold-into/move-layer>
   reason: <prose, 1-3 sentences — the rationale layer>
   preservation: <which mutation-test IDs or lint-suppression markers this must preserve>
   ```
5. **Validate** — run the repo's own test+coverage+mutation commands
   after each edit. Any edit that reduces per-test mutation kills or
   coverage **without rationale** is rolled back.

### Outputs

- **`plan.md`** — the list of plan entries, grouped by taxonomy class.
- **Per-edit commits**, each with the `reason:` field verbatim in the
  commit body. (This is the rationale layer from §7 of `report.md`.)
- **A changelog** listing renames, moves, and deletions so that reviewers
  can answer "where did `test_foo` go?" without running `git log -S`.

### Guardrails (non-negotiable — these rule out a huge class of bad moves)

- **Do not extract purely for testability** — citypaul's refactoring
  rule. Split SUT code for readability or DRY-of-knowledge, never for
  "so we can unit test it."
- **Do not dedup across genuinely different concepts** — citypaul's
  "DRY = knowledge, not code" rule. Two tests that *look* similar but
  cover different requirements do not get merged.
- **Do not invent tests.** A pass that adds tests is a different pass
  (test generation); this one only *improves* existing ones, which
  includes deleting bad ones.
- **Do not reduce mutation coverage.** Hard gate.
- **Do not reduce coverage without marking the deleted test as
  "duplicate of X" in the commit.** Coverage can legitimately drop when
  redundant tests are deleted; the rationale must name the absorber.
- **Cap total edits per pass.** A pass that proposes 200 changes is
  ungovernable. Prefer 10–30 reviewable moves; the next pass picks up
  where this one left off.

---

## 6. What makes a pass "successful"

Not "smells decreased." Not "Farley score went up." Those are the
metrics `report.md` already warned against.

### Primary success signals (per pass)

1. **Preserved mutation kill-set** (no regression in which mutants die).
2. **Strict subset of edits accepted by review**, with the rationale
   paragraph surviving unedited — the rationale is the product.
3. **Per-test docstring coverage** before vs after: every touched test
   has a one-sentence docstring that survives.
4. **Intent-cluster entropy** (roughly: are tests grouped by behavior,
   or by accident-of-history?). Computable from the embedding pass;
   trend it across passes.

### Secondary signals (informational only)

- Linter violations resolved *as a side effect of* a semantic move.
  (Don't target these directly; the repo's linter is in charge.)
- Build time reduction from wrong-level demotion.
- **Tautology Theatre count** (alf's four subtypes, summed with
  severities) trending down. Worth trending because it's reader-visible
  and the operational test ("prod code deleted → still passes?") is
  cheap to sanity-check. Report alongside the edit set, not as a
  primary KPI — a pass may legitimately strengthen assertions without
  reducing the count if it moves a test out of AP3 into a still-imperfect
  AP4, etc.
- **Hygiene-vs-value separation**, per alf: improvements to test
  *hygiene* (structure, naming, isolation) vs *value* (mutation
  kills, bug-catch). A pass that only improves hygiene should say so.
  A pass that claims value improvements without mutation evidence
  should be distrusted.

### Anti-signals (things we explicitly *don't* optimize)

- Raw test-count reduction. The goal isn't fewer tests; it's better ones.
- Smell-count reduction per TsDetect-class tools (EMSE 2023 warning).
- Coverage increase. A pass that improves tests but doesn't change coverage
  is a completely legitimate pass.

---

## 7. Non-goals, explicit

Re-stating the user's frame, in one place, so the next pass doesn't drift:

- **No linter orchestration.** The repo picks its own. We consume its
  output if present; we don't pick.
- **No fixed language set.** The taxonomy must be language-independent;
  bindings to runner conventions are thin adapters.
- **No SaaS dashboard, no cloud.** The pass runs locally, with the LLM
  the user is already using.
- **No new test generation.** Separate concern; handled by CoverUp,
  TestGen-LLM, etc.
- **No migration-as-primary.** JUnit4→5, Jest→Vitest, etc. is
  migration-work, not suite-curation; use OpenRewrite / jest-codemods
  directly for that.
- **No Farley scoreboard.** We use his axes for judgment, not for UX.

---

## 8. Open questions / gaps the audit surfaced

1. **How do we decide the "canonical" location for a clustered
   behavior?** Heuristics we have so far: most-public layer, smallest
   fixture surface, best name. What's the tie-breaker? Probably "the
   test file whose per-file behavior-docstring is most coherent with
   this cluster's centroid," but that wants validation on real PR
   review outcomes.

2. **Embedding-based clustering quality.** LTM (arXiv 2304.01397) shows
   CodeBERT + GA works for *test minimization* (keep coverage-preserving
   subsets). Does it transfer to *canonicalization decisions*? Maybe;
   needs a small labeled study on one of these repos.

3. **The "intentional duplication" trap.** `tab-yeet` intentionally
   duplicates `STORAGE_KEYS` in tests as a contract check. An LLM
   tempted to "dedup" this would break the guard. Detection: any
   duplicated literal whose home is *production code the test is
   meant to guard*. Explicit allowlist or metacomment
   (`# test-design: contract-duplication`) required.

4. **Cross-repo passes.** The three Jekyll gems share `spec_helper`
   wholesale. A "pass" scoped to one repo can't do anything about
   that; a meta-pass across a family of repos could extract a shared
   gem. That's a different feature; note, don't block on it.

5. **Mutation cost on large suites.** Running Stryker / mutmut / PIT
   per proposed edit is expensive. Descartes-style extreme mutation
   (Niedermayr) is cheap enough. Can we use extreme mutation as the
   per-edit gate and reserve full mutation for the end-of-pass check?
   Probably yes.

6. **When is a `not_to raise_error` test *right*?** If the documented
   contract is "this function swallows errors by design," the absence
   of raise *is* the behavior. Heuristic: if the docstring/name says
   "does nothing" and the function has no side effects, `.not_to
   raise_error` is still vacuous; if it says "swallows I/O errors" or
   "returns None on failure," pair with a positive assertion on the
   return/state.

7. **The "LLM judges the LLM" equivalent-mutant problem** (ACH, FSE
   2025). When the LLM proposes strengthening an assertion to kill a
   mutant, and a later mutation run finds that same assertion kills
   two mutants, one of which is equivalent-by-construction — do we
   count that as progress? Meta achieved 0.79 precision on
   equivalent-mutant filtering; we should be conservative and accept
   higher false-negative rates.

8. **Two-tier or not?** `report.md` frames this as
   "cleanup (Tier 1) vs architectural (Tier 2)." The audit supports
   that: 4.1–4.6 are mostly Tier 1; 4.7–4.9 straddle; functional
   regrouping (the "wholly reorganized suite" idea) is Tier 2. Worth
   deciding whether this doc's 10-entry taxonomy maps cleanly onto
   the two tiers, or whether we want a three-tier split
   (cleanup / assertion-strengthening / architectural).

9. **Pair with alf, don't replace.** A useful shipping model: alf runs
   as the *review* / scoring pass and emits its JSON (`farley_index`,
   per-property scores, tautology counts, worst-offender list); our
   transform pass consumes that JSON as its priority queue, proposes
   edits against the worst offenders, and re-runs alf after the
   validator gate to confirm the score moved in the right direction.
   The scoreboard becomes a progress indicator, not the product.
   Open question: is the alf JSON schema stable enough to depend on?
   (The repo pins it in `alf-test-design-reviewer.md`; acceptable for
   now.)

10. **Severity-aware editing order.** alf tags AP1/AP2 as Critical and
    AP3/AP4 as High. Our edit queue should respect that: Critical
    Tautology Theatre instances get proposed first regardless of which
    taxonomy entry they live under, because they represent zero-value
    tests that can often be *deleted outright*, which is the lowest-risk
    transform in the catalog. Open question: what's the right severity
    to assign to §4.1 clusters, which are about deletion *because of
    redundancy* rather than *because of vacuity*? Probably Medium until
    a human confirms the cluster interpretation.

11. **Static/LLM blend ratio per failure mode.** alf's 60/40 default
    and its T-specific inversion are defensible for scoring. For
    *acting* (our use case), the semantic entries (§4.1, §4.2, §4.5,
    §4.10) should lean LLM-heavy; the syntactic entries (§4.6, §4.8,
    §4.11) can lean static-heavy. Worth a small calibration study on
    the texarkanine corpus: does 60/40 miss things a 40/60 would
    catch, and vice versa?

---

## 9. What we'd pilot, in order

If this becomes a real thing, prove it out in this sequence (each step
is a week-to-month of work, not a session):

0. **Wire up `alf-test-design-reviewer` as the scoring oracle.** Before
   the first edit, let alf score the target suite and emit its JSON.
   Our transform pass consumes that as the priority queue; our
   validator re-runs alf post-edit to confirm the score moved. Zero
   new detection code required at this step — we're reusing existing
   prior art end-to-end.
1. **Describe-before-edit + Mystery Guest annotation (§4.10).** Lowest
   risk, immediate reader value, almost impossible to make worse.
2. **AP1/AP2 Tautology Theatre deletion (§4.3 ∩ §4.7 ∩ §4.4).** alf
   flags Critical; the transform is "delete the test, record why."
   Validator: every deletion must reduce alf's tautology count by 1
   without reducing mutation kill count. Highest-leverage, lowest-risk
   transform in the catalog.
3. **§4.5 Naming Lies + §4.3 residual vacuous assertions.** High
   value, high visibility, mutation-testable. By now we should have a
   calibrated sense of false-positive rates from the LLM.
4. **§4.1 — canonicalize-and-delete.** The headline feature. Requires
   the embedding pass + the clustering rationale + the mutation gate.
   Biggest payoff, biggest risk. Only start after the validator
   architecture has proven stable on steps 0–3.
5. **§4.2 — wrong-level moves** via `ast-grep` / `LibCST` / `jscodeshift`
   codemods driven by the plan. Consume alf's pyramid-shape audit as
   input; we decide the *moves*, alf's audit tells us *whether the
   shape improved*.
6. **AP3/AP4 (§4.7 remainder) — mock-of-the-SUT replacement.** Requires
   the repo to have a defined fake pattern; otherwise we'd be
   introducing a new abstraction, which overlaps with "don't extract
   for testability."
7. **§4.9 — shared state teardown.** Worth it, but per-ecosystem;
   save for after the polyglot core is stable.

---

## 10. TL;DR for the next pass over this document

- The unique value is **semantic moves** (cluster, canonicalize,
  relocate, rename-with-reason), not syntactic cleanup.
- Ten articulable failure modes (§4.1–§4.10 + a bonus), each
  seeable-fixable-polyglot by construction.
- Safety architecture is borrowed wholesale from citypaul's
  RED-GREEN-MUTATE-KILL-REFACTOR: **mutation kills are the gate**.
- **Detection vocabulary is borrowed wholesale from
  `alf-test-design-reviewer`**: Tautology Theatre as the unifying
  "would it pass if prod code were deleted?" rubric, AP1–AP4 as the
  named mock anti-patterns with severity grades, 60/40 static/LLM
  blend as the default scoring ratio, hygiene-vs-value as the
  two-number output shape. alf becomes the scoring oracle; we become
  the transform layer on top.
- The deliverable is a **plan artifact + per-edit rationale commits**,
  not a smell-count dashboard.
- Do not compete with linters, mutation tools, test generators, or
  reviewers like alf. Compose; the hands are mature, the brain is the
  gap.
- The Farley/Wright axes are the *judgment rubric*; the taxonomy is
  the *action list*; alf's taxonomies are the *detection vocabulary*;
  the citypaul refactoring rules are the *governor*.

---

## Appendix: sources walked

- `randommd/goodtests/report.md` (all §1–§6).
- `randommd/goodtests/farley.md` (Dave Farley, 8 properties).
- `https://medium.com/@gregwright_1301/ten-properties-of-good-unit-tests-3bbd49222754`
  (Greg Wright, props 1–8).
- `https://github.com/citypaul/.dotfiles/tree/main/claude/.claude/skills/test-design-reviewer`.
- `https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/refactoring/SKILL.md`.
- [`a4al6a/claude-code-agents/alf-test-design-reviewer`](https://github.com/a4al6a/claude-code-agents/tree/main/alf-test-design-reviewer)
  — agent definition, `docs/test-design-reviewer-research.md`,
  `docs/mock-anti-patterns-research.md`, and
  `skills/test-design-reviewer/signal-detection-patterns.md`. Source
  of Tautology Theatre and AP1–AP4.
- Direct audit of 11 `texarkanine`-owned repos with meaningful test
  suites, cited per finding above. Repos with shallow/no suites listed
  but not walked.
