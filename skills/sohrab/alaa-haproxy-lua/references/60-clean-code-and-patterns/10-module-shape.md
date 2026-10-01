# The module pattern

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

## Naming and layout

- One module per file, and the file name matches the module's purpose in lower case with hyphens: `token-guard.lua`.
- The test sits beside it as `<name>.test.lua`, and the minimal configuration as `<name>.cfg`, so a reviewer can see at a glance whether a module has a test.
- The registered name matches the file: `core.register_converters("token_guard", …)` in `token-guard.lua`, reachable from the configuration as `lua.token_guard`. Use underscores in registered names as the pack convention.
- Prefix the registered name when a module could collide with another team's: the `lua.` prefix is shared across every loaded file, so two files registering `validate` is a startup-order-dependent bug.
- Error messages start with the module name — `token-guard: length 3 is outside [8,64]` — because the HAProxy log line names the converter but not the file.

The ten-point quality bar that applies to all code in this pack is owned by `/alaa-project-constitution` `references/quality-bar.md`; this file adds only what is specific to Lua inside HAProxy.

For scope and related decisions, return to the [parent reference](../60-clean-code-and-patterns.md).
