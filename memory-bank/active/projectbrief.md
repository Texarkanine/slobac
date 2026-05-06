# Project Brief

## User Story

As a slobac maintainer, I want automated release management via release-please so that conventional commits on `main` automatically produce versioned releases with consistent version bumps across all plugin manifests, without any manual tagging or version-file editing.

## Use-Cases

### Use-Case 1: Cutting a release

Maintainer merges a `feat:` or `fix:` commit to `main`. Release-please opens or updates a Release PR that bumps `version.txt`, `.cursor-plugin/plugin.json`, and `.claude-plugin/plugin.json` in lockstep, and updates `CHANGELOG.md`. Maintainer merges the Release PR; release-please creates the GitHub release and tag.

### Use-Case 2: Preparing for future CI

GitHub App token is used rather than `GITHUB_TOKEN` so that CI workflows (none yet, but anticipated) will trigger on Release Please PRs when they are eventually added.

## Requirements

1. Add `release-please-config.json` using manifest-style configuration with `release-type: simple`.
2. Add `.release-please-manifest.json` with current version `0.2.0` at package root `.`.
3. Add `.github/workflows/release-please.yaml` that triggers on `push: main`, uses the shared GitHub App (`vars.HELPER_APP_ID` / `secrets.HELPER_APP_PRIVATE_KEY`) for token generation, and runs `googleapis/release-please-action@v4`.
4. The release-please config must update three version files in sync: `version.txt` (primary, managed by `simple` type), `.cursor-plugin/plugin.json` (`$.version` via extra-files), and `.claude-plugin/plugin.json` (`$.version` via extra-files).
5. The release-please Release PR header must be the bark-and-woof message from the jekyll-auto-thumbnails reference: `:service_dog: I have created a release \*bark\* \*woof\*`.
6. Use `bump-minor-pre-major: true` and `bump-patch-for-minor-pre-major: false` since the project is pre-1.0 (`0.x`).
7. Modify `.github/workflows/docs.yaml` to trigger on `push: tags: ['v*']` instead of `push: branches: [main]`, so documentation is only published for released code. PR builds (for link validation) and `workflow_dispatch` are preserved.

## Constraints

1. No publish step — this is version-management CI only.
2. No lockfile to update; release-please must not assume any exists.
3. The two plugin.json files must always be in sync (both updated on every release PR merge).
4. Token approach uses GitHub App, not `GITHUB_TOKEN`, for forward-compatibility with future branch-CI.
5. `include-component-in-tag: false` — single-package repo, no component prefix on tags.

## Acceptance Criteria

1. `release-please-config.json` and `.release-please-manifest.json` exist at repo root, are valid JSON, and match the specified configuration.
2. `.github/workflows/release-please.yaml` exists, is valid YAML, triggers on push to `main`, uses the GitHub App token action, and invokes `googleapis/release-please-action@v4` with manifest mode.
3. `.github/workflows/docs.yaml` is updated so the `push` trigger targets `tags: ['v*']` instead of `branches: [main]`; deploy job condition remains correct.
4. A push of a `feat:` conventional commit to `main` would (in CI) produce a Release PR that updates all three version files and `CHANGELOG.md`.
