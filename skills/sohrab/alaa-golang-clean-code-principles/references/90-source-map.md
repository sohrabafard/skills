# Source Map — Where These Principles Come From, and When to Re-Verify

Read this file when you are about to rely on a kit fact this skill states — identity types, pooling lanes,
metric names, provider idempotency, the scope phase, an analyzer or make target — or when a statement here
disagrees with what you see in a repository.

## Source priority

All paths below are relative to a repository root, not to any one machine. The kit repository is the Go module
`git.alaatv.com/vk/alaa-go-chi`; the service repository is whatever repo you are working in.

1. **The service repository** — its code, tests, `AGENTS.md`, `CLAUDE.md`, and migrations. Always wins for
   current behavior of that service.
2. **The kit repository, source first.** `CONTRACTS.md` (every code-enforced shape), `CONSTITUTION.md`,
   `GOVERNANCE.md`, `AGENTS.md`, `alaa-go-chi-framework.md`, `Makefile` (the real names of every gate),
   `docs/INDEX.md`, `docs/RUNBOOK.md`, `docs/CONSUMERS.md`, and `docs/change-requests/`. Wins for every
   kit-owned shape this skill cites.
3. **Kit code over kit documents when they disagree**, and treat *ratified* and *implemented* as different
   states. A decision register entry, a change request, or a `CONTRACTS.md` row can describe a value that no
   code reads yet. Confirm from source before claiming a key, metric, analyzer, or capability exists.
4. **The consumer design records** the principles were drawn from, in the kit repository's `docs/`:
   `news-service-go-architecture.md` and `notif-service-go-architecture.md`.
5. **This skill's origin document**, in the kit repository: `docs/alaa-golang-clean-code-principles.md`.
6. **Companion skills for their owned domains** — see `50-skill-boundaries.md` for the full ownership table.

**If you cannot reach the kit repository**, ask the user for its location or a copy, and mark every kit-derived
fact `[gap]` until you have it. Do not substitute memory, an example from this skill, or a plausible default.

## Facts most likely to rot

Each row names where the rule is stated in this skill and what to re-read before citing it.

| Fact | Re-read before citing |
|---|---|
| Identity types (`X-Project-Id` UUIDv7, `X-User-Id` int64) | `trustkit/` source and `CONTRACTS.md`; P3 in `10-kit-and-trust-boundary.md` |
| Pooling lanes (`PG_DSN` pooled, `PG_MIGRATE_DSN` direct) and the pooled-lane restrictions | `pgkit/` source, `linttools/pooledlane`; P6 in `20-domain-data-and-consistency.md` |
| Kit-owned metric names | `obskit/metricnames.go` (`KitMetricNames()`); P11 in `30-runtime-and-observability.md` |
| Kit-owned env keys | `configkit/keys.go` and `CONTRACTS.md`; P10 in `30-runtime-and-observability.md` |
| Analyzer and make-target names behind every proof line | the kit's `Makefile` and `linttools/` |
| Validation status for `INPUT_VALIDATION_FAILED` (400 vs 422) | `errkit/constructors.go` and `CONTRACTS.md`; the open question is recorded in P4 |
| Shutdown budget and phase interfaces | `runkit/lifecycle.go`; P9 in `30-runtime-and-observability.md` |
| Retry, backoff, deadline, and rate-limit capabilities | `jobkit/`, `mqkit/`, `rediskit/`, `httpkit/`; P7 in `20-domain-data-and-consistency.md` |
| Provider idempotency (Bale `request_id`, Mediana none) | `/alaa-bale-provider` (`$alaa-bale-provider`), `/alaa-sms-provider-mediana` (`$alaa-sms-provider-mediana`) |
| The active scope phase and the consumer roster | `docs/CONSUMERS.md`, `AGENTS.md`, `docs/change-requests/2026-07-14-kit-first-stabilization-scope.md` |

## Snapshot taken 2026-07-26 — a snapshot, not current truth

`KIT_FIRST_STABILIZATION` active. Consumers: `news` v1.6.1 active; `wa-api` v1.6.0 active and running **without
PostgreSQL or RabbitMQ**, on ClickHouse through `chkit`; `notif`, `entitlement-api`, and `tusd` paused. Re-read
`docs/CONSUMERS.md` before treating any of this as current — rows change without a change to this skill.

## Freshness triggers

Re-open the kit repository and update the affected reference file when any of these happens: a kit major
version; a change to the canonical envelope, envelope codec, or outbox DDL; a new readiness severity; a change
to trusted-header types; a new analyzer or make target that turns one of this skill's admitted gaps into a real
gate; a change request in `docs/change-requests/` moving from `proposed` to ratified *and implemented* on a
surface this skill cites; a new kit package absorbing a concern currently listed as service-local.

## Durable content — safe to trust without re-checking

The thirteen principles themselves: kit-first discipline, declared route posture, single-parse trust context,
errors-as-values, ports and adapters, transactional outbox, idempotency by construction, explicit wire shapes,
owned goroutines, boot-time config, bounded observability, boundary-true testing, contracts over reach-ins.
These are architectural invariants of this platform, not version-sensitive facts. Everything *quantitative* in
this skill — a status code, a timeout, a key name, a target name — is version-sensitive and belongs to the
table above.
