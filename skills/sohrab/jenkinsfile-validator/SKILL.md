---
name: jenkinsfile-validator
description: Validate, lint, and test Jenkinsfile pipelines (Declarative and Scripted) — syntax, best practices, plugin usage, credentials handling, and CPS/serialization pitfalls. Use when working with Jenkins pipeline files, checking pipeline syntax, or debugging pipeline failures. Do not use to generate new Jenkinsfiles from scratch (use `jenkinsfile-generator`), for GitHub Actions / GitLab CI / other CI systems, or for generic Groovy edits with no Jenkins pipeline semantics.
---

# Jenkinsfile Validator

## Overview

Validate, lint, and test Jenkinsfile pipelines in both Declarative and Scripted syntax.
This `SKILL.md` is the slim router; the full validation workflow, syntax references,
error reporting, and worked scenarios live in `references/playbook.md`. Load reference
files by their skill-relative path (for example `references/declarative_syntax.md`) —
never hard-code an absolute or pack-prefixed path, so the skill resolves identically
under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Jenkins, plugin, LTS, credentials, CPS, or pipeline-step behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  Jenkins docs, plugin docs, or live controller metadata confirm the guidance.

## When NOT to use

- Generating new Jenkinsfiles from scratch — use `jenkinsfile-generator`.
- GitHub Actions, GitLab CI, or other CI systems.
- Generic Groovy edits where Jenkins pipeline semantics are not involved.

## Workflow

1. Detect pipeline type (Declarative vs Scripted) and the steps/plugins used.
2. Lint syntax (Jenkins linter / `declarative-linter` where available) against
   `references/declarative_syntax.md` / `references/scripted_syntax.md`.
3. Detect referenced plugins and look up current docs (`references/common_plugins.md`).
4. Apply validation rules (agent/stage structure, credentials, CPS-safe code, security).
5. Report errors with file/line, severity, and fixes; verify against `references/best_practices.md`.
6. Re-validate after fixes until clean.

Full workflow, syntax references, error reporting, and worked scenarios:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — complete validation workflow, rules, examples
- `references/declarative_syntax.md` — Declarative pipeline reference
- `references/scripted_syntax.md` — Scripted pipeline reference
- `references/common_plugins.md` — frequently used plugins and their steps
- `references/best_practices.md` — Jenkins pipeline best practices
- `references/source-map.md` — official-source map for version-sensitive claims
