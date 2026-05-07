# TDD and Testing Discipline

Use this file before behavior-changing Go implementation.

## Core rule

No behavior-changing code is done until tests prove it.

Follow Red, Green, Refactor:

1. Red: write or update a failing test.
2. Green: implement the smallest passing change.
3. Refactor: improve design after tests pass.

This applies to domain logic, use cases, repositories, cache policy, handlers, bug fixes, and concurrency behavior.

## What to test first

Test the behavior closest to the rule:

- domain rule: domain unit test
- use case flow: use case unit test with fakes
- repository contract: fake-backed unit test or real DB integration test
- Redis cache policy: cache unit test with fake plus real Redis integration where needed
- HTTP error mapping: handler test
- validation: DTO validation test
- concurrency: race-sensitive unit or integration test

## Go test structure

- Use `*_test.go` files.
- Use table-driven tests for behavior matrices.
- Use `t.Run` for subtests.
- Use clear subtest names.
- Use `t.Helper()` in helpers.
- Use `t.Cleanup()` for cleanup.
- Keep tests deterministic.

## Test doubles

Prefer hand-written fakes for small interfaces. Use mocks only when the interaction itself is the behavior being tested.

Do not mock what you do not own unless the test needs that seam.

## Integration tests

Use real PostgreSQL, Redis, queues, or HTTP services only when behavior depends on real driver, storage, or network semantics.

Use Testcontainers when a real dependency is needed and the repo already supports containerized tests.

## Race and fuzz

- Run `go test -race ./...` for shared state, cache, goroutines, worker pools, and concurrency changes.
- Add fuzz tests for parsers, codecs, validators, and untrusted input.
- Keep fuzz targets fast, deterministic, and free of persistent global state.

## Agent workflow

When implementing:

1. inspect existing tests
2. add or update the focused failing test
3. run the focused test and confirm it fails for the right reason
4. implement the smallest change
5. rerun the focused test
6. refactor
7. rerun focused tests
8. run the broader package or repo tests that match risk

If a test cannot be added, record why and add the smallest meaningful validation instead.
