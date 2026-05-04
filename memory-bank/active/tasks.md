# Task: Per-skill LICENSES + REUSE.toml (static bundles)

* Task ID: per-skill-reuse-bundles
* Complexity: Level 2
* Type: Simple enhancement (licensing / compliance packaging)

Add committed `LICENSES/` texts and a skill-scoped `REUSE.toml` under each `skills/<name>/` tree so a marketplace-only install is REUSE-valid and ships AGPL + PPL-S (plus CC-BY-SA for `slobac-audit` manifesto docs). Add agentskills `license:` front matter on each `SKILL.md`. No generators or `pyproject.toml` wrappers unless manual `reuse lint` per skill is insufficient later.


## Test Plan (TDD)

Verification is **not** pytest (see `memory-bank/techContext.md` — no test runner yet). For this task, **`reuse lint` from each skill root** is the observable harness: run it **before** adding per-skill metadata (expect non-passing / actionable REUSE errors), then after each skill’s bundle is complete (expect exit code 0).

### Behaviors to Verify

- **[Batch root is a REUSE project]** `cd skills/slobac-batch && reuse lint` → process exits 0; no missing-license / missing-copyright findings for files under that tree.
- **[Scout root is a REUSE project]** Same for `skills/slobac-scout/`.
- **[Cross-suite root is a REUSE project]** Same for `skills/slobac-cross-suite/`.
- **[Audit root is a REUSE project]** Same for `skills/slobac-audit/`, with **`references/docs/**`** files annotated as **CC-BY-SA-4.0** and non-docs skill payload as **LicenseRef-PPL-S** (mirrors root `REUSE.toml` policy).
- **[SKILL.md license field]** Each `skills/*/SKILL.md` includes YAML `license:` whose meaning matches the bundled texts (headline PPL-S + pointer to `LICENSES/` and `REUSE.toml`; audit may mention CC-BY-SA docs in text or rely on `REUSE.toml` for detail—either way, no contradiction with `reuse lint`).
- **[AGPL bundled with PPL-S]** Every skill that declares `LicenseRef-PPL-S` includes `LICENSES/AGPL-3.0-or-later.txt` (byte-identical copy from repo root `LICENSES/AGPL-3.0-or-later.txt`).

### Edge Cases / Regression

- **Wrong glob in skill `REUSE.toml`:** `reuse lint` fails for paths with no annotation (e.g. forgetting `references/docs/**` override on audit).
- **Missing license file on disk:** `reuse lint` or REUSE complains that identifier has no matching file under `LICENSES/` (filenames must align with SPDX IDs used).
- **Repo root unchanged:** Root `REUSE.toml` and root `LICENSES/` remain authoritative for full-repo checks; per-skill trees only **duplicate** policy for standalone distribution (no accidental deletion of root files).

### Test Infrastructure

- **Framework:** [REUSE](https://reuse.software/) CLI (`reuse lint`).
- **Test location:** N/A (validator is CLI + cwd).
- **Conventions:** Run with **current working directory** = skill root (`skills/<name>/`).
- **New test files:** None (no pytest). Optional future CI job is advisory only per project brief.

## Implementation Plan

Each numbered step is one vertical slice: **verify RED → add artifacts → verify GREEN** for that slice before moving on.

1. **Baseline RED — confirm harness**
   - **Verify:** From repo root, run `cd skills/slobac-batch && reuse lint` (repeat appetite: spot-check one other skill). Capture that failures are **about missing REUSE metadata**, not unrelated environment errors. If `reuse` is not installed, stop and install tooling — document under Technology Validation.
   - **Files:** None.

2. **`slobac-batch` — LICENSES + REUSE.toml + SKILL front matter**
   - **Verify (RED):** `cd skills/slobac-batch && reuse lint` (non-zero / actionable).
   - **Files:**
     - Create `skills/slobac-batch/LICENSES/LicenseRef-PPL-S.txt` — copy from `LICENSES/LicenseRef-PPL-S.txt`.
     - Create `skills/slobac-batch/LICENSES/AGPL-3.0-or-later.txt` — copy from `LICENSES/AGPL-3.0-or-later.txt`.
     - Create `skills/slobac-batch/REUSE.toml` — `version = 1`, `SPDX-PackageName = "slobac-batch"`, `SPDX-PackageSupplier` matches root `REUSE.toml`; single `[[annotations]]` block `path = ["**/*"]` with `SPDX-FileCopyrightText` / `SPDX-License-Identifier = "LicenseRef-PPL-S"` (mirror root `skills/**` rule).
   - **Verify (GREEN):** `cd skills/slobac-batch && reuse lint` → success.
   - **Files:** Edit `skills/slobac-batch/SKILL.md` front matter — add `license:` (see project brief).
   - **Verify:** `reuse lint` still succeeds.

3. **`slobac-scout` — same pattern as batch**
   - **Files:** `skills/slobac-scout/LICENSES/` (same two files as step 2), `skills/slobac-scout/REUSE.toml` (`SPDX-PackageName = "slobac-scout"`), `skills/slobac-scout/SKILL.md` (`license:`).
   - **Verify:** RED (optional if predictable) → GREEN `reuse lint` after bundle + after SKILL edit.

4. **`slobac-cross-suite` — same pattern as batch**
   - **Files:** `skills/slobac-cross-suite/LICENSES/` (same two files), `skills/slobac-cross-suite/REUSE.toml` (`SPDX-PackageName = "slobac-cross-suite"`), `skills/slobac-cross-suite/SKILL.md` (`license:`).
   - **Verify:** GREEN `reuse lint` after bundle + after SKILL edit.

5. **`slobac-audit` — LICENSES including CC-BY-SA + scoped REUSE.toml + SKILL front matter**
   - **Verify (RED):** `cd skills/slobac-audit && reuse lint` fails until metadata exists.
   - **Files:**
     - Create `skills/slobac-audit/LICENSES/LicenseRef-PPL-S.txt`, `AGPL-3.0-or-later.txt`, `CC-BY-SA-4.0.txt` — copies from repo root `LICENSES/` (three files).
     - Create `skills/slobac-audit/REUSE.toml`: default `**/*` → `LicenseRef-PPL-S`; second `[[annotations]]` with `precedence = "override"`, `path = ["references/docs/**"]`, `SPDX-License-Identifier = "CC-BY-SA-4.0"` (mirror root `skills/slobac-audit/references/docs/**` rule); supplier/package fields consistent with root.
   - **Verify (GREEN):** `cd skills/slobac-audit && reuse lint` → success.
   - **Files:** Edit `skills/slobac-audit/SKILL.md` front matter — add `license:` per brief (headline + pointer; CC-BY-SA for docs may be in prose or left to `REUSE.toml`).
   - **Verify:** `reuse lint` still succeeds.

6. **Documentation touchpoints (minimal)**
   - **Files:** If `skills/slobac-audit/README.md` (or sibling READMEs) describes distribution, add **one short paragraph** that standalone installs include `LICENSES/` + `REUSE.toml` by design. Skip if no reader-facing “install from tarball” section exists yet.

## Technology Validation

- **REUSE CLI:** Required on developer/CI machines for `reuse lint`. Not added to `pyproject.toml` unless the project later chooses to pin it; validation = manual `which reuse` / `reuse --version` before build.
- **No new Python/npm dependencies** for this enhancement.

## Dependencies

- [REUSE](https://reuse.software/) tool (`reuse lint`) available in PATH when validating.
- Canonical license texts in repo root: `LICENSES/LicenseRef-PPL-S.txt`, `LICENSES/AGPL-3.0-or-later.txt`, `LICENSES/CC-BY-SA-4.0.txt`.

## Challenges & Mitigations

- **`reuse` not installed locally:** Mitigation — install via distro package or `pipx install reuse` per upstream docs; cannot complete GREEN without it.
- **REUSE.toml precedence / glob mistakes:** Mitigation — after each skill, run `reuse lint` only from that skill root; fix annotations until exit 0.
- **Drift between root and per-skill license text:** Mitigation — copies are static; if root `LICENSES/` changes later, update each skill’s copies in the same change (document in commit message). No automation in scope.

## Preflight (2026-05-04)

- **Result:** PASS — proceed to Build.
- **Advisory:** Reorder Implementation Plan bullets for steps 3–4 to put **Verify (RED)** before **Files** (parity with step 2); optional one-shot `reuse lint` over all `skills/*/` for regression after the last slice.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight
- [ ] Build
- [ ] QA
