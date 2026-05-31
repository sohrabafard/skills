---
name: terragrunt-validator
description: Validate, lint, security-scan, and dry-run Terragrunt configurations and Stacks. Use when working with `.hcl` / `terragrunt.hcl` / `terragrunt.stack.hcl` files, running `terragrunt plan`, checking dependency graphs, formatting HCL, or scanning IaC with Trivy/Checkov. Do not use to generate new Terragrunt from scratch (use `terragrunt-generator`), for plain Terraform-only projects (use the Terraform skills), or for generic HCL edits with no Terragrunt semantics.
---

# Terragrunt Validator

## Overview

Validate, lint, test, and dry-run Terragrunt configurations and Stacks. This `SKILL.md`
is the slim router; the full workflow, capabilities, troubleshooting, and examples live
in `references/playbook.md`. Load reference files by their skill-relative path (for
example `references/best_practices.md`) — never hard-code an absolute or pack-prefixed
path, so the skill resolves identically under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Terragrunt, Stacks, CLI redesign, Terraform/OpenTofu, provider, scanner, backend, or
  module behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  Terragrunt, Terraform/OpenTofu, provider, scanner, registry, or cloud-provider docs
  confirm the guidance.

## When NOT to use

- Generating new Terragrunt from scratch — use `terragrunt-generator`.
- Plain Terraform-only projects — use the Terraform skills.
- Generic HCL edits where Terragrunt semantics are not involved.

## Workflow

1. Detect the configuration type (`terragrunt.hcl`, child unit, `terragrunt.stack.hcl`)
   and the Terragrunt version; check `references/source-map.md` for version-sensitive behavior.
2. Format and lint: `terragrunt hcl fmt`/`hclfmt`, then validate HCL and inputs.
3. Detect custom providers/modules and look up their docs before asserting behavior.
4. Run `terragrunt validate` / `validate-inputs`, inspect the dependency graph, and
   dry-run with `terragrunt plan` when requested.
5. Security-scan generated IaC (Trivy, Checkov); fix findings and re-scan until clean.
6. Report results, errors, and a remediation summary.

Full step-by-step procedure, tool requirements, troubleshooting, and worked examples:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — complete validation workflow, capabilities, troubleshooting, examples
- `references/best_practices.md` — Terragrunt best-practice ruleset
- `references/source-map.md` — official-source map for version-sensitive claims
