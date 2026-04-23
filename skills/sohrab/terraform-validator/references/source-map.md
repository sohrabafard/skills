# Official-first source map

Use this map before validating version-sensitive Terraform content. HashiCorp Developer docs, Terraform Registry docs, provider maintainers, scanner docs, and cloud provider docs outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Terraform docs home: https://developer.hashicorp.com/terraform/docs
- Terraform CLI validate: https://developer.hashicorp.com/terraform/cli/commands/validate
- Terraform CLI fmt: https://developer.hashicorp.com/terraform/cli/commands/fmt
- Terraform CLI plan: https://developer.hashicorp.com/terraform/cli/commands/plan
- Terraform language: https://developer.hashicorp.com/terraform/language
- Terraform Registry providers: https://registry.terraform.io/browse/providers
- Checkov docs: https://www.checkov.io/1.Welcome/What%20is%20Checkov.html
- Trivy docs: https://aquasecurity.github.io/trivy/latest/
- OpenTofu docs when the runtime is OpenTofu: https://opentofu.org/docs/

## Freshness triggers

Fetch current official docs when validation depends on Terraform/OpenTofu versions, provider versions, scanner policy IDs, security advisories, deprecations, lock file behavior, backend behavior, or unknown resources/modules.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, forums, and community blogs only to troubleshoot observed failures. Confirm validation findings and fixes against Terraform, provider, scanner, or cloud provider docs.
