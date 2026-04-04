# Alaa Golang Full Guide

## Table of contents

- Release and compatibility policy
- Merged baseline
- Concurrency and lifecycle discipline
- Style and API hygiene
- Fiber service structure
- Validation baseline
- Routing heuristics

## Release and compatibility policy

Go does not have an official LTS branch. The official rule is that each major Go release stays supported until there are
two newer major releases. For this skill, that means:

- use the latest stable Go release as the primary target
- keep the still-supported previous major release in mind for real-world repos that have not moved yet
- verify the current release state from `https://go.dev/doc/devel/release` before making version-sensitive claims

At the time of this refresh:

- `go1.26.1` is the latest stable release
- `go1.25.8` is the previous still-supported line

For framework-heavy projects, do not assume that "latest Go" equals "safe framework upgrade". Fiber v3 explicitly warns
that its `unsafe` usage may not always be compatible with the latest Go version and says it has been tested with Go
`1.25` or higher. Always verify the framework's compatibility note before recommending a Go toolchain bump.

## Merged baseline

This skill merges three external influences into one Go-native operating model:

1. Concurrency discipline from `effect-concurrency-fibers`
    - translate "fiber lifecycle" ideas into Go ownership rules for goroutines, contexts, channels, and `errgroup`
    - favor bounded parallelism, explicit cancellation, and deterministic shutdown
2. Code clarity and correctness from the Uber Go style guide
    - prefer simple, explicit, reviewable code over cleverness
    - treat boundary safety, error handling, and performance defaults as part of maintainability
3. Production structure from the Fiber best-practices skill
    - keep transport thin, business logic out of handlers, and project layout modular without over-architecting

The resulting stance is:

- right-size the architecture to the problem
- keep public APIs small and internal code movable
- keep concurrency supervised
- keep observability and shutdown behavior first-class
- keep transport details separate from domain and storage logic

## Concurrency and lifecycle discipline

Translate the requested "fibers" guidance into Go like this:

### Goroutine ownership

- Every goroutine must have an owner.
- The owner must know how the goroutine exits, how it is canceled, and when it has fully stopped.
- Do not launch background work from random helpers just because `go func()` is cheap.

### Preferred sibling-task model

- Use `errgroup.WithContext` for sibling tasks that should fail together.
- Use `SetLimit` or another explicit limiter when parallelism can grow with input size.
- Keep task fan-out bounded around external I/O, remote APIs, or database work.

### Cancellation and timeouts

- Pass `context.Context` through every request, worker, and background operation that can block.
- Use `context.WithTimeout` or `context.WithDeadline` around remote calls and latency-sensitive work.
- In loops or select-based workers, always watch `ctx.Done()`.

### Racing operations

- Race two operations only when you can cancel the loser cleanly.
- "Fastest wins" is not safe if the slower path continues running and holding resources.
- If you add timeout races, make timeout behavior explicit in logs, metrics, or returned errors.

### Worker pools and channels

- Use worker pools when input volume is high enough to justify bounded parallel processing.
- Avoid large buffered channels unless you can explain the capacity, backpressure behavior, and overload outcome.
- A channel size of `0` or `1` is the default safe choice. Larger buffers require justification.

### Fire-and-forget rule

- Do not fire-and-forget goroutines in normal application code.
- If truly needed, define:
    - who owns the goroutine
    - which context or stop signal ends it
    - how shutdown waits for it
    - which logs or metrics prove it is healthy

### Shutdown order

For servers and workers:

1. stop accepting new work
2. cancel the owning context
3. wait for goroutines and worker pools to exit
4. close downstream resources after the workers that use them have stopped

## Style and API hygiene

Use the installed style skills for the full ruleset. The merged baseline here is the short version:

### Clarity

- Prefer early returns.
- Reduce nesting.
- Remove unnecessary `else` blocks after `return`, `break`, or `continue`.
- Keep handlers and orchestration functions thin.

### Interfaces and receivers

- Do not use pointers to interfaces.
- Verify interface compliance when the interface is part of the contract.
- Choose value or pointer receivers deliberately, especially for map elements, interface satisfaction, and mutation.

### State safety

- Zero-value mutexes are valid.
- Keep mutexes as named fields rather than embedded public implementation details.
- Copy slices or maps at boundaries when aliasing would leak internal mutable state.

### Errors

- Wrap errors with `%w` when callers need the original cause.
- Handle errors once, close to the right abstraction level.
- Avoid panics for normal control flow.
- Use structured logging rather than ad hoc `fmt.Println` traces.

### Performance defaults

- Prefer `strconv` over `fmt` for simple hot-path conversions.
- Preallocate slices or maps when size is known or clearly inferable.
- Do not speculate about performance. Measure first when the change is non-obvious.

### Public surface

- Export less by default.
- Keep package names simple and descriptive.
- Use field names in struct literals.
- Keep `context.Context` as the first parameter when it applies.

## Fiber service structure

Apply this section only when the project uses Fiber.

### Layout

- Put entrypoints in `cmd/<service>/main.go`.
- Keep server wiring, config loading, dependency construction, and lifecycle management outside route handlers.
- Keep business logic in `internal/` packages, not inside `main.go`.
- Use `pkg/` only for code that is intentionally reusable outside the service.

### Handler boundaries

- Keep Fiber handlers thin.
- Parse, validate, and normalize request data at the edge.
- Call services or use-cases from handlers instead of embedding business rules directly in the route layer.
- Avoid direct database, queue, or filesystem logic in handlers unless the task is trivially small and intentionally
  flat.

### Middleware and request-scoped data

- Use middleware deliberately and keep ordering explicit.
- If request IDs feed logs or traces, install the request ID middleware before the middleware that emits those values.
- Use request-scoped locals only for request-scoped data, not as a hidden service container.
- Constructor-inject shared dependencies during app bootstrap.

### Logging and observability

- Prefer structured JSON logs to ad hoc console prints.
- Log stable fields such as request ID, method, path, status, latency, and error category.
- Route deep observability work to `golang-observability` and `alaa-observability-soc`.

### Configuration and security

- Centralize environment parsing and config validation.
- Do not scatter `os.Getenv` calls across handlers.
- Make body limits, timeouts, trusted proxies, and other security-sensitive HTTP settings explicit.
- Trust proxy headers only for proxies you control.

### Interop

- Prefer native Fiber handlers for Fiber codepaths.
- Use `net/http` adaptors only when interoperability is a real requirement.
- Document any bridge layer because it changes semantics, performance, and debugging behavior.

## Validation baseline

Use the narrowest validation that matches the task:

- `go test ./...` for basic behavioral confidence
- `go test -race ./...` when shared state, goroutines, or channels are involved
- `go vet ./...` for native static checks
- project lint command or `golangci-lint` flow when lint ownership matters
- benchmarks or profiles only when performance is the real decision surface

For Fiber services, also validate:

- middleware order
- graceful shutdown
- timeouts and cancellation behavior
- proxy-trust behavior
- request IDs and logs on success and failure paths

## Routing heuristics

- If the task is "upgrade this codebase to current Go idioms", start with `golang-modernize`.
- If the task is "why is this concurrent code leaking, racing, or hanging", load `golang-concurrency`, `golang-context`,
  and often `golang-troubleshooting`.
- If the task is "implement or review a Fiber service", load `golang-project-layout`, `golang-design-patterns`,
  `golang-error-handling`, `golang-observability`, and `golang-testing`.
- If the task changes production behavior, then add the relevant Sohrab companion skills from `20-sohrab-companions.md`.
- If the repo already imports a Samber library, load the corresponding `golang-samber-*` skill rather than reinventing
  local conventions.
