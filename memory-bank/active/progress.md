# Progress

Expose SLOBAC as a Cursor and Claude Code plugin, with marketplace entries in `txrk9-agent-plugins`. Includes renaming the four skill directories from `slobac-*` to short names, updating SKILL.md `name` fields to `slobac:*`, updating all internal cross-references, rewriting the install docs for marketplace, and adding four manifest files.

**Complexity:** Level 3

## Phase Log

- **2026-05-05** — Complexity analysis complete. Level 3 selected: spans two repos, multiple manifest files with design decisions about plugin naming, skill auto-discovery, and cross-repo source referencing.
- **2026-05-05** — Plan phase complete. Scope expanded to include skill directory renames and SKILL.md `name` field updates to achieve `/slobac:audit` in both Cursor and Claude Code. Key insight: Cursor uses SKILL.md frontmatter `name` field for invocation (not folder name); Claude Code uses `plugin-name:folder-name`. Both renames required for consistent `/slobac:*` UX.
