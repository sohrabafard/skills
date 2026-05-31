---
name: ansible-generator
description: Generate best-practice Ansible playbooks, roles, tasks, and inventory files with correct FQCN modules, idempotency, and structure, then validate them. Use when authoring or scaffolding Ansible automation. Do not use to validate or debug existing Ansible with no generation need (use `ansible-validator`), for non-Ansible artifacts (Terraform, Helm, Dockerfile, CI), or for one-off shell automation that should remain a script.
---

# Ansible Generator

## Overview

Generate production-ready Ansible content that is idempotent, FQCN-correct, and
best-practice compliant, then validate it. This `SKILL.md` is the slim router; the full
capabilities, patterns, and worked examples live in `references/playbook.md`. Load
reference files by their skill-relative path (for example `references/module-patterns.md`)
— never hard-code an absolute or pack-prefixed path, so the skill resolves identically
under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Ansible, collection, ansible-lint, or Molecule behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  the official/primary source map confirms the guidance.

## When NOT to use

- Validating or debugging existing Ansible with no generation need — use `ansible-validator`.
- Terraform, Helm, Dockerfile, or CI/CD authoring unless Ansible is the main artifact.
- One-off shell automation that should remain a script.

## Workflow

1. Clarify the target (playbook, role, task file, inventory), hosts, and desired end state.
2. Read `references/best-practices.md` and `references/module-patterns.md` before generating.
3. Generate idempotent content using FQCN modules, handlers, variables, and proper structure.
4. Apply the best-practice rules (no shell where a module exists, `changed_when`/`check_mode`,
   secrets via vault, tags, naming).
5. Validate with the `ansible-validator` skill (ansible-lint, check mode, Molecule); fix and re-run.
6. Provide usage instructions and a final mandatory checklist.

Full capabilities, common patterns, troubleshooting, and worked examples:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — complete capabilities, patterns, checklist, examples
- `references/best-practices.md` — Ansible best-practice ruleset to enforce
- `references/module-patterns.md` — recommended module usage patterns
- `references/source-map.md` — official-source map for version-sensitive claims
