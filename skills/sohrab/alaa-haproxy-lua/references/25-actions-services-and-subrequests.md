# Actions, Services, and Subrequests

Read this file when the module registers `core.register_action` or `core.register_service`, or when a handler opens a socket. These are the handler types that run on live traffic in this fleet's gateway; converters and sample fetches are a different contract and live in `references/30-failure-visibility.md`.

## The one fact that separates these handlers from converters

**HAProxy reads the return value of a converter and of a sample fetch. It reads nothing back from an action or a service.**

`doc/lua-api/index.rst` gives the action prototype as receiving a `TXN` and returning nothing, and the service prototype as receiving an `AppletHTTP` or `AppletTCP` and returning nothing. Three consequences, each of which changes what you write:

1. **An action cannot fail a sample, because it produces none.** `return` and `return nil` inside an action body are both the same no-op. The `error(message, 0)` rule in `references/30-failure-visibility.md` is a converter and sample-fetch rule; inside an action, calling `error` aborts the handler and HAProxy logs it, but it does not by itself reject the request.
2. **The only output of an action is what it writes.** An action communicates through `TXN.set_var`, `TXN.http:req_set_header`, `TXN.set_priv`, and `TXN.log`. A configuration rule then reads that variable and decides. Nothing else the handler does is visible.
3. **Therefore every action needs a named failure variable and a configuration rule that acts on it.** Decide the variable name and its values before writing the handler body, and write the rejecting rule in the same change. An action whose failure path sets no variable fails open silently, which is the defect this file exists to prevent.

The observable test that an action is wired correctly: kill the dependency the action needs, send one request, and read the response status. If it is the backend's status rather than the gateway's rejection status, the action fails open.

## The failure variable pattern

Set exactly one variable that carries the decision, plus at most one that carries a reason code:

```lua
-- inside core.register_action("authz_enforce", { "http-req" }, function(txn) ... end)
local decision, reason = evaluate(txn)
if decision == nil then
    txn:set_var("txn.authz_status", 503)
    txn:set_var("txn.authz_reason", reason)   -- a code, never a raw error string
    return
end
```

```
http-request lua.authz_enforce if authz_required
http-request deny deny_status 503 if { var(txn.authz_status) -m int 503 }
```

The reason code is a contract name. `/alaa-services-contract` (`$alaa-services-contract`) owns every such name and its wire spelling; do not invent one in Lua. Whether the unreachable-dependency case denies or admits is a fail-closed judgement owned by `/alaa-security-review` (`$alaa-security-review`), and the status code and its retry semantics come from `/alaa-services-contract` (`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md`.

## Subrequests over the Socket class

`core.tcp()` returns a `Socket`. Actions, services, tasks, and applets may use it; converters and sample fetches may not, because they are unyieldable. This is the distinction rule 6 of `SKILL.md` states: the Socket class is scheduler-multiplexed and does not stall the thread, while `io.*`, `os.execute`, and `print` do.

A subrequest is a dependency on the request path. Six obligations, all observable:

1. **Set a connect timeout and a read timeout, separately, and set the read timeout after the connect succeeds.** `Socket.settimeout` applies to the next operation, not to the whole exchange, so one call before `connect` does not bound the read.
2. **Close the socket on every path out of the function, including every early return.** A handler that returns from a failure branch without `socket:close()` leaks a file descriptor per failing request, which becomes an outage under exactly the dependency failure the branch exists to handle.
3. **Validate every byte you concatenate into a request line for carriage return and line feed before concatenating it.** The Socket writes the bytes you give it and frames nothing. A value carrying `\r\n` splits your one subrequest into two, and the second one is attacker-shaped. Reject the value; do not strip. A `trim` that removes leading and trailing whitespace does not satisfy this, because an embedded `\r\n` survives it.
4. **Parse the response defensively and bound it.** Match the status line against an anchored pattern, cap the number of header lines you will read, and cap the bytes you will accept. An unbounded `while true do socket:receive("*l")` loop against a hostile or broken peer is a memory and latency defect.
5. **Shape-check any value from the response before promoting it into something a client or a backend sees.** A decision code that becomes an error body must match an anchored character-class pattern with a maximum length before it leaves the handler. `references/80-security.md` states the general trust rule; whether the peer is inside or outside the trust boundary is owned by `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).
6. **Decide the failure behaviour before writing the call, and make it explicit.** Fail closed for an authorization decision. The mechanism choice — timeout budget, whether to retry, whether to degrade — is shaped by `/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/10-deadlines-and-timeouts.md` and `references/20-retries.md`, and the Ala values themselves come from `/alaa-services-contract` (`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md`. This skill states no timeout number.

A worked instance of obligations 1, 2, and 4 done correctly, and of obligation 3 left open, is this fleet's own gateway module at `<repo>/haproxy/lua/authz-sidecar.lua`: its subrequest helper closes the socket on all seven exit paths and anchors its status-line match, and it concatenates verified-JWT claim values into request lines with only a whitespace `trim` between them and the wire.

## Cost, because these handlers run on every request

An action wired with a bare `http-request lua.name` and no `if` condition runs once per request, so its cost is multiplied by the full request rate of the frontend. Before adding work inside such a handler, state the bound of that work as its input grows and check it against the request rate: `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) `references/10-complexity-budget.md` owns how to state that bound and `references/40-call-in-a-loop.md` owns the per-item-call family this handler type attracts. A per-request handler that iterates a list whose length grows with configuration, tenants, or header count has a budget and must state it.

Under `lua-load` the multiplication is worse than the request rate suggests, because the handler holds the global Lua lock while it runs and every other thread that needs Lua waits behind it. `references/10-execution-model.md` states that trade and the decision between `lua-load` and `lua-load-per-thread`.

## Services and applets

`core.register_service(name, mode, handler)` registers a service invoked from the configuration with `http-request use-service lua.name`. The service terminates the transaction: it writes the response itself and no backend is selected. Three obligations specific to services:

- **A service that fans out to several targets sequentially has a worst case of targets multiplied by per-target timeout.** State that product against `tune.lua.service-timeout`, whose default is 4 s, before adding a target.
- **Gate a diagnostic service at the configuration, not in Lua.** Source-address and path conditions belong in the configuration rule so that `haproxy -c -f` and configuration review can see them; `/alaa-haproxy` (`$alaa-haproxy`) owns how that condition is expressed.
- **A service disabled by a configuration value is still loaded.** `lua-load` runs the file body regardless of whether any rule calls the handler, so its load-time cost, its registrations, and its defects are present in every process even when the feature flag is off. Deleting the `lua-load` line is what removes it.
