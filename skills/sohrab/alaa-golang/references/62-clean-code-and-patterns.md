# Clean Code and Go Patterns

Use this file when writing or reviewing Go code in this pack.

## Core rules

- Keep packages small and named by purpose.
- Avoid `utils`, `helpers`, and broad shared packages.
- Accept interfaces at consumer boundaries; return concrete types from constructors.
- Prefer constructor injection.
- Keep global mutable state out of service code.
- Avoid `init()` for service wiring.
- Propagate `context.Context`.
- Wrap errors with useful context.
- Do not log and return the same error repeatedly.
- Keep comments useful and sparse.

## Boundaries

Domain packages should not import:

- chi
- Fiber
- database drivers
- Redis clients
- queue clients
- HTTP request/response types

Transport packages adapt the outside world to use case inputs. Infrastructure packages adapt DB, Redis, queues, and external APIs to interfaces.

## Patterns to use

### Repository

Use for persistence boundaries and database-backed behavior.

### Use case or service

Use for application behavior that coordinates repositories, cache, transactions, authorization, and events.

### Adapter

Use to keep external systems behind small interfaces.

### Constructor

Use to make dependencies explicit and testable.

### Functional options

Use only when a constructor has many optional settings. Do not use options to hide required dependencies.

### Strategy

Use only when real interchangeable behavior exists, such as different cache policies or dispatch algorithms.

### Decorator or middleware

Use for cross-cutting behavior such as logging, tracing, metrics, retry wrappers, and cache decorators.

## Concurrency rules

- Every goroutine has an owner.
- Every goroutine has a cancellation path.
- Every goroutine reports errors or is intentionally fire-and-forget with documented reason.
- Use bounded worker pools for untrusted or high-volume work.
- Run race tests for shared state.

## Anti-patterns

- SQL in handlers
- Redis in handlers
- business logic in middleware
- global service containers used everywhere
- unbounded goroutines
- hidden retries in helper functions
- framework types in domain or repository interfaces
- cache lookups that bypass authorization
- broad interfaces with methods the consumer does not need

## Review checklist

- Is the behavior tested?
- Are dependencies explicit?
- Is the context propagated?
- Is the error useful and safe?
- Does the package name describe one purpose?
- Can the use case be tested without HTTP, DB, or Redis?
- Does the code preserve existing repo conventions?
