---
name: azure-pipelines-validator
description: "Validate, lint, and security-check Azure DevOps Pipeline YAML — schema, task inputs, hosted images, service connections, and security findings, with bundled checker scripts. Use when reviewing or debugging existing Azure Pipelines. Do not use to generate new pipelines from scratch (use `azure-pipelines-generator`), or for GitHub Actions / GitLab CI / Jenkins."
---

# Azure Pipelines Validator

## Purpose

This skill covers: Comprehensive toolkit for validating, linting, and securing Azure DevOps Pipeline configurations.

Keep this top-level file small. Load the topic map, supporting docs, examples, scripts, and the preserved full guide only as needed.

## When to use

- the user asks for work covered by this skill's description
- you need the bundled docs, examples, or scripts to follow the house workflow
- you want a routing-first entrypoint instead of loading a very large inline guide

## When NOT to use

- Generating new pipelines from scratch — use `azure-pipelines-generator`.
- GitHub Actions, GitLab CI, Jenkins, or other CI systems.
- Generic YAML edits where Azure Pipelines semantics are not involved.

## Quick start

1. Read the repo-local `AGENTS.md` and the current task constraints.
2. Read `docs/source-map.md` when validation depends on latest/current/version/security/current behavior, task inputs, hosted images, or service connections.
3. Read `docs/00-topic-map.md`.
4. Open only the smallest supporting docs, examples, or scripts needed for the exact task.
5. Read `docs/full-guide.md` only when the topic map is not enough.
6. Pair with the companion skill when generation and validation should both happen in the same task.

## Companion routing

- $azure-pipelines-generator
  - Pair it when the task is to generate or rewrite the target artifact, not just validate it.

## Reference navigation

- Official-first source map: `docs/source-map.md`
- Topic map: `docs/00-topic-map.md`
- Full preserved guide: `docs/full-guide.md`
- Supporting docs:
  - `docs/azure-pipelines-reference.md`
- Examples:
  - `examples/basic-pipeline.yml`
  - `examples/deployment-pipeline.yml`
  - `examples/docker-build.yml`
  - `examples/multi-platform.yml`
  - `examples/template-example.yml`
  - `examples/test-with-issues.yml`
- Scripts:
  - `scripts/check_best_practices.py`
  - `scripts/check_security.py`
  - `scripts/python_wrapper.sh`
  - `scripts/validate_azure_pipelines.sh`
  - `scripts/validate_syntax.py`
  - `scripts/yamllint_check.sh`
- Assets:
  - `assets/.yamllint`

## Maintenance rules

- Keep this file routing-first and easy to scan.
- Keep detailed guidance in `docs` instead of growing this file again.
- Keep the topic map aligned with the actual headings in the full guide.
- Keep paths in this file one hop away from `SKILL.md` so agents can discover them quickly.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only; confirm normative Azure Pipelines behavior against the source map.
