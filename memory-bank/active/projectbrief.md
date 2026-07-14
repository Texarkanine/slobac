# Project Brief

## User Story

As a reader of the SLOBAC docs site, I want a gentle creamy/papery visual theme in both light and dark modes so the manifesto feels warm and editorial rather than default Material indigo tech-docs.

## Use-Case(s)

### Use-Case 1

A visitor opens the published GitHub Pages docs (or a local `properdocs serve` preview) and sees warm cream/manila surfaces in light mode, with readable body text and restrained chrome.

### Use-Case 2

The same visitor toggles (or prefers) dark mode and sees a warm dark background with orange/amber accents for links and highlights — Claude-docs-adjacent feel without copying Anthropic brand hexes.

## Requirements

1. Restyle the ProperDocs / Material theme away from the current indigo `default`/`slate` palette.
2. Light mode: gentle creamy / papery / manila-warm surfaces (Cursor-docs and Claude-docs inspired).
3. Dark mode: warm dark background with warm orange accents for highlights/links (similar role to Claude’s orange-on-dark).
4. Use an original SLOBAC palette or openly reusable warm scales — do not drop in Anthropic/Claude reconstructed brand token packs as the site’s identity.
5. Preserve existing Material features, navigation, plugins, and content; this is theme/styling only.

## Constraints

1. Stay on ProperDocs + `mkdocs-material` (no theme-engine swap).
2. Do not rip Anthropic’s proprietary brand colors as a named “Claude” scheme.
3. Keep CI docs build (`--strict`) green; visual changes must not break validation.
4. Content under `skills/slobac-audit/references/docs/` is out of scope except where theme assets must live beside the build config.

## Acceptance Criteria

1. Light and dark palettes are both available (existing toggle / `prefers-color-scheme` pattern retained or improved).
2. Light mode reads as warm paper/cream, not cool gray or pure white default.
3. Dark mode uses warm neutrals and orange/amber accent highlights (not cool blue-slate + indigo).
4. Palette is documented as SLOBAC’s own tokens (or cited open scale), not as an Anthropic clone.
5. `uv run properdocs build --strict` (or project-equivalent docs CI) succeeds.
