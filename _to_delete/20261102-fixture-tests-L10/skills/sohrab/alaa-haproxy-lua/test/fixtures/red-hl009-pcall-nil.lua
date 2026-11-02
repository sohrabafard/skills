-- Red fixture for HL009: a registered converter swallows the error with pcall and
-- then returns nil, so every failure becomes a successful-looking sample.
-- Requires Lua 5.3 or newer.
local M = {}

function M.parse(value)
    local ok, result = pcall(function()
        return tonumber(value)
    end)
    if not ok then
        return nil
    end
    return tostring(result)
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("parse", M.parse)
end

return M
