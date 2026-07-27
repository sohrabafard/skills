# Topic Map

Load the one file whose condition matches the task in front of you. Every row states a situation you can observe, not a subject heading.

## Inside this skill

| You are about to | Read |
|---|---|
| choose between `lua-load` and `lua-load-per-thread`, or explain why a Lua handler slowed other traffic down | `references/10-execution-model.md` |
| look for the call that reads a header, sets a variable, writes a log line, opens a socket, or drives an applet | `references/20-api-surface.md` |
| write or review the failure path of a converter, sample fetch, or action, or explain why a rejected value still reached the backend | `references/30-failure-visibility.md` |
| take a timestamp, generate a random value, or produce an identifier that must not repeat | `references/40-time-randomness-identity.md` |
| write a test for a Lua module, choose a runner, or decide what proof a change needs before it ships | `references/50-testing.md` |
| decide the shape of a new module, or review one for structure, naming, state, and testability | `references/60-clean-code-and-patterns.md` |
| judge whether a handler is fast enough, size its allocation cost, or decide whether Lua is the wrong tool for this job | `references/70-performance.md` |
| handle a value that arrived from the network, or review a module that touches one | `references/80-security.md` |
| reload, restart, drain, or observe a process whose Lua state matters | `references/90-operations.md` |
| quote a version-sensitive fact, or re-check a claim in this skill against its origin | `references/SOURCES.md` |

## Worked example

`examples/haproxy-lua/token-guard.lua` is a complete correct module, `examples/haproxy-lua/token-guard.test.lua` is its test with a mock `core` object, and `examples/haproxy-lua/token-guard.cfg` is the smallest configuration that loads it and fails closed. Copy that shape when starting a new module instead of writing one from the descriptions in these references.

## Out of this skill

| You are about to | Use |
|---|---|
| write, change, or review an HAProxy directive, TLS, QUIC, stick tables, maps, peers, branch policy, or container and Kubernetes delivery | `/alaa-haproxy` (`$alaa-haproxy`) |
| encode or decode Crockford Base32, or match a UUIDv7 representation across runtimes | `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) |
| name a header, field, wire format, error code, telemetry field, or activation gate | `/alaa-services-contract` (`$alaa-services-contract`) |
| decide whether a change needs a security review, classify a threat, or apply the fail-closed doctrine | `/alaa-security-review` (`$alaa-security-review`) |
| decide whether a header arriving at the gateway may be trusted | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| decide what makes a test a test, which layer a behaviour belongs at, or which proof level a claim reached | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| decide whether telemetry is required for a change, or which gate it must pass | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| shape a timeout, retry, or degradation policy | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| check work against the ten-point quality bar | `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md` |
| choose a model or an effort level | `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` |
| plan multi-agent work across lanes | `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) |
