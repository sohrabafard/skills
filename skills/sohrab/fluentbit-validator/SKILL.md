---
name: fluentbit-validator
description: "Comprehensive toolkit for validating, linting, and testing Fluent Bit configurations. Use this skill when working with Fluent Bit config files, validating syntax, checking for best practices, identifying security issues, or performing dry-run testing."
---

# Fluent Bit Config Validator

## Purpose

This skill covers: Comprehensive toolkit for validating, linting, and testing Fluent Bit configurations. Use this skill when working with Fluent Bit config files, validating syntax, checking for best practices, identifying security issues, or performing dry-run testing.

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
2. Read `references/00-topic-map.md`.
3. Open only the smallest supporting docs, examples, or scripts needed for the exact task.
4. Read `references/full-guide.md` only when the topic map is not enough.
5. Pair with the companion skill when generation and validation should both happen in the same task.

## Companion routing

- $fluentbit-generator
  - Pair it when the task is to generate or rewrite the target artifact, not just validate it.

## Reference navigation

- Topic map: `references/00-topic-map.md`
- Full preserved guide: `references/full-guide.md`
- Scripts:
  - `scripts/validate.sh`
  - `scripts/validate_config.py`
- Tests:
  - `tests/invalid-missing-required.conf`
  - `tests/invalid-opentelemetry.conf`
  - `tests/invalid-security-issues.conf`
  - `tests/invalid-tag-mismatch.conf`
  - `tests/valid-basic.conf`
  - `tests/valid-multioutput.conf`
  - `tests/valid-opentelemetry.conf`

## Maintenance rules

- Keep this file routing-first and easy to scan.
- Keep detailed guidance in `references` instead of growing this file again.
- Keep the topic map aligned with the actual headings in the full guide.
- Keep paths in this file one hop away from `SKILL.md` so agents can discover them quickly.
