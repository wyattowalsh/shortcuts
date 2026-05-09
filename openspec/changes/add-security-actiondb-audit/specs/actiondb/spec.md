# Delta: `actiondb` for `add-security-actiondb-audit`

## ADDED Requirements

### Requirement: Implement Action Entries MVP
ActionDB MUST define known actions or source signals with stable IDs, names, permissions, risk tiers, and docs links.

#### Scenario: mvp-implemented
- GIVEN a known network action is scanned WHEN audit runs THEN the corresponding ActionDB risk metadata is attached.
