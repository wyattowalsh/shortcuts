# Capability: `future-ecosystem`

## Purpose

Track non-MVP extensions without letting them destabilize the core build.

## Requirements

### Requirement: Backlog Isolation

Future ecosystem ideas MUST be documented separately from MVP requirements.

#### Scenario: backlog-isolation

- GIVEN an advanced integration is proposed WHEN not MVP-critical THEN it lands in future backlog.

### Requirement: Plugin Architecture

The CLI MUST keep adapter boundaries explicit so future adapter/plugin expansion remains possible without destabilizing MVP behavior.

#### Scenario: plugin-architecture

- GIVEN a new DSL adapter is added WHEN registered THEN it declares capabilities and license notes.

### Requirement: API Surface

The project MUST treat any catalog API or OpenAPI schema as a post-stability proposal tracked separately from MVP requirements.

#### Scenario: api-surface

- GIVEN catalog schema stabilizes WHEN API proposal is created THEN Fumadocs OpenAPI generation can be considered.
