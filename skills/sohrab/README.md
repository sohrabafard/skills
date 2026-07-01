# Sohrab Skills

This pack is a public installable skill set for production-oriented coding agents.

The current pack mixes two patterns on purpose:

- routing-first umbrella skills where one entrypoint owns a full surface
- explicit generator/validator pairs where the narrow artifact workflow is still useful

## Pack design rules

- `SKILL.md` stays short and easy to scan
- large rulebooks move into `references/` or existing `docs/` folders
- `agents/openai.yaml` exists for every shipped skill
- mature surfaces prefer one routing-first owner instead of many tiny near-duplicates
- companion skills stay explicit where ownership boundaries still matter

## Core precedence rules

### 1. Arvan-first platform policy

If an infrastructure, Kubernetes, Helm, or deployment task targets ArvanCloud CaaS, the pack-level source of truth is:

- `caas-arvan-kuber`

If generic infra advice conflicts with Arvan constraints, Arvan-first wins unless the user explicitly approves an override.

### 2. Gateway trust policy

If a service lives behind the Ala gateway, the trust-boundary source of truth is:

- `alaa-trust-gateway-auth`

Use it for:

- JWT-derived identity
- trusted header rules
- tenant and project boundary propagation
- downstream service trust decisions
- auth-service route and error-contract guidance

### 3. Frontend family policy

For the standard Vue 3 + Quasar + Vite app family, start with:

- `alaa-frontend-developer`

Apply the default Vue / TypeScript quality baseline whenever coding, review, or refactor touches Vue SFCs, composables, Pinia stores, frontend TypeScript, or package-grade Vue APIs:

- `alaa-vue-typescript-clean-code`

Then route to the smallest companion skill that owns the next decision:

- build, deployment, Docker, CI, artifact, public-path, CDN, or proxy concerns:
  - `alaa-frontend-devops`
- documentation-only JSDoc or inline-comment work:
  - `alaa-frontend-doc-annotations`
- workspace package, `packages/*`, peer dependency, or asset-emission issues:
  - `alaa-mono-package`
- Quasar CLI, `quasar.config`, mode-specific, or Quasar upgrade details:
  - `quasar-skill-packe`

### 4. PHP / Laravel coding baseline

For PHP / Laravel work, the default coding baseline is:

- `alaa-php-clean-code`

Use it together with the smallest relevant companion skills:

- `alaa-laravel-architecture`
- `alaa-data-layer`
- `alaa-async-messaging`
- `alaa-laravel-job-rabbitmq`
- `alaa-octane-performance`
- `alaa-security-review`
- `alaa-observability-soc`
- `alaa-cicd-laravel-postgres`
- `alaa-docs-farsi`
- `alaa-mongodb-patterns`
- `alaa-trust-gateway-auth`
- `alaa-workflow`

## Pack-local vs system-level dependencies

The skills in this pack may reference system-level skills, but those are not part of the pack itself.

### Pack-local skills

These ship with the `sohrab` pack and should be treated as the portable public install surface.

### System-level skills

These may still be referenced when a task needs them:

- `$openai-docs`
  - for current official OpenAI and Codex guidance, citations, model guidance, prompt updates, CLI or app behavior
- `$playwright`
  - for explicit browser automation, navigation, or browser-based QA
- `$playwright-interactive`
  - for persistent browser debugging loops when the task explicitly needs interactive browser work

System-level skills are helper dependencies. They are not replaced by pack-local skills, and they are not required for every task.

## Default workflows

### Frontend workflow

1. Start with `alaa-frontend-developer`.
2. Apply `alaa-vue-typescript-clean-code` for Vue / TypeScript coding, review, refactor, or package-quality decisions.
3. Route immediately to `alaa-frontend-devops`, `alaa-frontend-doc-annotations`, or `alaa-mono-package` when the task crosses that boundary.
4. Pair with `quasar-skill-packe` when Quasar-specific behavior or config is part of the root cause.
5. Keep pure visual art direction outside the Sohrab pack unless a separate design skill is explicitly available in the current session.
6. Use `$playwright` or `$playwright-interactive` only when browser work is explicitly needed.

### PHP / Laravel workflow

1. Inspect the repository and existing conventions.
2. Use `alaa-workflow` for non-trivial, multi-file, risky, or long tasks.
3. Read `alaa-trust-gateway-auth` first when trusted headers, tenant derivation, or gateway auth semantics are involved.
4. Apply `alaa-php-clean-code` as the default coding baseline.
5. Pull in specialist skills only where the task actually enters their scope.
6. Keep docs, tests, and operational notes aligned before treating the work as done.

### Infra and delivery workflow

1. Start with the routing-first owner when one exists:
   - `alaa-k8s-helm`
   - `alaa-gitlab-ci-cd`
   - `alaa-bash-shell`
   - `alaa-makefile`
   - `alaa-docker-production`
2. Apply platform policy from `caas-arvan-kuber`, `alaa-haproxy`, or service-specific companion skills as needed.
3. Use explicit generator/validator pairs only on surfaces that still keep that split.
4. Keep operator-facing notes and rollback expectations aligned with the final output.

## Current skill map

### Core Ala architecture and policy

- `alaa-workflow`
- `alaa-prompting-guide`
- `alaa-low-noise`
- `alaa-services-contract`
- `alaa-trust-gateway-auth`
- `alaa-security-review`
- `alaa-observability-soc`
- `alaa-docs-farsi`
- `alaa-postman-collections`
- `alaa-crockford-base32-codecs`

### PHP / Laravel and service engineering

- `alaa-php-clean-code`
- `alaa-laravel-architecture`
- `alaa-data-layer`
- `alaa-async-messaging`
- `alaa-laravel-job-rabbitmq`
- `alaa-octane-performance`
- `alaa-cicd-laravel-postgres`
- `alaa-mongodb-patterns`
- `service-runtime-kit-governance`
- `alaa-laravel-public-api-contract-pack`

### Frontend and frontend delivery

- `alaa-frontend-developer`
- `alaa-vue-typescript-clean-code`
- `alaa-frontend-devops`
- `alaa-frontend-doc-annotations`
- `alaa-mono-package`
- `quasar-skill-packe`
- `alaa-shaka-player`

### Go and specialized app platforms

- `alaa-golang`
- `jitsi-platform-architect`

### Containers, CI/CD, Kubernetes, and platform delivery

- `alaa-docker-production`
- `alaa-gitlab-ci-cd`
- `alaa-k8s-helm`
- `alaa-haproxy`
- `caas-arvan-kuber`
- `tusd-upload-platform`
- `vector-rust-observability-pipelines`

### Build files, shell, and local automation

- `alaa-bash-shell`
- `alaa-makefile`

### Artifact-specific CI, IaC, and automation skills

- `ansible-generator`
- `ansible-validator`
- `azure-pipelines-generator`
- `azure-pipelines-validator`
- `fluentbit-generator`
- `fluentbit-validator`
- `github-actions-generator`
- `github-actions-validator`
- `jenkinsfile-generator`
- `jenkinsfile-validator`
- `terraform-generator`
- `terraform-validator`
- `terragrunt-generator`
- `terragrunt-validator`

### Observability queries and logging configuration

- `promql-generator`
- `promql-validator`
- `logql-generator`
- `loki-config-generator`

### Data platform and storage-specialized skills

- `clickhouse-performance-schema-ops`

## Recently consolidated or removed from this pack

These older skill folders are no longer part of the active pack surface:

- `dockerfile-generator`
- `dockerfile-validator`
- `makefile-generator`
- `makefile-validator`

Their active replacements are:

- `alaa-docker-production`
- `alaa-makefile`

## Definition of done

Work in this pack is considered ready when:

- the smallest correct skill is easy to discover from `SKILL.md`
- detailed guidance is preserved in one-hop `references/` or `docs/` files
- `agents/openai.yaml` exists and matches the current skill intent
- stale donor skill names are removed from active routing docs
- examples, checklists, and anti-patterns are preserved in simple English
- system-level helpers are clearly separated from pack-local skills

## Practical note

When a generic best practice conflicts with the Ala gateway trust model, Arvan platform rules, or the frontend artifact contract, document the reason for the deviation instead of hiding it.

## Routing delta notes

- Top-level `SKILL.md` files bias toward routing-first entrypoints and companion-skill delegation instead of duplicating deeper references.
- Some mature surfaces now use a single owner skill instead of separate generator/validator pairs.
- Where a responsibility narrowed, the skill points to the owning companion skill instead of repeating that companion's full rulebook.
- Fast-entry routers, checklists, and diagnostic maps are preferred when they reduce search and branch-selection time for agents.
