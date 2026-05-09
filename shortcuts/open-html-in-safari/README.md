# Open HTML

Open HTML is a source-first Apple Shortcut package for iOS and iPadOS. The canonical source is `src/open-html-in-safari.cherri`; generated `.shortcut` artifacts belong under `dist/` only.

The package icon is `icon.png`. It is used by the catalog, generated docs, and release metadata. Cherri 2.2.0 only supports built-in Shortcuts color and glyph icons, so the compiled shortcut uses a purple magic wand glyph as the most expressive in-shortcut fallback.

The shortcut appears in the share sheet for files. For local/offline use, share a bundled single-file HTML document into it. The shortcut shows a progress notification, reads the shared HTML text, base64-encodes it, and opens a `data:text/html;base64,...` URL in Safari.

Safari is the required runtime surface because Quick Look can preview HTML but does not reliably run page JavaScript. A `data:` URL has no filesystem base, so relative sibling assets will not load. Use `uv run shortcutkit html bundle path/to/index.html --output path/to/index.bundled.html --json` to inline supported local CSS and JavaScript before sharing the bundled file.

For real multi-file HTML apps in Safari, use the hosted profile instead: `uv run shortcutkit html publish path/to/site --provider here-now --dry-run --json` previews a here.now static publish without network egress. Any real publish is developer-initiated data egress and requires explicit approval.

The shortcut itself does not read or write the clipboard, call Shortcuts network actions, invoke AI/model actions, or run shell commands. It declares file-read access for the explicit share-sheet input and the `data:` URL scheme used to hand the bundled page to Safari. Only use bundled or hosted HTML that you trust.

## Manual Verification

1. Install the external Cherri compiler separately if you choose to compile this package.
2. Compile `src/open-html-in-safari.cherri` outside of automated gates.
3. Import the generated shortcut into Apple Shortcuts on iOS or iPadOS.
4. Build a constrained local bundle with `uv run shortcutkit html bundle path/to/index.html --output path/to/index.bundled.html --json`.
5. In Files, share the bundled `.html` file to Open HTML and confirm the starting progress notification appears.
6. Confirm Safari opens a `data:text/html;base64,...` page.
7. Confirm JavaScript inlined into the bundled HTML runs in Safari.
8. Confirm the shortcut does not stop in Quick Look and does not show an Open In picker.
9. For multi-file HTML, dry-run a here.now publish and perform any real publish only after explicit approval.
10. Run the shortcut without share-sheet input and confirm it stops with the no-input message.
11. Inspect the shortcut action list and confirm it only reads shared HTML text, encodes it, and opens a data URL in Safari.

Do not run external compiler, import, signing, opening, or installation flows without explicit maintainer opt-in.
