# PHP / Laravel design patterns

## Contents
- Decision posture
- MVC pattern
- Service pattern
- Interfaces and dependency injection
- Repository pattern
- Factory pattern
- Strategy pattern
- Observer pattern
- Adapter pattern
- Facade pattern
- Singleton pattern
- Pipeline pattern
- Command pattern
- DTO pattern
- Value object pattern
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
