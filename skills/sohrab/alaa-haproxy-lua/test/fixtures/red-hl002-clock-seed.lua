-- Red fixture for HL002: the PRNG is seeded from the clock, never from /dev/urandom.
-- Requires Lua 5.3 or newer.
local M = {}

local seeded = false

local function ensure_seeded()
    if seeded then
        return
    end
    math.randomseed(os.time())
    seeded = true
end

function M.token()
    ensure_seeded()
    return string.format("%08x", math.random(0, 16777215))
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("token", M.token)
end

return M
