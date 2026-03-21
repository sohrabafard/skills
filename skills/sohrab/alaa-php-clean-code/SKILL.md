---
name: alaa-php-clean-code
description: "Shared PHP and Laravel clean-code baseline for agent-written code: choose and apply design patterns consistently (interfaces + dependency injection, Repository, Factory, Strategy, DTO, value objects), use modern PHP 8.x features safely, enforce type safety and PSR/PER standards, follow Laravel best practices for requests, resources, authorization, Eloquent usage, performance, error handling, and documentation quality, and orchestrate coding work efficiently with subagents and parallel local work when explicitly allowed by the user and environment. Use when Codex writes, reviews, or refactors PHP/Laravel code and needs outputs that stay consistent across projects and agents."
---

# Purpose
Make PHP / Laravel code written by different agents look intentional, consistent, and easy to maintain.

This skill owns code shape inside files, classes, and methods:
- clean-code defaults
- SOLID usage
- design-pattern selection
- PHP 8.x feature usage
- type safety
- PSR / PER baseline
- Laravel code-level best practices
- app-level performance hygiene
- error-handling defaults

Use this skill before writing or reviewing PHP / Laravel code. If another companion skill also applies, this skill still provides the default coding baseline unless that companion explicitly overrides it.

# Scope and boundaries
- `alaa-laravel-architecture` owns service/module layering, API envelopes, `public_id`, and outbox-oriented application architecture.
- `alaa-data-layer` owns schema, indexes, SQL/query-plan tuning, pooling, concurrency, and Redis data primitives.
- `alaa-octane-performance` owns long-lived worker hygiene, Octane hot paths, and request-boundary reset rules.
- `alaa-async-messaging` and `alaa-laravel-job-rabbitmq` own queue, broker, retry, DLQ, and message-plane design.
- `alaa-security-review` owns security review gates and high-risk auth, tenant, validation, input, file, URL, and abuse analysis.
- `alaa-trust-gateway-auth` owns gateway-trust semantics for trusted headers, JWT-derived request identity, tenant context propagation, and downstream trust-boundary rules behind the Ala gateway.
- `alaa-observability-soc` owns logging schemas, tracing, metrics, alerts, Sentry, and runbooks.
- `alaa-cicd-laravel-postgres` owns CI, quality-gate automation, and pipeline behavior for Pint / PHPStan / tests.

- `alaa-docs-farsi` owns repo-wide documentation passes, README/docs/Postman sync, and docs-consistency guardian workflows. When this skill requires docs updates, use `alaa-docs-farsi` for alignment workflow but keep the resulting docs in simple, fluent English unless the user explicitly asks for another language.
- `openai-docs` owns authoritative, current documentation guidance for OpenAI products, APIs, models, prompts, and agent workflows. Read it when project docs or examples touch OpenAI-specific behavior and need official citations or current product guidance.

Do not duplicate or contradict companion skills. Keep only the code-level default here and hand off deeper concerns to the specialist skill.

# Source basis
This skill is grounded in:
- Laravel 13.x official docs
- PHP manual for PHP 8.x
- PHP-FIG PSR / PER specifications
- official OpenAI guidance for concise, boundary-driven, validation-oriented agent instructions
- official OpenAI guidance on agent orchestration, multi-agent patterns, parallel execution, and workflow-level evaluation

Repository, Factory, Strategy, DTO, and Value Object guidance in this skill are engineering conventions. They are not official PHP language requirements. Use them only when they buy clarity, consistency, or a meaningful boundary.

# Agent workflow
1. Inspect the repository and existing conventions before adding abstractions.
2. If the task changes module boundaries, API contracts, or outbox rules, read `alaa-laravel-architecture` first, then apply this skill inside those boundaries.
3. If the task touches gateway-trusted headers, downstream auth context, request identity propagation, or tenant context derived from the Ala gateway, read `alaa-trust-gateway-auth` before making PHP / Laravel code changes.
4. If the task changes behavior, request/response contracts, env vars, setup flows, or developer-facing usage, read `references/documentation-and-artifacts.md` and apply its docblock, README, Postman, environment-file, and diagram rules. Use `alaa-docs-farsi` for docs-alignment workflow, but keep the output in simple, fluent English unless the user explicitly asks for another language.
5. If the docs touch OpenAI products, APIs, models, prompts, or agent workflows and need official current references, read `openai-docs` before updating those docs.
6. If the user explicitly asks for subagents, delegation, or parallel agent work, read `references/agent-orchestration.md` and decide whether the task should stay single-agent or use a manager-plus-subagents workflow.
7. Choose the simplest pattern that solves the current problem. Do not stack patterns for aesthetics.
8. Prefer explicit types, immutable boundary objects, and constructor injection.
9. Keep side effects at the edges; keep core logic deterministic and easy to test.
10. Preserve naming, folder structure, and established team conventions unless the user explicitly asks for a change.
11. Add or update tests for behavior changes, then align all impacted documentation artifacts before claiming the work is done.

# Non-negotiable defaults
- Use `declare(strict_types=1);` in new PHP files unless the repository clearly avoids it.
- Type parameters, return values, and properties unless the framework contract prevents it.
- Prefer `readonly` DTOs and value objects when their semantics are stable.
- Prefer `DateTimeImmutable` for time values. Use `Psr\Clock\ClockInterface` when a clock seam materially improves testing or portability.
- Prefer enums plus `match` for closed sets and state branching.
- Prefer composition over inheritance.
- Keep classes focused: one primary responsibility, one main reason to change.
- Prefer explicit dependencies over service location.
- Keep validation, authorization, persistence, serialization, and transport concerns near the framework edges.
- Avoid hidden queries, hidden mutations, and hidden IO in getters, casts, accessors, or helper methods.
- Catch exceptions at boundaries to translate them. Do not bury failures with `null`, `false`, or silent logs.

# Pattern-selection guide
Read the following references selectively:
- `references/design-patterns.md`
  Read for Repository, Factory, Strategy, DTO, Value Object, Query Object / Filter DTO, and exception-translation guidance.
- `references/php-modern-and-psr.md`
  Read for PHP 8.x features, type safety, PSR / PER usage, error handling, low-level performance, and language-level anti-patterns.
- `references/laravel-best-practices.md`
  Read for service container / contracts / facades, Form Requests, API Resources, policies / gates, eager loading, N+1 prevention, chunking / lazy / cursor, and service-provider hygiene.
- `references/documentation-and-artifacts.md`
  Read when behavior changes require docblocks, README/docs updates, Postman collection v2.1 updates, environment artifacts, or request-flow diagrams.
- `references/agent-orchestration.md`
  Read when the task is large enough to benefit from subagents, delegation, or parallel local work. Use it only when the user explicitly asks for subagents, delegation, or parallel agent work and the environment policy allows it.

# Subagents and parallel work
- Start with a single-agent plan. Split only when the task has independent tracks, prompt complexity is getting unwieldy, or tool overlap is degrading quality.
- Prefer a manager pattern for coding work: one main agent keeps plan ownership, repository context, and final synthesis; subagents act as tools, workers, or focused reviewers.
- In environments that gate subagents behind explicit permission, do not spawn subagents unless the user explicitly asks for subagents, delegation, or parallel agent work.
- Delegate only bounded, self-contained subtasks with clear ownership and disjoint write scopes.
- Keep the immediate blocking next step local when possible; delegate sidecar or parallelizable work instead.
- While subagents run, continue non-overlapping local work instead of waiting idle.
- Use the environment's parallel tool-call facility for independent reads, searches, listings, and safe validations. In Codex desktop, that means `multi_tool_use.parallel` for independent developer-tool calls.
- Do not parallelize overlapping writes, commands that mutate shared state, or tools that explicitly should not run in parallel.
- Use fresh subagents for independent review or forward-checks when the task is tricky, and pass only the minimum context needed to avoid leaking the intended answer.

# Documentation baseline
- Documentation is part of done when behavior, contracts, setup steps, env vars, flows, or examples change.
- Add enough English docblocks to serve two goals:
  - richer type information when native PHP types are not enough
  - better human understanding of intent, invariants, side effects, units, formats, and non-obvious behavior
- Use docblocks for high-value cases such as array shapes, collection item types, template/generic hints for static analysis, callable signatures, thrown exceptions, and domain-specific invariants.
- Do not add noisy docblocks that merely restate an obvious method name or native scalar type.
- Keep docblocks in simple, fluent English.
- Treat stale docblocks as bugs. Update or remove them when code changes.
- Keep README, detailed docs, Postman collection, and environment artifacts aligned with the current code and current request/response behavior.
- Prefer Postman collection format v2.1.
- Keep one request item per operation. Save multiple response examples on that same request item for success and error variants instead of cloning separate request items only to show different responses.
- Include realistic dummy data, useful request or test scripts, saved examples for the important success and failure cases, and a separate environment file stored next to the collection.
- Keep request-flow diagrams updated in README or docs so backend and client engineers can see sequence, dependencies, and ordering. Mermaid is preferred when practical.
- Remove or replace stale docs and duplicate fragments, but do not delete high-value detail just to make docs shorter.
- When docs touch OpenAI-specific behavior, use `openai-docs` for official current references.

# Default decisions for common questions

## Interfaces and dependency injection
- Prefer constructor injection for growing classes and reusable collaborators.
- Add an interface only when there is a real seam: multiple implementations, external integration, package boundary, or a test double that improves clarity.
- Prefer injecting a concrete class when the dependency is stable, local, and zero-configuration resolution already works.
- Never inject the container into domain or service classes to fetch dependencies manually.

## Repository pattern
- Use a repository when there is a real persistence boundary, non-trivial query composition, aggregate-oriented persistence, or a store you may need to swap or isolate behind a stable contract.
- Do not create one repository per model by habit.
- Do not build generic base repositories that only mirror Eloquent or Query Builder CRUD.

## Factory pattern
- Use a factory when object creation enforces invariants, chooses between strategies, or assembles a graph that would otherwise leak branching logic into many call sites.
- Do not wrap `new` with a factory when construction is already obvious.
- Treat Eloquent model factories as testing and seeding tools, not as the default production factory pattern.

## DTOs and value objects
- Use DTOs at layer boundaries and for validated or filtered input.
- Use value objects for domain concepts with behavior or invariants such as `Money`, `Email`, `TenantId`, or `DateRange`.
- Do not pass raw associative arrays across layers when the shape matters.

## Strategy pattern
- Use it for interchangeable algorithms or provider-specific behavior.
- Prefer a small interface plus a resolver or factory over giant `switch` statements scattered across services.
- Do not introduce a strategy hierarchy when only one stable implementation exists.

## Laravel edge patterns
- Use Form Requests for complex validation and request authorization.
- Use API Resources for stable JSON contracts.
- Use policies or gates for authorization.
- Keep facades at framework edges. Prefer DI in services that may grow or need reuse.

# Performance baseline
- Prevent N+1 by default: eager load intentionally before loops or resources touch relations.
- Use `withCount`, `withExists`, selective `select(...)`, and resource helpers like `whenLoaded()` and `whenCounted()` to avoid accidental queries.
- For large datasets:
  - use `chunk()` for batch processing when iteration order is stable and you are not mutating the driving key
  - use `chunkById()` or `lazyById()` when updating rows during iteration
  - use `lazy()` for memory-friendly streaming when eager loading is not required
  - use `cursor()` cautiously; it cannot eager load relationships and may still hit PDO buffering limits
- For Octane or hot-path tuning, switch to `alaa-octane-performance`.
- For index or query-plan work, switch to `alaa-data-layer`.

# Error-handling baseline
- Throw specific exceptions with clear ownership.
- Translate exceptions centrally at HTTP, CLI, and queue boundaries.
- Keep exception messages safe for logs and clients. Put debugging context in structured logs, not user-facing strings.
- Do not catch `Throwable` unless you are at a real boundary and you rethrow or map it deliberately.
- For security-sensitive error behavior, follow `alaa-security-review`.
- For observability fields and alert semantics, follow `alaa-observability-soc`.

# SOLID interpretation for this repo
- Single Responsibility: split classes by reason to change, not by line count.
- Open / Closed: prefer extension through interfaces, strategies, and composition before branching across many call sites.
- Liskov: keep subtype contracts compatible; do not weaken preconditions or widen side effects.
- Interface Segregation: prefer small, role-based interfaces over god interfaces.
- Dependency Inversion: high-level policy depends on abstractions, but do not force abstractions where a concrete class is clearer and more stable.

Apply SOLID pragmatically. Clarity, fewer moving parts, and repo consistency beat textbook purity.

# Global anti-patterns
- Service locator or container injection in app code.
- Static helper classes that hide mutable state or IO.
- Fat controllers, fat jobs, fat listeners, or god services.
- Primitive obsession for domain concepts.
- Raw arrays used as de facto DTOs across layers.
- Generic repositories, managers, helpers, or util classes with vague responsibility.
- Overusing inheritance when composition or a value object is simpler.
- Dynamic properties, magic behavior, or hidden serialization tricks in new code.
- Named-argument usage across unstable public APIs where parameter renames would become breaking changes.
- Micro-optimizing without measurement or a clear hot path.

# Output contract when applying this skill
- State which pattern(s) you chose and why if the choice is non-obvious.
- Keep diffs minimal and aligned with repo conventions.
- Mention when you intentionally did *not* introduce a repository, interface, factory, or strategy.
- If behavior or contracts changed, either update the related docblocks, README/docs, Postman collection v2.1, environment artifact, and request-flow diagrams, or explicitly state why no documentation change was needed.
- If another specialist skill should own part of the work, say so and follow it instead of duplicating its rules.





