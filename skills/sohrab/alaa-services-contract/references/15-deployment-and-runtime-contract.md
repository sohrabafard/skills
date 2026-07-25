# Deployment and Runtime Contract

Use this file when the task touches how an Ala service is deployed, discovered, bootstrapped, or supplied with runtime infrastructure.

This file is Ala-specific and normative. Use `$alaa-docker-production` for generic Docker engineering details and `$caas-arvan-kuber` for the primary Arvan Kubernetes production path.

## Ownership split

Rules:
- treat Arvan Kubernetes as the primary production path for Ala services
- treat Docker Compose and Docker Swarm as supported Ala runtime modes that must still satisfy the same service contract
- load `$caas-arvan-kuber` for Helm, values layering, OCI chart delivery, cluster secrets, and GitLab rollout mechanics
- load `$alaa-docker-production` for Dockerfile hardening, runtime-user rules, Compose and Swarm delivery mechanics, and registry-plumbing details
- do not duplicate Kubernetes implementation detail in this file when the concern is already owned by `$caas-arvan-kuber`

## GitLab CI/CD baseline contract

Rules:
- for Ala Laravel backend services that follow the shared `platform-app-php` delivery model, default to the shared `service-ci-kit` project for GitLab CI/CD
- keep `.gitlab-ci.yml` as a thin include-based wrapper and pin an explicit `SERVICE_CI_KIT_REF`
- keep shared CI logic in `service-ci-kit`; do not copy shared `ci/scripts/*` trees or local semantic-release helper trees into service repositories
- keep only service-local CI assets in the app repo, such as `.gitlab-ci.yml`, `.releaserc.json`, `ci/helm/values.app.yaml`, `ci/helm/values.app.ops.yaml`, `ci/helm/values.app.hpa.yaml`, `ci/helm/values.ci.runtime.yaml`, and optional local overlays that the shared kit intentionally consumes
- when shared CI behavior must change, update `service-ci-kit` first, release a new kit ref, and then bump the pinned ref in service repositories
- load `$alaa-gitlab-ci-cd` for GitLab authoring, validation, and debugging, but keep the Ala fleet policy in this skill instead of moving it into the generic GitLab skill
- if a repository cannot use `service-ci-kit`, report the blocker explicitly instead of silently reintroducing a repo-owned pipeline

## Required deployment modes

Normalized Ala deployment modes:

| Mode             | Status in the Ala contract | Primary use                                                         |
|------------------|----------------------------|---------------------------------------------------------------------|
| Arvan Kubernetes | primary production path    | managed production rollout                                          |
| Docker Compose   | supported Ala runtime mode | single-host local, validation, or operator-managed runtime          |
| Docker Swarm     | supported Ala runtime mode | multi-node Docker runtime with production-capable service discovery |

Rules:
- new or refactored Ala services must document the Arvan Kubernetes path and both Docker paths, Compose and Swarm
- when a repository cannot support one of the Docker modes yet, report the blocker explicitly instead of silently omitting the mode
- prefer one wrapper entrypoint such as `scripts/docker/up-local.sh <compose|swarm>` or `dev|compose|swarm|prod` aliases when a repo exposes both modes
- keep mode names explicit in docs, scripts, and examples

## PostgreSQL source modes

Rules:
- choose the PostgreSQL source mode explicitly; do not auto-switch based on discovery
- keep the app runtime tuple explicit and stable: `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`
- keep bootstrap or admin connectivity separate from the app runtime tuple
- shared-mode bootstrap and external-mode provisioning must never be treated as permission to create a second runtime Postgres

### Mode 1 - Shared Ala Postgres

This mode uses the canonical Ala shared infra and canonical names.

Rules:
- when shared mode is selected, the service must target the canonical shared infra identity and canonical Postgres endpoint for that environment
- if the canonical shared infra already exists, the service must reuse it
- if the canonical shared infra already exists, the service must not create another Postgres, another infra project, or another shared-infra identity
- if the existing shared infra is unhealthy, unreachable, misnamed, or incompatible, fail fast and report the blocker explicitly
- only create shared infra when shared mode is explicitly selected, the canonical shared infra is absent, and the service owns a safe idempotent bootstrap path

#### Helm and Arvan Kubernetes shared mode

Rules:
- support the current Ala `infra-pipeline` model where runtime DB settings and bootstrap DB settings are provided through the shared platform flow
- keep the app runtime connection tuple explicit even when some values come from `infra-pipeline`-managed secrets or overlays
- keep app runtime DB host selection separate from `dbBootstrap.pgHost`
- do not require service-local chart logic to invent a second Postgres when `infra-pipeline`-managed shared Postgres is the selected mode

#### Docker Compose and Docker Swarm shared mode

Rules:
- in Docker shared mode, reuse the canonical shared infra project and canonical shared Postgres instead of creating a second service-local Postgres when shared infra already exists
- wrapper scripts may bootstrap the canonical shared infra only when it is absent and shared mode is explicitly selected
- wrapper scripts must fail fast on unhealthy or incompatible existing shared infra instead of auto-falling back to a new local Postgres

### Mode 2 - External Postgres

This mode is operator-selected explicitly.

Rules:
- use the explicit app runtime tuple `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, and `DB_PASSWORD`
- do not auto-switch into shared mode just because shared infra is discoverable
- do not create shared infra in external mode
- in Helm or Arvan Kubernetes external mode, allow runtime secrets or overlays to supply the full app tuple from an operator-managed external database
- in Docker Compose and Docker Swarm external mode, allow the app to connect directly to an external database without starting shared Postgres
- if the external database and user already exist, allow provisioning to be disabled

### Provisioning and admin separation

Rules:
- treat `DB_PROVISION_*` and equivalent bootstrap or admin credentials as a separate provisioning path, not as part of the app runtime tuple
- only use `DB_PROVISION_*` when the selected mode requires service-owned database or schema provisioning
- in external mode, `DB_PROVISION_*` may target the external server for one-time or idempotent provisioning, but that must not create or imply a second runtime Postgres
- in shared mode, `DB_PROVISION_*` may help provision the service-owned database, schema, user, or grants inside the canonical shared Postgres, but that must not create a second Postgres instance

## Shared Docker network contract

The canonical Ala shared Docker network is:
- `alaa-shared-network`

Rules:
- attach every Ala service that needs cross-repo Docker communication to `alaa-shared-network`
- create the shared network automatically when it does not exist
- do not require operators to create the network manually before first deploy
- keep cross-service Docker DNS on the shared network instead of inventing per-repo isolated networks when inter-service routing is required

## Shared Docker infra contract

The canonical Ala shared Docker infra identity is:
- `alaa-shared-infra`

Rules:
- if the canonical shared infra exists, must reuse it
- if the canonical shared infra exists, must not create a second shared-infra copy, another Postgres, or a renamed sibling infra project
- if the canonical shared infra exists but is unhealthy, unreachable, misnamed, or incompatible, fail fast and report the blocker explicitly
- only create the canonical shared infra when it is absent, shared mode is explicitly selected, and the service bootstrap owns a safe, idempotent creation path
- keep shared infra names stable across repos so services can discover the same Postgres, Redis, RabbitMQ, ClickHouse, or equivalent dependencies
- do not create a second copy of shared infra in shared mode

### Shared infra endpoints and reachability (verified 2026-07-19 — read this before claiming an infra service is missing)

Exact identity — there is no "alaa-infra-share" or "alaa-infra-network"; the only canonical names are:
- Compose project: `alaa-shared-infra` (env knob `DOCKER_SHARED_INFRA_PROJECT`)
- Docker network: `alaa-shared-network` (env knob `DOCKER_SHARED_NETWORK_NAME`)

In-network DNS aliases (containers attached to `alaa-shared-network` connect with these; never container names):

| Dependency | In-network endpoint | Host-published port (1-prefix rule) |
| --- | --- | --- |
| PostgreSQL | `postgres:5432` | `127.0.0.1:15432` |
| Redis | `redis:6379` | `127.0.0.1:16379` |
| RabbitMQ | `rabbitmq:5672` (mgmt `rabbitmq:15672` in-network) | `127.0.0.1:15672` |
| ClickHouse | `clickhouse:9000` or `shared-clickhouse:9000` (HTTP `:8123`) | `127.0.0.1:19000` (HTTP `127.0.0.1:18123`) |
| Adminer | `adminer:8080` | `127.0.0.1:9093` |

Owner standardization (2026-07-19): every shared-infra protocol port is host-published on `127.0.0.1` with a
**"1"-prefixed default** (5432→15432, 6379→16379, 5672→15672, 9000→19000, 8123→18123) through the generators'
`*_FORWARD_PORT` knobs. This skill owns the canonical names, the endpoint table, and the reuse-or-fail-fast
obligation; `$service-runtime-kit-governance` owns which generator variable carries each value and which kit
version ships it. Read that skill for the variable and version, and never pin a kit version in this file.
Two hard rules: (1) **services running in Docker always connect to the in-network aliases**, never the
host-published ports — those exist for host tools, local SDKs, and host-run tests; (2) destructive or
exact-assertion tests still use a disposable container, never the shared instance's data.

Environment philosophy (owner-finalized 2026-07-19): committed `.env` values and examples are written for the
**Docker deploy** — in-network aliases (`amqp://…@rabbitmq:5672/`, `redis://redis:6379/0`,
`postgres://…@postgres:5432/<db>`, `clickhouse:9000`). When a service deploys to Arvan Kubernetes instead, the
operator sets that environment's own endpoints (external managed infra hosts, or in-namespace service DNS) —
the env KEYS are the stable contract, the VALUES are deployment-environment-owned.

## Canonical service naming and Docker DNS contract

Rules:
- keep the top-level Compose or stack project name aligned with the service slug such as `auth`, `gateway`, `comment`, `ticket`, `vod`, or `wa`
- for PHP or Laravel HTTP entry services, expose the canonical internal app alias `<service>-platform-app-php`
- use the HTTP-serving app service, not workers, as the canonical backend alias
- make gateways, reverse proxies, and internal Docker callers target the canonical alias instead of replica container names or node IPs
- in Swarm, configure the canonical HTTP service with `endpoint_mode: vip` or an equivalent stable service-DNS behavior
- when a service is not PHP-based, expose one stable internal DNS name and document the equivalent canonical alias explicitly

## Gateway routing contract for Docker runtimes

Rules:
- in Docker Compose and Docker Swarm, gateway-side backend discovery uses direct DNS against the canonical backend alias
- do not couple gateway config to replica names, task IDs, or host IP lists
- keep gateway backend naming aligned with the service-owned canonical alias
- when a backend is not yet wired into the shared Docker runtime, document the gap instead of inventing alternate names

## Infra bootstrap and service-owned data contract

Rules:
- before app startup, ensure the required shared infra exists or can be reused safely
- keep infra bootstrap idempotent so repeated deploys converge instead of drift
- each service owns its own database, schema, user, grants, and bootstrap data inside the shared infra
- for PostgreSQL-backed services, provision a dedicated database and/or schema and service user, then apply the required grants idempotently
- in shared mode, do that provisioning inside the canonical shared Postgres instead of creating a new Postgres instance
- in external mode, provision against the explicit external server only when external provisioning is intentionally enabled
- do not treat app runtime credentials as bootstrap or admin credentials
- preserve the administrator or `postgres` maintenance path instead of narrowing infra access so far that emergency operations break
- for ClickHouse-backed services, create the service-local database, users, and DDL idempotently before assuming runtime readiness
- do not couple one service to another service's application schema or service-owned tables

## Secret and key material contract

Rules:
- never bake application secrets, App keys, Passport keys, or runtime credentials into images or committed files
- in Arvan Kubernetes, let the infra pipeline or chart-driven secret mounts provide the runtime secret material and follow `$caas-arvan-kuber`
- in Docker Compose and Docker Swarm, let wrapper scripts generate, synchronize, or provision the runtime secret material before bringing services up
- auth owns its own App key and Passport private and public key pair
- gateway may consume only the auth public key required to verify access tokens
- in Docker runtimes, synchronize the gateway copy of the auth public key automatically instead of relying on manual operator copying
- in Swarm, prefer external secrets with explicit `uid`, `gid`, and restrictive file `mode`

## Registry contract

Rules:
- route public upstream image pulls through a configurable pull-through mirror
- use `mirror.cdn.ir` as the normalized Ala default when the environment does not explicitly override the mirror
- treat the pull-through mirror rule as mandatory for all public upstream images in Ala repositories, including CI helper images, validation images, OpenFGA runtime or CLI images, and public Dockerfile base images
- for Ala GitLab pipelines, treat `MAIN_PUBLIC_DOCKER_REGISTRY_MIRROR` as the canonical public-mirror input variable
- normalize repo-local CI variables such as `PUBLIC_DOCKER_REGISTRY` from `MAIN_PUBLIC_DOCKER_REGISTRY_MIRROR` when a repository wants a shorter local alias, but do not invent direct-public fallback behavior in CI
- push and pull first-party images and OCI artifacts through the private registry path
- for Ala GitLab pipelines, keep first-party registry auth and OCI delivery on `MAIN_DOCKER_PRIVATE_REGISTRY`, `MAIN_DOCKER_PRIVATE_REGISTRY_USER`, and `MAIN_DOCKER_PRIVATE_REGISTRY_PASS`
- for Arvan Kubernetes image pulls, treat `MAIN_IMAGE_PULL_SECRET_NAME` as the canonical input for the namespace-local docker-registry secret name and wire it into the chart or manifest instead of assuming anonymous pulls
- keep registry credentials explicit in CI, runtime, and cluster configuration instead of relying on anonymous behavior
- do not hardcode direct Docker Hub pulls when the family mirror contract exists
- keep the repo-local environment variable names explicit in docs and CI, even when different repos choose slightly different variable names
- do not leave Kubernetes pull-secret values cosmetic; if a deploy script sets `image.pullSecrets` or an equivalent field, the chart or manifest must render that field into the pod spec

## Testing and validation contract

Rules:
- treat PostgreSQL and any service-required infra such as Redis, RabbitMQ, or ClickHouse as the production truth
- for Laravel services, also support fast tests and runtime validation on SQLite unless a documented blocker makes that impossible
- keep SQLite support as a test and validation acceleration path, not as a substitute for production readiness checks
- validate Docker configuration before deploy and fail fast on missing secrets, invalid Compose models, or missing bootstrap prerequisites
- keep service-level readiness checks aligned with the dependencies the service actually owns

## Review checklist

Flag a problem when you see:
- no documented Arvan Kubernetes production path
- no Compose or no Swarm story and no explicit blocker
- no shared `service-ci-kit` baseline for an Ala Laravel backend that follows the shared `platform-app-php` delivery model
- a non-thin `.gitlab-ci.yml` in a service repo that should use the shared kit
- shared `ci/scripts/*` or local semantic-release helper trees reintroduced into a service repo
- undocumented divergence from the shared kit baseline
- no explicit shared-versus-external Postgres mode selection
- no `alaa-shared-network` use where cross-service Docker routing is required
- no reuse or bootstrap path for `alaa-shared-infra`
- a service-local Postgres or sibling infra project being created while canonical shared infra already exists
- automatic fallback from shared mode to a new local Postgres
- implicit switching between shared and external Postgres modes
- `DB_PROVISION_*` or equivalent bootstrap credentials being treated as the app runtime tuple
- gateway or another proxy targeting replica names, task IDs, or host IPs instead of the canonical backend alias
- no canonical `<service>-platform-app-php` alias for a PHP or Laravel HTTP service and no documented equivalent
- secrets or keys copied manually instead of being generated, synchronized, or mounted by the deploy path
- direct public-registry pulls instead of the configured pull-through mirror
- no private-registry story for first-party images or OCI artifacts
- no SQLite fast-test path for a new Laravel service and no documented blocker
