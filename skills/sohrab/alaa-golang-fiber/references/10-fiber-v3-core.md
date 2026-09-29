# Fiber v3 Core: App, Config, Context Lifetime, Listener

Read this file when you are about to create a `fiber.App`, set `fiber.Config`, set server bounds,
or start and stop the listener.

Unless individually refreshed below, API names, signatures and defaults were verified against the
official Fiber v3 docs on **2026-07-26**. Source URLs are listed per claim and collected in `SOURCES.md`.

## Version and import

When checking Fiber package identity or compatibility, read [Version and import](./10-fiber-v3-core/10-version-and-import.md) for the verified module, Go minimum, and fasthttp boundary.

## Context value lifetime: the one memory-corruption hazard

When a request value may outlive its handler, read [Request value lifetime](./10-fiber-v3-core/20-request-value-lifetime.md) for buffer reuse and copying rules.

### `Immutable` is a boot-time service-wide decision

When deciding whether to enable immutable mode or use its accessors, read [Immutable mode](./10-fiber-v3-core/30-immutable-mode.md) for ownership, allocation, and safe accessor rules.

### `fiber.Ctx` is a `context.Context` whose cancellation does nothing

When passing context to dependencies from a handler, read [Context cancellation](./10-fiber-v3-core/40-context-cancellation.md) for cancellation limits and deadline handling.

## Server bounds

When configuring server limits, read [Server bounds](./10-fiber-v3-core/50-server-bounds.md) for defaults, platform caps, validation, and rejected values.

## Unmatched-route fast path (v3.5.0)

Before enabling the unmatched-route fast path, read [Server bounds](./10-fiber-v3-core/50-server-bounds.md) for middleware, response-contract, and preflight checks.

## Boot order

When constructing the application, read [Boot order](./10-fiber-v3-core/60-boot-order.md) for validated startup order and dependency boundaries.

## Listener and shutdown

When starting or stopping the listener, read [Listener and shutdown](./10-fiber-v3-core/70-listener-shutdown.md) for API choices, timeouts, readiness, draining, and close order.

## Hooks

When using lifecycle hooks, read [Hooks and custom context](./10-fiber-v3-core/80-hooks-and-custom-context.md) for their narrow diagnostic and readiness scope.

## Custom context

When adding a custom context, read [Hooks and custom context](./10-fiber-v3-core/80-hooks-and-custom-context.md) for the transport-only role and constructor-injection boundary.
