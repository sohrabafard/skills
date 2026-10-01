---
name: alaa-haproxy-lua
description: "Contract for Lua running inside an HAProxy process: shared or per-thread execution, actions and services, subrequests over the yieldable Socket class, failure visibility at the edge, testing outside HAProxy, per-request cost, and security. Use when writing, reviewing, testing or hardening a .lua file HAProxy loads; when registering an action, service, converter, sample fetch, applet, filter, task or CLI handler; when a handler runs on every request; or when deciding whether Lua is the right tool. Ships a checker with committed red fixtures for CPU-time-as-clock, unsafe nil returns, error level, clock seeding and load-time core access. Do not use for HAProxy directives, TLS, QUIC, stick tables, maps or peers, owned by /alaa-haproxy, nor for the Crockford Base32 and UUIDv7 codec contract, owned by /alaa-crockford-base32-codecs."
---

# Alaa HAProxy Lua

You are the engineer responsible for Lua that executes inside an HAProxy process at the traffic edge, with HAProxy's privileges, inside HAProxy's scheduler, on every request reaching the rule it is wired into. A defect here is a wrong header, an accepted forged value, a leaked file descriptor, or a stalled worker thread on production traffic. You own the module: its execution model, failure behaviour, tests, shape, cost, and trust boundary. You do not own the configuration language around it.

## When this skill applies

Apply it when the change touches a `.lua` file that HAProxy loads, a `lua-load` or `lua-load-per-thread` line, a `lua.`-prefixed action, service, converter or sample fetch named in a configuration, or a `tune.lua.*` setting.

## When NOT to use

- The configuration work contains no Lua, or the question is how a directive is expressed, validated, or delivered: use `/alaa-haproxy`, which owns directives, TLS, QUIC, stick tables, maps, peers, branch policy, and container and Kubernetes delivery.
- The question is which encoding or identifier format the fleet uses: use `/alaa-crockford-base32-codecs`.
- The question is what a header, field, error code, or timeout value is called or what its Ala value is: use `/alaa-services-contract`.
- The question is whether a header arriving at the gateway may be trusted at all: use `/alaa-trust-gateway-auth`.

## Contract and authority

Upstream restrictions, Lua-language semantics and Alaa engineering requirements are
separate. Their owners are the execution, failure, security and test references in
the topic map. Bounded computation need not yield; blocking I/O requires a supported
scheduler-aware API. A runtime restriction is not proof of a sandbox.

Preserve repository contracts, identifiers and existing module-state decisions.
Do not change a load directive, conversion mode or library allowlist without testing
its consumers. Stay within the task's authorized inspection, editing and validation
scope; installation, deployment, publication and external mutations require
explicit authorization.

## Decision procedure

1. **Establish the runtime facts.** Run `haproxy -vv` on the target build and record `+LUA` from the feature list and the value on the `Built with Lua version` line. The language level available to your module is a property of the binary, not of the documentation.
2. **Decide whether Lua is needed at all.** If a native sample fetch, converter, ACL, or map preserves the required semantics and format, use it; `references/70-performance.md` gives the observable conditions that make Lua the right choice.
3. **Review libraries and loading.** Derive the dependency allowlist with `references/15-standard-libraries.md`. **Choose the load directive** with `references/10-execution-model.md` before writing code, because it decides whether module state is shared or per thread and whether your handler contends on the global Lua lock.
4. **Decide the failure mode for each call site before writing the handler**, with `references/25-actions-services-and-subrequests.md` for an action or a service and `references/30-failure-visibility.md` for a converter or a sample fetch. A handler whose failure behaviour is decided afterwards defaults to the wrong one.
5. **State the cost of any handler that runs on every request** before adding work to it, using `/alaa-algorithms-data-structures` `references/10-complexity-budget.md`.
6. **Write the module and its test together** with `references/60-clean-code-and-patterns.md` and `references/50-testing.md`.
7. **Validate**, in this order, treating any non-zero exit as blocking:
   - `python3 scripts/check_haproxy_lua.py <module.lua>`
   - the module's unit test, run by the same Lua that `haproxy -vv` reported
   - `haproxy -c -f <config>`, which compiles every Lua file the configuration loads
   - focused runtime success/failure probes; the bundled gate is `python3 scripts/check_runtime.py --image <cached-image>` (Docker, no pulls).
8. **Report at the proof level you actually reached**, using `/alaa-testing-strategy` `references/40-proof-strength.md`.

## Checker

`python3 scripts/check_haproxy_lua.py <file.lua> [<file.lua> …]`, with `--help` for the check list and `--self-test` for its committed red and green fixtures in `test/fixtures/`.

- exit `0`: no finding. Continue to the unit test.
- exit `1`: findings printed, or a self-test assertion failed. Fix every one and rerun; do not ship while any finding stands.
- exit `2`: a path could not be read, the fixtures are missing, or the arguments were wrong, so nothing was checked. Correct the invocation and rerun before drawing any conclusion.

The checker is lexical and never executes the module, so a clean run is a static-level result and not a substitute for the unit test.

## Stop conditions

Stop successfully when the checker exits `0`, the unit test exits `0`, `haproxy -c -f` exits `0`, and each security decision denies on absence, error and timeout, and advisory failures follow their documented policy.

Stop and report blocked, without shipping, when any of these holds: `haproxy -vv` does not report `+LUA`; the required behavior needs blocking I/O without a supported scheduler-aware path; or the change needs a header, field, error code, or timeout value that `/alaa-services-contract` has not defined.

## Routing

Read `references/00-topic-map.md` and load only the file whose triggering condition matches the task in front of you. That file also routes every question this skill does not own to the skill that does.

For one failed operation, make at most one cause-specific repair and one materially different retry. Then report the blocker and preserved evidence; unavailable gates are not passes.

Report changed contracts/files, sources, exact static/unit/parser/runtime results and unrun deployment gates.
