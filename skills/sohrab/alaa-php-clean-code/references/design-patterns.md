# PHP / Laravel design patterns

## Contents
- Decision posture
- MVC pattern
- Service pattern
- Interfaces and dependency injection
- Repository pattern
- Decorator pattern
- Factory pattern
- DTO pattern
- Value object pattern
- Builder pattern
- Strategy pattern
- Observer pattern
- Adapter pattern
- Facade pattern
- Proxy pattern
- Composite pattern
- Iterator pattern
- State pattern
- Template method pattern
- Chain of responsibility / Pipeline
- Singleton pattern
- Pipeline pattern
- Command pattern
- Query object / filter DTO pattern
- Exception translation pattern
- Pattern-selection rule of thumb

## Decision posture
Use design patterns to reduce complexity, not to look advanced. A senior Laravel developer asks: "Where is this code becoming hard to understand, test, change, or keep safe under Octane?"

Prefer the smallest useful abstraction:
1. better name or private method
2. focused service
3. typed DTO or value object
4. strategy/factory/adapter where variation or external boundaries are real
5. repository/query object for persistence access and query composition
6. pipeline or command/job where workflow shape requires it

Do not stack patterns by habit. Every pattern must remove a real smell: fat controller, duplicated query, provider-specific API leakage, unstable array shape, scattered branching, hidden side effects, or unsafe long-lived worker state. Repository is the exception in Alaa Laravel application code: it is mandatory for persistence access, but it still must be named and shaped around a real aggregate, use case, read model, or persistence boundary.

## MVC pattern

### Purpose
Separate request handling, data/domain behavior, and response rendering. In Laravel, controllers receive HTTP requests, models represent persistence/domain-facing data, and views/resources serialize responses.

### Result
Code is easier to navigate and test because each layer has a clear job. Controllers should coordinate; they should not become validation, authorization, query, transaction, provider-selection, and serialization buckets.

### Laravel application
- Use controllers for orchestration.
- Use Form Requests for validation/authorization when meaningful.
- Use models for Eloquent persistence behavior.
- Use API Resources or views for response shape.
- Move business operations into services before controllers become fat.

### Anti-patterns
- Querying, authorizing, mutating, sending external requests, and formatting responses in one controller method.
- Putting response-specific formatting into models.
- Letting Blade/API resources trigger hidden queries.

## Service pattern

### Purpose
Move business operations out of controllers, jobs, listeners, commands, and models into focused service classes.

### Result
Business logic becomes reusable and testable without requiring HTTP requests. Controllers stay thin, and jobs/listeners can share the same operation without copy-pasting rules.

### Laravel application
- Use services for payments, registration, auth flows, wallet operations, file processing, notification decisions, imports, and domain-heavy actions.
- Accept typed DTOs, models, value objects, or scalar IDs as inputs.
- Keep services stateless under Octane; pass user/tenant/request context as method arguments.

### Anti-patterns
- A god service that owns unrelated workflows.
- Storing current user, request, tenant, headers, or trace state on the service.
- Moving controller code into a service without improving names, boundaries, or tests.

## Interfaces and dependency injection

### Use when
- A collaborator has multiple implementations.
- The dependency crosses a package or external-service boundary.
- A test seam improves clarity.
- Constructor injection makes the dependency graph explicit.

### Laravel application
- Type-hint dependencies in controllers, listeners, middleware, jobs, commands, and services.
- Bind interfaces in service providers only when the abstraction is real.
- Use contextual binding or contextual attributes for per-consumer differences.

### Good defaults
- Prefer constructor injection for stable collaborators.
- Prefer method injection only for short-lived framework edge concerns.
- Prefer a concrete class when zero-configuration resolution already works and the dependency is local and stable.

### Anti-patterns
- Injecting `ContainerInterface` or Laravel's container to resolve dependencies manually.
- Creating an interface for every class by habit.
- Binding obvious concrete classes unnecessarily.
- Mixing dependency resolution with business logic.

## Repository pattern

### Use when
- Any application-layer code needs to read or write persistence.
- A controller, service, job, listener, command, policy, action, pipeline, or adapter needs Eloquent/query-builder data.
- Query composition needs a stable home.
- The code works against a meaningful persistence boundary, read model, aggregate, or use case.

### Laravel application
- Keep repositories in the persistence layer defined by the repo architecture, or follow the nearest existing repository convention.
- Let services orchestrate business rules and call repositories for persistence and query composition.
- Accept typed filter DTOs instead of raw request arrays.
- Put all touched Eloquent/query-builder read/write composition behind a repository unless the code is an allowed exception.
- Allowed exceptions: model relationships/scopes/casts/accessors, migrations, factories, seeders, test fixtures/assertions, resources reading already-loaded models, and framework glue where Laravel requires the model API.

### Good defaults
- Model the repository around an aggregate, use case, read model, or persistence boundary, not around generic CRUD.
- Keep business rules, authorization, and serialization out of the repository.
- Return domain objects, DTOs, collections, or paginators that match repo conventions.
- Keep simple operations simple, but still behind the repository boundary.

### Anti-patterns
- Direct Eloquent or query-builder reads/writes in controllers, services, jobs, listeners, commands, policies, actions, pipelines, or adapters.
- One vague repository per Eloquent model with only uncurated `create`, `update`, `delete`, `find` pass-throughs.
- A generic `BaseRepository` that becomes a dumping ground.
- Hiding all Eloquent behavior behind thin wrappers with no value.
- Putting authorization or domain rules in the repository.

## Decorator pattern

### Use when
- A cross-cutting concern (caching, logging, metrics, retries, tracing) must wrap an existing interface without changing its implementations.
- Caching a repository: this is the canonical Alaa home for Redis caching — a `Cached<Domain>Repository` implementing the same repository interface and wrapping the store implementation (e.g. `PostgresCommentRepository`).
- Behavior must be stackable or removable per environment (e.g. no cache decorator in tests).

### Laravel application
- Implement the same interface as the wrapped class; take it as the first constructor argument.
- Compose in the service provider binding (closure that builds inner + decorator); callers keep depending on the interface and never know the decorator exists.
- Cache decorators delegate reads through `Cache::remember`/`flexible` and invalidate on writes right after delegating; on cache-store failure they call the inner implementation directly so a Redis outage never becomes a request failure.
- Key design, TTL, invalidation, and fallback policy come from `alaa-data-layer` (`references/50-redis-laravel-octane.md`); the decorator seam itself is defined in `alaa-laravel-architecture`.

### Good defaults
- One concern per decorator; stack two small decorators rather than writing one mixed one.
- The decorator holds no business rules, no query composition, and no mutable request state (Octane-safe: stateless, context passed per call).
- Keep the decorator's method list identical to the interface — if it needs extra public methods, the abstraction is wrong.

### Anti-patterns
- Caching inside the concrete repository (forces every caller through the cache and makes fallback and testing impossible).
- `Cache::` calls in controllers or services for domain data instead of a decorator.
- A decorator that swallows inner-layer exceptions other than cache-infrastructure failures.
- Decorators that add behavior the interface consumer must know about (leaky abstraction).

## Factory pattern

### Use when
- Construction enforces invariants.
- Creation chooses between strategies or implementations.
- Object graphs are complex enough that direct construction becomes noisy.
- A domain object should not expose its internal assembly steps broadly.

### Laravel application
- Use factories to build complex DTOs, value objects, strategies, integration clients, or domain aggregates.
- Keep service-provider bindings separate from domain factories.
- Reserve Eloquent model factories for testing and seeding unless the repository explicitly uses them as fixtures only.

### Good defaults
- Prefer direct construction with named arguments when the object is already simple.
- Keep factories narrow and intention-revealing.
- Use the factory to centralize branching or invariant enforcement, not to hide obvious code.

### Anti-patterns
- Wrapping `new` with no added value.
- Using a factory to hide poor object design.
- Reusing test factories as production construction logic.
- Building a huge "factory manager" that knows too much about the app.

## DTO pattern

### Use when
- Data crosses a layer boundary.
- Validated request input needs a stable typed shape.
- Query filters or command payloads should be explicit.
- You want to avoid associative-array drift.

### Laravel application
- Build DTOs from Form Request validated data.
- Use filter DTOs for repository queries and list endpoints.
- Keep DTOs small, typed, and preferably `readonly`.

### Good defaults
- Treat DTOs as transport-shaped objects, not as active domain objects.
- Use nullable fields only when the contract genuinely allows absence.
- Prefer multiple focused DTOs over one giant "everything" payload.

### Anti-patterns
- Passing arrays across controllers, services, and repositories.
- Letting DTOs accumulate domain logic and persistence concerns.
- Reusing Eloquent models as DTOs.
- Hiding unvalidated input inside a DTO constructor.

## Value object pattern

### Use when
- A domain concept has invariants or behavior.
- A primitive value carries business meaning.
- Equality should be value-based, not identity-based.
- Immutability improves correctness.

### Laravel application
- Use value objects for concepts such as `Money`, `Email`, `TenantId`, `PhoneNumber`, `DateRange`, or domain-specific IDs.
- Pair them with custom casts only when the cast does not hide heavy IO or surprising behavior.
- Use backed enums when the concept is a closed set with a stable scalar representation.

### Good defaults
- Prefer `readonly` properties or `readonly` classes when supported by the repo's PHP version.
- Validate invariants inside the constructor or named constructors.
- Keep formatting or parsing behavior close to the value object when it is intrinsic to the concept.

### Anti-patterns
- Primitive obsession for key business concepts.
- Mutable value objects.
- Heavy framework coupling inside domain value objects.
- Overusing custom casts that hide queries or extra writes.

## Builder pattern

### Use when
- Construction is multi-step, conditional, or order-sensitive and a single constructor call (even with named arguments) becomes unreadable.
- A complex immutable object (report definition, export config, notification payload, search criteria) is assembled from many optional parts.
- The assembly steps deserve validation before the final object exists.

### Laravel application
- Laravel itself is builder-heavy: the query builder, `Mail`/`Notification` fluent APIs, `Http::withHeaders()->timeout()->retry()`, and pending-object APIs are builders. Use them idiomatically instead of wrapping them.
- Write a domain builder only when constructing the object inline is genuinely noisy: a fluent `withX()`/`build()` class whose `build()` validates invariants and returns a `readonly` DTO or value object.
- On PHP 8.5, prefer named arguments plus `clone($obj, [...])` withers first; reach for a builder only when steps are conditional or shared across call sites.

### Good defaults
- `build()` is the single place invariants are enforced; a builder that can emit an invalid object is worse than no builder.
- Keep builders stateless between uses or cheap to construct; under Octane never reuse a mutable builder instance across requests.
- Return immutable results (`readonly` DTO/value object).

### Anti-patterns
- A builder wrapping a three-argument constructor.
- Fluent setters on the domain object itself, leaving it mutable and half-initialized between calls.
- Builders that hide required fields as optional setters, deferring failures to runtime deep in the flow.

## Strategy pattern

### Use when
- Multiple algorithms or providers share one responsibility.
- Selection rules are stable and explicit.
- The same branching logic would otherwise spread across many services.

### Laravel application
- Define a small interface and separate implementations.
- Resolve the strategy via a dedicated factory, map, or service-provider binding.
- Keep caller code focused on invoking behavior, not on re-implementing selection logic.

### Good defaults
- Keep the interface role-based and narrow.
- Make selection rules explicit and testable.
- Prefer composition over inheritance between strategies.

### Anti-patterns
- One large strategy interface that every implementation barely satisfies.
- A strategy pattern for a single permanent implementation.
- Hiding unrelated policies inside a single resolver.
- Replacing a simple `match` with an abstraction that adds no flexibility.

## Observer pattern

### Use when
- A model lifecycle event should trigger organized side effects.
- Audit logs, cache invalidation, slug generation, cleanup, or related record maintenance belongs outside the controller.
- The side effect is tightly related to the model event and not a full business workflow.

### Laravel application
- Use Laravel model observers for `created`, `updated`, `deleted`, `restored`, and similar events.
- Keep observers small and deterministic.
- Queue slow external side effects when appropriate.
- Under Octane, keep observers stateless and avoid retained request context.

### Good defaults
- Prefer observers for local model-event side effects.
- Prefer domain services/events/listeners for broader workflows that cross aggregates or integrations.
- Make side effects idempotent when retries or repeated events are possible.

### Anti-patterns
- Hiding major business workflows in model events.
- Performing slow external IO synchronously in a model observer.
- Depending on request/auth/tenant globals inside observers instead of explicit context.

## Adapter pattern

### Use when
- External provider APIs need a stable internal interface.
- A payment, SMS, email, storage, analytics, CRM, map, or auth provider has provider-specific payloads.
- You need to protect application code from third-party naming, errors, and response formats.

### Laravel application
- Define a small internal contract such as `SmsSender`, `PaymentGateway`, or `AnalyticsClient`.
- Put provider-specific mapping in adapter classes.
- Translate provider exceptions into app-owned integration exceptions.
- Pass request-specific headers/options per call; do not mutate a shared client under Octane.

### Good defaults
- Keep adapters at integration boundaries.
- Return app-owned DTOs or result objects instead of raw provider responses when the shape matters.
- Make provider selection explicit through config, a factory, or contextual binding.

### Anti-patterns
- Letting provider payload keys spread into controllers and services.
- Logging provider secrets or raw tokens.
- Caching mutable provider clients with per-request headers.

## Facade pattern

### Two meanings — keep them distinct
- **GoF facade**: one focused class that gives application code a simple, intention-named API over a complex subsystem (a multi-step provider flow, a legacy module, a cluster of SDK calls). In Alaa Laravel code this is a plain injected service such as `PaymentFacade` or `MediaPipelineFacade`: small methods named by business use case, returning app-owned DTOs, hiding subsystem ordering and quirks. Use it when callers keep re-orchestrating the same subsystem steps.
- **Laravel `Facade` classes** (`Cache::`, `Queue::`, `Log::`): static proxies to container services — an access mechanism, not the GoF pattern. The rules below govern them.

### Use when
- Laravel's facade API keeps framework-edge orchestration readable.
- The operation is clearly infrastructure-facing, such as cache, log, queue, mail, storage, DB transaction boundaries, or events.

### Laravel application
- Facades are acceptable in controllers, console commands, service providers, tests, and small orchestration code.
- Prefer constructor injection in reusable services and domain-facing code.
- Use facade fakes in tests where the repo convention supports them.

### Good defaults
- Keep facade calls near Laravel edges.
- Avoid facade-heavy services when dependencies should be explicit.
- Avoid mutating global facade-backed state during a request under Octane.

### Anti-patterns
- Using facades as hidden dependencies in growing domain services.
- Runtime mutation of config, locale, auth, HTTP defaults, or global state.
- Treating facade convenience as permission to skip boundaries.

## Proxy pattern

### Use when
- Access to an object must be controlled or deferred without changing its interface: lazy initialization of expensive services, guarded access, or remote-call stand-ins.
- A heavy dependency (report engine, warmed SDK client, large object graph) is injected widely but used rarely.

### Laravel application
- PHP 8.4+ has native lazy objects: `ReflectionClass::newLazyGhost()` (the object initializes itself on first real use) and `ReflectionClass::newLazyProxy()` (a stand-in forwards to a real instance built by a factory). Prefer a ghost when you control construction and initialization; prefer a proxy when another layer must construct the real instance — and then watch object identity, because proxy and real instance are different objects.
- Laravel's container and Octane already defer most service construction; add explicit lazy objects only when a measured startup or memory cost justifies them.
- Eloquent relations are effectively lazy proxies for data access; the discipline for them (eager loading, `preventLazyLoading()`) lives in `laravel-best-practices.md`.
- Distinguish from Decorator: a decorator adds behavior to a real instance; a proxy controls when/whether the real instance exists or is reached.

### Anti-patterns
- Hand-rolled magic `__get`/`__call` proxy classes on PHP 8.4+ repos where native lazy objects do the job without magic.
- Lazy proxies around cheap objects — deferral machinery costing more than construction.
- Identity-sensitive code (`spl_object_id`, strict `===` registry checks) mixed with `newLazyProxy` without an explicit note.

## Composite pattern

### Use when
- Data or rules are recursive trees and callers should treat a leaf and a group uniformly: category trees, menu/navigation structures, nested comments, organizational units, composable validation or eligibility rules.

### Laravel application
- Model the node contract as one small interface (e.g. `EligibilityRule::passes(Context $ctx): bool`); leaves implement it directly, and composites (`AllOf`, `AnyOf`) hold `RuleInterface[]` children and implement the same interface. Specification-style rule composition is the highest-value use.
- For persistent trees, pair the in-memory composite with a deliberate storage strategy (adjacency list, path/materialized path, or a package the repo already uses) — recursion in PHP must not become recursion in queries; load the tree in bounded queries, then compose.
- Blade/component nesting already gives UI composition; do not force a class-based composite for rendering.

### Good defaults
- Guard depth and cycles explicitly when input is user-shaped.
- Keep leaf and composite behavior contract-identical (LSP): callers never type-check for "is this a group".

### Anti-patterns
- A composite interface with `addChild`/`removeChild` on leaves that throw `NotSupported` — split the mutable-tree API from the evaluation API.
- Unbounded recursive queries (N+1 per tree level) hidden behind an elegant in-memory composite.

## Iterator pattern

### Use when
- A traversal should be consumed lazily without materializing the whole dataset, or a custom aggregate should be `foreach`-able without exposing internals.

### Laravel application
- PHP generators (`yield`) are the idiomatic iterator: streaming file lines, paginated API pages, transformed rows. Laravel's `LazyCollection` (and `lazy()`/`cursor()` on queries) is the framework-native generator wrapper — prefer it over hand-written `Iterator` implementations.
- Choose the traversal tool by mutation and memory behavior via the large-dataset table in `laravel-best-practices.md` (`chunk`, `chunkById`, `lazy`, `lazyById`, `cursor`).
- Implement `IteratorAggregate` (returning a generator) on domain collections when a typed collection object earns its keep; implement the low-level `Iterator` interface only for genuinely custom traversal state.

### Anti-patterns
- Materializing huge arrays and then "optimizing" downstream, when a generator/LazyCollection keeps memory flat.
- Generators with hidden side effects per step — iteration must be re-runnable or explicitly single-pass.
- A custom collection class that re-implements twenty Collection methods for one use site.

## State pattern

### Use when
- A domain lifecycle has real states with guarded transitions: order/enrollment/invoice status, moderation flow, subscription lifecycle, document workflow.
- Status `if`/`switch` branches are spreading across services and controllers.

### Laravel application
- Default shape: a backed enum for the state plus one transition authority. Keep a `canTransitionTo(self $to): bool` (or a `match`-based transition table) on the enum, and route every status write through one service/aggregate method that enforces it — never scatter `$model->status = ...` assignments.
- Behavior that varies heavily per state can move to per-state classes behind one interface (classic State pattern) — usually only when states have many verbs each; for most CRUD-plus-workflow services the enum + transition table is enough.
- If the repo already uses a state-machine package (e.g. model-states), follow it; do not introduce one for a three-state lifecycle.
- Persist states as stable string-backed enum values; treat renames as contract changes.

### Anti-patterns
- Boolean soup (`is_active`, `is_archived`, `is_pending`) representing one exclusive lifecycle.
- Transition rules duplicated in controllers, jobs, and admin panels instead of one authority.
- Status changed silently as a side effect of unrelated updates (mass assignment reaching `status`).

## Template method pattern

### Use when
- Several implementations share one fixed algorithm skeleton with small varying steps, and the skeleton itself must stay in one place.

### Laravel application
- Use sparingly: an abstract class with a `final` public method calling small `protected` hooks (e.g. an import base: `run()` = validate → transform → persist → report, subclasses supply `transform()`).
- Prefer composition first — a service taking strategy/closure steps, or a pipeline — because inheritance couples subclasses to the base class forever. Template method wins only when the skeleton must be un-overridable and implementations are a closed, code-owned set.
- Keep hooks few and intention-named; a base class with ten abstract methods is an interface pretending to be an algorithm.

### Anti-patterns
- Deep inheritance chains where each level overrides part of the parent's flow.
- A template base class accumulating shared helpers until it becomes a god base.
- Using template method where the varying part is data, not behavior (a config array would do).

## Chain of responsibility / Pipeline

Laravel's middleware stack and `Pipeline` are chain-of-responsibility implementations: each handler receives the payload and the `$next` closure, and decides to handle, transform, pass on, or short-circuit. The pipeline guidance below is the canonical Alaa form of this pattern; reach for a hand-rolled linked chain only when handlers must be discovered/ordered dynamically at runtime, which is rare. Short-circuiting (returning early without calling `$next`) is a first-class outcome — make it explicit and tested, not an exception in disguise.

## Singleton pattern

### Use when
- One shared instance is expensive to create and safe to reuse.
- The service is immutable, tenant-agnostic, and stateless.
- A framework or SDK client benefits from reuse and accepts per-call context safely.

### Laravel application
- Use container `singleton()` only when lifetime safety is proven.
- Prefer transient/scoped bindings for mutable or request-aware services.
- Under Octane, assume singleton instances live across many users and tenants.

### Good defaults
- Singleton services must not hold current user, tenant, request, locale, trace, auth, or headers.
- Pass request-specific data into methods.
- Keep singleton caches bounded and tenant-aware.

### Anti-patterns
- Singleton "current context" services.
- Static caches that grow forever or omit tenant/project keys.
- SDK clients mutated with per-request headers or tokens.

## Pipeline pattern

### Use when
- A workflow is a sequence of independent, reorderable steps.
- Import validation, checkout, content moderation, request enrichment, search filtering, or permission checks have many small phases.
- Each phase can be tested in isolation.

### Laravel application
- Use Laravel's `Pipeline` or a repo-local equivalent when it clarifies flow.
- Keep each pipe focused on one step.
- Pass a typed payload/DTO when the workflow state matters.
- Under Octane, do not let pipe instances retain payloads between requests.

### Good defaults
- Prefer a pipeline when step order is explicit and likely to evolve.
- Prefer a plain service method when the flow is short and stable.
- Keep side effects explicit and boundary-aware.

### Anti-patterns
- A pipeline for two obvious method calls.
- Pipes that depend on hidden globals or mutate unrelated state.
- A payload array whose shape changes silently between steps.

## Command pattern

### Use when
- An action should be executed, queued, retried, delayed, logged, or replayed as its own unit.
- Work should leave the HTTP request path.
- A CLI command or job is the natural boundary for an operation.

### Laravel application
- Laravel jobs and Artisan commands are common command-pattern implementations.
- Use jobs for slow IO, notifications, imports, exports, video processing, webhooks, and synchronization.
- Dispatch after commit when queued work depends on committed rows.
- Keep payloads explicit and idempotent.

### Good defaults
- Prefer IDs and typed payloads over serialized broad object graphs.
- Add retry/backoff/timeout policy where the repo expects it.
- Make handlers idempotent and tenant-aware.

### Anti-patterns
- Doing slow external work in HTTP controllers when async offload is available.
- Non-idempotent jobs with retries.
- Serializing models or service objects when scalar IDs and DTOs are enough.

## Query object / filter DTO pattern

### Use when
- Query logic becomes too complex for one repository method signature.
- Optional filters, sorts, and scopes multiply.
- Search or listing logic deserves its own testable unit.

### Laravel application
- Keep validated filter input in a typed DTO.
- Introduce a query object when repository methods become hard to read, then call it from the repository boundary.
- Keep pagination, sorting, and filtering explicit.

### Good defaults
- Let the controller build or receive validated filter data.
- Keep the repository or query object responsible for query composition only.
- Align query naming with the endpoint or use case.

### Anti-patterns
- Passing raw `Request` objects or unvalidated arrays into query code.
- One 20-parameter repository method.
- Mixing business decisions with SQL composition.
- Using a query object as a hidden service locator for unrelated state.

## Exception translation pattern

### Use when
- A low-level exception should become a domain-level failure or a safe HTTP response.
- External integrations need stable, app-specific error handling.
- Queue, CLI, or HTTP boundaries need consistent failure behavior.

### Laravel application
- Throw specific domain or integration exceptions from services and adapters.
- Translate them centrally in exception handlers, responders, or boundary-specific mappers.
- Keep logs structured and safe.

### Good defaults
- Catch low-level exceptions close to the boundary that understands them.
- Preserve the previous exception when wrapping.
- Map to stable internal codes where the repo already uses them.

### Anti-patterns
- Catching every exception and returning `false`.
- Logging and swallowing failures.
- Throwing generic `Exception` everywhere.
- Leaking sensitive low-level error details to clients.

## Pattern-selection rule of thumb
- Prefer no pattern over the wrong pattern.
- Add a pattern only when it reduces duplication, clarifies a boundary, or makes the code safer to evolve.
- If a concrete class, direct constructor call, or local `match` is already clear, keep it simple.
