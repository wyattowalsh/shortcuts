# Open HTML Examples

These fixtures are organized by the way you share them into the `Open HTML`
shortcut from iOS Files. Start with the smallest single-file fixture so any
failure isolates the direct HTML render path before testing folders or ZIPs.

## iPhone Test Matrix

| Input | File or folder to share | Expected shortcut screen | Expected Safari result | After returning to Shortcuts |
| --- | --- | --- | --- | --- |
| Single file | `single-file/01-inline-counter.html` | Blocking preflight confirmation shows `single-file`, the input name, and zero scanned local files before HTML is read | Counter page renders and the button increments | here.now dry-run and publish commands appear, then Quick Look/Open In backups are offered |
| Single file | `single-file/02-data-card.html` | Blocking preflight confirmation shows `single-file` and `02-data-card.html` before HTML is read | Inline CSS and SVG render as a compact data card | Same here.now and backup prompts |
| Single file | `single-file/03-form-state.html` | Blocking preflight confirmation shows `single-file` and `03-form-state.html` before HTML is read | Form text updates without external assets | Same here.now and backup prompts |
| Directory | `directories/flat-app/` | Blocking preflight confirmation shows `folder`, `index.html`, and scanned local files | CSS, JavaScript, manifest, and SVG references render from rewritten `data:` URLs when supported | Same here.now and backup prompts |
| Directory | `directories/mini-gallery/` | Blocking preflight confirmation shows `folder`, `index.html`, and scanned local files | Gallery styling, script, and SVG images render when supported | Same here.now and backup prompts |
| ZIP archive | `zips/flat-app.zip` | Blocking preflight confirmation shows `zip`, `index.html`, and scanned extracted files | ZIP is extracted, bundled locally, and opened in Safari | Same here.now and backup prompts |
| ZIP archive | `zips/mini-gallery.zip` | Blocking preflight confirmation shows `zip`, `index.html`, and scanned extracted files | ZIP gallery renders through the local bundle attempt | Same here.now and backup prompts |

## Phone Steps

1. Install or import the rebuilt `Open HTML.shortcut` on the iPhone.
2. Put the example files in iCloud Drive, AirDrop them, or otherwise make them visible in the iOS Files app.
3. In Files, long-press the fixture, choose Share, then choose `Open HTML`.
4. Confirm the launch canary appears: `Open HTML launched from the share sheet.`
5. Confirm the pre-read confirmation appears and the detected mode matches the fixture type.
6. Tap through to Safari and confirm it opens a `data:text/html;base64,...` page.
7. Return to Shortcuts after the Safari check.
8. Confirm the here.now dry-run and publish commands are shown.
9. Use Quick Look or Open In only if Safari rendered poorly.

## Fixture Notes

- `single-file/01-inline-counter.html`: inline CSS and JavaScript, no external assets.
- `single-file/02-data-card.html`: a visually richer single document with inline SVG.
- `single-file/03-form-state.html`: a small form that proves JavaScript state updates run.
- `directories/flat-app/`: small app with `index.html`, CSS, JavaScript, manifest, and logo.
- `directories/mini-gallery/`: image gallery with CSS, JavaScript, and SVG image files.
- `zips/flat-app.zip`: ZIP version of `directories/flat-app/`.
- `zips/mini-gallery.zip`: ZIP version of `directories/mini-gallery/`.

## Hosted URL Dry Run

From the repository root, preview what would publish to here.now without network
upload:

```bash
uv run shortcutkit html publish shortcuts/open-html-in-safari/examples/directories/flat-app --provider here-now --dry-run --json
```

Run the same command with `--run` only when you intend to upload and create a
shareable URL.
