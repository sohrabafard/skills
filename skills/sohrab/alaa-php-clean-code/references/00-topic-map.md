# Topic map — the only router in this skill

Three axes, three tables. Every row is an observable condition, not a subject: match the situation, read what the row names, and read nothing else.

## 1. Task → local file

| You are about to… | Read |
|---|---|
| Add a route, controller, or endpoint | `laravel-best-practices.md`, then `design-patterns.md` (Service, Repository) |
| Write or change a service, or move business flow out of a controller | `design-patterns.md` (Service, DTO, Value object) + `solid-in-practice.md` |
| Read or write persistence from application-layer code | `design-patterns.md` (Repository, Query object) + `laravel-best-practices.md` ("Repository-first persistence") |
| Add caching to domain data | `design-patterns.md` (Decorator). The gate that must pass first is in `alaa-data-layer references/50-redis-laravel-octane.md`, "Step 0" |
| Integrate a vendor or provider SDK (SMS, payment, storage, external API) | `design-patterns.md` (Adapter, Strategy, Abstract factory, Exception translation) |
| Queue, delay, retry, or audit an action as its own unit | `design-patterns.md` (Command) + `octane-clean-code.md` |
| Model a status or lifecycle with guarded transitions | `design-patterns.md` (State) |
| Choose a pattern, or review a pattern someone else chose | `design-patterns.md` — run the symptom → pattern diagnostic at its top before anything else |
| Reach for Flyweight, Memento, Visitor, Bridge, Prototype, Iterator, Composite, or Mediator | `design-patterns-rare.md`. The diagnostic table in `design-patterns.md` routes here |
| Decide whether code is worth refactoring, or name what is wrong with it | `code-smells-and-refactoring-triggers.md` |
| Refactor, design a new slice, or touch more than one file | `refactor-modes.md` |
| Rename a class, method, namespace, file, folder, or concept | `consistency-and-naming.md` |
| Answer a SOLID question, or justify an abstraction | `solid-in-practice.md` |
| Bind a service, add a static property, write an observer, or reuse an SDK client | `octane-clean-code.md`, then `/alaa-octane-performance` (`$alaa-octane-performance`) for the invariant itself |
| Use a PHP 8.4+ or 8.5 language feature, a PSR interface, or a type you are unsure of | `php-modern-and-psr.md` |
| Write or repair a Pest test, or choose a database-refresh trait | `laravel-best-practices.md` ("Tests"), then `/alaa-testing-strategy` (`$alaa-testing-strategy`) for what the test must prove |
| Change behaviour that a docblock, README, Postman item, env var, or diagram describes | `documentation-and-artifacts.md` |
| Say "latest", "current", "deprecated", "secure", or name a tool version | `source-map.md` |

The two most expensive mistakes this skill prevents are persistence composed outside a repository and a `Cache::` call outside a decorator. When the task touches persistence or caching in any way, the Repository and Decorator sections are not optional reading.

## 2. Claim → authority, and what wins on conflict

You are about to state something. If it appears here, this skill is not the authority: read the owner, use its wording, and report drift rather than restating it.

| The claim you are about to make | Authority, which wins |
|---|---|
| A timeout, retry count, backoff figure, pool bound, acquire wait, or shed threshold | `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. This skill states no number |
| Whether a call may retry at all, how it degrades, or what a breaker does | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| An error code, event name, queue name, metric name, log field, header name, or envelope shape | `/alaa-services-contract` (`$alaa-services-contract`) |
| That a signal, log, or metric is required | `/alaa-observability-soc` (`$alaa-observability-soc`) wins on whether it is required; `/alaa-services-contract` wins on what it is called |
| Which values a worker may never retain, and how state is reset between requests | `/alaa-octane-performance` (`$alaa-octane-performance`). Its wording is the invariant; `octane-clean-code.md` only shapes patterns around it |
| A cache key layout, TTL, invalidation rule, index, or query plan | `/alaa-data-layer` (`$alaa-data-layer`) |
| That a repository layer is complete enough to add caching | `alaa-data-layer references/50-redis-laravel-octane.md`, "Step 0 — repository-pattern gate" |
| Where a tenant, project, or user identity comes from | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| That a test is sufficient, that a double is honest, or that a claim is proven | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| A complexity bound, or which N+1 resolution a growing path needs | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| That a change needs no design pass | `/alaa-system-design` (`$alaa-system-design`) owns the trigger list |
| A quality criterion or review bar | `alaa-project-constitution references/quality-bar.md` |
| A model name or reasoning-effort setting | `/alaa-prompting-guide` (`$alaa-prompting-guide`). Name no model |

### The three upstream skills

A production Laravel repository ships three agent skills at `.agents/skills/` that **this repository does not own and cannot control** — `laravel-best-practices/`, `octane-development/`, and `pest-testing/`. They can be re-pulled, reworded, or removed between runs. Route to them for mechanics and worked examples; never let one of them be the only place a safety-critical invariant is stated, and where a rule protects cross-request state, tenant isolation, or an authorization decision, this skill states it outright even when upstream also does.

Four upstream rules are actively wrong for these services and are overridden by name, each with the owner that wins, in `laravel-best-practices.md` under "Overrides of the upstream skill" and in that file's "Tests" section. Read those before following an upstream rule on tenant context, `once()` memoization, comments, or test deletion.

## 3. Task → sibling skill

Routing is mandatory, not advice. If a row fires, do not continue the affected part of the task until that skill has been read. The full ownership map, including the concerns this skill contributes inside each boundary, is in `SKILL.md`.

| Your change touches… | Read first |
|---|---|
| More than one file, or behaviour, or the whole project | `/alaa-workflow` (`$alaa-workflow`) — create or update its plan artifact |
| A layer boundary, an API contract, a DTO boundary, `public_id`, route binding, or outbox flow | `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) |
| An interface another component calls, which component writes a piece of data, a consistency / ordering / idempotency / concurrency / caching property, a dependency edge, a new deployable unit, or what a caller sees when a dependency is slow or gone | `/alaa-system-design` (`$alaa-system-design`) |
| A trusted header, request identity, tenant or project derivation, step-up auth, or downstream auth propagation | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| An object-level relationship authorization decision | `/openfga` (`$openfga`) |
| A migration, query, index, transaction, lock, Redis key, or tenant scoping in persistence | `/alaa-data-layer` (`$alaa-data-layer`) |
| Octane, Swoole, RoadRunner, a hot path, a singleton, request-scoped state, or worker lifecycle | `/alaa-octane-performance` (`$alaa-octane-performance`) |
| A job, event, consumer, retry, DLQ, idempotency key, or outbox consumer | `/alaa-async-messaging` (`$alaa-async-messaging`); add `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq`) when RabbitMQ or AMQP topology is involved |
| Auth, authorization, validation of untrusted input, file handling, URL fetching, secrets, tenancy, or privilege | `/alaa-security-review` (`$alaa-security-review`) |
| A log, trace, metric, alert, correlation ID, or Sentry behaviour | `/alaa-observability-soc` (`$alaa-observability-soc`) for the requirement, `/alaa-services-contract` (`$alaa-services-contract`) for the name |
| A test, or any claim that a check passed | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| CI, Pint or PHPStan configuration, a test command, or a quality gate | `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) |
| README, docs, Postman collection, env docs, or a diagram | `/alaa-repo-docs` (`$alaa-repo-docs`) — output in English unless the user asks otherwise |
| A composer dependency bump, or a Laravel 12 → 13 upgrade | `/alaa-laravel-upgrade-all-packages` (`$alaa-laravel-upgrade-all-packages`) |
| A Crockford Base32, integer, string, or UUIDv7 codec that must match JS, shell, or HAProxy Lua | `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) |
| A destructive, irreversible, or production-affecting operation | `/alaa-controlled-ops` (`$alaa-controlled-ops`) |
| Delegation to subagents, lane planning, or a review gate | `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) |
| A Codex-only tool or runtime affordance, including parallel tool invocation | `/alaa-codex-runtime-ops` (`$alaa-codex-runtime-ops`) |
| MongoDB, and the repository already uses it or the user asked for it | `/alaa-mongodb-patterns` (`$alaa-mongodb-patterns`) |
| An OpenAI API, model, prompt, tool, or product claim in docs or examples | `/openai-docs` (`$openai-docs`) |

### Combined scenarios that recur

- **Gateway-backed HTTP endpoint with database work**: `/alaa-workflow`, `/alaa-laravel-architecture`, `/alaa-trust-gateway-auth`, `/alaa-data-layer`, `/alaa-security-review`, `/alaa-testing-strategy`, and `/alaa-repo-docs` when the contract or its examples changed.
- **RabbitMQ consumer or outbox listener**: `/alaa-workflow`, `/alaa-laravel-architecture`, `/alaa-async-messaging`, `/alaa-laravel-job-rabbitmq`, `/alaa-observability-soc`, `/alaa-testing-strategy`, plus `/alaa-security-review` when auth or tenant boundaries are involved.
- **Whole-project cleanup**: `/alaa-workflow` and `/alaa-laravel-architecture` first, this skill throughout, then any skill whose row fires during the audit.

Where multiple rows fire, read them in the order that protects contracts first. Name every skill that governed the work in the final report — that naming is the audit trail proving routing happened.
