# Performance

The honest position first: **Lua should be the exception in an HAProxy configuration, not the default extension mechanism.** Native sample fetches, converters, ACLs, and map files are C, they take no Lua lock, they allocate nothing on the Lua heap, and they cannot time out mid-request. Reach for Lua when the native surface genuinely cannot express the behaviour, and treat every Lua call in a request path as a cost you have chosen to pay.

## When Lua is the wrong tool

Use the native mechanism, and delete the Lua, when any of these is observable:

- **A native sample fetch or converter already produces the value.** `uuid([4|7])`, `rand([range])`, `digest`, `hmac`, `base64`, `url_dec`, `regsub`, `field`, `word`, and the header and URI fetches cover most of what edge Lua gets written for. Check the configuration manual for the running branch before writing a handler.
- **The logic is a lookup keyed by a string.** A map file with `map_str`, `map_beg`, `map_dom`, or `map_reg` is a hash lookup in C, is reloadable through the runtime API without restarting, and is auditable by an operator who does not read Lua.
- **The logic is a boolean decision on request attributes.** An ACL expresses it, and an ACL is visible in the configuration where a reviewer will look for it.
- **The logic is arithmetic or counting across requests.** A stick table does it in C with shared state, and peers replicate it across nodes.
- **The work needs an external service.** A Lua `Socket` or `HTTPClient` call in a request path adds an unbounded dependency to every request; an SPOE agent or a backend keeps it out of the Lua state. Route the reliability shape of that dependency to `/alaa-reliability-sla` (`$alaa-reliability-sla`).

Lua is the right tool when the transformation is stateful across several fields of one request, when it needs a real parser, when it produces a response body, or when the alternative is a chain of native converters nobody can read. Directive selection for the native mechanisms is owned by `/alaa-haproxy` (`$alaa-haproxy`).

## What a converter costs

Converters and sample fetches are **unyieldable**. The configuration manual says so directly for `tune.lua.burst-timeout`: for them, hitting the timeout "could simply indicate that the handler is doing too much computation, which could result from an improper design given that such handlers, which often block the request execution flow, are expected to terminate quickly", and lowering `tune.lua.forced-yield` "won't help".

So a converter runs to completion inside the request. Under `lua-load` it holds the global Lua lock for that whole time and every other thread that needs Lua waits. The design rule that follows: **a converter's cost must be bounded by a constant, or by an input length you bounded yourself before the loop.**

## Allocation and the garbage collector

Every Lua string is heap-allocated and immutable, and every table constructor allocates. At a few thousand requests per second, a handler that allocates a handful of objects per request is producing tens of thousands of objects per second for the collector.

`tune.lua.burst-timeout` counts garbage-collection time. The manual is explicit that this "could lead to some false positives on saturated systems (where GC is having hard time to catch up and consumes most of the available execution runtime)" and names reducing the module's memory footprint as the first remedy. A handler that allocates heavily therefore does not merely run slowly; it makes *other* handlers time out.

Rules that remove most per-request allocation:

- **Never build a string with `..` in a loop.** Each concatenation allocates a new string and copies both sides, so a loop over *n* pieces allocates *n* strings and copies quadratically. Collect the pieces into a table and call `table.concat` once, or use `core.concat()` which HAProxy provides for this purpose.
- **Never construct a lookup table per call.** Build it in the file body and close over it.
- **Prefer `string.byte` over `string.sub` for single-character inspection.** `string.sub` allocates a one-character string per call; `string.byte` returns an integer and allocates nothing.
- **Return the input unchanged when it is already correct.** A validator that lower-cases unconditionally allocates on every valid request for no result.
- **Hoist `string.format` patterns and reuse them**, and keep `string.format` out of the success path entirely — it belongs in the error path, which is rare by design.

## What to precompute at load time

Anything that does not depend on the request: alphabets and byte allowlists, parsed load-time arguments, compiled patterns, constant strings, and localised globals. Load time is the one place where cost is paid once and blocking is permitted, so spend it freely there.

Under `lua-load-per-thread`, remember the multiplier: a precomputed table costs its size times `nbthread`, and `tune.lua.maxmem` bounds Lua memory per process.

## Pattern matching on attacker-controlled input

Lua patterns are not regular expressions and have no backtracking engine, so they do not exhibit catastrophic exponential backtracking. They can still be driven quadratic by nested `%s*`-style repetitions over a long subject, and every `gsub` allocates a result string.

The rule that covers both: **bound the length before matching.** Reject anything longer than the maximum you accept, then match. This is a security rule as much as a performance one; `references/80-security.md` states its threat form.

## Measuring rather than guessing

Three observations to take before changing anything, in this order:

1. `haproxy -vv` — confirm `+LUA` and the Lua version, since a claim about Lua performance that does not name the interpreter is not a claim.
2. The stats page or Prometheus exporter under representative load, before and after — request rate and response time, which is where a Lua stall shows up as latency on requests that do not touch Lua at all.
3. `tune.lua.burst-timeout` aborts in the log. One abort is a design fact, not a tuning parameter: it says the handler is doing more work than a request path allows.

Raising a `tune.lua.*` timeout to stop aborts hides the symptom and leaves the stall. Reduce the work, or move it out of Lua.
