# `error(message)` versus `error(message, 0)`

Level `0` suppresses the position information Lua prepends to the message. Historical capture on HAProxy 2.8.16/Lua 5.4.6 (26 July 2026), the two produce these log lines:

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

`pcall` is useful in a test harness and in runtime cleanup/recovery that preserves the declared failure contract. `examples/haproxy-lua/token-guard.test.lua` uses it that way.

`pcall` inside a sample handler violates the error contract when it hides an unexpected fault or returns an undeclared success-shaped value, because it can convert a fault — a genuine invalid input, a typo in the module, an out-of-memory error — into a successful sample. The shipped pattern to recognise and reject in review:

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

For a sample-producing handler using the error contract, re-raise a sanitized constant error after cleanup. Actions may catch expected dependency errors and leave the configured deny decision intact. Never catch an unexpected fault and silently publish success.

For scope and related decisions, return to the [parent reference](../30-failure-visibility.md).
