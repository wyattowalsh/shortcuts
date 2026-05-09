# Security Policy

## Reporting

Report vulnerabilities by opening a private security advisory when available, or by contacting the maintainers listed in `MAINTAINERS.md` with a concise reproduction, affected paths, and impact.

Do not publish working exploits for shortcuts, generated artifacts, signing flows, credential handling, or CI secrets before maintainers have had a reasonable opportunity to respond.

## Review Model

Security review distinguishes:

- declared permissions in `shortcut.yml`;
- detected capabilities in source files and artifacts;
- unknown or unsupported signals;
- review status and reviewer notes;
- release provenance and checksums.

Strict audit mode fails closed for unknown high-risk evidence. The project never claims that a shortcut is absolutely safe.

## High-Risk Capability Classes

Network, shell execution, URL schemes, credentials, file access, calendar, contacts, location, photos, clipboard, JavaScript, external apps, and AI/model usage are modeled separately.

AI/model usage must declare provider class, input data classes, whether data leaves the device where known, output handling, and user-facing privacy notes.
