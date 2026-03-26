---
name: azure-pipelines-validator
description: "Comprehensive toolkit for validating, linting, and securing Azure DevOps Pipeline configurations."
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

- do not use this skill as a generic replacement for unrelated tooling work
- do not use it when the task is to build a brand-new artifact from scratch

## Quick start

1. Read the repo-local `AGENTS.md` and the current task constraints.
2. Read `docs/00-topic-map.md`.
3. Open only the smallest supporting docs, examples, or scripts needed for the exact task.
4. Read `docs/full-guide.md` only when the topic map is not enough.
5. Pair with the companion skill when generation and validation should both happen in the same task.

## Companion routing

- $azure-pipelines-generator
  - Pair it when the task is to generate or rewrite the target artifact, not just validate it.

## Reference navigation

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
