# Delta: `catalog-registry` for `add-catalog-release-pipeline`

## ADDED Requirements

### Requirement: Implement Catalog JSON MVP
The system MUST generate `catalog/catalog.json` from valid manifests.

#### Scenario: mvp-implemented
- GIVEN two valid manifests WHEN catalog generation runs THEN both appear with normalized IDs.
