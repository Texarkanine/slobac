# Expected findings — `naming-lies` scenario

**Target suite root:** `tests/fixtures/audit/naming-lies/`
**In-scope smells:** `naming-lies`
**Expected finding count:** 3

Shape mirrors the audit report template. The three findings exercise each arm of the prescribed three-way fix: **rename**, **strengthen**, **investigate**. The audit is correct when every finding names the specific arm and cites rationale that compares the title's claim against the body's verified behavior.

## Findings

### 1. `test_token_counts_default_to_zero` — path: INVESTIGATE

- **Location:** `test_session_lifecycle.py` → module level
- **Smell:** `naming-lies`
- **Rationale:** Title claims "default to zero" — a schema-level invariant about newly-inserted rows with no `token_count` provided. The body inserts a row with `token_count = 5` and asserts `> 0`. The body does not verify the default; neither does it verify anything especially strong. The audit cannot tell from the test alone whether the operator meant to guard the schema default or the post-insert value.
- **Prescribed remediation:** **Investigate.** Apply [describe-before-edit](../../../../docs/principles.md#behavior-articulation-before-change): ask what the test is supposed to prove. Then pick rename or strengthen per the resolved intent. Audit report must surface the ambiguity rather than silently picking a path.
- **Why this isn't a false positive:** Title nouns (`default`, `zero`) do not appear as surface in the body's assertion (`> 0`). Semantically, `> 0` contradicts `default to zero`, not strengthens or weakens it.

### 2. `test_should_use_cyan_blue_styling_for_descriptions` — path: RENAME

- **Location:** `test_session_lifecycle.py` → module level
- **Smell:** `naming-lies`
- **Rationale:** Title promises ANSI/color-styling verification; body does no color check, no ANSI regex, no theme mock. Body instead verifies that the `workspace_slug` field is present and non-empty — a clean claim, just not the claim the title made.
- **Prescribed remediation:** **Rename.** Body is the real contract; title was aspirational. New name encodes the behavior, e.g. `test_session_row_preserves_non_empty_workspace_slug`. Preservation gate: rename-only; call graph unchanged.
- **Why this isn't a false positive:** Title tokens `cyan`, `blue`, `styling`, `descriptions` have zero surface in the body. The body is self-consistent and strong on its own terms.

### 3. `test_workspace_slug_is_last_path_segment_of_repo_path` — path: STRENGTHEN

- **Location:** `test_session_lifecycle.py` → module level
- **Smell:** `naming-lies`
- **Rationale:** Title captures a specific derivation rule: the slug is the last path segment of the repo path. Body inserts `'some-project'` (which happens to have no path separator) and asserts only `len > 0`. The assertion does not verify the derivation rule — a row with slug `'/absolute/path/no-last-segment-match'` would pass the assertion without satisfying the title.
- **Prescribed remediation:** **Strengthen.** The title is the real intent. Hand off to [`vacuous-assertion`](../../../../docs/taxonomy/vacuous-assertion.md): replace the `len > 0` assertion with an equality check that verifies the slug equals the last path segment of a representative repo path (e.g. insert with slug derived from `/home/x/proj/some-project` and assert `slug == 'some-project'`). Preservation gate: mutation kill-set delta ≥ 0 after strengthening.
- **Why this isn't a false positive:** Title nouns (`last`, `path`, `segment`, `repo`) have no surface in the assertion `len(row[0]) > 0`. Title makes a derivation claim the body does not verify.

## Tests that must NOT be flagged

### `test_closing_a_session_deletes_its_row`

- **Location:** `test_session_lifecycle.py` → module level
- **Why not a lie:** Title uses "deletes"; body executes `DELETE FROM sessions` and asserts the row is gone. Surface tokens differ (English verb vs SQL keyword) but the semantic match is exact. The audit must resolve synonymy, not just tokenize.
- **False-positive guard:** See `skills/slobac-audit/references/smells/naming-lies.md` — naive title/body tokenization will miss cross-language synonyms (English-verb ↔ SQL-keyword, English-adjective ↔ CSS-property, etc.). Semantic equivalence must be considered before flagging.

## Notes

- Scenario contains 4 tests total: 3 should be flagged as `naming-lies` with the specific fix arm named, 1 must not be flagged. The per-finding fix arm (rename / strengthen / investigate) is load-bearing — a finding that gets the smell right but names the wrong arm is a build-phase bug.
- Findings must emit the fix arm in a way a downstream reader (human or another agent) can mechanically extract. The report template's "Prescribed remediation" field is where the arm surfaces.
