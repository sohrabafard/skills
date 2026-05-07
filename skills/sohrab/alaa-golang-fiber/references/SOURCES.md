# Fiber Source Map

Use these sources when a Fiber detail is version-sensitive or must be exact.

## Official Fiber docs

### https://docs.gofiber.io/

Use for current Fiber version, installation, Go version requirement, zero-allocation/context lifetime rules, and basic routing.

### https://docs.gofiber.io/whats_new/

Use for Fiber v3 changes, migration notes, `ListenConfig`, hooks, routing changes, middleware data access, and v2-to-v3 differences.

### https://docs.gofiber.io/api/app/

Use for `fiber.App`, `app.Test`, route registration, config, and app behavior.

### https://docs.gofiber.io/api/ctx/

Use for `fiber.Ctx`, `Locals`, value access, request and response behavior.

### https://docs.gofiber.io/guide/go-context/

Use for Go context behavior and integration notes.

### https://docs.gofiber.io/guide/error-handling/

Use for returned errors, custom `ErrorHandler`, `fiber.Error`, and recover requirements.

### https://docs.gofiber.io/guide/validation/

Use for `StructValidator`, bind validation, and validator examples.

### https://docs.gofiber.io/guide/reverse-proxy/

Use for reverse proxy deployment, HTTP/2, proxy headers, and edge setup.

### https://docs.gofiber.io/middleware/healthcheck/

Use for liveness, readiness, startup, and probe response behavior.

### https://docs.gofiber.io/middleware/requestid/

Use for request ID middleware, header behavior, and context helper access.

### https://docs.gofiber.io/middleware/cors/

Use for CORS options and unsafe wildcard/credentials combinations.

### https://docs.gofiber.io/middleware/limiter/

Use for limiter config, storage behavior, and multi-instance cautions.

## Go testing sources

### https://pkg.go.dev/testing

Use for `testing.T`, `testing.F`, `t.Run`, `t.Helper`, `t.Cleanup`, and package-level test behavior.

### https://go.dev/blog/subtests

Use for table-driven subtests, sub-benchmarks, parallel subtest behavior, and focused `go test -run` usage.

### https://go.dev/doc/security/fuzz/

Use for Go fuzzing rules, seed corpus behavior, fast deterministic fuzz targets, and security-sensitive input testing.

## Conflict order

1. official Fiber docs
2. official Go docs
3. repo-local service contracts and `alaa-golang`
4. vendored public Go skills
5. community examples only for troubleshooting concrete symptoms
