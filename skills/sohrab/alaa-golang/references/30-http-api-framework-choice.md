# HTTP API Framework Choice

Use this file when the task is about picking, reviewing, or justifying the HTTP layer for a Go service.

## Default decision for this pack

For a new HTTP API, choose `chi`.

Use `fiber` only when there is a clear reason. Do not treat router choice as a taste issue.

## Why `chi` is the default here

`chi` fits this stack better because it stays inside the standard `net/http` model.

That matters in this environment because you care about:

- trusted gateway integration
- predictable request context and cancellation
- explicit timeouts and graceful shutdown
- easy interop with OpenTelemetry, Prometheus, reverse proxies, and standard middleware
- low-friction testing with `httptest`
- long-term maintainability under production pressure

`chi` is also a small dependency with minimal abstraction cost. It feels like Go, not like a framework trying to hide Go.

## When `fiber` is a valid choice

Choose `fiber` when at least one of these is true:

- the existing service already uses Fiber and the team wants consistency
- the team explicitly wants Fiber's Express-like ergonomics
- there is measured evidence that the chosen workload benefits enough from Fiber and the team accepts the tradeoffs
- the surrounding repo already invested in Fiber middleware, helpers, and conventions

## Why `fiber` is not the default here

Fiber is built on `fasthttp`, not the standard `net/http` stack.

That can be completely fine, but it changes the interoperability story. In this pack, that matters because the baseline heavily uses standard `net/http` assumptions across middleware, observability, testing, reverse proxies, and operational debugging.

Use Fiber on purpose, not by accident.

## Decision table

### Choose `chi` when

- you are starting a new service
- the service sits behind a trusted gateway or HAProxy and you want standard request semantics
- observability and operational clarity matter more than framework convenience
- you want the easiest path to `otelhttp`, `promhttp`, standard middleware, and standard tests
- the service has long-lived maintainers and should feel like idiomatic Go

### Choose `fiber` when

- the repo already uses Fiber
- the team is already productive with Fiber and accepts its model
- you have measured performance reasons, not assumed ones
- you are comfortable validating observability, timeout, proxy, and shutdown behavior carefully in that stack

## Red flags before choosing `fiber`

- “It is faster” without benchmark evidence for your workload
- “It feels nicer” when the rest of the platform is `net/http`-oriented
- “We may migrate later” with no migration plan
- “It is more like Node” when the real need is better local conventions, not a different router

## Red flags before choosing `chi`

- the repo already has deep Fiber conventions and you are trying to replace them casually
- the team expects framework-driven features that you have no plan to rebuild with idiomatic helpers

## Practical rule

For this pack:

- new HTTP API: `chi`
- existing Fiber service: keep Fiber unless there is a strong reason to migrate
- migration from Fiber to `chi`: treat as architecture work, not routine refactoring

## What to read next

- Read `31-chi-api-guide.md` when `chi` is chosen.
- Read `40-production-ready-package-catalog.md` for supporting packages around routing, validation, config, logging, and observability.
- Route to `golang-project-layout` ( `$golang-project-layout` ), `golang-context` ( `$golang-context` ), `golang-observability` ( `$golang-observability` ), and `golang-testing` ( `$golang-testing` ) for the implementation details around the chosen transport.
