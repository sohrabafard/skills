---
name: alaa-laravel-architecture
description: "Laravel layer map and legal call graph for Ala services (Controller to Service to Repository to DB): what crosses a boundary, where the cache seam, error envelope, degraded response and domain event are produced, DTO-versus-Resource-versus-Model exposure, provider register-versus-boot placement, and a gate for layer violations, public-id leaks and provider I/O. Use when a change crosses two layers or the public surface: adding or moving a route, controller, service, repository, DTO, resource, policy, binding or event. Do not use for a rule verifiable inside one class (naming, types, method length, patterns in a file) - that is /alaa-php-clean-code. Route design-before-code to /alaa-system-design; envelope, code and metric names to /alaa-services-contract; timeout and page-size values to its failure-load file; degradation doctrine to /alaa-reliability-sla; cache policy to /alaa-data-layer."
---

# Alaa Laravel Architecture

Fix where each decision lands in a Laravel tree, so two agents implementing the same feature in two Ala services produce the same layout.

This skill owns the layer map and the call graph over it, and it is domain-agnostic: it fixes the layout, not the endpoints. **It owns no value.** Everything it touches that carries one — envelope keys, error codes, identifier format, page-size bound, pagination style — is fleet-wide and owned by `/alaa-services-contract` (`$alaa-services-contract`); this skill fixes only which class produces it. No rule here is specific to one service, and the quality bar it is judged against is `alaa-project-constitution references/quality-bar.md`.

Companion skills are written `/name` for Claude Code and `$name` for Codex; both forms name the same skill.

## The ownership test — apply it before writing a rule or opening a reference

**A rule verifiable by reading one class in isolation belongs to `/alaa-php-clean-code` (`$alaa-php-clean-code`). A rule whose verification requires reading two layers, or reading the public surface a caller sees, belongs here.**

Method length, naming, types, injection style, and pattern choice inside a file are all checkable in one file: theirs. That a Controller never reaches a Repository, that no internal identifier reaches a response, that an event is emitted after commit, that caching sits on an interface rather than inside a Service — none of these is visible in any single file: ours. When both skills could state a rule, this skill points and `/alaa-php-clean-code` holds the wording.

## The call graph

These are the legal edges, and the only legal edges:

- `Controller → Service → Repository → DB`
- `Controller → Resource → JSON`
- `Service → Policy/Gate` before any state change or any read the caller is not entitled to
- `Service → domain event`, after the transaction commits

Every forbidden edge, with what to write instead:

| Forbidden edge | Write instead |
|---|---|
| Controller → Repository, Eloquent, or `DB::` | Controller → Service → Repository |
| Controller or Service → `Cache::`/`Redis::` for domain data | a decorator on the repository interface — `references/20-composition-and-boot.md` |
| Service → raw array as API output | Service → DTO → Resource |
| Repository → business rule, authorization decision, or event emission | the Service holds all three |
| Controller or Service → inline validation | a FormRequest, whose `validated()` output the Controller passes on |
| Provider `register()` or `boot()` → cache, Redis, DB, HTTP, filesystem | defer it — `references/20-composition-and-boot.md` |
| Controller → assembling an error or degraded response body | raise a domain exception; one handler renders it — `references/40-degraded-mode.md` |

None of these is a style preference. Each is the edge that produces a defect no single-file review can see, which is why `scripts/architecture-gate.sh` exists.

## Where to read next

`references/00-topic-map.md` maps an observable situation to the one file that answers it. Read it before opening any other reference.

## Before claiming a layer change done

Run `sh scripts/architecture-gate.sh --app-dir app`; exit 0 is required. It is a floor, not a proof: `references/80-acceptance-gate.md` holds the findings, the blind spots, the waiver rule, and the three tests and one documentation obligation that complete a boundary change.

## When NOT to use

- The rule can be checked by reading one class on its own: naming, types, method length, or a pattern
  applied inside a single file. Nothing crosses a boundary, so there is no call graph to test.
- The change stays inside one layer and adds, moves, or removes no route, controller, service, repository,
  DTO, resource, policy, provider binding, or emitted event.
- The task is choosing a design before any code exists, or picking a timeout, retry, page-size, or
  envelope value. The routing table below names each owner.

## What this skill does not own

Where a rule here and a rule in the owning skill disagree, **the owning skill wins and the statement here is deleted** rather than kept as a second opinion.

| Not owned here | Owner |
|---|---|
| What makes a test a test, which layer a behaviour is tested at, doubles, proof levels, flake | `/alaa-testing-strategy` — `$alaa-testing-strategy` |
| Failure doctrine: deadlines, retries, breakers, bulkheads, admission and shedding, degradation, idempotency, error budgets | `/alaa-reliability-sla` — `$alaa-reliability-sla` |
| Every timeout, retry count, pool bound, acquire wait, shed threshold, and page-size bound | `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` |
| Envelope keys and values, error and event code names, public identifier format, health and readiness shapes, trusted headers, metric names, the deprecation procedure | `/alaa-services-contract` — `$alaa-services-contract` |
| Whether a signal is required, its cardinality and sampling budget, alerting and retention | `/alaa-observability-soc` — `$alaa-observability-soc`. On *whether* required, SOC wins; on *what it is called*, the contract wins. |
| Class shape, naming, types, method and class size, SOLID, pattern selection, the repository-first persistence rule, PATCH absent-versus-null semantics | `/alaa-php-clean-code` — `$alaa-php-clean-code` |
| Cache key design, TTL, invalidation strategy, stampede control, Redis-down cache behaviour, schema, indexes, isolation, lock and pool mechanics | `/alaa-data-layer` — `$alaa-data-layer` |
| The repository-pattern completeness gate that precedes any caching | `alaa-data-layer references/50-redis-laravel-octane.md`, "Step 0" |
| Broker topology, prefetch, acknowledgement, consumer concurrency, retry and DLQ mechanics, event delivery semantics | `/alaa-async-messaging` — `$alaa-async-messaging`; RabbitMQ transport `/alaa-laravel-job-rabbitmq` — `$alaa-laravel-job-rabbitmq` |
| Complexity budgets, the real bound on a growing input, structure choice, the whole N+1 family | `/alaa-algorithms-data-structures` — `$alaa-algorithms-data-structures` |
| Whether a list route paginates, its ordering tuple, its index, and the cursor's shape | `/alaa-keyset-pagination` — `$alaa-keyset-pagination` |
| Tenant derivation, JWT verification, header sanitisation, who may assert a trusted header | `/alaa-trust-gateway-auth` — `$alaa-trust-gateway-auth`; object-level relationship authorization `/openfga` — `$openfga` |
| Threat classes, review triggers, the fail-closed discriminator, every security verdict | `/alaa-security-review` — `$alaa-security-review` |
| What a long-lived worker may retain between requests, reset mechanics, worker sizing | `/alaa-octane-performance` — `$alaa-octane-performance` |
| Pre-implementation design: bounding a subsystem, extend-versus-new-service, contract-before-code, data ownership, candidate comparison | `/alaa-system-design` — `$alaa-system-design`. Read it **before** the change, not during it, whenever the change meets any of the six trigger conditions that skill lists — it owns the list. It settles the answer; this skill places it in a Laravel tree. |
| Docs workflow, README, Postman, and diagram alignment | `/alaa-repo-docs` — `$alaa-repo-docs`; docblocks and artifact rules `alaa-php-clean-code references/documentation-and-artifacts.md` |
| Running the gate as a pipeline stage, static analysis, and release gating | `/alaa-cicd-laravel-postgres` — `$alaa-cicd-laravel-postgres` |
| Project policy, archetypes, and the ten-criterion quality bar itself | `/alaa-project-constitution` — `$alaa-project-constitution` |
| Model and effort selection, prompting, skill authoring | `/alaa-prompting-guide` — `$alaa-prompting-guide` |
| Multi-lane planning and resumable state | `/alaa-workflow` — `$alaa-workflow`; lane orchestration `/alaa-cc-orchestrator` — `$alaa-codex-orchestrator` |
