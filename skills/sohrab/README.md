# Sohrab Skills

This pack is a public installable skill set for production-oriented coding agents.

It now contains:

- 54 original skills from the `sohrab` pack
- 3 new portable companion skills:
  - `alaa-frontend-devops`
  - `alaa-frontend-doc-annotations`
  - `alaa-mono-package`

The pack is designed around simple routing-first skill entrypoints:

- `SKILL.md` stays short and easy to scan
- large rulebooks move into `references/` or existing `docs/` folders
- `agents/openai.yaml` exists for every skill
- generator and validator skills stay explicit and opt-in
- domain skills are easier to discover and route automatically

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
- `$frontend-skill`
  - for visually ambitious or art-direction-heavy frontend work
- `$playwright`
  - for explicit browser automation, navigation, or browser-based QA
- `$playwright-interactive`
  - for persistent browser debugging loops when the task explicitly needs interactive browser work

System-level skills are helper dependencies. They are not replaced by pack-local skills, and they are not required for every task.

## Default workflows

### Frontend workflow

1. Start with `alaa-frontend-developer`.
2. Route immediately to `alaa-frontend-devops`, `alaa-frontend-doc-annotations`, or `alaa-mono-package` when the task crosses that boundary.
3. Pair with `quasar-skill-packe` when Quasar-specific behavior or config is part of the root cause.
4. Use `$frontend-skill` only for strong visual design work.
5. Use `$playwright` or `$playwright-interactive` only when browser work is explicitly needed.

### PHP / Laravel workflow

1. Inspect the repository and existing conventions.
2. Use `alaa-workflow` for non-trivial, multi-file, risky, or long tasks.
3. Read `alaa-trust-gateway-auth` first when trusted headers, tenant derivation, or gateway auth semantics are involved.
4. Apply `alaa-php-clean-code` as the default coding baseline.
5. Pull in specialist skills only where the task actually enters their scope.
6. Keep docs, tests, and operational notes aligned before treating the work as done.

### Infra and platform workflow

1. Generate with the smallest relevant generator skill.
2. Apply platform policy from `caas-arvan-kuber`, `alaa-haproxy`, or `alaa-docker-production` as needed.
3. Validate with the matching validator skill.
4. Keep operator-facing notes and rollback expectations aligned with the final output.

## Current skill map

### Frontend and frontend delivery

- `alaa-frontend-developer`
- `alaa-frontend-devops`
- `alaa-frontend-doc-annotations`
- `alaa-mono-package`
- `quasar-skill-packe`
- `alaa-shaka-player`

### PHP / Laravel and application policy

- `alaa-php-clean-code`
- `alaa-laravel-architecture`
- `alaa-data-layer`
- `alaa-async-messaging`
- `alaa-laravel-job-rabbitmq`
- `alaa-octane-performance`
- `alaa-security-review`
- `alaa-observability-soc`
- `alaa-trust-gateway-auth`
- `alaa-cicd-laravel-postgres`
- `alaa-docs-farsi`
- `alaa-mongodb-patterns`
- `alaa-workflow`
- `clickhouse-performance-schema-ops`

### Platform, gateway, and delivery

- `caas-arvan-kuber`
- `alaa-haproxy`
- `alaa-docker-production`
- `tusd-upload-platform`
- `vector-rust-observability-pipelines`

### Kubernetes and Helm

- `helm-generator`
- `helm-validator`
- `k8s-yaml-generator`
- `k8s-yaml-validator`
- `k8s-debug`

### Docker, shell, and build files

- `dockerfile-generator`
- `dockerfile-validator`
- `bash-script-generator`
- `bash-script-validator`
- `makefile-generator`
- `makefile-validator`

### CI / CD

- `azure-pipelines-generator`
- `azure-pipelines-validator`
- `github-actions-generator`
- `github-actions-validator`
- `gitlab-ci-generator`
- `gitlab-ci-validator`
- `jenkinsfile-generator`
- `jenkinsfile-validator`

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

### Internal helper

- `alaa-low-noise`

## Definition of done

Work in this pack is considered ready when:

- the smallest correct skill is easy to discover from `SKILL.md`
- detailed guidance is preserved in one-hop `references/` or `docs/` files
- `agents/openai.yaml` exists and matches the current skill intent
- old project-local donor skill names are no longer required inside this pack
- examples, checklists, and anti-patterns are preserved in simple English
- system-level helpers are clearly separated from pack-local skills

## Practical note

When a generic best practice conflicts with the Ala gateway trust model, Arvan platform rules, or the frontend artifact contract, document the reason for the deviation instead of hiding it.

## Routing delta notes

- No skill names changed in this enrichment pass.
- Top-level `SKILL.md` files now bias toward routing-first entrypoints and companion-skill delegation instead of duplicating deeper references.
- When a responsibility narrowed, the skill now points to the owning companion skill instead of repeating that companion's full rulebook.
- Fast-entry routers, checklists, and diagnostic maps were added where they improve branch selection speed for agents.
