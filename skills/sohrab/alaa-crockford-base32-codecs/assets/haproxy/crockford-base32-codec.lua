-- Pure lowercase Crockford Base32 codecs for bytes, integers, strings, and UUIDv7 values.
--
-- This module is shaped for HAProxy `lua-load` / `lua-load-per-thread` usage.
-- It registers reusable converters when the HAProxy `core` object is available
-- while still returning a plain Lua table for non-HAProxy callers.
--
-- Integer strategy:
-- - positive integers encode as minimal unsigned Crockford Base32 digits
-- - negative integers encode as `-` plus the minimal unsigned magnitude
-- - zero always encodes as `0`

local M = {}

local ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
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

local function trim_leading_decimal_zeros(value)
    local trimmed = value:gsub("^0+", "")

    if trimmed == "" then
        return "0"
    end

    return trimmed
end

local function normalize_integer_input(value)
    local text = tostring(value)

    if type(value) == "number" then
        local integer = math.tointeger(value)

        if integer == nil then
            error("Integer input must be a Lua integer value.")
        end

        text = tostring(integer)
    end

    if not text:match("^%-?%d+$") then
        error("Integer input must be a canonical base-10 integer.")
    end

    local negative = text:sub(1, 1) == "-"
    local magnitude = negative and text:sub(2) or text
    magnitude = trim_leading_decimal_zeros(magnitude)

    return negative and magnitude ~= "0", magnitude
end

local function divide_decimal_string_by_32(decimal)
    local carry = 0
    local quotient = {}

    for index = 1, #decimal do
        carry = (carry * 10) + tonumber(decimal:sub(index, index))
        local digit = math.floor(carry / 32)

        if #quotient > 0 or digit ~= 0 then
            quotient[#quotient + 1] = tostring(digit)
        end

        carry = carry % 32
    end

    if #quotient == 0 then
        return "0", carry
    end

    return table.concat(quotient), carry
end

local function encode_unsigned_decimal_to_base32(decimal)
    if decimal == "0" then
        return "0"
    end

    local digits = {}
    local value = decimal

    while value ~= "0" do
        local quotient, remainder = divide_decimal_string_by_32(value)
        digits[#digits + 1] = ALPHABET:sub(remainder + 1, remainder + 1)
        value = quotient
    end

    local reversed = {}

    for index = #digits, 1, -1 do
        reversed[#reversed + 1] = digits[index]
    end

    return table.concat(reversed)
end

local function multiply_decimal_string_by_32_and_add(decimal, addend)
    local carry = addend
    local reversed = {}

    for index = #decimal, 1, -1 do
        local value = (tonumber(decimal:sub(index, index)) * 32) + carry
        reversed[#reversed + 1] = tostring(value % 10)
        carry = math.floor(value / 10)
    end

    while carry > 0 do
        reversed[#reversed + 1] = tostring(carry % 10)
        carry = math.floor(carry / 10)
    end

    local digits = {}

    for index = #reversed, 1, -1 do
        digits[#digits + 1] = reversed[index]
    end

    return table.concat(digits)
end

local function split_signed_encoded_integer(encoded)
    if encoded == nil or encoded == "" then
        error("Integer payload cannot be empty.")
    end

    local negative = encoded:sub(1, 1) == "-"
    local magnitude = negative and encoded:sub(2) or encoded
    magnitude = normalize_encoded(magnitude)

    if magnitude == "" then
        error("Integer payload cannot be empty.")
    end

    if #magnitude > 1 and magnitude:sub(1, 1) == "0" then
        error("Integer payload must use a minimal Crockford Base32 representation.")
    end

    return negative, magnitude
end

local function decode_unsigned_base32_to_decimal(encoded)
    local decimal = "0"

    for index = 1, #encoded do
        local character = encoded:sub(index, index)
        local value = LOOKUP[character]

        if value == nil then
            error(string.format("Invalid Crockford Base32 integer character [%s].", character))
        end

        decimal = multiply_decimal_string_by_32_and_add(decimal, value)
    end

    return trim_leading_decimal_zeros(decimal)
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

function M.encode_int(value)
    local negative, magnitude = normalize_integer_input(value)
    local encoded = encode_unsigned_decimal_to_base32(magnitude)

    if negative and encoded ~= "0" then
        return "-" .. encoded
    end

    return encoded
end

function M.decode_int(encoded)
    local negative, magnitude = split_signed_encoded_integer(encoded)
    local decimal = decode_unsigned_base32_to_decimal(magnitude)

    if negative and decimal ~= "0" then
        return "-" .. decimal
    end

    return decimal
end

function M.encode_string(value)
    return M.encode_bytes(value)
end

function M.decode_string(encoded)
    return M.decode_bytes(encoded)
end

function M.generate_uuid_v7()
    local bytes = random_bytes(16)
    local milliseconds = (os.time() * 1000) + math.floor((os.clock() * 1000) % 1000)
    local parts = {}

    for index = 1, 16 do
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

function M.encode_uuid_v7(uuid)
    local bytes = uuid_to_bytes(uuid)
    assert_uuid_v7_bytes(bytes)

    return M.encode_bytes(bytes)
end

function M.decode_uuid_v7(encoded)
    local payload = M.decode_bytes(encoded)
    assert_uuid_v7_bytes(payload)

    return bytes_to_uuid(payload)
end

local function safe_wrapper(name, callback)
    return function(...)
        local ok, result = pcall(callback, ...)

        if ok then
            return result
        end

        if core ~= nil and core.Warning ~= nil then
            core.Warning(string.format("crockford-base32-codec.lua %s failed: %s", name, result))
        end

        return nil
    end
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("crockford_b32_encode_bytes", safe_wrapper("encode_bytes", function(value)
        return M.encode_bytes(value or "")
    end))

    core.register_converters("crockford_b32_decode_bytes", safe_wrapper("decode_bytes", function(value)
        return M.decode_bytes(value or "")
    end))

    core.register_converters("crockford_b32_encode_string", safe_wrapper("encode_string", function(value)
        return M.encode_string(value or "")
    end))

    core.register_converters("crockford_b32_decode_string", safe_wrapper("decode_string", function(value)
        return M.decode_string(value or "")
    end))

    core.register_converters("crockford_b32_encode_int", safe_wrapper("encode_int", function(value)
        return M.encode_int(value or "0")
    end))

    core.register_converters("crockford_b32_decode_int", safe_wrapper("decode_int", function(value)
        return M.decode_int(value or "")
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
end

return M
