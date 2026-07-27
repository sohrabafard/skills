# Clean Code and Design Patterns

The constraints here are not general Lua style. They come from three properties of the environment: the module is loaded once and called on every request, the only global HAProxy injects is `core`, and a stall is charged to other people's traffic.

Copy `examples/haproxy-lua/token-guard.lua` when starting a module. It is the shape this file describes, and it passes the checker with zero findings.

## The module pattern

```lua
-- <name>.lua - one sentence on what it does.
-- Requires Lua 5.3 or newer.
-- Load with: lua-load-per-thread /etc/haproxy/lua/<name>.lua

local M = {}

-- load-time constants and precomputed tables here

function M.<operation>(...)
    ...
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("<name>", M.<operation>)
end

return M
```

Four properties, each with a reason that is specific to this environment.

**A returned table beats globals.** Under `lua-load` a Lua global is visible to every other loaded file and every thread, so two modules that both define `helper` silently overwrite each other. Under `lua-load-per-thread` the manual states globals are thread-local and "it is strongly recommended not to use global variables in programs loaded this way", so a global written on one thread is invisible on the next and the bug appears only under load. A local table returned at the end has neither failure mode.

**Registration is guarded, and the guard names the function it is about to call.** `if core ~= nil and core.register_converters ~= nil then` is the entire mechanism that lets a unit test load the file. Checking `core ~= nil` alone is not enough, because a mock that omits a registration function then fails inside the guard.

**The handler is reachable directly.** `return M` lets a test call `M.validate(input)` without reconstructing a converter invocation.

**The minimum Lua version is written in the file.** The version is a property of the deployment that no other file records, and it decides which interpreter the test must run under.

## Locals, closures, and upvalues

**Localise every global you call more than once per request**, at load time:

```lua
local string_byte = string.byte
local string_format = string.format
```

A global read in Lua is a hash lookup in the globals table. Inside a loop over the bytes of a request value, that lookup happens once per byte, on every request. Hoisting it costs one line and removes the lookup entirely.

**Hold configuration in upvalues, not in globals or in re-read state.** A closure over a load-time value is the natural configuration mechanism here: the value is computed once, is private to the module, and is visible to every call without a lookup.

```lua
local function make_validator(max_length)
    return function(value)
        if #value > max_length then
            error("too long", 0)
        end
        return value
    end
end
```

**Precompute at load time whatever does not depend on the request.** Byte allowlists, format strings, parsed configuration, and lookup tables belong in the file body. Rebuilding a table per request allocates per request; see `references/70-performance.md`.

## Metatables

Use a metatable when it removes repetition that would otherwise be written by hand: `__index` for a shared method table on objects a filter creates per stream, and `__call` to make a configured object usable where a plain function is expected.

Do not use a metatable for a converter or a fetch. Those handlers receive strings and return strings, `__index` on a hot path adds a lookup per miss, and a metatable makes the module harder to load in a test for no gain. A metatable that exists to look sophisticated is a cost paid on every request.

## Pure codec versus stateful handler

Separate them inside the file, and the separation decides where every test assertion goes.

A **pure function** takes its inputs as arguments, touches no `core` object and no `TXN`, and returns a value or raises. It is testable with no mock at all, it can be reused by a fetch and an action alike, and it is where all of the logic belongs.

A **stateful handler** reads the transaction, calls the pure function, and writes the result. It should contain no branching beyond the call and the write:

```lua
core.register_action("stamp_token", { "http-req" }, function(txn)
    local raw = txn:get_var("txn.raw_token")
    txn:set_var("txn.token", M.validate(raw), true)
end)
```

When a handler is more than a few lines, the logic has leaked out of the pure function and the tests are about to become HAProxy-dependent.

## Per-request state

Module-level locals are per Lua state and live for the lifetime of the process or thread. Putting request data there leaks it between unrelated requests, and under `lua-load` between unrelated threads.

- Per-request Lua values: `TXN.set_priv` and `TXN.get_priv`.
- Values the configuration must see: `TXN.set_var` with `ifexist` set to `true`.
- Values shared between threads: a module-level table under `lua-load` only, and only after accounting for the global Lua lock.

## Keeping the module testable

**Never touch `core` at load time outside the guard.** This is rule 5 of the body and check HL006 of the checker, and it is the difference between a module that has tests and one that does not.

**Never read a file, open a socket, or resolve a name at the top level unconditionally.** Do it inside `core.register_init`, or guard it so the test path skips it. A test that has to create `/etc/haproxy/...` to load a module will not be written.

**Never call `os.exit` from module code.** It ends the HAProxy process, and HAProxy forbids it at runtime for that reason.

## Naming and layout

- One module per file, and the file name matches the module's purpose in lower case with hyphens: `token-guard.lua`.
- The test sits beside it as `<name>.test.lua`, and the minimal configuration as `<name>.cfg`, so a reviewer can see at a glance whether a module has a test.
- The registered name matches the file: `core.register_converters("token_guard", …)` in `token-guard.lua`, reachable from the configuration as `lua.token_guard`. Registered names use underscores because the configuration reads them as identifiers.
- Prefix the registered name when a module could collide with another team's: the `lua.` prefix is shared across every loaded file, so two files registering `validate` is a startup-order-dependent bug.
- Error messages start with the module name — `token-guard: length 3 is outside [8,64]` — because the HAProxy log line names the converter but not the file.

The ten-point quality bar that applies to all code in this pack is owned by `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md`; this file adds only what is specific to Lua inside HAProxy.
