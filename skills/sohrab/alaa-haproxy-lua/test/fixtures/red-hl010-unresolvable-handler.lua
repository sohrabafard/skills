-- Red fixture for HL010: the converter handler is built by a call, so this checker
-- cannot find its body and cannot evaluate HL004 for it. The closure it returns does
-- signal failure by returning nil, which is the defect HL010 exists to keep visible.
-- Requires Lua 5.3 or newer.
local M = {}

local function make_checker(maximum)
    return function(value)
        if #value > maximum then
            return nil
        end
        return value
    end
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("check", make_checker(64))
end

return M
