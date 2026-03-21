---
name: alaa-php-clean-code
description: "Deterministic PHP 8.5 / Laravel 13 clean-code baseline for writing, reviewing, and refactoring code with one-author consistency: enforce naming, SOLID, explicit types, modern PHP features, Laravel edge patterns, and mode-aware refactors (scoped soft, scoped hard with contract preservation, whole-project preserve-local, whole-project normalize-to-Alaa). Use before changing PHP/Laravel code; route to companion skills mandatorily when architecture, gateway trust, data, async, Octane, security, observability, CI, docs, or MongoDB concerns are in scope."
---

# Purpose
Make PHP / Laravel code written by different agents look like it came from one careful author.

This skill owns code shape inside files, classes, methods, and local module boundaries:
- naming and code-shape consistency
- clean-code defaults
- pragmatic SOLID usage
- design-pattern selection
- PHP 8.5 feature usage and type safety
- PSR / PER baseline
- Laravel code-level best practices
- local performance hygiene
- boundary-first error handling
- mode-aware refactor discipline

Use this skill before writing, reviewing, or refactoring PHP / Laravel code. If a companion skill also applies, this skill remains the default code-quality baseline inside that companion skill's boundaries.

# When to use
Use this skill when the task includes any of the following:
- writing a new PHP or Laravel slice
- refactoring a controller, request, service, repository, job, listener, resource, policy, DTO, value object, strategy, factory, command, or support class
- cleaning up duplicated logic, weak abstractions, vague naming, or hidden side effects
- making a PHP / Laravel codebase more consistent across modules or across multiple agents
- performing a whole-project cleanup or normalization pass

# Compatibility target
Target repositories using:
- PHP 8.5
- Laravel 13

Default target in this skill pack is Laravel 13 on PHP 8.5.

If a repository is older or mid-upgrade, follow repo reality first and use the newest features only where the runtime and toolchain support them safely. Do not let a Laravel 13 repository drift back to Laravel 12 conventions during new code generation, refactors, reviews, or upgrade planning.

# Laravel 13 baseline
Apply this section whenever the repository already targets Laravel 13 or the task is a Laravel 12 -> 13 upgrade, follow-up refactor, review, or plan.

- Treat Laravel 13 as the primary framework target, not as a dual 12/13 baseline.
- For upgrade work, audit the official dependency bumps first:
  - `laravel/framework` -> `^13.0`
  - `laravel/boost` -> `^2.0` when installed
  - `laravel/tinker` -> `^3.0` when installed
  - `phpunit/phpunit` -> `^12.0` when installed
  - `pestphp/pest` -> `^4.0` when installed
- Compare framework-owned files against the Laravel 13 application skeleton before carrying old bootstrap, config, or test boilerplate forward.
- Update direct CSRF middleware references from `VerifyCsrfToken` or `ValidateCsrfToken` to `PreventRequestForgery` when touching middleware registration, route exclusions, or tests.
- Audit cache payloads against `cache.serializable_classes`; prefer arrays and scalars unless an explicit allow-list of cached classes is justified.
- Preserve Laravel 12-era generated cache or session names only through explicit `CACHE_PREFIX`, `REDIS_PREFIX`, and `SESSION_COOKIE` config. Do not assume old framework fallbacks still apply.
- When code listens to queue events or queue telemetry, account for `JobAttempted::$exception` and `QueueBusy::$connectionName`.
- Re-check domain route precedence, custom morph pivot table names, `Container::call` nullable defaults, Bootstrap pagination view names, `Str` factory reset behavior in tests, and `Js::from` unicode expectations when those surfaces exist.
- Be cautious with named arguments when calling Laravel framework methods; parameter names are not part of Laravel's backwards-compatibility promise.
- Prefer Laravel 13 conveniences only when they reduce custom code or improve clarity:
  - `Queue::route(...)` for central queue / connection routing
  - queue attributes such as `#[Tries]`, `#[Backoff]`, `#[Timeout]`, and `#[FailOnTimeout]`
  - `PreventRequestForgery` middleware configuration APIs
  - first-party JSON:API resources when the contract really is JSON:API
- Do not introduce Laravel AI SDK, semantic search, vector search, or JSON:API resources just because Laravel 13 offers them. Add them only when the repository already uses them or the user explicitly asks for them.

# Ownership and companion-skill boundaries
This skill owns code quality inside the chosen architecture. It does not replace specialist skills.

- `alaa-workflow` owns the mandatory plan-and-report workflow for non-trivial, multi-file, behavior-changing, or whole-project tasks.
- `alaa-laravel-architecture` owns layering, API envelopes, `public_id`, DTO boundaries, and outbox-oriented Laravel architecture.
- `alaa-trust-gateway-auth` owns gateway-trust semantics for trusted headers, JWT-derived request identity, tenant context propagation, and downstream trust rules behind the Ala gateway.
- `alaa-data-layer` owns schema, migrations, indexes, query plans, concurrency, pooling, and Redis data primitives.
- `alaa-octane-performance` owns long-lived worker hygiene, request reset rules, and Octane hot-path behavior.
- `alaa-async-messaging` and `alaa-laravel-job-rabbitmq` own queue, broker, retry, DLQ, idempotency, and message-plane design.
- `alaa-security-review` owns security review gates and high-risk auth, tenant, validation, file, URL, and abuse analysis.
- `alaa-observability-soc` owns logging schemas, traces, metrics, alerts, Sentry, and operational runbooks.
- `alaa-cicd-laravel-postgres` owns CI, quality-gate automation, Pint, PHPStan, and pipeline behavior.
- `alaa-docs-farsi` owns repo-wide docs-alignment workflow, Postman sync, and docs consistency checks. When this skill requires docs updates, use that workflow but keep the resulting docs in simple, fluent English unless the user explicitly asks for another language.
- `openai-docs` owns authoritative, current guidance for OpenAI APIs, models, prompts, tools, agent workflows, and product behavior. Read it when docs, examples, or integration notes touch OpenAI-specific behavior and need official current references or citations.
- `alaa-mongodb-patterns` applies only when the repository already uses MongoDB or the user explicitly requests MongoDB work.

Do not duplicate or contradict companion skills. Route to them when their trigger fires, then apply this skill inside those boundaries.

# Mandatory operating model
Do not skip these steps.

1. Classify the task mode using `references/refactor-modes.md`.
2. If the task is non-trivial, multi-file, behavior-changing, or whole-project, read `alaa-workflow` first and create or update the required plan artifact.
3. Run the companion-skill routing checklist in `references/companion-skill-routing.md`. Read every required companion skill before editing affected code.
4. In Laravel repositories, check whether `laravel/boost` is installed and usable. If it is available, use Boost as the first Laravel-aware inspection and documentation layer before making framework, package, schema, route, config, or runtime assumptions. Prefer Boost MCP tools and Boost documentation search when relevant, but keep explicit user instructions, repo-local rules, this skill, and any triggered companion skills as the governing source for code shape, naming, refactor mode, and contract preservation.
5. Inspect the repository's current conventions, then decide whether the task should preserve local conventions or normalize toward the Alaa convention set.
6. Read `references/consistency-and-naming.md` before renaming classes, methods, namespaces, files, folders, or concepts.
7. Read the technical references that fit the change: patterns, modern PHP / PSR, Laravel edge practices, docs artifacts, and agent orchestration.
8. Implement the smallest coherent change set that satisfies the selected mode.
9. Validate behavior, tests, and documentation alignment before calling the work done.

# Task-mode defaults
Task mode is mandatory. If the user does not specify one, infer the safest option.

- Default to `scoped-soft` for new code and local refactors.
- Use `scoped-hard-contract-preserving` when the user asks for a deeper internal cleanup but still expects API and public contracts to remain stable.
- Default to `whole-project-preserve-local` when the user asks for a repo-wide cleanup without explicitly requesting a global Alaa normalization.
- Use `whole-project-normalize-alaa` only when the user explicitly wants repo-wide standardization toward one global Alaa convention set.
- For new code or local refactors, keep the new or touched slice fully aligned with this skill and refactor adjacent code only as far as needed to keep behavior safe, contracts intact, and the local design coherent.

Read `references/refactor-modes.md` whenever the task includes refactoring, new slice design, or more than one touched file.

# Companion-skill routing summary
Routing is mandatory, not optional advice.

Read `references/companion-skill-routing.md` for the full checklist. The short version is:
- Read `alaa-workflow` for non-trivial, multi-file, behavior-changing, or whole-project work.
- Read `alaa-laravel-architecture` before changing module boundaries, API contracts, `public_id` handling, DTO boundaries, cross-layer flow, or outbox behavior.
- Read `alaa-trust-gateway-auth` before touching trusted headers, request identity, tenant or project derivation, step-up auth, downstream auth propagation, or any Ala-gateway boundary.
- Read `alaa-data-layer` before touching migrations, queries, indexes, transactions, tenant scoping in persistence, Redis primitives, or data concurrency.
- Read `alaa-octane-performance` before touching Octane, Swoole, RoadRunner, hot paths, singletons, request-scoped state, or long-lived worker behavior.
- Read `alaa-async-messaging` before changing jobs, events, consumers, retries, idempotency, outbox consumers, or message-driven side effects.
- Read `alaa-laravel-job-rabbitmq` when the async surface includes RabbitMQ, AMQP topology, Laravel RabbitMQ jobs, DLQ, or queue transport details.
- Read `alaa-security-review` before auth, authorization, validation, file handling, URL fetching, secrets, tenancy, privilege, or externally facing trust surfaces.
- Read `alaa-observability-soc` before changing logs, traces, metrics, alerts, correlation IDs, or Sentry behavior.
- Read `alaa-cicd-laravel-postgres` before changing CI, static analysis, test gating, repo quality gates, or pipeline commands.
- Read `alaa-docs-farsi` when README, docs, Postman, or diagrams must change.
- Read `openai-docs` when docs, examples, or integration notes touch OpenAI APIs, models, prompts, tools, or agent workflows and need current official guidance or citations.
- Read `alaa-mongodb-patterns` only for MongoDB repositories or MongoDB-specific requests.

If a trigger fires, do not continue the affected part of the task until that skill has been read.

# Core consistency rules
- One concept, one canonical term. Do not let synonyms drift across layers.
- Names must reveal business intent or technical role. Prefer `PublishInvoiceJob` over `InvoiceProcessor`.
- Align boundary names across related artifacts: Request, Data/DTO, Service, Repository, Resource, Policy, Job, Listener, and tests should center on the same domain term.
- Avoid vague buckets such as `Helper`, `Util`, `Common`, `Manager`, `Processor`, or `BaseRepository` unless the repository already uses them and the current mode explicitly preserves them.
- Preserve a strong local convention when the repository already has one. Only normalize to the Alaa convention set in `whole-project-normalize-alaa` mode.
- In normalize-to-Alaa mode, standardize naming and layer roles according to `alaa-laravel-architecture` plus `references/consistency-and-naming.md`.

# Pattern decision order
Choose the simplest abstraction that fixes the real problem.

1. Start with a plain class, private method extraction, or tighter naming.
2. Add a DTO when validated or transferred data needs a stable typed shape.
3. Add a value object when a domain concept has invariants or behavior.
4. Add a strategy when algorithms or providers vary behind one contract.
5. Add a factory when construction enforces invariants or hides meaningful branching.
6. Add a repository when persistence logic is non-trivial, repeated, or represents a real boundary.
7. Add an interface only when there is a real seam: multiple implementations, package boundary, external integration, or a test seam that genuinely helps clarity.

Do not stack Repository + Factory + Strategy + Interface merely for aesthetics. Every abstraction must earn its keep.

# Default design decisions
Keep these defaults visible here; detailed pattern guidance lives in `references/design-patterns.md`.

- Prefer constructor injection for growing classes and reusable collaborators.
- Add an interface only for a real seam: multiple implementations, external integration, package boundary, or a test seam that genuinely improves clarity.
- Add a repository only for a meaningful persistence boundary, repeated non-trivial query logic, or aggregate-oriented persistence. Do not create one per model by habit, and avoid generic base repositories.
- Add a factory when construction enforces invariants or hides meaningful branching. Do not wrap obvious `new` calls with no added value.
- Use DTOs for validated or transferred layer-boundary data, and use value objects for domain concepts with invariants or behavior.
- Use a strategy when algorithms or providers genuinely vary. Do not introduce a strategy hierarchy for one stable implementation.

# Non-negotiable defaults
- Use `declare(strict_types=1);` in new PHP files unless the repository clearly avoids it.
- Type parameters, return values, and properties unless a framework contract prevents it.
- Prefer `readonly` DTOs and value objects when their semantics are stable.
- Prefer `DateTimeImmutable` for time values.
- Prefer enums plus `match` for closed sets and explicit branching.
- Prefer composition over inheritance.
- Keep classes focused on one primary reason to change.
- Prefer constructor injection and explicit dependencies over service location.
- Keep side effects at the edges and keep core logic deterministic.
- Avoid hidden IO, hidden queries, hidden mutations, and hidden state.
- Catch exceptions at real boundaries to translate them. Do not bury failures behind `null`, `false`, or silent logs.
- Keep public parameter names stable where named arguments may be used.

# SOLID posture
Apply SOLID pragmatically rather than mechanically.

- Split classes by reason to change, not by line count alone.
- Prefer extension through composition, small strategies, and focused services before scattering branching across many call sites.
- Keep subtype contracts compatible, keep interfaces role-based, and prefer a clear concrete class over a forced abstraction when the dependency is local and stable.

Clarity, fewer moving parts, and repo consistency beat textbook purity.

# Laravel defaults
- Keep controllers thin and deterministic.
- Use Form Requests for meaningful validation and request authorization.
- Use API Resources for stable JSON responses.
- Use policies or gates for authorization.
- Prefer DTOs or typed inputs over passing raw validated arrays across layers when the shape matters.
- Prefer Eloquent directly when the query is simple and local; move to a repository only when a real persistence boundary appears.
- Prevent N+1 by default with deliberate eager loading and resource helpers such as `whenLoaded()`, `whenCounted()`, and `whenAggregated()` when appropriate.
- For large dataset traversal, use `chunk`, `chunkById`, `lazy`, `lazyById`, or `cursor` deliberately based on mutation and memory behavior.
- Keep facades near framework edges. Prefer dependency injection in services and domain-facing code.
- Follow repository folder structure first. If the repository has no strong convention and the task enters architecture territory, defer folder and layer decisions to `alaa-laravel-architecture`.

# Error-handling baseline
- Throw specific exceptions with clear ownership.
- Translate exceptions centrally at HTTP, CLI, queue, and integration boundaries.
- Preserve the previous exception when wrapping low-level failures.
- Keep client-visible error messages safe and stable.
- Put debugging detail into structured logs, not into user-facing strings.
- For security-sensitive behavior, follow `alaa-security-review`.
- For logging fields, trace semantics, and alert implications, follow `alaa-observability-soc`.

# Performance baseline
- Measure before micro-optimizing.
- Avoid repeated encode/decode churn, broad object graphs, and unnecessary temporary arrays in hot code.
- Prefer small immutable objects for stable data.
- Avoid reflection-heavy or magic-heavy abstractions in performance-sensitive paths.
- For data-layer performance, query shape, or indexing, switch to `alaa-data-layer`.
- For long-lived worker and hot-path behavior, switch to `alaa-octane-performance`.

# Documentation baseline
Documentation is part of done when behavior, contracts, setup, env vars, request or response shapes, flows, or examples change.

- Keep docblocks in simple, fluent English.
- Add docblocks where they improve type clarity, explain non-obvious intent, or capture invariants and side effects.
- Remove or update stale docblocks immediately.
- Keep README, docs, Postman collection v2.1, environment artifacts, and request-flow diagrams aligned with the current code.
- Prefer one request item per operation in Postman, with multiple saved responses on that same item.
- Keep request-flow diagrams current; Mermaid is preferred when practical.
- Use `alaa-docs-farsi` for the docs workflow when docs artifacts are in scope, but keep the actual output in English unless the user explicitly asks otherwise.

# References to read selectively
- `references/refactor-modes.md`
  Read whenever the task includes refactoring, new slice design, or more than one touched file.
- `references/companion-skill-routing.md`
  Read at the start of every non-trivial task and before any whole-project refactor.
- `references/consistency-and-naming.md`
  Read before renaming, extracting, consolidating, or normalizing code shape.
- `references/design-patterns.md`
  Read for Repository, Factory, Strategy, DTO, Value Object, Query Object / Filter DTO, and exception-translation guidance.
- `references/php-modern-and-psr.md`
  Read for PHP 8.5 features, type safety, PSR / PER usage, and language-level anti-patterns.
- `references/laravel-best-practices.md`
  Read for Form Requests, Resources, policies, service container usage, eager loading, resource shape, provider hygiene, and test expectations.
- `references/documentation-and-artifacts.md`
  Read when behavior changes require docblocks, README or docs updates, Postman collection changes, environment artifacts, or request-flow diagrams.
- `references/agent-orchestration.md`
  Read only when the user explicitly asks for subagents, delegation, or parallel agent work and the environment allows it.

# Subagents and parallel work
Keep this skill single-agent by default. Detailed orchestration guidance lives in `references/agent-orchestration.md`.

- Start with one local plan and split only when independent tracks materially improve quality or speed.
- Prefer a manager pattern: one main agent keeps plan ownership, repository context, and final synthesis.
- Delegate only bounded subtasks with clear ownership and disjoint write scopes.
- Keep the immediate blocking next step local when possible, and continue non-overlapping local work while delegated work runs.
- Use `multi_tool_use.parallel` for independent developer-tool reads and safe validations, not for overlapping writes or tools that forbid parallel execution.

# Output contract when applying this skill
Keep the final report concise but auditable.

- State the selected task mode.
- State which companion skills governed the work.
- State whether public contracts were preserved, and note any intentional exceptions.
- Mention the important patterns you introduced or intentionally avoided when the choice is non-obvious.
- State test and validation status honestly.
- State documentation alignment status.
- State remaining risk or follow-up work.

# Global anti-patterns
- Service locator or container injection in app code.
- Static helper classes that hide mutable state or IO.
- Fat controllers, fat jobs, fat listeners, or god services.
- Primitive obsession for domain concepts that deserve a value object.
- Raw associative arrays acting as de facto DTOs across layers.
- Generic repositories, helpers, managers, or util classes with vague responsibility.
- Overusing inheritance when composition or a value object is simpler.
- Dynamic properties, magic behavior, or hidden serialization tricks in new code.
- Changing public contracts accidentally during a cleanup.
- Turning a local feature task into an unbounded whole-repo rewrite.
- Claiming a companion skill was respected without actually routing to it when its trigger fired.
