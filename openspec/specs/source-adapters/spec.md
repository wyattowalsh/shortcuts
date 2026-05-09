# Capability: `source-adapters`

## Purpose

Integrate source languages and artifact modes without overpromising universal build/decompile support.

## Requirements

### Requirement: Capability Matrix

Each adapter MUST declare build, export, inspect, test, and license capabilities.

#### Scenario: capability-matrix

- GIVEN adapters are listed WHEN docs are generated THEN capabilities are visible.

### Requirement: External Process Boundary

Cherri and Jelly integrations MUST call external binaries and MUST NOT vendor incompatible compiler code into core packages.

#### Scenario: external-process-boundary

- GIVEN the repo is packaged WHEN license checks run THEN GPL/non-commercial compiler code is absent from core.

### Requirement: Manual Mode

Manual source mode MUST be first-class and documented.

#### Scenario: manual-mode

- GIVEN a manifest uses `source.mode: manual` WHEN build runs THEN it reports manual build instructions instead of failing unclearly.

### Requirement: Build Metadata

Builds MUST record adapter version, command, environment, and source hash when that information is available.

#### Scenario: build-metadata

- GIVEN a shortcut is built WHEN release metadata is generated THEN adapter metadata is included.
