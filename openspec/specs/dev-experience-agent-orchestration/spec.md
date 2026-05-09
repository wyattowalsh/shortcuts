# Capability: `dev-experience-agent-orchestration`

## Purpose

Coordinate parallel coding agents and human maintainers across a large monorepo build.

## Requirements

### Requirement: Agent Guidance
The repo MUST include AGENTS.md guidance at root and MAY include path-specific guidance.

#### Scenario: agent-guidance
- GIVEN Codex starts in the repo WHEN it discovers AGENTS.md THEN it receives setup, style, and verification guidance.

### Requirement: Task Claims
Agents MUST claim tasks before editing implementation files.

#### Scenario: task-claims
- GIVEN a task is unclaimed WHEN an agent starts work THEN it creates `.agent/claims/<task-id>.json`.

### Requirement: Handoffs
Agents MUST write handoff notes after completing or blocking a task.

#### Scenario: handoffs
- GIVEN an agent completes a task WHEN it exits THEN `.agent/handoffs/<task-id>.md` includes commands run and evidence.

### Requirement: Wave Gates
The project MUST define wave gates that prevent later waves from invalidating incomplete foundations.

#### Scenario: wave-gates
- GIVEN W2 schema tasks are incomplete WHEN W3 audit tasks start THEN the scheduler flags unmet dependencies.
