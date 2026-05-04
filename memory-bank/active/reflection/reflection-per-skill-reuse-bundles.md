---
task_id: per-skill-reuse-bundles
date: 2026-05-04
complexity_level: 2
---

# Reflection: Per-skill LICENSES + REUSE.toml (static bundles)

## Summary

Added REUSE-compliant, self-contained license bundles (`LICENSES/`, `REUSE.toml`, `license:` front matter) to all four SLOBAC skills so a marketplace-only install carries AGPL+PPL-S (+ CC-BY-SA for audit docs) without the repo root. All acceptance criteria were met; `reuse --root . lint` exits 0 for every skill root and for the repo root.

## Requirements vs Outcome

Full delivery. All five requirements and three acceptance criteria from the project brief were satisfied:

- All four skills have `LICENSES/` (PPL-S + AGPL; audit also CC-BY-SA) and a skill-scoped `REUSE.toml`.
- `slobac-audit` `references/docs/**` is annotated CC-BY-SA-4.0 with that text present.
- Each `SKILL.md` carries a `license:` field consistent with the bundled files.
- Static only — no generators, no new entries in `pyproject.toml`.

One unplanned addition: `BUNDLED-AGPL.md` (one per skill) was introduced to satisfy REUSE's "no unused licenses" rule for the bundled AGPL text. This is consistent with the brief's intent and adds no maintenance overhead.

## Plan Accuracy

The plan was accurate in sequence and file scope; two REUSE-specific surprises required on-the-fly adjustments.

**Surprise 1 — `--root .` is mandatory for nested REUSE projects.** The plan's test harness described `cd skills/slobac-batch && reuse lint`, but plain `reuse lint` inside a Git working tree always ascends to the nearest `.git` root and lints the entire monorepo. The correct command is `reuse --root . lint` from the skill directory. The tasks.md Test Plan was corrected in-place during Build.

**Surprise 2 — every `LICENSES/*.txt` must be referenced by at least one annotation.** REUSE treats an unreferenced license file as an error ("unused license"). The AGPL text is bundled for downstream legal compliance, but no skill source file carries an AGPL identifier. The fix — `BUNDLED-AGPL.md` with an AGPL override annotation — is minimal, self-documenting, and leaves zero debug artifacts.

The identified challenge ("REUSE.toml precedence / glob mistakes") did not materialize; the CC-BY-SA override for `references/docs/**` worked on the first attempt.

## Build & QA Observations

Build was clean once the two surprises were resolved. Each slice's RED→GREEN cycle worked as designed. QA found no defects; no rework was required. Final lint counts: batch 3/3, scout 4/4, cross-suite 3/3, audit 28/28, repo root 163/163.

## Insights

### Technical

- **`reuse --root .` is load-bearing inside a Git monorepo.** Plain `reuse lint` always ascends to the `.git` boundary; the `--root .` flag is required to treat a subdirectory as a self-contained REUSE project. Any future per-skill or per-package REUSE work in this repo must use this flag.
- **REUSE's "no unused licenses" rule requires a witness annotation for compliance-only bundled texts.** A license file in `LICENSES/` not referenced by any annotation causes `reuse lint` to fail. The `BUNDLED-AGPL.md` pattern (a minimal file whose sole purpose is to carry the annotation) is a clean, repeatable solution for bundling licenses that exist for downstream legal obligations rather than for annotating source files.

### Process

- **Preflight caught plan-shape gaps before any build work began.** The first preflight run failed because the Implementation Plan didn't explicitly encode the RED/GREEN verification ordering per slice. Catching this before Build saved iteration later — the enforcement cost is worth the up-front friction.
- **`reuse lint` as a TDD harness works well.** Running per-skill RED (pre-artifacts) and GREEN (post-artifacts) gave precise, fast feedback per slice. The pattern generalizes to any compliance-validator-as-test approach.

### Million-Dollar Question

If per-skill REUSE compliance had been a foundational assumption from the start, the resulting architecture would be identical to what was built. The "duplicate-for-standalone-distribution" pattern is the correct tradeoff for a monorepo that also ships distributable skill bundles: the repo root retains full-tree lint authority, and each skill carries its own bundle for marketplace distribution. Nothing structurally simpler exists at this intersection of constraints.
