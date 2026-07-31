local M = {}

function M.high(value)
    local n = tonumber(value) or 0
    return tostring(n >> 8)
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("high", M.high)
end

return M
