# Slobac audit command
_Exported on 5/7/2026 at 08:54:48 CDT from Cursor (3.3.12)_

---

**User**

/slobac-audit 

---

**Cursor**

`slobac-audit` needs two things from you before it can run:

## 1. Target suite root (required)

You didn’t name a directory. The workflow **does not** default to the whole repo — please give an explicit path to the tests to audit (for example `tests/`, `tests/unit/`, or another folder).

## 2. Smell scope

You didn’t name any smell slugs. Under this skill, **no slugs** means the **full supported-slug set** (“all” / unscoped).

---

Reply with **only** the target directory path (and optionally a different output file path if you don’t want `./slobac-audit.md`). After that, the audit can proceed with all taxonomy slugs and the default report location (or the next free name if `slobac-audit.md` already exists).

---

**User**

@tests - all smells, 200k context window

---

**Cursor**

Running the slobac-audit workflow: gathering taxonomy slugs, reference materials, and enumerating the `tests` directory.



Reading taxonomy entries for Detection Scope and building the suite manifest from the `tests` directory.



Suite manifest: 29 `*.test.sh` files, 388,842 chars total — under the 200k-window content budget (~400k chars at 60%), so one batch. ~379 tests → richness `full`. Launching the batch assessor (readonly) to read all test files and taxonomy entries, then running the cross-suite assessor.



Verifying key batch findings against source and retrying completion of the behavior-summary table (batch output was truncated).



Writing the report to `slobac-audit.md`, merging verified batch findings and cross-suite results.



Report written to **`/home/mobaxterm/git/ai-rizz/slobac-audit.md`** (no existing file there, so no `-2` suffix).

**Scopes covered:** full taxonomy (**15** slugs): `conditional-logic`, `deliverable-fossils`, `implementation-coupled`, `monolithic-test-file`, `mystery-guest`, `naming-lies`, `over-specified-mock`, `presentation-coupled`, `pseudo-tested`, `rotten-green`, `semantic-redundancy`, `shared-state`, `tautology-theatre`, `vacuous-assertion`, `wrong-level`.

Per the audit workflow, **details live only in that report** — open it for findings, explicit zero-scope lines, orchestration notes (200k context, one batch assessor, cross-suite run, planned `full` behavior summaries), and “tests considered but not flagged.”

