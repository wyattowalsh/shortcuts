# Design notes: `observability-qa`

## Design stance

Define quality gates, generated evidence, coverage, and CI artifacts.

## Integration points

- `packages/shortcutkit` for CLI behavior when applicable.
- `packages/schemas` for machine-readable validation contracts.
- `apps/docs` for generated documentation and user-facing references.
- `planning/task-graph.yaml` for implementation sequencing.

## Non-goals

- Do not hide platform limitations.
- Do not introduce broad dependencies without explicit acceptance criteria.
- Do not allow generated artifacts to drift silently.
