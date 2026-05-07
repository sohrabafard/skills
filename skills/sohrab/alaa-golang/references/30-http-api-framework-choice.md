# HTTP API Framework Choice

Use this file when choosing, reviewing, or justifying the HTTP layer for a Go service.

## Decision order

1. If the user explicitly says chi, use chi.
2. If the user explicitly says Fiber, load `alaa-golang-fiber` ( `$alaa-golang-fiber` ).
3. If the repo already imports `github.com/go-chi/chi/v5`, preserve chi.
4. If the repo already imports `github.com/gofiber/fiber/v3` or older Fiber, load `$alaa-golang-fiber` and preserve Fiber.
5. If the repo is raw and small/simple, recommend chi.
6. If the repo is raw and large, high-concurrency, latency-sensitive, or SLA-heavy, recommend Fiber and load `$alaa-golang-fiber`.
7. If the repo is raw and unclear, inspect expected traffic, route count, middleware needs, team preference, and deployment model before choosing.

Do not migrate frameworks casually.

## Choose chi when

- the service is small or simple
- standard `net/http` semantics are more valuable than framework features
- `httptest`, `otelhttp`, `promhttp`, and ordinary middleware compatibility matter most
- the team wants low abstraction and long-term maintainability
- the repo already uses chi

Read `31-chi-api-guide.md` next.

## Choose Fiber when

- the repo already uses Fiber
- the user explicitly chooses Fiber
- the service is large or high-concurrency
- strict latency or heavy request volume makes Fiber's model worth the tradeoff
- the team accepts `fasthttp` semantics and Fiber-specific context rules

Load `alaa-golang-fiber` ( `$alaa-golang-fiber` ) next.

## Why the split exists

Chi keeps Go services close to the standard library. That is excellent for small services and for teams that want the simplest possible HTTP stack.

Fiber can be a strong choice for larger, high-concurrency services, but it is built on `fasthttp`, not standard `net/http`. That means agents must learn Fiber-specific context, middleware, testing, proxy, and shutdown behavior before editing a Fiber service.

## Red flags

Before choosing chi:

- the repo already has deep Fiber conventions
- the service is explicitly expected to be very high-concurrency and the team wants Fiber

Before choosing Fiber:

- the service is small and simple
- the team only wants Fiber because it feels like Express
- the repo depends heavily on standard `net/http` middleware
- no one has accepted Fiber-specific context and proxy behavior

## Practical rule

- explicit framework choice: follow it
- existing framework: preserve it
- raw small/simple service: chi
- raw large/high-concurrency service: Fiber
- migration: architecture work, not routine refactoring
