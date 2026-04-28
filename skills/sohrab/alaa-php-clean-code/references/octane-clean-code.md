# Octane-safe clean code

## Contents
- Core rule
- Long-lived worker state
- Dependency injection and container lifetime
- Pattern-specific Octane cautions
- Swoole to RoadRunner portability
- Review checklist
- Validation expectations

## Core rule
Assume every Alaa Laravel service runs under Octane unless repo evidence proves otherwise.

Under Octane, request workers are long-lived. Code that is clean under PHP-FPM can be unsafe if it stores request-specific state in a static property, singleton, global cache, reused SDK client, mutable facade state, or closure captured by a long-lived object.

Clean code for this fleet must be:
- explicit about inputs
- stateless by default
- tenant-aware
- reset-aware
- portable across Swoole and RoadRunner unless runtime-specific code is intentionally in scope

## Long-lived worker state

### Never retain request-specific data
Do not retain these values in static properties, globals, singletons, service-provider properties, or long-lived closures:
- `Request`
- authenticated user or profile
- tenant/project/school/branch context
- authorization result
- locale
- request headers
- correlation/request/trace IDs
- per-request validation result
- per-request external client headers or tokens

Pass this data explicitly as method arguments or through a request-scoped DTO/service that the app resets between requests.

### Safe state
These are usually safe to keep in singletons:
- immutable configuration read at boot
- tenant-agnostic stateless services
- SDK clients with fixed configuration and per-call headers/options
- compiled maps of strategy classes, enum mappings, or known capability metadata

Even safe singleton state must not grow with request count.

## Dependency injection and container lifetime

### Good defaults
- Constructor-inject stable collaborators.
- Method-pass request-specific context.
- Use interfaces only for real seams.
- Bind mutable request-scoped services with the repo's scoped/transient convention.
- Keep singleton bindings immutable and tenant-agnostic.

### Avoid
- Injecting `Request` into singleton-like services.
- Storing `auth()->user()`, tenant context, locale, or headers in a service constructor.
- Reusing an HTTP client while mutating default headers per request.
- Using the service container inside business logic to hide lifecycle mistakes.

## Pattern-specific Octane cautions

### MVC
Controllers may read request context, but they must not retain it. Keep controllers thin and pass validated inputs into services or DTOs.

### Service pattern
Services should be stateless orchestrators. If a service needs user or tenant context, pass it to the method instead of storing it on the service.

### Repository pattern
Repositories must not remember the "current tenant" internally. Accept tenant/project identifiers or typed filter DTOs explicitly, or use a repo-approved global-scope/RLS approach that is reset-safe.

### Factory pattern
Factories may keep immutable maps of supported strategies or adapters. Do not cache provider instances when those instances carry request headers, tokens, tenant values, or mutable options.

### Strategy pattern
Strategies should be stateless. If a strategy needs request data, pass it to `execute`, `calculate`, `handle`, or another explicit method.

### Observer pattern
Observers run inside the same long-lived app. Keep them stateless, avoid hidden IO in model events unless intentional, and queue slow side effects when the repo policy supports it.

### Adapter pattern
Adapters should translate external APIs into internal contracts. Do not mutate a shared adapter/client with per-request headers; pass headers/options per call or create a short-lived request-specific client wrapper.

### Facade pattern
Facades are acceptable near Laravel edges. Avoid using facades to mutate global runtime state during a request. Prefer dependency injection in domain-facing services.

### Singleton pattern
Singleton is high-risk under Octane. Use it only for immutable, tenant-agnostic, stateless, or expensive SDK-style objects that accept request-specific data per method call. Never store current user, tenant, request, locale, trace, or authorization state in a singleton.

### Pipeline pattern
Pipeline steps must not retain the payload between requests. Steps should transform or validate the passed payload and then release it.

### Command/job pattern
Jobs and commands are safer places for slow work, but they still need idempotency, bounded retries, and explicit tenant context. Do not serialize broad object graphs when IDs and typed payloads are enough.

## Swoole to RoadRunner portability
The fleet is expected to migrate from Swoole to RoadRunner. Keep application code portable:
- prefer Laravel Octane, Laravel container, PSR, Symfony, and framework abstractions
- isolate Swoole-only APIs behind runtime-owned adapters when unavoidable
- do not rely on Swoole task workers from business services unless the runtime design explicitly owns that choice
- avoid coroutine-specific assumptions in ordinary services, repositories, policies, resources, and jobs
- validate Octane reset behavior through framework-level hooks instead of server-specific globals where possible

## Review checklist
Before finalizing PHP/Laravel code, ask:
- Does any static property, singleton, facade mutation, or closure retain request-specific data?
- Does every tenant/project-specific query, cache key, memoization key, and policy decision include trusted tenant/project context?
- Are current user, request, locale, headers, trace IDs, and auth state passed explicitly instead of stored?
- Are services, factories, strategies, adapters, observers, listeners, jobs, and pipeline steps stateless or reset-safe?
- Is any Swoole-specific code isolated from domain/application code?
- Would the same code behave correctly after 10,000 requests handled by the same worker?

## Validation expectations
- For leak-prone changes, add tests that simulate two different users/tenants/projects in sequence.
- For cache or memoization changes, prove cache keys cannot cross tenants.
- For singleton or scoped binding changes, inspect the service provider and the consuming class lifecycle.
- For RoadRunner migration readiness, search for direct `Swoole`, coroutine, task-worker, and server-specific API usage in touched code.
- If runtime hooks, worker tuning, memory growth, or hot-path performance are in scope, switch to `alaa-octane-performance`.
