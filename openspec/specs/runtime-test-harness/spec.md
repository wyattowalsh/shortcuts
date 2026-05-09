# Capability: `runtime-test-harness`

## Purpose

Provide optional macOS runtime testing around the Apple `shortcuts` CLI.

## Requirements

### Requirement: Optional macOS Runtime

Runtime tests MUST be optional and MUST NOT block Linux-only contributors by default.

#### Scenario: optional-macos-runtime

- GIVEN Linux CI runs WHEN runtime tests are configured THEN macOS-only cases are skipped.

### Requirement: Input Output Fixtures

Runtime tests MUST support input paths, output paths, output type, stdout/stderr, and exit code capture.

#### Scenario: input-output-fixtures

- GIVEN a text fixture WHEN runtime test runs THEN output assertions can compare file contents.

### Requirement: Prompt Avoidance

Runtime tests MUST warn if a shortcut declares prompts, alerts, or manual input.

#### Scenario: prompt-avoidance

- GIVEN a manifest marks interactive prompts WHEN runtime test is requested THEN the harness warns before execution.

### Requirement: Install Boundary

The harness MUST distinguish install/import, run, and assertion steps.

#### Scenario: install-boundary

- GIVEN a shortcut is not installed WHEN test runs THEN the failure points to install/import setup.
