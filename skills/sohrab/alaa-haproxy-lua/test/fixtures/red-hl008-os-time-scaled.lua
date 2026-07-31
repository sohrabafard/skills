-- Red fixture for HL008: os.time() multiplied to fake sub-second resolution.
-- Requires Lua 5.3 or newer.
local M = {}

function M.stamp()
    return tostring(os.time() * 1000)
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("stamp", M.stamp)
end

return M
