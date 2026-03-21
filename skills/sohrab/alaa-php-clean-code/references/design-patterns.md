# PHP / Laravel design patterns

## Contents
- Interfaces and dependency injection
- Repository pattern
- Factory pattern
- DTO pattern
- Value object pattern
- Strategy pattern
- Query object / filter DTO pattern
- Exception translation pattern

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
- Persistence logic is non-trivial and repeated.
- Query composition deserves a stable home.
- The code works against a meaningful persistence boundary or aggregate.
- Multiple storage implementations are plausible.

### Laravel application
- Keep repositories in the persistence layer defined by the repo architecture.
- Let services orchestrate business rules and call repositories for persistence and query composition.
- Accept typed filter DTOs instead of raw request arrays.

### Good defaults
- Model the repository around the domain use case, not around generic CRUD.
- Keep business rules, authorization, and serialization out of the repository.
- Return domain objects, DTOs, collections, or paginators that match repo conventions.

### Anti-patterns
- One repository per Eloquent model with only `create`, `update`, `delete`, `find`.
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

## Query object / filter DTO pattern

### Use when
- Query logic becomes too complex for one repository method signature.
- Optional filters, sorts, and scopes multiply.
- Search or listing logic deserves its own testable unit.

### Laravel application
- Keep validated filter input in a typed DTO.
- Optionally introduce a query object when repository methods become hard to read.
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
