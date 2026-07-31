# House Companions for Go Work

The skills a Go task reaches when it crosses out of Go and into workflow, delivery, edge, or documentation. The
doctrine and platform owners — contracts, reliability, security, trust, data, messaging, observability, kit
governance, clean code, Fiber, prompting — are in `05-what-this-skill-does-not-own.md` and are not repeated here.

Trigger forms: Claude Code `/name`, Codex `$name`. Load a skill when the condition in its row holds, and not
otherwise.

## Running the work

| Load | When you are about to… |
|---|---|
| `/alaa-workflow` (`$alaa-workflow`) | start Go work that spans more than one session, more than one phase, or more files than one message can track — it holds durable plan and execution state |
| `/alaa-low-noise` (`$alaa-low-noise`) | run a repository search, a log tail, or a command whose output would fill the context and bury the signal |
| `/alaa-cc-orchestrator` (`$alaa-cc-orchestrator`) | split Go work into specialist lanes with independent verification and review gates in Claude Code |
| `/alaa-codex-orchestrator` (`$alaa-codex-orchestrator`) | do the same in Codex |
| `/alaa-controlled-ops` (`$alaa-controlled-ops`) | run a command that touches a shared system, a live environment, or anything not reversible from the repository |
| `/alaa-memory-os` (`$alaa-memory-os`) | record a drift note, a decision, or context that a later session must find |

## Delivery and runtime

| Load | When you are about to… |
|---|---|
| `/alaa-docker-production` (`$alaa-docker-production`) | write or change a Dockerfile, a Compose file, a Swarm stack, or an image-hardening step for a Go service |
| `/alaa-k8s-helm` (`$alaa-k8s-helm`) | change a Kubernetes or OpenShift object, a Helm chart, a probe, a rollout strategy, or a Route |
| `/caas-arvan-kuber` (`$caas-arvan-kuber`) | deploy to Arvan CaaS, where generic Kubernetes guidance does not match the platform |
| `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) | write or debug `.gitlab-ci.yml`, a runner configuration, a cache, or a pipeline stage |
| `/alaa-makefile` (`$alaa-makefile`) | add or change a `make` target that other agents or CI will invoke |
| `/alaa-haproxy` (`$alaa-haproxy`) | change edge routing, TLS termination, header trust, connection limits, or edge rate limiting in front of a Go service |
| `/service-runtime-kit-governance` (`$service-runtime-kit-governance`) | generate or change local runtime and shared-infrastructure definitions that Go and Laravel services must share |

## Data and integration surfaces

| Load | When you are about to… |
|---|---|
| `/clickhouse-performance-schema-ops` (`$clickhouse-performance-schema-ops`) | design or change a ClickHouse table, a materialized view, or an ingest path |
| `/alaa-mongodb-patterns` (`$alaa-mongodb-patterns`) | work against MongoDB from a Go service |
| `/alaa-partitioned-table-fk-audit` (`$alaa-partitioned-table-fk-audit`) | add or change a foreign key on a partitioned Postgres table |
| `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) | encode or decode a public identifier in Crockford Base32 |
| `/openfga` (`$openfga`) | model or query relationship-based authorization in OpenFGA |
| `/tusd-upload-platform` (`$tusd-upload-platform`) | work on resumable upload behaviour or the tusd service |
| `/alaa-bale-provider` (`$alaa-bale-provider`) · `/alaa-sms-provider-mediana` (`$alaa-sms-provider-mediana`) | integrate with those messaging or SMS providers |
| `/alaa-mono-package` (`$alaa-mono-package`) | change how a mono-package is structured, published, or consumed |

## Documentation and artifacts

| Load | When you are about to… |
|---|---|
| `/alaa-postman-collections` (`$alaa-postman-collections`) | produce or update a Postman collection or an OpenAPI artifact for a Go service |
| `/alaa-repo-docs` (`$alaa-repo-docs`) | create, refresh, reorganize, or cross-link any repository Markdown document for a Go service — `README.md`, the `docs/` deep dives, `remaining-task.md`, documentation navigation, or repo-local links — writing each one in the language it already uses. A Persian companion such as `README.fa.md` is one case of this row, and only when the user explicitly asks for that companion |
| `/alaa-signoz-clickhouse-docs` (`$alaa-signoz-clickhouse-docs`) | query SigNoz or write a ClickHouse query against telemetry data |

## Rule for every row above

**Rule:** load the companion before writing the code it governs, not to review the code afterwards. A companion loaded
after the work is done can only find defects; loaded first it prevents them.

**Forbidden:** reproducing a companion's rules into a Go service's own documentation. **Rule:** cite the companion by
name and let it stay the single source.
