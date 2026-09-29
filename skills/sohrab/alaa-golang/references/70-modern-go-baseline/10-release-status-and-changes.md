Version-sensitive claims in this topic depend on [Go version source ledger](../SOURCES.md).

## Verified releases and consumer applicability

Go **1.27.1** was the current stable patch verified on **2026-09-29** against
https://go.dev/doc/devel/release and https://go.dev/doc/go1.27. The retained 1.26 guidance below
was verified on **2026-07-26** against https://go.dev/doc/go1.26 and https://go.dev/ref/spec.
The kit's `go 1.26.5` directive was observed that day, not reverified for this refresh.

The consumer's `go.mod`, build tags, selected toolchain and CI remain authoritative for adoption.
A newer upstream release does not authorize changing a consumer directive or a private-kit phase.
Recheck `../SOURCES.md` before relying on version-sensitive guidance.
## Go 1.27 changes to assess

- Generic methods require the matching language version; interface methods still cannot declare type
  parameters. Use them only when they clarify an existing concrete-type API, not to replace simple ports.
- `go test` now enables the `stdversion` vet check. Fix newer-API use against the file's effective Go
  version; do not disable the check or raise the directive merely to silence it.
- `goroutineleak` profiling is stable; the `goroutineleakprofile` experiment flag is removed. Remove that
  flag on this toolchain. Keep profiler access private and do not treat an empty profile as proof of no leaks.
- `encoding/json/v2` and `encoding/json/jsontext` are stable. Keep existing wire semantics until an explicit
  migration tests duplicate keys, invalid UTF-8, field matching and error handling. `encoding/json` remains
  supported; its implementation changed, so avoid tests depending on exact decoder error strings.
- Removed `GODEBUG` compatibility toggles require an upgrade audit. Route TLS posture changes to
  `/alaa-security-review`; do not restore legacy crypto to make a test pass.
