---
task_id: release-please-ci
complexity_level: 2
date: 2026-05-06
status: completed
---

# TASK ARCHIVE: Add release-please CI pipeline

## SUMMARY

Added manifest-style release-please configuration and a GitHub Actions workflow to automate versioned releases from conventional commits on `main`. Updated the docs workflow to deploy only when a GitHub release is published (not on every push to `main`). Updated `techContext.md` to document the new toolchain.

## REQUIREMENTS

- `release-please-config.json` with `release-type: simple`, `bump-minor-pre-major: true`, extra-files syncing `$.version` in both `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json`, and bark/woof PR header.
- `.release-please-manifest.json` seeded at `0.2.0`.
- `.github/workflows/release-please.yaml` triggered on push to `main`, using GitHub App token (`vars.HELPER_APP_ID` / `secrets.HELPER_APP_PRIVATE_KEY`) and `googleapis/release-please-action@v4` in manifest mode.
- `.github/workflows/docs.yaml` trigger changed from `push: branches: [main]` to `release: types: [published]`; PR builds and `workflow_dispatch` preserved.

All requirements delivered.

## IMPLEMENTATION

Four files touched (3 new, 1 modified):

- **`release-please-config.json`** — `simple` type, `bump-minor-pre-major`, `include-component-in-tag: false`, two extra-files entries for plugin JSONs using `jsonpath: $.version`, bark/woof `pull-request-header`.
- **`.release-please-manifest.json`** — `".": "0.2.0"`.
- **`.github/workflows/release-please.yaml`** — push-to-main trigger, `actions/create-github-app-token@v3` for GitHub App auth, `googleapis/release-please-action@v4` with explicit `config-file` and `manifest-file` paths.
- **`.github/workflows/docs.yaml`** — `release: types: [published]` replaced `push: branches: [main]`.

QA caught a missing `techContext.md` entry for release-please; fixed inline as a trivial documentation update.

## TESTING

- JSON configs validated with `python3 -m json.tool`.
- YAML workflows validated with `yaml.safe_load`.
- Full release-please pipeline will be exercised after merge once `HELPER_APP_ID` and `HELPER_APP_PRIVATE_KEY` are configured in repo settings.

## LESSONS LEARNED

- `release-type: simple` + `extra-files` with `jsonpath` is the right approach for managing custom JSON version files without language-specific assumptions. `version.txt` is an inconsequential internal artifact.
- `release: types: [published]` is strictly more correct than `push: tags: ['v*']` as a docs deploy trigger — it fires when the GitHub release actually exists, not the moment the tag ref lands. Preflight's radical-innovation step surfaced this improvement.
- Plugin.json files are consumed statically by plugin frameworks and can't redirect to an external version source. Syncing via extra-files is the correct design given the constraint.

## PROCESS IMPROVEMENTS

- For pure-config tasks (no executable logic), the TDD ordering constraint is necessarily inverted: config files must exist before they can be validated. Plans for config-only tasks should preemptively flag this so preflight doesn't spend reasoning cycles on it.

## TECHNICAL IMPROVEMENTS

None — clean implementation matching the reference pattern from `jekyll-auto-thumbnails`.

## NEXT STEPS

- Configure `HELPER_APP_ID` (repo variable) and `HELPER_APP_PRIVATE_KEY` (repo secret) in slobac GitHub settings.
- Ensure "Allow GitHub Actions to create and approve pull requests" is enabled under repo Settings → Actions → General → Workflow permissions.
- After merge, release-please will create `version.txt` on its first run.
