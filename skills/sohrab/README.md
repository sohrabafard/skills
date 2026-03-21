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

Current target baseline for new work and refactors:
- PHP 8.5
- Laravel 13

Use it together with:

- `alaa-laravel-architecture` for layering, API contracts, `public_id`, and outbox-oriented application structure
- `alaa-data-layer` for schema, indexes, query shaping, concurrency, and Redis data primitives
- `alaa-octane-performance` for long-lived worker and hot-path safety
- `alaa-async-messaging` and `alaa-laravel-job-rabbitmq` for async, queue, retry, and DLQ design
- `alaa-security-review` for security review and auth or tenant-risk checks
- `alaa-observability-soc` for logs, metrics, traces, alerts, and Sentry
- `alaa-cicd-laravel-postgres` for CI quality gates, Pint, PHPStan, and tests
- `alaa-docs-farsi` for docs-alignment workflow, while keeping final docs in simple English when `alaa-php-clean-code` says so
- `openai-docs` when docs, examples, or integration notes touch OpenAI APIs, models, prompts, tools, or agent workflows and need current official references or citations
- `alaa-workflow` for non-trivial, multi-file, behavior-changing, or whole-project tasks

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
2. For non-trivial, multi-file, behavior-changing, or whole-project work, read `alaa-workflow` first and establish the plan artifact it requires.
3. Read `alaa-laravel-architecture` if the task changes module boundaries, contracts, or outbox rules.
4. Read `alaa-trust-gateway-auth` first if the service is behind the Ala gateway or trusted-header semantics are involved.
5. Apply `alaa-php-clean-code` as the default coding baseline.
6. Pull in specialist skills only where needed: data, async, Octane, security, observability, CI, docs, and OpenAI docs.
7. Update tests and align documentation artifacts before considering the task done.

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

## Reusable prompts for `alaa-php-clean-code`

### 1) Scoped work or new slice, with soft refactor

```text
Inspect this PHP / Laravel project and implement or refactor only the requested slice using `alaa-php-clean-code` in `scoped-soft` mode.
Target PHP 8.5 and Laravel 13 conventions where the repository supports them.
For Laravel 12 -> 13 upgrades or post-upgrade refactors, explicitly audit `PreventRequestForgery`, `cache.serializable_classes`, cache or session naming fallbacks, queue event payload changes, domain route precedence, and custom morph pivot table names where relevant.
Keep the touched slice fully aligned with clean-code, naming, SOLID, explicit types, modern PHP, PSR/PER, and Laravel best practices.
Preserve repo-local conventions unless they directly block clarity, and refactor adjacent code only as far as needed to keep behavior safe and the local design coherent.
If the task is non-trivial, multi-file, or behavior-changing, use `alaa-workflow` first.
Use `alaa-laravel-architecture` if the task changes module boundaries, DTO boundaries, `public_id`, API contracts, or outbox behavior.
Use `alaa-trust-gateway-auth` if the code touches Ala gateway trust, tenant derivation, trusted headers, or downstream auth context.
Use specialist skills only when the code actually enters their scope, including `alaa-data-layer`, `alaa-octane-performance`, `alaa-async-messaging`, `alaa-laravel-job-rabbitmq`, `alaa-security-review`, `alaa-observability-soc`, `alaa-cicd-laravel-postgres`, `alaa-docs-farsi`, and `alaa-mongodb-patterns`.
Use `openai-docs` when docs, examples, or integration notes touch OpenAI APIs, models, prompts, tools, or agent workflows and need current official references or citations.
Do not introduce generic repositories, managers, helpers, or factories unless they add real value.
After the code changes, update the nearest tests and align any impacted docblocks, README/docs, Postman collection v2.1, environment artifacts, and request-flow diagrams.
Finish with a concise audit showing the selected mode, governing skills used, contract-preservation status, validations run, documentation status, and remaining risks.
```

### 2) Scoped work, with hard refactor but preserved API contracts

```text
Inspect this PHP / Laravel project and refactor the requested slice using `alaa-php-clean-code` in `scoped-hard-contract-preserving` mode.
Target PHP 8.5 and Laravel 13 conventions where the repository supports them.
For Laravel 12 -> 13 upgrades or post-upgrade refactors, explicitly audit `PreventRequestForgery`, `cache.serializable_classes`, cache or session naming fallbacks, queue event payload changes, domain route precedence, and custom morph pivot table names where relevant.
Perform a serious internal cleanup of the selected area: improve naming, remove weak abstractions, extract DTOs/value objects/strategies/services/repositories only where they buy clarity, and make the code look like it was written by one careful author.
Preserve external and public contracts by default, including routes, request and response fields, response envelopes, status codes, event names and payloads, queue payloads, env var names, and any other documented integration surface, unless I explicitly authorize a breaking change.
If the task is non-trivial or multi-file, use `alaa-workflow` first.
Use `alaa-laravel-architecture` before changing layer flow, DTO boundaries, `public_id`, API contracts, or outbox behavior.
Use `alaa-trust-gateway-auth` before touching Ala gateway trust, tenant context derivation, trusted headers, request identity, step-up auth, or downstream auth propagation.
Use specialist skills only when the task enters their scope, including `alaa-data-layer`, `alaa-octane-performance`, `alaa-async-messaging`, `alaa-laravel-job-rabbitmq`, `alaa-security-review`, `alaa-observability-soc`, `alaa-cicd-laravel-postgres`, `alaa-docs-farsi`, and `alaa-mongodb-patterns`.
Use `openai-docs` when docs, examples, or integration notes touch OpenAI APIs, models, prompts, tools, or agent workflows and need current official references or citations.
Keep diffs reviewable, add or update regression tests where feasible, and align all impacted docs artifacts before considering the work done.
Finish with a concise audit showing the selected mode, governing skills used, preserved contracts, intentional exceptions, validations run, documentation status, and remaining risks.
```

### 3) Whole-project refactor, preserving repo-local conventions

```text
Inspect this entire PHP / Laravel repository and refactor it using `alaa-php-clean-code` in `whole-project-preserve-local` mode.
Use `alaa-workflow` first and execute the work in phased, reviewable batches.
Target PHP 8.5 and Laravel 13 conventions where the repository supports them, but preserve the repository's own established naming and layering dialect unless a convention is clearly broken or inconsistent.
For Laravel 12 -> 13 upgrades or post-upgrade refactors, explicitly audit `PreventRequestForgery`, `cache.serializable_classes`, cache or session naming fallbacks, queue event payload changes, domain route precedence, and custom morph pivot table names where relevant.
Make the whole codebase cleaner and more consistent: tighten naming, remove duplication, improve explicit types, reduce vague abstractions, strengthen DTO/value-object boundaries where they are clearly helpful, and standardize local conventions so the repository feels like it was written by one author.
Do not force a foreign naming system onto the project in this mode.
Use `alaa-laravel-architecture` for module boundaries, contracts, `public_id`, DTO boundaries, and outbox rules.
Use `alaa-trust-gateway-auth` for any gateway-trust, tenant-context, or downstream-auth surfaces.
Use specialist skills only where their scope is truly entered, including `alaa-data-layer`, `alaa-octane-performance`, `alaa-async-messaging`, `alaa-laravel-job-rabbitmq`, `alaa-security-review`, `alaa-observability-soc`, `alaa-cicd-laravel-postgres`, `alaa-docs-farsi`, and `alaa-mongodb-patterns`.
Use `openai-docs` when docs, examples, or integration notes touch OpenAI APIs, models, prompts, tools, or agent workflows and need current official references or citations.
Preserve public contracts by default unless I explicitly approve broader changes.
Keep tests, docblocks, README/docs, Postman collection v2.1, environment artifacts, and request-flow diagrams aligned with the implementation throughout the refactor.
Finish with a concise audit showing the selected mode, governing skills used, preserved contracts, validations run, documentation status, remaining risks, and follow-up phases if needed.
```

### 4) Whole-project refactor, normalizing to the global Alaa convention set

```text
Inspect this entire PHP / Laravel repository and refactor it using `alaa-php-clean-code` in `whole-project-normalize-alaa` mode.
Use `alaa-workflow` first and execute the refactor in phased, reviewable batches.
Target PHP 8.5 and Laravel 13 conventions where the repository supports them, and actively normalize the codebase toward one global Alaa convention set so the repository feels aligned with other Alaa-style projects.
For Laravel 12 -> 13 upgrades or post-upgrade refactors, explicitly audit `PreventRequestForgery`, `cache.serializable_classes`, cache or session naming fallbacks, queue event payload changes, domain route precedence, and custom morph pivot table names where relevant.
Use `alaa-laravel-architecture` as the structural source of truth for layer flow, DTO boundaries, `public_id`, API envelopes, and outbox behavior.
Normalize naming, folder intent, and code shape across the repo: remove vague helpers/managers/base repositories, prefer explicit DTOs and value objects where they clarify boundaries, standardize service/repository/resource/policy/request roles, and make repeated feature slices structurally consistent.
Preserve external and public contracts by default unless I explicitly authorize broader changes.
Use `alaa-trust-gateway-auth` for any gateway-trust, tenant-context, or downstream-auth surfaces.
Use specialist skills only where their scope is truly entered, including `alaa-data-layer`, `alaa-octane-performance`, `alaa-async-messaging`, `alaa-laravel-job-rabbitmq`, `alaa-security-review`, `alaa-observability-soc`, `alaa-cicd-laravel-postgres`, `alaa-docs-farsi`, and `alaa-mongodb-patterns`.
Use `openai-docs` when docs, examples, or integration notes touch OpenAI APIs, models, prompts, tools, or agent workflows and need current official references or citations.
Keep tests, docblocks, README/docs, Postman collection v2.1, environment artifacts, and request-flow diagrams aligned with the implementation throughout the refactor.
Finish with a concise audit showing the selected mode, governing skills used, preserved contracts, intentional exceptions, validations run, documentation status, remaining risks, and follow-up phases if needed.
```
