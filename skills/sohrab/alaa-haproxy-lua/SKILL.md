---
name: alaa-haproxy-lua
description: "Engineering contract for Lua that runs inside an HAProxy process: execution model, API surface, failure visibility at the edge, testing outside HAProxy, clean code, design patterns, performance, and security. Use when writing, reviewing, testing, debugging, or hardening a .lua file loaded by lua-load or lua-load-per-thread; when registering a converter, sample fetch, action, service, applet, filter, task, or CLI handler; or when deciding whether Lua is the right tool at all. Ships a pre-ship checker for CPU-time-as-clock, nil failure returns, error level, and load-time core access. Do not use for HAProxy configuration directives, TLS, QUIC, stick tables, maps, peers, or container and Kubernetes delivery, which belong to /alaa-haproxy ($alaa-haproxy). Do not use for the shared Crockford Base32 or UUIDv7 codec contract, which belongs to /alaa-crockford-base32-codecs ($alaa-crockford-base32-codecs)."
---

# Alaa HAProxy Lua

You are the engineer responsible for Lua that executes inside an HAProxy process at the traffic edge, with HAProxy's privileges, inside HAProxy's scheduler, on every request reaching the rule it is wired into. A defect here is a wrong header, an accepted forged value, or a stalled worker thread on production traffic. You own the module: its execution model, failure behaviour, tests, shape, cost, and trust boundary. You do not own the configuration language around it.

## When this skill applies

Apply it when the change touches a `.lua` file that HAProxy loads, a `lua-load` or `lua-load-per-thread` line, a `lua.`-prefixed converter or sample fetch in a configuration, or a `tune.lua.*` setting. Apply `/alaa-haproxy` (`$alaa-haproxy`) instead when the configuration work contains no Lua.

## Absolute rules

Each of these seven is a fact about how HAProxy executes Lua, not a preference.

1. **Never call `os.clock()` in an HAProxy Lua module.** It returns process CPU time consumed, so it is neither a clock nor an entropy source. Take wall-clock time from `core.now()`.
2. **Never signal failure by returning `nil` from a converter, sample fetch, or action.** HAProxy converts Lua `nil` into a boolean-false sample, which *sets* the target variable and renders as `0`, so every `-m found` guard downstream passes. Call `error(message, 0)`, which fails the sample and leaves the variable unset.
3. **Never call `error(message)` without the level argument `0`.** The default level prefixes the operator-facing message with the absolute path and line number of the deployed file, which HAProxy logs at ALERT.
4. **Never generate an identifier in Lua when the running HAProxy provides one.** `uuid(7)` is a native sample fetch documented since 3.0; a Lua reimplementation adds a seeding defect and a clock defect and removes nothing.
5. **Never touch the `core` object in the file body outside an `if core ~= nil and core.register_… ~= nil then` guard.** An unguarded reference makes the module impossible to load in a unit test, which is how untested edge code ships.
6. **Never perform blocking I/O, and never call `os.execute`, `os.exit`, `print`, or any `io.*` function, from a registered handler.** HAProxy forbids these at runtime because they stall the scheduler for every connection on the thread. Do that work in the file body or in `core.register_init` and hold the result in an upvalue.
7. **Never put a byte received from the network into a message passed to `error` or `core.log`.** Those messages reach the operator log at ALERT, one line per occurrence, so attacker-controlled content there is both an injection channel and a log-flood lever.

## Decision procedure

1. **Establish the runtime facts.** Run `haproxy -vv` on the target build and record `+LUA` from the feature list and the value on the `Built with Lua version` line. The language level available to your module is a property of the binary, not of the documentation.
2. **Decide whether Lua is needed at all.** If a native sample fetch, converter, ACL, or map file produces the value, use it and stop; `references/70-performance.md` gives the observable conditions that make Lua the right choice.
3. **Choose the load directive** with `references/10-execution-model.md` before writing code, because it decides whether module state is shared or per thread and whether your handler contends on the global Lua lock.
4. **Decide the failure mode for each call site before writing the handler** with `references/30-failure-visibility.md`. A handler whose failure behaviour is decided afterwards defaults to the wrong one.
5. **Write the module and its test together** with `references/60-clean-code-and-patterns.md` and `references/50-testing.md`.
6. **Validate**, in this order, treating any non-zero exit as blocking:
   - `python3 scripts/check_haproxy_lua.py <module.lua>`
   - the module's unit test, run by the same Lua that `haproxy -vv` reported
   - `haproxy -c -f <config>`, which compiles every Lua file the configuration loads
7. **Report at the proof level you actually reached**, using `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md`.

## Checker

`python3 scripts/check_haproxy_lua.py <file.lua> [<file.lua> …]`, with `--help` for the check list and `--self-test` for its own fixtures.

- exit `0`: no finding. Continue to the unit test.
- exit `1`: findings printed. Fix every one and rerun; do not ship while any finding stands.
- exit `2`: unreadable path or wrong arguments, so no file was checked. Correct the invocation and rerun before drawing any conclusion.
- exit `3`: `--self-test` failed, so the checker's verdicts are untrustworthy. Report the failing case and review the module by hand.

The checker is lexical and never executes the module, so a clean run is a static-level result and not a substitute for the unit test.

## Stop conditions

Stop successfully when the checker exits `0`, the unit test exits `0`, `haproxy -c -f` exits `0`, and every failure path of every registered handler has a configuration rule that rejects the request.

Stop and report blocked, without shipping, when any of these holds: `haproxy -vv` does not report `+LUA`; the required behaviour needs a blocking call inside a request path; or the change needs a header, field, or wire-format name that `/alaa-services-contract` (`$alaa-services-contract`) has not defined.

## Routing

Read `references/00-topic-map.md` and load only the file whose triggering condition matches the task in front of you. That file also routes every question this skill does not own to the skill that does.

When choosing a model or an effort level for this work, read `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md`; this skill names no model.
