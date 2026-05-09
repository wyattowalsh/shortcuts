# Design: add HTML runtime profiles

## Runtime profiles

`hosted` is the reliable Safari profile for multi-file HTML. `shortcutkit html publish --provider here-now --dry-run --json` reports the files and endpoints that would be used without network egress; `--run` is the only path that may contact here.now and must redact sensitive claim URLs from persisted outputs.

`local-bundled` is the offline/private profile. It accepts a single HTML entrypoint, inlines supported local CSS and JavaScript, rejects unsupported or high-risk patterns, and emits a `.bundled.html` file intended for the shortcut's `data:text/html;base64,...` flow.

## CLI behavior

HTML commands live under a Typer subapp named `html` to keep runtime tooling separate from shortcut package validation. JSON output is deterministic and uses stable status values so docs, tests, and downstream agents can reason about profile suitability.

## Manifest and docs behavior

The manifest gains optional `html_runtime` metadata. Catalog, docs, and release metadata surface runtime profiles, entrypoints, generated bundle assets, unsupported-pattern diagnostics, and the distinction between hosted multi-file support and local bundled support.

## Security behavior

Security scanning expands source suffixes to include `.html`, `.css`, `.js`, and `.mjs`. Audits compare detected domains and URL schemes in these files with declared permissions, and flag here.now hosting as intentional network/data-egress metadata rather than hidden shortcut runtime behavior.

## Verification

- `uv run wagents openspec validate`
- `uv run shortcutkit html analyze <fixture> --json`
- `uv run shortcutkit html bundle <fixture> --output <tmp> --json`
- `uv run pytest packages/shortcutkit/tests/test_cli.py packages/shortcutkit/tests/test_manifest.py packages/shortcutkit/tests/test_security.py packages/shortcutkit/tests/test_catalog.py packages/shortcutkit/tests/test_adapters_runtime_release.py`
- `uv run shortcutkit validate shortcuts/open-html-in-safari`
- `uv run shortcutkit lint shortcuts/open-html-in-safari`
- `uv run shortcutkit security audit --strict`
- `uv run shortcutkit catalog generate --check`
- `uv run shortcutkit docs generate --docs-root apps/docs --check`
