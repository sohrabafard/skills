---
name: github-actions-generator
description: Generate production GitHub Actions workflows and custom local actions (composite, JS, Docker) — least-privilege permissions, SHA-pinned action versions, OIDC, matrices, reusable workflows, and concurrency — then validate them. Use when authoring new Actions CI/CD or reusable actions. Do not use to validate or debug existing workflows with no generation need (use `github-actions-validator`), for GitLab CI / Jenkins / other CI systems, or for application code changes that do not affect GitHub Actions.
---

# GitHub Actions Generator

## Overview

Generate production-ready GitHub Actions workflows and custom actions following current
security and naming standards, then validate them with `github-actions-validator`. This
`SKILL.md` is the slim router; the capabilities, triggers/expressions/context references,
modern features, and common patterns live in `references/playbook.md`. Load reference
files by their skill-relative path (for example `references/common-actions.md`) — never
hard-code an absolute or pack-prefixed path, so the skill resolves identically under
Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  GitHub Actions behavior, runner images, public actions, permissions, OIDC, or
  reusable-workflow limits.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  GitHub Docs or the action-maintainer source confirm the guidance.

## When NOT to use

- Validating or debugging existing workflows with no generation need — use `github-actions-validator`.
- GitLab CI, Jenkins, or other CI systems.
- Application code changes that do not affect GitHub Actions.

## Workflow

1. Determine the resource (workflow vs composite/JS/Docker action) and triggers
   (`references/advanced-triggers.md`).
2. Read `references/best-practices.md` and `references/common-actions.md` before generating.
3. Generate with mandatory standards: least-privilege `permissions`, SHA-pinned action
   versions, `concurrency`, and OIDC instead of long-lived secrets.
4. Use expressions/contexts and modern features correctly
   (`references/expressions-and-contexts.md`, `references/modern-features.md`).
5. Validate with the `github-actions-validator` skill; fix and re-validate.
6. Provide usage instructions.

Full capabilities, triggers/expressions references, modern features, and patterns:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — capabilities, validation workflow, patterns, summary
- `references/best-practices.md` — mandatory standards and best practices
- `references/common-actions.md` — vetted common actions
- `references/custom-actions.md` — authoring composite/JS/Docker actions
- `references/advanced-triggers.md` — event triggers and filters
- `references/expressions-and-contexts.md` — expression and context reference
- `references/modern-features.md` — modern Actions features
- `references/source-map.md` — official-source map for version-sensitive claims
