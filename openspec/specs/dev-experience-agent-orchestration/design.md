# Design notes: `dev-experience-agent-orchestration`

## Design stance

Coordinate parallel coding agents and human maintainers across a large monorepo build.

## Integration points

- `packages/shortcutkit` for CLI behavior when applicable.
- `packages/schemas` for machine-readable validation contracts.
- `apps/docs` for generated documentation and user-facing references.
- `planning/task-graph.yaml` for implementation sequencing.

## Non-goals

- Do not hide platform limitations.
- Do not introduce broad dependencies without explicit acceptance criteria.
- Do not allow generated artifacts to drift silently.
