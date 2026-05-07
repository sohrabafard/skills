---
name: alaa-golang
description: "Use this skill as the main entrypoint for Go work in Alaa-style systems: chi or Fiber HTTP APIs, services behind a trusted gateway, gRPC, GraphQL, CLIs, workers, repositories, Redis cache layers, testing, TDD, clean architecture, design patterns, concurrency, observability, security, and production delivery. It routes to installed Go skills, routes Fiber work to `alaa-golang-fiber`, teaches chi for small raw services, recommends Fiber for raw large/high-concurrency services, and enforces repository pattern, Redis cache safety, TDD, and `99.99%+` service readiness."
---

# Alaa Golang

## Purpose

Use this skill first for serious Go work in this pack.

It is a router, policy layer, and local gap-filler. It does not replace the installed public Go skills. It chooses the
right Go skill, adds Sohrab companion skills, and keeps framework, repository, cache, testing, and production rules
aligned with this platform.

## When NOT to use

- Do not use for non-Go implementation work.
- Do not use for frontend-only, Terraform-only, Kubernetes-only, or CI-only tasks unless Go service behavior is involved.
- Do not use as a substitute for a narrower public Go skill when the task is only one isolated Go topic.
- Do not use to migrate an existing chi service to Fiber, or Fiber to chi, unless the user explicitly asks for migration.

## Default stance

- Start with repository evidence: `go.mod`, imports, routes, tests, docs, and existing conventions.
- Explicit user framework choice wins.
- Existing repo framework wins.
- Raw small/simple HTTP services should use chi.
- Raw large, high-concurrency, latency-sensitive, or SLA-heavy HTTP services should use Fiber and `$alaa-golang-fiber`.
- DB-backed services must use repository pattern.
- Redis is a cache layer unless the repo explicitly defines another role.
- Behavior-changing work must start with a failing or updated test.
- Keep handlers thin, use cases explicit, repositories isolated, context propagated, and shutdown deterministic.
- Prefer standard library and small dependencies unless a dependency removes real complexity.

## Fast path

1. Read `references/full-guide.md` for the Go service baseline.
2. For HTTP APIs, read `references/30-http-api-framework-choice.md`.
3. If chi is chosen or already present, read `references/31-chi-api-guide.md`.
4. If Fiber is chosen or already present, load `alaa-golang-fiber` ( `$alaa-golang-fiber` ).
5. Read `references/10-installed-golang-skills.md` and load only the matching public Go skills.
6. Read `references/60-service-architecture-patterns.md` for DB-backed services.
7. Read `references/61-redis-cache-layer.md` when Redis cache behavior is involved.
8. Read `references/62-clean-code-and-patterns.md` for architecture or code quality work.
9. Read `references/63-tdd-and-testing-discipline.md` before behavior-changing implementation.
10. Read `references/20-sohrab-companions.md` when platform, trust, data, delivery, or contracts matter.
11. Read `references/SOURCES.md` when version-sensitive claims need live verification.

## Routing rules

- language upgrades and modern idioms: use `golang-modernize` ( `$golang-modernize` )
- project layout, architecture, DI, type design, style, and naming: use `golang-project-layout` ( `$golang-project-layout` ), `golang-design-patterns` ( `$golang-design-patterns` ), `golang-dependency-injection` ( `$golang-dependency-injection` ), `golang-structs-interfaces` ( `$golang-structs-interfaces` ), `golang-code-style` ( `$golang-code-style` ), and `golang-naming` ( `$golang-naming` )
- concurrency, cancellation, safety, errors, and debugging: use `golang-concurrency` ( `$golang-concurrency` ), `golang-context` ( `$golang-context` ), `golang-safety` ( `$golang-safety` ), `golang-error-handling` ( `$golang-error-handling` ), and `golang-troubleshooting` ( `$golang-troubleshooting` )
- data, Redis, repositories, and dependencies: use `golang-database` ( `$golang-database` ), `golang-data-structures` ( `$golang-data-structures` ), `golang-dependency-management` ( `$golang-dependency-management` ), and `golang-popular-libraries` ( `$golang-popular-libraries` ), then apply local repository and cache references
- HTTP transport: use this skill for chi decisions and `$alaa-golang-fiber` for Fiber; use `golang-swagger` ( `$golang-swagger` ) for Swagger/OpenAPI
- gRPC and GraphQL: use `golang-grpc` ( `$golang-grpc` ) and `golang-graphql` ( `$golang-graphql` )
- CLIs and config: use `golang-cli` ( `$golang-cli` ), `golang-spf13-cobra` ( `$golang-spf13-cobra` ), and `golang-spf13-viper` ( `$golang-spf13-viper` ) when those packages appear
- DI frameworks: prefer manual DI first; route existing `wire`, `dig`, `fx`, or `samber/do` usage to the matching public Go skill
- quality, operations, and delivery: use `golang-testing` ( `$golang-testing` ), `golang-stretchr-testify` ( `$golang-stretchr-testify` ), `golang-lint` ( `$golang-lint` ), `golang-benchmark` ( `$golang-benchmark` ), `golang-performance` ( `$golang-performance` ), `golang-observability` ( `$golang-observability` ), `golang-security` ( `$golang-security` ), `golang-documentation` ( `$golang-documentation` ), and `golang-continuous-integration` ( `$golang-continuous-integration` )
- Samber packages: if the repo imports a Samber library, load the matching `golang-samber-*` skill

## Mandatory local rules

- Do not put SQL, Redis, queue calls, or business rules in HTTP handlers.
- Keep framework types out of domain, use case, and repository packages.
- Use repository interfaces at use case boundaries and infrastructure implementations behind them.
- Use cache-aside Redis by default and make invalidation explicit.
- Add or update unit tests before implementation for behavior changes.
- Run focused tests, then `go test ./...`; add `go test -race ./...` for shared state, cache, goroutines, or workers.
- Preserve trusted-gateway and service-contract rules; do not trust client-supplied identity or tenant context.

## Reference map

- `references/00-topic-map.md` - shortest reading path
- `references/full-guide.md` - merged Go service baseline
- `references/10-installed-golang-skills.md` - public Go skill routing
- `references/20-sohrab-companions.md` - Sohrab companion skill routing
- `references/30-http-api-framework-choice.md` - chi vs Fiber decision rules
- `references/31-chi-api-guide.md` - chi guide for small/simple services
- `references/40-production-ready-package-catalog.md` - curated package list
- `references/50-gap-coverage.md` - local gap policy
- `references/60-service-architecture-patterns.md` - repository pattern and service boundaries
- `references/61-redis-cache-layer.md` - Redis cache layer rules
- `references/62-clean-code-and-patterns.md` - Go clean code and patterns
- `references/63-tdd-and-testing-discipline.md` - TDD and test policy
- `references/SOURCES.md` - live source map

## Maintenance rules

- Keep this file compact and routing-first.
- Keep detailed framework, package, repository, Redis, and testing guidance in `references/`.
- Keep `references/10-installed-golang-skills.md` in exact parity with `vendor/cc-skills-golang/skills`.
- Keep skill names written with `$skill-name` where explicit routing helps the agent.
