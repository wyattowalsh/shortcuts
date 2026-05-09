# W6 Launch Handoff

Launch readiness artifacts added:

- `ROADMAP.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/bug.yml`
- `.github/ISSUE_TEMPLATE/shortcut.yml`
- `.github/workflows/release.yml`
- `.github/workflows/scorecard.yml`
- `.github/workflows/license.yml`
- `apps/docs/content/docs/reference/known-limitations.mdx`
- `apps/docs/content/docs/reference/troubleshooting.mdx`
- `apps/docs/content/docs/contributing/release-checklist.mdx`

Final verification passed with `pnpm build`, `uv run pytest`, and `uv run shortcutkit security audit --strict`.
