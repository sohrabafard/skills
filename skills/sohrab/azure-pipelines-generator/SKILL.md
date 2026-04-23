---
name: azure-pipelines-generator
description: "Comprehensive toolkit for generating best practice Azure DevOps Pipelines following current standards and conventions. Use this skill when creating new Azure Pipelines, implementing CI/CD workflows, or building deployment pipelines."
---

# Azure Pipelines Generator

## Purpose

This skill covers: Comprehensive toolkit for generating best practice Azure DevOps Pipelines following current standards and conventions. Use this skill when creating new Azure Pipelines, implementing CI/CD workflows, or building deployment pipelines.

Keep this top-level file small. Load the topic map, supporting docs, examples, scripts, and the preserved full guide only as needed.

## When to use

- the user asks for work covered by this skill's description
- you need the bundled docs, examples, or scripts to follow the house workflow
- you want a routing-first entrypoint instead of loading a very large inline guide

## When NOT to use

- do not use this skill as a generic replacement for unrelated tooling work
- do not use it when the task is only to audit, lint, or debug an existing file

## Quick start

1. Read the repo-local `AGENTS.md` and the current task constraints.
2. Read `docs/source-map.md` when the task mentions latest/current/version/security/current behavior, task inputs, hosted images, or service connections.
3. Read `docs/00-topic-map.md`.
4. Open only the smallest supporting docs, examples, or scripts needed for the exact task.
5. Read `docs/full-guide.md` only when the topic map is not enough.
6. Pair with the companion skill when generation and validation should both happen in the same task.

## Companion routing

- $azure-pipelines-validator
  - Pair it before final delivery so generated output is checked with the matching validation workflow.

## Reference navigation

- Official-first source map: `docs/source-map.md`
- Topic map: `docs/00-topic-map.md`
- Full preserved guide: `docs/full-guide.md`
- Supporting docs:
  - `docs/best-practices.md`
  - `docs/tasks-reference.md`
  - `docs/templates-guide.md`
  - `docs/yaml-schema.md`
- Examples:
  - `examples/basic-ci.yml`
  - `examples/dotnet-cicd.yml`
  - `examples/go-cicd.yml`
  - `examples/kubernetes-deploy.yml`
  - `examples/multi-stage-cicd.yml`
  - `examples/python-cicd.yml`
  - `examples/template-usage.yml`
  - `examples/templates`

## Maintenance rules

- Keep this file routing-first and easy to scan.
- Keep detailed guidance in `docs` instead of growing this file again.
- Keep the topic map aligned with the actual headings in the full guide.
- Keep paths in this file one hop away from `SKILL.md` so agents can discover them quickly.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only; confirm normative Azure Pipelines behavior against the source map.
