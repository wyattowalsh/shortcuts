# Capability: `docs-site`

## Purpose

Serve the developer docs, catalog, generated references, search, and LLM endpoints.

## Requirements

### Requirement: Fumadocs Next App
The docs app MUST use Next.js App Router with Fumadocs and an ESM `next.config.mjs`.

#### Scenario: fumadocs-next-app
- GIVEN dependencies are installed WHEN docs build runs THEN Fumadocs MDX compiles.

### Requirement: Collections
The docs app MUST define Fumadocs MDX collections in `source.config.ts` with build-time schemas.

#### Scenario: collections
- GIVEN invalid frontmatter WHEN docs build runs THEN validation fails.

### Requirement: Search
The docs app MUST expose a search API backed by Fumadocs/Orama.

#### Scenario: search
- GIVEN docs are built WHEN `/api/search` is queried THEN relevant docs can be returned.

### Requirement: LLM Endpoints
The docs app MUST expose `/llms.txt` and `/llms-full.txt`.

#### Scenario: llm-endpoints
- GIVEN the docs site is deployed WHEN `/llms.txt` is fetched THEN it returns a curated index.

### Requirement: Generated References
The docs app MUST include generated pages for schemas, CLI, ActionDB, security rules, and catalog.

#### Scenario: generated-references
- GIVEN `shortcutkit docs generate` runs WHEN docs build runs THEN reference pages are present.
