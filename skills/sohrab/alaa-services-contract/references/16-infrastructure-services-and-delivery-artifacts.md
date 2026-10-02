# Infrastructure Services and Delivery Artifacts

Ala fleet only. Read this file before creating or choosing a container image, toolchain layer, chart, CI include
or template, generator, hook pack, or script meant for more than one repository or pipeline, and whenever a task
asks which project owns a delivery step, how the gateway's configuration is produced, or whether a Compose or
Swarm production target exists. It owns the registry of shared delivery artifacts, the check-before-creating
rule, project roles, delivery flows, and the gateway generation facts. Deployment modes, shared-infra reuse, and
the CI baseline rules stay in `15-deployment-and-runtime-contract.md`; the gateway prefix map and route
ownership stay in `25-end-to-end-flow-and-boundaries.md`.

Notation: `<repo>/<path>` is a path inside the repository named in the same row or sentence. This file carries
no version, tag, or digest; the owning repository's files are the live source for every pin, name, and status
(`90-source-map.md`). Entries were verified read-only on 2026-10-03.

When a sibling repository is not checked out, or a command or registry is unreachable, mark the entry
unverified and continue. Never conclude from a missing checkout that an artifact does not exist.

## Check before creating

Before creating a new artifact of a kind listed in the first paragraph (editing an existing one does not
trigger this):

1. Match the capability you need against the "Provides" column of the registry below, by capability, not by
   name.
2. Ask `$alaa-memory-os` whether existing infrastructure already provides that capability, under its active
   adapter's rule for existence and ownership questions. Recall fails open: no answer is not evidence of
   absence.
3. Verify every hit in the owning repository.
4. Record the answer in the change's plan or PR description: the entry reused or extended with its evidence,
   or the reason no entry fits with the sources checked. Inside an orchestrated run, the orchestrator's
   planning phase owns the record format.
5. When an entry fits, reuse it or extend it in its owning repository. A parallel artifact needs its owner's or
   the user's explicit decision; until then stop, name the fitting entry and its gap, and create nothing.

A new shared artifact that fits no entry adds its entry here in the same effort. The owner of an artifact
updates its entry in the same effort that adds, renames, moves, or retires it.

## Registry

Status values: `live` (published and in use), `unpublished` (implemented in the owning repository, not yet
published or run in the target; the pointer names the blocking item), `planned`, `being decided` (names the
deciding document). Deploy items `EO-NN` live in `<repo>/docs/employer-open-items.md` of `deploy`.

| Name | Owner | Artifact and reference form | Provides | Consumers |
|---|---|---|---|---|
| CI job image | `ci-image` | Image `alaa/ci/image` in Nexus. Tool pins in `<repo>/tools/versions.env` and `<repo>/tools/tool-images.env`. The Runner pin is `RUNNER_JOB_IMAGE` in the `deploy` `.env.example`; `deploy` is its only writer | kubectl, helm with plugins, kubeconform, yamllint, python3, shellcheck, GNU grep, yq, jq, docker CLI and buildx, skopeo, psql and pg_dump, node, and the other tools its README lists | The deploy-tools image; Runner-default jobs once `RUNNER_JOB_IMAGE` points at it (EO-32) |
| Deploy toolkit | `deploy` | Charts `<repo>/helm/alaa-service` and `<repo>/helm/gitlab-runner-wrapper`; class layers `<repo>/values/classes/`; `<repo>/scripts/helm-release.sh`; `<repo>/scripts/alaa-deploy`; schemas `<repo>/schemas/service-contract.v1.json` and `<repo>/schemas/gateway-route-set.v1.json`; `<repo>/scripts/monitor-release.sh`; operator scripts `<repo>/scripts/sync-openshift-secret.sh`, `<repo>/scripts/db-ensure-privileges.sh`, `<repo>/scripts/db-export.sh`; CD pipeline `<repo>/.gitlab-ci.yml` and `<repo>/ci/` | Per-service release, Runner install, ServiceContract validation and label encoding, route-set assembly, release monitoring, Secret sync, DB grants and export | Operators; the CD pipeline; `service-ci-kit` (contract validation through the deploy-tools image); `gateway` local runtime (`alaa-deploy route-set assemble`) |
| Deploy-tools image | `deploy` | Image `alaa/deploy-tools`, built from `<repo>/docker/deploy-tools/Dockerfile` `FROM` the CI job image (`DEPLOY_TOOLS_BASE_IMAGE` defaults to `RUNNER_JOB_IMAGE`); consumers pin `DEPLOY_TOOLS_IMAGE` by digest | Deploy-owned content only (`alaa-deploy`, chart, schemas, class layers, CI scripts); entrypoint `alaa-deploy`. Installs no tool | Service pipelines (validate and label, no network); the `deploy` release jobs |
| Service CI kit | `service-ci-kit` | GitLab includes `<repo>/gitlab/php-service.yml` (full PHP pipeline) and `<repo>/gitlab/contract-and-handoff.yml` (stack-neutral build, label, smoke, handoff); the consumer pins it only through the include `ref:` | Image build with the two contract labels, smoke by digest, semantic release, handoff of `SERVICE` and `IMAGE_DIGEST` to `deploy`. Never deploys and holds no cluster credential | Laravel services (PHP include); `gateway` and `client` (stack-neutral include) |
| Service runtime kit | `service-runtime-kit` | Generator `<repo>/scripts/render-runtime.sh`, `<repo>/scripts/validate-runtime.sh`, `<repo>/scripts/up-local.sh`, `<repo>/scripts/bootstrap-service-repos.sh` with `<repo>/contracts/service-bootstrap.tsv`; repo-support pack `<repo>/templates/repo-support/` (managed `.gitattributes`, LF and BOM hook scripts) | Compose and Swarm runtime generation, PgBouncer and Octane files, the LF/BOM repo-support pack. Not CI and not Kubernetes | Laravel and PHP service repositories |
| PHP base image | `octane-base` | Image `alaa/services/octane-base` in Nexus; the consumer pins it in its `Dockerfile` (`OCTANE_BASE_IMAGE`) and `runtime/service.runtime.env` | PHP Octane base with the Laravel runtime extensions, Nexus APK key, provenance and SBOM | Laravel service images |
| Gateway | `gateway` | Image with the render-only chart `<repo>/charts/gateway` and `<repo>/scripts/gateway-start`; its own `deploy/service.yaml` (class `edge`); released by `deploy` | Edge HAProxy: JWT verification, header sanitizing and injection, posture, routing from the assembled route set | Every service behind the gateway; `client` through `consumes.gatewayUrl` |
| Nexus | organization platform | Internal image registry, chart OCI repository, and npm, apk and pip proxies. Each consumer takes the address from an env variable whose current value is in its own `.env.example` (in `deploy`: `DOCKER_REGISTRY`, `RUNNER_REGISTRY_HOST`, `RUNNER_CHART_OCI_REF`, commented `PIP_INDEX_URL`) | The only permitted artifact source for the offline target. A missing artifact is an import task recorded as a deploy `EO-NN` item, never a reason to fetch from the internet | Every build and release |

| Name | Verify presence | Decisions live in | Mechanics owner | Status |
|---|---|---|---|---|
| CI job image | `<repo>/tools/versions.env` in `ci-image`; a registry read of `alaa/ci/image` where network access is authorized | `ci-image` `<repo>/README.md` ("Consumers and Ownership"), `<repo>/CHANGELOG.md` | `$alaa-gitlab-ci-cd`, `$alaa-docker-production` | `unpublished` (EO-32) |
| Deploy toolkit | Files named in the entry; `deploy` `<repo>/docs/BIG_PICTURE.md` repository map | `deploy` `<repo>/AGENTS.md`, `<repo>/docs/service-contract.md`, `<repo>/docs/rfc/`, `<repo>/docs/employer-open-items.md` | `$alaa-k8s-helm`, `$caas-arvan-kuber`, `$alaa-bash-shell` | CD pipeline `unpublished`: never run on GitLab (EO-12, EO-30) |
| Deploy-tools image | `<repo>/docker/deploy-tools/Dockerfile`; `DEPLOY_TOOLS_IMAGE` in the `deploy` `.env.example` | As the deploy toolkit | `$alaa-docker-production` | `unpublished` (EO-32); a deploy pipeline is not created while `DEPLOY_TOOLS_IMAGE` lacks a digest |
| Service CI kit | `<repo>/gitlab/contract-and-handoff.yml`, `<repo>/VERSION` and the repository's tags | `service-ci-kit` `<repo>/README.md`, `<repo>/docs/rfc/`; the handoff definition is `deploy` `<repo>/ci/handoff-inputs.yaml`, which wins on a conflict | `$alaa-gitlab-ci-cd` | Current major `unpublished` while its tag is missing; read `<repo>/VERSION` against the tags |
| Service runtime kit | `<repo>/scripts/render-runtime.sh`, `<repo>/VERSION`; in a consumer, `runtime/service.runtime.env` and the generated files | `service-runtime-kit` `<repo>/README.md`, `<repo>/docs/02-service-ci-kit-vs-service-runtime-kit.md`, `<repo>/docs/requests-for-change/` | `$service-runtime-kit-governance`, `$alaa-docker-production` | `live` for local runtime; read `<repo>/VERSION` against the tags for the current line |
| PHP base image | `octane-base` `<repo>/README.md` registry line; the consumer's `OCTANE_BASE_IMAGE` | `octane-base` `<repo>/README.md`, `<repo>/CHANGELOG.md` | `$alaa-docker-production`, `$alaa-octane-performance` | `live` |
| Gateway | `<repo>/charts/gateway`, `<repo>/scripts/gateway-start`, `<repo>/snapshots/README.md` | `gateway` `<repo>/AGENTS.md`, `<repo>/docs/route-set.md`, `<repo>/docs/error-code-registry.md`, `<repo>/docs/DOCKER_SHARED_RUNTIME.md` | `$alaa-haproxy`, `$alaa-trust-gateway-auth` | Kubernetes path `unpublished` with the deploy toolkit; non-Kubernetes production `being decided` (deploy RFC 0006) |
| Nexus | The consumer's `.env.example` variable | `deploy` `<repo>/docs/employer-open-items.md` | `$alaa-docker-production`, `$alaa-gitlab-ci-cd` | `live`; individual repositories missing from it are EO items |

External platform services (GitLab, OpenShift, Arvan CaaS) are not entries: `$alaa-gitlab-ci-cd`,
`$alaa-k8s-helm`, and `$caas-arvan-kuber` own them, and the deploy EO register records what the employer
provides.

## Project roles

| Project | Owns | Never holds | Runtime served |
|---|---|---|---|
| Service repository (`auth`, `content`, `comment-service`) | Application code; `deploy/service.yaml` (ServiceContract v1, class `laravel`), the only per-service source for routes, body caps, env keys, and database and broker defaults; runtime-kit inputs; a thin `.gitlab-ci.yml` | Chart, manifest, RBAC, cluster credential, release, migrate, or monitor job, gateway posture keys | Kubernetes through `deploy`; local Compose and Swarm |
| `client` | Quasar SSR/PWA front end; its contract (class `edge`) with `consumes.gatewayUrl` and `consumes.apiPrefixes` | Chart, manifest, release job, trusted header | Image on Kubernetes; `quasar dev` locally |
| `gateway` | HAProxy image, posture (public paths, rate limits, authz route groups, sanitize lists, JWT and TOTP) in `charts/gateway` keyed `<service>/<route>`, its contract (class `edge`), `gateway-start`, `snapshots/` | A releasable template, environment overlay, release job, backend routes or ports | Kubernetes (render at start); local shared Docker |
| `deploy` | Schemas, class layers, both charts, release script, CD pipeline, the EO register; only writer of `RUNNER_JOB_IMAGE` | Secrets, any per-service route, body cap, or env key, gateway posture, a dev chart or values file, invented hosts, internet downloads, cluster-scoped RBAC | Kubernetes/OpenShift production only |
| `service-ci-kit` | Service CI: build, label, smoke, release, handoff | Any cluster, Helm, kubectl, kubeconfig, Secret, migration, or DB job; a public-registry fallback | CI only |
| `service-runtime-kit` | Local Compose and Swarm generation for Laravel and PHP | GitLab CI logic, Kubernetes or OpenShift release | Local Compose; Swarm templates |
| `ci-image` | The CI toolchain image and its pins | Runner installation, application build stacks, Secrets, tool pins duplicated elsewhere | Job image for all CI; base of deploy-tools |
| `octane-base` | The PHP Octane base image | Service logic | Base of Laravel service images |

A contract has one of two classes, `laravel` or `edge` (`deploy` `<repo>/schemas/service-contract.v1.json`).
A Go service, and services that have only a runtime-kit row, have no documented release path yet; report that
gap instead of inventing a class. The contract field reference is `deploy` `<repo>/docs/service-contract.md`;
the Persian walkthrough of roles and flows is `deploy` `<repo>/docs/architecture-guide.md`.

## Delivery flows

Each step lists its owner and the projects it affects. Commands run from the root of the repository named.

These tables assign owners; they authorize nothing. A step that calls a cluster, GitLab, or Nexus, or publishes,
releases, rolls back, or syncs a Secret, needs the user's explicit authorization for that action.

### A. New service

| # | Step | Owner | Affected |
|---|---|---|---|
| 1 | Optional local bootstrap: add a row to `service-runtime-kit` `contracts/service-bootstrap.tsv`, run `bash scripts/bootstrap-service-repos.sh`, then `render-runtime.sh` and `validate-runtime.sh` | Service developer | Service repo, `service-runtime-kit` |
| 2 | Write `deploy/service.yaml`: workloads, Secret references by name and key only, `gateway.routes`, `requestBody.maxBodyBytes`, database and broker defaults, `preDeployJobs.migrate`. Validate against a deploy checkout: `DEPLOY_REPO_DIR=../deploy bash scripts/contract-validate.sh` prints `VALID` (`content` names it `<repo>/scripts/validate-contract.sh`) | Service developer; consult `gateway`, `client`, `deploy` | Service repo |
| 3 | Wire CI: thin `.gitlab-ci.yml` including the service CI kit, `.releaserc.json`, a `Dockerfile` with a `runtime` target; GitLab variables `DEPLOY_TOOLS_IMAGE` (by digest), `ALAA_DEPLOY_PROJECT`, and the registry credentials | Service developer | Service repo, GitLab, `service-ci-kit` |
| 4 | Honour the release-derived env (for Laravel, `OCTANE_PACKAGE_MAX_LENGTH` and `OCTANE_MAX_EXECUTION_TIME` in `config/octane.php`) | Service developer | Service repo |
| 5 | Add posture for each new route: `publicPaths`, an authz group with `endpointRef` (value `<service>/<endpoint>`), `routePolicies` and `methodOverrideRoutes` (keys `<service>/<route>`) | Gateway owner | `gateway`, `deploy` |
| 6 | When the client calls the service, add the prefix to `consumes.apiPrefixes` and the `Dockerfile` `*_API_PREFIX` default; `<repo>/scripts/checkServiceContract.ts` fails drift in CI | Client owner | `client` |
| 7 | Register in `deploy`: `bash scripts/snapshot-contracts.sh --projects-dir ..` writes `tests/alaa-service/snapshots/<svc>.contract.json` (gate input only); add the service to its class lists in `tests/alaa-service/checks/`; add it to `inputs.SERVICE.options` in `<repo>/ci/handoff-inputs.yaml`, then `bash ci/handoff.sh spec`; add `<SVC>_IMAGE_REPOSITORY`, `<SVC>_IMAGE_DIGEST` (empty by design), `<SVC>_APP_VERSION` to `.env.example` and the `tests/alaa-service/release.env` fixture; touch `values/secret-access.yaml` only for a Secret not named `<release>-*` or shared. No per-service values file exists | Deploy owner; consult the service | `deploy` |
| 8 | Route set: the next gateway release assembles it from ConfigMaps labelled `alaa.io/service-contract=v1` | Deploy pipeline (automatic) | `gateway`, `deploy` |
| 9 | Create the Nexus image repository `<DOCKER_REGISTRY>/alaa/services/<svc>` and the protected GitLab variable `<SVC>_IMAGE_REPOSITORY`; record each unknown as a new deploy EO item | Employer platform | Nexus, GitLab, `deploy` |
| 10 | Provision Secrets (flow B1 step 1) | Operator | `deploy` |
| 11 | Once per clone, enable the LF/BOM hooks: `bash scripts/setup-git-hooks-bom.sh` | Each developer | The clone |
| 12 | The first default-branch pipeline hands off; `release:apply` fails unless step 10 and the flow B1 prerequisites are ready. Flows B and C follow | Pipeline | Service repo, `deploy` |

### B. First deployment

Two cases differ: bootstrapping the whole fleet into an empty namespace with no gateway (B1), and adding one
backend to a running fleet (B2). The deploy handoff pipeline releases one service per run with `SERVICE` and
`IMAGE_DIGEST`; `release:apply` is manual, and the handoff digest becomes `<SVC>_IMAGE_DIGEST`
(`<repo>/ci/release.sh` in `deploy`). That pipeline has not run on GitLab (EO-12, EO-30). The deploy runbook
steps run from the approved operator or CD host with `<repo>/scripts/helm-release.sh`, where the operator supplies
`<SVC>_IMAGE_DIGEST` (the digest of the image imported into Nexus) in `--env-file` or the process environment.

#### B1. Fleet bootstrap

Prerequisites (deploy runbook `<repo>/docs/runbook/40-before-first-deployment.md`): `OPENSHIFT_NAMESPACE` differs
from `MONITORING_NAMESPACE`; images are in Nexus by digest; the Runner is installed; the GitLab settings exist;
the deploy project has `KUBECONFIG` (File), `EXPECTED_API_SERVER`, `WATCH_KUBECONFIG`, `OPENSHIFT_NAMESPACE`, the
Secret File variables, and `DEPLOY_TOOLS_IMAGE` and `GATE_TOOLS_IMAGE` with `@sha256`. The operator owns every
step unless noted; every step affects `deploy` and the cluster.

| # | Step | Affected |
|---|---|---|
| 1 | Secrets: `bash scripts/sync-openshift-secret.sh [--check] NS SECRET KEY=FILE ...`; each FILE is a path, never a value. A GitLab File variable is a file only inside a job Pod, and no pipeline job runs this script (deploy runbook 80 is the template of a future job). Today the operator runs it from the approved operator or CD host: writes the values to temporary files from the source the runbook names, checks with `--check`, runs it, and deletes the files; they are never committed. It needs `KUBECONFIG` and `EXPECTED_API_SERVER`. Generate Passport keys on an offline host with `bash scripts/generate-passport-keys.sh` | `auth`, `content`, `comment-service`, `gateway` (reads `auth-passport-public`) |
| 2 | Database grants: the organization creates the database, role, and RabbitMQ vhost (EO-03, EO-05); then `bash scripts/db-ensure-privileges.sh` (idempotent) runs once per service, after they exist and before the first apply (runbook 40) | Laravel backends |
| 3 | Migrations run in the `migrate` pre-install/pre-upgrade hook on every release, so migrations follow expand/contract and seeders are idempotent. Owner: the service and the hook | Laravel backends |
| 4 | Release order: Laravel backends in any order, then `gateway`, then `client`, then exposure | All services |
| 5 | Each release: `scripts/helm-release.sh SVC --dry-run`, then apply | The target service |
| 6 | Gateway bootstrap: a backend release exits 2 until the gateway policy is readable. Before the first gateway release set `GATEWAY_IMAGE_REPOSITORY` and `GATEWAY_IMAGE_DIGEST`; unset the digest after it | `gateway`, backends |
| 7 | `scripts/helm-release.sh gateway`; needs Secret `auth-passport-public` and `GATEWAY_NAMESPACE` equal to `OPENSHIFT_NAMESPACE` | `gateway` |
| 8 | Exposure: `PUBLIC_EXPOSURE` defaults to `none`; `route` or `ingress` works on OpenShift, only `ingress` on Arvan, and both need `PUBLIC_HOST` (EO-15). Owner: operator and employer | `gateway`, `client` |
| 9 | Smoke through `oc port-forward svc/gateway-web 8080:80` on each `/<prefix>/api/health`. A 503 `AUTHZ_SERVICE_UNAVAILABLE` on sidecar-enforced routes is expected until authz-sidecar has a deployer (EO-26) | `gateway`, backends |
| 10 | `bash scripts/monitor-release.sh --all --logs 40` | All releases |

#### B2. Adding one backend to a running fleet

Prerequisite: flow A steps 1 to 11 are done, and the gateway, client, and other backends run.

| # | Step | Owner | Affected |
|---|---|---|---|
| 1 | Add the new routes' posture to the gateway profile (flow A step 5). Every `endpointRef` must name an endpoint in the route set, or the gateway render fails; so the gateway release comes after the backend exists in the cluster | Gateway owner | `gateway` |
| 2 | Build a new gateway image: `gateway-start` renders the chart baked into the image, so posture changes only with a new image. Record its digest | Gateway owner | `gateway` |
| 3 | Secrets and database for the new service (B1 steps 1 and 2) | Operator, organization | `deploy` |
| 4 | Release the backend, through the handoff pipeline (`release:dry-run`, then the manual `release:apply`) or from the operator host with `<SVC>_IMAGE_DIGEST`. The backend reads the gateway policy from the deployed gateway's ConfigMap. Only when `helm-release.sh` prints D24 (the new gateway image raised `forwardedHeaderAllowanceBytes`): set `GATEWAY_IMAGE_REPOSITORY` and `GATEWAY_IMAGE_DIGEST` to the new image, re-release the backends it lists, release the gateway, then unset `GATEWAY_IMAGE_DIGEST` | Operator | The new service |
| 5 | When the deployed route set lacks the new contract, `helm-release.sh` prints `GATEWAY RE-RELEASE REQUIRED`. Release the gateway with the new image: `scripts/helm-release.sh gateway` with `GATEWAY_IMAGE_DIGEST` set to the new digest, or the gateway's own handoff. The pipeline's `release:gateway` re-releases only the deployed digest, so it never delivers the new image | Operator | `gateway` |
| 6 | Smoke the new service's routes and run `bash scripts/monitor-release.sh --all --logs 40` | Operator | All releases |

### C. Update and rollback

| # | Step | Owner | Affected |
|---|---|---|---|
| 1 | Service pipeline on the default branch: `make_tag_version`, `build` (validates the contract with `alaa-deploy`, builds with both labels, pushes), `smoke` (pulls by digest, checks the labels), `release`, `handoff_prepare`, `handoff` | Service and `service-ci-kit` | Service repo, Nexus |
| 2 | Handoff sends only `SERVICE` and `IMAGE_DIGEST` through `trigger:inputs` to `ALAA_DEPLOY_PROJECT`; with no new release the child pipeline is a no-op | `service-ci-kit` | Service repo, `deploy` |
| 3 | The deploy pipeline is created only for a pipeline source on the protected default branch with `DEPLOY_TOOLS_IMAGE` carrying `@sha256`; otherwise the upstream trigger fails | `deploy` | Service repo, `deploy` |
| 4 | Jobs `handoff:validate`, `release:dry-run`, `release:apply` (manual and blocking unless `RELEASE_APPLY_MODE=auto`), `release:monitor`, `release:gateway` | `deploy`; operator applies | The target service |
| 5 | `release:gateway` runs `helm-release.sh gateway --check-sync` and re-releases the deployed gateway digest only on exit 3 (stale route set); a new gateway image needs flow B2 step 5 | `deploy` | `gateway` |
| 6 | Apply phases: inputs, preflight, lint, render, secret-preflight, contract-preflight (prefix conflict, body cap, handler budget), helm-upgrade with the migrate hook and `--wait`, route-admission, helm-test, gateway-sync. A changed contract SHA prints `GATEWAY RE-RELEASE REQUIRED` | `deploy` | Target service, `gateway` |
| 7 | Evidence stays in the `release-diagnostics/` artifact; the scheduled `release:watch` job reads with `WATCH_KUBECONFIG` and reports an unhealthy release or a stale route set | `deploy` | All releases |
| 8 | Off the default branch, `gate:chart` runs the strict chart gate. It needs `GATE_TOOLS_IMAGE` with `@sha256`; without it, job `tools-image:missing` fails (EO-31) | `deploy` | `deploy` |

Rollback:

- A failed upgrade reverts itself: the upgrade runs with `--atomic` (Helm 3) or `--rollback-on-failure`
  (Helm 4). The script prints a `helm rollback` hint, or `helm uninstall` after a failed first install; read
  `helm history` before following it. A release stuck in `pending-*` follows deploy runbook 90.
- Rollback never reverses migrations, seeds, or credential changes.
- After any backend rollback, re-release the gateway with `scripts/helm-release.sh gateway`, only with the
  user's explicit authorization for that release.
- Ordering of two competing digests of one service, and cancel or retry, are undecided (deploy RFC 0001 and
  RFC 0002).
- After a Secret change: sync it, then `oc rollout restart deploy -l app.kubernetes.io/instance=RELEASE`.

### D. Local runtime

| Step | Owner | Affected |
|---|---|---|
| Laravel backend: prepare `.env` beside the service (Secrets and DB credentials), `runtime/service.runtime.env`, `runtime/hooks/`; run `bash scripts/runtime/render-runtime.sh` (generates `docker-compose*.yml`, `docker/octane/`, `docker/pgbouncer/`, `<repo>/scripts/docker/up-local.sh`; never hand-edit them), then `bash scripts/runtime/validate-runtime.sh` and `bash scripts/docker/up-local.sh` | Service developer | Service repo, `service-runtime-kit` |
| Shared infra is the Compose project `alaa-shared-infra` (`15-deployment-and-runtime-contract.md`); the first service to start creates it, so check `docker ps` first. `deploy` also ships `docker-compose-dev-only-infra.yaml` | Developer | Every local service |
| Gateway: run `<repo>/scripts/docker/up-local.sh` with `compose` or `swarm` in `gateway` (next section) | Gateway owner | `gateway` |
| Client: `pnpm install`, then `quasar dev` | Client owner | `client` |
| Contract check: `bash tests/contracts/run.sh --validate path/to/service.yaml` in `deploy` | Service developer | Service repo |

Local and contract values may differ on purpose (for example a queue worker timeout); queue names, tries, and
worker roles must match between `runtime/service.runtime.env` and the contract. A check of that match is
planned, not implemented, so the service owner keeps them equal by hand (deploy
`<repo>/docs/service-contract.md`, "Overlap with service-runtime-kit inputs").

## Responsibility matrix

| Task | Responsible | Consulted | Affected |
|---|---|---|---|
| Edit `deploy/service.yaml` | Service | `gateway`, `client`, `deploy` | |
| Change a schema or class layer | `deploy` | | Services, `gateway`, `client`, `service-ci-kit` |
| Gateway posture | `gateway` | Service | `deploy` |
| Backend body cap and prefix | Service | | `gateway`, `deploy` |
| Build, label, push an image | Service, `service-ci-kit` | `deploy`, `ci-image`, employer | |
| Define the handoff | `deploy` | Employer | Services, `service-ci-kit` |
| Render and apply a release | `deploy` | `ci-image`, employer | `gateway`, `client` |
| Assemble the route set and re-release the gateway | `deploy` | | `gateway` |
| Provision Secrets | `deploy` operator, employer | Service, `gateway` | |
| DB grants and dumps | `deploy` operator, employer | Service | |
| Run migrations | Service (code), `deploy` (hook) | | |
| Register a service in `deploy` | `deploy` | Service | |
| Nexus repository and digest | Employer | Every project | |
| Local Compose runtime | `service-runtime-kit`, service (inputs) | | |
| Local gateway | `gateway` | Service, `service-runtime-kit`, `deploy` | |
| Toolchain image and `RUNNER_JOB_IMAGE` | `ci-image` (image), `deploy` (pin), employer (publication) | | |
| Runner install and upgrade | `deploy`, employer | | `ci-image` |
| Public exposure | `deploy`, employer | | `gateway`, `client` |
| authz-sidecar | Employer (EO-26) | | `gateway`, `deploy` |

## Gateway configuration: generated, read, and non-Kubernetes targets

Kubernetes path: a backend release renders a `<release>-service-contract` ConfigMap, a cache of the image label.
Only the gateway release assembles the GatewayRouteSet from those ConfigMaps and mounts it as `route-set.json`;
the image's `gateway-start` renders `haproxy.cfg` from the baked chart, the profile, and that route set at Pod
start, runs `haproxy -c`, then starts HAProxy. Routing data (prefix, upstream, strip, body caps) comes only from
the route set, and therefore from each backend's contract. Posture lives only in the gateway repository.

Reading the generated configuration: `gateway` `<repo>/snapshots/` holds three generated files:
`alaa-service.haproxy.cfg` (Kubernetes profile, `cluster` route set), `docker-shared.haproxy.cfg` (shared Docker
profile, from the synthetic `full-surface.local.json` route set), and `<repo>/snapshots/README.md` with one route
table per profile: route key, prefix, target, upstream, strip, public paths, authz groups. Regenerate with
`make snapshot`; `bash scripts/render-snapshot.sh --check` covers all three and runs in `make ci-local` and the
gateway CI job. The snapshots are rendered from fixture route sets with fabricated digests: never the deployed
configuration, never hand-edited, never a value source for `deploy`. The deploy-assembled render is
not snapshotted, because it drifts with the deploy checkout.

Gateway error codes, including the HAProxy-generated `REQUEST_TIMEOUT` (408) and `GATEWAY_TIMEOUT` (504),
live in the gateway's own registry `<repo>/docs/error-code-registry.md`, as `10-core-service-contract.md`
requires of every service.

Compose and Swarm: `helm/alaa-service` is never used, and `deploy` `<repo>/scripts/helm-release.sh` accepts only a
`cluster` route set. The gateway's `<repo>/scripts/docker/up-local.sh` copies the sibling contracts, runs
`alaa-deploy route-set assemble` (from `DEPLOY_REPO_DIR` or `DEPLOY_TOOLS_IMAGE`) with target `local`,
namespace `docker-shared`, and placeholder digests, renders `charts/gateway` on the host with
`docker/values.shared-network.yaml` (needs `helm`), and mounts the result in place of `gateway-start`. Swarm
adds content-hashed Swarm configs and `docker stack deploy`, documented as local or single-node. Backends have
generated Swarm stacks; the gateway has only this local profile.

No production gateway path exists on Compose or Swarm: no production stack, no deploy-side Swarm release, no
operator procedure. That is inferred from absence, and deploy RFC 0006
(`<repo>/docs/rfc/0006-production-gateway-on-a-non-kubernetes-target.md`) holds the decision. Until it
closes, report a request for one as an owner decision, and never ship the `local` route set, the widened local
overlay, or placeholder digests as production.

## Open items

- Who reviews an entry change when the owning repository has a different maintainer is undecided; until it is,
  the skill pack maintainer reviews.
- The deploy merge-request gate image `GATE_TOOLS_IMAGE` is not in Nexus yet (deploy EO-31); without it the
  gate runs only on a developer machine.
- A drift check that fails when a named file or variable disappears from its owning repository is not built,
  and its home is undecided. It must skip with an explicit message when the sibling repositories are absent.
