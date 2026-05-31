---
name: ansible-validator
description: Validate, lint, test, and dry-run Ansible playbooks, roles, collections, and inventories with ansible-lint, Molecule, check mode, and Checkov. Use when working with Ansible `.yml` / `.yaml` files, debugging playbook execution, auditing automation security, or testing custom modules and collections. Do not use to author new Ansible from scratch (use `ansible-generator`), for non-Ansible artifacts (Terraform, Helm, Dockerfile, CI), or for plain YAML edits with no Ansible semantics.
---

# Ansible Validator

## Overview

Validate, lint, test, and dry-run Ansible content. This `SKILL.md` is the slim router;
the full workflow, capabilities, troubleshooting, and examples live in
`references/playbook.md`. Load reference files by their skill-relative path (for example
`references/security_checklist.md`) — never hard-code an absolute or pack-prefixed path,
so the skill resolves identically under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Ansible, collection, ansible-lint, Molecule, or Checkov behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  the official/primary source map confirms the guidance.

## When NOT to use

- Generating new Ansible content from scratch — use `ansible-generator`.
- Terraform, Helm, Dockerfile, or CI/CD validation unless Ansible is the main artifact.
- General YAML edits with no Ansible semantics.

## Workflow

1. Identify the artifact (playbook, role, collection, inventory) and target Ansible/collection versions.
2. Lint with `ansible-lint`; check YAML and module/FQCN correctness.
3. Detect custom or deprecated modules and look up current alternatives (`references/module_alternatives.md`).
4. Dry-run with check mode (`--check --diff`); run Molecule scenarios when present.
5. Security-audit against `references/security_checklist.md` (and Checkov where applicable); fix and re-run.
6. Report findings, errors, and a remediation summary.

Full procedure, tool prerequisites, error troubleshooting, and worked examples:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — complete validation workflow, capabilities, examples
- `references/best_practices.md` — Ansible best-practice ruleset
- `references/common_errors.md` — frequent errors and fixes
- `references/module_alternatives.md` — deprecated → current module mapping
- `references/security_checklist.md` — security audit checklist
- `references/source-map.md` — official-source map for version-sensitive claims
