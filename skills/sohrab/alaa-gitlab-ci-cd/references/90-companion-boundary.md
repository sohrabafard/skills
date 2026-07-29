# Companion boundary

## What this skill owns

`alaa-gitlab-ci-cd` owns **how a gate is expressed on a runner** — the job graph,
`rules:` and `needs:`, every expression of a cache key, artifact retention and
`expire_in`, and the runner image reference — and **decides no gate**. Which
checks must exist, what each asserts, and whether a non-zero exit blocks or
informs belong to the skill that owns that stack: `/alaa-frontend-devops`
(`$alaa-frontend-devops`) for a frontend repository, `/alaa-cicd-laravel-postgres`
(`$alaa-cicd-laravel-postgres`) for a PHP or Laravel service. When a request asks
this skill to decide whether a check should block, name the owner and write the
mechanism, not the verdict.

Concretely, this skill owns: executor selection and tuning, runner tags and job
placement, `config.toml` and the Helm chart's `runners.config`, variable and
input mechanics and precedence, and CI failure triage.

## The floating-toolchain split

`/alaa-frontend-devops` (`$alaa-frontend-devops`) declares the prohibition — a
floating tag such as `node:lts` fails its toolchain gate — and this skill does
not restate it.

This skill owns the **pinning mechanism**: how a pinned reference is written in
each of the five places one can appear. They are enumerated with their exact
syntax in `cache-artifacts-and-pinning.md`, together with the tag-versus-digest
rule, the private-registry-with-a-port form, and the single-variable fan-out that
makes a version move one edit.

## What this skill does not own

| Subject | Owner | Where the line falls |
|---|---|---|
| the frontend delivery gate register: the predicate a gate asserts, the command that evaluates it, the artifact it inspects | `/alaa-frontend-devops` (`$alaa-frontend-devops`) | it decides the gate; this skill writes the job that runs it |
| the PHP and Laravel gate register, the test-database policy, migration reversibility, and the dependency-audit severity floor | `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) | same split, PHP side |
| Dockerfile authorship, layer order, multi-stage boundaries, image minimisation, Compose authorship and the fail-closed interpolation invariant | `/alaa-docker-production` (`$alaa-docker-production`) | this skill decides how the build job is expressed; that skill decides what goes into the image |
| Helm chart authorship, chart values semantics, cluster RBAC and namespace design as policy | `/alaa-k8s-helm` (`$alaa-k8s-helm`) | this skill writes the runner's own `values.yaml` only |
| Arvan-managed Kubernetes behaviour, its pinned cluster version, and what that platform permits | `/caas-arvan-kuber` (`$caas-arvan-kuber`) | this skill writes the runner configuration; that skill states what the platform accepts |
| how a cache or routing decision is expressed as a proxy directive | `/alaa-haproxy` (`$alaa-haproxy`) | a CDN or proxy cache is not a job cache |
| threat classification, exposure severity, credential rotation and disclosure, and fail-closed doctrine for security decisions | `/alaa-security-review` (`$alaa-security-review`) | this skill writes the hardened form; that skill decides how bad an exposure is and what must happen next |
| why a timeout, retry, backoff, idempotency or degradation mechanism exists, and fail-open for availability | `/alaa-reliability-sla` (`$alaa-reliability-sla`) | this skill states only how a timeout or a retry is written in YAML, never what the value should be |
| what a pipeline or deploy event must emit, its requirement level and its retention | `/alaa-observability-soc` (`$alaa-observability-soc`) | this skill writes the artifact and the log line; that skill decides whether the signal is required |
| shared names and values: log fields, the `alaa_*` metric catalog, `OTEL_*` names and defaults, the host-port table, canonical shared-infra names | `/alaa-services-contract` (`$alaa-services-contract`) | any name a second service also reads |
| test layering, doubles, flake control, and what a given check proves | `/alaa-testing-strategy` (`$alaa-testing-strategy`) | this skill runs the command; that skill decides the command is the right proof |
| change control and proof strength for a production change | `/alaa-controlled-ops` (`$alaa-controlled-ops`) | whether this deploy may proceed at all |
| complexity budgets and structure choice in application code | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) | the job graph's own complexity stays here |
| designing a service or subsystem before implementation | `/alaa-system-design` (`$alaa-system-design`) | |
| the quality bar itself | `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md` | |
| which generator variable expresses a runtime value | `/service-runtime-kit-governance` (`$service-runtime-kit-governance`) | |
| shell script structure, `set -Eeuo pipefail`, argument parsing and ShellCheck | `/alaa-bash-shell` (`$alaa-bash-shell`) | when job logic outgrows a few inline lines and moves into a `.sh` file |
| a Make target's definition, and keeping the local verdict identical to the runner's | `/alaa-makefile` (`$alaa-makefile`) | this skill writes the job that calls the target |
| CDN origin bucket, object lifecycle and invalidation | `/alaa-minio-object-storage` (`$alaa-minio-object-storage`), `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) | including the bucket behind a distributed runner cache |
| model selection and reasoning effort | `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` | |

## The discriminating question for fail-closed versus fail-open

When a dependency cannot answer, does proceeding without it let something through
that must not get through? If yes, it is a security decision and
`/alaa-security-review` (`$alaa-security-review`) owns the fail-closed rule. If no,
it is an availability decision and `/alaa-reliability-sla`
(`$alaa-reliability-sla`) owns the degradation shape.
