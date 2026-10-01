# The eight execution contexts

The Lua API reference enumerates them, and each API call documents which contexts it is legal in. Checking the context before calling is cheaper than discovering it in production.

1. **body** — the file itself, executed at `lua-load` time, in initialisation mode. This is where registrations happen and where blocking file reads are permitted.
2. **init** — a function registered with `core.register_init()`, run after configuration parsing, still in initialisation mode. Use it for checks that need the parsed configuration.
3. **task** — a function registered with `core.register_task()`, running concurrently with traffic after the scheduler starts.
4. **action** — registered with `core.register_action()`, receives a `TXN`, may return an `act.*` control code.
5. **sample-fetch** — registered with `core.register_fetches()`, receives a `TXN` plus up to twelve string arguments, returns a sample-compatible value. Usable in configuration as `lua.<name>`.
6. **converter** — registered with `core.register_converters()`, receives a string plus up to twelve string arguments, returns a sample-compatible value. The reference calls converters "stateless" and says they "cannot access to any context".
7. **filter** — a class of callbacks registered with `core.register_filter()`.
8. **event** — a handler passed to `core.event_sub()` or `Server.event_sub()`.

Initialisation mode and runtime mode differ in what is allowed: in initialisation mode DNS resolution works and socket I/O does not, and HAProxy is blocked while the code runs; in runtime mode DNS resolution is unavailable and sockets work, with execution multiplexed against request processing.

For scope and related decisions, return to the [parent reference](../10-execution-model.md).
