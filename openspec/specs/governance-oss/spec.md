# Capability: `governance-oss`

## Purpose

Establish contribution, security, license, maintainer, and community governance.

## Requirements

### Requirement: Contribution Requirements
Contributed shortcuts MUST include manifest, README, permission declarations, and security notes where relevant.

#### Scenario: contribution-requirements
- GIVEN a PR adds a shortcut without permissions WHEN CI runs THEN it fails.

### Requirement: License Policy
The repo MUST define license policy for code, docs, examples, and generated artifacts.

#### Scenario: license-policy
- GIVEN an adapter dependency is GPL WHEN license check runs THEN policy explains external boundary.

### Requirement: Security Reporting
SECURITY.md MUST define reporting process and response expectations.

#### Scenario: security-reporting
- GIVEN a vulnerability is found WHEN reporter reads SECURITY.md THEN contact/escalation path is clear.

### Requirement: Maintainer Review
Review requirements MUST scale by risk tier.

#### Scenario: maintainer-review
- GIVEN a shell-tier shortcut PR WHEN review begins THEN two maintainers are required.
