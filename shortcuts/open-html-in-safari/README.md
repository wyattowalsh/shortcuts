# Open HTML

Open HTML is a source-first Apple Shortcut package for iOS and iPadOS. The canonical source is `src/open-html-in-safari.cherri`; generated `.shortcut` artifacts belong under `dist/` only.

The package icon is `icon.png`. It is used by the catalog, generated docs, and release metadata. Cherri 2.2.0 only supports built-in Shortcuts color and glyph icons, so the compiled shortcut uses a purple magic wand glyph as the most expressive in-shortcut fallback.

## Supported Input Types

The shortcut appears in the share sheet for file, rich text, text, and URL handoffs because iOS Files can present an HTML document through more than one content representation. It handles three primary input types:

1. **Single HTML file** — The shortcut asks you to choose `Single HTML file`, resolves the shared input as renderable HTML text without file metadata lookup, base64-encodes that render text, and opens it in Safari as `data:text/html;base64,...`.
2. **ZIP archive** — The shortcut extracts the archive, finds `index.html` or another HTML file, attempts a best-effort local bundle, and opens the generated bundled HTML in Safari.
3. **Folder** — The shortcut scans the folder recursively, finds `index.html` or another HTML file, attempts a best-effort local bundle, and opens the generated bundled HTML in Safari.

## Primary Path: Local Safari Rendering

Safari is the first runtime surface because Quick Look can preview HTML but does not reliably run page JavaScript or CSS. A `data:` URL has no filesystem base, so raw relative sibling assets will not load.

For ZIP and folder inputs, Open HTML now attempts a constrained on-device bundle before Safari opens. It reads the selected HTML file, finds supported local asset files from the shared input, rewrites matching file-name references to `data:` URLs, base64-encodes the generated HTML, and opens that bundled result in Safari.

| Input | Local render | Share URL offer |
| --- | --- | --- |
| Single `.html` file | User-selected resolved-text `data:` URL path | Shown after Safari returns |
| ZIP archive | Extract, choose HTML, best-effort asset rewrite | Shown after Safari returns |
| Folder | Recursive scan, choose HTML, best-effort asset rewrite | Shown after Safari returns |

This is intentionally best-effort. It handles straightforward same-name references to CSS, JavaScript, images, fonts, JSON, and web manifests. It is not a replacement for the deterministic repo bundler, which understands nested paths, CSS `url()` dependencies, `@import`, and `srcset`.

For reliable local rendering, bundle first:

```bash
uv run shortcutkit html bundle path/to/index.html --output path/to/index.bundled.html --json
```

This inlines local CSS, JavaScript, images, fonts, manifests, CSS `url()` dependencies, and `srcset` into a single self-contained `.html` file. The resulting file opens reliably in Safari via the `data:` URL scheme.

For single HTML files, the shortcut uses `getText(ShortcutInput)` before Base64 encoding so iOS resolves the shared Files item into renderable HTML content before Safari opens. This is optimized for normal UTF-8 HTML documents, which covers the bundled examples and most hand-authored single-file pages. For unusual legacy encodings or very large files, use the deterministic CLI bundler first.

After launch, the shortcut shows the Shortcuts-reported input type and asks what you shared: `Single HTML file`, `ZIP archive`, or `Folder`. Choosing `Single HTML file` avoids file metadata lookup entirely and reads the shared input as text. ZIP and folder choices still use file actions because they need archive extraction or folder traversal. After the read succeeds, the shortcut shows render text length and the expected `data:text/html;base64,...` target.

The first action is a launch canary: `Open HTML launched from the share sheet.` If that does not appear after tapping the share-sheet button, iOS did not run this installed shortcut artifact.

## here.now Share URL Deployment

After the local Safari render attempt, Open HTML always shows the here.now deployment command for a shareable hosted URL. For multi-file apps that cannot be bundled into a single file, are too large for `data:` URL rendering, or need to be shared with someone else, use the hosted profile:

```bash
# Preview without network egress
uv run shortcutkit html publish path/to/site --provider here-now --dry-run --json

# Real publish; returns a shareable siteUrl
uv run shortcutkit html publish path/to/site --provider here-now --run --json
```

Anonymous here.now publishes create public share URLs that expire after 24 hours. Publishing with an API key can create permanent sites and higher limits. The shortcut itself does not upload files; the explicit `shortcutkit html publish` command performs the deployment and reports the returned `siteUrl`.

The JSON output includes the deployment status, `site_url`, publishable file list, SHA-256 hashes, fingerprint, and expiration metadata when available.

## Examples

The examples are organized by share-sheet input type under `examples/`:

| Folder | Use from iPhone | What it proves |
| --- | --- | --- |
| `examples/single-file/` | Share one `.html` file into `Open HTML` | Inline CSS/JavaScript runs through the resolved-text `data:` URL path |
| `examples/directories/` | Share a folder such as `flat-app/` or `mini-gallery/` | The shortcut finds `index.html`, rewrites supported local assets, and renders the generated bundle |
| `examples/zips/` | Share `flat-app.zip` or `mini-gallery.zip` | Archive extraction, HTML selection, local bundle attempt, and Safari rendering |

Start with `examples/single-file/01-inline-counter.html`, then test
`examples/directories/flat-app/`, then `examples/zips/flat-app.zip`.

### Testing On iPhone

1. Install or import the rebuilt `Open HTML.shortcut` on the iPhone.
2. Put `examples/single-file/01-inline-counter.html` in iCloud Drive, AirDrop it, or otherwise make it visible in the iOS Files app.
3. In Files, long-press the HTML file, choose Share, then choose `Open HTML`.
4. Confirm the launch canary appears, then tap OK.
5. In the input-kind picker, choose `Single HTML file`.
6. Confirm the preflight screen reports `Detected mode: single-file`.
7. Confirm Safari opens a `data:text/html;base64,...` page.
8. Confirm the counter page renders and its button increments.
9. Return to Shortcuts and confirm the here.now dry-run and publish commands are shown.
10. Repeat with `examples/directories/flat-app/`, `examples/zips/flat-app.zip`, and the gallery fixtures, choosing the matching input kind each time.

## Quick Look and Open In Backups

If Safari renders poorly, return to Shortcuts. Open HTML offers two backup methods:

1. **Quick Look** — Preview the original shared file
2. **Open In** — Native iOS file handoff picker

These backups are intentionally file-based because they preserve the original file.

## Security

- The shortcut does not read or write the clipboard
- No AI/model actions or shell commands
- File-read access is only for the explicit share-sheet input
- The `data:` URL scheme is used to hand the page to Safari
- here.now publish requires an explicit `shortcutkit html publish --run` command
- The API key is loaded from `HERENOW_API_KEY` env or `~/.herenow/credentials` — never hardcoded

## Manual Verification

1. Install the external Cherri compiler separately if you choose to compile this package.
2. Compile `src/open-html-in-safari.cherri` outside of automated gates.
3. Import the generated shortcut into Apple Shortcuts on iOS or iPadOS.
4. Build a constrained local bundle with `uv run shortcutkit html bundle shortcuts/open-html-in-safari/examples/directories/flat-app/index.html --output /tmp/flat-app.bundled.html --json`.
5. In Files, share `examples/single-file/01-inline-counter.html` or `/tmp/flat-app.bundled.html` to Open HTML and confirm the starting progress notification appears.
6. Confirm Safari opens a `data:text/html;base64,...` page.
7. Confirm UTF-8 text, CSS, and JavaScript inlined into the bundled HTML all render correctly in Safari.
8. Test with `examples/zips/flat-app.zip` and `examples/zips/mini-gallery.zip`. Confirm extraction, the local bundled render notification, and Safari rendering.
9. Test with `examples/directories/flat-app/` and `examples/directories/mini-gallery/`. Confirm recursive scanning, the local bundled render notification, and Safari rendering.
10. Return to Shortcuts and confirm the here.now deployment command is shown after the local Safari attempt.
11. Run `uv run shortcutkit html publish path/to/site --provider here-now --dry-run --json` and verify it lists only intended publishable files.
12. Perform any real hosted publish with `--run` only after explicit approval, then confirm the command returns a shareable `siteUrl`.
13. Return to Shortcuts, accept the Quick Look backup prompt, and confirm the original shared file previews.
14. Accept the Open In backup prompt and confirm iOS offers the native file handoff picker.
15. Run the shortcut without share-sheet input and confirm it stops with the no-input message.
16. Confirm the shortcut only reads shared files, attempts local bundled rendering, encodes the render result, opens a data URL in Safari, and offers Quick Look/Open In backups.

Do not run external compiler, import, signing, opening, or installation flows without explicit maintainer opt-in.
