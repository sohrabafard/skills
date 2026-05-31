---
name: jenkinsfile-generator
description: Generate production Jenkinsfiles in both Declarative and Scripted syntax — stages, agents, Docker/Kubernetes pods, shared libraries, credentials, and post conditions — then validate them. Use when authoring new Jenkins pipelines or CI/CD workflows on Jenkins. Do not use to validate or debug existing Jenkinsfiles with no generation need (use `jenkinsfile-validator`), for GitHub Actions / GitLab CI / other CI systems, or for application code changes that do not affect Jenkins pipeline behavior.
---

# Jenkinsfile Generator

## Overview

Generate production-ready Jenkinsfiles (Declarative preferred; Scripted when needed), then
validate them with `jenkinsfile-validator`. This `SKILL.md` is the slim router; the syntax
references, Docker/Kubernetes and shared-library patterns, generator scripts, and examples
live in `references/playbook.md`. Load reference files by their skill-relative path (for
example `references/common_plugins.md`) — never hard-code an absolute or pack-prefixed
path, so the skill resolves identically under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Jenkins, plugin, LTS, credentials, or pipeline-step behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  Jenkins docs, plugin docs, or live controller metadata confirm the guidance.

## When NOT to use

- Validating or debugging existing Jenkinsfiles with no generation need — use `jenkinsfile-validator`.
- GitHub Actions, GitLab CI, or other CI systems.
- Application code changes that do not affect Jenkins pipeline behavior.

## Workflow

1. Choose syntax (Declarative by default) and the agent model (label, Docker, or Kubernetes pod).
2. Read `references/best_practices.md` and `references/common_plugins.md` before generating.
3. Generate the pipeline: stages, steps, environment, credentials, `post` conditions, and
   shared-library usage as needed.
4. Apply best practices (least-privilege credentials, timeouts, `options`, parallelism, CPS-safe code).
5. Validate with the `jenkinsfile-validator` skill; fix and re-validate.
6. Provide usage instructions.

Full syntax references, Docker/Kubernetes and shared-library patterns, scripts, and examples:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — syntax references, patterns, generator scripts, examples
- `references/best_practices.md` — Jenkins pipeline best practices
- `references/common_plugins.md` — frequently used plugins and their steps
- `references/source-map.md` — official-source map for version-sensitive claims
