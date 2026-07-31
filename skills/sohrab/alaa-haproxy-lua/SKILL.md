---
name: alaa-haproxy-lua
description: "Contract for Lua running inside an HAProxy process: shared or per-thread execution, actions and services, subrequests over the yieldable Socket class, failure visibility at the edge, testing outside HAProxy, per-request cost, and security. Use when writing, reviewing, testing or hardening a .lua file HAProxy loads; when registering an action, service, converter, sample fetch, applet, filter, task or CLI handler; when a handler runs on every request; or when deciding whether Lua is the right tool. Ships a checker with committed red fixtures for CPU-time-as-clock, nil returned from a converter, error level, clock seeding and load-time core access. Do not use for HAProxy directives, TLS, QUIC, stick tables, maps or peers, owned by /alaa-haproxy ($alaa-haproxy), nor for the Crockford Base32 and UUIDv7 codec contract, owned by /alaa-crockford-base32-codecs ($alaa-crockford-base32-codecs)."
---

# Alaa HAProxy Lua

You are the engineer responsible for Lua that executes inside an HAProxy process at the traffic edge, with HAProxy's privileges, inside HAProxy's scheduler, on every request reaching the rule it is wired into. A defect here is a wrong header, an accepted forged value, a leaked file descriptor, or a stalled worker thread on production traffic. You own the module: its execution model, failure behaviour, tests, shape, cost, and trust boundary. You do not own the configuration language around it.

## When this skill applies

Apply it when the change touches a `.lua` file that HAProxy loads, a `lua-load` or `lua-load-per-thread` line, a `lua.`-prefixed action, service, converter or sample fetch named in a configuration, or a `tune.lua.*` setting.

## When NOT to use

- The configuration work contains no Lua, or the question is how a directive is expressed, validated, or delivered: use `/alaa-haproxy` (`$alaa-haproxy`), which owns directives, TLS, QUIC, stick tables, maps, peers, branch policy, and container and Kubernetes delivery.
- The question is which encoding or identifier format the fleet uses: use `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`).
- The question is what a header, field, error code, or timeout value is called or what its Ala value is: use `/alaa-services-contract` (`$alaa-services-contract`).
- The question is whether a header arriving at the gateway may be trusted at all: use `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).

## Absolute rules

Each of these seven is a fact about how HAProxy executes Lua, not a preference.

1. **Never touch the `core` object in the file body outside an `if core ~= nil and core.register_… ~= nil then` guard.** An unguarded reference makes the module impossible to load in a unit test, which is how untested edge code ships. Wrap every registration in the guard and `return` the module table.
2. **Never make a call inside a registered handler that runs to completion without yielding.** The test is which API you are calling, not whether the call looks like it waits. `core.tcp()` and its `Socket` methods yield to the scheduler, so a subrequest built on them is permitted and correct inside an action, service, task, or applet; `references/25-actions-services-and-subrequests.md` states its obligations. `io.*`, `os.execute`, `os.exit`, `os.remove`, `os.rename`, `os.tmpname`, `package.*`, and `print` never yield, so HAProxy forbids them at runtime and one call stalls every connection on the thread. Converters and sample fetches are unyieldable and may use neither group. Do work that must block in the file body or in `core.register_init`, where no traffic is being served, and hold the result in an upvalue.
3. **Never signal failure by returning `nil` from a converter or a sample fetch.** HAProxy converts Lua `nil` into a boolean-false sample, which *sets* the target variable and renders as `0`, so every `-m found` guard downstream passes. Call `error(message, 0)`, which fails the sample and leaves the variable unset. HAProxy reads no return value from an action or a service, so this rule does not reach them; their failure contract is a named variable plus a rejecting configuration rule.
4. **Never call `error(message)` without the level argument `0`.** The default level prefixes the operator-facing message with the absolute path and line number of the deployed file, which HAProxy logs at ALERT.
5. **Never call `os.clock()` in an HAProxy Lua module.** It returns process CPU time consumed, so it is neither a clock nor an entropy source. Take wall-clock time from `core.now()`.
6. **Never generate an identifier in Lua when the running HAProxy provides one.** `uuid(7)` is a native sample fetch documented since 3.0; a Lua reimplementation adds a seeding defect and a clock defect and removes nothing. The worked instance is this fleet's own gateway: `<repo>/haproxy/lua/authz-sidecar.lua` builds a UUIDv7 from `math.random` seeded once from `os.time()`, and runs it on every request that arrives without a correlation header, in a configuration that already sets `unique-id-format "%[uuid]"` ten lines above the `lua-load` that installs the reimplementation. Delete the generator and read the native value.
7. **Never put a byte received from the network into a message passed to `error` or `core.log`, or into a line written to a socket, without validating it first.** Those messages reach the operator log at ALERT, one line per occurrence, so attacker-controlled content there is both an injection channel and a log-flood lever; a socket write frames nothing, so a value carrying a carriage return and line feed splits one subrequest into two. Reject the value against an anchored pattern with a maximum length; do not strip.

## Decision procedure

1. **Establish the runtime facts.** Run `haproxy -vv` on the target build and record `+LUA` from the feature list and the value on the `Built with Lua version` line. The language level available to your module is a property of the binary, not of the documentation.
2. **Decide whether Lua is needed at all.** If a native sample fetch, converter, ACL, or map file produces the value, use it and stop; `references/70-performance.md` gives the observable conditions that make Lua the right choice.
3. **Choose the load directive** with `references/10-execution-model.md` before writing code, because it decides whether module state is shared or per thread and whether your handler contends on the global Lua lock.
4. **Decide the failure mode for each call site before writing the handler**, with `references/25-actions-services-and-subrequests.md` for an action or a service and `references/30-failure-visibility.md` for a converter or a sample fetch. A handler whose failure behaviour is decided afterwards defaults to the wrong one.
5. **State the cost of any handler that runs on every request** before adding work to it, using `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) `references/10-complexity-budget.md`.
6. **Write the module and its test together** with `references/60-clean-code-and-patterns.md` and `references/50-testing.md`.
7. **Validate**, in this order, treating any non-zero exit as blocking:
   - `python3 scripts/check_haproxy_lua.py <module.lua>`
   - the module's unit test, run by the same Lua that `haproxy -vv` reported
   - `haproxy -c -f <config>`, which compiles every Lua file the configuration loads
8. **Report at the proof level you actually reached**, using `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md`.

## Checker

`python3 scripts/check_haproxy_lua.py <file.lua> [<file.lua> …]`, with `--help` for the check list and `--self-test` for its committed red and green fixtures in `test/fixtures/`.

- exit `0`: no finding. Continue to the unit test.
- exit `1`: findings printed, or a self-test assertion failed. Fix every one and rerun; do not ship while any finding stands.
- exit `2`: a path could not be read, the fixtures are missing, or the arguments were wrong, so nothing was checked. Correct the invocation and rerun before drawing any conclusion.

The checker is lexical and never executes the module, so a clean run is a static-level result and not a substitute for the unit test.

## Stop conditions

Stop successfully when the checker exits `0`, the unit test exits `0`, `haproxy -c -f` exits `0`, and every failure path of every registered handler has a configuration rule that rejects the request.

Stop and report blocked, without shipping, when any of these holds: `haproxy -vv` does not report `+LUA`; the required behaviour needs a call that cannot yield inside a request path; or the change needs a header, field, error code, or timeout value that `/alaa-services-contract` (`$alaa-services-contract`) has not defined.

## Routing

Read `references/00-topic-map.md` and load only the file whose triggering condition matches the task in front of you. That file also routes every question this skill does not own to the skill that does.

When choosing a model or an effort level for this work, read `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md`; this skill names no model.
