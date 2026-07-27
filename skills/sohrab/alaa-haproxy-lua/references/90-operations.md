# Operations

What happens to Lua when the process changes shape, and how to see a Lua module once it is running.

## Reload and hot restart

A reload starts a new HAProxy process that parses the configuration and loads every Lua file from scratch. Three consequences follow, and each has been the cause of a production surprise.

**Lua state does not survive a reload.** Every module-level table, cache, counter, and seed is rebuilt in the new process. A counter kept in a Lua local resets to zero on every reload; if the value must survive, it belongs in a stick table, not in Lua. Persistence of HAProxy's own stats across reloads is a configuration feature owned by `/alaa-haproxy` (`$alaa-haproxy`).

**Load-time work is paid again on every reload.** A module that reads a large file or builds a large table in the body adds that cost to every reload, multiplied by `nbthread` under `lua-load-per-thread`. A reload that takes seconds is a reload operators avoid running.

**A Lua error at load time aborts the new process.** The old process keeps serving, so the symptom is "the reload did nothing" rather than an outage. Run `haproxy -c -f <config>` before every reload; it exercises the same load path and exits non-zero on a Lua syntax error, a missing file, or an error raised in the file body.

## In-flight work during a reload

The old process finishes its established connections while the new one accepts new ones, so both are running Lua at once, from potentially different versions of the file.

- **A `core.register_task` task in the old process keeps running until that process exits.** A task that writes to an external system therefore has two writers during the overlap. Make task work idempotent, or key it by something that makes a duplicate harmless.
- **A task with no `tune.lua.task-timeout` runs unbounded**; the manual notes the default is unset "because a task may remain alive during of the lifetime of HAProxy". A task that never returns keeps the old process alive and holds its memory and file descriptors.
- **An in-flight request in the old process completes against the old module.** Never assume a deploy makes the previous behaviour unreachable at the instant of reload; a validation change is live only once the old process has drained.

## Observing a Lua module in production

There is no Lua-specific runtime introspection, so observability has to be built into the module and the configuration.

- **`core.log(level, msg)`** is the module's only direct channel to the operator. Where the line goes depends on configuration the module cannot see: `tune.lua.log.loggers` (default `on`) routes it to the proxy's loggers, and `tune.lua.log.stderr` (default `auto`) additionally routes it to stderr when no logger applies. Confirm at least one of the two is in effect before relying on a log line as evidence.
- **A HAProxy variable is the cheapest signal.** Write the handler's outcome to a variable with `TXN.set_var(txn, name, value, true)` and include it in the log format; the value then appears on every request line with no extra Lua cost.
- **A Lua runtime error appears at ALERT**, naming the handler and the state id: `Lua converter 'token_guard': [state-id 2] runtime error: …`. The `state-id` is the Lua state, which under `lua-load-per-thread` identifies the thread. Alert on the appearance of that string, because a converter erroring in production means requests are being rejected or samples are failing.
- **A `tune.lua.*` timeout abort is a design signal, not a tuning signal.** Treat it as a defect report against the handler.

Which of these are *required* for a given change, and at what level, is owned by `/alaa-observability-soc` (`$alaa-observability-soc`). The names of log fields, events, and metrics are owned by `/alaa-services-contract` (`$alaa-services-contract`). This file states only what HAProxy Lua makes available.

## Deploying a module

1. Run `python3 scripts/check_haproxy_lua.py <module.lua>` and require exit 0.
2. Run the module's unit test under the interpreter `haproxy -vv` reported, and require exit 0.
3. Run `haproxy -c -f <config>` on the target host with the module in its deployed path, and require exit 0. Validating against a copy in a different directory does not test the `lua-load` path the deployed configuration names.
4. Reload, then confirm the new process is the one serving before declaring the change live.

Steps 3 and 4 are the general HAProxy deployment discipline established by `/alaa-haproxy` (`$alaa-haproxy`); follow that skill for the reload mechanics, the drain bounds, and the rollout gates. This file adds only that the Lua module must be present at its configured path when step 3 runs, because `haproxy -c -f` reads and compiles it.

## Rollback

A Lua change rolls back by restoring the previous file and reloading, which means the previous file must still exist on the host. Deploy the module as a versioned artifact next to the configuration that names it, so that a rollback of the configuration and a rollback of the module are one action rather than two that can be applied out of order.
