---
name: alaa-workflow
description: "Phase-based workflow for long, risky, or multi-file tasks with low-noise execution and resumable plans."
---

# Alaa Workflow

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Workflow.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- long or multi-phase tasks
- multi-file behavior-changing work
- same-branch coordination where progress tracking matters
- tasks that need resumable execution artifacts

## When NOT to use

- tiny one-file tasks with no coordination cost
- read-only questions that do not need phased execution

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. Pair with the listed companion skills before making changes outside this skill's ownership.

## Companion routing

- $alaa-low-noise
  - Pair when the task also touches compact output and low-noise command discipline.

## Reference navigation

- Section map and fast routing:
  - `references/00-topic-map.md`
- Full preserved guidance, rules, examples, and checklists:
  - `references/full-guide.md`

## Maintenance rules

- Keep this file routing-first and plain.
- Put detailed rules into `references/full-guide.md` instead of growing this file.
- Keep the topic map aligned with the actual headings in the full guide.
- Re-check companion-skill routing when ownership boundaries change.
