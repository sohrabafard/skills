---
name: github-actions-validator
description: Validate, lint, and test GitHub Actions workflows and custom local/public actions with actionlint and act — syntax, permissions, OIDC, pinned action versions, runner images, and reusable-workflow limits. Use when working with `.github/workflows/*.yml`, auditing workflow security, or debugging workflow runs. Do not use to generate new workflows from scratch (use `github-actions-generator`), for GitLab CI / Jenkins / other CI systems, or for generic YAML where GitHub Actions semantics do not matter.
---

# GitHub Actions Validator

## Overview

Validate, lint, and test GitHub Actions workflows and actions. This `SKILL.md` is the
slim router; the full assistant workflow, validation procedure, troubleshooting, and a
complete multi-error worked example live in `references/playbook.md`. Load reference
files by their skill-relative path (for example `references/actionlint_usage.md`) — never
hard-code an absolute or pack-prefixed path, so the skill resolves identically under
Claude and Codex. Run any bundled scripts from this skill's own directory.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  GitHub Actions behavior, runner images, public actions, actionlint, act, permissions,
  OIDC, or reusable-workflow limits.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  GitHub Docs, tool docs, or the action-maintainer source confirm the guidance.

## When NOT to use

- Generating new workflows from scratch — use `github-actions-generator`.
- GitLab CI, Jenkins, or other CI systems.
- Generic YAML validation where GitHub Actions semantics do not matter.

## Workflow

1. Identify the resource (workflow, composite/JS/Docker action, reusable workflow).
2. Lint with `actionlint` (`references/actionlint_usage.md`); optionally dry-run with `act`
   (`references/act_usage.md`).
3. Audit security: least-privilege `permissions`, OIDC over long-lived secrets, and SHA-pinned
   action versions (`references/action_versions.md`).
4. Check runner-image assumptions (`references/runners.md`) and modern-feature usage
   (`references/modern_features.md`).
5. Report errors with file/line and fixes (`references/common_errors.md`); re-validate until clean.

Full assistant workflow, validation procedure, and the worked multi-error example:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — full assistant + validation workflow, troubleshooting, worked example
- `references/actionlint_usage.md` — actionlint usage
- `references/act_usage.md` — local execution with act
- `references/action_versions.md` — pinning and current action versions
- `references/runners.md` — runner images and capabilities
- `references/modern_features.md` — modern Actions features
- `references/common_errors.md` — frequent errors and fixes
- `references/source-map.md` — official-source map for version-sensitive claims
