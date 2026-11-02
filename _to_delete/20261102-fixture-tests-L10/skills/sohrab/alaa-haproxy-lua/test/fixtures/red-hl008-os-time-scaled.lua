-- Regression: historical HL008 red fixture is now valid coarse unit conversion.
-- Millisecond units with whole-second precision are deliberate, not extra precision.
-- Requires Lua 5.3 or newer.
local M = {}

function M.stamp()
    return tostring(os.time() * 1000)
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("stamp", M.stamp)
end

return M
