# Delta: `shortcutkit-cli` for `add-html-runtime-profiles`

## ADDED Requirements

### Requirement: HTML Analyze Command

The system MUST expose `shortcutkit html analyze <entrypoint>` and emit deterministic diagnostics for local HTML runtime suitability.

#### Scenario: analyze-local-bundled-suitability

- GIVEN an HTML entrypoint with local CSS and JavaScript references WHEN `shortcutkit html analyze <entrypoint> --json` runs THEN the output includes the `local-bundled` profile status, discovered assets, size classification, and unsupported patterns.

### Requirement: HTML Bundle Command

The system MUST expose `shortcutkit html bundle <entrypoint> --output <path>` for constrained local bundled HTML.

#### Scenario: bundle-supported-local-assets

- GIVEN an HTML entrypoint with supported local CSS and JavaScript assets WHEN the bundle command runs THEN it writes a single `.bundled.html` file and emits JSON containing the output path and SHA-256 digest when requested.

### Requirement: HTML Hosted Publish Command

The system MUST expose `shortcutkit html publish <site> --provider here-now` with dry-run as the safe default and `--run` as the explicit network opt-in.

#### Scenario: publish-dry-run-no-egress

- GIVEN a static site directory WHEN `shortcutkit html publish <site> --provider here-now --dry-run --json` runs THEN no network publish occurs and JSON describes the candidate files and provider.

#### Scenario: publish-run-requires-opt-in

- GIVEN a static site directory WHEN `shortcutkit html publish <site> --provider here-now --run --json` runs THEN the command may contact here.now and MUST redact sensitive claim URLs from persisted outputs.
