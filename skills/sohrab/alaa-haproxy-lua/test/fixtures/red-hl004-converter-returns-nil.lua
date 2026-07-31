-- Red fixture for HL004: a registered converter signals failure by returning nil.
-- Requires Lua 5.3 or newer.
local M = {}

function M.decode(value)
    if #value == 0 then
        return nil
    end
    return value
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("decode", M.decode)
end

return M
