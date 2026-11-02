-- Red fixture for HL007: print() inside a registered handler.
-- Requires Lua 5.3 or newer.
local M = {}

function M.trace(value)
    print(value)
    return value
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("trace", M.trace)
end

return M
