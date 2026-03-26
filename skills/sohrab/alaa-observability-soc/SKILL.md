---
name: alaa-observability-soc
description: "Use this skill when the task involves logs, traces, metrics, or alerting work or correlation IDs or incident evidence requirements. Do not use it when feature work with no observability surface change."
---




# Alaa Observability SOC

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Observability SOC.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- logs, traces, metrics, or alerting work
- correlation IDs or incident evidence requirements
- Sentry integration or cleanup
- operational visibility reviews

## When NOT to use

- feature work with no observability surface change
- pure UI or frontend-only tasks

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. Pair with the listed companion skills before making changes outside this skill's ownership.

## Severity rubric

| Signal type | Use when                                                        |
|-------------|-----------------------------------------------------------------|
| log only    | the event is useful for forensics but not actionable on its own |
| metric      | you need durable trend visibility or SLO math                   |
| alert       | a human should investigate within working hours                 |
| page        | the condition is urgent enough to interrupt an operator now     |

## Companion routing

- $alaa-security-review
  - Pair when the task also touches security event semantics and sensitive data controls.
- $alaa-octane-performance
  - Pair when the task also touches long-lived worker observability concerns.

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
