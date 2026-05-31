# Modern Terraform Features, Version Awareness, and Generation Patterns

Read this reference when the task needs version-specific feature decisions, modern
Terraform syntax (1.8+), recurring generation patterns, or error triage. The main
`SKILL.md` keeps only the workflow; the depth lives here.

## Version awareness

Always consider version compatibility:

1. **Terraform version**
   - Use a `required_version` constraint with both lower and upper bounds.
   - Default to `>= 1.10, < 2.0` for modern features (ephemeral resources, write-only).
   - Use `>= 1.14, < 2.0` for the latest features (actions, query command).
   - Document any version-specific feature used (see matrix below).

2. **Provider versions (as of December 2025)**
   - AWS: `~> 6.0` (latest: v6.23.0)
   - Azure: `~> 4.0` (latest: v4.54.0)
   - GCP: `~> 7.0` (latest: v7.12.0) — 7.0 includes ephemeral resources & write-only attributes
   - Kubernetes: `~> 2.23`
   - Use `~>` for minor-version flexibility; pin major versions.
   - Re-check `references/source-map.md` before asserting any "latest" version.

3. **Module versions**
   - Always pin module versions.
   - Review module documentation for version compatibility.
   - Test module updates in non-production first.

### Terraform version feature matrix

| Feature | Minimum Version |
|---------|-----------------|
| `terraform_data` resource | 1.4+ |
| `import {}` blocks | 1.5+ |
| `check {}` blocks | 1.5+ |
| Native testing (`.tftest.hcl`) | 1.6+ |
| Test mocking | 1.7+ |
| `removed {}` blocks | 1.7+ |
| Provider-defined functions | 1.8+ |
| Cross-type refactoring | 1.8+ |
| Enhanced variable validations | 1.9+ |
| `templatestring` function | 1.9+ |
| Ephemeral resources | 1.10+ |
| Write-only arguments | 1.11+ |
| S3 native state locking | 1.11+ |
| Import blocks with `for_each` | 1.12+ |
| Actions block | 1.14+ |
| List resources (`tfquery.hcl`) | 1.14+ |
| `terraform query` command | 1.14+ |

## Modern Terraform features (1.8+)

### Provider-defined functions (Terraform 1.8+)

Provider-defined functions extend Terraform's built-in functions with provider-specific logic.

**Syntax:** `provider::<provider_name>::<function_name>(arguments)`

```hcl
# AWS Provider Functions (v5.40+)
locals {
  # Parse an ARN into components
  parsed_arn = provider::aws::arn_parse(aws_instance.web.arn)
  account_id = local.parsed_arn.account
  region     = local.parsed_arn.region

  # Build an ARN from components
  custom_arn = provider::aws::arn_build({
    partition = "aws"
    service   = "s3"
    region    = ""
    account   = ""
    resource  = "my-bucket/my-key"
  })
}

# Google Cloud Provider Functions (v5.23+)
locals {
  region = provider::google::region_from_zone(var.zone)  # "us-west1-a" -> "us-west1"
}

# Kubernetes Provider Functions (v2.28+)
locals {
  manifest_yaml = provider::kubernetes::manifest_encode(local.deployment_config)
}
```

### Ephemeral resources (Terraform 1.10+)

Ephemeral resources provide temporary values that are **never persisted** in state or
plan files. Critical for handling secrets securely.

```hcl
# Generate a password that never touches state
ephemeral "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Fetch secrets ephemerally from AWS Secrets Manager
ephemeral "aws_secretsmanager_secret_version" "api_key" {
  secret_id = aws_secretsmanager_secret.api_key.id
}

# Ephemeral variables (declare with ephemeral = true)
variable "temporary_token" {
  type      = string
  ephemeral = true
}

# Ephemeral outputs
output "session_token" {
  value     = ephemeral.aws_secretsmanager_secret_version.api_key.secret_string
  ephemeral = true
}
```

### Write-only arguments (Terraform 1.11+)

Write-only arguments accept ephemeral values and are never persisted. They use the
`_wo` suffix and require a version attribute.

```hcl
ephemeral "random_password" "db_password" {
  length = 16
}

resource "aws_db_instance" "main" {
  identifier        = "mydb"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  engine            = "postgres"
  username          = "admin"

  # Write-only password - never stored in state!
  password_wo         = ephemeral.random_password.db_password.result
  password_wo_version = 1  # Increment to trigger password rotation

  skip_final_snapshot = true
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id

  secret_string_wo         = ephemeral.random_password.db_password.result
  secret_string_wo_version = 1
}
```

### Enhanced variable validations (Terraform 1.9+)

Validation conditions can now reference other variables, data sources, and local values.

```hcl
data "aws_ec2_instance_type_offerings" "available" {
  filter {
    name   = "location"
    values = [var.availability_zone]
  }
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"

  validation {
    condition = contains(
      data.aws_ec2_instance_type_offerings.available.instance_types,
      var.instance_type
    )
    error_message = "Instance type ${var.instance_type} is not available in the selected AZ."
  }
}

variable "min_instances" {
  type    = number
  default = 1
}

variable "max_instances" {
  type    = number
  default = 10

  validation {
    condition     = var.max_instances >= var.min_instances
    error_message = "max_instances must be >= min_instances"
  }
}
```

### S3 native state locking (Terraform 1.11+)

S3 now supports native state locking without DynamoDB.

```hcl
terraform {
  backend "s3" {
    bucket  = "my-terraform-state"
    key     = "project/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true

    # S3-native locking (Terraform 1.11+)
    use_lockfile = true

    # DEPRECATED: DynamoDB locking (still works but no longer required)
    # dynamodb_table = "terraform-locks"
  }
}
```

### Import blocks (Terraform 1.5+)

Declarative resource imports without command-line operations.

```hcl
import {
  to = aws_instance.web
  id = "i-1234567890abcdef0"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  # ... configuration must match existing resource
}

import {
  for_each = var.existing_bucket_names
  to       = aws_s3_bucket.imported[each.key]
  id       = each.value
}
```

### Moved and removed blocks

Safely refactor resources without destroying them.

```hcl
moved {
  from = aws_instance.old_name
  to   = aws_instance.new_name
}

moved {
  from = aws_vpc.main
  to   = module.networking.aws_vpc.main
}

# Cross-type refactoring (1.8+)
moved {
  from = null_resource.example
  to   = terraform_data.example
}

# Remove resource from state without destroying (1.7+)
removed {
  from = aws_instance.legacy

  lifecycle {
    destroy = false
  }
}
```

### Import blocks with for_each (Terraform 1.12+)

```hcl
locals {
  buckets = {
    "staging" = "bucket1"
    "uat"     = "bucket2"
    "prod"    = "bucket3"
  }
}

import {
  for_each = local.buckets
  to       = aws_s3_bucket.this[each.key]
  id       = each.value
}

resource "aws_s3_bucket" "this" {
  for_each = local.buckets
}
```

### Actions block (Terraform 1.14+)

Actions enable provider-defined operations outside the standard CRUD model (Lambda
invocations, cache invalidations, database backups).

```hcl
action "aws_lambda_invoke" "process_data" {
  function_name = aws_lambda_function.processor.function_name
  payload       = jsonencode({ action = "process" })
}

action "aws_cloudfront_create_invalidation" "invalidate_cache" {
  distribution_id = aws_cloudfront_distribution.main.id
  paths           = ["/*"]
}
```

Trigger actions via a resource lifecycle `action_trigger`, or manually:

```bash
terraform apply -invoke action.aws_lambda_invoke.process_data
```

### List resources and query command (Terraform 1.14+)

```hcl
# my-resources.tfquery.hcl
list "aws_instance" "web_servers" {
  filter {
    name   = "tag:Environment"
    values = [var.environment]
  }
  include_resource = true
}
```

```bash
terraform query
terraform query -generate-config-out="import_config.tf"
terraform query -json
```

### Preconditions and postconditions (Terraform 1.5+)

```hcl
resource "aws_instance" "example" {
  instance_type = "t3.micro"
  ami           = data.aws_ami.example.id

  lifecycle {
    precondition {
      condition     = data.aws_ami.example.architecture == "x86_64"
      error_message = "The selected AMI must be for the x86_64 architecture."
    }
    postcondition {
      condition     = self.public_dns != ""
      error_message = "EC2 instance must be in a VPC that has public DNS hostnames enabled."
    }
  }
}
```

## Common generation patterns

### Pattern 1: Simple resource creation
"Create an AWS S3 bucket with versioning" -> `main.tf` (bucket + versioning),
`variables.tf` (name, tags), `outputs.tf` (ARN, name), `versions.tf` (provider pins).

### Pattern 2: Module-based infrastructure
"Set up a VPC using the official AWS VPC module" -> identify `terraform-aws-modules/vpc/aws`,
web-search the latest version + docs, generate with appropriate inputs, validate.

### Pattern 3: Multi-provider configuration
"Create infrastructure across AWS and Datadog" -> standard provider (AWS) + custom
provider (Datadog); web-search the Datadog provider docs with version; configure both,
add provider aliases if needed; validate.

### Pattern 4: Complex resource with dependencies
"Create an ECS cluster with ALB and auto-scaling" -> multiple resource blocks with
proper dependencies, data sources (AMIs, AZs), locals for computed config, comprehensive
variables/outputs, implicit-reference dependency management.

## Error handling

1. **Provider not found** — ensure the provider is in `required_providers`, verify the
   `namespace/name` source address, check the version-constraint syntax.
2. **Invalid resource arguments** — consult web-search results for custom providers,
   check required vs optional arguments, verify value types.
3. **Circular dependencies** — review references, use explicit `depends_on` if needed,
   consider splitting into modules.
4. **Validation failures** — run the `terraform-validator` skill for detailed errors,
   fix issues one at a time, re-validate after each fix.
