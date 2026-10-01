# Actions, Services, and Subrequests

Read this file when the module registers `core.register_action` or `core.register_service`, or when a handler opens a socket. Converters and sample fetches are a different contract and live in `references/30-failure-visibility.md`.

## Handler output contracts

Converters and fetches produce samples. Actions consume a TXN and can return `act.*`
control codes: `act.CONTINUE` is the default, `act.DENY` rejects, `act.ERROR` reports
an internal error, and `act.STOP` stops the current ruleset (it is not a deny).
`act.YIELD` re-executes the action on resumption, so repeated side effects require
care. `TXN.done` is another response-termination path. These APIs require their
own context and protocol tests; do not return arbitrary application integers as
if HAProxy ignored them. Source: v3.4.6 `hlua_action` and API `Act` class.

An uncaught Lua action error logs and normally continues rule processing. Therefore
an access-controlling action still needs a preinitialized deny decision and a
configuration guard for unexpected errors/timeouts, even if normal rejection uses
`act.DENY`. A service/applet writes its own response instead of returning a sample.
For advisory work, use the owner-approved degradation policy rather than demanding
that every action deny traffic.

## The failure variable pattern

Initialize the decision in configuration before calling Lua; publish success only
after the complete result has passed validation. This also denies on unexpected
exceptions, timeouts and early returns, not just anticipated dependency errors.

```haproxy
# Harness-local name/status; fleet wire values remain with their owner.
http-request set-var(txn.guard_ok) bool(false)
http-request lua.guard
http-request deny deny_status 403 unless { var(txn.guard_ok) -m bool }
```

```lua
-- Last operation on successful validation only:
txn:set_var("txn.guard_ok", true, true)
```

An advisory action may have a documented degradation policy instead. A service
writes its own response; a later action-style deny rule cannot repair a partially
sent response. Decide status/body before sending headers and test partial failures.

The reason code is a contract name. `/alaa-services-contract` owns every such name and its wire spelling; do not invent one in Lua. Whether the unreachable-dependency case denies or admits is a fail-closed judgement owned by `/alaa-security-review`, and the status code and its retry semantics come from `/alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`.

## Subrequests over the Socket class

`core.tcp()` returns a `Socket`. Actions, services, tasks, and applets may use it; converters and sample fetches may not, because they are unyieldable. The relevant distinction is: the Socket class is scheduler-multiplexed and does not stall the thread, while `io.*`, `os.execute`, and `print` do.

A subrequest is a dependency on the request path. Six obligations, all observable:

1. **Set a connect timeout and a read timeout, separately, and set the read timeout after the connect succeeds.** `Socket.settimeout` sets operation timeouts, not an overall exchange deadline. Repeated reads can exceed a single-operation budget; enforce aggregate elapsed time and byte limits.
2. **Close the socket on every path out of the function, including every early return.** A handler that returns from a failure branch without `socket:close()` leaks a file descriptor per failing request, which becomes an outage under exactly the dependency failure the branch exists to handle.
3. **Validate every byte you concatenate into a request line for carriage return and line feed before concatenating it.** The Socket writes the bytes you give it and frames nothing. A value carrying `\r\n` splits your one subrequest into two, and the second one is attacker-shaped. Reject the value; do not strip. A `trim` that removes leading and trailing whitespace does not satisfy this, because an embedded `\r\n` survives it.
4. **Parse the response defensively and bound it.** Match the status line against an anchored pattern, cap the number of header lines you will read, and cap the bytes you will accept. An unbounded `while true do socket:receive("*l")` loop against a hostile or broken peer is a memory and latency defect.
5. **Shape-check any value from the response before promoting it into something a client or a backend sees.** A decision code that becomes an error body must match an anchored character-class pattern with a maximum length before it leaves the handler. `references/80-security.md` states the general trust rule; whether the peer is inside or outside the trust boundary is owned by `/alaa-trust-gateway-auth`.
6. **Decide the failure behaviour before writing the call, and make it explicit.** Fail closed for an authorization decision. The mechanism choice — timeout budget, whether to retry, whether to degrade — is shaped by `/alaa-reliability-sla` `references/10-deadlines-and-timeouts.md` and `references/20-retries.md`, and the Ala values themselves come from `/alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`. This skill states no timeout number.

Use fixed destinations and validated request components; test malformed responses, refusal, delayed reads and early close against an isolated peer when a subrequest is introduced. The bundled sample/action probes do not prove subrequest behavior.

## Cost, because these handlers run on every request

An action wired with a bare `http-request lua.name` and no `if` condition runs once per request, so its cost is multiplied by the full request rate of the frontend. Before adding work inside such a handler, state the bound of that work as its input grows and check it against the request rate: `/alaa-algorithms-data-structures` `references/10-complexity-budget.md` owns how to state that bound and `references/40-call-in-a-loop.md` owns the per-item-call family this handler type attracts. A per-request handler that iterates a list whose length grows with configuration, tenants, or header count has a budget and must state it.

Under `lua-load` the multiplication is worse than the request rate suggests, because the handler holds the global Lua lock while it runs and every other thread that needs Lua waits behind it. `references/10-execution-model.md` states that trade and the decision between `lua-load` and `lua-load-per-thread`.

## Services and applets

`core.register_service(name, mode, handler)` registers a service invoked from the configuration with `http-request use-service lua.name`. The service terminates the transaction: it writes the response itself and no backend is selected. Three obligations specific to services:

- **Bound sequential fanout by an overall wall-time deadline.** Sum the per-target exchange budgets, including retries and backoff, before adding a target; enforce the remaining deadline across operations. An inactivity timeout alone does not bound an exchange. Separately bound Lua execution with `tune.lua.service-timeout`: it counts pure Lua runtime and excludes sleep, so it is not the network deadline (v3.4.6 `doc/configuration.txt`, lines 4949-4953).
- **Gate a diagnostic service at the configuration, not in Lua.** Source-address and path conditions belong in the configuration rule so that `haproxy -c -f` and configuration review can see them; `/alaa-haproxy` owns how that condition is expressed.
- **A service disabled by a configuration value is still loaded.** `lua-load` runs the file body regardless of whether any rule calls the handler, so its load-time cost, its registrations, and its defects are present in every process even when the feature flag is off. Deleting the `lua-load` line is what removes it.
