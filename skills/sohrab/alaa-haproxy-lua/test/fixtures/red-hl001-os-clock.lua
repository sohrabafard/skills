-- Red fixture for HL001: os.clock() used as if it were a clock.
-- Requires Lua 5.3 or newer.
local M = {}

function M.elapsed()
    return tostring(os.clock())
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("elapsed", M.elapsed)
end

return M
