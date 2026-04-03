-- Shared lowercase Crockford Base32 helpers plus no-conflict typed tokens.
--
-- This module is shaped for HAProxy `lua-load` / `lua-load-per-thread` usage.
-- It registers a few converters and fetches when the HAProxy `core` object is
-- available, while still returning a reusable table for plain Lua callers.
-- The UUIDv7 helper uses Lua-side pseudo-random bytes, so treat it as suitable
-- for request identifiers and correlation values, not for secrets.

local M = {}

local ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
local TYPE_BYTES = "b"
local TYPE_INTEGER = "n"
local TYPE_STRING = "s"
local TYPE_UUID_V7 = "v"

local LOOKUP = {}
for index = 1, #ALPHABET do
    LOOKUP[ALPHABET:sub(index, index)] = index - 1
end

local seeded = false

local function normalize_encoded(value)
    local normalized = string.lower(value):gsub("%-", "")

    normalized = normalized:gsub("[il]", "1")
    normalized = normalized:gsub("o", "0")

    return normalized
end

local function extract_payload(token, expected_prefix)
    if token == nil or token == "" then
        error("Typed token cannot be empty.")
    end

    local prefix = string.lower(token:sub(1, 1))

    if prefix ~= expected_prefix then
        error(string.format("Expected token prefix [%s], got [%s].", expected_prefix, prefix))
    end

    return token:sub(2)
end

local function ensure_seeded()
    if seeded then
        return
    end

    local seed = os.time() + math.floor(os.clock() * 1000000)
    math.randomseed(seed)
    math.random()
    math.random()
    math.random()
    seeded = true
end

local function random_bytes(count)
    ensure_seeded()

    local parts = {}

    for index = 1, count do
        parts[index] = string.char(math.random(0, 255))
    end

    return table.concat(parts)
end

local function bytes_to_uuid(bytes)
    local hex = {}

    for index = 1, #bytes do
        hex[index] = string.format("%02x", string.byte(bytes, index))
    end

    local joined = table.concat(hex)

    return table.concat({
        joined:sub(1, 8),
        joined:sub(9, 12),
        joined:sub(13, 16),
        joined:sub(17, 20),
        joined:sub(21, 32),
    }, "-")
end

local function uuid_to_bytes(uuid)
    local normalized = string.lower(uuid)

    if not normalized:match("^[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]%-%x%x%x%x%-%x%x%x%x%-%x%x%x%x%-%x%x%x%x%x%x%x%x%x%x%x%x$") then
        error("UUID must be in canonical 8-4-4-4-12 hexadecimal form.")
    end

    local compact = normalized:gsub("%-", "")
    local parts = {}

    for index = 1, #compact, 2 do
        parts[#parts + 1] = string.char(tonumber(compact:sub(index, index + 1), 16))
    end

    return table.concat(parts)
end

local function assert_uuid_v7_bytes(bytes)
    if #bytes ~= 16 then
        error("UUID payload must contain exactly 16 bytes.")
    end

    local version = string.byte(bytes, 7) >> 4
    local variant = string.byte(bytes, 9) & 0xC0

    if version ~= 7 then
        error("UUID payload must be version 7.")
    end

    if variant ~= 0x80 then
        error("UUID payload must use the RFC 4122 variant bits.")
    end
end

function M.encode_bytes(bytes)
    if bytes == "" then
        return ""
    end

    local buffer = 0
    local bit_count = 0
    local parts = {}

    for index = 1, #bytes do
        buffer = (buffer << 8) | string.byte(bytes, index)
        bit_count = bit_count + 8

        while bit_count >= 5 do
            bit_count = bit_count - 5
            local value = (buffer >> bit_count) & 31
            parts[#parts + 1] = ALPHABET:sub(value + 1, value + 1)
            buffer = buffer & ((1 << bit_count) - 1)
        end
    end

    if bit_count > 0 then
        local value = (buffer << (5 - bit_count)) & 31
        parts[#parts + 1] = ALPHABET:sub(value + 1, value + 1)
    end

    return table.concat(parts)
end

function M.decode_bytes(encoded)
    local normalized = normalize_encoded(encoded)

    if normalized == "" then
        return ""
    end

    local buffer = 0
    local bit_count = 0
    local parts = {}

    for index = 1, #normalized do
        local character = normalized:sub(index, index)
        local value = LOOKUP[character]

        if value == nil then
            error(string.format("Invalid Crockford Base32 character [%s].", character))
        end

        buffer = (buffer << 5) | value
        bit_count = bit_count + 5

        while bit_count >= 8 do
            bit_count = bit_count - 8
            parts[#parts + 1] = string.char((buffer >> bit_count) & 0xFF)
            buffer = buffer & ((1 << bit_count) - 1)
        end
    end

    if bit_count > 0 and buffer ~= 0 then
        error("Invalid Crockford Base32 payload padding bits.")
    end

    return table.concat(parts)
end

function M.encode_bytes_token(bytes)
    return TYPE_BYTES .. M.encode_bytes(bytes)
end

function M.decode_bytes_token(token)
    return M.decode_bytes(extract_payload(token, TYPE_BYTES))
end

function M.encode_int(value)
    local integer = math.tointeger(value)

    if integer == nil then
        error("Integer token input must be a Lua integer value.")
    end

    return TYPE_INTEGER .. M.encode_bytes(string.pack(">i8", integer))
end

function M.decode_int(token)
    local payload = M.decode_bytes(extract_payload(token, TYPE_INTEGER))

    if #payload ~= 8 then
        error("Integer token payload must decode to exactly 8 bytes.")
    end

    local value = string.unpack(">i8", payload)

    return value
end

function M.encode_string(value)
    return TYPE_STRING .. M.encode_bytes(value)
end

function M.decode_string(token)
    return M.decode_bytes(extract_payload(token, TYPE_STRING))
end

function M.generate_uuid_v7()
    local bytes = random_bytes(16)
    local milliseconds = (os.time() * 1000) + math.floor((os.clock() * 1000) % 1000)
    local parts = {}

    for index = 16, 1, -1 do
        parts[index] = bytes:sub(index, index)
    end

    for index = 6, 1, -1 do
        parts[index] = string.char(milliseconds & 0xFF)
        milliseconds = milliseconds >> 8
    end

    parts[7] = string.char((string.byte(parts[7]) & 0x0F) | 0x70)
    parts[9] = string.char((string.byte(parts[9]) & 0x3F) | 0x80)

    return bytes_to_uuid(table.concat(parts))
end

function M.generate_uuid_v7_token()
    return M.encode_uuid_v7(M.generate_uuid_v7())
end

function M.encode_uuid_v7(uuid)
    local bytes = uuid_to_bytes(uuid)
    assert_uuid_v7_bytes(bytes)

    return TYPE_UUID_V7 .. M.encode_bytes(bytes)
end

function M.decode_uuid_v7(token)
    local payload = M.decode_bytes(extract_payload(token, TYPE_UUID_V7))
    assert_uuid_v7_bytes(payload)

    return bytes_to_uuid(payload)
end

function M.decode_token(token)
    local prefix = string.lower((token or ""):sub(1, 1))

    if prefix == TYPE_BYTES then
        return { type = "bytes", value = M.decode_bytes_token(token) }
    end

    if prefix == TYPE_INTEGER then
        return { type = "int", value = M.decode_int(token) }
    end

    if prefix == TYPE_STRING then
        return { type = "string", value = M.decode_string(token) }
    end

    if prefix == TYPE_UUID_V7 then
        return { type = "uuidv7", value = M.decode_uuid_v7(token) }
    end

    error(string.format("Unsupported typed token prefix [%s].", prefix))
end

local function safe_wrapper(name, callback)
    return function(...)
        local ok, result = pcall(callback, ...)

        if ok then
            return result
        end

        if core ~= nil and core.Warning ~= nil then
            core.Warning(string.format("crockford-base32-token-codec.lua %s failed: %s", name, result))
        end

        return nil
    end
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("crockford_b32_encode_string", safe_wrapper("encode_string", function(value)
        return M.encode_string(value or "")
    end))

    core.register_converters("crockford_b32_decode_string", safe_wrapper("decode_string", function(value)
        return M.decode_string(value or "")
    end))

    core.register_converters("crockford_b32_encode_int", safe_wrapper("encode_int", function(value)
        return M.encode_int(tonumber(value))
    end))

    core.register_converters("crockford_b32_decode_int", safe_wrapper("decode_int", function(value)
        return tostring(M.decode_int(value or ""))
    end))

    core.register_converters("crockford_b32_encode_uuidv7", safe_wrapper("encode_uuid_v7", function(value)
        return M.encode_uuid_v7(value or "")
    end))

    core.register_converters("crockford_b32_decode_uuidv7", safe_wrapper("decode_uuid_v7", function(value)
        return M.decode_uuid_v7(value or "")
    end))
end

if core ~= nil and core.register_fetches ~= nil then
    core.register_fetches("crockford_b32_uuidv7", function()
        return M.generate_uuid_v7()
    end)

    core.register_fetches("crockford_b32_uuidv7_token", function()
        return M.generate_uuid_v7_token()
    end)
end

return M
