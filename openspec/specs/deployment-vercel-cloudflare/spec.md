# Capability: `deployment-vercel-cloudflare`

## Purpose

Deploy the Fumadocs site to Vercel using Cloudflare-managed DNS.

## Requirements

### Requirement: Vercel Project

The docs app MUST be deployable as a Vercel project with root directory `apps/docs`.

#### Scenario: vercel-project

- GIVEN Vercel builds the project WHEN root directory is set THEN the Next app builds.

### Requirement: External DNS Flow

The runbook MUST use Vercel domain inspection and external DNS configuration for Cloudflare.

#### Scenario: external-dns-flow

- GIVEN DNS remains at Cloudflare WHEN domain is added THEN the runbook instructs adding exact Vercel-provided records in Cloudflare.

### Requirement: Subdomain Preference

The deployment runbook MUST prefer `docs.<domain>` over apex for MVP unless a maintainer records an explicit exception.

#### Scenario: subdomain-preference

- GIVEN a maintainer deploys MVP WHEN choosing domain THEN subdomain CNAME is recommended.

### Requirement: SSL Verification

The runbook MUST include SSL, CAA, and DNS verification commands.

#### Scenario: ssl-verification

- GIVEN deployment completes WHEN verification runs THEN DNS and cert status are checked.
