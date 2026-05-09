# Capability: Agent Orchestration

## Purpose

Enable multiple waves of parallel subagents to implement the monorepo without collisions.

## Requirements

### Requirement: Task Graph Source of Truth
The system MUST maintain a machine-readable task graph.

#### Scenario: Agent selects work
- GIVEN a subagent is assigned a task ID
- WHEN it opens `planning/task-graph.yaml`
- THEN it can find dependencies, owned paths, outputs, and acceptance criteria

### Requirement: Wave-Based Parallelism
Tasks MUST be organized into dependency waves.

#### Scenario: Wave 2 starts
- GIVEN all Wave 1 blocking tasks are complete
- WHEN Wave 2 agents start
- THEN each agent works on non-overlapping file globs

### Requirement: Handoff Notes
Every subagent MUST produce handoff notes for completed or blocked tasks.

#### Scenario: Task blocked
- GIVEN an agent cannot complete a task
- WHEN it stops work
- THEN it records blockers, assumptions, files touched, and next steps

### Requirement: File Ownership
Each task MUST declare path globs that bound its intended changes.

#### Scenario: Agent touches unowned file
- GIVEN an agent modifies a file outside assigned globs
- WHEN review occurs
- THEN the change requires explicit justification
