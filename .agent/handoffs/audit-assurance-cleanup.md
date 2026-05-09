# Audit Assurance Cleanup Handoff

## Scope

Addressed pre-commit audit findings from code-review and security-audit passes:

- Ignored local editor settings and SwiftPM build outputs via `.gitignore`.
- Hardened release workflow input handling by using environment variables, package path validation, least-privilege permissions, and `persist-credentials: false`.
- Added least-privilege permissions and non-persistent checkout credentials across CI, catalog, security, license, runtime, and release workflows.
- Made security audit upload JSON artifacts even when strict audit fails, then fail explicitly.
- Enforced declared network domain allowlists in strict audit with `mismatch.network.domains` findings.
- Constrained artifact and external adapter entrypoints to relative paths inside the shortcut package root.
- Added regression fixtures/tests for undeclared network domains and traversal entrypoints.

## Verification

Passed after fixes:

- `uv run ruff check .`
- `uv run ty check packages/shortcutkit/src`
- `uv run pytest`
- `uv run shortcutkit security audit --strict`
- `uv run python scripts/check-licenses.py`
- `rtk git diff --check`

## Notes

- `.vscode/` is now ignored and intentionally left unmodified on disk.
- `shortcuts_codex_jumpstart_prompt_v3.md` remains pre-existing untracked user/source material and should not be included in the build-out commits unless explicitly requested.
