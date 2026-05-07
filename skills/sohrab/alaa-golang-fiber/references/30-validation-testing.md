# Validation and Testing

Use this file before changing Fiber request contracts or behavior.

## Binding

- Bind request data into transport DTOs, not domain entities.
- Keep DTO validation at the edge.
- Convert DTOs into use case inputs after validation.
- Keep raw Fiber binding behavior out of domain packages.

## Validation

Configure a `StructValidator` in `fiber.Config` when using Fiber bind validation.

Use `go-playground/validator/v10` when field and cross-field validation belongs on request DTOs. Treat binding errors and validation errors separately:

- binding error: request could not be parsed
- validation error: request parsed but violated rules

Return stable client errors and avoid leaking internal field names if the public API uses different names.

## TDD workflow

For behavior changes:

1. Red: write or update a failing test first.
2. Green: implement the smallest code that passes.
3. Refactor: improve names, boundaries, and duplication after tests pass.

Run the focused test after each step. Finish with `go test ./...`.

## Handler tests

Use `app.Test(req, fiber.TestConfig{...})` for Fiber handler behavior.

Test:

- status codes
- response body shape
- headers
- request ID or trace propagation when relevant
- validation errors
- domain error mapping
- panic recovery behavior
- auth or trusted gateway middleware behavior

## Unit tests

Unit-test domain, use case, repository contracts, and cache policy without Fiber.

Prefer hand-written fakes for small interfaces. Use mocks only when call interaction is the behavior being tested.

## Integration tests

Use real PostgreSQL, Redis, queues, or proxies only when the behavior depends on real storage, driver, or network semantics.

Route broader Go testing decisions to `$golang-testing` and Testify-specific work to `$golang-stretchr-testify` when the repo uses it.

## Race and fuzz

- Run `go test -race ./...` for shared state, caches, goroutines, workers, and high-concurrency code.
- Add fuzz tests for parsers, codecs, validators, and untrusted input surfaces.
- Keep fuzz targets fast, deterministic, and free of persistent global state.
