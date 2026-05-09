# Delta: `monorepo-foundation` for `bootstrap-monorepo-foundation`

## ADDED Requirements

### Requirement: Implement Workspace Files MVP
The repo MUST include root workspace files for pnpm, Turborepo, uv/Python packaging, editor defaults, and git hygiene.

#### Scenario: mvp-implemented
- GIVEN a fresh clone WHEN dependencies are installed THEN JS and Python workspaces resolve without unrelated warnings.
