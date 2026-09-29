The official Fiber API baseline for this slice was verified on **2026-07-26**; claim-specific source URLs and later refresh dates are in [SOURCES.md](../SOURCES.md).

## Listener and shutdown

Verified at https://pkg.go.dev/github.com/gofiber/fiber/v3 and
https://raw.githubusercontent.com/gofiber/fiber/v3.3.0/listen.go on 2026-07-26:

- `func (app *App) Listen(addr string, config ...ListenConfig) error`
- `func (app *App) Shutdown() error`
- `func (app *App) ShutdownWithTimeout(timeout time.Duration) error`
- `func (app *App) ShutdownWithContext(ctx context.Context) error`

`ListenConfig` fields that matter for a production service, with their documented defaults:

| Field | Default | Use |
| --- | --- | --- |
| `GracefulContext` | `nil` | A `context.Context` whose cancellation begins graceful shutdown. Wire it to `SIGINT` and `SIGTERM`. |
| `ShutdownTimeout` | `10 * time.Second` | Budget for draining in-flight requests. `0` disables the timeout and waits forever. |
| `DisableStartupMessage` | `false` | Set `true`; the ASCII banner is noise in structured logs. |
| `EnablePrefork` | `false` | Leave `false`. Prefork forks multiple processes on one port and breaks in-process metric registries, connection pools and readiness state. |
| `ListenerNetwork` | `NetworkTCP4` | Set explicitly if the deployment needs IPv6 or a Unix socket. |

Shutdown order, matching the kit's four ordered phases (`stop_intake`, `drain_workers`,
`flush_buffers`, `close_pools`) on a 30s total budget:

1. Flip readiness to not-ready and let the load balancer drain the pod, before the listener stops.
2. Cancel `GracefulContext` so Fiber stops accepting connections and drains in flight within
   `ShutdownTimeout`.
3. Cancel background workers and wait for them.
4. Flush buffered writes, spans and metrics.
5. Close database pools, cache clients, queue connections and exporters.
6. Log the shutdown result once, with the phase that consumed the budget if any did.

Step 1 precedes step 2. A service that stops the listener first returns connection errors to
traffic the load balancer has not yet stopped sending.
