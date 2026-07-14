# Task: creamy-papery-docs-theme

* Task ID: creamy-papery-docs-theme
* Complexity: Level 2
* Type: simple enhancement

Restyle the ProperDocs / Material docs site from indigo default/slate to an original SLOBAC warm paper (light) + warm dark with amber/orange accents theme, wired through Material custom CSS variables and `extra_css`.

## Test Plan (TDD)

### Behaviors to Verify

- [Palette wiring]: `properdocs.yaml` theme palette uses `primary: custom` and `accent: custom` (both light and dark entries) → Material loads custom CSS variables instead of indigo
- [Stylesheet registration]: `properdocs.yaml` lists `extra_css` including `stylesheets/extra.css` → build includes the override sheet
- [Light scheme tokens]: CSS for `[data-md-color-scheme="default"]` (or `:root` / default scheme) defines warm paper background and warm ink foreground via `--md-default-bg-color` / `--md-default-fg-color` (and primary/accent shades) → light mode is cream/paper, not cool gray/white+indigo
- [Dark scheme tokens]: CSS for `[data-md-color-scheme="slate"]` defines warm dark background and amber/orange primary/accent (and typeset link color where overridden) → dark mode uses warm neutrals with orange highlights
- [Warm chrome surfaces]: both schemes set warm `--md-code-bg-color` (and footer bg) → code wells / footer do not remain cool-gray defaults on paper/ember canvases
- [No indigo palette]: palette blocks no longer set `primary: indigo` / `accent: indigo` → default Material indigo is gone
- [Strict build]: `uv run properdocs build --strict` → exits 0 (existing CI gate; no link/theme breakage)
- [Edge — toggle retained]: both light and dark palette entries with toggle icons remain → user can still switch schemes
- [Edge — manifesto untouched]: taxonomy/principles markdown content unchanged → theme-only change
- [Edge — empty CSS regression]: stylesheet file is non-empty and contains both scheme selectors → empty override cannot silently ship

### Test Infrastructure

- Framework: pytest (existing; `pyproject.toml` `[tool.pytest.ini_options]` `testpaths = ["tests/python"]`)
- Test location: `tests/python/unit/`
- Conventions: `test_*.py` modules, plain pytest functions, Path-based file reads (see `test_end_to_end.py` / sibling unit tests); no browser/visual harness exists
- New test files: `tests/python/unit/test_docs_theme_tokens.py`
- Out of band (not automated): visual acceptance via `uv run properdocs serve` during QA — no visual-regression framework to extend; do not invent Playwright/Percy for this task

## Implementation Plan

1. **Stub theme contract tests (fail first)**
   - Files: `tests/python/unit/test_docs_theme_tokens.py` (new)
   - Changes: Add tests asserting `properdocs.yaml` palette custom + `extra_css`, and that `skills/slobac-audit/references/docs/stylesheets/extra.css` exists with default + slate scheme selectors and required `--md-*` custom properties (paper bg, warm fg, amber accents). Run pytest — expect failures.

2. **Add empty stylesheet + wire config (still red on token assertions)**
   - Files: `skills/slobac-audit/references/docs/stylesheets/extra.css` (new), `properdocs.yaml`
   - Changes: Create stylesheet path; set `extra_css: [stylesheets/extra.css]`; set both palette entries to `primary: custom`, `accent: custom`; keep `scheme: default` / `scheme: slate` and existing toggles / `prefers-color-scheme` media queries. Stub CSS with scheme selectors but placeholder values if needed so wiring tests start passing while token-content tests still fail.

3. **Implement SLOBAC paper/ember token set**
   - Files: `skills/slobac-audit/references/docs/stylesheets/extra.css`
   - Changes: Original warm palette (inspired by open warm scales such as Tailwind stone/amber *feel*, not Anthropic reconstruction hex packs). Light: cream/paper `--md-default-bg-color`, warm ink fg, soft ember primary header, amber accent/links. Dark (`slate`): warm charcoal bg, warm elevated surfaces, amber/orange `--md-primary-*` / `--md-accent-*` / `--md-typeset-a-color` for orange-on-dark highlights. Also warm secondary surfaces so the theme does not read as “cream canvas + cold Material chrome”: `--md-code-bg-color`, `--md-code-fg-color`, and footer vars (`--md-footer-bg-color` / fg) under both schemes. Tune `--md-hue` only if needed as a secondary tweak — prefer explicit hex tokens for predictability. Comment in CSS that tokens are SLOBAC-original.

4. **Make contract tests green; run strict build**
   - Files: `tests/python/unit/test_docs_theme_tokens.py`, (verify) `properdocs.yaml`, `extra.css`
   - Changes: Align test expectations with final token names/selectors; run `uv run pytest tests/python/unit/test_docs_theme_tokens.py` then full `tests/python`; run `uv run properdocs build --strict`.

5. **Docs / orientation touch-ups if needed**
   - Files: `memory-bank/techContext.md` only if Design System pointer is warranted; skip README/CONTRIBUTING unless they currently claim indigo branding (they do not today)
   - Changes: Optional one-line Design System pointer to `stylesheets/extra.css` as the docs visual authority — only if techContext’s Design System section is the right home; otherwise leave persistent files alone per update rules.

## Technology Validation

No new technology - validation not required. Uses existing ProperDocs + Material custom CSS variables ([Changing the colors](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/)).

## Dependencies

- Existing: `properdocs`, `mkdocs-material` (docs dependency group)
- Existing: pytest for contract tests
- No new packages

## Challenges & Mitigations

- [CSS lives under manifesto `docs_dir`]: Material `extra_css` paths are relative to `docs_dir`, so the sheet must sit under `skills/slobac-audit/references/docs/stylesheets/`. Mitigation: keep only theme assets there; do not alter manifesto markdown; ensure `.pages` / awesome-pages ignores non-md (default).
- [Accidental Anthropic hex clone]: Easy to paste reconstruction packs. Mitigation: pick distinct SLOBAC hexes; comment “original / open-scale inspired”; avoid naming tokens `claude` / `anthropic`.
- [Material header vs body contrast]: Custom primary can make header too loud or muddy. Mitigation: softer ember for light primary; reserve stronger amber for dark accents/links; iterate once under `properdocs serve` during build/QA.
- [No visual regression harness]: Automated tests cannot prove “creamy feel.” Mitigation: contract tests for wiring + tokens; visual check is explicit QA acceptance criterion.
- [REUSE / license path]: New file under skill docs tree may fall under existing CC-BY-SA mapping. Mitigation: confirm `skills/slobac-audit/REUSE.toml` glob coverage; no new license text unless mapping excludes stylesheets.

## Pre-Mortem

- [Plan “failed” because the site still looked like default Material despite CSS]: Cause would be wrong scheme selectors or forgetting `primary: custom`. Covered by Challenges (wiring) + Behaviors 1–2; keep step 2 ordering (wire before polish).
- [Plan “failed” because reviewers called it a Claude rip]: Cause would be copying published Anthropic reconstruction tokens. Already covered by Challenge 2; during build, deliberately offset hues from common `#faf9f5` / `#c96442` clones if those appear in drafts.
- [Plan “failed” because pytest had nothing honest to assert and green-washed]: Avoid testing only “file exists.” Token tests must assert specific custom-property *presence under both scheme selectors* and absence of indigo in yaml.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA

## Build Checklist

- [x] Stub theme contract tests (fail first)
- [x] Add stylesheet + wire `properdocs.yaml` (`primary`/`accent: custom`, `extra_css`)
- [x] Implement SLOBAC paper/ember token set (incl. code/footer chrome)
- [x] Contract tests green; full `tests/python` green; `properdocs build --strict` green
- [x] `techContext.md` Design System pointer updated

## Preflight Amendments

- Extended token scope to code-block and footer surfaces under both schemes (avoids cold Material chrome on a warm canvas).
- Confirmed `references/docs/**` REUSE override → new `stylesheets/extra.css` is CC-BY-SA-4.0 with the manifesto tree (acceptable; no plan change required).

## QA Results

- PASS. Visual check (light + dark via `properdocs serve`): cream paper canvas and ember header in light; warm charcoal + orange link accents in dark.
- Trivial fix applied: softened dark-mode `--md-primary-fg-color` from `#f59e0b` to `#b45309` so the header is gentler while `--md-typeset-a-color` / accent stay `#fb923c` for orange highlights.
