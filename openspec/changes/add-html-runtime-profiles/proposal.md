# Change proposal: add HTML runtime profiles

## Summary

Add explicit HTML runtime profiles for `Open HTML`: a hosted Safari profile for multi-file sites via here.now, and a constrained local bundled profile for single-file HTML opened from Shortcuts.

## Why

Device testing showed that pure Shortcuts file-link handoff is not reliable for local multi-file HTML in Safari: `Get Link to File` requires the file to already be uploaded to iCloud, picker-based flows can hang, and `data:` URLs do not provide a filesystem base for sibling assets. The repo needs a truthful, testable runtime contract that distinguishes real Safari multi-file hosting from offline bundled HTML.

## Scope

- Add `shortcutkit html analyze`, `shortcutkit html bundle`, and dry-run/opt-in here.now publish behavior.
- Extend shortcut manifests with HTML runtime profile metadata.
- Update security audit, catalog/docs rendering, and release metadata to surface HTML runtime risks and generated assets.
- Reset `shortcuts/open-html-in-safari` from file-link handoff to the bundled-only `data:` URL contract.
- Add tests and fixtures for analyzer, bundler, manifest, security, catalog, and release behavior.

## Out of scope

- Importing, installing, signing, or running shortcuts in the user's Shortcuts library.
- Performing a real here.now publish without an explicit `--run` opt-in and user approval.
- Promising arbitrary local multi-file Safari support from a pure Shortcut.
- Vendoring Cherri, Jelly, or non-permissive compiler code.
