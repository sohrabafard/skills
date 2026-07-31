-- Red fixture for HL003: error() without level 0 leaks the deployed file path.
-- Requires Lua 5.3 or newer.
local M = {}

function M.check(value)
    if value == "" then
        error("check: empty value")
    end
    return value
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("check", M.check)
end

return M
