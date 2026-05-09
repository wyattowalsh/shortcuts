# Delta: `security-audit` for `add-security-actiondb-audit`

## ADDED Requirements

### Requirement: Implement Permission Mismatch MVP
The audit MUST compare detected evidence against declared permissions.

#### Scenario: mvp-implemented
- GIVEN detected network access is undeclared WHEN strict audit runs THEN it fails.
