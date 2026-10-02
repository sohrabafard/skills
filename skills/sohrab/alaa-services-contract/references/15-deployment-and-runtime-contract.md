# Deployment and Runtime Contract

Use this file when the task touches how an Ala service is deployed, discovered, bootstrapped, or supplied with runtime infrastructure.

This file is Ala-specific and normative. Before creating or choosing a shared image, chart, CI include, generator, hook pack, or shared script, read `16-infrastructure-services-and-delivery-artifacts.md` first; it owns the registry of what already exists. Use `$alaa-docker-production` for generic Docker engineering details, `$alaa-k8s-helm` for chart and manifest mechanics, and `$caas-arvan-kuber` for Arvan CaaS platform facts.

## Ownership split

Rules:
- treat Kubernetes/OpenShift, released only from the `deploy` repository, as the only Ala production path; the current target is one offline OpenShift namespace
- treat Docker Compose and Docker Swarm as supported Ala runtime modes that must still satisfy the same service contract; whether either becomes a production target is undecided (`16-infrastructure-services-and-delivery-artifacts.md`)
- load `$alaa-k8s-helm` for Helm, values layering, OCI chart delivery, and rollout mechanics, `$alaa-gitlab-ci-cd` for pipeline mechanics, and `$caas-arvan-kuber` for a fact that differs on Arvan CaaS
- load `$alaa-docker-production` for Dockerfile hardening, runtime-user rules, Compose and Swarm delivery mechanics, and registry-plumbing details
- do not duplicate Kubernetes implementation detail in this file when the concern is already owned by `$alaa-k8s-helm` or `$caas-arvan-kuber`

## GitLab CI/CD baseline contract

Rules:
- for every Ala service image, default to the shared `service-ci-kit` project for GitLab CI/CD: Laravel and PHP services include its PHP pipeline, other services its stack-neutral contract-and-handoff include (`16-infrastructure-services-and-delivery-artifacts.md` names both)
- keep `.gitlab-ci.yml` as a thin include-based wrapper and pin the kit only through the include `ref:`; do not set `SERVICE_CI_KIT_REF` in a wrapper
- keep shared CI logic in `service-ci-kit`; do not copy shared `ci/scripts/*` trees or local semantic-release helper trees into service repositories
- keep only these CI inputs in the app repo: `.gitlab-ci.yml`, `.releaserc.json`, `deploy/service.yaml`, and a `Dockerfile` (with a `runtime` target for the PHP pipeline); a service repository holds no releasable chart, release values, deploy job, or cluster credential, because deployment lives only in the `deploy` repository (the gateway's render-only `charts/gateway` is image content)
- when shared CI behavior must change, update `service-ci-kit` first, release a new kit tag, and then bump the include `ref:` in service repositories
- load `$alaa-gitlab-ci-cd` for GitLab authoring, validation, and debugging, but keep the Ala fleet policy in this skill instead of moving it into the generic GitLab skill
- if a repository cannot use `service-ci-kit`, report the blocker explicitly instead of silently reintroducing a repo-owned pipeline

## Required deployment modes

Normalized Ala deployment modes:

| Mode                 | Status in the Ala contract | Primary use                                                    |
|----------------------|----------------------------|----------------------------------------------------------------|
| Kubernetes/OpenShift | only production path       | release from `deploy` with the image-embedded service contract |
| Docker Compose       | supported Ala runtime mode | single-host local, validation, or operator-managed runtime     |
| Docker Swarm         | supported Ala runtime mode | multi-node Docker runtime; production use undecided            |

Which project owns each delivery step, and the current state of a Compose or Swarm production target for the
gateway, live in `16-infrastructure-services-and-delivery-artifacts.md`.

Rules:
- new or refactored Ala services must ship `deploy/service.yaml` for the Kubernetes/OpenShift path and document both Docker paths, Compose and Swarm
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

#### Kubernetes/OpenShift

Rules:
- PostgreSQL, Redis, RabbitMQ, and the OTel Collector are external inputs of a release; the organization creates the database, role, and RabbitMQ vhost (deploy EO-03, EO-05), and no release creates a Postgres
- the operator grants privileges with the deploy script `<repo>/scripts/db-ensure-privileges.sh` (idempotent), once per service after the database and role exist and before the first apply
- keep the app runtime tuple explicit: the database defaults come from the service contract and the credentials from the service's runtime Secret

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
- in Kubernetes/OpenShift external mode, the service's runtime Secret and its contract's database defaults supply the full app tuple from an operator-managed external database
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
`postgres://…@postgres:5432/<db>`, `clickhouse:9000`). When a service deploys to Kubernetes/OpenShift instead, the
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
- in Kubernetes/OpenShift, reference pre-existing per-service Secrets by name; the operator creates them with the deploy script `<repo>/scripts/sync-openshift-secret.sh` (flow B in `16-infrastructure-services-and-delivery-artifacts.md`), and a release fails clearly when a required Secret or key is absent
- in Docker Compose and Docker Swarm, let wrapper scripts generate, synchronize, or provision the runtime secret material before bringing services up
- auth owns its own App key and Passport private and public key pair
- gateway may consume only the auth public key required to verify access tokens
- in Docker runtimes, synchronize the gateway copy of the auth public key automatically instead of relying on manual operator copying
- in Swarm, prefer external secrets with explicit `uid`, `gid`, and restrictive file `mode`

## Registry contract

Rules:
- pull and push every image and OCI artifact, first-party or public upstream, only through internal Nexus; there is no public-registry fallback, and an image missing from Nexus is an import task (Nexus entry in `16-infrastructure-services-and-delivery-artifacts.md`)
- treat the Nexus-only rule as mandatory for every image in Ala repositories, including CI helper images, validation images, OpenFGA runtime or CLI images, and Dockerfile base images
- take the registry address from `DOCKER_REGISTRY`; in Ala GitLab pipelines use `MAIN_DOCKER_REGISTRY` with `MAIN_DOCKER_REGISTRY_USER` and `MAIN_DOCKER_REGISTRY_PASS`
- the image pull Secret is a deploy input: `MAIN_IMAGE_PULL_SECRET_NAME` is optional with an empty default (whether Nexus needs one is deploy EO-07); a service repository sets no pull Secret
- keep registry credentials explicit in CI and runtime configuration; whether cluster pulls need a Secret is deploy EO-07
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
- no `deploy/service.yaml` for the Kubernetes/OpenShift production path
- no Compose or no Swarm story and no explicit blocker
- no shared `service-ci-kit` baseline for an Ala service image
- a releasable chart, release values, deploy job, or cluster credential in a service repository
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
- direct public-registry pulls instead of internal Nexus
- no private-registry story for first-party images or OCI artifacts
- no SQLite fast-test path for a new Laravel service and no documented blocker
