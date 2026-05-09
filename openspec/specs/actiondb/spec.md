# Capability: `actiondb`

## Purpose

Provide structured metadata for Shortcuts actions, source signals, risk categories, and remediation text.

## Requirements

### Requirement: Action Entries

ActionDB MUST define known actions or source signals with stable IDs, names, permissions, risk tiers, and docs links.

#### Scenario: action-entries

- GIVEN a known network action is scanned WHEN audit runs THEN the corresponding ActionDB risk metadata is attached.

### Requirement: Detector Rules

ActionDB MUST include detector rules for source languages and artifacts when a signal is used by strict audit.

#### Scenario: detector-rules

- GIVEN Cherri source contains a URL WHEN scanning runs THEN domain evidence is emitted.

### Requirement: Unknown Handling

Unknown high-risk actions MUST fail strict audit unless explicitly reviewed.

#### Scenario: unknown-handling

- GIVEN an opaque artifact has unknown action evidence WHEN strict audit runs THEN the audit fails closed.

### Requirement: Versioning

ActionDB changes MUST be versioned and reflected in audit output.

#### Scenario: versioning

- GIVEN ActionDB changes WHEN an audit result is generated THEN the ActionDB version is included.
