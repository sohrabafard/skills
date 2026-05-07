# Sohrab Companion Skills

Use this file when the Go task crosses platform, workflow, contract, or trust boundaries that are not owned by generic Go skills.

## Workflow and context management

### alaa-workflow ( `$alaa-workflow` )

Use it when the Go task is long, multi-phase, risky, or spread across many files and needs durable plan and execution state.

### alaa-low-noise ( `$alaa-low-noise` )

Use it when repo search, logs, or command output could flood context and reduce signal.

## Go framework companion

### alaa-golang-fiber ( `$alaa-golang-fiber` )

Use it when the repo already uses Fiber, the user explicitly chooses Fiber, or a raw service is large, high-concurrency,
latency-sensitive, or SLA-heavy enough to justify Fiber's model.

## Observability, security, and trust

### alaa-observability-soc ( `$alaa-observability-soc` )

Use it when Go instrumentation also affects incident evidence, correlation IDs, alert semantics, or SOC-facing observability rules.

### alaa-security-review ( `$alaa-security-review` )

Use it when the Go change affects authn, authz, tenant isolation, secret handling, or any real trust boundary.

### alaa-trust-gateway-auth ( `$alaa-trust-gateway-auth` )

Use it when the Go service consumes trusted gateway headers, verified identity context, or downstream trust semantics.

### alaa-haproxy ( `$alaa-haproxy` )

Use it when the service behavior depends on HAProxy routing, header trust, TLS termination, rate limiting, or edge policy.

## Delivery and platform

### alaa-docker-production ( `$alaa-docker-production` )

Use it when the Go service also needs production Dockerfile, image hardening, Compose, or Swarm guidance.

### alaa-k8s-helm ( `$alaa-k8s-helm` )

Use it when the Go issue extends into Kubernetes, Helm, or OpenShift objects, probes, Routes, rollout behavior, or service exposure.

### caas-arvan-kuber ( `$caas-arvan-kuber` )

Use it when Arvan CaaS-specific delivery constraints matter and generic Kubernetes advice is not enough.

### alaa-gitlab-ci-cd ( `$alaa-gitlab-ci-cd` )

Use it when the repository needs `.gitlab-ci.yml`, runner, caching, or delivery-pipeline design and debugging.

## Data, async, docs, and contracts

### alaa-async-messaging ( `$alaa-async-messaging` )

Use it when the Go service or surrounding system needs queues, eventing, retries, DLQs, idempotency, or broker-topology rules.

### alaa-data-layer ( `$alaa-data-layer` )

Use it when the change affects schema behavior, cache policy, locking, tenant-scoped data access, or shared data contracts.

### alaa-docs-farsi ( `$alaa-docs-farsi` )

Use it when the Go task also requires durable repository documentation or human-facing notes in Persian.

### alaa-mono-package ( `$alaa-mono-package` )

Use it when the task changes how a mono-package is structured or consumed.

### alaa-services-contract ( `$alaa-services-contract` )

Use it when the Go service must follow pack-wide service contracts for health, readiness, response shape, naming, or operational behavior.
