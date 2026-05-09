# Capability: App Intents Examples

## Purpose

Provide Swift reference implementations for app-exposed shortcuts and Siri/App Shortcut developer patterns.

## Requirements

### Requirement: Minimal AppIntent Example

The repository MUST include a minimal Swift `AppIntent` example.

#### Scenario: Developer explores minimal intent

- GIVEN a developer opens `app-intents/snippets`
- WHEN they inspect `MinimalAppIntent.swift`
- THEN they see the smallest production-quality intent pattern

### Requirement: AppShortcutsProvider Example

The repository MUST include an `AppShortcutsProvider` example with phrase guidance.

#### Scenario: Siri phrase review

- GIVEN an example defines phrases
- WHEN docs are generated
- THEN phrase design guidance is linked from the example

### Requirement: Entity and Enum Examples

The repository MUST include typed intent examples covering `AppEnum` and parameterized intents, and MUST document where `AppEntity` examples belong when added.

#### Scenario: Parameterized action

- GIVEN an example creates a task with priority
- WHEN a developer reads it
- THEN they can see typed parameters and validation

### Requirement: Testing Guidance

App Intents examples MUST include testing and preview guidance.

#### Scenario: Example modified

- GIVEN a developer changes a Swift example
- WHEN CI or local validation runs
- THEN formatting, build guidance, and manual Siri/Shortcuts verification steps are available
