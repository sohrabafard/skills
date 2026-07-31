-- Green fixture: the converter shape, with every failure raised at level 0.
-- Requires Lua 5.3 or newer.
local M = {}

local ALLOWED = {}
for i = 48, 57 do
    ALLOWED[i] = true
end

function M.check(value)
    if type(value) ~= "string" then
        error("check: sample is not a string", 0)
    end
    if #value == 0 or #value > 64 then
        error("check: length outside [1,64]", 0)
    end
    for i = 1, #value do
        if not ALLOWED[string.byte(value, i)] then
            error("check: byte at offset " .. i .. " is not allowed", 0)
        end
    end
    return value
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("check", M.check)
end

return M
