---
task_id: per-skill-reuse-bundles
complexity_level: 2
date: 2026-05-04
status: completed
---

# TASK ARCHIVE: Per-skill LICENSES + REUSE.toml (static bundles)

## SUMMARY

Added REUSE-compliant, self-contained license bundles (`LICENSES/`, `REUSE.toml`, `license:` front matter) to all four SLOBAC skills (`slobac-audit`, `slobac-batch`, `slobac-cross-suite`, `slobac-scout`) so a marketplace-only install carries the full AGPL + PPL-S license texts (plus CC-BY-SA-4.0 for `slobac-audit` docs) without requiring the repo root. All acceptance criteria were met; `reuse --root . lint` exits 0 for every skill root and for the repo root (163/163 files).

One unplanned addition: `BUNDLED-AGPL.md` (one per skill) was introduced to satisfy REUSE's "no unused licenses" rule for the bundled AGPL text. This is consistent with the brief's intent and adds no maintenance overhead.

## REQUIREMENTS

From the project brief:

1. Every skill at `skills/*/SKILL.md` has bundled license texts under that skill's `LICENSES/` using REUSE-required layout and filenames aligned with SPDX identifiers.
2. Every skill has a `REUSE.toml` whose paths are relative to the skill root and mirror repo policy (PPL-S for prompt-shaped payload, CC-BY-SA-4.0 for `slobac-audit` docs subtree).
3. `SKILL.md` YAML front matter includes a `license:` string pointing humans and validators at the bundle.
4. AGPL-3.0-or-later full text is bundled wherever PPL-S is claimed (PPL-S extends AGPL by reference).
5. **Static only:** no Makefile, `pyproject.toml` scripts, or generators.

All five requirements and all three acceptance criteria (per-skill `reuse --root . lint` exits 0; all four skills contain `LICENSES/` + `REUSE.toml`; each `SKILL.md` has a consistent `license:` field) were fully satisfied.

## IMPLEMENTATION

**Per skill bundle structure (batch, scout, cross-suite):**

- `LICENSES/LicenseRef-PPL-S.txt` — byte-identical copy from repo root
- `LICENSES/AGPL-3.0-or-later.txt` — byte-identical copy from repo root
- `LICENSES/BUNDLED-AGPL.md` — minimal witness file annotated as `AGPL-3.0-or-later`; satisfies REUSE "no unused licenses" rule; documents the PPL-S ↔ AGPL relationship
- `REUSE.toml` — `version = 1`, package name/supplier consistent with root, single `[[annotations]]` block `path = ["**/*"]` → `LicenseRef-PPL-S`
- `SKILL.md` — added `license:` front matter (headline PPL-S + pointer to `LICENSES/` and `REUSE.toml`)

**`slobac-audit` additions:**

- Same as above plus `LICENSES/CC-BY-SA-4.0.txt` (third license text)
- `REUSE.toml` has a second `[[annotations]]` block with `precedence = "override"`, `path = ["references/docs/**"]`, `SPDX-License-Identifier = "CC-BY-SA-4.0"` — mirrors root `REUSE.toml` policy for the manifesto docs subtree
- `README.md` — added standalone licensing paragraph noting that `LICENSES/` and `REUSE.toml` ship with each skill for marketplace/tarball distribution

**Repo root:** unchanged (no deletions or modifications to root `LICENSES/` or `REUSE.toml`).

## TESTING

Verification used `reuse --root . lint` as the TDD harness (no pytest; no test runner in scope):

- **RED baseline (before artifacts):** Confirmed each skill root lacked REUSE metadata and would fail lint.
- **GREEN per slice:** After adding `LICENSES/` + `REUSE.toml` for each skill, ran `reuse --root . lint` from the skill directory — exit 0 required before proceeding.
- **Post-SKILL.md lint:** Re-ran after adding `license:` front matter to confirm no regression.
- **Final file counts:** batch 3/3, scout 4/4, cross-suite 3/3, audit 28/28.
- **Repo root regression:** `reuse lint` at repo root — exit 0 (163/163 files).
- **Docs build:** `uv run properdocs build --strict` — exit 0.
- **`/niko-qa` semantic review:** No defects found; no rework required.

## LESSONS LEARNED

- **`reuse --root .` is load-bearing inside a Git monorepo.** Plain `reuse lint` always ascends to the `.git` boundary; `--root .` is required to treat a subdirectory as a self-contained REUSE project. Any future per-skill or per-package REUSE work in this repo must use this flag. The tasks.md Test Plan was corrected in-place during Build to reflect this.
- **REUSE's "no unused licenses" rule requires a witness annotation for compliance-only bundled texts.** A `LICENSES/*.txt` not referenced by any annotation causes `reuse lint` to fail. The `BUNDLED-AGPL.md` pattern is a clean, repeatable solution for bundling licenses that exist for downstream legal obligations rather than for annotating source files.
- **`reuse lint` as a TDD harness works well.** Per-skill RED → GREEN cycles gave precise, fast feedback per slice. The pattern generalizes to any compliance-validator-as-test approach.

## PROCESS IMPROVEMENTS

- **Preflight caught plan-shape gaps before any build work began.** The first preflight run failed because the Implementation Plan didn't explicitly encode RED/GREEN verification ordering per slice. Catching this before Build saved iteration later.
- Future tasks involving nested REUSE projects inside a Git monorepo should explicitly call out `reuse --root . lint` (not `reuse lint`) in the Test Plan from day one.

## TECHNICAL IMPROVEMENTS

- If more skills are added to the repo, the `BUNDLED-AGPL.md` + per-skill `REUSE.toml` pattern can be stamped out mechanically from the existing four examples. A future generator or Makefile target could automate this if the skill count grows significantly — but not warranted now (constraint: static only unless `reuse lint` proves insufficient).

## NEXT STEPS

None. The per-skill REUSE bundle pattern is complete and validated. The repo root retains full-tree lint authority; each skill carries its own bundle for marketplace distribution.
