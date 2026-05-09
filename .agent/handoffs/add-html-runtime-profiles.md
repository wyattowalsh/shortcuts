# add-html-runtime-profiles

Status: completed 2026-05-09T22:15:28Z

## Scope Completed

- Added OpenSpec change `add-html-runtime-profiles` covering CLI, manifest, security audit, catalog/docs, and release behavior.
- Added `shortcutkit html analyze`, `shortcutkit html bundle`, and `shortcutkit html publish` commands.
- Implemented deterministic HTML runtime analysis, constrained local bundling, and here.now dry-run publish metadata in `packages/shortcutkit/src/shortcutkit/html_runtime.py`.
- Updated `Open HTML` from the invalidated `getFileLink(ShortcutInput)` handoff to the bundled-only `data:text/html;base64,...` flow.
- Added manifest `html_runtime` metadata for `local-bundled` and `hosted` profiles.
- Expanded security scanning to `.html`, `.css`, `.js`, and `.mjs` sources and added reviewed hosted-profile audit metadata.
- Surfaced HTML runtime metadata in catalog JSON, generated docs, and release assets.
- Added fixtures and tests for HTML analysis, bundling, dry-run publish, manifest metadata, security scanning, catalog output, and release metadata.

## Files Changed By Category

- OpenSpec: `openspec/changes/add-html-runtime-profiles/**`.
- CLI/runtime: `packages/shortcutkit/src/shortcutkit/cli.py`, `packages/shortcutkit/src/shortcutkit/html_runtime.py`, `packages/shortcutkit/src/shortcutkit/models.py`.
- Schema/security/catalog/docs/release: `packages/schemas/shortcut-manifest.schema.json`, `packages/shortcutkit/src/shortcutkit/security.py`, `packages/shortcutkit/src/shortcutkit/catalog.py`, `packages/shortcutkit/src/shortcutkit/docs.py`, `packages/shortcutkit/src/shortcutkit/release.py`.
- Shortcut package: `shortcuts/open-html-in-safari/shortcut.yml`, `shortcuts/open-html-in-safari/README.md`, `shortcuts/open-html-in-safari/src/open-html-in-safari.cherri`.
- Tests/fixtures: `packages/shortcutkit/tests/test_cli.py`, `packages/shortcutkit/tests/test_manifest.py`, `packages/shortcutkit/tests/test_security.py`, `packages/shortcutkit/tests/test_catalog.py`, `packages/shortcutkit/tests/test_adapters_runtime_release.py`, `packages/shortcutkit/tests/fixtures/html-supported/**`, `packages/shortcutkit/tests/fixtures/html-external/**`, `packages/shortcutkit/tests/fixtures/html-source-domain/**`.
- Generated outputs: `catalog/catalog.json`, `apps/docs/content/docs/generated/catalog.mdx`.

## Verification

- `rtk npx -y @fission-ai/openspec@latest validate add-html-runtime-profiles --strict` passed.
- `rtk npx -y @fission-ai/openspec@latest validate --all --strict` passed for the repo OpenSpec tree.
- `uv run wagents openspec validate` also exited 0, but its output referenced the broader local `wagents` OpenSpec workspace rather than this repo's visible change list.
- `uv run pytest packages/shortcutkit/tests/test_cli.py packages/shortcutkit/tests/test_manifest.py packages/shortcutkit/tests/test_security.py packages/shortcutkit/tests/test_catalog.py packages/shortcutkit/tests/test_adapters_runtime_release.py` passed: 37 tests.
- `uv run ruff check .` passed.
- `uv run ty check packages/shortcutkit/src` passed.
- `uv run shortcutkit validate shortcuts/open-html-in-safari` passed.
- `uv run shortcutkit lint shortcuts/open-html-in-safari` passed.
- `uv run shortcutkit html analyze packages/shortcutkit/tests/fixtures/html-supported/index.html --json` passed.
- `uv run shortcutkit html publish packages/shortcutkit/tests/fixtures/html-supported --provider here-now --dry-run --json` passed without network publish.
- `uv run shortcutkit security audit --strict` passed.
- `uv run shortcutkit catalog generate` completed and `uv run shortcutkit catalog generate --check` passed.
- `uv run shortcutkit docs generate --docs-root apps/docs` completed and `uv run shortcutkit docs generate --docs-root apps/docs --check` passed.
- `uv run pytest` passed: 38 tests.
- `pnpm build` passed.
- `uv run shortcutkit build shortcuts/open-html-in-safari --json` returned `status: skipped` because the external Cherri adapter was not executed without `--run-external`.
- `uv run shortcutkit validate shortcuts/examples/clean-clipboard` passed.
- `uv run shortcutkit lint shortcuts/examples/clean-clipboard` passed.
- `rtk git diff --check` passed.

## Security And Privacy Impact

- Local bundled profile keeps shortcut runtime network disabled and uses only explicit share-sheet file/text input plus the declared `data` URL scheme.
- Hosted here.now profile is represented as developer-initiated publish metadata, not shortcut runtime network access.
- Real here.now publish remains blocked/gated; `publish --run` returns a blocked result until credentials/API details and explicit data-egress approval are provided.
- Device import, install, signing, app opening, and shortcut execution were not performed.

## Blockers And Follow-Up

- No real here.now publish was performed; user approval and provider API details are still required for live hosted proof.
- No generated `.shortcut` rebuild or device execution was performed; external Cherri compiler and Shortcuts library operations require explicit approval.
- Final device proof remains manual: install/import only after approval, share bundled HTML, confirm Safari opens and executes inlined JavaScript, and separately validate hosted multi-file Safari behavior if publishing is approved.

## Dirty Worktree Notes

- The worktree was dirty before this task started, with many modified and untracked files from prior work. This handoff records only the files intentionally touched for `add-html-runtime-profiles`.
- `shortcuts_codex_jumpstart_prompt_v3.md` was not touched.
