# Design notes: app-intents

## Status

Planned.

## Design intent

This capability is designed to be implemented in small, testable increments. The corresponding task graph entries are in `planning/task-graph.yaml`.

## Interfaces

- OpenSpec requirements: `openspec/specs/app-intents/spec.md`
- Change proposals: `openspec/changes/**/specs/app-intents/spec.md`
- Implementation paths: see `planning/task-graph.yaml`

## Non-goals

- Avoid relying on undocumented Apple internals for critical guarantees.
- Avoid bundling incompatible third-party compiler code into the permissive core.
- Avoid turning the repository into an unreviewed shortcut dump.
