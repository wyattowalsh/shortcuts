# OpenSpec Validation Fix Handoff

## Scope

Fixed copied shortcuts OpenSpec spec wording so the direct local OpenSpec validator passes for this repository.

Changed requirement text in:

- `openspec/specs/actiondb/spec.md`
- `openspec/specs/app-intents/spec.md`
- `openspec/specs/app-intents-lab/spec.md`
- `openspec/specs/catalog-registry/spec.md`
- `openspec/specs/deployment-vercel-cloudflare/spec.md`
- `openspec/specs/fumadocs-site/spec.md`
- `openspec/specs/future-ecosystem/spec.md`
- `openspec/specs/observability-qa/spec.md`
- `openspec/specs/runtime-test-harness/spec.md`
- `openspec/specs/shortcut-manifest/spec.md`
- `openspec/specs/source-adapters/spec.md`

## Verification

Passed:

- `rtk npx -y @fission-ai/openspec@latest validate --all --json --strict`
- `rtk git diff --check`

Notes:

- The direct local validator reports 30/30 copied shortcuts OpenSpec artifacts passed.
- Some requirements still contain `MAY` in sentences that also contain `MUST`; the validator accepts them because the requirement text is normative.
- Implementation behavior was not changed in this pass.
