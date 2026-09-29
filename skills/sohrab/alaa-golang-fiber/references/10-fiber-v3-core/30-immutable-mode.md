The official Fiber API baseline for this slice was verified on **2026-07-26**; claim-specific source URLs and later refresh dates are in [SOURCES.md](../SOURCES.md).

### `Immutable` is a boot-time service-wide decision

`fiber.Config.Immutable` defaults to `false`
(https://docs.gofiber.io/api/fiber, verified 2026-07-26). Setting it `true` makes Fiber allocate a
copy of every returned value, which costs allocation and throughput on every request and buys
safety globally.

That trade is made once, by the service owner, at boot, for the whole service, and recorded in the
service's `docs/DECISIONS.md`. It is never invoked at a call site as a reason to skip a copy: a
per-site claim that "Immutable is on" cannot be verified at that site, and it silently breaks if the
service later turns `Immutable` off for throughput.

`App.GetString(s string) string` and `App.GetBytes(b []byte) []byte` are the companions to that
decision, not substitutes for copying. They "return `s` unchanged when `Immutable` is disabled or
`s` resides in read-only memory. Otherwise [they return] a detached copy"
(https://docs.gofiber.io/next/api/app, verified 2026-07-26). Because they are no-ops when
`Immutable` is disabled, using them in a service that has not enabled `Immutable` retains a value
that will be overwritten. Use them only in a service whose `Immutable` decision is recorded as
enabled; use `utils.CopyString` / `utils.CopyBytes` everywhere else.
