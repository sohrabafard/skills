-- token-guard.lua - a converter that validates an opaque client-supplied token.
--
-- Requires Lua 5.3 or newer. HAProxy supports Lua 5.3 and above only
-- (HAProxy INSTALL, section 4.7 "Lua"), so no 5.1 or LuaJIT fallback exists.
--
-- Load it per thread, because the module holds no mutable state:
--     lua-load-per-thread /etc/haproxy/lua/token-guard.lua
--
-- The converter returns the input unchanged when the token is well formed and
-- calls error(message, 0) otherwise. An error makes the HAProxy sample fail, so
-- the target variable stays unset and the configuration can reject the request.
-- Returning nil instead would produce a boolean-false sample that renders as 0
-- and passes every "-m found" guard.

local M = {}

-- Hot globals resolved once at load time. Each lookup avoided here is a hash
-- lookup avoided on every byte of every request.
local string_byte = string.byte
local string_format = string.format

-- Byte allowlist precomputed at load time: lowercase Crockford-style tokens use
-- 0-9 and a-z. Building this table per request would allocate on every call.
local ALLOWED_BYTE = {}
for code = 48, 57 do ALLOWED_BYTE[code] = true end -- 0-9
for code = 97, 122 do ALLOWED_BYTE[code] = true end -- a-z

local MIN_LENGTH = 8
local MAX_LENGTH = 128

-- validate returns the token unchanged, or raises. max_length arrives from the
-- HAProxy configuration as a string, because every converter argument is a
-- string.
function M.validate(token, max_length)
    if type(token) ~= "string" then
        error("token-guard: sample is not a string", 0)
    end

    local limit = tonumber(max_length) or MAX_LENGTH
    if limit < MIN_LENGTH or limit > MAX_LENGTH then
        error(
            string_format(
                "token-guard: configured max length %s is outside [%d,%d]",
                tostring(max_length),
                MIN_LENGTH,
                MAX_LENGTH
            ),
            0
        )
    end

    -- Bound the length before scanning, so an attacker cannot make the loop
    -- cost grow with the size of the value they send.
    local length = #token
    if length < MIN_LENGTH or length > limit then
        error(
            string_format(
                "token-guard: length %d is outside [%d,%d]",
                length,
                MIN_LENGTH,
                limit
            ),
            0
        )
    end

    for offset = 1, length do
        local code = string_byte(token, offset)
        if not ALLOWED_BYTE[code] then
            -- The message carries the offset and the byte value, never the
            -- token itself, because HAProxy logs this line at ALERT level.
            error(
                string_format(
                    "token-guard: byte 0x%02x at offset %d is not allowed",
                    code,
                    offset
                ),
                0
            )
        end
    end

    return token
end

-- Registration is guarded so that `dofile` from a unit test loads the module
-- without a HAProxy core object present.
if core ~= nil and core.register_converters ~= nil then
    core.register_converters("token_guard", M.validate)
end

return M
