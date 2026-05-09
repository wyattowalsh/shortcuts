# Design notes: fumadocs-site

## Status

Planned.

## Design intent

This capability is designed to be implemented in small, testable increments. The corresponding task graph entries are in `planning/task-graph.yaml`.

## Interfaces

- OpenSpec requirements: `openspec/specs/fumadocs-site/spec.md`
- Change proposals: `openspec/changes/**/specs/fumadocs-site/spec.md`
- Implementation paths: see `planning/task-graph.yaml`

## Non-goals

- Avoid relying on undocumented Apple internals for critical guarantees.
- Avoid bundling incompatible third-party compiler code into the permissive core.
- Avoid turning the repository into an unreviewed shortcut dump.
