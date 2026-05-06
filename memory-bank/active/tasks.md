# Task: Add release-please CI pipeline

* Task ID: release-please-ci
* Complexity: Level 2
* Type: Simple Enhancement (CI/CD configuration)

Add manifest-style release-please configuration and a GitHub Actions workflow to automate versioned releases from conventional commits. Also update the docs workflow to publish only on tag push, not on every `main` push.

**Files touched:**
- `release-please-config.json` (new)
- `.release-please-manifest.json` (new)
- `.github/workflows/release-please.yaml` (new)
- `.github/workflows/docs.yaml` (modified)


## Test Plan (TDD)

### Behaviors to Verify

- `release-please-config.json` is valid JSON and contains required fields (`release-type: simple`, `bump-minor-pre-major: true`, `packages."."` with extra-files for both plugin JSONs and the bark/woof PR header)
- `.release-please-manifest.json` is valid JSON with `".": "0.2.0"`
- `.github/workflows/release-please.yaml` is valid YAML, triggers on `push: branches: [main]`, defines correct permissions, uses GitHub App token step, and invokes `googleapis/release-please-action@v4` with manifest mode
- `.github/workflows/docs.yaml` push trigger is changed from `branches: [main]` to `tags: ['v*']`; `pull_request` and `workflow_dispatch` triggers are preserved; deploy job condition remains `github.event_name != 'pull_request'`
- Extra-files entries reference the correct JSON paths (`$.version`) for both `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json`

### Edge Cases

- JSON extra-files use correct `jsonpath` key (not `json-path` or `path`): `"jsonpath": "$.version"`
- `include-component-in-tag: false` is set at the package level (single-package repo)
- Concurrency group on the release-please workflow uses `cancel-in-progress: false` (matching the reference pattern — release PRs must not be cancelled)
- The docs deploy `if:` condition handles the new triggers correctly (tag push → deploy; PR → build only; workflow_dispatch → deploy)

### Test Infrastructure

- Framework: none (CI config — no unit test runner in slobac for YAML/JSON files)
- Test location: N/A
- Conventions: N/A
- New test files: none
- Validation method: `python3 -m json.tool` for JSON files; `python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))"` for YAML (or equivalent)

## Implementation Plan

1. Create `release-please-config.json`
   - Files: `release-please-config.json`
   - Changes: New file. `release-type: simple`, `bump-minor-pre-major: true`, `bump-patch-for-minor-pre-major: false`, `include-component-in-tag: false`. Package `"."` with `extra-files` array containing two JSON-type entries for `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json` (both `$.version`), and `pull-request-header` set to the bark/woof string.

2. Create `.release-please-manifest.json`
   - Files: `.release-please-manifest.json`
   - Changes: New file. Single entry: `".": "0.2.0"` (current version from both plugin.json files).

3. Create `.github/workflows/release-please.yaml`
   - Files: `.github/workflows/release-please.yaml`
   - Changes: New file. Trigger: `push: branches: [main]`. Permissions: `contents: write`, `pull-requests: write`, `issues: write`. Concurrency: group `${{ github.workflow }}-${{ github.ref }}`, `cancel-in-progress: false`. Single job `release-please` with two steps: (a) `actions/create-github-app-token@v1` using `vars.HELPER_APP_ID` and `secrets.HELPER_APP_PRIVATE_KEY`, (b) `googleapis/release-please-action@v4` with `token: ${{ steps.generate-token.outputs.token }}` and no `release-type` (manifest mode default).

4. Modify `.github/workflows/docs.yaml`
   - Files: `.github/workflows/docs.yaml`
   - Changes: Replace `push: branches: [main]` trigger block with `push: tags: ['v*']`. Deploy job `if:` condition stays as `github.event_name != 'pull_request'` (correct for tag push + workflow_dispatch → deploy; PR → build only).

5. Validate all files locally
   - Files: all four above
   - Changes: Run JSON and YAML syntax validation to confirm no parse errors before committing.

## Technology Validation

No new runtime dependencies. `googleapis/release-please-action@v4` and `actions/create-github-app-token@v1` are well-established GitHub Actions — no local installation required. Validation is purely syntax-checking the config files.

## Dependencies

- `vars.HELPER_APP_ID` and `secrets.HELPER_APP_PRIVATE_KEY` must be configured in the slobac GitHub repository settings (operator responsibility; out of scope for this task).
- `googleapis/release-please-action@v4` must be accessible from GitHub Actions runners (public action, no additional setup needed).

## Challenges & Mitigations

- **`extra-files` JSON path key name**: release-please uses `jsonpath` (not `json-path`). Validated against the release-please-action documentation and the source.
- **`simple` type creates `version.txt`**: intentional; this is the canonical version file for release-please. The two plugin.json files are secondary extras. No consumer reads `version.txt` today.
- **docs deploy condition after trigger change**: `github.event_name != 'pull_request'` correctly covers `release: [published]` and workflow_dispatch deploys without modification. No change needed to the deploy job beyond the trigger update.
- **GitHub App token action version**: Use `actions/create-github-app-token@v3` (matching jekyll-auto-thumbnails reference).
- **Preflight advisory (applied)**: Changed docs trigger from `push: tags: ['v*']` to `release: types: [published]` — semantically more precise; fires when GitHub release is actually published (not just when tag is pushed).

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight
- [x] Build
- [x] QA
