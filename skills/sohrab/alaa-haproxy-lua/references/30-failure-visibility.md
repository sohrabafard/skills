# Failure Visibility at the Edge

A Lua handler that fails badly does not raise an exception anyone sees. It produces a plausible value, the configuration accepts it, and the request continues to the backend. This file states what each failure shape actually renders and which one you must use.

**Scope: converters and sample fetches.** They are the only handler types whose return value HAProxy reads back and turns into a sample, so they are the only ones every rule below applies to. An action or a service returns nothing HAProxy consumes; its failure contract is a named variable plus a rejecting configuration rule, and it is stated in `references/25-actions-services-and-subrequests.md`. Applying the rules below to an action produces a rule that cannot be satisfied, and applying the action contract to a converter leaves the converter failing open.

## What a Lua return value becomes

HAProxy converts the Lua value your handler returns into a sample. `doc/lua.txt` gives the mapping:

| Lua type | HAProxy sample type |
|---|---|
| `number` | `sint` |
| `boolean` | `bool` |
| `string` | `str` |
| `userdata` | `bool` (false) |
| `nil` | `bool` (false) |
| `table` | `bool` (false) |
| `function` | `bool` (false) |
| `thread` | `bool` (false) |

**`nil` is not "no value". `nil` is boolean false.** A converter that returns `nil` returns a successful sample whose value is false, which renders as the string `0`.

## Measured rendering

Observed on HAProxy 2.8.16 with Lua 5.4.6 on 26 July 2026, using a frontend that fed each result into a variable and a header:

| Handler behaviour | `var(txn.x)` after it | `var(txn.x,DEFAULT)` | `set-header` result | ACL `var(txn.x) -m found` |
|---|---|---|---|---|
| returns a string | the string | the string | header set to the string | matches |
| returns `nil` | `0` | `0` | header set to `0` | **matches** |
| calls `error(...)` | unset | `DEFAULT` | header **added with an empty value** | does not match |

Two conclusions follow, and both invert the intuitive reading.

1. **Returning `nil` is the most dangerous failure shape available.** The variable is set, the default in `var(name,default)` never fires, and `-m found` matches. A guard written as `deny unless { var(txn.token) -m found }` passes a value the handler explicitly rejected.
2. **A failing sample does not reject anything on its own.** `http-request set-header` still adds the header, with an empty value. The rejection has to be a separate rule.

## The rule

**Signal every failure of a converter or a sample fetch with `error(message, 0)`.** The sample then fails, the target variable stays unset, and a configuration rule can act on that. Inside an action or a service there is no sample to fail, so `error` there aborts the handler and logs, and the rejection has to come from the variable the handler set before it raised.

**Pair every fallible converter or fetch with an explicit rejection at its call site**, because setting a variable is not a decision:

```
http-request set-var(txn.token) var(txn.raw_token),lua.token_guard(64)
http-request deny deny_status 400 unless { var(txn.token) -m found }
```

The `deny` line is what makes the failure closed. Without it, a rejected value is merely absent and the request proceeds.

**Decide the failure mode per call site, not per module.** Two shapes exist and choosing between them is a judgement about what the value is for:

- **Reject** — the value gates access, identifies a caller, or is written to a header a backend will trust. The handler raises and the configuration denies. This is the default; take it unless the second case is argued.
- **Explicit sentinel** — the value is advisory, the request is still valid without it, and a downstream consumer can distinguish "absent" from "present". The handler returns a string the configuration recognises, never `nil` and never the empty string, because the empty string is also what a failed sample renders as in a header.

Which of the two applies is a fail-closed question owned by `/alaa-security-review` (`$alaa-security-review`); the sentinel *value* itself is a contract name owned by `/alaa-services-contract` (`$alaa-services-contract`).

## `error(message)` versus `error(message, 0)`

Level `0` suppresses the position information Lua prepends to the message. Measured on the same build, the two produce these log lines:

```
error("level-one-message")
  Lua converter 'e_lvl1': [state-id 0] runtime error: /home/claude/t/err.lua:1: level-one-message
    from [C]: in global 'error', /home/claude/t/err.lua:1: in function line 1.

error("level-zero-message", 0)
  Lua converter 'e_lvl0': [state-id 0] runtime error: level-zero-message
    from [C]: in global 'error', /home/claude/t/err.lua:2: in function line 2.
```

Three facts to carry from that output:

- The default level puts the **absolute deployed path and line number inside the message itself**, where it is copied into alerts, tickets, and dashboards.
- Level `0` removes it from the message. The traceback HAProxy appends still names the file, so `error(message, 0)` reduces the leak and does not eliminate it. Never rely on the message being private.
- HAProxy logs the failure at **ALERT**, once per occurrence. A handler that raises on attacker-controlled input gives the attacker one ALERT line per request. Validate cheaply and bound the input before the expensive check, and keep the message short and constant-shaped.

## Where `pcall` is correct and where it hides the defect

`pcall` is correct in exactly one place: **a test harness**, where the test needs to assert that a call raised. `examples/haproxy-lua/token-guard.test.lua` uses it that way.

`pcall` inside a registered handler is wrong whenever its failure branch returns a value, because it converts every fault — a genuine invalid input, a typo in the module, an out-of-memory error — into a successful sample. The shipped pattern to recognise and reject in review:

```lua
local function safe_wrapper(name, callback)
    return function(...)
        local ok, result = pcall(callback, ...)
        if ok then return result end
        core.Warning(name .. " failed: " .. tostring(result))
        return nil            -- becomes boolean false, sets the variable, renders as 0
    end
end
```

The warning here is worse than useless: it creates the impression that the failure was handled while the caller receives a value that passes every downstream guard. Delete the wrapper and let the error reach HAProxy, which logs it and fails the sample.

`pcall` inside a handler is acceptable only when the failure branch re-raises with `error(message, 0)` after adding context. If it re-raises unchanged, it is adding nothing and should be removed.

## Booleans are ambiguous across versions

`tune.lua.bool-sample-conversion` exists because HAProxy-to-Lua conversion historically turned booleans into integers. The manual states that when the option is not set explicitly and a Lua script is loaded, HAProxy emits a warning and defaults to `pre-3.1-bug`, and that the setting "must be set before any `lua-load` or `lua-load-per-thread` directive for it to be considered, else it is ignored".

The rule for module authors: **never return a Lua boolean from a converter or fetch, and never compare a value fetched from HAProxy against `true` or `false`.** Return and compare strings. That removes the module's dependence on a process-wide setting it cannot see. Whether to set the option, and to which value, is a configuration decision owned by `/alaa-haproxy` (`$alaa-haproxy`).

## Failures that are not your handler's

Two failure paths sit outside the handler and are still yours to design for.

- **Load failure.** A Lua syntax error, a missing file, or an error raised in the file body aborts startup. `haproxy -c -f <config>` reproduces it before deployment and exits non-zero; see `references/50-testing.md`.
- **Timeout.** A handler that exceeds `tune.lua.burst-timeout` is aborted mid-execution. Any state it left half-written in a HAProxy variable stays half-written, so write the variable once, at the end, from a value that is already complete.
