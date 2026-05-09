# Delta: `shortcut-manifest` for `add-html-runtime-profiles`

## ADDED Requirements

### Requirement: HTML Runtime Metadata

The manifest validator MUST accept optional `html_runtime` metadata that describes supported HTML runtime profiles, entrypoints, bundle outputs, size gates, and hosting providers.

#### Scenario: manifest-records-html-runtime-profiles

- GIVEN a shortcut supports bundled local HTML and hosted multi-file HTML WHEN validation and catalog generation run THEN the manifest metadata is accepted and surfaced without treating hosted publishing as shortcut runtime network access.

### Requirement: Bundled Local URL Scheme Declaration

A shortcut manifest that opens local bundled HTML through a `data:` URL MUST declare the `data` URL scheme.

#### Scenario: bundled-profile-declares-data-scheme

- GIVEN source opens `data:text/html;base64,...` WHEN strict audit runs THEN the audit passes only when `declared_permissions.url_schemes` includes `data`.
