# Official-first source map

Use this map before validating version-sensitive Terragrunt content. Terragrunt docs, Terraform/OpenTofu docs, provider docs, scanner docs, and module registry docs outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Terragrunt docs home: https://docs.terragrunt.com/
- Terragrunt CLI: https://docs.terragrunt.com/reference/cli/
- Terragrunt configuration blocks: https://docs.terragrunt.com/reference/hcl/blocks/
- Terragrunt attributes: https://docs.terragrunt.com/reference/hcl/attributes/
- Terragrunt Stacks: https://docs.terragrunt.com/features/stacks/
- Terraform CLI validate: https://developer.hashicorp.com/terraform/cli/commands/validate
- OpenTofu docs: https://opentofu.org/docs/
- Checkov docs: https://www.checkov.io/1.Welcome/What%20is%20Checkov.html
- Trivy docs: https://aquasecurity.github.io/trivy/latest/

## Freshness triggers

Fetch current official docs when validation depends on Terragrunt versions, CLI redesign behavior, Stacks, OpenTofu/Terraform versions, scanner policy IDs, security advisories, provider/module versions, or deprecated commands.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, discussions, and community blogs only to troubleshoot symptoms. Confirm validation findings and fixes against Terragrunt, Terraform/OpenTofu, scanner, or provider docs.
