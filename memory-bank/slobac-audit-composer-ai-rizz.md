# Code smells audit with context window
_Exported on 5/7/2026 at 08:55:19 CDT from Cursor (3.3.12)_

---

**User**

/slobac-audit @tests all smells, 200k context window

---

**Cursor**

Running the slobac-audit workflow: locating the skill's `references/`, enumerating taxonomy slugs and detection scopes, then building the suite manifest and performing the audit.



Building the suite manifest and reading test files to perform the audit. Gathering file stats and taxonomy signals for smell detection.



Partitioning: total 421,735 chars exceeds the 200k×60% ≈400k-char content budget — splitting into two batches (lex order: batch 1 through `unit/test_skill_sync.test.sh` ≈399k chars; batch 2 = last two unit files). Richness=full (~440 tests). Searching the suite for taxonomy signals and reading `common.sh` plus representative tests.



The audit is written to:

**`/home/mobaxterm/Documents/git/ai-rizz/slobac-audit.md`**

**Scope:** all taxonomy slugs (15 entries), target **`tests/`**, planned against a **200k-token** window with **two** batched passes (suite total ~**422k chars** versus the usual **~400k-char** ≈60% allowance), **cross-suite** pass for **`semantic-redundancy`**, **`wrong-level`**, and **`deliverable-fossils`** (Phase B), behavior summaries **`full`** richness — full detail and remediation text are only in that file, per the skill.

