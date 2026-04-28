# Alaa Services Contract Topic Map

Use this file to choose the smallest relevant reference file before loading the full guide.

## Service modes

- `Mode 0 - Skill scope and onboarding view`
  - Use when the task is about whether this skill applies, what it standardizes, how to choose the service mode, or auth-specific frontend routing notes for the `auth` service.
  - Read `05-scope-service-modes-and-auth-routing.md` first.
- `Mode A - Any Ala backend service`
  - Use when the task is about `service` identity, route families, `/api/health`, `/api/ready`, readiness checks, response headers, or observability event naming.
  - Read `10-core-service-contract.md` and `20-operational-and-observability-contract.md` first.
- `Mode A+ - Platform observability directive`
  - Use when the task is about OpenTelemetry exporter setup, OTLP endpoint ownership, queryable `trace_id`, exception delivery to SigNoz when Sentry is absent, Collector gateway topology, Prometheus scrape endpoints, metric-family selection, label/cardinality budgets, queue or dependency instrumentation, exemplars, or a shared telemetry contract across Go, Laravel, HAProxy, Vector, WA, OpenFGA, and future services.
  - Read `20-operational-and-observability-contract.md` and `21-alaa-platform-observability-directive.md`.
- `Mode A++ - Deployment and runtime contract`
  - Use when the task is about Arvan Kubernetes versus Docker ownership, Docker Compose or Docker Swarm support, explicit shared-versus-external Postgres mode selection, shared Docker networking, hard shared-infra reuse, duplicate shared-infra prevention, `DB_PROVISION_*` separation, canonical service DNS aliases, gateway DNS or VIP behavior, key ownership, registry usage, SQLite fast-test support, or the shared `service-ci-kit` GitLab CI/CD baseline and thin-wrapper `.gitlab-ci.yml` model for Ala Laravel services.
  - Read `15-deployment-and-runtime-contract.md` after `10-core-service-contract.md`.
- `Mode B - Laravel backend service`
  - Use when the task is about Laravel API response boundaries, Resources, middleware order, public `project_id` validation and resolution, or Laravel-specific route and command expectations.
  - Read `30-trusted-ingress-and-laravel-contract.md` after the core contract.
- `Mode C - Laravel downstream trusted service`
  - Use when the service sits behind the Ala gateway, consumes sanitized trusted headers, or needs to normalize `X-Project-Id`.
  - Read `30-trusted-ingress-and-laravel-contract.md` and pair with `$alaa-trust-gateway-auth`.
- `Mode C+ - Permission catalog consumer`
  - Use when the task is about `config/permissions.php`, permission names, bitmap ids, generated service permission configs, `X-Access` permission mapping, or catalog drift checks.
  - Read `35-permission-catalog-and-service-configs.md` and pair with `$alaa-trust-gateway-auth`.
- `Mode D - Laravel auth-boundary service`
  - Use when the service itself owns the trust boundary and still must satisfy the same outward trusted-ingress behavior.
  - Read `30-trusted-ingress-and-laravel-contract.md` and `50-laravel-copy-baselines.md`.
- `Mode E - Platform flow and boundaries view`
  - Use when the task is about client -> gateway -> service flow, service ownership, the role of `authz-sidecar` or `entitlement-spoa`, `entitlement-api`, `projector`, OpenFGA, `content` versus legacy `vod`, or internal-hop discipline.
  - Read `25-end-to-end-flow-and-boundaries.md`.

## Cross-cutting references

- `20-operational-and-observability-contract.md`
  - Exact `X-Request-Id` and `traceparent` rules, structured log field contract, event and code naming, metrics-boundary rules, and `RequestObservabilityMiddleware`.
- `21-alaa-platform-observability-directive.md`
  - Full telemetry architecture, OTLP/Collector responsibilities, SigNoz/Sentry role split, exception fallback rules, Prometheus scrape rules, shared metric catalog, runtime-specific notes, current service reality, and validation rules for observability work.
- `40-apply-checklist-and-anti-patterns.md`
  - Use before finalizing a contract change or skill-driven implementation review.
- `50-laravel-copy-baselines.md`
  - Use only when you need copy-oriented Laravel baselines after understanding the owning rules, especially for shared `project_id` / `TrustedProjectContext` validation snippets.
- `90-source-map.md`
  - Official-first source map for version-sensitive standards, framework docs, observability docs, and community-source limits.

## Working rule

- Start with the smallest file that owns the rule you need.
- Load `full-guide.md` only when the task is broad enough that split-file navigation would cost more context than it saves.
- When observability design is in scope, treat `20` and `21` as a pair: `20` owns the exact stable surfaces and `21` owns the larger telemetry design.
