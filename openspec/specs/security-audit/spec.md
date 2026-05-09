# Capability: `security-audit`

## Purpose

Audit shortcut projects for permission, privacy, artifact, and provenance risks.

## Requirements

### Requirement: Permission Mismatch
The audit MUST compare detected evidence against declared permissions.

#### Scenario: permission-mismatch
- GIVEN detected network access is undeclared WHEN strict audit runs THEN it fails.

### Requirement: Risk Tiers
The audit MUST assign risk tiers and review requirements.

#### Scenario: risk-tiers
- GIVEN shell execution is detected WHEN audit runs THEN tier `shell` and two-reviewer requirement are emitted.

### Requirement: AI Model Usage
AI/model actions MUST distinguish on-device, Private Cloud Compute, extension model/ChatGPT, and unknown providers where possible.

#### Scenario: ai-model-usage
- GIVEN Use Model is declared with Extension Model WHEN docs render THEN data egress is marked maybe/external.

### Requirement: URL Scheme Audit
URL schemes and x-callback-url MUST be detected and declared.

#### Scenario: url-scheme-audit
- GIVEN source contains `shortcuts://x-callback-url` WHEN audit runs THEN callback risk metadata is emitted.

### Requirement: Artifact Provenance
Release artifacts MUST include checksums and source/build metadata when available.

#### Scenario: artifact-provenance
- GIVEN a `.shortcut` artifact exists WHEN audit runs THEN missing checksum is reported.
