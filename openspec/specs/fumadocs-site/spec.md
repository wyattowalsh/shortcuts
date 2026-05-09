# Capability: Fumadocs Developer Site

## Purpose

Provide a production-grade documentation site for users, contributors, and agents.

## Requirements

### Requirement: Next.js App Router

The docs site MUST use Next.js App Router under `apps/docs`.

#### Scenario: Build docs app

- GIVEN dependencies are installed
- WHEN `pnpm --filter @shortcuts/docs build` runs
- THEN the docs site builds successfully

### Requirement: Fumadocs MDX

The docs site MUST use Fumadocs MDX and ESM configuration.

#### Scenario: Next config

- GIVEN `apps/docs/next.config.mjs`
- WHEN the app builds
- THEN Fumadocs MDX is configured via `createMDX`

### Requirement: Generated Reference Content

The docs site MUST render generated shortcut catalog, manifest schema, CLI reference, and security rule pages.

#### Scenario: Manifest schema changes

- GIVEN `packages/schemas/shortcut.schema.json` changes
- WHEN docs generation runs
- THEN the docs reference page updates or drift check fails

### Requirement: Search

The docs site MUST provide self-hosted search by default.

#### Scenario: Search query

- GIVEN the docs site is running
- WHEN a user searches for `network permissions`
- THEN relevant docs and shortcuts appear

### Requirement: LLM Routes

The docs site MUST expose `llms.txt` and `llms-full.txt` routes.

#### Scenario: Agent reads docs

- GIVEN an AI coding agent requests `/llms-full.txt`
- WHEN the route loads
- THEN it receives processed Markdown for the docs corpus

### Requirement: Versioning and Changelog

The docs site MUST document the versioned docs and changelog strategy before any CLI or manifest breaking change ships.

#### Scenario: CLI breaking change

- GIVEN a CLI breaking change ships
- WHEN docs are deployed
- THEN migration notes and changelog are available
