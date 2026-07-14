---
task_id: creamy-papery-docs-theme
complexity_level: 2
date: 2026-07-14
status: completed
---

# TASK ARCHIVE: creamy-papery-docs-theme

## SUMMARY

Restyled the ProperDocs / Material docs site from indigo default/slate to an original SLOBAC **paper/ember** theme: warm cream light (`#f6f0e4`), warm charcoal dark (`#1c1914`), ember header chrome, orange link accents (`#fb923c`). Dark header primary settled on variant **D** (`#de8131`) after operator side-by-side review. Theme CSS lives under the manifesto `docs_dir`; contract-tested; strict build green.

## REQUIREMENTS

- Creamy/papery light mode and warm dark with orange highlights (Cursor/Claude-docs *feel*, not Anthropic hex rip)
- Stay on ProperDocs + Material; content unchanged
- Original or openly inspired tokens; light+dark toggle retained
- CI `properdocs build --strict` remains green

## IMPLEMENTATION

- `properdocs.yaml`: `primary`/`accent: custom`; `extra_css: stylesheets/extra.css`
- `skills/slobac-audit/references/docs/stylesheets/extra.css`: scheme tokens for `default` and `slate` (surfaces, primary/accent, code, footer, typeset links)
- `tests/python/unit/test_docs_theme_tokens.py`: wiring + token contract tests (text/regex on yaml — `!!python/object/apply` slugify blocks `yaml.safe_load`)
- `memory-bank/techContext.md`: Design System pointer to the CSS file
- Post-reflect: dark primary tuned via variant board A–F; operator approved **D** (`#de8131`); F rejected as too bright

## TESTING

- pytest: 5 new theme contracts; full `tests/python` 29 passed
- `uv run properdocs build --strict` passed
- `/niko-qa` visual check light+dark; later operator browser compare for header D vs F

## LESSONS LEARNED

- Material `primary` paints the full header — use deeper/softer primary for chrome and keep bright orange on `--md-typeset-a-color` / accent for “highlights.”
- Light and dark should be *paired* tokens, not one shared header hex.
- MkDocs configs with Python constructors need text contracts, not SafeLoader YAML parses.
- Side-by-side HTML variant cards beat serial “try one hex” loops for color picks.

## PROCESS IMPROVEMENTS

- For future palette tweaks, a throwaway `scratch/` preview board (gitignored) is enough; no need to invent multiple Material schemes.

## TECHNICAL IMPROVEMENTS

- Optional later: a distinct SLOBAC project mark (not the personal Texarkanine dog/# logo) if/when branding is an explicit task — out of scope here.

## NEXT STEPS

None for this theme task. A SLOBAC logo (separate from owner personal brand) can be a future `/niko` if desired.
