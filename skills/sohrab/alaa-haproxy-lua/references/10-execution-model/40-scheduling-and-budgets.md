# Yielding, blocking, and timeouts

Lua that does not yield holds the thread. HAProxy forces a yield every `tune.lua.forced-yield` instructions in the contexts that can yield, and enforces timeouts everywhere.

**Yieldable handlers** are tasks, actions, services, and applets. Check the documented context of each API: being yieldable does not authorize every API. The `Socket` class multiplexes supported operations through the scheduler.

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

Every default in that table is a pinned value read from one branch of the manual, so re-derive it for the branch you deploy before quoting a number:

```
haproxy -v | head -1
curl -fsS https://raw.githubusercontent.com/haproxy/haproxy/refs/tags/v3.4.6/doc/configuration.txt \
  | grep -n -A6 'tune.lua.burst-timeout'
```

Replace `v3.4.6` with the tag matching the branch the first command reported. `references/SOURCES.md` records which tag each value above was read from and gives the same re-derivation for every other pin in this skill.

Sleeping time is not counted against `burst-timeout`, `session-timeout`, or `service-timeout`; only pure Lua runtime is. Garbage-collection cycles *are* counted against `burst-timeout`, which the manual flags as a source of false positives on saturated systems.

**Bounded computation may run without yielding.** Ordinary function calls, string
validation and arithmetic are not prohibited merely because they complete
synchronously. Converters and fetches require this short, non-yielding shape.
Blocking filesystem/process operations and unbounded C-library calls can stall the
thread; HAProxy cannot make an arbitrary library scheduler-aware. The upstream Lua
architecture lists runtime-prohibited operations (`io`, file I/O, process execution,
filesystem mutation, package loading and stdout printing). Treat this as an API usage
restriction, not proof that every call is intercepted: library availability and
fork/thread protections are separate mechanisms. Load dependencies before traffic;
use `core.log` for runtime logging and supported HAProxy sockets for asynchronous I/O.

A burst timeout bounds Lua execution windows, not the total subrequest wall time.
Configure operation timeouts and an overall deadline separately. Diagnose slow code,
GC pressure and scheduler contention before changing timeout or forced-yield values;
the manual permits measured tuning, not a universal setting or guaranteed preemption
of a blocked native call.

For scope and related decisions, return to the [parent reference](../10-execution-model.md).
