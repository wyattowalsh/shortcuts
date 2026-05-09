# Capability: `shortcut-manifest`

## Purpose

Define the typed shortcut manifest contract that powers validation, security review, catalog generation, docs, and release metadata.

## Requirements

### Requirement: Manifest Required

Every shortcut package MUST include a `shortcut.yml` manifest.

#### Scenario: manifest-required

- GIVEN a directory under `shortcuts/` lacks a manifest WHEN validation runs THEN it fails with the missing path.

### Requirement: Strict Identity

A manifest MUST include stable `id`, `name`, `version`, `summary`, `category`, `status`, `license`, and maintainer metadata.

#### Scenario: strict-identity

- GIVEN a manifest has an invalid semver WHEN validation runs THEN the path and field are reported.

### Requirement: Declared Permissions

A manifest MUST declare sensitive permissions and data egress expectations.

#### Scenario: declared-permissions

- GIVEN network access is declared false WHEN source contains an HTTP URL THEN strict audit reports a mismatch.

### Requirement: Compatibility

A manifest MUST record supported platforms, OS versions, device requirements, and Apple Intelligence requirements where relevant.

#### Scenario: compatibility

- GIVEN a shortcut uses Use Model WHEN catalog renders THEN compatibility and AI requirements are visible.

### Requirement: Tests Metadata

A manifest MUST declare static and runtime test metadata when package-specific tests are present.

#### Scenario: tests-metadata

- GIVEN a runtime test requires macOS WHEN Linux CI runs THEN it is skipped with an explanation.
