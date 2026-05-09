# AGENTS.md

## Setup Commands

```bash
pnpm install --frozen-lockfile
uv sync --all-packages
```

## Core Verification

```bash
uv run ruff check .
uv run ty check packages/shortcutkit/src
uv run pytest
uv run shortcutkit validate shortcuts/examples/clean-clipboard
uv run shortcutkit lint shortcuts/examples/clean-clipboard
uv run shortcutkit catalog generate --check
uv run shortcutkit security audit --strict
uv run shortcutkit docs generate --docs-root apps/docs --check
pnpm build
```

## Code Style

- Python target is 3.13.
- Use `uv` for Python package and command execution.
- Use Pydantic v2, Typer, Rich, and pytest for `shortcutkit`.
- Use `pnpm` for JavaScript and TypeScript work.
- Use Next.js App Router, Fumadocs, Tailwind CSS v4, and shadcn/ui-compatible tokens in `apps/docs`.
- Keep adapters capability-based and external-process based.
- Do not treat `.shortcut` artifacts as source.
- Do not vendor GPL or non-commercial compiler code into permissive core packages.

## Agent Workflow

- Claim tasks in `.agent/claims` before editing.
- Write `.agent/handoffs/<task-id>.md` before finishing.
- Do not edit shared files without noting why in the claim or handoff.
- Keep internal planning, audit, and handoff files out of public docs and LLM routes.
