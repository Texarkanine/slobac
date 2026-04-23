---
task_id: phase0-docs-publish
date: 2026-04-23
complexity_level: 2
---

# Reflection: Phase 0 docs publishing — mkdocs-material to GitHub Pages

## Summary

Published the `docs/` manifesto to GitHub Pages via mkdocs-material + a pared-down GitHub Actions workflow using `actions/deploy-pages` (no `gh-pages` branch). Strict-mode link validation is in place as the mechanized defense for the cross-link integrity invariant named in `systemPatterns.md`. All plan requirements met; clean build; one plan amendment during preflight (`mkdocs-redirects` for URL-stability pre-positioning) and three small deviations during build, all justified and documented.

## Requirements vs Outcome

Every plan requirement shipped. One side-effect deliverable marked optional in the plan (root `README.md`) shipped because the repo had no README at all — low-cost, high-signal addition. Zero requirements dropped. One addition during preflight (`mkdocs-redirects` plugin + dep) was accretive and within scope.

## Plan Accuracy

The plan sequence was right and did not need reordering. The file list was complete; `.gitignore` was handled as a known "add as needed" item and landed cleanly. Challenges that actually materialized were a near-miss for the plan's Challenge #1 ("strict mode surfaces latent broken cross-links"): the plan assumed broken links would be real authoring errors. The actual cause of the three build failures was cross-renderer slug divergence — a class of drift the plan hadn't explicitly named. The mitigation (fix the source) would've been wrong; the correct mitigation (configure a GitHub-compatible slugifier) preserved the raw-markdown-on-github.com property that the plan implicitly valued.

## Build & QA Observations

Build was mostly smooth. One iteration loop during Step 4 local validation tuned the slugifier + `validation:` config; one more tuned `docs/.pages` to drop an unsupported `title:` key. Neither was expensive. QA caught two real trivial issues, both traceable to my own authoring habits rather than plan deficiencies: (1) expanding `markdown_extensions` beyond what the plan authorized (YAGNI), (2) leaving `systemPatterns.md` describing cross-link drift defense as grep-only after we'd mechanized a secondary defense. QA was productive, not redundant.

## Insights

### Technical

- **`strict: true` in mkdocs 1.5+ does not imply comprehensive link validation.** Strict mode promotes *already-emitted* warnings to errors — it does not change what gets emitted at what level. Anchor validity is INFO by default; to make the build fail on missing anchors, you must explicitly set `validation.anchors: warn` alongside `strict: true`. Without this knowledge, you can configure strict mode and believe you're protected while a real class of drift slips through silently. Worth remembering for any future mkdocs project: the two configs are orthogonal, and both are needed.

- **GitHub and python-markdown slugify punctuation differently.** Markdown authored for native github.com rendering uses GitHub's slug rules (e.g. `Extreme mutation / pseudo-tested methods` → `#extreme-mutation--pseudo-tested-methods`, note the double-hyphen for the `/`). python-markdown (mkdocs default) uses `#extreme-mutation-pseudo-tested-methods` with a single hyphen. `pymdownx.slugs.slugify(case='lower')` is a drop-in that produces GitHub-compatible slugs, letting the same source markdown resolve identically on both surfaces. If the source-markdown-renders-on-GitHub property is load-bearing (which it is here — Phase 0's value prop is "self-contained read"), this is the correct choice.

### Process

- **Plan-as-contract even for plausible defaults.** I expanded `markdown_extensions` from the plan's explicit list to "the full mkdocs-material recommended stack" on reflex. Defensible, not plan-authorized. QA caught it cleanly, but the habit to break is "the plan said what it said; if more is needed, amend the plan, don't build past it." Future plans should authorize exact dependencies and the build should not expand.

### Million-Dollar Question

Setting this up earlier rather than later would have caught three pre-existing latent cross-link anchor bugs (`taxonomy/pseudo-tested.md` → glossary, `taxonomy/wrong-level.md` → glossary, `glossary.md` self-link) that had been shipped-but-broken since the initial manifesto commit. They wouldn't show as broken in raw-github.com markdown (where the slugs they were authored against work), but they would've been broken on the *published* site. Running mkdocs strict on day 1 of the manifesto would have caught them at authoring time instead of during Phase 0 publication. That's a real win for "mechanize the gate as early as you can afford to" — the cost of adding the gate is fixed; the value compounds with every piece of content authored since the gate existed.

Beyond that, no sweeping redesign: the choice to author markdown for GitHub-native rendering first and retrofit mkdocs via a compatible slugifier was correct. If we'd authored for python-markdown slugs first, the raw-github.com experience would be worse today, and that's the harder-to-reverse of the two constraints.
