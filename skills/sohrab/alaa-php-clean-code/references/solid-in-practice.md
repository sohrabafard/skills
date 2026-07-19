# SOLID in practice (PHP 8.5 / Laravel 13)

## Contents
- How to apply SOLID here
- Single Responsibility (SRP)
- Open/Closed (OCP)
- Liskov Substitution (LSP)
- Interface Segregation (ISP)
- Dependency Inversion (DIP)
- SOLID review checklist

## How to apply SOLID here
SOLID is a lens for finding the smell, not a scoring system. Apply each principle only where its absence is causing real pain: hard-to-test code, shotgun changes, unstable contracts, or unsafe Octane state. The pattern catalog in `design-patterns.md` is the toolbox; this file explains which principle each tool serves.

## Single Responsibility (SRP)
One reason to change per class. In Laravel terms: a class that mixes validation, authorization, query composition, business rules, and serialization changes for five unrelated reasons.

- ✅ Do: `CommentService` (rules + events) calling `CommentRepositoryInterface` (queries) and returning DTOs that a Resource serializes. Each class changes for one reason.
- ❌ Don't: a controller method that validates inline, checks `auth()->user()->can(...)`, composes an Eloquent query, mutates the model, and builds the JSON array. Every product change touches this method, and none of it is testable in isolation.

Practical cuts: fat controller → Form Request + Service; fat service → split by use case, not by entity; fat repository → query objects per read model.

## Open/Closed (OCP)
Add behavior by adding classes, not by editing stable ones. Relevant when variation is real: providers, algorithms, channels, tenant-specific policies.

- ✅ Do: new SMS provider = new class implementing `SmsSender` + one binding/map entry (Strategy + Adapter). Existing senders and callers stay untouched.
- ❌ Don't: `match ($provider) { 'mediana' => ..., 'kavenegar' => ..., }` duplicated in three services, each edited for every new provider.
- Balance: a single local `match` in one factory is fine — OCP applies to the call sites, not to the one place selection is centralized.

## Liskov Substitution (LSP)
Every implementation must honor the interface's contract — same invariants, same exception ownership, no surprise preconditions. This is what makes decorators and fakes trustworthy.

- ✅ Do: `CachedCommentRepository` returns exactly what `PostgresCommentRepository` would return (possibly staler), and falls through to it on cache failure. Callers cannot tell the difference — that is LSP working.
- ❌ Don't: an implementation that returns `null` where the interface promises an exception, throws `RedisException` from a method whose contract is domain-only exceptions, or requires callers to call `warmUp()` first.
- Test seam: run the same contract test against the real implementation, the decorator, and the fake.

## Interface Segregation (ISP)
Consumer-shaped interfaces. A port with fifteen methods is a database interface wearing a costume; implementations and fakes then carry dead weight.

- ✅ Do: split `CommentRepositoryInterface` (write path) from `CommentQueryInterface` (list/read models) when a consumer needs only one side.
- ❌ Don't: one `BaseRepositoryInterface` with generic CRUD that every repository "implements" with half the methods throwing `NotSupported`.

## Dependency Inversion (DIP)
High-level code depends on abstractions it owns; infrastructure implements them. In Laravel: services depend on repository/adapter interfaces; providers bind concretes; the container does the wiring.

- ✅ Do: `CommentService` takes `CommentRepositoryInterface` in its constructor; the provider binds Postgres (optionally wrapped by the cache decorator). Swapping stores or adding caching never touches the service.
- ❌ Don't: `new PostgresCommentRepository()` inside a service, `app()->make(...)` service-location in domain code, or a domain class importing a vendor SDK directly.
- Recognition signals that DIP is being violated (invert at a small interface when any appear): a service cannot be unit-tested without a database, broker, or vendor API; swapping a provider means editing business classes instead of one binding; a test mocks concrete classes instead of passing a fake through a constructor.
- The abstraction belongs to the consumer: shape the interface as what the service *needs* (domain-shaped, few methods), not as a mirror of what the infrastructure offers — a port that mirrors pgx/Eloquent/SDK is inverted in name only.
- DIP is what makes the repository-pattern gate for Redis caching possible: caching can only be inserted at an interface seam that already exists.

## SOLID review checklist
- Can I name the one reason each touched class changes? (SRP)
- Would the next provider/algorithm/channel require editing existing call sites? (OCP)
- Could every implementation, decorator, and fake pass the same contract test? (LSP)
- Does any consumer see interface methods it never calls? (ISP)
- Does any domain/service class construct or locate its own infrastructure? (DIP)
