# `lua-load` versus `lua-load-per-thread`

The configuration manual states the difference precisely, and it is the single decision that determines whether your module is correct under load.

`lua-load` "loads and executes a Lua file in the shared context that is visible to all threads. Any variable set in such a context is visible from any thread. This is the easiest and recommended way to load Lua programs but it will not scale well if a lot of Lua calls are performed, as only one thread may be running on the global state at a time. A program loaded this way will always see 0 in the `core.thread` variable."

`lua-load-per-thread` "loads and executes a Lua file into each started thread. Any global variable has a thread-local visibility so that each thread could see a different value. As such it is strongly recommended not to use global variables in programs loaded this way. An independent copy is loaded and initialized for each thread, everything is done sequentially and in the thread's numeric order from 1 to nbthread. If some operations need to be performed only once, the program should check the `core.thread` variable to figure what thread is being initialized. Programs loaded this way will run concurrently on all threads and will be highly scalable. This is the recommended way to load simple functions that register sample-fetches, converters, actions or services once it is certain the program doesn't depend on global variables."

Decide with one question: **does any state have to be shared between threads?**

- No shared state — the module registers pure converters, fetches, or actions, and any table it holds is read-only after load: use `lua-load-per-thread`. Each thread gets its own copy and avoids serialization on the shared Lua state; measure throughput and memory.
- Shared mutable state is required — a counter, a cache, a queue read by one task and written by handlers: use `lua-load`, and accept that only one thread executes Lua at a time.

Three consequences that change how you write code:

1. **Module-level state is per process or per thread, never per request.** A local declared in the file body is initialised once for the whole lifetime of that Lua state. Putting request data there leaks it between requests. Per-request state belongs in `TXN.set_priv` / `TXN.get_priv` or in a HAProxy variable.
2. **Seeding runs once per Lua state, not once per process.** Under `lua-load-per-thread` the file body runs `nbthread` times, sequentially, inside the same second. Anything derived from a coarse clock at load time is therefore near-identical across threads. See `references/40-time-randomness-identity.md`.
3. **Memory multiplies by `nbthread` under per-thread loading.** A 40 MB precomputed table is 40 MB times the thread count. `tune.lua.maxmem` sets a per-process ceiling in megabytes and defaults to zero, meaning unlimited; the manual's stated reason for setting one is that "a bug in a script will not result in the system running out of memory".

## The global Lua lock

The manual names it directly in `tune.lua.forced-yield`: the default yield interval is "10000 instructions for scripts loaded using `lua-load-per-thread` and MAX(500, 10000 / nbthread) instructions for scripts loaded using `lua-load` (it was found to be an optimal value for performance while taking care of not creating thread contention with multiple threads competing for the global lua lock)."

Choose the load model from state ownership and measured contention. Changing it also
changes task multiplicity, initialization, memory and cache consistency; do not
mechanically migrate existing shared modules. A yielding shared-state callback can
interleave with another callback, so the global Lua lock is not an application
transaction spanning a yield.

## Where to do work that must happen once

Read files, parse configuration, and build lookup tables in the **body** or in **init**, where blocking calls are permitted and no traffic is being served, then hold the result in an upvalue. Under `lua-load-per-thread`, guard genuinely once-per-process work with `core.thread == 1`, which the manual names as the way to tell which thread is being initialised.

Changing any `tune.lua.*` value, `nbthread`, or a `lua-load` line is a configuration change: apply `/alaa-haproxy` for the directive and validation rules.

For scope and related decisions, return to the [parent reference](../10-execution-model.md).
