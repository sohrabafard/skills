# 0002 - Infrastructure services and shared delivery artifacts in alaa-services-contract

Status: proposed
Trigger condition: an agent rebuilt shared infrastructure that already existed because no skill named it.
Owner: skill pack maintainer; Reviewer: none yet; Date: 2026-10-02
Supersedes: none; Superseded by: none

## 1. Problem

Agents working in one Ala repository see that repository's files and little else. When a task needs an
image, toolchain, chart, CI include, generator, hook pack, or script, the agent builds one if the local
files do not show an existing one. The fleet already owns many such artifacts, but no skill lists them.
`alaa-services-contract` owns shared surfaces and the deployment baseline
(`references/15-deployment-and-runtime-contract.md`). It names `service-ci-kit` and the shared-infra reuse
rule, but it does not say which repository owns which image, chart, include or generator. Hindsight `reflect`
knew the answer; knowledge-page search did not surface it. Recall that depends on query wording is not a guard.

## 2. Evidence

Incident, 2026-10-02, in `D:/Sohrab/Project/deploy/docs/_agent_plans/20261001-114507_alaa-service-gateway-client__service-contracts-ssot.md`,
section "ci-image and the deploy-tools image":

- Agents designing the ServiceContract release model created a tools image `alaa/deploy-tools` in deploy
  (`docker/deploy-tools/Dockerfile`, `.env.example` key `DEPLOY_TOOLS_IMAGE`) with its own helm, jq, yq and
  skopeo pins.
- They had seen only `RUNNER_JOB_IMAGE` in `deploy/.env.example` (an `alpine/helm` image). They did not know
  the organization job image `alaa/ci/image` from the `ci-image` repository.
- `ci-image` already supplies kubectl, helm, jq, yq, skopeo, buildx, python3, shellcheck, kubeconform, psql
  and node (`ci-image/README.md` "Scope"; pins in `ci-image/tools/versions.env` and `tool-images.env`).
- The deploy-tools image is now defined as a thin layer over that job image (comment on `DEPLOY_TOOLS_IMAGE`
  in `deploy/.env.example`), after the duplicate pins had been designed.

Near-misses in the same work:

- `service-runtime-kit` already owned the LF/BOM repo-support pack (`templates/repo-support/`,
  `scripts/setup-git-hooks-bom.*`), while deploy carries its own `scripts/setup-git-hooks-bom.*`.
- The `service-ci-kit` versus `service-runtime-kit` boundary (CI pipeline versus local runtime generation)
  is stated in each README but not in the skill.
- The deploy contract tooling (`scripts/alaa-deploy`, `schemas/service-contract.v1.json`) is consumed by
  `service-ci-kit` (`gitlab/contract-and-handoff.yml`), so a second validator elsewhere would drift.

## 3. Proposal

Add a registry of infrastructure services and shared delivery artifacts to `alaa-services-contract`, plus a
"check before creating" rule.

### 3.1 Entry shape

One entry per artifact family, with these fields:

| Field | Content |
|---|---|
| Name | Short stable name |
| Owning repository | Repository name, for example `ci-image` |
| Artifact | Kind (image, chart, template, include, package, script set) |
| Reference form | The form a consumer writes, with no version, tag or digest. States where the pin lives (file or variable) |
| Provides | What it supplies, in one line, so overlap can be judged |
| Consumers | Repositories or jobs that use it today |
| Mechanics owner | The skill that owns how to author or run it |
| Status | `live`, `planned`, or `being decided`, with a pointer when not `live` |

Entries carry no version pins, counts, or dates, following the skill's rule that volatile facts live in the
owner. The reference form points to the owning variable, for example "`RUNNER_JOB_IMAGE` in the deploy
`.env.example`".

### 3.2 Initial entries (verified read-only on 2026-10-02)

| Name | Owner | Artifact and reference form | Provides | Mechanics owner |
|---|---|---|---|---|
| CI job image | `ci-image` | Image `alaa/ci/image` in Nexus; pin in the consumer variable (`RUNNER_JOB_IMAGE` in deploy); tool pins in `ci-image/tools/versions.env` | kubectl, helm (+diff, unittest), kubeconform, yamllint, python3, shellcheck, yq, jq, docker CLI and buildx, buildctl, skopeo, mc, psql/pg_dump/pg_restore, trivy, cosign, node | `$alaa-gitlab-ci-cd`, `$alaa-docker-production` |
| Deploy toolkit | `deploy` | Charts `helm/alaa-service`, `helm/gitlab-runner-wrapper`; `scripts/helm-release.sh`; `schemas/service-contract.v1.json`, `schemas/gateway-route-set.v1.json`; `scripts/alaa-deploy`; `scripts/monitor-release.sh`; DB operator scripts `scripts/db-ensure-privileges.sh`, `scripts/db-export.sh`; thin layer `docker/deploy-tools` (base = CI job image, key `DEPLOY_TOOLS_IMAGE`); CD pipeline (planned) | Per-service release, Runner install, ServiceContract validation and labels, release monitoring, DB grants and export | `$alaa-k8s-helm`, `$caas-arvan-kuber` |
| Service CI kit | `service-ci-kit` | GitLab includes `gitlab/php-service.yml` (full PHP pipeline) and `gitlab/contract-and-handoff.yml` (stack-neutral build, label, smoke, handoff); pin in the consumer's `SERVICE_CI_KIT_REF` | Image build with contract labels, smoke by digest, release, handoff to deploy. Never deploys | `$alaa-gitlab-ci-cd` |
| Service runtime kit | `service-runtime-kit` | Generator (`scripts/render-runtime.sh`, `scripts/up-local.sh`) and `templates/repo-support/` (managed `.gitattributes`, LF/BOM hook scripts) | Compose and Swarm runtime generation, PgBouncer, Octane files, LF/BOM repo-support pack. Not CI | `$service-runtime-kit-governance`, `$alaa-docker-production` |
| PHP base image | `octane-base` | Image `alaa/services/octane-base` in Nexus; pin in the service Dockerfile | PHP Octane base with Laravel runtime extensions, provenance and SBOM | `$alaa-docker-production`, `$alaa-octane-performance` |
| Gateway | `gateway` | Image and chart `charts/gateway`; rendered config consumed by deploy | Edge HAProxy: JWT verification, header sanitizing and injection, routing. Platform dependency | `$alaa-haproxy`, `$alaa-trust-gateway-auth` |
| Nexus | organization platform | Internal registry, npm, apk and pip proxies; addresses come from env variables whose current values are in the consuming repository's `.env.example` | Only permitted artifact source in the offline target | `$alaa-docker-production`, `$alaa-gitlab-ci-cd` |

Evidence read directly: the `ci-image` README and `tools/`, the `deploy` tree, `.env.example` and
`docs/BIG_PICTURE.md`, the `service-ci-kit` `gitlab/` files and README, the `service-runtime-kit` README and
`templates/repo-support`, the `octane-base` README, and the `gateway` README and `charts/`.

Not verified, to be marked as such in the entry until confirmed:

- Whether `alaa/ci/image` is published in Nexus. The deploy `.env.example` says it is not yet (tracked there as EO-32).
- A single canonical source for the npm, apk and pip proxy addresses. Deploy documents `PIP_INDEX_URL` only as a commented line.
- The published registry path of the gateway image and chart. Only `gateway/charts` was seen.
- The deploy CD pipeline. `docs/BIG_PICTURE.md` lists it as planned; the entry says `planned`.
- The `octane-base` and `service-runtime-kit` consumers list (not enumerated per service).

### 3.3 "Check before creating" rule

Before an agent creates a new image, toolchain layer, chart, CI include, generator, hook pack, or script that
could overlap an infrastructure artifact, it must:

1. Read the registry reference file and match the intended capability against the "Provides" column.
2. Ask Hindsight (`reflect`) about the capability, not the artifact name, for existing infrastructure.
3. Record the answer in the change's plan or PR description: the entry reused or extended, or the reason no entry fits.
4. When an entry fits, reuse it or extend it in its owning repository. Creating a parallel artifact needs the
   owner's decision, under the same stop cases as the skill's hard contract rule.

A new artifact that fits no entry adds an entry in the same effort (section 5).

## 4. Placement in the skill

- New file `references/16-infrastructure-services-and-delivery-artifacts.md`, next to
  `15-deployment-and-runtime-contract.md`.
- Topic map: add to Mode A++ the trigger vocabulary "which image, chart, CI include, generator or toolchain
  already exists; creating a new tools image, base image, hook pack or pipeline helper". Read `16` before `15`.
- `SKILL.md` trigger table: one row, "Creating or choosing an image, toolchain, chart, CI include, generator,
  hook pack or shared script -> `16-infrastructure-services-and-delivery-artifacts.md`".
- `SKILL.md` description: add "shared delivery artifacts" to the use-when sentence. The edit goes through
  `$alaa-prompting-guide`.
- One rule, one file. `16` owns the registry and the check-before-creating rule only. `15` keeps deployment
  modes, shared-infra reuse and the CI baseline, and links to `16` instead of restating entries. The `15`
  sentence naming `service-ci-kit` as the default CI project stays in `15`; the registry entry points to it.
  `95-fleet-conformance.md` stays a dated snapshot of rule conformance and holds no registry data. Tool
  mechanics stay in the companion skills named in the entries.
- `90-source-map.md`: add one line that the owning repository's README and variable files outrank the
  registry on a pin.

## 5. Maintenance

- The owner of an artifact updates its entry in the same effort that adds, renames, moves or retires the artifact.
- Drift check idea (not built): a read-only script in this repository reads each entry's owning repository,
  reference variable and file names from a small machine-readable block in `16`, and fails when a named file
  or variable no longer exists in the checkout. It skips with an explicit message when the sibling
  repositories are absent.
- An entry with status `being decided` names the deciding document and is revisited when it closes.

## 6. Alternatives considered

- Hindsight only. Rejected as the sole home: the incident shows recall misses depend on query wording, and
  memory must not be the only home of a contract. Hindsight stays the second check in the rule.
- Per-repository `AGENTS.md` only. Rejected as the sole home: the agent in deploy did not read `ci-image`
  instructions, and each repository would restate the others' artifacts. Each owning repository still
  documents its own artifact; the registry only points to it.
- Entries inside `15-deployment-and-runtime-contract.md`. Rejected: `15` is rule text for deployment modes;
  a registry has a different change rate and a different reader trigger.
- An index file outside the skill. Rejected: agents load skills, not unreferenced files.

## 7. Open questions

1. The placement of `ci-image` (own repository versus inside deploy) is being decided now. The CI job image
   entry must follow that decision; until it closes, the entry is `being decided` and names the deploy plan
   as the decision record.
2. Does the registry include external platform services (GitLab, OpenShift, Arvan) or only artifacts the fleet
   owns? This RFC proposes owned artifacts plus Nexus and the gateway as dependencies.
3. Who reviews entry changes when the owning repository has a different maintainer?
4. Should the drift check live in this repository or in each owning repository's CI?
5. Is the Hindsight step mandatory for every agent runtime, or only where Hindsight is the active memory adapter?
6. When `16` ships, Phase A step 4 of both orchestrators' `references/verification-and-gates.md` (the existing-infrastructure check) becomes a pointer to its check-before-creating rule, so the rule keeps a single owner.
7. The gateway generates the HAProxy request-timeout code `REQUEST_TIMEOUT` (408, `timeout http-request` or a body wait) and `GATEWAY_TIMEOUT` (504), and neither is registered in the fleet error-code references; should `alaa-services-contract` register both, so the gateway's static errorfile codes are named once for every consumer?
