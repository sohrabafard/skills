# Tracing components and ownership

## Tracing

3.3 adds `acme` and `ssl` trace sources. For the separate experimental
OpenTelemetry component, actual-build requirements and OpenTracing migration,
read `15-capabilities-3.4.md` and `10-version-and-branch.md`.

Runtime tracing is expensive and it reads request content. Turn it on for a bounded investigation
with a stated end, and turn it off when that investigation ends — not "after the incident", which
is not an observable condition. The mechanical form of bounded is to write the disable command
into the incident record at the same moment you write the enable command.

Whether tracing is required, and what the trace fields are called, is decided by
`/alaa-observability-soc` and `/alaa-services-contract`.
