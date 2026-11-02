-- Red fixture for HL006: the registration is not behind a core guard, so no unit
-- test can require this module.
-- Requires Lua 5.3 or newer.
local M = {}

function M.echo(value)
    return value
end

core.register_converters("echo", M.echo)

return M
