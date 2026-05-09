# Change proposal: add agent orchestration hardening

## Summary

Implement the capabilities: `dev-experience-agent-orchestration`, `observability-qa`.

## Why

This change advances the `shortcuts` monorepo toward a source-first, reviewable, secure, documented, and agent-friendly OSS platform for Apple Shortcuts and App Intents.

## Scope

- Implement MVP behavior for the listed capabilities.
- Add tests, docs, generated references, and CI hooks where applicable.
- Update task graph handoff notes after completion.

## Out of scope

- Unrelated broad rewrites.
- Runtime behavior not supported by available platform tooling.
- Vendoring incompatible external compiler code.
