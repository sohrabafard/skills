# Topic Map

Load the one file whose condition matches the task in front of you. Every row states a situation you can observe, not a subject heading.

## Inside this skill

| You are about to | Read |
|---|---|
| choose between `lua-load` and `lua-load-per-thread`, or explain why a Lua handler slowed other traffic down | `references/10-execution-model.md` |
| look for the call that reads a header, sets a variable, writes a log line, opens a socket, or drives an applet | `references/20-api-surface.md` |
| write or review an action or a service, open a socket from a handler, call another service from the request path, or explain why a handler that failed did not reject the request | `references/25-actions-services-and-subrequests.md` |
| write or review a converter or a sample fetch, decide what its failure returns, or explain why a rejected value still reached the backend | `references/30-failure-visibility.md` |
| take a timestamp, generate a random value, or produce an identifier that must not repeat | `references/40-time-randomness-identity.md` |
| write a test for a Lua module, choose a runner, or decide what proof a change needs before it ships | `references/50-testing.md` |
| decide the shape of a new module, or review one for structure, naming, state, and testability | `references/60-clean-code-and-patterns.md` |
| judge whether a handler is fast enough, size its allocation cost, or decide whether Lua is the wrong tool for this job | `references/70-performance.md` |
| handle a value that arrived from the network, or review a module that touches one | `references/80-security.md` |
| reload, restart, drain, or observe a process whose Lua state matters | `references/90-operations.md` |
| quote a version-sensitive fact, or re-check a claim in this skill against its origin | `references/SOURCES.md` |

Converters and sample fetches are the only handler types whose return value HAProxy reads, and every rule that follows from that lives in `references/30-failure-visibility.md`. A module that registers none of them does not need that file; a module that registers one cannot be reviewed without it.

## Worked example

`examples/haproxy-lua/token-guard.lua` is a complete correct converter, `examples/haproxy-lua/token-guard.test.lua` is its test with a mock `core` object, and `examples/haproxy-lua/token-guard.cfg` is the smallest configuration that loads it and fails closed. Copy that shape when starting a new converter instead of writing one from the descriptions in these references. For an action or a service, copy the shape in `references/25-actions-services-and-subrequests.md` instead, because a converter's failure contract does not transfer to them.

The checker's fixtures under `test/fixtures/` are also readable examples: each red fixture is the smallest module that violates exactly one rule, and `green-clean-module.lua` is the smallest module that violates none.

## Out of this skill

| You are about to | Use |
|---|---|
| write, change, or review an HAProxy directive, TLS, QUIC, stick tables, maps, peers, branch policy, or container and Kubernetes delivery | `/alaa-haproxy` (`$alaa-haproxy`) |
| encode or decode Crockford Base32, or match a UUIDv7 representation across runtimes | `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) |
| name a header, field, wire format, error code, telemetry field, or activation gate, or take the Ala value of a timeout, retry budget, or failure code | `/alaa-services-contract` (`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md` |
| decide whether a change needs a security review, classify a threat, or apply the fail-closed doctrine to a security decision | `/alaa-security-review` (`$alaa-security-review`) |
| decide whether a header arriving at the gateway may be trusted, or where the trust boundary of an authorization sidecar sits | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| state the bound of work inside a handler that runs on every request, or catch a per-item call inside one | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) `references/10-complexity-budget.md` |
| decide why a timeout, retry, or degradation mechanism exists and what shape it takes | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| decide what makes a test a test, which layer a behaviour belongs at, or which proof level a claim reached | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| decide whether telemetry is required for a change, or which gate it must pass | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| check work against the ten-point quality bar | `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md` |
| choose a model or an effort level | `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` |
| plan multi-agent work across lanes | `/alaa-cc-orchestrator` (`$alaa-cc-orchestrator`), or `/alaa-codex-orchestrator` (`$alaa-codex-orchestrator`) in Codex |
