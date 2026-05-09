# Capability: `catalog-registry`

## Purpose

Generate a machine-readable and human-readable catalog from manifests, audits, releases, and docs metadata.

## Requirements

### Requirement: Catalog JSON

The system MUST generate `catalog/catalog.json` from valid manifests.

#### Scenario: catalog-json

- GIVEN two valid manifests WHEN catalog generation runs THEN both appear with normalized IDs.

### Requirement: Catalog Lockfile

The system MUST keep catalog output deterministic and MUST introduce `catalog/catalog.lock.json` if generated snapshots require additional lockfile state.

#### Scenario: catalog-lockfile

- GIVEN catalog is regenerated twice without changes THEN lockfile content is stable.

### Requirement: Permission Badges

Catalog entries MUST include permission/risk badges.

#### Scenario: permission-badges

- GIVEN a networked shortcut WHEN catalog renders THEN the network badge is visible.

### Requirement: Docs Data

Catalog generation MUST produce docs data for Fumadocs pages.

#### Scenario: docs-data

- GIVEN catalog generation runs WHEN docs build runs THEN generated catalog pages resolve.
