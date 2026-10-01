# Build and directive proof

## Confirming a directive exists before using it

A directive that exists in one branch may not exist in the branch that will run the config, and
the config file gives no hint either way. Two checks, in order:

1. `haproxy -vv` on the binary that will run it. It prints a `Feature list` of `+NAME`/`-NAME`
   tokens - `+QUIC`, `+KTLS`, `+PROMEX`, `+ZLIB`, `-LUA` and so on - and the TLS library it was
   built against. That list, not a document, is what says whether this build has QUIC, kTLS, Lua,
   tracing or the Prometheus exporter. `haproxy -v` alone also prints the branch's own support
   status, for example "long-term supported branch - will stop receiving fixes around Q2 2031",
   which is the fastest single check that a binary is on a branch worth deploying.
2. `haproxy -c -f <cfg>` on that same binary. This answers "does this directive exist in this
   branch, spelled this way, in this section". An unknown keyword is a fatal error naming the
   line and the section, so the check is conclusive.

**When the directive is absent**, the replacement is one of three things and never "leave it out
and hope": use the documented predecessor named in the branch manual for the branch you run; put
the whole block behind `.if version_atleast(<branch>)` so a mixed estate loads what it can (see
`20-core-config-and-timeouts.md`); or upgrade the binary. Choosing silently to omit the directive
is what turns a missing security control into a config that starts.

On 3.3 and later, `haproxy -vq`, `haproxy -vqs` and `haproxy -vqb` print the version, the status
and the branch as bare strings, which is what a script should parse instead of the `-v` banner.
