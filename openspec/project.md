# OpenSpec project: `shortcuts`

## Purpose

`shortcuts` is an OSS monorepo for source-first Apple Shortcuts, Siri/App Shortcuts, App Intents examples, typed manifests, security review, testing, catalog generation, release automation, and developer documentation.

## Source-of-truth model

- Current system behavior lives under `openspec/specs/**/spec.md`.
- Proposed changes live under `openspec/changes/<change-id>/**`.
- OpenSpec project config lives in `openspec/config.yaml`.
- Major changes MUST have `proposal.md`, `design.md`, `tasks.md`, and one or more delta specs.
- Delta specs MUST use:
  - `## ADDED Requirements`
  - `## MODIFIED Requirements`
  - `## REMOVED Requirements`
- Every requirement MUST include at least one `#### Scenario:` block.
- Archive completed changes only after implementation and verification.

## Change IDs

Use kebab-case, verb-led IDs:

- `bootstrap-monorepo-foundation`
- `add-shortcutkit-cli-and-schemas`
- `add-security-actiondb-audit`
- `add-catalog-release-pipeline`
- `add-fumadocs-dev-docs-site`
- `add-vercel-cloudflare-deployment`
- `add-source-adapters-runtime-tests`
- `add-app-intents-lab`
- `add-agent-orchestration-hardening`
- `launch-oss-beta`

## Requirement keywords

Use RFC-style keywords consistently:

- `MUST` / `MUST NOT`: non-negotiable.
- `SHOULD` / `SHOULD NOT`: default behavior; exceptions require rationale.
- `MAY`: optional behavior.

## Engineering conventions

- Monorepo package manager: `pnpm`.
- Python package manager: `uv`.
- Python target: 3.13.
- Python libraries: Typer, Pydantic v2, Pydantic Settings, Rich, Loguru, Tenacity only when useful, pytest, Ruff, ty.
- Frontend stack: Next.js App Router, TypeScript, Fumadocs v16+, Tailwind CSS v4.
- CI MUST run static checks on Linux.
- macOS Shortcuts runtime tests MUST be optional/manual or self-hosted.
- Release artifacts MUST include checksums and permission metadata.
- Generated files MUST be reproducible or clearly labeled snapshots.

## Security conventions

- Every shortcut MUST have a manifest.
- Every manifest MUST declare permission usage.
- Security-sensitive capabilities MUST have review gates.
- Network, shell, URL scheme, x-callback-url, credential, file, calendar, contact, location, photo, clipboard, JavaScript, AppleScript, and AI/model usage MUST be declared.
- Unsafe or unknown actions MUST fail closed in strict mode unless explicitly approved.

## Agent conventions

- Agents MUST read this file before implementing.
- Agents MUST read relevant `openspec/specs/**` and `openspec/changes/**`.
- Agents MUST not implement outside assigned task globs.
- Agents MUST create claim and handoff files for task execution.
- Agents MUST update task status only after verification.
- Agents MUST record assumptions and blockers in handoff notes.
