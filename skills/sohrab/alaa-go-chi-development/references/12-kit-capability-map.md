# Kit Capability Map

Navigation, not a second contract. Every symbol, flag, default, and bound below was read from kit source on
2026-07-26; re-verify against the live kit before you rely on one. Start from `CONTRACTS.md`, `docs/RUNBOOK.md`,
`docs/INDEX.md`, `docs/scaffold-cli-reference.md`, `go.mod`, the `Makefile`, and the package source.

Module identity is `git.alaatv.com/vk/alaa-go-chi`. For the current released state read `CHANGELOG.md`; this file
pins no version.

## Where decisions live (read before designing kit-owned behaviour)

This file names locations and states no decision's content, so that a new decision does not make it wrong.

- `docs/change-requests/` holds every change request, baseline proposal, and scope decision, named
  `YYYY-MM-DD-<slug>.md`. **Read newest first**, and read the whole batch for the surface you are touching.
- `docs/change-requests/2026-07-21-kit-bug-remediation-decision-register.md` is the aggregate register: ratified
  `Owner outcome` blocks D-01 through D-24, a `Consumer-tunable env surface` table of keys, defaults and clamps,
  and two owner-approved post-ratification review rounds dated 2026-07-23 that take precedence over the items
  they refine.
- Requests filed after that register are a **separate, newer channel** and have not been merged into it. As of
  2026-07-26 the newest batch is six requests dated 2026-07-25, every one `status: proposed`. Never treat a
  proposed request as decided, and never treat this paragraph as the current inventory — list the directory.
- **Ratified is not implemented.** Before stating that an env key, flag, or capability exists, find it in source.
  A consumer-binding value reaches consumer repositories only through the generated
  `docs/consumer-templates/{AGENTS.md,CLAUDE.md}`; landing it only at the kit root is governance drift.

## Routing — what the kit exposes versus who owns the doctrine

The kit owns the mechanism. The rules that mechanism must satisfy belong elsewhere; adopt the owner's vocabulary.

| Concern | Kit surface | Doctrine owner |
|---|---|---|
| Envelopes, readiness bodies, header names, `X-Access` wire encoding, deadlines, code and metric registries | `httpkit`, `errkit`, `readykit`, `trustkit`, `obskit` | `/alaa-services-contract` (`$alaa-services-contract`) |
| Retries, timeouts, breakers, shedding, degradation, error budgets, SLOs | `jobkit`, `mqkit`, `rediskit`, `runkit` | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Trusted headers, `TrustCtx`, tenancy | `trustkit` | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`); verdicts `/alaa-security-review` (`$alaa-security-review`) |
| TOTP step-up | `trustkit` | trust semantics `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`); contract shape `/alaa-services-contract` (`$alaa-services-contract`) `references/32-auth-totp-and-step-up-contract.md`; verdicts `/alaa-security-review` (`$alaa-security-review`) |
| Permission names and bitmap ids | the `servicePermissions` seam | `/alaa-permission-generator` (`$alaa-permission-generator`), catalog `alaa-permission-catalog` |
| Postgres, pooling lanes, migrations, Redis | `pgkit`, `rediskit` | `/alaa-data-layer` (`$alaa-data-layer`) |
| RabbitMQ, outbox, consumers, DLQ, idempotency | `mqkit`, `outboxkit`, `jobkit` | `/alaa-async-messaging` (`$alaa-async-messaging`) |
| Log, metric, trace and Sentry design; alert authoring | `obskit` | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Container, Kubernetes, Helm and Arvan mechanics; replica and autoscaling values | generated deploy templates | `/alaa-docker-production` (`$alaa-docker-production`), `/alaa-k8s-helm` (`$alaa-k8s-helm`), `/caas-arvan-kuber` (`$caas-arvan-kuber`) |
| GitLab pipelines | `cikit` | `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) |
| OpenAPI and Postman artifacts | `apicontractkit`(+`postman`) | `/alaa-postman-collections` (`$alaa-postman-collections`), `/golang-swagger` (`$golang-swagger`) |
| Shared local-runtime identity shared with the Laravel fleet | `scaffold/templates.go` output | `/service-runtime-kit-governance` (`$service-runtime-kit-governance`) |
| Documentation craft for anything you write here | — | `/alaa-repo-docs` (`$alaa-repo-docs`) |

## Packages — twenty-seven, and what each owns

Import these; never re-implement, re-prefix, or fork one. If a task looks like it needs one of these behaviours,
the answer is an import.

`configkit` boot config, env catalog, redaction, lane opt-out · `errkit` immutable typed errors, append-only
codes, one boundary mapping · `httpkit` hardened server, fixed middleware chain, strict binding, envelopes, route
inventory · `trustkit` `TrustCtx`, four route postures, permission bitmap, TOTP, gateway proof · `readykit`
liveness plus required/degraded/informational readiness and `ops ready --json` · `runkit` process roles,
lifecycle, ordered shutdown · `obskit` slog fields, OTel traces/metrics/exemplars, Sentry for panics and
programming faults only · `idkit` UUIDv7 and Crockford rendering · `audiencekit` canonical audience predicate ·
`filterkit` closed boot-compiled per-endpoint filter sets over flat query parameters, rendered to parameterized
Postgres and ClickHouse fragments · `mediakit` the platform media delivery payload contract · `pgkit` two-lane
Postgres, tiers, composed goose migrations, keyset and testdb helpers · `chkit` ClickHouse read-only analytical
lane · `rediskit` Redis transport, cache adapter, invalidation, degraded readiness · `mqkit` RabbitMQ transport,
confirming publisher, envelope, topology, consumer shell, receipts · `outboxkit` transactional outbox ·
`jobkit` Postgres job queue · `seedkit` idempotent seeders · `ctlopskit` ControlledOps kernel: durable state,
approval, TOTP, audit, execution fencing · `bulkkit` bounded itemized-mutation engine · `genkit` Tier-2
regeneration from `ops/ops.yaml` · `contracttest` black-box conformance assertions · `apicontractkit`(+`postman`)
API-contract merge, bidirectional coverage, Postman generation · `scaffold` the service generator and its
goldens · `cikit` generated GitLab phase jobs · `linttools` the custom analyzers · `refops` kit-local evidence ·
`ctlopskit`/`bulkkit` transports under their own subpackages.

Two facts a consumer must not get wrong:

- **`refops` is kit-internal evidence only.** Its own package doc states it is not a template for a consumer
  service and not a scaffolded artifact. Do not copy it, cite it as an example, or expect it in a generated tree.
- **`bulkkit`'s `Descriptor[Req, Item]` surface is marked EXPERIMENTAL** pending first real-consumer adoption.
  Say so whenever you propose building on it.

There is also a root-level `chaos/` failure-injection harness driven by `make chaos-harness`. It is kit-local
proof, not a consumer-facing package.

**Documentation coverage is uneven, and that is a fact to state rather than paper over.** Six packages have
task-oriented guides in `docs/`: `configkit`, `errkit`, `filterkit`, `httpkit`, `obskit`, `trustkit`. Most others
carry a package doc comment in `doc.go`. `apicontractkit` and `cikit` have neither; `linttools` and `scaffold`
have no `doc.go` either. For those, source and `CONTRACTS.md` are the only descriptions — read them, and mark any
claim you cannot ground `NEEDS_CONFIRMATION`.

## Service code owns

Domain entities, use cases, policies, repositories behind application ports, provider translation, domain
schemas, events and error codes, and composition of only the roles and capabilities the service actually uses.
Everything platform-shaped above is imported.

## CLI — `cmd/alaa-go-chi`

`docs/scaffold-cli-reference.md` is authoritative and itself warns that three `--help` descriptions are stale;
prefer the reference and source over `--help` output.

**`alaa-go-chi new service <name>`** — flags: `--parent-dir` (enforced as required at runtime, and `--help` does
not annotate it), `--module-path`, `--kit-module`, `--kit-version`, `--kit-replace`, `--goprivate`, `--tier`
(`direct|small|medium|large`, default `small`), `--no-git`, `--force`, `--without-postgres`, `--without-rabbitmq`.
`--force` overwrites scaffold-owned files in a non-empty target and warns when the target is a git repository
with history, pointing at `upgrade` instead. Normal generation pins a released kit and commits no local `replace`.

**`alaa-go-chi upgrade --dir <repo>`** — three ownership classes: kit-owned files are rewritten in place;
consumer seams are never overwritten and instead emit `<path>.kitnew` beside the file when the render differs;
and a skip set — including `go.mod`, `go.sum`, and `internal/genops/` — is never written, so the kit pin is bumped
by hand. Resolve every `.kitnew` before reporting an upgrade done.

**`alaa-go-chi gen`** — regenerates Tier-2 output from `ops/ops.yaml`. It refuses to run when the generator's own
kit version differs from the consumer's `go.mod` pin; that refusal is the diagnosis, not an obstacle. `--check`
regenerates to memory and diffs against the working tree without writing — the drift gate. Note that `gen`'s own
help text names a `make gen-check` target that does not exist in the kit `Makefile`; the drift target that does
exist is `tier2-drift`.

Other binaries under `cmd/`: `alaa-api-contract`, `alaa-lint`, `alaa-metricname-lint`, `alaa-structtag-lint`,
`alaa-uuid-lint`, `alaa-text-lint` (check/fix/staged), `alaa-obskit-render`.

## Verified runtime facts

**`httpkit` server bounds** come from validated env with boot-enforced clamps; the band is fixed in code and only
the value inside it is tunable. `HTTP_READ_TIMEOUT` default 10s, range [1s, 300s]; `HTTP_WRITE_TIMEOUT` 30s,
[1s, 900s]; `HTTP_IDLE_TIMEOUT` 120s, [1s, 1800s]; `HTTP_MAX_BODY_BYTES` 1 MiB, [1 KiB, 64 MiB]. An
out-of-band or unparsable value fails boot and names the offending key. `ReadHeaderTimeout` equals `ReadTimeout`
and is not separately configurable. `MaxHeaderBytes` is deliberately unset because `net/http` applies its own
1 MiB default.

**The middleware chain is fixed**, outermost first: recover → correlation → span → access-log/metrics →
body-cap. `httpkit.Bind[T]` enforces the JSON content type, wraps the body in `http.MaxBytesReader` at the
configured cap, calls `DisallowUnknownFields`, and rejects a second JSON document in the same body.
`AllowUnknownFields()` is a per-route option documented as scoped to ProviderFacing webhook dialects. The router
fails closed on a nil posture and refuses any route that reaches the mux without a declared family
(`ErrUnlabeledRoute`).

**Shutdown is owned by `runkit`** in four ordered phases — `stop_intake`, `drain_workers`, `flush_buffers`,
`close_pools` — each receiving a quarter of a total budget that is **hardcoded at 30s**.

**`pgkit` runs two lanes**: a pooled runtime pool sized by `PG_MAX_CONNS` (default 20) and a direct migrate pool
fixed at 2 connections, one of which is reserved for the advisory lock. Tier bands are selected by
`PG_SCALE_TIER` (`direct|small|medium|large`) and set PgBouncer usage, pool size, pooler replicas, max client
connections, and the Postgres slice. DDL and session operations use the direct admin lane.
`pgkit.ComposeMigrations` orders service and kit sources by owned version bands; never renumber or hand-merge.

**`rediskit` is deliberately unforgiving**: client retries are disabled outright (`MaxRetries = -1`), dial, read,
write and pool timeouts are all set to the call timeout (default 250 ms), a non-positive TTL is rejected, a miss
is a clean miss, and a failing Redis reports Degraded readiness. Redis is never truth.

**`jobkit` has full-jitter exponential backoff** bounded by a ceiling. **`mqkit` has no Go-level retry or
backoff.** No circuit breaker exists anywhere in the kit.

**`linttools` ships five analyzers**, wired to Make targets: `lint-metricnames`, `lint-structtags`,
`lint-no-genrandomuuid`, `lint-text`, and a pooled-lane analyzer (`lint-analysis`) that forbids `LISTEN/NOTIFY`,
`SET`, and `pg_advisory_lock` under transaction pooling.

**`.env.example` defines 52 keys.** Treat it, `configkit/keys.go`, and `CONTRACTS.md` as one set that must agree;
a key in one and not the others is a finding.

**Metric names are currently bare.** `obskit/metricnames.go` declares fifteen constants and not one carries an
`alaa_` prefix. A prefix is proposed and not ratified — do not write one, and do not describe the current names
as prefixed.

## Absent capabilities — say "absent", never "available"

The kit has **no rate limiting, no circuit breaking, no backpressure, no load shedding, no in-flight admission
cap, and no ingress request deadline.** `http_requests_in_flight` is an observability gauge, not admission
control. The kit's own `AGENTS.md` names rate limits and circuit breakers among its design goals; that is
aspiration, and restating it as capability is exactly the error this section exists to prevent. A service needing
any of them files a baseline proposal — see `20-` — and routes the design to `/alaa-reliability-sla`
(`$alaa-reliability-sla`).

## Ratified but not implemented, as of 2026-07-26

Verify each before quoting it; the point of the list is that ratification alone proves nothing.

- The **per-route body-cap override** does not exist in code, and the ceiling is still 64 MiB rather than the
  ratified 100 MiB.
- `SHUTDOWN_TIMEOUT` and `SHUTDOWN_GRACE_HINT` are ratified and absent from both `configkit` and `.env.example`;
  the shutdown budget is the hardcoded 30s above.
- `PG_ROLLBACK_TIMEOUT`, `MQ_PREFETCH`, `MQ_WORKER_HEALTH_PORT`, and the ratified `JOB_*` and `OUTBOX_*`
  additions (`JOB_EXECUTION_TIMEOUT`, `JOB_MAX_ATTEMPTS`, `JOB_BACKOFF_*`, `JOB_CIRCUIT_THRESHOLD`,
  `JOB_RETRYABLE_SQLSTATES`, `OUTBOX_PUBLISH_TIMEOUT`, `OUTBOX_MAX_CONCURRENCY`, `OUTBOX_MAX_ATTEMPTS`,
  `OUTBOX_BACKOFF_*`, `OUTBOX_METRICS_CADENCE`) are absent. What **does** exist today from those families is
  `OUTBOX_BATCH`, `OUTBOX_TICK`, and `JOB_LANES`.

## Open contradictions to name, not to resolve

- **400 versus 422 for validation.** `errkit.Validation()` returns 400 and `errkit.SemanticValidation()` returns
  422, and both render code `INPUT_VALIDATION_FAILED`. `CONTRACTS.md` shows 422 in its canonical example and 400
  in its strict-JSON sections, and the envelope permits both. There is an open request on this. Cite the
  contradiction, pick nothing, and do not encode either side into a new surface.
- **No maintainer or reviewer is assigned.** `.rules/500-merge-release-and-ownership.md` owns the roster and
  forbids inventing one. Do not write a workflow step that assumes a named approver exists; write "project owner"
  and say the roster is unassigned.
- **`BYPASS_GATEWAY_PROOF` defaults to `true`.** In bypass mode the loader neither resolves nor retains the proof
  header or secret, and the gateway-proof middleware skips validation entirely; setting it `false` restores
  constant-time proof validation and boot-time failure on incomplete proof configuration. The bypass is safe only
  where a gateway-only network boundary actually exists — and a generated NetworkPolicy is not evidence that it
  does. Therefore: **treat the bypass as unproven unless a decision record in the kit repo names the control that
  enforces the boundary, the party who verified it, and the date of verification.** Absent that record, report
  the boundary as `NEEDS_CONFIRMATION`. Any change to this key is a security-review trigger — route it to
  `/alaa-security-review` (`$alaa-security-review`) in the same change.

## Validation entry points — the one list

Kit `Makefile` targets, verified 2026-07-26: `test`, `test-fast`, `test-race`, `build`, `vet`, `contracttest`,
`api-contract`, `contracts-doc`, `governance-structure`, `gate-phase0`, `gate-phase1`, `gate-phase2` and their
`-manifest` variants, `docs-consumer-gates`, `lint-analysis`, `lint-structtags`, `lint-metricnames`,
`lint-no-genrandomuuid`, `lint-text`, `format-text`, `normalize-staged-text`, `tier2-drift`, `budget-guard`,
`pool-budget-guard`, `promtool-check-alerts`, `dashboard-alert-import`, `postgres-truth-tier`,
`redis-truth-tier`, `rabbitmq-truth-tier`, `seed-idempotency`, `migrate-updowup`, `chaos-harness`,
`totp-contract`, `precommit`, `install-hooks`, `verify-hooks`, `bootstrap-news`, `bootstrap-consumers`. Add
`go test ./...`, `go test -race ./...`, `go vet ./...`, vulnerability analysis, and `git diff --check` in
proportion to what the change touches. Which proof level each target reaches is in `05-`; no other file in this
skill repeats this list.
