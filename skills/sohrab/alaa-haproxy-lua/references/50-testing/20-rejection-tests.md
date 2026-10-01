# Table-driven cases

One table, one row per input, one loop. The value is that adding a case is adding a row, so nobody skips the awkward input because writing another function felt expensive.

```lua
local rejected = {
    { name = "empty string",     token = "" },
    { name = "too short",        token = "abc" },
    { name = "uppercase byte",   token = "abcdefgH" },
    { name = "embedded newline", token = "abcdef\ngh" },
    { name = "embedded NUL",     token = "abcdef\0gh" },
    { name = "non-string sample", token = 12345 },
}

for _, case in ipairs(rejected) do
    local ok, message = pcall(module.validate, case.token)
    check("rejects " .. case.name, ok == false, tostring(message))
end
```

Include the embedded newline and the embedded NUL in every case set for a handler that touches network bytes, because those two are what turn a validation gap into header injection.

## Prove the failure path, not the happy path

A converter's failure path decides whether a forged value reaches the backend, so it is the half that must be tested. Three assertions per rejection, all present in the shipped example:

1. **The call raised.** `pcall` returned `false`.
2. **The message carries no source position.** `message:match("^[^\n]-%.lua:%d+:") == nil` fails when someone writes `error(msg)` instead of `error(msg, 0)`, which is otherwise invisible until it appears in a production alert.
3. **The message does not echo the rejected value.** `message:find(case.token, 1, true) == nil` keeps attacker-controlled bytes out of the operator log.

Prove the assertions bite, by removal. Two mutations of the example module, each run against the unchanged test on 26 July 2026:

| Mutation | Test result |
|---|---|
| `error("… not a string", 0)` → `error("… not a string")` | 27 of 28 checks passed, exit 1, failing check names the leaked path |
| dropping `length < MIN_LENGTH` from the length guard | 22 of 25 checks passed, exit 1, three checks fail including the property |

A test suite that still passes after you break the module is measuring nothing.

For scope and related decisions, return to the [parent reference](../50-testing.md).
