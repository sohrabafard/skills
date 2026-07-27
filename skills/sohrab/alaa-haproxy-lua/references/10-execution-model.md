# Execution Model

Most HAProxy Lua defects are execution-model defects wearing a logic-defect costume. Read this file before writing the first line of a module.

## How Lua is embedded

HAProxy links a Lua interpreter into its own process when built with `USE_LUA=1`. Confirm both facts on the target binary before writing code:

```
haproxy -vv | grep -E '\+LUA|Built with Lua version'
```

The feature list must contain `+LUA` and the `Built with Lua version` line names the exact interpreter your module will run under. A build without `+LUA` rejects `lua-load` at configuration parse time, so this check is what turns a runtime surprise into a pre-work fact.

## Which Lua version

HAProxy's `INSTALL` file, section 4.7, states: "Only versions 5.3 and above are supported", and lists the library names it searches as `lua5.5`, `lua55`, `lua5.4`, `lua54`, `lua5.3`, `lua53`, `lua`. Two consequences follow.

- **LuaJIT is not a supported target.** LuaJIT implements Lua 5.1, below the supported floor, so a module does not need a 5.1 compatibility path for HAProxy. Write for 5.3 and above.
- **Bitwise operators, integer division, `math.tointeger`, and `math.type` are always available** in an HAProxy build, because they arrived in 5.3. They are *not* available when someone unit-tests the module with a stray `lua5.1` binary, which fails with `unexpected symbol near '>'` on the first `>>`. Record the minimum version in a comment at the top of every module so the test environment is chosen deliberately rather than by whichever `lua` is first on `PATH`.

The `Built with Lua version` line is the authority for which interpreter to run tests under. Do not infer it from the distribution's `lua` package.

## `lua-load` versus `lua-load-per-thread`

The configuration manual states the difference precisely, and it is the single decision that determines whether your module is correct under load.

`lua-load` "loads and executes a Lua file in the shared context that is visible to all threads. Any variable set in such a context is visible from any thread. This is the easiest and recommended way to load Lua programs but it will not scale well if a lot of Lua calls are performed, as only one thread may be running on the global state at a time. A program loaded this way will always see 0 in the `core.thread` variable."

`lua-load-per-thread` "loads and executes a Lua file into each started thread. Any global variable has a thread-local visibility so that each thread could see a different value. As such it is strongly recommended not to use global variables in programs loaded this way. An independent copy is loaded and initialized for each thread, everything is done sequentially and in the thread's numeric order from 1 to nbthread. If some operations need to be performed only once, the program should check the `core.thread` variable to figure what thread is being initialized. Programs loaded this way will run concurrently on all threads and will be highly scalable. This is the recommended way to load simple functions that register sample-fetches, converters, actions or services once it is certain the program doesn't depend on global variables."

Decide with one question: **does any state have to be shared between threads?**

- No shared state — the module registers pure converters, fetches, or actions, and any table it holds is read-only after load: use `lua-load-per-thread`. Each thread gets its own copy, no lock is taken, and throughput scales with `nbthread`.
- Shared mutable state is required — a counter, a cache, a queue read by one task and written by handlers: use `lua-load`, and accept that only one thread executes Lua at a time.

Three consequences that change how you write code:

1. **Module-level state is per process or per thread, never per request.** A local declared in the file body is initialised once for the whole lifetime of that Lua state. Putting request data there leaks it between requests. Per-request state belongs in `TXN.set_priv` / `TXN.get_priv` or in a HAProxy variable.
2. **Seeding runs once per Lua state, not once per process.** Under `lua-load-per-thread` the file body runs `nbthread` times, sequentially, inside the same second. Anything derived from a coarse clock at load time is therefore near-identical across threads. See `references/40-time-randomness-identity.md`.
3. **Memory multiplies by `nbthread` under per-thread loading.** A 40 MB precomputed table is 40 MB times the thread count. `tune.lua.maxmem` sets a per-process ceiling in megabytes and defaults to zero, meaning unlimited; the manual's stated reason for setting one is that "a bug in a script will not result in the system running out of memory".

## The global Lua lock

The manual names it directly in `tune.lua.forced-yield`: the default yield interval is "10000 instructions for scripts loaded using `lua-load-per-thread` and MAX(500, 10000 / nbthread) instructions for scripts loaded using `lua-load` (it was found to be an optimal value for performance while taking care of not creating thread contention with multiple threads competing for the global lua lock)."

HAProxy's own performance guidance is blunt about the threshold: above 32 CPUs, `lua-load-per-thread` is required rather than advised, because with `lua-load` "the script is run on a single CPU at a time and because it can share state, must lock, which stalls the other CPUs".

The operational consequence: a slow handler under `lua-load` does not slow only its own request. It holds the global state and every other thread that needs Lua waits behind it.

## The eight execution contexts

The Lua API reference enumerates them, and each API call documents which contexts it is legal in. Checking the context before calling is cheaper than discovering it in production.

1. **body** — the file itself, executed at `lua-load` time, in initialisation mode. This is where registrations happen and where blocking file reads are permitted.
2. **init** — a function registered with `core.register_init()`, run after configuration parsing, still in initialisation mode. Use it for checks that need the parsed configuration.
3. **task** — a function registered with `core.register_task()`, running concurrently with traffic after the scheduler starts.
4. **action** — registered with `core.register_action()`, receives a `TXN`, returns nothing.
5. **sample-fetch** — registered with `core.register_fetches()`, receives a `TXN` plus up to five string arguments, returns a string. Usable in configuration as `lua.<name>`.
6. **converter** — registered with `core.register_converters()`, receives a string plus up to five string arguments, returns a string. The reference calls converters "stateless" and says they "cannot access to any context".
7. **filter** — a class of callbacks registered with `core.register_filter()`.
8. **event** — a handler passed to `core.event_sub()` or `Server.event_sub()`.

Initialisation mode and runtime mode differ in what is allowed: in initialisation mode DNS resolution works and socket I/O does not, and HAProxy is blocked while the code runs; in runtime mode DNS resolution is unavailable and sockets work, with execution multiplexed against request processing.

## Yielding, blocking, and timeouts

Lua that does not yield holds the thread. HAProxy forces a yield every `tune.lua.forced-yield` instructions in the contexts that can yield, and enforces timeouts everywhere.

**Yieldable handlers** are tasks, actions, services, and applets. They may call `core.sleep()`, `core.msleep()`, `core.yield()`, or `core.wait()`, and they may use the `Socket` class, whose blocking-looking calls are multiplexed by the scheduler.

**Unyieldable handlers are converters and sample fetches.** The manual is explicit that for them, reaching `tune.lua.burst-timeout` "could simply indicate that the handler is doing too much computation, which could result from an improper design given that such handlers, which often block the request execution flow, are expected to terminate quickly", and that lowering `tune.lua.forced-yield` will not help. A converter must therefore be short and allocation-light by construction, not by tuning.

The timeouts, with their documented defaults:

| Setting | Applies to | Default |
|---|---|---|
| `tune.lua.burst-timeout` | any handler, per single uninterrupted execution window | 1000 ms |
| `tune.lua.session-timeout` | actions, filters, CLI handlers, cumulative Lua runtime | 4 s |
| `tune.lua.service-timeout` | services | 4 s |
| `tune.lua.task-timeout` | tasks | unset, because a task may live as long as the process |
| `tune.lua.forced-yield` | instructions between forced yields | 10000 per-thread, `MAX(500, 10000 / nbthread)` shared |
| `tune.lua.maxmem` | Lua memory per process, in megabytes | 0, meaning unlimited |

Sleeping time is not counted against `burst-timeout`, `session-timeout`, or `service-timeout`; only pure Lua runtime is. Garbage-collection cycles *are* counted against `burst-timeout`, which the manual flags as a source of false positives on saturated systems.

**Synchronous I/O from Lua stalls every connection on that thread**, and under `lua-load` it stalls every thread that needs Lua. HAProxy forbids the filesystem and process functions at runtime for exactly this reason: `os.remove`, `os.rename`, `os.tmpname`, `package.*`, `io.*`, `file.*`, `os.execute`, and `os.exit`. `print` is also prohibited, because it writes to stdout and can block; use `core.log` or `TXN.log`.

## Where to do work that must happen once

Read files, parse configuration, and build lookup tables in the **body** or in **init**, where blocking calls are permitted and no traffic is being served, then hold the result in an upvalue. Under `lua-load-per-thread`, guard genuinely once-per-process work with `core.thread == 1`, which the manual names as the way to tell which thread is being initialised.

Changing any `tune.lua.*` value, `nbthread`, or a `lua-load` line is a configuration change: apply `/alaa-haproxy` (`$alaa-haproxy`) for the directive and validation rules.
