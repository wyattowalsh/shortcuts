# Contributing

Contributions should improve the source-first Shortcuts engineering workflow.

## Shortcut Contributions

Every shortcut package must include:

- `shortcut.yml`;
- `README.md`;
- declared permissions;
- source files or artifact provenance;
- security notes for sensitive capabilities;
- tests where feasible.

Do not submit `.shortcut` files as the only source of truth. Generated artifacts belong in `dist/` with checksums and provenance metadata.

## Local Checks

```bash
uv sync --all-packages
uv run ruff check .
uv run ty check packages/shortcutkit/src
uv run pytest
uv run shortcutkit validate shortcuts/examples/clean-clipboard
uv run shortcutkit catalog generate --check
uv run shortcutkit security audit --strict
uv run shortcutkit docs generate --docs-root apps/docs --check
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm --filter @shortcuts/docs build
```

## Review Tiers

Network, AI/model, URL scheme, artifact provenance, and shell-execution changes must include audit output in the pull request. Shell execution, unknown high-risk audit findings, and release/signing changes require two maintainer reviews.

If a platform-specific or networked check cannot run, document the exact blocker in the pull request.
