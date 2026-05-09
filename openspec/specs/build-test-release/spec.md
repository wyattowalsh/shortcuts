# Capability: Build, Test, and Release

## Purpose

Define reproducible build, validation, test, and release workflows for shortcuts and tools.

## Requirements

### Requirement: Static Validation
Static validation MUST run on Linux CI for every pull request.

#### Scenario: PR opened
- GIVEN a pull request modifies manifests
- WHEN CI runs
- THEN schema validation, linting, and catalog drift checks execute on Linux

### Requirement: Optional macOS Runtime Tests
Runtime Shortcuts tests MUST be isolated to macOS runners and marked optional or required per package.

#### Scenario: Runtime-compatible shortcut
- GIVEN a shortcut declares headless runtime tests
- WHEN macOS CI is available
- THEN the runtime harness invokes the shortcut and asserts outputs

### Requirement: Manual Verification
Shortcuts that cannot be tested headlessly MUST include manual verification steps.

#### Scenario: UI prompt shortcut
- GIVEN a shortcut requires interactive user prompts
- WHEN validation runs
- THEN it must include `tests.manual` checklist entries

### Requirement: Release Notes
Release automation MUST generate release notes with permissions, compatibility, checksums, install steps, and changelog.

#### Scenario: Release requested
- GIVEN a maintainer tags `shortcut/<id>/v1.0.0`
- WHEN release workflow runs
- THEN release notes are generated from manifest and audit data

### Requirement: Artifact Checksums
Every release artifact MUST have a SHA-256 checksum.

#### Scenario: Artifact produced
- GIVEN `dist/foo.shortcut` exists
- WHEN release packaging runs
- THEN `dist/foo.shortcut.sha256` is produced
