# Mode C — Consumer Development on alaa-go-chi

You are implementing, extending, or migrating a service that consumes the kit. Your service owns **only its
domain**; everything platform-shaped comes from the kit. This file tells you how to stay inside that line and
what to do when the line pinches.

## 0. Session preconditions (do these before writing code)

1. Load `/alaa-golang` and `/alaa-golang-clean-code-principles`. All Go you write in this session is judged
   against P1–P13; if you cannot load them, apply the P1–P13 fallback table in the repo `CLAUDE.md` and report
   the missing skill as a blocker.
2. Read the service's architecture document (news Rev 4+, notif Rev 6+, or the migration note for
   entitlement/tusd) and the kit's `CONTRACTS.md` sections your task touches. Repo truth outranks both.
3. Check `docs/CONSUMERS.md` in the kit repo. If your service has no row — or the file does not exist — register
   it now per `references/50-consumer-registry.md`. This is the **only** write a consumer agent ever makes in
   the kit repository.
4. Pin the kit: the service's `go.mod` requires `git.alaatv.com/vk/alaa-go-chi` at a specific minor version.
   Never `replace`-direct it to a local checkout in committed code; a local `replace` during debugging must be
   removed before the task is reported done.
5. Wire this skill into the repo so future sessions cannot miss it: the consumer repo must have `CLAUDE.md` and
   `AGENTS.md` at its root naming `alaa-go-chi-development` (alongside `alaa-golang` and
   `alaa-golang-clean-code-principles`) as mandatory. The kit ships the canonical pair in
   `docs/consumer-templates/` — install those (substituting `<service>`) rather than writing your own; scaffold
   emission of the pair is tracked in the kit's
   `docs/change-requests/2026-07-08-scaffold-emit-agent-instruction-files.md`. The governance layer only works if
   every consumer session actually loads it.

## 1. What is kit-owned (never re-implement, never fork)

If your task seems to need any of these behaviors, the answer is an import, not an implementation:

- success/error envelopes; JSON binding (`httpkit.Bind[T]`), strict-JSON rules, body caps
- the middleware chain and its order; correlation headers; panic recovery
- route families (`Trusted` / `Anonymous` / `ProviderFacing` / `Operational`)
- trusted-header parsing, `TrustCtx`, permission-bitmap decode, `RequirePermission`, `RequireTOTP`,
  gateway-proof middleware
- health/readiness envelopes and severities (`required` / `degraded` / `informational`)
- metric names, log field vocabulary, OTel/Sentry wiring
- Postgres pool construction, the two-lane DSN contract (`PG_DSN` pooled / `PG_MIGRATE_DSN` direct),
  `PG_SCALE_TIER` bands, goose runner, testdb helpers, budget guards
- MQ envelope codec, confirming publisher, consumer shell, `command_receipts` DDL, topology declaration
- canonical outbox DDL + relay; job queue (`jobkit`); seeders (`seedkit`); UUIDv7 (`idkit`);
  audience predicate (`audiencekit`); env-key catalog; `contracttest`; scaffold, CI and deploy templates

A quick self-test that catches most violations: **if the code you are about to write would look identical in a
second Ala service, stop — it belongs in the kit** (file a baseline proposal, `references/20-*`).

## 2. The decision tree for every new piece of logic

```
Is this behavior already in the kit?
├─ yes → import it. If its API doesn't fit, do NOT copy/patch:
│         ├─ small mismatch → write a thin local wrap (adapter around the kit call,
│         │   no behavior fork), add a `// KIT-WRAP(<date>): <reason>` comment,
│         │   and file a change request the same day. Max lifetime: two kit releases.
│         └─ real gap or bug → file a change request (references/20) and either
│             wait, or wrap as above if the task cannot wait.
├─ no, but ≥2 consumers could plausibly need it → baseline proposal FIRST
│   (references/20). Implement it in your service only as a clearly-bounded
│   temporary wrap if the schedule demands, marked KIT-WRAP the same way.
└─ no, genuinely domain-specific → implement it in your service, in the layer
    P5 dictates (domain/application/infrastructure), per the clean-code skill.
```

"Plausibly shared" errs toward the kit. The Redis story shows the split precisely, and it is instructive because
it moved: the generic Redis *transport* (client, cache-aside adapter, version-key invalidator, degraded readiness)
was identical across services, so it became kit-owned — `rediskit` (framework §12 decision 6, resolved 2026-07-18).
Import it; do not re-implement a go-redis client or cache adapter. Only the Redis *domain shapes* that were proven
genuinely different (news's corpus cache with its visibility predicate, notif's rate-limiter bucket) stay
service-local — the transport is kit, the shape is yours. That is the general test: abstract the mechanics both
services share, keep the domain policy each owns. If you keep something local, write the one-paragraph
justification in your service's `docs/DECISIONS.md`; an auditor will look for it.

## 3. Building a new consumer (news, notif, future services)

1. Generate with the scaffold: `alaa-go-chi new service <name> --parent-dir <path>` — never hand-copy another
   service's tree. The scaffold output (docs skeleton, Dockerfile, Helm/Compose, CI baseline, contracttest job)
   is part of the contract; keep it, fill the TODOs.
2. Register the service (§0.3) with status `bootstrapping`.
3. Wire only the subcommands you use (`serve|consume|dispatch|relay|migrate|seed|topology|ops`).
   - **Datastore-free services are first-class** (a read-only API over ClickHouse or an external API, kit v0.4.0+):
     do not ship placeholder `PG_DSN`/`RABBITMQ_URL` values. Declare the absent lanes —
     `configkit.Load(ctx, configkit.WithoutPostgres(), configkit.WithoutRabbitMQ())` boots with no PG/MQ keys and
     fails loudly if one is set anyway — and pass the matching `contracttest.DocSurfaces{WithoutPostgres: true,
     WithoutRabbitMQ: true, WithoutScaffoldRoutes: true}` to `AssertDocsPresent` so the docs gate asserts only the
     core contracts (envelopes, readiness, correlation, kit metric/event vocabulary) a datastore-free service can
     truthfully make. See `CONTRACTS.md` → Environment Keys.
4. Domain implementation follows the service's architecture doc; every contract question resolves against
   `CONTRACTS.md`, not memory.
5. CI must run the kit-shipped gates from day one: `contracttest`, migration up-down-up, seeder idempotency,
   struct-tag lint, metric-name lint, permission-map drift, `golangci-lint`, `govulncheck`, `go test -race`.
   While the platform has no assigned GitLab runners, the accepted proof is the local runnerless path
   (`/alaa-local-ci-smoke` where installed): report `local_ci_smoke_passed; runner_contract_pending` — never
   claim remote CI green.
6. Update the registry row to `active` once contracttest passes.

## 4. Migrating an existing service (entitlement-api, tusd)

Migration is a behavior-preserving refactor, so it is stricter than greenfield:

1. **Inventory first.** Before changing anything, produce a timestamped inventory doc in the migrating repo
   (`docs/kit-adoption/YYYY-MM-DD-<service>-kit-adoption-inventory.md`): every surface the service currently
   hand-rolls that the kit owns (envelopes, readiness, pooling, outbox, …), mapped to the kit package that
   replaces it, plus every behavior that has **no** kit equivalent. For entitlement-api, start from the existing
   `2026-07-05-entitlement-platform-kit-adoption.md` in the kit's docs — entitlement is both the donor of the
   pooling model and a consumer of it.
2. Register the service with status `migrating`.
3. Replace surface by surface, one reviewable change each, in this order: config/env → envelopes+middleware →
   readiness → pgkit lanes → mq/outbox/jobs → observability. After each surface, the service's own tests plus
   `contracttest` (for the surfaces already migrated) must pass.
4. Gaps discovered during migration are the richest source of kit improvements — each becomes a change request
   or baseline proposal, **not** a local patch. tusd especially (an upload server with its own protocol) will
   have `ProviderFacing`-style surfaces the kit may not cover yet; document, don't improvise.
5. Never mix a behavior change into a migration change. If migration reveals a real bug in the old service,
   report it separately.

## 5. Kit upgrades (consuming a new kit version)

When the kit owner announces a new version (or an audit/propagation prompt asks you to upgrade):

1. Read the kit's `CONTRACTS.md` change-history entries and any deprecation records between your pinned version
   and the target.
2. Bump `go.mod`, run the full gate (`go build ./...`, `go test -race ./...`, `contracttest`, lints).
3. A red `contracttest` after an upgrade means either your service relied on something outside the contract
   (fix the service) or the kit broke a contract in a minor (file a change request flagged `severity: blocking`
   — minors must never break).
4. Update your registry row's `kit_version`.
5. Remove any `KIT-WRAP` whose underlying request shipped in this version.

## 6. What a consumer session must never do

- Edit any file in the kit repo except `docs/CONSUMERS.md` (registration/roster updates only).
- Copy kit source into the service, even "temporarily".
- Re-declare kit-owned metric names, env keys, error codes, or envelope shapes locally.
- Rename or re-prefix kit metrics/env keys (one renamed metric kills the shared dashboards).
- Suppress, skip, or weaken `contracttest` to make an upgrade pass.
- Ship a `KIT-WRAP` without a same-day change request or baseline proposal on file.
