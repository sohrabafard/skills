# Official-first source map

Use this map before generating version-sensitive Terraform content. HashiCorp Developer docs, Terraform Registry docs, provider maintainers, and cloud provider docs outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Terraform docs home: https://developer.hashicorp.com/terraform/docs
- Terraform language: https://developer.hashicorp.com/terraform/language
- Terraform CLI: https://developer.hashicorp.com/terraform/cli
- Terraform style guide: https://developer.hashicorp.com/terraform/language/style
- Terraform Registry providers: https://registry.terraform.io/browse/providers
- Terraform Registry modules: https://registry.terraform.io/browse/modules
- Terraform AWS provider: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- Terraform AzureRM provider: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
- Terraform Google provider: https://registry.terraform.io/providers/hashicorp/google/latest/docs
- OpenTofu docs when the runtime is OpenTofu: https://opentofu.org/docs/

## Freshness triggers

Fetch current official docs when the task mentions `latest`, Terraform/OpenTofu version numbers, provider versions, new/deprecated resource arguments, backend behavior, moved/import blocks, module versions, provider security behavior, or registry modules not covered locally.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, forums, and community blogs only to troubleshoot observed failures. Confirm HCL syntax, provider arguments, lifecycle behavior, and security recommendations against primary docs.
