# Relevant Sohrab Companion Skills

Use this file when a Go task also crosses one of the Sohrab-owned boundaries in this pack. These skills are already
publicly installed, so route to them by skill name only.

## alaa-workflow

Use `alaa-workflow` when the Go task is long, multi-phase, risky, or spread across multiple files and needs plan and
state artifacts. It keeps execution resumable and auditable instead of turning complex work into ephemeral terminal
chatter.

## alaa-low-noise

Use `alaa-low-noise` when the Go task risks context bloat through large searches, big logs, repo-wide audits, or
long-running commands. It keeps the work reviewable without flooding the terminal or the model context.

## alaa-observability-soc

Use `alaa-observability-soc` when the Go change affects logs, traces, metrics, alerting, incident evidence, or
correlation IDs at the system level. Pair it with `golang-observability` when you need both Go instrumentation details
and Sohrab operational guardrails.

## alaa-security-review

Use `alaa-security-review` when the Go task changes authn, authz, tenant isolation, or another trust boundary. Pair it
with `golang-security` when the code-level hardening and the system-level security review both matter.

## alaa-docker-production

Use `alaa-docker-production` when the Go service also needs production Dockerfile, Docker Compose, image hardening,
shared-network, registry, or container-runtime guidance. This is the delivery companion when Go code ships as a
container.

## caas-arvan-kuber

Use `caas-arvan-kuber` when the Go service is deployed on Arvan CaaS and the Kubernetes, Helm, or delivery rules must
follow Arvan-specific constraints. Do not assume generic Kubernetes defaults beat that platform contract.

## k8s-debug

Use `k8s-debug` when the Go issue is no longer just in the code and now includes failing pods, cluster networking,
deployment rollout problems, or runtime resource pressure. It is the operational debugging companion for Go services on
Kubernetes.

## alaa-docs-farsi

Use `alaa-docs-farsi` when the Go task also requires durable repository docs, architecture notes, onboarding material,
or human-facing operational guidance. It complements `golang-documentation`, which is more Go-doc and package-doc
focused.

## alaa-async-messaging

Use `alaa-async-messaging` when the Go service or surrounding system needs robust eventing, jobs, retries, DLQ behavior,
idempotency, or broker-topology guidance. This is the right companion when concurrency extends into distributed async
flows.

## alaa-data-layer

Use `alaa-data-layer` when the Go change affects schema behavior, Redis locks, cache semantics, or multi-tenant data
access policy. It complements `golang-database`, which owns the Go application-side query and transaction patterns.

## alaa-mono-package

Use `alaa-mono-package` when the Go task lives in a mono-package or changes how the root app consumes an internal
package. It keeps package-boundary decisions consistent with the rest of this pack.

## alaa-services-contract

Use `alaa-services-contract` when the Go service must follow an Ala service contract for health, readiness, envelopes,
observability middleware, deployment expectations, or service naming. This is the contract owner when local preference
should yield to pack-wide service consistency.

## alaa-trust-gateway-auth

Use `alaa-trust-gateway-auth` when the Go service consumes trusted gateway headers, JWT-derived identity, tenant
propagation, or downstream trust semantics. It should own gateway-trust behavior instead of leaving those rules implicit
in application code.

## alaa-haproxy

Use `alaa-haproxy` when the Go service sits behind HAProxy and the task touches TLS termination, header trust, rate
limiting, load balancing, canaries, or HAProxy-side observability. It is the reverse-proxy companion for Go delivery and
edge behavior.
