# Security

Lua runs inside the HAProxy process, with HAProxy's privileges, on the first hop that touches untrusted bytes. Everything a client sends can reach a Lua function, and anything that function writes is trusted by everything behind it.

Security **review triggers, threat classes, and the fail-closed doctrine** are owned by `/alaa-security-review` (`$alaa-security-review`); apply that skill to decide whether a change needs review and what "fail closed" requires. **Header names, field names, wire formats, and error codes** are owned by `/alaa-services-contract` (`$alaa-services-contract`); this file names none. **Whether a header arriving at the gateway may be trusted at all** is owned by `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). This file states only what is specific to Lua inside HAProxy.

## The trust rule

**Every value that reached your handler from the network is untrusted, including the ones that look structural.** Headers, the path, the query string, cookies, the body, the TLS SNI value, and the PROXY protocol fields are all client-controlled unless a preceding rule proved otherwise. A value that a previous hop set is trusted only to the extent that the hop was authenticated and the header could not be spoofed past it, which is the question `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) answers.

**Validate before use, and state the positive replacement for every rejection.** A validation with no defined outcome is not a validation. For each field, decide and write down three things before the code: the accepted shape, what happens on rejection, and what the request looks like afterwards.

| Rejection outcome | When it applies | Mechanism |
|---|---|---|
| deny the request | the value gates access or identifies a caller | `error(message, 0)` in Lua, `deny unless { var(…) -m found }` in the configuration |
| strip the value and continue | the value is advisory and the backend behaves correctly without it | do not set the variable, and delete any inbound copy of the field |
| substitute a defined sentinel | a downstream consumer needs to distinguish absent from invalid | return a string the contract defines; never `nil`, never the empty string |

`nil` is not one of the options, for the reason in `references/30-failure-visibility.md`: it becomes a boolean-false sample that sets the variable and renders as `0`.

## Injection through what Lua writes

A Lua handler's return value flows into `set-header`, `set-var`, `set-path`, `set-query`, `set-uri`, log formats, and map keys. Each is a place where a byte you did not reject becomes structure someone else parses.

- **CR and LF are header structure.** A value containing `\r` or `\n` written into a header is header injection into everything behind the proxy. Reject both bytes explicitly rather than assuming HAProxy filters them.
- **NUL truncates in C consumers.** A value containing `\0` can be one string in Lua and a shorter one in a downstream C library. Reject it.
- **Separators are path and query structure.** `/`, `?`, `#`, `&`, `=`, and `;` change meaning when written into `set-path` or `set-query`. Reject or encode; do not pass through.
- **The log line is a parsed format too.** A value written into a log field with quotes, newlines, or the field delimiter breaks the parser downstream and can forge a log record.

**Prefer an allowlist of permitted bytes over a denylist of forbidden ones**, because a denylist is only as complete as the author's imagination and a new consumer can add structure the denylist never covered. The example module allowlists `0-9` and `a-z` and rejects every other byte, including the ones above.

**Bound the length before the loop, always.** Reject anything longer than the maximum you accept before doing per-byte work, so an attacker cannot choose your handler's cost by choosing their input size. This is the same rule as the performance one, and both reasons hold at once.

## Secrets

**Never place a secret in a Lua global, a module-level local, or any message passed to `error` or `core.log`.**

- Under `lua-load` a module-level value is visible to every other Lua file loaded into the same shared state, including files added later by someone else.
- Lua error messages reach the operator log at ALERT, and the traceback HAProxy appends names the file and line even when `error(message, 0)` is used.
- Anything logged is retained by the log pipeline, which is a different trust domain than the proxy.

Read secrets at init time from a source outside the repository, keep them in a single upvalue that is not returned in the module table, and never write them into a HAProxy variable, because variables are readable by every rule in the configuration and by any log format that names them.

## Egress from the edge

`core.tcp()` and `core.httpclient()` let an edge process open outbound connections. That changes the process from a thing that receives traffic into a thing that initiates it, with these consequences:

- **A request-path call adds an unbounded dependency to every request it runs on.** The edge is the layer with the least tolerance for a slow dependency.
- **Server-side request forgery becomes reachable** the moment any part of the destination is derived from client input. Never build a destination address, host, port, or path from a request value; select from a fixed set of destinations that exist in the code.
- **The outbound path must be constrained where it is enforceable**, which is the network policy, not the Lua. Route that to `/alaa-haproxy` (`$alaa-haproxy`) for the configuration side.

Prefer a task context over a request context for anything that must talk to another service: `core.register_task` runs concurrently with traffic and can sleep, so a slow dependency costs a stale cached value instead of a stalled request.

## Resource exhaustion

Lua is inside the proxy's own memory and scheduling budget, so a handler that consumes them is a denial-of-service vector against everything the proxy serves.

- **Never loop over an attacker-controlled length without a bound you enforced.**
- **Never allocate proportionally to an attacker-controlled size** — no `string.rep`, no table built one entry per input byte, no `gsub` over an unbounded subject.
- **Never recurse on attacker-controlled structure.** Lua's stack overflow becomes an error inside the request path, and the error path is also attacker-triggerable.
- **Set `tune.lua.maxmem`.** The manual's stated reason is that a limit ensures "a bug in a script will not result in the system running out of memory". The default is unlimited.
- **Treat each raised error as an attacker-controllable log line.** HAProxy logs a Lua runtime error at ALERT, once per occurrence: verified on HAProxy 2.8.16 on 26 July 2026, two malformed requests produced exactly two ALERT lines. A handler that raises on every malformed request lets a client drive log volume, so keep the message short and constant-shaped and rate-limit the source in the configuration rather than suppressing the error.

## Review checklist for a Lua module at the boundary

Every line must be answerable with evidence, not intent.

1. Which values does this module read from the network, and where is each one's accepted shape written down?
2. What happens on rejection, per call site, and which configuration rule enforces it?
3. Can any output byte be CR, LF, NUL, or a separator meaningful to a consumer of that field?
4. Is every loop and allocation bounded by a limit the module enforces before the loop?
5. Does any error or log message contain a byte that came from the request, or a secret?
6. Does the module open any outbound connection, and is any part of the destination derived from the request?
7. Does the module mutate load-balancer state — server weight, drain, maintenance, map, or ACL contents?

Answer 6 or 7 affirmatively and the change is a trust-boundary change: apply `/alaa-security-review` (`$alaa-security-review`) before it ships.
