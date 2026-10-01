-- Execute the plain unit test in an isolated environment in HAProxy's interpreter.
local env = setmetatable({}, {__index = _G})
env._G = env
env.arg = {[0] = "/pkg/examples/haproxy-lua/token-guard.test.lua"}
env.os = setmetatable({exit = function(code) assert(code == 0, "unit failures") end}, {__index = os})
env.dofile = function(path) return assert(loadfile(path, "t", env))() end
env.dofile(env.arg[0])
