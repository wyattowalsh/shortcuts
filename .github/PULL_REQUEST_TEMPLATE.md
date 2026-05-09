## Summary

-

## Verification

- [ ] `uv run ruff check .`
- [ ] `uv run ty check packages/shortcutkit/src`
- [ ] `uv run pytest`
- [ ] `uv run shortcutkit catalog generate --check`
- [ ] `uv run shortcutkit security audit --strict`
- [ ] `pnpm build`

## Security And Provenance

- [ ] Sensitive permissions are declared in `shortcut.yml`.
- [ ] `.shortcut` artifacts are not committed outside `dist/`.
- [ ] Release artifacts include checksums when applicable.
