# Delta for app-intents

## ADDED Requirements

### Requirement: Add App Intents Lab Delivery
The system SHALL implement the `add-app-intents-lab` change according to its proposal, design, tasks, and affected capability requirements.

#### Scenario: Change implemented
- GIVEN the `add-app-intents-lab` proposal is approved
- WHEN implementation is complete
- THEN all tasks in `openspec/changes/add-app-intents-lab/tasks.md` are checked off
- AND relevant validation commands pass
- AND updated docs or generated artifacts are committed

#### Scenario: Change blocked
- GIVEN an implementation blocker is discovered
- WHEN work stops
- THEN the blocker is recorded in the task graph or handoff notes
- AND no task is marked complete without verification
