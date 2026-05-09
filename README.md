# shortcuts

`shortcuts` is an OSS monorepo for developer-grade Apple Shortcuts, Siri/App Shortcuts, and App Intents development.

The wedge is simple: source-controlled, reviewable Apple Shortcuts. A shortcut package is not a loose exported `.shortcut` file; it is a manifest-centered project with source, docs, validation, security review, catalog metadata, tests where feasible, and release provenance.

## What This Repo Provides

- `shortcut.yml` manifests as the contract for validation, docs, security review, catalog generation, tests, and releases.
- `shortcutkit`, a Python CLI for manifest validation, linting, security audit, catalog generation, adapter checks, docs generation, and release helpers.
- JSON Schemas under `packages/schemas` for non-Python consumers.
- ActionDB seed data for known risky capabilities and detector metadata.
- Example shortcut packages under `shortcuts/examples/**`.
- App Intents examples and snippets under `app-intents/**`.
- A Fumadocs/Next.js docs site under `apps/docs` with Tailwind CSS v4, shadcn/ui-compatible styling, Orama search, and LLM routes.

## Quick Start

```bash
uv sync --all-packages
uv run shortcutkit --version
uv run shortcutkit validate shortcuts/examples/clean-clipboard
uv run shortcutkit lint shortcuts/examples/clean-clipboard
uv run shortcutkit security audit --strict
uv run shortcutkit catalog generate --check
uv run shortcutkit adapter check --json
uv run shortcutkit release metadata shortcuts/examples/clean-clipboard
```

For docs:

```bash
pnpm install --frozen-lockfile
pnpm --filter @shortcuts/docs build
```

## Shortcut Package Contract

Every shortcut package must include `shortcut.yml`.

```txt
shortcuts/examples/clean-clipboard/
  shortcut.yml
  README.md
  src/
  tests/
  dist/        # generated/release artifacts only
```

`.shortcut` files are generated release artifacts or fixtures, not canonical source.

## Security Language

This project does not claim shortcuts are absolutely safe. It reports declared permissions, detected capabilities, review status, provenance, and unknowns so maintainers and users can make informed decisions.

## Repository Status

This repo now includes the beta-oriented vertical slice: schemas, `shortcutkit`, ActionDB-backed audit, generated catalog/docs, adapter/runtime gates, release metadata helpers, App Intents snippets, and launch workflows. External shortcut compilers, macOS runtime execution, signing, and artifact distribution remain explicit opt-in surfaces.
