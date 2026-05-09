# Capability: `shortcutkit-cli`

## Purpose

Provide the Python CLI for validation, linting, catalog generation, security audit, adapters, tests, docs generation, and releases.

## Requirements

### Requirement: Entrypoint
The system MUST expose `shortcutkit` and MAY expose `sk` as an alias.

#### Scenario: entrypoint
- GIVEN the package is installed WHEN `shortcutkit --version` runs THEN it prints the version.

### Requirement: Validation Command
`shortcutkit validate` MUST validate manifests using Pydantic and JSON Schema.

#### Scenario: validation-command
- GIVEN invalid YAML WHEN validation runs THEN a clear parse error is emitted.

### Requirement: Lint Command
`shortcutkit lint` MUST check repo structure, README presence, generated artifact hygiene, and manifest/doc consistency.

#### Scenario: lint-command
- GIVEN a shortcut package lacks README WHEN lint runs THEN it reports the missing file.

### Requirement: Catalog Command
`shortcutkit catalog generate --check` MUST detect catalog drift.

#### Scenario: catalog-command
- GIVEN a manifest changes without regenerating catalog WHEN check runs THEN it fails.

### Requirement: Security Command
`shortcutkit security audit --strict --json` MUST output structured audit results.

#### Scenario: security-command
- GIVEN a mismatch is found WHEN JSON output is requested THEN severity, rule ID, path, and remediation are emitted.

### Requirement: Adapter Commands
`shortcutkit build` and `shortcutkit test` MUST dispatch through capability-aware adapters.

#### Scenario: adapter-commands
- GIVEN a missing external adapter WHEN build runs THEN it emits an actionable installation message.
