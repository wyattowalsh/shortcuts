# W6 CI Evidence

Linux-equivalent checks passed locally:

- `uv run ruff check .`
- `uv run ty check packages/shortcutkit/src`
- `uv run pytest`
- `uv run shortcutkit catalog generate --check`
- `uv run shortcutkit docs generate --docs-root apps/docs --check`
- `uv run shortcutkit security audit --strict`
- `/Users/ww/Library/pnpm/.tools/pnpm/10.11.0/bin/pnpm lint`
- `pnpm typecheck`
- `pnpm build`

`rtk lint` warning persists as a wrapper issue; direct pinned pnpm lint passed.
