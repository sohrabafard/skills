The official Fiber API baseline for this slice was verified on **2026-07-26**; claim-specific source URLs and later refresh dates are in [SOURCES.md](../SOURCES.md).

## Hooks

Fiber's startup and shutdown hooks carry lifecycle events only: startup diagnostics, the
readiness flip, and the shutdown result. No business logic runs in a hook, because a hook has no
request context, no trust context and no error path back to a client.

## Custom context

`Ctx` is an interface in v3 with `DefaultCtx` as its implementation, and `NewWithCustomCtx` builds
an app over a custom one (https://docs.gofiber.io/whats_new, verified 2026-07-26). Use a custom
context only to remove duplication that is genuinely at the transport edge, such as a repeated
accessor for a value the trust middleware placed in the request context. Dependencies reach
handlers through constructor injection on the handler struct, never through a custom context.
