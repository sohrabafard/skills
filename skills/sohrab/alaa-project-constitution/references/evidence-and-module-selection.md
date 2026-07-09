# Evidence and Module Selection

Use this reference after reading the root template. Search narrowly, then read the smallest
set of files that can establish ownership, current behavior, and real validation commands.

## Evidence priority

1. Safe executable truth: routes, schemas, migrations, manifests, generated output, tests,
   CI definitions, task runners, and reproducible runtime inspection.
2. Maintained canonical contracts, ADRs, architecture/security docs, and runbooks.
3. Existing constitution and agent guidance.
4. Comments, task notes, memory, examples, and external guidance.

Absence from a limited search is not evidence of absence. Record `UNKNOWN` when the
inspection surface is incomplete.

Before module selection, inventory the constitutional corpus and choose `THIN_CHARTER` or
`FULL_CHARTER`. Mature `CONTRACTS.md`, governance, ADR, policy, generated-contract, and
upstream-framework sources normally require a thin charter that incorporates detail by
reference instead of copying it.

## High-signal inventory

| Domain | Common evidence |
|---|---|
| Instructions | `AGENTS.md`, `CLAUDE.md`, `.claude/**`, `.agents/**`, `.codex/**`, rules, skills |
| Identity/docs | `README*`, docs index, architecture docs, ADRs, governance, contracts, runbooks |
| Go | `go.mod`, `go.work`, `cmd/**`, `internal/**`, `pkg/**`, `*.go`, Go tests |
| PHP/Laravel | `composer.json`, `artisan`, `app/**`, `routes/**`, `config/**`, migrations, PHPUnit/Pest |
| Frontend | `package.json`, lockfiles, Vue/React/Quasar/Nuxt/Next/Vite configs, routes, stores, service workers, browser tests |
| APIs | route registration, OpenAPI, Postman, protobuf/GraphQL, resources/serializers, error contracts, SDK generation |
| Data | migrations, schema/SQL, ORM models, repositories, indexes, seeders, backfills, recovery scripts |
| Async | broker config, queue/topic declarations, jobs, consumers, outbox/inbox, schedulers, event schemas, DLQ tooling |
| Realtime | WebSocket/SSE servers and clients, heartbeat/reconnect logic, connection limits, auth refresh |
| Gateway/proxy | trusted-header middleware, route posture, HAProxy/nginx/APISIX/Envoy/Traefik/ingress configs, ACLs/maps |
| Cache/Redis | key builders, TTLs, invalidation, locks, sessions, rate limits, degraded-mode tests |
| Integrations | provider adapters/SDKs, callbacks, webhook verification, payment/SMS/email/storage contracts |
| Media/files | upload/download/storage, tus, signed URLs, Shaka/streaming/DRM, transcode jobs, cleanup |
| Search | Elasticsearch/OpenSearch/Meilisearch, projections, indexing, rebuild/replay/reconciliation |
| Infra/runtime | Dockerfiles, Compose, Helm/Kubernetes, Terraform/Ansible, CI/CD, deploy/render scripts, env templates |
| Observability | OpenTelemetry, Prometheus, SigNoz, Loki/Vector/Fluent Bit, Sentry, dashboards, alerts, health/readiness |
| Generated/docs | generators, templates, golden files, codegen, scaffold tests, OpenAPI/Postman/SDK artifacts |

## Classifying conditional modules

Use positive ownership evidence. A dependency name or optional environment variable alone
does not prove the repository owns the behavior.

| Module | Include when | Common false positive |
|---|---|---|
| `MONOREPO_PACKAGES_SDK_CLI` | multiple packages/apps, shared libraries, SDK/CLI/scaffold/public artifacts | vendored packages or examples only |
| `UPSTREAM_KIT_FRAMEWORK_CONTRACTS` | repository consumes a versioned kit/framework/SDK/scaffold/platform contract owned elsewhere | ordinary third-party library with no inherited project policy |
| `API_CONTRACTS` | repository owns API routes/shapes/errors/auth/versioning or generated clients | it only calls another service's API |
| `GO_CHI` | Go source/module/binaries; chi/net/http where relevant | Go tool used only during build |
| `LARAVEL_PHP_OCTANE` | PHP/Laravel application or library source | PHP script copied as utility |
| `FRONTEND_WEB_SSR_PWA` | browser app/SDK; retain SSR/PWA subsections only with evidence | static docs site assets only |
| `GATEWAY_PROXY_TRUST` | app trust boundary and/or actual proxy config; name owned side | trusted headers mentioned only in external docs |
| `DATA_MIGRATIONS` | owned persistent schema/access/migrations/index/backfill | transient test fixture only |
| `REDIS_CACHE_LOCKS` | owned cache/session/lock/rate-limit behavior | unused dependency/env example |
| `ASYNC_JOBS_EVENTS` | owned producer/consumer/job/outbox/scheduler/event behavior | synchronous webhook client only |
| `REALTIME_STREAMING` | owned WebSocket/SSE/streaming connection behavior | ordinary HTTP streaming download |
| `INTEGRATIONS_WEBHOOKS` | owned provider adapter or inbound/outbound webhook contract | generic HTTP client with no provider ownership |
| `MEDIA_FILES` | owned upload/download/storage/media/playback behavior | README images or test fixtures |
| `SEARCH_INDEXING` | owned search/index/projection/read-model behavior | database text search used incidentally |
| `INFRA_CI_RUNTIME` | repository owns build/deploy/runtime/CI config | docs merely describe another team's infra |
| `OBSERVABILITY_SOC` | repository owns telemetry schema/config/dashboard/alert/runbook | framework default logging only |
| `DOCS_GENERATED_AGENT_GUIDANCE` | repository owns docs, generators, goldens, runbooks, or agent guidance | no maintained project guidance/artifacts |

## Validation command discovery

Accept commands only when they are present in repository truth, such as:

- manifest scripts (`package.json`, `composer.json`, task definitions);
- `Makefile`, Taskfile, Justfile, scripts, CI steps, or maintained developer docs;
- framework-native test/build/lint commands already used by the project.

Do not invent a conventional command because it is common for the stack. If multiple
commands disagree, report drift and prefer the executable/CI-owned path after verification.

## Evidence ledger minimum

For each binding rule with project-specific facts, capture:

- claim or rule;
- canonical path and relevant section/symbol;
- what the evidence proves and what it does not prove;
- freshness or last verification date;
- confidence (`HIGH`, `MEDIUM`, `LOW`);
- drift/TODO when sources disagree.

Do not include secrets, raw logs, or personal/production data in the ledger.
