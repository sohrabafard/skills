---
name: bash-script-generator
description: "Comprehensive toolkit for generating best practice bash scripts following current standards and conventions. Use this skill when creating new bash scripts, implementing shell automation, text processing workflows, or building production-ready command-line tools."
---

# Bash Script Generator

## Purpose

This skill covers: Comprehensive toolkit for generating best practice bash scripts following current standards and conventions. Use this skill when creating new bash scripts, implementing shell automation, text processing workflows, or building production-ready command-line tools.

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
2. Read `docs/00-topic-map.md`.
3. Open only the smallest supporting docs, examples, or scripts needed for the exact task.
4. Read `docs/full-guide.md` only when the topic map is not enough.
5. Pair with the companion skill when generation and validation should both happen in the same task.

## Companion routing

- $bash-script-validator
  - Pair it before final delivery so generated output is checked with the matching validation workflow.

## Reference navigation

- Topic map: `docs/00-topic-map.md`
- Full preserved guide: `docs/full-guide.md`
- Supporting docs:
  - `docs/bash-scripting-guide.md`
  - `docs/generation-best-practices.md`
  - `docs/script-patterns.md`
  - `docs/text-processing-guide.md`
- Examples:
  - `examples/log-analyzer.sh`
- Scripts:
  - `scripts/generate_script_template.sh`
- Assets:
  - `assets/templates`

## Maintenance rules

- Keep this file routing-first and easy to scan.
- Keep detailed guidance in `docs` instead of growing this file again.
- Keep the topic map aligned with the actual headings in the full guide.
- Keep paths in this file one hop away from `SKILL.md` so agents can discover them quickly.
