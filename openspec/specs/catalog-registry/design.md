# Design notes: `catalog-registry`

## Design stance

Generate a machine-readable and human-readable catalog from manifests, audits, releases, and docs metadata.

## Integration points

- `packages/shortcutkit` for CLI behavior when applicable.
- `packages/schemas` for machine-readable validation contracts.
- `apps/docs` for generated documentation and user-facing references.
- `planning/task-graph.yaml` for implementation sequencing.

## Non-goals

- Do not hide platform limitations.
- Do not introduce broad dependencies without explicit acceptance criteria.
- Do not allow generated artifacts to drift silently.
