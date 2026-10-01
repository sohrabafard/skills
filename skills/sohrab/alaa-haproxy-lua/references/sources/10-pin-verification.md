# Re-deriving a pin

Every version-sensitive value in this skill is pinned to a branch tag or to one local build. Each command below re-derives one class of pin without trusting this file. Run the first command before the others, because it names the tag the rest must use.

```
haproxy -v | head -1                                   # the branch actually installed
haproxy -vv | grep -E '\+LUA|Built with Lua version'    # Lua support and the interpreter version
```

```
TAG=v3.4.6    # replace with the tag matching the branch the first command reported
BASE=https://raw.githubusercontent.com/haproxy/haproxy/refs/tags/$TAG

curl -fsS $BASE/INSTALL              | grep -n -B2 -A8 'versions 5.3 and above'   # the Lua version floor
curl -fsS $BASE/doc/configuration.txt | grep -n -A6  'tune.lua.burst-timeout'      # every tune.lua.* default
curl -fsS $BASE/doc/configuration.txt | grep -n -A8  'lua-load-per-thread'         # the two load directives
curl -fsS $BASE/doc/configuration.txt | grep -n -A6  '^uuid('                      # uuid() and its version argument
curl -fsS $BASE/doc/lua.txt          | grep -n -A20 'Lua types'                    # the sample-type conversion table
curl -fsS $BASE/doc/lua-api/index.rst | grep -n -A6  'register_converters'         # a handler prototype and its contexts
```

To find which tags exist before choosing one:

```
curl -fsS https://api.github.com/repos/haproxy/haproxy/tags | grep -o '"name": "v[0-9.]*"' | head
```

Which of those branches is LTS, and whether the estate should move to another one, is owned by `/alaa-haproxy` `references/10-version-and-branch.md`. This file only tells you how to read the manual for a branch you have already chosen.

The local measurements in this file were taken on one build; re-derive that build's identity with `haproxy -vv | head -3` before comparing a number against your own.

For scope and related decisions, return to the [parent reference](../SOURCES.md).
