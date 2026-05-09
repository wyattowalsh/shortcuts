# Capability: `observability-qa`

## Purpose

Define quality gates, generated evidence, coverage, and CI artifacts.

## Requirements

### Requirement: Verification Evidence

CI MUST produce machine-readable evidence for validation, audit, catalog, docs, and tests.

#### Scenario: verification-evidence

- GIVEN CI runs WHEN artifacts are uploaded THEN audit/catalog/test outputs are available.

### Requirement: Coverage

Python tests MUST report coverage for core CLI modules when coverage tooling is available in the local environment.

#### Scenario: coverage

- GIVEN pytest runs WHEN coverage is configured THEN coverage XML is produced.

### Requirement: Drift Detection

Generated docs/catalog/schema outputs MUST support `--check` drift detection.

#### Scenario: drift-detection

- GIVEN generated output is stale WHEN check runs THEN CI fails.

### Requirement: Failure Mapping

Failures MUST include rule IDs or task IDs where the failing check can map to a stable identifier.

#### Scenario: failure-mapping

- GIVEN a security audit fails WHEN output is shown THEN rule ID and remediation are present.
