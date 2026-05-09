# Maintainers

Current maintainer group:

- shortcuts maintainers

## Review Expectations

Low-risk documentation and metadata changes may be reviewed by one maintainer.

Shortcuts with shell execution, credential access, network exfiltration risk, signing changes, or unknown high-risk audit findings require two maintainer reviews before release.

## Release Checklist

- Run `uv run shortcutkit security audit --strict`.
- Run `uv run shortcutkit catalog generate --check`.
- Run `uv run shortcutkit docs generate --docs-root apps/docs --check`.
- Generate release metadata and notes with `uv run shortcutkit release metadata <package>` and `uv run shortcutkit release notes <package>`.
- Verify checksums for any `.shortcut` artifacts under `dist/`.
