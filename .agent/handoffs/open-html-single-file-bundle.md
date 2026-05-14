# Handoff: Open HTML Single-File Render Fix

**Task ID:** open-html-single-file-bundle
**Agent:** codex
**Branch:** main, with pre-existing dirty worktree preserved
**Claim:** `.agent/claims/open-html-single-file-bundle.json`
**Updated:** 2026-05-14T09:46:47Z

## Summary

Fixed the on-device single-file failure path where sharing `examples/single-file/01-inline-counter.html` completed with a checkmark but did not visibly open Safari.

The shortcut no longer Base64-encodes the shared file object directly for single HTML inputs. It now accepts file, rich text, text, and URL share-sheet representations, shows a blocking launch canary before any `ShortcutInput` metadata access, shows a blocking pre-read confirmation before attempting to read HTML text, resolves every supported input type to local render HTML text, shows ready metadata after the read succeeds, Base64-encodes the render text, and opens Safari with `data:text/html;base64,...`.

## Changes

- `src/open-html-in-safari.cherri`
  - Detects `.html` / `.htm` from lowercase extension and filename before folder fallback.
  - Widens share-sheet input classes to `file, richtext, text, url` because iOS Files can expose HTML through richer representations.
  - Adds a first-action launch canary before any input metadata lookup.
  - Uses `getText(@targetFile)` for single files, ZIP-selected HTML, and folder-selected HTML.
  - Removes the direct `base64Encode(@targetFile)` single-file path.
  - Adds a pre-read `confirm(...)` prompt with input name, detected mode, entry HTML, local bundling status, and scanned file count.
  - Keeps the ready `show(...)` screen after HTML text is resolved, including render text character count and Safari target scheme.
  - Keeps the here.now command display after returning from Safari.
  - Keeps Quick Look and Open In backups behind confirmations.
- `shortcut.yml`, package README, generated catalog/docs
  - Updated single-file runtime metadata from direct-byte rendering to resolved-text rendering.
  - Documented the UTF-8/normal HTML assumption and deterministic CLI bundler fallback.
  - Added phone test expectations for the pre-read confirmation, ready screen, Safari data URL, here.now prompt, and backups.
- `examples/README.md`
  - Reworked into an iPhone test matrix for single files, directories, and ZIP archives.
- `packages/shortcutkit/tests/test_security.py`
  - Updated focused source assertions to require `base64Encode(@renderHtml)` and reject `base64Encode(@targetFile)`.
- `dist/Open HTML.shortcut.sha256`
  - Updated to match the rebuilt external Cherri artifact.

## Verification

- `uv run shortcutkit validate shortcuts/open-html-in-safari` passed.
- `uv run shortcutkit lint shortcuts/open-html-in-safari` passed.
- `uv run shortcutkit security audit shortcuts/open-html-in-safari --strict` passed with expected file-read and `data` URL-scheme review findings.
- `uv run pytest packages/shortcutkit/tests/test_security.py -k open_html` passed: 3 passed, 7 deselected.
- `uv run shortcutkit build shortcuts/open-html-in-safari --json` passed as a dry adapter resolution.
- `uv run shortcutkit build shortcuts/open-html-in-safari --run-external --json` rebuilt `dist/Open HTML.shortcut` successfully.
- `shasum -a 256 -c shortcuts/open-html-in-safari/dist/Open\ HTML.shortcut.sha256` passed.
- `uv run shortcutkit catalog generate --check` passed after regenerating `catalog/catalog.json`.
- `uv run shortcutkit docs generate --docs-root docs --check` passed after regenerating `docs/content/docs/generated/catalog.mdx`.
- `pnpm build` passed for the Fumadocs/Next docs site.
- `git diff --check` passed.

## Remaining Manual Device Proof

Install or import the rebuilt `Open HTML.shortcut` on the iPhone, then share `examples/single-file/01-inline-counter.html` from Files into Open HTML.

Expected result:

1. The launch canary appears immediately after tapping Open HTML from the share sheet.
2. The blocking pre-read confirmation appears and reports `single-file`.
3. The ready screen appears after the file is read.
4. Safari opens a `data:text/html;base64,...` page.
5. The counter page renders and the button increments.
6. Returning to Shortcuts shows the here.now commands and backup prompts.

Then repeat with `examples/directories/flat-app/` and `examples/zips/flat-app.zip`.
