# Delta: `runtime-test-harness` for `add-source-adapters-runtime-tests`

## ADDED Requirements

### Requirement: Implement Optional macOS Runtime MVP
Runtime tests MUST be optional and MUST NOT block Linux-only contributors by default.

#### Scenario: mvp-implemented
- GIVEN Linux CI runs WHEN runtime tests are configured THEN macOS-only cases are skipped.
