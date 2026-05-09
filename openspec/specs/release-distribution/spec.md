# Capability: `release-distribution`

## Purpose

Define release packaging, checksums, generated notes, and optional distribution channels.

## Requirements

### Requirement: Release Metadata
Every shortcut release MUST include release metadata with checksums, manifest snapshot, audit result, and source commit.

#### Scenario: release-metadata
- GIVEN release notes are generated WHEN artifact exists THEN SHA-256 is included.

### Requirement: Tagging
The repo MUST use consistent tag patterns for toolkit, shortcuts, catalog, and app-intents releases.

#### Scenario: tagging
- GIVEN a shortcut release WHEN tag is created THEN it follows `shortcut/<id>/vX.Y.Z`.

### Requirement: Install Instructions
Release notes MUST include install/import instructions and risk summary.

#### Scenario: install-instructions
- GIVEN a networked shortcut release WHEN notes render THEN network domains and data egress are visible.

### Requirement: Optional Mirrors
iCloud links and RoutineHub mirrors MAY be included but MUST NOT become source of truth.

#### Scenario: optional-mirrors
- GIVEN a mirror link is present WHEN catalog renders THEN canonical source remains GitHub/repo metadata.
