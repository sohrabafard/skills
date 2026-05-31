---
name: terragrunt-generator
description: Generate best-practice Terragrunt configurations — root configs, child modules, Stacks (`terragrunt.stack.hcl`), feature flags, and multi-environment setups — then validate them. Use when scaffolding new Terragrunt projects or DRY multi-env infrastructure. Do not use to validate or debug existing Terragrunt with no generation need (use `terragrunt-validator`), for plain Terraform-only projects (use the Terraform skills), or for cloud-architecture prose where HCL is not the expected artifact.
---

# Terragrunt Generator

## Overview

Generate production-ready Terragrunt configurations (including 2025 Stacks, feature flags,
exclude/errors blocks, and OpenTofu engine), then validate them. This `SKILL.md` is the
slim router; the architecture patterns, capabilities, examples, and quick-reference card
live in `references/playbook.md`. Load reference files by their skill-relative path (for
example `references/common-patterns.md`) — never hard-code an absolute or pack-prefixed
path, so the skill resolves identically under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Terragrunt, Stacks, CLI redesign, Terraform/OpenTofu, provider, backend, or module behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  Terragrunt, Terraform/OpenTofu, provider, registry, or cloud-provider docs confirm the guidance.

## When NOT to use

- Validating or debugging existing Terragrunt with no generation need — use `terragrunt-validator`.
- Plain Terraform-only projects — use the Terraform skills.
- Cloud-architecture prose where Terragrunt HCL is not the expected artifact.

## Workflow

1. Choose the architecture pattern (single root, multi-env, Stacks) — see `references/playbook.md`.
2. Read `references/common-patterns.md` (and the `terragrunt-validator` skill's
   `references/best_practices.md`) before generating.
3. Generate root config, child modules, and/or `terragrunt.stack.hcl` with prefer-modern
   blocks (`exclude`/`errors`/`feature`), correct `dependency`/`dependencies`, and DRY inputs.
4. Avoid deprecated attributes (`skip`, `retryable_errors`); use their modern replacements.
5. Validate with the `terragrunt-validator` skill; fix findings and re-validate.
6. Provide usage and environment-promotion instructions.

Full architecture patterns, capabilities, common issues, and the quick-reference card:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — architecture patterns, capabilities, examples, quick-reference card
- `references/common-patterns.md` — reusable Terragrunt patterns
- `references/source-map.md` — official-source map for version-sensitive claims
- `terragrunt-validator` skill `references/best_practices.md` — shared best-practice ruleset
