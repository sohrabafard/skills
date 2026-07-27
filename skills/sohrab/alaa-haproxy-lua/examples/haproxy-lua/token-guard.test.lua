-- token-guard.test.lua - unit test for token-guard.lua outside HAProxy.
--
-- Run it with the same Lua that HAProxy links, which `haproxy -vv` reports on
-- the line "Built with Lua version":
--     lua5.4 token-guard.test.lua
--
-- The test supplies a mock `core` object before loading the module, so the
-- module's registration branch runs and the test can assert what was
-- registered. No HAProxy process is involved and no network is touched.

local mock_core = {
    converters = {},
    fetches = {},
    logs = {},
}

function mock_core.register_converters(name, handler)
    mock_core.converters[name] = handler
end

function mock_core.register_fetches(name, handler)
    mock_core.fetches[name] = handler
end

function mock_core.log(level, message)
    mock_core.logs[#mock_core.logs + 1] = { level = level, message = message }
end

function mock_core.Warning(message)
    mock_core.log("warning", message)
end

function mock_core.Alert(message)
    mock_core.log("alert", message)
end

-- core is a global in HAProxy, so install it as a global here.
_G.core = mock_core

local here = arg[0]:match("^(.*[/\\])") or "./"
local guard = dofile(here .. "token-guard.lua")

local failures = 0
local checks = 0

local function check(name, ok, detail)
    checks = checks + 1
    if ok then
        print(string.format("ok   %s", name))
    else
        failures = failures + 1
        print(string.format("FAIL %s: %s", name, detail or "assertion failed"))
    end
end

-- 1. The module registered exactly the converter the configuration names.
check(
    "registers converter token_guard",
    type(mock_core.converters["token_guard"]) == "function",
    "converter was not registered"
)

-- 2. Accepted inputs. Each case is the whole contract for one input.
local accepted = {
    { name = "minimum length", token = "abcdefgh" },
    { name = "digits and letters", token = "01hq9mz7k3pv" },
    { name = "at the configured limit", token = string.rep("a", 32), limit = "32" },
}

for _, case in ipairs(accepted) do
    local ok, result = pcall(guard.validate, case.token, case.limit)
    check(
        "accepts " .. case.name,
        ok and result == case.token,
        tostring(result)
    )
end

-- 3. Rejected inputs. A converter's failure path is the half that decides
-- whether a forged value reaches the backend, so every rejection is a case.
local rejected = {
    { name = "empty string", token = "" },
    { name = "too short", token = "abc" },
    { name = "longer than the limit", token = string.rep("a", 200) },
    { name = "uppercase byte", token = "abcdefgH" },
    { name = "embedded newline", token = "abcdef\ngh" },
    { name = "embedded NUL", token = "abcdef\0gh" },
    { name = "non-string sample", token = 12345 },
    { name = "limit above the module maximum", token = "abcdefgh", limit = "9999" },
}

for _, case in ipairs(rejected) do
    local ok, message = pcall(guard.validate, case.token, case.limit)
    check("rejects " .. case.name, ok == false, "call succeeded and returned " .. tostring(message))

    if ok == false then
        -- error(message, 0) must be used, so the message must not begin with a
        -- "file.lua:12:" position prefix that would leak the deployed path into
        -- the HAProxy log.
        check(
            "rejection of " .. case.name .. " carries no source position",
            type(message) == "string" and message:match("^[^\n]-%.lua:%d+:") == nil,
            tostring(message)
        )
        -- The message must not echo the rejected value back into the log.
        if type(case.token) == "string" and #case.token > 0 then
            check(
                "rejection of " .. case.name .. " does not echo the token",
                message:find(case.token, 1, true) == nil,
                tostring(message)
            )
        end
    end
end

-- 4. Property: no accepted token contains a byte outside the allowlist. A
-- table-driven case set only covers the inputs someone thought of; this covers
-- the shape of the whole accepted set. The seed is fixed so a failure is
-- reproducible from the printed seed alone.
local SEED = 20260726
math.randomseed(SEED)

-- The pool is mostly in-alphabet, so a useful share of candidates is accepted.
-- Drawing uniformly from all 256 byte values would make the property vacuous:
-- nothing would be accepted and the assertion would hold for the wrong reason.
local POOL = "0123456789abcdefghijklmnopqrstuvwxyzA-_\n\0"

local property_violations = 0
local accepted_count = 0
for _ = 1, 5000 do
    local length = math.random(1, 40)
    local bytes = {}
    for index = 1, length do
        local pick = math.random(1, #POOL)
        bytes[index] = POOL:sub(pick, pick)
    end
    local candidate = table.concat(bytes)
    local ok, result = pcall(guard.validate, candidate)
    if ok then
        accepted_count = accepted_count + 1
        if #result < 8 or #result > 128 then
            property_violations = property_violations + 1
        end
        for index = 1, #result do
            local code = string.byte(result, index)
            local allowed = (code >= 48 and code <= 57) or (code >= 97 and code <= 122)
            if not allowed then
                property_violations = property_violations + 1
            end
        end
    end
end

check(
    string.format(
        "property: 5000 random inputs (seed %d), %d accepted, none out of alphabet",
        SEED,
        accepted_count
    ),
    property_violations == 0,
    string.format("%d violating bytes", property_violations)
)

-- A property that accepts nothing proves nothing, so the acceptance count is
-- itself an assertion.
check(
    "property case set is not vacuous",
    accepted_count >= 100,
    string.format("only %d of 5000 candidates were accepted", accepted_count)
)

print("")
print(string.format("%d of %d checks passed", checks - failures, checks))
os.exit(failures == 0 and 0 or 1)
