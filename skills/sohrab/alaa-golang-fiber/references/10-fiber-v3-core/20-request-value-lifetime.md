The official Fiber API baseline for this slice was verified on **2026-07-26**; claim-specific source URLs and later refresh dates are in [SOURCES.md](../SOURCES.md).

## Context value lifetime: the one memory-corruption hazard

Fiber reuses request buffers. The docs state, for `Params`, `Query`, `Get`, `Body`, `Cookies` and
their siblings: "The returned value is valid only within the handler. Do not store references."
(https://docs.gofiber.io/api/ctx, verified 2026-07-26.)

`SKILL.md` states the constraint. This is its scope: a value outlives the handler when it is stored
in a struct, sent to a goroutine, put in a cache, logged after the handler returns, passed to a
worker or a queue, or captured by a closure that outlives the handler. Each of those is readable off
the code, so the rule needs no judgement call.

The copy functions are named. Use them:

- `utils.CopyString(s string) string` for strings.
- `utils.CopyBytes(b []byte) []byte` for byte slices.

Both are documented at https://docs.gofiber.io/api/ctx (verified 2026-07-26).

```go
func (h *NewsHandler) Publish(c fiber.Ctx) error {
	// Retained past the handler, so it is copied at the point of extraction.
	newsID := utils.CopyString(c.Params("id"))

	go h.warmCache(newsID) // safe: newsID owns its own backing array

	return c.SendStatus(fiber.StatusAccepted)
}
```

There is no agent-granted exception to this rule. If a value never leaves the handler frame, no
copy is needed, and that is a property you can read off the code rather than a judgement call:
if the value is only read and returned within the same function body, it does not outlive the
handler.
