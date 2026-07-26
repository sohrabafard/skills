# Octane-safe pattern shaping

## What this file is, and what it is not

This file answers one question: **for each design pattern, what shape does it have to take so the Octane worker invariants hold?** It states no invariant of its own.

**The invariants live in `/alaa-octane-performance` (`$alaa-octane-performance`), and its wording governs.** That skill owns, and this file does not restate:

- the enumerated list of values that may never be retained, and the enumerated sites where retaining them is forbidden;
- the reset mechanism — the scoped-binding form, the `config/octane.php` flush list, and the request-terminated listener;
- worker lifecycle, reload, and sizing;
- the cross-request leak regression test and the mechanic that makes it fail against a leaking implementation;
- connection and Redis lifecycle, and the cache tiers;
- Swoole-to-RoadRunner portability, including which Swoole-only APIs may appear where;
- precedence over the upstream `octane-development` skill, which this repository does not own.

Read it before binding any service, adding any static property, reusing any SDK client, or shipping a change to a service that a worker resolves once. If you have read only this file, you have not yet read the invariant — go there.

`SKILL.md` carries the three always-loaded code-shape rules: nothing belonging to one request is retained beyond it; a per-request value arrives as a method argument; a memoization key inside a long-lived object carries the tenant or project identifier.

## Per-pattern shaping

Six patterns carry their Octane note inside `design-patterns.md` itself, at the pattern: **Service**, **Observer**, **Adapter**, **Facade**, **Singleton**, and **Pipeline**. Read them there; they are not repeated here.

The rest, one line each:

| Pattern | The shape that holds under a long-lived worker |
|---|---|
| MVC | A controller may read request context and must not retain it. It hands validated input to a service or a DTO and keeps nothing on itself. |
| Repository | A repository never remembers "the current tenant". It takes the tenant or project identifier, or a typed filter DTO, per call — or uses a reset-safe global-scope/RLS approach the repository already sanctions. A repository that resolves tenancy internally leaks it to the next request on that worker. |
| Factory | A factory may hold an immutable map of strategy or adapter class names. It must not hold a built provider instance that carries request headers, tokens, tenant values, or mutable options — build those per call. |
| Strategy | A strategy is stateless. Request data arrives as an argument to `execute`, `calculate`, `handle`, or whatever the contract's method is named, never as constructor state. |
| Builder | A builder is either constructed per use or holds no accumulated state. Never reuse one mutable builder instance across requests: the second request inherits the first request's partial payload. |
| Proxy / lazy object | A lazy ghost or proxy resolved into a worker-lifetime service initialises once for the worker, not once per request. Only use one for a dependency whose initialised state is request-independent. |
| DTO / value object | `readonly` makes these safe to share by construction. A mutable DTO reachable from a worker-lifetime object is a leak; `clone` it or make it `readonly`. |
| Command / job | A job carries scalar IDs and typed payloads plus its tenant or project identifier explicitly, never an ambient one. Its handler is idempotent, because a retry is the normal consequence of an at-least-once queue. |
| Prototype | Default `clone` is shallow. Implement `__clone()` to deep-copy nested mutable objects, or a shared nested object becomes cross-request state. |
| Flyweight | Shared intrinsic state is immutable; per-use extrinsic state is a method argument. A mutable shared instance is a cross-request data leak by construction. |

## The one review check this file owns

Every service, factory, strategy, adapter, observer, listener, job, and pipeline step touched by the change is either stateless or reset-safe — name which, per class, before declaring the work done. If you cannot name it for a class, that class is the finding.

For a leak-prone change, the regression test and what it must assert belong to `/alaa-octane-performance` (`$alaa-octane-performance`). For cache and memoization keys, key design belongs to `alaa-data-layer references/50-redis-laravel-octane.md`.
