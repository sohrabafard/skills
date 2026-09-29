The official Fiber API baseline for this slice was verified on **2026-07-26**; claim-specific source URLs and later refresh dates are in [SOURCES.md](../SOURCES.md).

## Server bounds

`fiber.Config` verified at https://docs.gofiber.io/api/fiber on 2026-07-26:

| Field | Type | Fiber default | Why the default is unsafe |
| --- | --- | --- | --- |
| `ReadTimeout` | `time.Duration` | `0` | Unbounded. A client that opens a connection and dribbles a request header holds a connection open forever (slowloris). |
| `WriteTimeout` | `time.Duration` | `0` | Unbounded. A slow reader pins a response and its buffers indefinitely. |
| `IdleTimeout` | `time.Duration` | `0` | Unbounded. Keep-alive connections are never reaped. |
| `BodyLimit` | `int` | `4 * 1024 * 1024` | 4 MiB, larger than the platform request cap. |
| `Immutable` | `bool` | `false` | See the context-lifetime section above. |
| `TrustProxy` | `bool` | `false` | Forwarded headers are not trusted until this is `true`; see `20-routing-middleware-errors.md`. |
| `TrustProxyConfig` | `TrustProxyConfig` | `{}` | No proxies trusted; see `20-routing-middleware-errors.md`. |
| `StructValidator` | `StructValidator` | `nil` | Bind performs no validation; see `30-validation-testing.md`. |
| `ErrorHandler` | `ErrorHandler` | `DefaultErrorHandler` | Renders Fiber's own error shape, not the platform envelope. |

`SKILL.md` requires all four to be set and names `/alaa-services-contract` as the owner of their values. For reference, the kit's chi services
run `HTTP_READ_TIMEOUT` 10s, `HTTP_WRITE_TIMEOUT` 30s, `HTTP_IDLE_TIMEOUT`
120s and `HTTP_MAX_BODY_BYTES` 1 MiB, each read from validated environment configuration and
clamped at boot to a permitted range. A Fiber service reads the same environment keys and enforces
the same clamps, because an operator who tunes one service should not need to learn a second
vocabulary.

```go
app := fiber.New(fiber.Config{
	ReadTimeout:     cfg.HTTP.ReadTimeout,
	WriteTimeout:    cfg.HTTP.WriteTimeout,
	IdleTimeout:     cfg.HTTP.IdleTimeout,
	BodyLimit:       int(cfg.HTTP.MaxBodyBytes),
	StructValidator: &structValidator{validate: validator.New()},
	ErrorHandler:    envelopeErrorHandler,
})
```

A config value that arrives out of range fails the boot. Do not clamp silently and do not default
quietly: an operator who sets `HTTP_READ_TIMEOUT=0` intending "no limit" must be told at boot that
the value is rejected, not discover it during an incident.

## Unmatched-route fast path (v3.5.0)

`SkipUnmatchedRoutes` defaults to `false`; enabling it returns `404`/`405` before middleware runs,
with a CORS-preflight exception (https://github.com/gofiber/fiber/releases/tag/v3.5.0, verified
2026-09-29). Keep it disabled when correlation, access logs, metrics or trust checks depend on that
chain. Before enabling it, prove missing-path and wrong-method responses still satisfy the platform
error and correlation contracts, and test preflight behavior. A faster router is not that proof.
