-- Pure lowercase Crockford Base32 codecs for bytes, integers, strings, and UUIDv7 values.
--
-- Wire format owner: skill `alaa-crockford-base32-codecs`,
-- `references/10-shared-codec-contract.md`. Change this file only together with the
-- PHP, JavaScript, and shell implementations, then run
-- `scripts/codec-conformance.sh` from that skill.
--
-- Runtime support: HAProxy supports only Lua 5.3 and above (HAProxy INSTALL, 4.7),
-- so LuaJIT is not a supported HAProxy target; check `haproxy -vv` before deploying.
-- This module additionally runs under a standalone 5.1 or 5.2 interpreter for
-- testing and CLI use. Every bit operation below is
-- written as arithmetic on values under 2^48 so the module parses and runs on
-- interpreters without the 5.3 bitwise operators.
--
-- HAProxy notes: the module registers converters and one fetch when the global `core`
-- object is present. Converters propagate errors instead of returning `nil`, so a
-- malformed input fails the sample rather than yielding an empty value. HAProxy
-- execution model, `lua-load` choice, and edge failure handling belong to
-- `/alaa-haproxy-lua` (`$alaa-haproxy-lua`), not to this file.

local M = {}

local ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
local LOOKUP = {}

for index = 1, #ALPHABET do
    LOOKUP[ALPHABET:sub(index, index)] = index - 1
end

local POW2 = {}

do
    local value = 1

    for index = 0, 48 do
        POW2[index] = value
        value = value * 2
    end
end

local function fail(message)
    -- Level 0 keeps the absolute source path and line number out of HAProxy logs.
    error(message, 0)
end

local function shift_right(value, bits)
    return math.floor(value / POW2[bits])
end

local function low_bits(value, bits)
    return value % POW2[bits]
end

local function normalize_encoded(value)
    local normalized = string.lower(value):gsub("%-", "")

    normalized = normalized:gsub("[il]", "1")
    normalized = normalized:gsub("o", "0")

    return normalized
end

-- UTF-8 validation follows RFC 3629: overlong forms, surrogate code points, and code
-- points above U+10FFFF are rejected, matching `TextDecoder(fatal)` and Python `str`.
local function is_valid_utf8(text)
    local index = 1
    local length = #text

    while index <= length do
        local first = text:byte(index)
        local following, lower, upper

        if first < 0x80 then
            following, lower, upper = 0, 0x80, 0xBF
        elseif first >= 0xC2 and first <= 0xDF then
            following, lower, upper = 1, 0x80, 0xBF
        elseif first == 0xE0 then
            following, lower, upper = 2, 0xA0, 0xBF
        elseif first >= 0xE1 and first <= 0xEC then
            following, lower, upper = 2, 0x80, 0xBF
        elseif first == 0xED then
            following, lower, upper = 2, 0x80, 0x9F
        elseif first >= 0xEE and first <= 0xEF then
            following, lower, upper = 2, 0x80, 0xBF
        elseif first == 0xF0 then
            following, lower, upper = 3, 0x90, 0xBF
        elseif first >= 0xF1 and first <= 0xF3 then
            following, lower, upper = 3, 0x80, 0xBF
        elseif first == 0xF4 then
            following, lower, upper = 3, 0x80, 0x8F
        else
            return false
        end

        if index + following > length then
            return false
        end

        for offset = 1, following do
            local continuation = text:byte(index + offset)
            local minimum = offset == 1 and lower or 0x80
            local maximum = offset == 1 and upper or 0xBF

            if continuation < minimum or continuation > maximum then
                return false
            end
        end

        index = index + following + 1
    end

    return true
end

local random_source = nil
local clock_source = nil
local seeded = false

local function seed_from_urandom()
    local handle = io.open("/dev/urandom", "rb")

    if handle == nil then
        return nil
    end

    local chunk = handle:read(6)
    handle:close()

    if chunk == nil or #chunk < 6 then
        return nil
    end

    local seed = 0

    for index = 1, #chunk do
        seed = (seed * 256) + chunk:byte(index)
    end

    return seed
end

local function seed_from_process_state()
    -- Table addresses vary per process under ASLR, which separates states that would
    -- otherwise share a one-second `os.time()` seed.
    local address = tostring({})
    local mixed = 0

    for index = 1, #address do
        mixed = ((mixed * 31) + address:byte(index)) % 1000000007
    end

    return (os.time() * 1000) + mixed
end

local function ensure_seeded()
    if seeded then
        return
    end

    math.randomseed(seed_from_urandom() or seed_from_process_state())
    math.random()
    math.random()
    math.random()
    seeded = true
end

local function random_byte()
    if random_source ~= nil then
        return math.floor(random_source()) % 256
    end

    ensure_seeded()

    return math.random(0, 255)
end

--- Replace the random byte source, which the conformance harness uses for determinism.
-- @param source function returning one integer in the range 0..255, or nil to restore
--   the module default.
function M.set_random_source(source)
    random_source = source
end

--- Replace the millisecond clock, which the conformance harness uses for determinism.
-- @param source function returning milliseconds since the Unix epoch, or nil to
--   restore the module default.
function M.set_clock(source)
    clock_source = source
end

--- Report the timestamp source that `generate_uuid_v7` will use.
-- @return string one of "injected", "core.now", or "os.time".
function M.clock_source_name()
    if clock_source ~= nil then
        return "injected"
    end

    if core ~= nil and core.now ~= nil and pcall(core.now) then
        return "core.now"
    end

    return "os.time"
end

local function now_milliseconds()
    if clock_source ~= nil then
        return math.floor(clock_source())
    end

    -- `core.now()` is documented for body, init, task, and action context. The UUIDv7
    -- fetch runs in sample-fetch context, so the call is guarded and falls back to
    -- `os.time()` at one-second resolution when it is unavailable.
    if core ~= nil and core.now ~= nil then
        local ok, snapshot = pcall(core.now)

        if ok and type(snapshot) == "table" and type(snapshot.sec) == "number" then
            return (snapshot.sec * 1000) + math.floor((snapshot.usec or 0) / 1000)
        end
    end

    return os.time() * 1000
end

local last_milliseconds = -1
local sequence = 0

-- RFC 9562 section 6.2 method 1: a 12-bit counter in `rand_a` keeps identifiers from
-- one process strictly increasing even when the clock resolution is coarse.
local function next_timestamp_and_sequence()
    local milliseconds = now_milliseconds()

    if milliseconds > last_milliseconds then
        last_milliseconds = milliseconds
        sequence = (random_byte() * 8) + shift_right(random_byte(), 5)

        return milliseconds, sequence
    end

    sequence = sequence + 1

    if sequence > 4095 then
        last_milliseconds = last_milliseconds + 1
        sequence = 0
    end

    return last_milliseconds, sequence
end

local function trim_leading_decimal_zeros(value)
    local trimmed = value:gsub("^0+", "")

    if trimmed == "" then
        return "0"
    end

    return trimmed
end

local function normalize_integer_input(value)
    local text

    if type(value) == "number" then
        if value ~= value or value == math.huge or value == -math.huge or value ~= math.floor(value) then
            fail("Integer input must be a canonical base-10 integer.")
        end

        text = string.format("%.0f", value)
    elseif type(value) == "string" then
        text = value
    else
        fail("Integer input must be a canonical base-10 integer.")
    end

    if not text:match("^%-?%d+$") then
        fail("Integer input must be a canonical base-10 integer.")
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
        fail("Integer payload cannot be empty.")
    end

    local negative = encoded:sub(1, 1) == "-"
    local magnitude = negative and encoded:sub(2) or encoded
    magnitude = normalize_encoded(magnitude)

    if magnitude == "" then
        fail("Integer payload cannot be empty.")
    end

    if #magnitude > 1 and magnitude:sub(1, 1) == "0" then
        fail("Integer payload must use a minimal Crockford Base32 representation.")
    end

    return negative, magnitude
end

local function decode_unsigned_base32_to_decimal(encoded)
    local decimal = "0"

    for index = 1, #encoded do
        local character = encoded:sub(index, index)
        local value = LOOKUP[character]

        if value == nil then
            fail(string.format("Invalid Crockford Base32 integer character [%s].", character))
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

    if not normalized:match("^%x%x%x%x%x%x%x%x%-%x%x%x%x%-%x%x%x%x%-%x%x%x%x%-%x%x%x%x%x%x%x%x%x%x%x%x$") then
        fail("UUID must be in canonical 8-4-4-4-12 hexadecimal form.")
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
        fail("UUID payload must contain exactly 16 bytes.")
    end

    local version = shift_right(string.byte(bytes, 7), 4)
    local variant_byte = string.byte(bytes, 9)
    local variant = variant_byte - low_bits(variant_byte, 6)

    if version ~= 7 then
        fail("UUID payload must be version 7.")
    end

    if variant ~= 0x80 then
        fail("UUID payload must use the RFC 4122 variant bits.")
    end
end

--- Encode raw bytes as lowercase Crockford Base32 without padding.
function M.encode_bytes(bytes)
    if bytes == "" then
        return ""
    end

    local buffer = 0
    local bit_count = 0
    local parts = {}

    for index = 1, #bytes do
        buffer = (buffer * 256) + string.byte(bytes, index)
        bit_count = bit_count + 8

        while bit_count >= 5 do
            bit_count = bit_count - 5
            local value = low_bits(shift_right(buffer, bit_count), 5)
            parts[#parts + 1] = ALPHABET:sub(value + 1, value + 1)
            buffer = low_bits(buffer, bit_count)
        end
    end

    if bit_count > 0 then
        local value = low_bits(buffer * POW2[5 - bit_count], 5)
        parts[#parts + 1] = ALPHABET:sub(value + 1, value + 1)
    end

    return table.concat(parts)
end

--- Decode lowercase or alias-normalized Crockford Base32 into raw bytes.
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
            fail(string.format("Invalid Crockford Base32 character [%s].", character))
        end

        buffer = (buffer * 32) + value
        bit_count = bit_count + 5

        while bit_count >= 8 do
            bit_count = bit_count - 8
            parts[#parts + 1] = string.char(low_bits(shift_right(buffer, bit_count), 8))
            buffer = low_bits(buffer, bit_count)
        end
    end

    if bit_count > 0 and buffer ~= 0 then
        fail("Invalid Crockford Base32 payload padding bits.")
    end

    return table.concat(parts)
end

--- Encode one signed integer as sign plus minimal unsigned Crockford Base32 digits.
function M.encode_int(value)
    local negative, magnitude = normalize_integer_input(value)
    local encoded = encode_unsigned_decimal_to_base32(magnitude)

    if negative and encoded ~= "0" then
        return "-" .. encoded
    end

    return encoded
end

--- Decode one signed Crockford Base32 integer into canonical base-10 text.
function M.decode_int(encoded)
    local negative, magnitude = split_signed_encoded_integer(encoded)
    local decimal = decode_unsigned_base32_to_decimal(magnitude)

    if negative and decimal ~= "0" then
        return "-" .. decimal
    end

    return decimal
end

--- Encode one UTF-8 byte string as lowercase Crockford Base32.
function M.encode_string(value)
    if not is_valid_utf8(value) then
        fail("Text input is not valid UTF-8.")
    end

    return M.encode_bytes(value)
end

--- Decode one Crockford Base32 payload back into a UTF-8 byte string.
function M.decode_string(encoded)
    local decoded = M.decode_bytes(encoded)

    if not is_valid_utf8(decoded) then
        fail("Decoded payload is not valid UTF-8.")
    end

    return decoded
end

--- Generate one canonical UUIDv7 string for correlation use.
function M.generate_uuid_v7()
    local milliseconds, counter = next_timestamp_and_sequence()
    local parts = {}
    local remaining = milliseconds

    for index = 6, 1, -1 do
        parts[index] = string.char(low_bits(remaining, 8))
        remaining = shift_right(remaining, 8)
    end

    parts[7] = string.char(0x70 + shift_right(counter, 8))
    parts[8] = string.char(low_bits(counter, 8))
    parts[9] = string.char(0x80 + low_bits(random_byte(), 6))

    for index = 10, 16 do
        parts[index] = string.char(random_byte())
    end

    return bytes_to_uuid(table.concat(parts))
end

--- Encode one canonical UUIDv7 string as lowercase Crockford Base32.
function M.encode_uuid_v7(uuid)
    local bytes = uuid_to_bytes(uuid)
    assert_uuid_v7_bytes(bytes)

    return M.encode_bytes(bytes)
end

--- Decode one Crockford Base32 UUID payload back into canonical UUIDv7 text.
function M.decode_uuid_v7(encoded)
    local payload = M.decode_bytes(encoded)
    assert_uuid_v7_bytes(payload)

    return bytes_to_uuid(payload)
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("crockford_b32_encode_bytes", function(value)
        return M.encode_bytes(value or "")
    end)

    core.register_converters("crockford_b32_decode_bytes", function(value)
        return M.decode_bytes(value or "")
    end)

    core.register_converters("crockford_b32_encode_string", function(value)
        return M.encode_string(value or "")
    end)

    core.register_converters("crockford_b32_decode_string", function(value)
        return M.decode_string(value or "")
    end)

    core.register_converters("crockford_b32_encode_int", function(value)
        return M.encode_int(value or "0")
    end)

    core.register_converters("crockford_b32_decode_int", function(value)
        return M.decode_int(value or "")
    end)

    core.register_converters("crockford_b32_encode_uuidv7", function(value)
        return M.encode_uuid_v7(value or "")
    end)

    core.register_converters("crockford_b32_decode_uuidv7", function(value)
        return M.decode_uuid_v7(value or "")
    end)
end

if core ~= nil and core.register_fetches ~= nil then
    core.register_fetches("crockford_b32_uuidv7", function()
        return M.generate_uuid_v7()
    end)
end

return M
