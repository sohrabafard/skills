---
name: alaa-golang
description: "Use this skill as the main entrypoint for Go work in Alaa-style systems: HTTP APIs, services behind a trusted gateway, gRPC, workers, dependency choice, testing, debugging, modernization, observability, and production delivery on Kubernetes, OpenShift, Docker, or Swarm. It routes to the right installed Go skills, defaults new HTTP APIs to chi unless the repo or measured constraints justify Fiber, adds Sohrab companion skills when platform or trust boundaries matter, and provides a curated package catalog plus a practical chi guide."
---

# Alaa Golang

## Purpose

Use this skill first for serious Go work in this pack.

It is a router, policy layer, and gap-filler. It does not replace the installed public Go skills. It decides which ones to
load, adds the right Sohrab companion skills, and keeps Go, package, and Codex guidance aligned with your platform and
operating model.

## Environment this skill assumes

- high-concurrency production services
- security-sensitive and observability-sensitive systems
- SLA-minded delivery with explicit failure handling and graceful shutdown
- HTTP APIs behind a trusted gateway
- Redis for cache and coordination, PostgreSQL for OLTP, ClickHouse for analytics
- deployment on Kubernetes or OpenShift, plus local Docker and sometimes Docker Swarm

## Default stance

- start standard-library first and justify every dependency
- for new HTTP APIs, prefer `chi` over `fiber`
- use `fiber` only when the repo already uses it or there is a measured reason to accept `fasthttp`-style tradeoffs
- keep transport thin, config typed, shutdown explicit, and observability built in from day one
- prefer `pgx` plus `sqlc` over heavyweight ORM-first designs for PostgreSQL services in this stack
- prefer explicit worker ownership, bounded concurrency, and context propagation everywhere
- prefer clean code, small interfaces, stable contracts, and behavior-safe changes over framework cleverness

## Fast path

1. Read `references/full-guide.md` for the merged Go baseline.
2. If the task touches an HTTP API, read `references/30-http-api-framework-choice.md` first.
3. If `chi` is chosen or the task is educational, read `references/31-chi-api-guide.md`.
4. Read `references/10-installed-golang-skills.md` and load only the public Go skills that match the task.
5. Read `references/20-sohrab-companions.md` when the task crosses platform, CI, contract, security, or trust boundaries.
6. Read `references/40-production-ready-package-catalog.md` only when dependency choice is part of the task.
7. Read `references/SOURCES.md` when you need live verification or official docs.

## Routing rules

- language and standard-library upgrades: use `golang-modernize` ( `$golang-modernize` )
- layout, architecture, DI, type design, and style: use `golang-project-layout` ( `$golang-project-layout` ), `golang-design-patterns` ( `$golang-design-patterns` ), `golang-dependency-injection` ( `$golang-dependency-injection` ), `golang-structs-interfaces` ( `$golang-structs-interfaces` ), `golang-code-style` ( `$golang-code-style` ), and `golang-naming` ( `$golang-naming` )
- concurrency, cancellation, safety, errors, and runtime debugging: use `golang-concurrency` ( `$golang-concurrency` ), `golang-context` ( `$golang-context` ), `golang-safety` ( `$golang-safety` ), `golang-error-handling` ( `$golang-error-handling` ), and `golang-troubleshooting` ( `$golang-troubleshooting` )
- data and dependency work: use `golang-data-structures` ( `$golang-data-structures` ), `golang-database` ( `$golang-database` ), `golang-dependency-management` ( `$golang-dependency-management` ), and `golang-popular-libraries` ( `$golang-popular-libraries` )
- transport work: use `golang-grpc` ( `$golang-grpc` ) for gRPC and protobuf, and use `golang-cli` ( `$golang-cli` ) for CLIs and jobs
- quality, operations, and delivery: use `golang-testing` ( `$golang-testing` ), `golang-linter` ( `$golang-linter` ), `golang-benchmark` ( `$golang-benchmark` ), `golang-performance` ( `$golang-performance` ), `golang-observability` ( `$golang-observability` ), `golang-security` ( `$golang-security` ), `golang-documentation` ( `$golang-documentation` ), and `golang-continuous-integration` ( `$golang-continuous-integration` )
- if the repo already uses a Samber library, load the matching `golang-samber-*` skill instead of inventing local conventions

## HTTP API rule

For this pack, the default answer for a new HTTP API is `chi`.

Choose `fiber` only when one of these is true:

- the repo already uses Fiber
- the team explicitly wants Fiber's ergonomics and accepts its non-`net/http` semantics
- there is a measured hot-path reason, not a guessed one

Do not switch routers casually in an existing service. Treat router changes as architecture work.

## Subagent strategy

Use subagents only when they create real leverage.

- one read-only subagent can verify live package, release, or framework facts from official docs
- one read-only subagent can inspect the repo for existing framework, logger, DI, config, or package choices
- one implementation-focused subagent can draft a narrow code change only after the baseline is clear

Keep subagents narrow, parallel, and disposable. Use them for research or repo inspection, not for duplicating the same reasoning.

## Reference map

- `references/00-topic-map.md` - very short navigation layer
- `references/full-guide.md` - merged Go baseline and delivery stance
- `references/10-installed-golang-skills.md` - public Go skill routing
- `references/20-sohrab-companions.md` - Sohrab companion skill routing
- `references/30-http-api-framework-choice.md` - `chi` vs `fiber` decision rules
- `references/31-chi-api-guide.md` - practical `chi` guide for this stack
- `references/40-production-ready-package-catalog.md` - curated package list and when to use each package
- `references/SOURCES.md` - live sources and what each source is good for

## Maintenance rules

- keep this file routing-first and compact
- keep detailed package notes, framework guidance, and examples in `references/`
- keep the `chi`-first HTTP API rule consistent across this file, `full-guide.md`, and the package catalog
- keep skill names written with the `$skill-name` form wherever explicit routing helps the agent
- re-check official Go, package, and OpenAI sources whenever version-sensitive wording changes
