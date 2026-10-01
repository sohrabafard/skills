# Sources

Use this file when a claim in this skill is version-sensitive, when a user asks for current behaviour, or when a fact here contradicts what the running binary reports.

## Source priority

1. **The running binary.** `haproxy -vv` and `haproxy -c -f <config>` beat every document, because the build decides which Lua version, which features, and which directives exist.
2. **The official manual for the branch actually deployed** — the configuration manual for `lua-load`, `lua-load-per-thread`, `tune.lua.*`, and the native sample fetches; `doc/lua-api/index.rst` for the API; `doc/lua.txt` for the architecture and the type-conversion table; `INSTALL` section 4.7 for the supported Lua versions.
3. **This skill's references**, which record what was read and when.
4. **Community answers**, only for concrete troubleshooting after the three above have been checked.

Branch status, release currency, and which branch is LTS are owned by `/alaa-haproxy` `references/SOURCES.md`. Do not restate a branch fact here; read it there.

## Re-check triggers

Re-verify before quoting when the task involves: the supported Lua version floor; the availability or version arguments of a native sample fetch such as `uuid`; a `tune.lua.*` default; the documented context list for an API call; or any behaviour on a branch other than the one recorded below.

## Primary locations

- HAProxy documentation index — https://docs.haproxy.org/
- Configuration manual, per branch — https://docs.haproxy.org/3.4/configuration.html and the matching path for the branch in use
- Lua architecture and first steps — https://www.haproxy.org/download/3.4/doc/lua.txt
- Lua API reference source — `doc/lua-api/index.rst` in the HAProxy source tree, rendered by HAProxy Technologies at https://www.haproxy.com/documentation/haproxy-lua-api/
- Build requirements for Lua — `INSTALL`, section 4.7, in the HAProxy source tree
- Lua language reference — https://www.lua.org/manual/5.4/

Read the target source and proof registers together before treating a claim as currently verified.

## Focused references

When re-deriving a version-sensitive pin, read [ordered binary inspection and source retrieval commands](./sources/10-pin-verification.md).

Before quoting a 3.4.6 source claim, read [the immutable archive identity, claim-to-source ledger and introduction/maintenance distinction](./sources/20-target-source-register.md).

When assessing what the target run proved, read [the exact build, gate results, repaired attempt and unrun proof limits](./sources/30-target-proof-register.md).

When consulting older captures or unresolved observations, read [dated source reads, old-build measurements and explicitly unverified claims](./sources/40-historical-evidence.md).
