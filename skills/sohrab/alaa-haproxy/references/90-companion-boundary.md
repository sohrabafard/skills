# Companion Boundary

The boundary sentence for the caching and routing half is stated once, in `SKILL.md`, and is not
repeated here. This file is the full table.

## What `alaa-haproxy` owns

- How any routing, caching, TLS-termination, rate-limiting, load-balancing or drain decision is
  **expressed as an HAProxy directive**.
- The branch-and-version discipline for HAProxy itself: which branch a config targets, what
  `haproxy -vv` and `haproxy -c -f` prove, and what breaks across a branch change.
- The Runtime API surface and what each command answers.
- The `log-format` string that emits the fields another skill names.
- The mechanism of HAProxy's own subsystems — how `peers` replicates, what a stick table does at
  saturation, what the object cache will not store, what a soft stop does to a listener.

## What it does not own

| Decision | Owner | The condition under which that owner decides |
|---|---|---|
| Which `Cache-Control` value belongs to which response class; which paths are content-hashed; the frontend delivery gate register | `/alaa-frontend-devops` (`$alaa-frontend-devops`) | whenever a caching or asset-routing task arrives with no stated policy, because the policy follows from how the build names its files |
| Lua scripting in HAProxy: `lua-load`, `http-request lua.<name>`, Lua converters and sample fetches, Lua-backed SPOE, and the Lua implementation that 3.3 requires for email alerts | `/alaa-haproxy-lua` (`$alaa-haproxy-lua`) | the moment a task would add, review, debug or performance-tune any Lua that runs inside HAProxy |
| Log field names, the metric catalog, `OTEL_*` names and defaults, the host-port table, canonical shared-infra names | `/alaa-services-contract` (`$alaa-services-contract`) | whenever a name or a value crosses a service boundary |
| Whether a signal is required, what alerts on it, and why | `/alaa-observability-soc` (`$alaa-observability-soc`) | before adding, removing or gating on any metric, log field or trace |
| Timeout and retry **values**, backoff, circuit breaking, backpressure, degradation, fail-open doctrine | `/alaa-reliability-sla` (`$alaa-reliability-sla`) | whenever the question is what a number should be, or what should happen when a dependency cannot answer and the risk is availability |
| Threat classification, exposure severity, fail-closed doctrine, what may be logged | `/alaa-security-review` (`$alaa-security-review`) | whenever a change alters a trust boundary, an admin surface, or what a failure lets through |
| What a downstream may conclude from a header this proxy set | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) | whenever HAProxy is the component that establishes caller identity |
| Kubernetes workload, chart, probe-object and NetworkPolicy authorship | `/alaa-k8s-helm` (`$alaa-k8s-helm`) | whenever the artifact is a manifest or a chart rather than an HAProxy directive |
| The same, on Arvan CaaS, where the Kubernetes version is pinned | `/caas-arvan-kuber` (`$caas-arvan-kuber`) | whenever the target is Arvan CaaS |
| Image build, base image, user, capabilities, pull policy, digest pinning, Compose | `/alaa-docker-production` (`$alaa-docker-production`) | whenever the artifact is a Dockerfile or a Compose file |
| How any gate is expressed on a runner: the job graph, `rules:`, `needs:`, artifacts, runner images | `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) | whenever the artifact is provider pipeline YAML |
| Making a local invocation give the same verdict as the runner | `/alaa-makefile` (`$alaa-makefile`) | whenever a gate needs a local entry point |
| Change control, rollout proof strength, what evidence a canary step needs | `/alaa-controlled-ops` (`$alaa-controlled-ops`) | before a change with a blast radius larger than one proxy ships |
| Complexity budgets and structure choice | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) | whenever a lookup cost grows with tenants, routes or table entries |
| Designing the subsystem, including any requirement HAProxy cannot meet — a hard global quota, for example | `/alaa-system-design` (`$alaa-system-design`) | whenever the correct answer is that this is not a proxy problem |
| Which generator variable expresses a runtime value, when the config is generated rather than written | `/service-runtime-kit-governance` (`$service-runtime-kit-governance`) | whenever the config is emitted by the runtime kit |
| Test layering, doubles, flake control | `/alaa-testing-strategy` (`$alaa-testing-strategy`) | whenever a proxy behaviour needs a test rather than a config check |
| The quality bar these files are measured against | `/alaa-project-constitution` (`$alaa-project-constitution`), `references/quality-bar.md` | when reviewing this skill itself |
| Model and effort selection for any agent-facing artifact | `/alaa-prompting-guide` (`$alaa-prompting-guide`), `references/50-effort-and-thinking.md` | whenever an emitted artifact would otherwise carry a model or effort key |

## Lua, specifically

Lua is the boundary this skill was silent about, and silence read as authority. HAProxy Lua is
**not this skill's subject**. `/alaa-haproxy-lua` (`$alaa-haproxy-lua`) owns it.

What stays here: confirming from `haproxy -vv` that the running build has Lua at all, before any
Lua is written. What goes there: everything after that.

`/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) is a **helper within** Lua work,
not its owner. Pair it when HAProxy Lua needs Crockford Base32, UUIDv7 or another pure codec that
must match backend, frontend or CLI code — after `/alaa-haproxy-lua` (`$alaa-haproxy-lua`) has
been consulted about the Lua itself.
