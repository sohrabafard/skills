# Locals, closures, and upvalues

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

Do not use a metatable for a converter or a fetch. Keep those handlers as plain functions; `__index` on a hot path adds a lookup per miss, and a metatable makes the module harder to load in a test for no gain. Their input and return types follow `references/20-api-surface.md` and `references/30-failure-visibility.md`.

For scope and related decisions, return to the [parent reference](../60-clean-code-and-patterns.md).
