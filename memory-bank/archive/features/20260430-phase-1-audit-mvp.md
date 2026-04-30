---
task_id: phase-1-audit-mvp
complexity_level: 3
date: 2026-04-30
status: completed
---

# TASK ARCHIVE: Phase 1 Audit MVP (`deliverable-fossils` + `naming-lies`)

## SUMMARY

Shipped Phase 1 of [VISION.md](../../../planning/VISION.md): a harness-portable audit skill at `skills/slobac-audit/` covering two SLOBAC taxonomy smells (`deliverable-fossils` and `naming-lies`). The audit is packaged as an AgentSkills.io-compatible `SKILL.md` + typed `references/` directory tree, runnable in both Cursor and Claude Code. It produces a portable markdown report naming each flagged test, the smell, the rationale, and the prescribed remediation. It is read-only — it never modifies test code.

The task went through four architecture passes on the core DRY question (how the skill's canonical per-smell content and the reader-facing manifesto site share one source of truth), landing on the simplest possible structure: the full manifesto lives inside the skill bundle at `skills/slobac-audit/references/docs/`, and `properdocs.yml` points its `docs_dir` directly there. No generator, no sync script, no wrappers, no indirection.

Fixtures for four test scenarios were authored (deliverable-fossils, naming-lies, both-smells, clean) with expected-findings documents following TDD discipline.

## REQUIREMENTS

### Functional

- An operator in Cursor or Claude Code can invoke the audit and scope it to one, the other, or both smells via natural-language input.
- The audit emits a portable markdown report named `slobac-audit.md` (operator-overridable) with a per-finding shape: test location, smell slug, rationale citing the canonical entry, prescribed remediation, and a false-positive guard ("why this isn't a false positive").
- The audit is read-only — it never modifies test code.
- Two smells built for real (not stubbed): `deliverable-fossils` (two-phase rename→regroup fix) and `naming-lies` (three-way rename/strengthen/investigate fix), specifically chosen to stress-test that the shared architecture accommodates genuinely different fix shapes.
- Out-of-scope slug requests are refused with a clear message rather than silently skipped.

### Design Questions Resolved

1. **Customization granularity (OQ1):** Ur-Skill with per-smell entries under `references/`, packaged as an AgentSkills.io-shaped `SKILL.md` + `references/` tree. Phase-2 extensibility: adding a smell is adding a file. Both harnesses support this primitive without harness-specific glue.

2. **Docs ↔ skill DRY mechanism (OQ2 → OQ2-redux → OQ3 → third rework, four passes):** After four architecture passes, resolved as: the skill bundle holds the full canonical manifesto at `skills/slobac-audit/references/docs/`; `properdocs.yml` `docs_dir` points directly there; no indirection, no sync script, no wrappers. See IMPLEMENTATION for the full four-pass journey.

### Portability Preference

Cross-harness portable; no Cursor-only `.mdc` frontmatter or Claude Code-only `hooks.json`. `SKILL.md` + `references/` is the most stable cross-harness primitive available at ship time (this repo's Niko skill system uses the same shape).

### Out of Scope

- Apply capability (VISION Phase 3) — audit-only.
- Remaining 13 taxonomy entries (VISION Phase 2).
- Publishing to any plugin marketplace.
- Harness support beyond Cursor and Claude Code.

## IMPLEMENTATION

### Final Shipped Architecture

```
skills/slobac-audit/
├── SKILL.md                              # audit workflow: scope-parsing, detection loop,
│                                         # report emission
└── references/
    ├── docs/                             # full SLOBAC manifesto (canonical authoring surface)
    │   ├── index.md
    │   ├── principles.md
    │   ├── glossary.md
    │   ├── workflows.md
    │   ├── .pages
    │   └── taxonomy/
    │       ├── README.md                 # taxonomy-entry shape spec
    │       ├── deliverable-fossils.md    # canonical smell definition (Phase-1; includes
    │       ├── naming-lies.md            #   False-positive guards section)
    │       └── <13 other slugs>.md      # canonical smell definitions (Phase-2-deferred;
    │                                    #   stub False-positive guards section)
    └── report-template.md               # per-finding skeleton for slobac-audit.md
```

`properdocs.yml` `docs_dir: skills/slobac-audit/references/docs` — properdocs renders directly from the skill tree, no wrappers, no `docs/` directory at repo root.

```
tests/fixtures/audit/
├── README.md                            # fixture convention documentation
├── deliverable-fossils/
│   ├── test_plugin_registry.py          # planted fossils + negative example
│   └── expected-findings.md
├── naming-lies/
│   ├── test_session_lifecycle.py        # planted lies + negative example
│   └── expected-findings.md
├── both-smells/
│   ├── test_mixed.py                    # fossils + lies + one overlapping both
│   └── expected-findings.md
└── clean/
    ├── test_example.py                  # well-named, body-matching tests
    └── expected-findings.md
```

### Key Design Decisions

#### OQ1 — Customization Primitive Shape (Resolved, High Confidence, Held Through All Reworks)

**Decision:** Option 2 — Ur-Skill with per-smell entries under `references/`, AgentSkills.io shape.

**Options eliminated:**
- Option 1 (monolithic, all smells inline) — explicitly rejected by operator as unscalable to Phase 2.
- Option 3 (one skill per smell) — duplicates the workflow prose N times; workflow bug-fixes require N edits.
- Option 4 (Ur-Skill + Sub-Agents per smell) — Sub-Agent invocation semantics differ across harnesses; adds portability risk for Phase-1 scope that doesn't require it.
- Option 5 (Day-1 Plugin) — two harness-specific plugin builds before a single smell has shipped.

**Key insight:** this repo's Niko skill system already uses the same shape (`SKILL.md` + typed `references/` subdirs). Option 2 is the existing precedent, not a new one.

**Tradeoff accepted:** Sub-Agent per-smell prompt isolation is not built day 1. If Phase-2's 15-smell scope causes prompt-context bloat, the migration path is additive (wrap the existing `references/docs/taxonomy/<slug>.md` files in Sub-Agent definitions).

---

#### OQ2 Pass 1 — Original Docs ↔ Skill DRY (Invalidated)

**Decision (original):** Option D — docs canonical; skill `references/smells/<slug>.md` carries audit-specific augmentation only; SKILL.md workflow instructs the agent to read both files per in-scope smell. Marked "high confidence."

**Why it was invalidated:** The decision conflated *filesystem co-location* (files live in the same repo tree) with *runtime co-location* (paths are reachable from the skill's install root at invocation). An AgentSkills.io skill's runtime root is its own install directory (`~/.claude/skills/slobac-audit/`, a user-level Cursor install, or wherever the operator drops the bundle). `docs/taxonomy/<slug>.md` is not reachable from that root. Option D depended on runtime co-location, which does not survive install.

**New invariant codified:** Invariant #11 — Skill-root self-containment. Every file the skill reads at agent-runtime must be reachable via a path anchored inside the skill's own root.

---

#### OQ2-redux Pass 2 — Generator + Drift-Check CI Gate (Shipped, Then Rejected)

**Decision:** Option E — docs canonical; a Python script (`scripts/sync-taxonomy.py`) generates verbatim copies of each `docs/taxonomy/<slug>.md` into `skills/slobac-audit/references/taxonomy/<slug>.md`; a CI job runs `--check` mode and fails on drift. Skill reads the committed copies. Hand-authored augmentation files (`references/smells/*.md`) carry audit-specific content.

**Options eliminated:**
- H (role-split operational playbook) — drift is structural by design; violates zero-drift (QA#1) and manifesto-independence (QA#2) simultaneously.
- K (vendored copy, manual sync) — drift is silent; no enforcement; scales badly to 15 smells.
- M (vendored copy + hash check) — strictly weaker than E: detects but doesn't resolve drift.
- J (runtime fetch from public URL) — harness portability risk (not all skill runtimes permit arbitrary HTTP); offline-use impossible; URL stability becomes part of the skill's interface.

**Why it was subsequently rejected (operator review post-build):**
1. Committing generated code is architecturally a smell. The 15 `references/taxonomy/*.md` files are derivative committed content; even with the drift-gate, the "remember to regenerate before commit" ritual silently rots.
2. The `references/smells/*.md` augmentation files were 35–60% restated manifesto content (Fix-phase labels, Related-modes cross-refs, ticket-as-provenance rule). An editor updating the manifesto had no structural prompt to open the augmentation file, so the restated content would drift silently.

**Root cause (shared):** OQ2-redux preserved the premise that `docs/taxonomy/*.md` is the authoring source of truth. Under Invariant #11, the only way to satisfy both "docs is canonical" and "skill is self-contained" simultaneously is some flavor of copy-with-sync-discipline. Option E was a competent instance of that pattern. The pattern itself was the problem.

---

#### OQ3 Pass 3 — Canonical-in-Bundle, Site-Rendered-via-Snippet (Shipped, Then Superseded by Third Rework)

**Decision:** Option γ — definitional canonical + discursive wrapper. Skill bundle holds canonical taxonomy at `skills/slobac-audit/references/docs/taxonomy/<slug>.md`; `docs/taxonomy/<slug>.md` becomes a bare `pymdownx.snippets` directive (`--8<-- "skills/slobac-audit/references/docs/taxonomy/<slug>.md"`). Augmentation files deleted; false-positive guards promoted into canonical as a first-class section; invocation phrases inlined into SKILL.md scope-parsing.

**Key unlock:** Operator confirmed "nobody reads `docs/*.md` directly — readers consume the rendered properdocs site." This eliminated the constraint that killed snippet-based options in OQ2 ("build-time only; incompatible with github.com rendering").

**Options eliminated:**
- α (maximal canonical) — functionally identical to γ for Phase-1 scope; lacks the named wrapper affordance for optional reader-framing prose.
- β (minimal canonical) — violates operator signals ("there might not be ANY" wrapping requires Description in every wrapper; "tight description" was not a push for minimalism below the manifesto's current content).

**Why it was subsequently superseded:** the 15 snippet-include wrappers at `docs/taxonomy/<slug>.md` existed solely as an indirection layer to bridge properdocs's `docs_dir: docs` expectation with the canonical content inside the skill. Pure structural overhead.

---

#### Third Rework — Full Manifesto in Bundle (Final State)

**Decision:** move the entire `docs/` tree into `skills/slobac-audit/references/docs/` and point `properdocs.yml` `docs_dir` at it. Delete all 15 snippet-include wrappers and the `docs/` directory.

**No creative phase required.** The approach was unambiguous: `git mv` + delete wrappers + update config.

**What this eliminates:**
- All 15 snippet-include wrappers (pure indirection, zero content).
- The `pymdownx.snippets` dependency for content composition.
- The "link-path footgun" from the second rework (canonical files' relative links now resolve at their actual filesystem location because properdocs renders from that location).
- The published-URL workaround in SKILL.md's governor-rule cite (`principles.md` is now inside the skill root).

**The four-pass progression summarized:**
1. OQ2: external `docs/` path read at runtime → invalidated by Invariant #11.
2. OQ2-redux: generator + committed copies + CI drift-gate → rejected; committed generated content is a smell, augmentation files drift.
3. OQ3: snippet-include wrappers + canonical-in-bundle → superseded; wrappers are pure indirection.
4. Third rework: direct `docs_dir` pointer, no sync mechanism, no wrappers → final.

### Key Files Touched

| File | Change |
|---|---|
| `skills/slobac-audit/SKILL.md` | Authored (new); 4 rounds of revision. Final: scope-parsing with inline NL vocabulary, single-file canonical read, intra-skill principle cite, read-only Constraints. |
| `skills/slobac-audit/references/docs/taxonomy/deliverable-fossils.md` | Migrated from `docs/taxonomy/`; Phase-1 False-positive guards section added. |
| `skills/slobac-audit/references/docs/taxonomy/naming-lies.md` | Migrated from `docs/taxonomy/`; Phase-1 False-positive guards section added. |
| `skills/slobac-audit/references/docs/taxonomy/<13 other slugs>.md` | Migrated from `docs/taxonomy/`; stub False-positive guards section added. |
| `skills/slobac-audit/references/docs/principles.md` | Migrated from `docs/principles.md`. |
| `skills/slobac-audit/references/docs/glossary.md` | Migrated from `docs/glossary.md`. |
| `skills/slobac-audit/references/docs/workflows.md` | Migrated from `docs/workflows.md`. |
| `skills/slobac-audit/references/docs/index.md` | Migrated from `docs/index.md`. |
| `skills/slobac-audit/references/docs/.pages` | Migrated from `docs/.pages`. |
| `skills/slobac-audit/references/docs/taxonomy/README.md` | Migrated; shape spec updated to include `## False-positive guards` section. |
| `skills/slobac-audit/references/report-template.md` | Authored (new); citation instruction references `references/docs/taxonomy/<slug>.md`. |
| `skills/slobac-audit/README.md` | Authored (new); install/invocation docs; fixture smoke-test instructions. |
| `tests/fixtures/audit/` | All 4 scenario dirs with Python files + expected-findings.md (new). |
| `properdocs.yml` | `docs_dir` updated to `skills/slobac-audit/references/docs`; `edit_uri` updated to match. |
| `.github/workflows/docs.yaml` | Final state: drift-check step added (first rework) then removed (second rework); net: CI unchanged from pre-task state. |
| `planning/VISION.md` | 14 `../docs/` relative refs → published URLs. |
| `README.md` | Phase-1 install/use section added; entry-point links updated. |
| `memory-bank/techContext.md` | Updated through all reworks; final: "Full-manifesto-in-bundle" pattern. |
| `memory-bank/systemPatterns.md` | Updated through all reworks; final: canonical-in-bundle authoring model, structural manifesto-independence, Invariant #11. |
| `memory-bank/productContext.md` | Stale `docs/` reference fixed (QA catch). |

### Invariants Codified or Revised

- **New — Invariant #11 (Skill-root self-containment):** Every file the skill reads at agent-runtime must be reachable via a path anchored inside the skill's own root directory. No `../` escapes from the root; no bare `docs/` path references; no harness-cwd assumptions. Structurally satisfied in the final architecture by construction: the full manifesto lives inside the skill root.
- **Revised — Invariant #3 (Manifesto-independence):** Under the canonical-in-bundle architecture, manifesto-independence is structurally absolute. There is one document per smell; forking is impossible. The audit skill doesn't reference the manifesto — it is the manifesto's home. The reader-facing site is a properdocs-rendered derivative.

### Implementation Phases (L3 Workflow)

| Phase | Result | Notes |
|---|---|---|
| Plan (original) | Pass | 14-step TDD plan; OQ1/OQ2 identified |
| Creative OQ1 | High confidence | Ur-Skill + references shape |
| Creative OQ2 | High confidence → **Invalidated** | Option D; missed Invariant #11 |
| Preflight (original) | Pass w/ 2 amendments | Report default path; always-present augmentation file |
| Build (original) | Pass | 12 of 14 steps; 1 unneeded, 1 conditional not triggered |
| QA (original) | Pass | 1 trivial fix (Skill version scope-creep) |
| Reflect (original) | Complete | Insight #2 retroactively invalidated |
| Plan (rework 1) | Pass | Invariant #11 codified; OQ2-redux opened |
| Creative OQ2-redux | High confidence → **Rejected post-build** | Option E; operator rejected committed generated content |
| Preflight (rework 1) | Pass w/ amendments | R4–R6 expanded; R5a added |
| Build (rework 1) | Pass | R1–R8, R10, R11; R9 operator-gated |
| QA (rework 1) | Superseded by rework 2 | — |
| Creative OQ3 | High confidence → **Superseded by third rework** | Option γ; snippet-include wrappers later eliminated |
| Plan (rework 2) | Pass | S1–S14 |
| Preflight (rework 2) | Pass w/ 2 MAJOR amendments | S1+S2 combined commit; S4a added |
| Build (rework 2) | Pass | S1–S14; S7 was no-op |
| QA (rework 2) | Pass | 1 trivial fix (stale "augmentation file" reference) |
| Reflect (rework 2) | Pass | Second retraction of insight #2; process insights |
| Plan (rework 3) | Pass | T1–T10; no creative phase needed |
| Preflight (rework 3) | Pass w/ 1 MAJOR amendment | T5d: VISION.md 14 broken `../docs/` refs |
| Build (rework 3) | Pass | T1–T10 |
| QA (rework 3) | Pass | 2 trivial fixes (stale `docs/` in systemPatterns.md and productContext.md) |
| Reflect (rework 3) | Complete | Third-rework evolution note |

## TESTING

### TDD Discipline

Fixtures and expected-findings were authored **before** SKILL.md workflow prose and per-smell content. Writing `expected-findings.md` first surfaced the specific false-positive cases that needed explicit guards, reshaping the detection prose in the final skill.

### Behaviors Verified

| Behavior | Mechanism |
|---|---|
| B1 — Fossils detected | `deliverable-fossils/` fixture + expected-findings |
| B2 — Naming-lies detected | `naming-lies/` fixture + expected-findings |
| B3 — Scoping honored | `both-smells/` fixture; single-smell scope emits only that smell's findings |
| B4 — Clean suite → no findings | `clean/` fixture + expected-findings |
| B5 — Negative-example guards | Each smell fixture includes a negative-example test; audit does not flag it |
| B6 — Report structure invariant | Five-field per-finding shape (location, slug, rationale, remediation, FP-guard) |
| B7 — Both harnesses | Operator-gated (manual harness validation); per plan, not a ship gate |
| B9 — Invariant #11 spot-check | `rg '(\.\./\.\./|^\s*docs/)' skills/slobac-audit/` → zero results |
| B10 — Docs build under new `docs_dir` | `properdocs build --strict` passes clean |
| B13 — Relative links resolve natively | Canonical files' `../principles.md#anchor` links resolve at filesystem location since properdocs renders from that location |

### Verification Gates (Final Build)

- `properdocs build --strict` passes clean.
- Invariant #11 spot-check: zero cross-root escapes in agent-runtime files.
- All fixture Python files parse as valid Python 3.
- All cross-links in skill tree resolved (no broken relative paths).

### Test Infrastructure Notes

Fixture scenarios are **input** to the audit, not automated tests of SLOBAC itself. They are manual-operator-run: invoke the skill in the target harness against a fixture path, compare output to `expected-findings.md`. A scripted eval harness (golden-file comparison or structured-pattern validation) is Phase 2+ scaffolding, explicitly deferred.

## LESSONS LEARNED

### Technical

**Prompt-artifact TDD is real and worth doing.** Writing `expected-findings.md` before the SKILL.md detection prose is forcing function. It surfaces the specific false-positive cases (cross-language synonymy, refactor-as-behavior, domain-vocabulary collisions) that need codifying in canonical guards. Without fixtures, guards would be aspirational; with fixtures, guards are behavior-grounded.

**The five-field per-finding invariant is the quality lever.** Location + smell slug + rationale + remediation + false-positive guard. The single most important of the five is the false-positive guard — it forces the audit to show its work and gives the reader a disagreement handle without re-running the audit.

**Structural enforcement beats procedural enforcement whenever it's available.** The four-pass architecture journey demonstrated this at scale: OQ2 (external read) → Invariant #11 → OQ2-redux (generator + CI gate, procedural) → operator rejection → OQ3 (snippet-include, structural) → third rework (direct `docs_dir`, maximally structural). Each pass eliminated a mechanism the prior one introduced. The final architecture has fewer moving parts than any intermediate.

**`docs_dir` pointing deep into a subdirectory works fine.** `properdocs.yml` with `docs_dir: skills/slobac-audit/references/docs` is unusual but properdocs/mkdocs has no restriction on path depth. Rendered site, `edit_uri`, nav ordering — all work identically.

**`git mv` preserves history across architectural inversions.** The 15-file taxonomy migration kept full git blame for every canonical entry. For an authoring-surface migration, git history is part of the deliverable.

**Snippet-include inverts the authoring surface without losing the reader surface.** `pymdownx.snippets` + `check_paths: true` + `strict: true` gives structural integrity on the link between canonical and rendering wrapper. It's a zero-maintenance sync mechanism. This pattern is worth knowing for future skills that need to own canonical content consumed by a rendered site. (Note: in Phase 1's final third rework, even this mechanism was eliminated as unnecessary indirection — direct `docs_dir` was simpler — but the pattern remains valid for cases where the canonical can't be the `docs_dir` directly.)

**The three-way fix-arm decision rules for naming-lies are genuinely subjective at the edges.** rename / strengthen / investigate distinction was iterated on; the final shape codifies heuristics ("title is specific and testable → lean strengthen; title is a shape-claim → lean rename; both suspect → investigate") but doesn't fully eliminate judgment. Acceptable: the manifesto itself doesn't eliminate the judgment either.

### Process

**"Advisory not applied" is an ambiguous state.** A preflight advisory raised but not applied is a footgun during build: the line between "nice idea, low cost, why not include it" and "operator explicitly deferred, build must not include it" blurs under build-phase momentum. The original QA caught the `Skill version` field implementing a "not applied" advisory as scope-creep. Two possible fixes for future tasks:
1. Preflight either applies an advisory or explicitly forbids it — no middle state.
2. Unapplied advisories are recorded in `tasks.md` under a "Forbidden during build absent operator approval" section, which build must explicitly check.

**When multiple creative-phase passes fail at the same architectural boundary, the constraint itself may be wrong.** OQ2 and OQ2-redux both preserved the premise that `docs/taxonomy/*.md` is the authoring source of truth. Each pass met its stated constraints; neither asked whether the premise itself was load-bearing. The operator's clarification ("nobody reads raw docs") was the unlock. The lesson: before the third attempt, escalate to the operator — "we have failed this boundary twice; can we re-examine the constraint?"

**The four-pass calibration debt is a Phase-2 checklist item.** Each creative-phase decision in this task was marked "high confidence" and subsequently failed a later-surfaced constraint. Phase-2 creative-phase invocations on SLOBAC should explicitly ask: "What will the operator's first reaction to the shipped artefact be, and can we surface that objection now?" as a hedge.

**The simplest architecture often survives multiple creative passes.** The process insight is not "we should have skipped to the simplest answer." Each intermediate was necessary to understand why it was unnecessary. But when the operator signals dissatisfaction with complexity, the corrective direction is almost always toward fewer moving parts, not different moving parts.

**Uncommitted build artifacts from a superseded rework are a feature, not a hazard.** Because the first rework's build changes were never committed (QA was superseded before it ran), the second rework started from a clean HEAD. No revert commits, no tangled git history. The L3 workflow's phase-gating (commit happens at QA or later, not at build start) is what created this outcome.

**Phase-mapping commits are load-bearing when multiple phase boundaries are crossed in one session.** This task crossed build → QA → reflect (and rework phases) in single sessions; the explicit commit between phases is what keeps the memory bank auditable rather than a smear of uncommitted state.

## PROCESS IMPROVEMENTS

**For the "advisory not applied" pattern:** Either collapse it (preflight applies or forbids; no middle ground) or make unapplied advisories explicit build-time inhibitors in `tasks.md`. The current three-state system (applied / not applied / forbidden) collapses silently to two states during build if the distinction is only documented in the preflight narrative.

**For recurring creative-phase failures:** Add a checkpoint before the N-th creative pass: "We have failed this architectural boundary N-1 times. Before proceeding, what is the unstated constraint we are most likely missing?" This is cheap at pass 2; it is load-bearing at pass 3.

**For fixture-expected-findings convention:** Codify the fixture-first TDD discipline from this task for Phase 2's 13 additional smells. Specifically: (a) `expected-findings.md` is always authored before `SKILL.md` workflow prose and canonical guards; (b) the expected-findings format should mirror the report template closely enough that manual comparison is mechanical.

## TECHNICAL IMPROVEMENTS

**Phase 2 smell scope:** The 13 non-Phase-1 canonical taxonomy entries were migrated with stub `## False-positive guards` sections ("No audit-specific guards yet; Phase-2 per-smell work will author these."). Phase-2 per-smell work should follow the same fixture-first discipline: fixture + expected-findings before guard authoring.

**Sub-Agents migration path:** Reserved from OQ1 analysis. If Phase-2's 15-smell ur-Skill prompt overflows context budgets in the target harness, the migration is: write Sub-Agent wrappers around the existing `references/docs/taxonomy/<slug>.md` files. The canonical content files are already there; no reshaping required.

**`references/scope-vocabulary.yaml` as Phase-2 candidate:** SKILL.md currently enumerates per-smell invocation phrases inline in Step 2 prose. At 15-smell scale, a `references/scope-vocabulary.yaml` (or equivalent) would make Phase-2 additions a data edit rather than a SKILL.md prose edit. Surfaced as a Phase-2 entry-point candidate.

**`edit_uri` contributor UX:** After the `docs_dir` migration, the properdocs site's "Edit this page" link for taxonomy entries points directly to the canonical file (`skills/slobac-audit/references/docs/taxonomy/<slug>.md`) rather than a snippet-include wrapper. This is strictly better contributor UX: clicking "Edit" lands at the actual content. Worth documenting in the contributor guide.

**Pre-commit hook for Invariant #11:** The current enforcement is procedural (code review) and one-time structural (spot-check). If future contributors begin introducing `../` cross-root references in the skill tree, a simple CI lint (`rg '(\.\./\.\./|^\s*docs/)' skills/slobac-audit/SKILL.md skills/slobac-audit/references/`) is an additive Phase-2 improvement.

**Report versioning:** Stamping each emitted `slobac-audit.md` with the manifesto git ref / audit-skill version that produced it would support VISION §1.2's portability goal (a reviewer three months later can trace which smell definitions a finding was based on). Explicitly deferred from Phase-1 per operator; flagged for reconsideration before Phase-2 ships.

## NEXT STEPS

1. **Phase 2 — Extend audit scope to remaining 13 smells.** Each smell needs: (a) canonical `## False-positive guards` section authored; (b) invocation vocabulary added to SKILL.md Step 2; (c) fixture scenario + expected-findings. Approach: per-smell creative phase if the fix shape is genuinely ambiguous; direct build if the manifesto's Signals and Prescribed Fix are sufficient.

2. **Manual harness validation (deferred from plan).** Operator runs the skill against each fixture in each harness (Cursor and Claude Code) and confirms findings match `expected-findings.md`. Not a ship gate for Phase 1; a quality gate for Phase 2 readiness. Target: B7 (cross-harness output equivalence) and B1–B5 (smell-specific detection).

3. **Scripted eval harness (Phase 2 scaffolding).** Replace the manual fixture-comparison gate with a golden-file or structured-pattern validation runner. The `expected-findings.md` format was designed to be machine-parseable; Phase 2 is when the scale justifies automation.

4. **Phase 3 — Apply capability.** VISION Phase 3: agent applies the audit report's remediations to the target test suite. The apply layer's shape is entirely deferred; Phase 1's read-only architecture has no bearing on it.
