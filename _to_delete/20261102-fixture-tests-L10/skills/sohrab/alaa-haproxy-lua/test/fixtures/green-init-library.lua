-- Initialization I/O and bounded non-yielding computation are permitted.
-- Requires Lua 5.4 or newer.
local M = {}
function M.initialize()
    local handle = assert(io.open("/dev/null", "rb"))
    handle:close()
end
function M.echo(value)
    return string.upper(value)
end
if core ~= nil and core.register_init ~= nil then
    core.register_init(M.initialize)
    core.register_converters("echo", M.echo)
end
return M
