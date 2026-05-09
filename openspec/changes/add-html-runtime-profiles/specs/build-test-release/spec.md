# Delta: `build-test-release` for `add-html-runtime-profiles`

## ADDED Requirements

### Requirement: Release HTML Runtime Assets

Release metadata MUST include generated HTML bundle assets and checksums when they are part of the runtime contract.

#### Scenario: release-records-bundled-html-asset

- GIVEN a package has a generated `.bundled.html` runtime asset WHEN release metadata is generated THEN the asset path, size, and SHA-256 digest are included.

### Requirement: Device Verification Boundaries

Release and test metadata MUST keep device execution, shortcut import, and real hosted publish verification as explicit manual gates.

#### Scenario: manual-device-proof-required

- GIVEN Open HTML cannot be device-tested in headless CI WHEN validation runs THEN `tests.manual` records the required device checks and blocked external operations.
