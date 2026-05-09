# Capability: `monorepo-foundation`

## Purpose

Define root workspace, package managers, governance files, CI skeleton, and repository conventions.

## Requirements

### Requirement: Workspace Files
The repo MUST include root workspace files for pnpm, Turborepo, uv/Python packaging, editor defaults, and git hygiene.

#### Scenario: workspace-files
- GIVEN a fresh clone WHEN dependencies are installed THEN JS and Python workspaces resolve without unrelated warnings.

### Requirement: Governance Files
The repo MUST include OSS governance and contribution files before accepting shortcut submissions.

#### Scenario: governance-files
- GIVEN a contributor opens the repo WHEN they inspect the root THEN license, security, contributing, code of conduct, and maintainers docs are present.

### Requirement: Path Ownership
The repo MUST define path ownership for parallel teams and agents.

#### Scenario: path-ownership
- GIVEN two agents claim tasks WHEN their path globs overlap THEN the claim system marks a conflict.

### Requirement: Baseline CI
The repo MUST run baseline static checks on pull requests.

#### Scenario: baseline-ci
- GIVEN a PR WHEN CI runs THEN workspace, schemas, Python tests, docs checks, and security checks are invoked or explicitly skipped.
