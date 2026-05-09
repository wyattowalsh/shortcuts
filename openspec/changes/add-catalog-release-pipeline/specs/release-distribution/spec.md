# Delta: `release-distribution` for `add-catalog-release-pipeline`

## ADDED Requirements

### Requirement: Implement Release Metadata MVP
Every shortcut release MUST include release metadata with checksums, manifest snapshot, audit result, and source commit.

#### Scenario: mvp-implemented
- GIVEN release notes are generated WHEN artifact exists THEN SHA-256 is included.
