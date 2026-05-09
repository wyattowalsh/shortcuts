# Delta: `shortcut-manifest` for `add-shortcutkit-cli-and-schemas`

## ADDED Requirements

### Requirement: Implement Manifest Required MVP
Every shortcut package MUST include a `shortcut.yml` manifest.

#### Scenario: mvp-implemented
- GIVEN a directory under `shortcuts/` lacks a manifest WHEN validation runs THEN it fails with the missing path.
