# Routing, Middleware, and Errors

Use this file for Fiber route design, middleware order, error mapping, CORS, limiter, and trusted proxy behavior.

## Routing

- Group routes by stable API version or domain boundary.
- Keep route registration close to the transport package.
- Keep handlers small and call use cases.
- Do not perform DB queries or Redis calls in handlers.
- Avoid dynamic route mutation in production services unless the repo explicitly owns that pattern.

## Middleware order

Use a clear order:

1. recover
2. request ID
3. tracing/log context
4. security headers when used
5. CORS when the service owns browser access
6. trusted gateway or auth context extraction
7. rate limit or backpressure
8. body parsing and validation
9. handlers

Mount public health and readiness endpoints intentionally. Do not accidentally put protected business middleware in front of probes unless the platform contract requires it.

## Errors

Handlers and middleware should return errors. Centralize HTTP error mapping in `fiber.Config.ErrorHandler`.

Rules:

- Map domain errors to stable status codes.
- Return validation errors in a stable response shape.
- Log internal details once, at the boundary.
- Do not return SQL details, secrets, stack traces, trusted identity internals, or authorization reasons to clients.
- Use recover middleware because Fiber does not recover panics by default.

## Request ID

Use Fiber request ID middleware or the platform request ID contract. In Fiber v3, middleware data may be exposed through package helper functions such as `requestid.FromContext(c)`. Prefer those helpers over stringly `Locals` lookups for middleware-owned values.

## CORS

Configure CORS only when the service owns browser-facing behavior.

- Never combine wildcard origins with credentials.
- Never write an `AllowOriginsFunc` that returns true for every origin.
- Prefer explicit origins from config.
- Keep CORS policy aligned with gateway and frontend deployment rules.

## Limiter

Fiber limiter in-memory storage is process-local. That is not a global limit in multi-replica services.

Use:

- gateway-level limits for shared platform policy
- Redis/shared storage when service-local limits must work across replicas
- explicit key generation that cannot be spoofed by untrusted headers

## Trusted proxy

Only trust forwarded headers when trusted proxy config is enabled and restricted to known proxy IPs or ranges.

Do not derive client IP, host, scheme, tenant, identity, or authorization context from spoofable client headers.

Pair with `$alaa-trust-gateway-auth` and `$alaa-haproxy` when gateway trust semantics matter.
