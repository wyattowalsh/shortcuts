# Design: launch oss beta

## Capability mapping

- `governance-oss`
- `release-distribution`
- `observability-qa`

## Implementation principles

- Start with validation and static checks.
- Keep generated outputs reproducible.
- Prefer narrow adapters over monolithic integrations.
- Add docs and tests in the same change where behavior is introduced.
- Preserve path ownership and avoid task-graph drift.

## Verification

- Run relevant `shortcutkit` commands.
- Run language-specific tests.
- Run docs build when docs/content/generated references change.
- Run `openspec validate --all --strict` if OpenSpec CLI is installed.
