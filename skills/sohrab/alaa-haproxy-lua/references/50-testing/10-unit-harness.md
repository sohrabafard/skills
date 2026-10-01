# Unit tests with a mock `core`

HAProxy injects `core` and other API globals (including `act`). Set it yourself before loading the module, and the module's registration branch runs against your table instead of HAProxy's.

```lua
local mock_core = { converters = {}, fetches = {}, logs = {} }

function mock_core.register_converters(name, handler)
    mock_core.converters[name] = handler
end

function mock_core.log(level, message)
    mock_core.logs[#mock_core.logs + 1] = { level = level, message = message }
end

_G.core = mock_core

local module = dofile("token-guard.lua")
```

This works only if the module obeys two rules, which is the practical reason they exist:

1. **Every `core` reference in the file body sits inside the `if core ~= nil and core.register_… ~= nil then` guard.** An unguarded `core.register_converters(...)` at file scope raises `attempt to index a nil value (global 'core')` the moment a test loads the file.
2. **The module returns its table.** `return M` at the end of the file gives the test direct access to the functions, so a test can call `M.validate` without going through the registration table.

The mock is a double, and a double can drift from the real object. Record what binds it: here, the binding is that the registration names asserted in the test are the same strings the configuration uses under the `lua.` prefix, and `haproxy -c -f` fails when they disagree.

## Which runner

**Use the interpreter that `haproxy -vv` reports on the `Built with Lua version` line.** Testing under a different Lua tests a different language: `lua5.1` rejects `>>` with `unexpected symbol near '>'` and has no `math.tointeger`, while HAProxy supports only 5.3 and above. A test failure caused by the wrong interpreter looks exactly like a module defect and wastes the review.

**Ship the test as a plain Lua script with no dependencies**, runnable as `lua5.4 <module>.test.lua`, so it runs on any machine that has the interpreter and needs no package manager inside a container image. `examples/haproxy-lua/token-guard.test.lua` is that shape: a table-driven case set, a property case, `os.exit(0)` on success and `os.exit(1)` on any failure.

`busted`, installed with `luarocks install busted`, is the conventional Lua test framework and gives assertions, spies, and structured output for a suite that outgrows a single file. Its installation was attempted in this skill's build environment on 26 July 2026 and failed while fetching a transitive dependency, so its behaviour under this pack is **unverified**; verify it in your own environment before making a suite depend on it.

For scope and related decisions, return to the [parent reference](../50-testing.md).
