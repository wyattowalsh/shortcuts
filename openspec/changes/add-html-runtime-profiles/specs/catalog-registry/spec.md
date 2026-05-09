# Delta: `catalog-registry` for `add-html-runtime-profiles`

## ADDED Requirements

### Requirement: Catalog HTML Runtime Profiles

Catalog entries MUST include HTML runtime profile metadata when a shortcut manifest declares `html_runtime`.

#### Scenario: catalog-renders-html-runtime

- GIVEN Open HTML declares hosted and local bundled runtime profiles WHEN catalog generation runs THEN generated catalog JSON includes profile names, support status, provider names, and bundle asset metadata.

### Requirement: Documentation HTML Runtime Profiles

Generated docs MUST explain the difference between hosted multi-file Safari support and constrained local bundled support when runtime profile metadata exists.

#### Scenario: docs-render-runtime-limitations

- GIVEN Open HTML declares both profiles WHEN docs generation runs THEN the generated reference includes the runtime profiles and their limitations.
