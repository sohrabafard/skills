# Sohrab Skills

This directory contains the Sohrab skill set for two main streams of work:

- Arvan-first infrastructure and platform delivery
- PHP / Laravel application engineering, including gateway-aware services

The goal is not just to generate code or config, but to keep outputs production-ready, consistent across projects, and aligned with the same operational rules, coding standards, and documentation expectations.

## Core precedence rules

### 1. Arvan-first platform policy
For ArvanCloud CaaS, the platform policy skill is:

- `caas-arvan-kuber`

If another infra, Kubernetes, Helm, Docker, or deployment skill conflicts with Arvan requirements, Arvan-first wins unless you explicitly request an override.

### 2. Gateway trust policy
For services that live behind the Ala gateway, the trust-boundary source of truth is:

- `alaa-trust-gateway-auth`

Use it for JWT-derived request identity, trusted headers, tenant context propagation, and downstream trust rules.

### 3. PHP / Laravel coding baseline
For PHP / Laravel code, the default coding baseline is:

- `alaa-php-clean-code`

Use it together with:

- `alaa-laravel-architecture` for layering, API contracts, `public_id`, and outbox-oriented application structure
- `alaa-data-layer` for schema, indexes, query shaping, concurrency, and Redis data primitives
- `alaa-octane-performance` for long-lived worker and hot-path safety
- `alaa-async-messaging` and `alaa-laravel-job-rabbitmq` for async, queue, retry, and DLQ design
- `alaa-security-review` for security review and auth or tenant-risk checks
- `alaa-observability-soc` for logs, metrics, traces, alerts, and Sentry
- `alaa-cicd-laravel-postgres` for CI quality gates, Pint, PHPStan, and tests
- `alaa-docs-farsi` for docs-alignment workflow, while keeping final docs in simple English when `alaa-php-clean-code` says so

## Default workflows

### Arvan-first infrastructure workflow
Use this order:

1. Generate a baseline with the relevant generator skill.
2. Apply Arvan-first constraints from `caas-arvan-kuber`.
3. Validate with the matching validator skill.
4. Iterate until the output is clean without breaking Arvan rules.
5. Ship operator-facing documentation and runbook material.

### PHP / Laravel service workflow
Use this order:

1. Inspect the repository and existing conventions.
2. Read `alaa-laravel-architecture` if the task changes module boundaries, contracts, or outbox rules.
3. Read `alaa-trust-gateway-auth` first if the service is behind the Ala gateway or trusted-header semantics are involved.
4. Apply `alaa-php-clean-code` as the default coding baseline.
5. Pull in specialist skills only where needed: data, async, Octane, security, observability, CI, docs.
6. Update tests and align documentation artifacts before considering the task done.

## Arvan-first rules summary

These constraints most often change the final output versus generic Kubernetes advice:

- Explicit resources are mandatory, and requests must equal limits, including `ephemeral-storage`
- Multi-document YAML is acceptable for Arvan panel paste flows
- Newer CPU generation scheduling may require node affinity
- HPA is the default fit for stateless workloads
- Stateful workloads need explicit, documented scaling rules
- Domain and ingress setup may require Arvan-specific prerequisites
- Config mounts should avoid shadowing busy directories
- Prefer namespace-scoped RBAC and avoid cluster-scope resources unless explicitly approved
- Prefer modern API versions, but stay compatible with actual cluster capabilities

## Current skill map

### Platform, runtime, and policy
- `caas-arvan-kuber`
- `haproxy-3.2`
- `alaa-docker-production`

### PHP / Laravel application engineering
- `alaa-laravel-architecture`
- `alaa-php-clean-code`
- `alaa-data-layer`
- `alaa-async-messaging`
- `alaa-laravel-job-rabbitmq`
- `alaa-octane-performance`
- `alaa-security-review`
- `alaa-observability-soc`
- `alaa-trust-gateway-auth`
- `alaa-cicd-laravel-postgres`
- `alaa-docs-farsi`
- `alaa-workflow`
- `alaa-mongodb-patterns`

### Kubernetes and Helm
- `helm-generator`
- `helm-validator`
- `k8s-yaml-generator`
- `k8s-yaml-validator`
- `k8s-debug`

### Docker and scripting
- `dockerfile-generator`
- `dockerfile-validator`
- `bash-script-generator`
- `bash-script-validator`
- `makefile-generator`
- `makefile-validator`

### CI / CD
- `gitlab-ci-generator`
- `gitlab-ci-validator`
- `github-actions-generator`
- `github-actions-validator`
- `jenkinsfile-generator`
- `jenkinsfile-validator`
- `azure-pipelines-generator`
- `azure-pipelines-validator`

### Infrastructure as code and automation
- `terraform-generator`
- `terraform-validator`
- `terragrunt-generator`
- `terragrunt-validator`
- `ansible-generator`
- `ansible-validator`

### Observability and logging
- `promql-generator`
- `promql-validator`
- `logql-generator`
- `loki-config-generator`
- `fluentbit-generator`
- `fluentbit-validator`

### Other specialized skills currently present
- `clickhouse-performance-schema-ops`
- `tusd-upload-platform`
- `vector-rust-observability-pipelines`

## Definition of done

Work is considered ready when the relevant rules are satisfied:

- Arvan constraints are respected where deployment touches ArvanCloud CaaS
- Gateway trust behavior is correct for services behind the Ala gateway
- PHP / Laravel code follows the shared architecture and clean-code baseline
- Validation and quality gates for the changed area have been run when available
- Documentation is aligned with the implementation
- No stale or duplicate docs remain for the changed behavior

For PHP / Laravel work, documentation alignment includes:

- English docblocks where they add type clarity or explain non-obvious behavior
- updated README or docs pages when behavior or setup changed
- Postman collection v2.1 kept current, with one request item per operation and multiple saved responses on that same item
- a separate environment file stored next to the Postman collection when needed
- updated request-flow diagrams, preferably in Mermaid

## Practical note

When a generic best practice conflicts with Arvan platform constraints or the Ala gateway trust model, document the reason for the deviation instead of hiding it.

## Reusable Prompt For Any PHP / Laravel Project

```text
Inspect this PHP / Laravel project and refactor it in small, reviewable diffs so it aligns with the Sohrab skill set.
Use `alaa-laravel-architecture` for layering, contracts, `public_id`, and outbox boundaries;
use `alaa-php-clean-code` as the default coding baseline for clean code, SOLID, design-pattern selection, type safety, modern PHP 8.x, PSR/PER, Laravel best practices, documentation quality, and efficient agent workflow;
use specialist skills only where the code actually enters their scope, including `alaa-data-layer`, `alaa-octane-performance`, `alaa-async-messaging`, `alaa-laravel-job-rabbitmq`, `alaa-security-review`, `alaa-observability-soc`, `alaa-cicd-laravel-postgres`, `alaa-docs-farsi`, and `alaa-trust-gateway-auth`.
Preserve behavior unless a bug, security issue, or explicit requirement justifies change.
Remove weak or duplicate abstractions, prefer explicit types and clear boundaries, keep controllers thin,
keep side effects at the edges, and avoid generic repositories or factories unless they add real value.
After code changes, align docblocks, README/docs, Postman collection v2.1, environment artifacts, and request-flow diagrams so nothing stale or duplicated remains.
Finish with a concise report of what changed, what was validated, what still carries risk, and any follow-up work that is still needed.
```
