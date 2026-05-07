# Test audit for code smells
_Exported on 5/7/2026 at 08:55:07 CDT from Cursor (3.3.12)_

---

**User**

/slobac-audit @tests all smells - 1M context window

---

**Cursor**

Now I'll launch the cross-suite assessor with the merged behavior summaries. The batch produced one consolidated table covering all 33 files; I'll feed it forward along with the three in-scope cross-suite slugs.

The cross-suite assessor summarized instead of emitting the formal five-field findings. I need to retrieve the structured findings to compose the report.

Wrote the report to `/home/mobaxterm/Documents/git/ai-rizz/slobac-audit.md`.

**Scope covered:** all 15 supported slugs (the `all` wildcard). 13 per-test/per-file slugs ran through one batch assessor (the suite's ~389K chars fit comfortably under the 1M-token content budget); the 3 cross-suite slugs (`semantic-redundancy`, `wrong-level`, `deliverable-fossils` Phase B) ran through one cross-suite assessor over the merged behavior summaries with `full` richness.

**Headline numbers:** 17 findings — 7 `semantic-redundancy` (cross-suite), plus per-test: 3 `vacuous-assertion`, 2 `naming-lies`, 2 `rotten-green`, 1 `tautology-theatre`, 1 `conditional-logic`, 1 `monolithic-test-file`. Eight slugs cleared with zero findings (`deliverable-fossils` both phases, `implementation-coupled`, `mystery-guest`, `over-specified-mock`, `presentation-coupled`, `pseudo-tested`, `shared-state`, `wrong-level`). The largest concentrations are the `test_cli_init.test.sh` ↔ `test_initialization.test.sh` cross-tier duplication (4 findings) and `test_help_and_usage.test.sh`'s loose oracles (3 findings).

