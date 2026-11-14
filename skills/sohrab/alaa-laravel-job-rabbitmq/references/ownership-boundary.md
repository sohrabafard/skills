# Ownership boundary — what this skill does not own

Read this file before you state a rule about a number, a name, an observability level, messaging architecture, deployment, test design, security, code shape, complexity or worker hygiene. Where an entry names another owner, point at it and write nothing of your own on that ground. `SKILL.md`, "Ownership boundary", owns the rule that the named owner wins on conflict.

- **The ten-point quality bar itself** — `alaa-project-constitution references/quality-bar.md`.
- **Failure behaviour doctrine** (retries, backoff, deadlines, breakers, degradation, the idempotency
  contract, error budgets) — `/alaa-reliability-sla`. **Every number** it implies —
  timeout, retry count, prefetch value, delivery limit, threshold, margin —
  `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.
- **Names**: queue, exchange and vhost names and event-versus-command topology in
  `alaa-services-contract references/23-queue-and-exchange-registry.md`; log, event and metric names in
  `alaa-services-contract references/24-metric-registry.md` — `/alaa-services-contract`.
- **Observability requirement levels, gates and alerts** — `/alaa-observability-soc`.
- **Messaging architecture**: transport choice, event design, fan-out, DLQ replay procedure, prefetch tuning
  — `/alaa-async-messaging`. Retry and DLQ **strategy** is `/alaa-reliability-sla`,
  not this skill and not `/alaa-async-messaging`.
- **Deployment**: chart keys, probes, rollout strategy and autoscaler shapes — `/alaa-k8s-helm`; runtime image contents including `ext-pcntl` — `/alaa-docker-production`; broker cluster, vhost and permission administration and Arvan defaults —
  `/caas-arvan-kuber`.
- **Correctness and testability**: what makes a test a test, layers, doubles, proof strength, flake —
  `/alaa-testing-strategy`.
- **Security**: fail-closed versus fail-open, threat classes, untrusted input — `/alaa-security-review`; trusted headers and tenant derivation — `/alaa-trust-gateway-auth`.
- **Clean code, SOLID and design-pattern selection** — `alaa-php-clean-code references/design-patterns.md` via `/alaa-php-clean-code`.
- **Complexity budgets, structure choice and the N+1 family inside handlers** —
  `/alaa-algorithms-data-structures`.
- **Long-lived worker hygiene, cross-request state and memory drift** — `/alaa-octane-performance`. **Pre-implementation design pass** — `/alaa-system-design`. **Generated runtime wrappers** —
  `/service-runtime-kit-governance`. **Plan files and phasing** —
  `/alaa-workflow`.
