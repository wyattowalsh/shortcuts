# Delta: `security-audit` for `add-html-runtime-profiles`

## ADDED Requirements

### Requirement: HTML Source Scanning

The security audit MUST scan `.html`, `.css`, `.js`, and `.mjs` files under shortcut source trees for URL, URL-scheme, and action detector signals.

#### Scenario: detects-domains-in-html-assets

- GIVEN shortcut source contains an HTML or JavaScript file with an HTTP URL WHEN strict audit runs THEN undeclared domains are reported as mismatches.

### Requirement: HTML Runtime Profile Risk Reporting

The security audit MUST distinguish shortcut runtime permissions from developer-initiated hosted publish operations declared in `html_runtime` metadata.

#### Scenario: hosted-publish-is-metadata-not-shortcut-network

- GIVEN a manifest declares a here.now hosted HTML profile but the shortcut runtime does not make network requests WHEN strict audit runs THEN the hosted profile is reported for review without requiring `declared_permissions.network.allowed` for the shortcut runtime.
