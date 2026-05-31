---
name: terraform-validator
description: Validate, lint, security-scan, and dry-run Terraform / OpenTofu — `fmt`, `init`, `validate`, Checkov security scan, `plan`, and provider-doc lookup. Use when checking `.tf` / `.tfvars` files, auditing infrastructure-as-code, or debugging configurations. Do not use to generate new Terraform from scratch (use `terraform-generator`), for Terragrunt projects (use the Terragrunt skills), or for generic HCL edits with no Terraform semantics.
---

# Terraform Validator

## Overview

Validate, lint, security-scan, and dry-run Terraform/OpenTofu with intelligent provider
documentation lookup. This `SKILL.md` is the slim router; the full validation workflow,
security cross-reference, provider-detection logic, scripts, and examples live in
`references/playbook.md`. Load reference files by their skill-relative path (for example
`references/security_checklist.md`) — never hard-code an absolute or pack-prefixed path,
so the skill resolves identically under Claude and Codex. Run any bundled scripts from
this skill's own directory.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Terraform, OpenTofu, provider, scanner, backend, module, or registry behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  Terraform/OpenTofu, provider, scanner, registry, or cloud-provider docs confirm the guidance.

## When NOT to use

- Generating new Terraform from scratch — use `terraform-generator`.
- Terragrunt projects — use the Terragrunt skills.
- Generic HCL edits where Terraform semantics are not involved.

## Workflow

1. Format check: `terraform fmt -check -recursive`.
2. Initialize: `terraform init` (backend off for validation when appropriate).
3. Validate: `terraform validate`; detect implicit/custom providers and look up their docs.
4. Security scan with Checkov; cross-reference findings (`references/security_checklist.md`,
   `references/common_errors.md`) and fix.
5. Dry-run with `terraform plan` when requested.
6. Loop fix-and-revalidate until all checks pass; report results clearly.

Full workflow, security cross-reference, provider detection, scripts, and worked examples:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — complete validation workflow, security cross-ref, scripts, examples
- `references/best_practices.md` — Terraform best-practice ruleset
- `references/advanced_features.md` — advanced validation features
- `references/common_errors.md` — frequent errors and fixes
- `references/security_checklist.md` — security audit checklist
- `references/source-map.md` — official-source map for version-sensitive claims
