-- Green fixture: the action shape this fleet's gateway actually uses. It registers
-- an action and no converter, drives a subrequest over the yieldable Socket class,
-- uses the idiomatic "return nil, err" pair in its internal helpers, and wraps a
-- fallible call in pcall. None of that is a finding, because HAProxy reads no return
-- value back from an action. A checker that reports HL004 or HL009 here is the
-- false-positive class this fixture exists to hold shut.
-- Requires Lua 5.3 or newer.
local M = {}

local CONNECT_TIMEOUT = 0.5
local READ_TIMEOUT = 1.5

local function read_status_line(socket)
    local line, err = socket:receive("*l")
    if line == nil then
        return nil, err or "read_failed"
    end
    return tostring(line), nil
end

local function subrequest(host, port, path)
    local socket = core.tcp()
    socket:settimeout(CONNECT_TIMEOUT)

    local connected, connect_err = socket:connect(host, port)
    if not connected then
        socket:close()
        return nil, connect_err or "connect_failed"
    end

    socket:settimeout(READ_TIMEOUT)

    local request = "HEAD " .. path .. " HTTP/1.1\r\nHost: " .. host .. "\r\nConnection: close\r\n\r\n"
    local sent, send_err = socket:send(request)
    if not sent then
        socket:close()
        return nil, send_err or "send_failed"
    end

    local status_line, status_err = read_status_line(socket)
    socket:close()
    if status_line == nil then
        return nil, status_err or "status_line_failed"
    end

    local status = tonumber(status_line:match("^HTTP/%d+%.%d+%s+(%d%d%d)"))
    if status == nil then
        return nil, "invalid_status_line"
    end

    return status, nil
end

function M.enforce(txn)
    local ok, fetched = pcall(function()
        return txn.sf:path()
    end)
    local path = "/"
    if ok and type(fetched) == "string" then
        path = fetched
    end

    local status, err = subrequest("127.0.0.1", 18091, path)
    if status == nil then
        txn:set_var("txn.authz_status", 503)
        txn:set_var("txn.authz_reason", err)
        return
    end

    txn:set_var("txn.authz_status", status)
end

if core ~= nil and core.register_action ~= nil then
    core.register_action("enforce", { "http-req" }, M.enforce)
end

return M
