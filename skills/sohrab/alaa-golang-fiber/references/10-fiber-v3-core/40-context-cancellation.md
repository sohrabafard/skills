The official Fiber API baseline for this slice was verified on **2026-07-26**; claim-specific source URLs and later refresh dates are in [SOURCES.md](../SOURCES.md).

### `fiber.Ctx` is a `context.Context` whose cancellation does nothing

In v3, `fiber.Ctx` implements `context.Context`. It is not a usable cancellation source: "Due to
current limitations in how fasthttp works, `Deadline()`, `Done()` and `Err()` are no-ops."
(https://docs.gofiber.io/api/ctx, verified 2026-07-26.)

The consequence is load-bearing on a platform that requires every outbound call to be bounded:
**passing `c` itself as the `context.Context` for a database query, a Redis command, or an HTTP call
gives that call no deadline and no cancellation on client disconnect.** Derive a real one:

```go
func (h *NewsHandler) Get(c fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(c.Context(), h.readTimeout)
	defer cancel()

	item, err := h.app.GetNews(ctx, utils.CopyString(c.Params("id")))
	if err != nil {
		return err
	}
	return c.JSON(item)
}
```

`c.Context()` returns "a `context.Context` that can be used outside the handler"; `c.RequestCtx()`
returns the `*fasthttp.RequestCtx`
(https://docs.gofiber.io/whats_new, verified 2026-07-26). Deadlines you attach with
`context.WithTimeout` work normally; what does not work is relying on Fiber to cancel for you.

Never pass `fiber.Ctx` into `internal/domain`, `internal/application`, a repository, a worker or a
background job. Those take `context.Context` and plain Go types.
