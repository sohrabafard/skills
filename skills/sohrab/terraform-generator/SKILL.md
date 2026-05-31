---
name: terraform-generator
description: Generate production-ready Terraform / OpenTofu configurations (HCL) — resources, variables, outputs, modules, providers, and backends. Use when the task is to author or scaffold new `.tf` / `.tfvars` files, build a Terraform project, or add infrastructure resources. Triggers on creating AWS/Azure/GCP/Kubernetes/custom-provider infrastructure as code. Do not use to validate or debug existing Terraform with no generation need (use `terraform-validator`), for Terragrunt projects (use the Terragrunt skills), or for cloud-architecture prose where HCL is not the expected artifact.
---

# Terraform Generator

## Overview

Generate production-ready Terraform/OpenTofu configurations that follow current best
practices, then validate them. This `SKILL.md` is the workflow; depth lives in
`references/`. Load reference files by their skill-relative path (for example
`references/terraform_best_practices.md`) — never hard-code an absolute or pack-prefixed
path, so the skill resolves identically under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Terraform, OpenTofu, provider, backend, module, or registry behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  HashiCorp, OpenTofu, provider, registry, or cloud-provider docs confirm the guidance.

## When NOT to use

- Validating or debugging existing Terraform with no generation need — use `terraform-validator`.
- Terragrunt projects — use the Terragrunt skills.
- Cloud-architecture prose where Terraform HCL is not the expected artifact.

## Required workflow

**Complete every REQUIRED step in order. Do not skip a step.**

| Step | Action | Required |
|------|--------|----------|
| 1 | Understand requirements (providers, resources, modules, versions, backend) | ✅ |
| 2 | Detect custom/third-party providers/modules and look up their docs | ✅ |
| 3 | Read the relevant `references/` files before generating | ✅ |
| 4 | Generate HCL with all best practices applied | ✅ |
| 5 | Add data sources for dynamic values (region, account, AZs, AMIs) | ✅ |
| 6 | Add lifecycle protection on critical resources (KMS, DBs, data buckets) | ✅ |
| 7 | Run the `terraform-validator` skill | ✅ |
| 8 | Fix every validation/security failure and re-validate until all pass | ✅ |
| 9 | Provide usage instructions (files, next steps, security reminders) | ✅ |

> If validation fails (`terraform validate` or security scan), you MUST fix and
> re-validate until all checks pass before Step 9.

### Step 2 — custom providers/modules

Standard HashiCorp providers (aws, azurerm, google, kubernetes) need no lookup.
For third-party or custom providers/modules (e.g. `datadog/datadog`, registry or
private modules), look up version-specific docs first:

- `WebSearch` query: `"[provider/module] terraform [version] documentation [resource]"`.
- Prefer official sources (registry.terraform.io, provider sites): required/optional
  arguments, attribute references, example usage, version notes.
- If a Context7-style docs MCP is available, use it as an alternative.

### Step 3 — read references before generating

| Reference | Read when |
|-----------|-----------|
| `references/terraform_best_practices.md` | Always — required patterns and structure |
| `references/provider_examples.md` | Generating AWS/Azure/GCP/Kubernetes resources |
| `references/common_patterns.md` | Multi-environment, workspace, or complex setups |
| `references/modern-features-and-patterns.md` | Version-specific features (1.8+), generation patterns, error triage |
| `references/source-map.md` | Any version/security-sensitive claim |

### Step 5 — required data sources (never hardcode)

```hcl
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" {}
# AMIs via data "aws_ami" with filters; existing VPCs via data "aws_vpc"
```

### Step 6 — required lifecycle protection

Add `lifecycle { prevent_destroy = true }` on resources whose accidental destruction
loses data or breaks service: KMS keys, RDS instances/clusters, S3 buckets with data,
DynamoDB tables with data, ElastiCache clusters, Secrets Manager secrets.

For S3 lifecycle configurations, always include an abort-incomplete-multipart-upload
rule (Checkov `CKV_AWS_300`):

```hcl
rule {
  id     = "abort-incomplete-uploads"
  status = "Enabled"
  filter {}
  abort_incomplete_multipart_upload { days_after_initiation = 7 }
}
```

### Step 7-8 — validate and fix loop

Run the `terraform-validator` skill (it runs `terraform fmt -check`, `init`, `validate`,
a Checkov security scan, and optional `plan`). On any failure: review the error, fix the
file, re-run the validator, and repeat until all checks pass. Common fixes — `CKV_AWS_300`
(add abort-multipart rule), `CKV_AWS_24` (restrict SSH from `0.0.0.0/0`), `CKV_AWS_16`
(`storage_encrypted = true`).

### Step 9 — usage instructions

After all checks pass, report: the generated files and their purpose; next steps
(`terraform init` → `plan` → `apply`); customization checklist (tfvars, backend, tags);
and security reminders (review IAM, keep secrets out of VCS, enable encrypted state with
locking).

## Standard file layout

`main.tf` · `variables.tf` (with `description`, `type`, and `validation`) · `outputs.tf`
(with `description`) · `versions.tf` (`required_version` + pinned `required_providers`) ·
optional `backend.tf`, `locals.tf`, `data.tf`. Use modules with pinned versions, `locals`
for computed values, `dynamic` blocks for repetition, and never hardcode secrets. See
`references/terraform_best_practices.md` for the full ruleset.

## Resources

- `references/` — best practices, provider examples, common patterns, modern features,
  and the official-source map (load by skill-relative path).
- `assets/` — copyable project templates (`minimal-project/`, and others when present).

## Notes

- Always run `terraform-validator` after generation.
- Web search is essential for custom providers/modules.
- Prefer readable, well-commented, least-surprise configurations.
