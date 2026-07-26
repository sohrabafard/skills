# chi Under Load

Read this whenever someone asks whether chi — or the kit — can carry a service's traffic, and whenever a task calls
for rate limiting, an in-flight cap, load shedding, or circuit breaking.

The short answer this file exists to make defensible: **the router is not what decides whether a service survives
load.** Admission control decides it, and admission control is a kit-owned surface that is partly present and partly
absent. This file separates the two, with the source each fact was read from.

All kit facts below were read from `alaa-go-chi` source on **2026-07-26**. Re-read them from source before relying on
one; a skill statement is not proof that the kit implements a feature.

## 1. What a chi service on the kit already has

| Capability | Where it lives | Where it is stated |
|---|---|---|
| All four `http.Server` bounds, from validated environment, clamped at boot | `httpkit/config.go` | `45-failure-behavior-at-the-call-site.md` section 4 |
| A request body cap enforced by the last middleware in the chain | `httpkit/middleware.go` | `45-failure-behavior-at-the-call-site.md` sections 4 and 5 |
| A fixed middleware chain — recover, correlation, span, access-log and metrics, body cap — that a service cannot reorder or partially adopt | `httpkit/middleware.go` | here |
| A family-first router that fails closed: a route that reaches the mux without a declared family is rejected with `ErrUnlabeledRoute` | `httpkit/route_inventory.go` | `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) P2 |
| One error-envelope mapper for the whole service | `errkit` | `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) P4 |
| Four-phase ordered shutdown with a fixed total budget | `runkit/lifecycle.go` | `45-failure-behavior-at-the-call-site.md` section 7 |
| Two separate Postgres lanes: a transaction-pooled application pool and a fixed two-connection admin pool, with a scale-tier selector | `pgkit/pool.go`, `pgkit/tier.go` | `/alaa-data-layer` (`$alaa-data-layer`) owns which lane and which tier |
| A Redis client with library retries disabled, a fixed short per-call timeout, a mandatory positive TTL on every write, a miss treated as a miss rather than an error, and readiness reported at degraded rather than required severity | `rediskit/config.go`, `rediskit/cache.go`, `rediskit/doc.go` | `61-redis-cache-layer.md` |
| Black-box conformance tests for the trust boundary, the error envelope, readiness, and the route inventory | `contracttest/` | `/alaa-go-chi-development` (`$alaa-go-chi-development`) |
| Five build-enforced analyzers, including one that forbids `LISTEN/NOTIFY`, `SET`, and `pg_advisory_lock` under transaction pooling | `linttools/`, exposed as `make lint-*` targets | `/alaa-go-chi-development` (`$alaa-go-chi-development`) |

That set is why the kit is the default. A service written outside it starts with none of it and maintains every piece
alone.

## 2. What the kit does not have

Verified absent from `alaa-go-chi` source on 2026-07-26. Each of these is a control a service under real load needs,
and **none of them exists in the kit today**:

- **Rate limiting** — no per-client, per-route, or global limiter.
- **An in-flight request cap** — nothing refuses a request because too many are already running.
- **Load shedding** — no policy that decides to reject rather than queue when saturated.
- **Circuit breaking** — nothing anywhere in the kit, including around Redis, Postgres, or the broker. `mqkit` has no
  retry or backoff in Go at all: a failed delivery is either requeued by the broker or dead-lettered with a receipt.
- **An ingress request deadline** — see `45-failure-behavior-at-the-call-site.md` section 1, including the change
  request that would add it and what it is blocked on.

`jobkit` does have real full-jitter exponential backoff. That is the only backoff implementation in the kit, it is
scoped to job execution, and it is not an admission control.

## 3. Two claims that look like evidence and are not

**`http_requests_in_flight` is a gauge, not a cap.** It is an observability signal declared in `obskit`. It reports
concurrency; it refuses nothing. **Forbidden:** citing its existence as evidence that the kit limits concurrency.

**The kit's `AGENTS.md` names "rate limits, circuit breakers" among its design goals.** That sentence describes intent.
No code implements it. **Forbidden:** quoting a goals, roadmap, or design-intent statement — in `AGENTS.md`,
`README.md`, a decision register, or a change request — as evidence that a capability exists. **Rule:** a capability
exists when you have found the code that implements it and can name the file.

## 4. Where each absence is taken

Every item in section 2 is a **kit-owned surface**: it belongs in the fixed middleware chain, in `httpkit.Config`, or
in the request context the chain builds. That ownership decides the route, and it is not negotiable by a service.

**Forbidden:** implementing a rate limiter, an in-flight cap, a shedder, a circuit breaker, or an ingress deadline
helper inside a service repository on the kit. Doing so forks a kit surface, gives the platform one copy per service,
and is exactly what P1 forbids.

**Rule:** when a service needs one of these, file a change request through `/alaa-go-chi-development`
(`$alaa-go-chi-development`), stating the control, the surface it belongs on, and the evidence that the service needs
it. That skill owns the intake, the decision record, and the active scope phase.

**Rule:** while a control is unfilled, the limits that do exist are at the edge, not in the service — routing, TLS
termination, connection limits, and edge rate limiting belong to `/alaa-haproxy` (`$alaa-haproxy`), and the doctrine
for what those limits should be belongs to `/alaa-reliability-sla` (`$alaa-reliability-sla`). Say plainly in your
report that the service-level control is absent and name the change request; do not let an edge limit be reported as
if the service had the control.

## 5. Fiber closes none of this

Fiber is a different HTTP engine. It changes how bytes become a request; it does not add a rate limiter's policy, an
in-flight budget, a shedding decision, a breaker's state machine, or a request deadline to an Ala service.

Every item in section 2 is architecture a service must have regardless of which router parses its requests. Moving to
Fiber would therefore leave the gap open **and** give up everything in section 1.

**Forbidden:** proposing Fiber as a response to a load, latency, or SLA concern. **Rule:** answer a load concern with
section 2 — name the missing control and the change request — and leave the framework where
`30-http-api-framework-choice.md` puts it.

## 6. What to do when asked "will this hold?"

**Rule:** answer with four statements, in this order, and no framework comparison:

1. Which bounds from section 1 the service already has, named from source.
2. Which controls from section 2 it lacks.
3. What evidence of behaviour under load exists — load test, capacity test, chaos or failover test, live SLO — and
   what does not. Use the evidence vocabulary in `alaa-go-chi-development` `references/05-phase-and-source-truth.md`
   and never let a lower tier stand in for a higher one; unit tests are not capacity evidence.
4. Which change request or which doctrine owner closes each gap.

**Forbidden:** answering the question with a throughput number, a benchmark, or a framework name.
