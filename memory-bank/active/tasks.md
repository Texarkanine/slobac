# Task: Onboard Remaining 9 Smells — REWORK

* Task ID: onboard-remaining-smells
* Complexity: Level 2
* Type: Rework / refactor (drift-surface reduction; no new behavior)

Reduce the SKILL.md surface that mirrors taxonomy content. The original implementation reached 15-smell parity by inlining a 15-row supported-smells table, a 15-bullet natural-phrase map, and three Cursor / Claude Code dispatch boilerplate blocks into `skills/slobac-audit/SKILL.md`. All three are duplicate or drift-prone surfaces. This rework moves natural-phrase mappings into per-entry taxonomy sections (one canonical home per slug for everything about that slug), delegates supported-slug enumeration to "the taxonomy entry exists," and elides the harness-specific dispatch examples. The just-shipped 9 fixtures and the just-completed onboarding work are preserved untouched.

## Test Plan (TDD)

### Behaviors to Verify

The "tests" for a docs-and-instructions refactor are mechanical-gate assertions (`grep`/`rg` on the changed surfaces) and the existing CI gate (`properdocs build --strict`).

**R1 — taxonomy delegation + slug-only contract:**

- **B1 — SKILL has no inlined supported-smells table:** `rg "Supported smells \(" skills/slobac-audit/SKILL.md` returns 0 matches.
- **B2 — SKILL instructs structural enumeration:** SKILL.md Step 2 prose explicitly states the supported set is enumerated by file existence under `references/docs/taxonomy/` (`README.md` excluded). Verified by reading the section.
- **B2b — SKILL enforces slug-only invocation:** SKILL.md Step 2 prose explicitly states operators invoke by explicit slug; non-slug or fuzzy-phrase requests are **refused** (not silently resolved). The refusal lists the supported slug set and prompts the operator to re-invoke with explicit slugs. Verified by reading the section.
- **B2c — SKILL preserves bulk-select wildcard:** SKILL.md Step 2 prose recognizes a small whitelist of unambiguous wildcard tokens (`all`, `everything`, unscoped) as a request for the full supported-slug set. This is not phrase-to-slug fuzzy matching — it is an explicit "all" gesture, unambiguous by definition. (If operator subsequently rejects this carve-out, drop it; surface as decision point during build.)
- **B3 — SKILL has no inlined operator-phrase map:** `rg "^- \`[a-z][a-z-]+\` — \"" skills/slobac-audit/SKILL.md` returns 0 matches.
- **B4 — SKILL does NOT reference the Aliases section as a runtime input:** `rg "Aliases" skills/slobac-audit/SKILL.md` returns 0 matches. Aliases live in the taxonomy entries strictly for human-search discoverability on the published docs site; the orchestrator never reads them.
- **B5 — Each taxonomy entry carries an `## Aliases` section:** `rg -l "^## Aliases$" skills/slobac-audit/references/docs/taxonomy/*.md` returns exactly 15 paths (one per entry; the taxonomy `README.md` does not get the section).
- **B6 — Each migrated alias set matches its current SKILL.md content:** for each of the 15 slugs, the bullets under `## Aliases` in `taxonomy/<slug>.md` are the same bullets currently at SKILL.md lines 38-52 (verbatim, modulo formatting; no editorial expansion). The slug-name prefix is dropped from each bullet (since the section already lives in the slug's file).
- **B7 — Taxonomy README shape SoT documents the new section as a discoverability aid:** `taxonomy/README.md` lists `## Aliases` as a required section in the canonical entry shape, and the section's purpose-and-audience explanation states it is for human search discoverability on the published docs site (operators landing from a fuzzy query find the right entry, then invoke by slug). The shape SoT explicitly notes the orchestrator does not consume the section at runtime.

**R2 — harness-neutral dispatch:**

- **B8 — No harness-specific tool names in SKILL.md:** `rg "\`Task\` tool|dispatch_agent" skills/slobac-audit/SKILL.md` returns 0 matches.
- **B9 — Each of the three dispatch sites uses a uniform harness-neutral instruction:** Steps 3, 5, 7 of SKILL.md each contain one sentence telling the agent to launch a readonly subagent with the named skill plus the required inputs. No bullet block enumerating Cursor / Claude Code / Other harnesses.
- **B10 — No contributor rationale in SKILL.md:** No meta-note explaining why harness names were dropped (rationale lives in commit messages and `slobac-audit/README.md` if anywhere).

**Mirror cleanup:**

- **B11 — `slobac-audit/README.md` lead paragraph drops hardcoded count:** the L3 paragraph no longer says "Supports all 15 manifesto smells" or any count-pinned variant. Phrasing equivalent to "supports every smell defined in the manifesto." The human-facing supported-smells table beneath is **preserved** — that's contributor documentation, legitimate as a mirror.
- **B11b — `slobac-audit/README.md` "Scope and non-goals" reflects structural enumeration:** the bullet at README line 176 currently asserts a manually-curated supported-slug table backs slug refusal. After the rework it asserts: full taxonomy parity is achieved by enumerating taxonomy entry filenames (no manual curation), and a slug whose entry does not exist is refused. The substance — "audit never silently skips a requested smell" — is preserved.
- **B12 — `memory-bank/techContext.md` lead summary drops hardcoded count:** the lead paragraph references the three detection scopes by name without pinning a smell count or enumerating slugs.

**Regression gates:**

- **B13 — `properdocs build --strict` passes** after every phase that touches `references/docs/`.
- **B14 — Operator-invocation flow under new slug-only contract is sane:** mental walkthrough — operator invokes `/slobac-audit tautology-theatre vacuous-assertion`, agent resolves both slugs against `taxonomy/<slug>.md` existence, partitions by detection scope, dispatches batch and (where present) cross-suite assessors. Operator invokes `/slobac-audit tests that mock the SUT`, agent refuses with the supported-slug list and asks for explicit slugs. Operator invokes `/slobac-audit all`, agent expands to the full supported-slug set.
- **B15 — Existing 9 fixtures untouched:** `git diff` against the rework-init commit (HEAD) shows zero changes under `tests/fixtures/audit/`. Their presence and content are preserved.

### Edge Cases

- **`deliverable-fossils` is the only slug with multi-scope detection** (per-test + cross-suite). Its taxonomy entry's existing structure works as-is — adding `## Natural phrases` is uniform with the other 14. The SKILL.md Step 2 partition logic keeps reading `Detection Scope` per-entry; no special-case logic.
- **Existing taxonomy entries already have varying section counts** (Signals / False-positive guards / Prescribed Fix / Example / Related modes / Polyglot notes). Adding `## Aliases` must place consistently across all 15 — propose **immediately after Summary, before Description** so alias terms live near the canonical name. This keeps the section's purpose ("alternate terms a search engine indexes for this slug") tight to the slug's identity.

- **Slug-only contract removes the orchestrator's phrase-resolution responsibility entirely.** Old SKILL.md Step 2 attempted fuzzy phrase-to-slug resolution; new contract refuses. Aliases stay in the taxonomy purely for **human-side discoverability** — published docs site search, manifesto cross-references, drive-by reading. The orchestrator never reads them. This is the operator's explicit decision: minimal ambiguity, slugs only, invocation contract is unforgiving in the right way.

- **The "all" wildcard:** previously SKILL.md treated "audit everything", "all smells", and unscoped as resolving to the full supported set. This is technically a phrase-to-set rule, not a phrase-to-slug rule, and it is unambiguous by definition (no fuzzy match). Plan preserves it as an explicit wildcard whitelist (`all`, `everything`, unscoped) — surface as a build-time decision point in case operator wants to drop it for strict slug-only.
- **The SKILL.md frontmatter `description:` field was already softened by the operator pre-plan** (`commit 2d5c4d4`: changed from "Supports all 15 manifesto smells across 3 detection scopes (per-test, per-file, cross-suite)." to "Audit a test suite for common test smells based on the SLOBAC manifesto."). This is R1-aligned; the field needs no further edits in this plan.

### Test Infrastructure

- **Mechanical gates:** `rg`/`grep` for presence/absence assertions, `uv run properdocs build --strict` for cross-link integrity.
- **No new test framework.** No new test files. Fixtures from the original task are inputs to the audit, not tests of SLOBAC; rework does not modify them.
- **Manual verification step (B14)** is a mental walkthrough by the implementer — no automated check, mirrors the prior task's manual-validation convention for `expected-findings.md` against canonical entries.

## Implementation Plan

The plan is **taxonomy-first, SKILL-second, mirror-third, verify-fourth**. Step ordering is strict: the per-entry sections must exist before SKILL.md is rewritten to read from them; SKILL.md surgery runs as one batch to avoid leaving the file in a half-migrated state across commits.

### Phase A — Per-entry rollout (R1, taxonomy side)

1. **Update `taxonomy/README.md` shape SoT.**
    - Files: `skills/slobac-audit/references/docs/taxonomy/README.md`.
    - Changes: Add `## Aliases` to the documented canonical entry shape, positioned immediately after `## Summary` and before `## Description`. State the section's **purpose and audience** clearly: alternate terms by which the smell may be named or searched, intended for **human-side discoverability** when readers land on the docs site from a fuzzy query (e.g. via search engine or manifesto cross-link). Explicitly note that the orchestrator does **not** consume this section at runtime — the audit orchestrator requires explicit slug invocation, not phrase resolution. Required form: bullet list of double-quoted alias phrases.

2. **Migrate 15 operator-phrase lists into per-entry `## Aliases` sections.**
    - Files: each of `skills/slobac-audit/references/docs/taxonomy/<slug>.md` for `<slug>` ∈ {`deliverable-fossils`, `naming-lies`, `vacuous-assertion`, `tautology-theatre`, `pseudo-tested`, `over-specified-mock`, `implementation-coupled`, `presentation-coupled`, `conditional-logic`, `mystery-guest`, `rotten-green`, `shared-state`, `monolithic-test-file`, `semantic-redundancy`, `wrong-level`}.
    - Changes: insert a `## Aliases` section between Summary and Description in each entry. The bullet content is the existing curated phrase list from `slobac-audit/SKILL.md` lines 38-52, copied verbatim per slug — no editorial expansion in this rework. One bullet per quoted phrase, exactly as currently rendered. The slug-name prefix is dropped from each bullet (since the section already lives in the slug's file). Source for each entry is the corresponding SKILL.md bullet line.

3. **Run `properdocs build --strict`.**
    - Files: none modified.
    - Changes: regression gate after the per-entry rollout. Confirms anchor consistency, no broken cross-links, and that the new section's headers don't collide with existing ones.

### Phase B — SKILL.md surgery (R1 SKILL side + R2)

4. **Replace SKILL.md Step 2 supported-smells table and operator-phrase map with slug-only structural-enumeration prose.**
    - Files: `skills/slobac-audit/SKILL.md`.
    - Changes:
      - Delete the `**Supported smells (15):**` heading + the table (lines 16-34).
      - Delete the operator-phrase bullet list (lines 36-52).
      - Convert the trailing "audit everything, all smells, unscoped" line (line 53) into a structured wildcard rule: explicitly whitelist `all`, `everything`, and an unscoped invocation as the bulk-select gesture for the full supported-slug set. This is the only non-slug input the orchestrator accepts.
      - Delete the refusal paragraph that names example slugs (line 55) and replace with a slug-only contract paragraph: (a) supported-slug set is the set of entry filenames under `references/docs/taxonomy/` excluding `README.md`; (b) operators invoke by **explicit slug**; (c) free-text or fuzzy-phrase requests are **refused** with the supported-slug list, prompting the operator to re-invoke with explicit slugs (the orchestrator never silently resolves a phrase to a slug); (d) operator-named slugs whose taxonomy entry does not exist are also refused with the supported-slug list.
      - Preserve the existing detection-scope partition instruction (current line 39, "read its `Detection Scope` from `references/docs/taxonomy/<slug>.md`") — that part already works structurally.
      - **Do not** reference the `## Aliases` section anywhere in SKILL.md. It is not a runtime input.

5. **Replace harness-specific dispatch blocks at SKILL.md Steps 3, 5, 7.**
    - Files: `skills/slobac-audit/SKILL.md`.
    - Changes: At each of the three subagent-dispatch sites, delete the `**Harness-specific dispatch:**` bullet block (Cursor / Claude Code / Other harnesses lines). Replace with one sentence at the end of each step: "Launch a readonly subagent with the `slobac-X` skill, providing the inputs above." (Vary `X` per site: scout / batch / cross-suite.) No contributor rationale, no meta-note, no fallback prose.

### Phase C — Mirror cleanup (drop hardcoded counts in lead paragraphs)

6. **Soften `slobac-audit/README.md` lead paragraph and rewrite "Scope and non-goals" parity assertion.**
    - Files: `skills/slobac-audit/README.md`.
    - Changes:
      - **Lead paragraph** (line 3): "Supports all 15 manifesto smells across 3 detection scopes" → "Supports every smell defined in the manifesto, across three detection scopes (per-test, per-file, cross-suite)." Preserve the supported-smells table at lines 9-26 (contributor documentation; human-readable mirror is acceptable here even though it carries the same drift risk; if a future reader wants to remove it, that is a separate decision).
      - **Scope and non-goals** (line 176): the current bullet attributes refusal to a manually-curated supported-slug table. After the rework, refusal is structural — enumeration is by taxonomy-entry-file existence. Rewrite the bullet to reflect this: full taxonomy parity is achieved by structural enumeration, a future taxonomy entry is automatically supported once its file exists, and a request for any slug whose taxonomy entry does not exist is refused with a clear message. Preserve the closing assertion "the audit never silently skips a requested smell."

7. **Soften `memory-bank/techContext.md` lead summary.**
    - Files: `memory-bank/techContext.md`.
    - Changes: Replace the lead summary's hardcoded count + per-test enumeration with: "Supports every smell defined in the manifesto, across three detection scopes (per-test, per-file, cross-suite)." Drop the parenthetical 15-slug enumeration. The detail of "which slugs are in which scope" is now reachable via the manifesto itself; this lead paragraph is orientation, not an index.

### Phase D — Verification

8. **`uv run properdocs build --strict`.**
    - Files: none modified.
    - Changes: final cross-link integrity gate. Same advisory as the original task — properdocs builds from `references/docs/`, so it directly exercises Phase A changes (taxonomy entries + README) but does not exercise SKILL.md or the two README/techContext lead-paragraph edits. Those are validated by step 9 grep audit.

9. **Grep audit (mechanical-gate assertions for B1–B12).**
    - Files: none modified; this is verification only.
    - Changes: run the grep / rg patterns enumerated in the Test Plan's Behaviors-to-Verify section. Fix any failures inline if trivial; if a failure indicates a missed touchpoint (analogous to the original task's frontmatter-description straggler), fix it and re-run the audit.

10. **Manual operator-invocation walkthrough.**
    - Files: none modified.
    - Changes: pick three operator phrases (e.g. "audit my tests for tautology", "find naming lies", "what's the most over-specified mock test in here") and trace mentally through the new SKILL.md Step 2 to confirm the phrase still resolves to the correct slug via per-entry `## Natural phrases` lookup. This stands in for an integration test of the structural-enumeration design.

## Technology Validation

No new technology — validation not required. All edits are markdown.

## Dependencies

- The 15 taxonomy entries at `skills/slobac-audit/references/docs/taxonomy/<slug>.md` (already exist; gain a uniform new section).
- The taxonomy shape SoT at `taxonomy/README.md` (gains one required section in the canonical-shape documentation).
- `properdocs` toolchain pinned in `pyproject.toml` / `uv.lock` (unchanged).

## Challenges & Mitigations

- **Asymmetry / typo risk across 15 per-entry edits.** The phrase lists must be copied verbatim from the current SKILL.md state to preserve operator-recall fidelity. Mitigation: do the rollout in one focused step (step 2), without editorialization. Verify with B6 (per-slug content match against the current SKILL.md).
- **`taxonomy/README.md` shape SoT and the 15 entries can drift if rolled out in different orders.** Mitigation: README.md SoT is updated *first* (step 1), entries follow uniformly (step 2). Both are committed before SKILL.md is touched.
- **SKILL.md half-migrated state risk if Phase B is split across commits.** Mitigation: steps 4 and 5 are batched into one commit ("rework: delegate manifesto enumeration + neutralize dispatch in SKILL.md") so SKILL.md is never half-rewritten on disk.
- **Mirror tables in `slobac-audit/README.md` are intentionally preserved.** A future reader may ask "why didn't you delete the table?" Mitigation: the project brief's R1 explicitly scopes README to lead-paragraph phrasing only; preserve the table as contributor documentation; note the deliberate decision in the rework reflection.
- **The frontmatter description was already softened by operator manual edit.** Mitigation: noted in the Edge Cases section; no plan step needed for that field; verify with grep that no count remains in SKILL.md frontmatter (B12-adjacent check).

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight (PASS with amendment + pre-build contract shift; B11b added; B2b/B2c/B4 inverted post-amend)
- [x] Build (Phases A→D shipped across three commits: taxonomy aliases rollout, SKILL.md surgery, mirror cleanup)
- [x] QA (PASS — one trivial DRY fix applied inline at SKILL.md Step 2 refusal payload prose; properdocs rebuilt green)
- [x] Reflect (rework section appended to existing reflection-onboard-remaining-smells.md; persistent files reconciled — productContext.md surgical fix to subset-selection UX phrasing; systemPatterns.md not invalidated; techContext.md updated during build)
