# Delta: `governance-oss` for `launch-oss-beta`

## ADDED Requirements

### Requirement: Implement Contribution Requirements MVP
Contributed shortcuts MUST include manifest, README, permission declarations, and security notes where relevant.

#### Scenario: mvp-implemented
- GIVEN a PR adds a shortcut without permissions WHEN CI runs THEN it fails.
