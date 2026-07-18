# Consumer Development — Building a Service on the Kit

Phase gate: this mode executes only while consumer work is active per
[05-phase-and-source-truth](05-phase-and-source-truth.md). During `KIT_FIRST_STABILIZATION`, do not open, edit,
validate, register from, or prompt a consumer repository; demonstrate anything consumer-shaped with kit-local
scaffold fixtures instead, and treat consumer-named requests as kit-improvement input.

Your service owns **only its domain**; everything platform-shaped comes from the kit. This file tells you how to
stay inside that line and what to do when the line pinches.

## Session preconditions (before writing code)

1. Load `alaa-golang-clean-code-principles` (P1–P13 is the bar for all Go you write) and normally `alaa-golang`,
   plus the domain companion skills the touched surfaces require (per the repo `AGENTS.md` routing).
2. Read the service's architecture/domain doc and the kit `CONTRACTS.md` sections your task touches. Repo truth
   outranks both.
3. Pin an immutable released `git.alaatv.com/vk/alaa-go-chi` version in `go.mod`. Never commit a local `replace`;
   a debugging `replace` must be removed before the task is reported done.
4. Check `docs/CONSUMERS.md` in the kit repo. If your service has no row, register it per
   [50-consumer-registry](50-consumer-registry.md) — the only kit-repo write a consumer agent ever makes.
5. Wire the governance in: the consumer repo's root `CLAUDE.md`/`AGENTS.md` must name `alaa-go-chi-development`,
   `alaa-golang`, and `alaa-golang-clean-code-principles` as mandatory. Install the kit's canonical pair from
   `docs/consumer-templates/` (substituting the service name) rather than writing your own.

## Kit-owned surfaces (import, never re-implement, never fork)

If your task seems to need any of these, the answer is an import, not an implementation:

- success/error envelopes; JSON binding, strict-JSON rules, body caps; the middleware chain and its order;
  correlation headers; panic recovery; route families (`Trusted`/`Anonymous`/`ProviderFacing`/`Operational`)
- trusted-header parsing, `TrustCtx`, permission-bitmap decode, `RequirePermission`, `RequireTOTP`, gateway-proof
- health/readiness envelopes and severities; lifecycle/shutdown ordering (`runkit`)
- metric names, log field vocabulary, OTel/Sentry wiring (`obskit`); env-key catalog (`configkit`)
- Postgres pools, two-lane DSN contract, scale tiers, composed goose migrations, testdb helpers (`pgkit`)
- Redis transport, cache adapter, invalidation, degraded readiness, cache metrics (`rediskit`)
- MQ envelope codec, confirming publisher, consumer shell, receipts, topology (`mqkit`); outbox (`outboxkit`);
  jobs (`jobkit`); seeders (`seedkit`); UUIDv7 (`idkit`); audience predicate (`audiencekit`)
- ControlledOps state/approval/audit (`ctlopskit`); bulk mechanics (`bulkkit`); Tier-2 generation (`genkit`)
- API contract merge/validation/Postman (`apicontractkit`); `contracttest`; scaffold, CI, deploy templates, lints
- shared-infra provisioning/attachment (generated wrappers + `deploy/shared-infra/compose.yaml` under the
  canonical `alaa-shared-infra` identity); permission-map generation (`alaa-permission-catalog` via the
  `alaa-permission-generator` skill)

Service code owns: domain entities, use cases, policies, repositories behind application ports, provider
translation, domain schemas/events/error codes, and composition of only the roles/capabilities it uses.

## Decision tree for every new piece of logic

```
Is this behavior already in the kit? (verify in the capability map + current source)
├─ yes → import it. If its API doesn't fit, do NOT copy/patch:
│         ├─ small mismatch → thin local wrap (adapter, no behavior fork), marked
│         │   `// KIT-WRAP(<date>): <reason>`, change request filed the SAME DAY.
│         │   Max lifetime: two kit releases.
│         └─ real gap or bug → file a kit change request (references/20) and either
│             wait, or wrap as above if the task cannot wait.
├─ no, but platform-shaped or ≥2 consumers could plausibly need it → baseline
│   proposal FIRST (references/20); implement only as a bounded KIT-WRAP if the
│   schedule demands.
└─ no, genuinely domain-specific → implement it in your service, in the layer
    P5 dictates, per the clean-code skill.
```

The self-test that catches most violations: **if the code you are about to write would look materially identical in
a second Ala service, stop — it belongs in the kit.** The rediskit story shows the split: the generic Redis
transport (client, cache adapter, invalidator, readiness) was identical across services and became kit-owned; only
each service's domain cache shapes stayed local. Abstract the shared mechanics, keep the domain policy. If you keep
something local on purpose, record the one-paragraph justification in the service's `docs/DECISIONS.md`.

## Build flow (new service)

1. Generate with `alaa-go-chi new service <name> --parent-dir <dir>` — never hand-copy another service's tree.
   Generated policy, docs, deploy, API-contract, hooks, and CI surfaces are part of the contract; keep them, fill
   the TODOs, replace placeholder routes with thin handlers over domain use cases.
2. Register the service with status `bootstrapping`; wire only the subcommands the service actually uses
   (`serve|consume|dispatch|relay|migrate|seed|topology|ops`).
3. Choose capabilities from [12-kit-capability-map](12-kit-capability-map.md); verify every symbol against current
   kit source/docs before use.
4. Define canonical domain/API/event/data contracts before implementation; assign every route exactly one posture.
   Declare the service's permissions in `alaa-permission-catalog` using the `alaa-permission-generator` skill: it
   generates `internal/authz/permissions_gen.go` in your service and syncs the `auth` seed. Wire that generated map
   into the `servicePermissions` seam (replacing the generated `trustkit.DenyAllPermissions` placeholder). Never
   hand-write permission names or bitmap ids, and re-run the generator — in both catalog consumers — whenever
   permissions change.
5. Keep `domain <- application <- infrastructure`; handlers parse, invoke one use case, render.
6. Commit authoritative state, outbox/audit/receipt/idempotency records that must agree in one transaction; bound,
   cancel, and own every worker/goroutine with defined retry/DLQ/terminal/replay/shutdown semantics.
7. Wire low-cardinality logs/metrics/traces and required/degraded readiness. Never expose secrets/PII/raw payloads.
8. Keep route truth, OpenAPI, fixtures, Postman, extraction chains, docs, deploy roles, and CI synchronized
   (`make api-contract`).
   For local/dev infra, use the generated shared-infra path: attach to (or let the wrappers provision) the one
   canonical `alaa-shared-infra` instance on `alaa-shared-network`. Never add a service-owned Postgres/Redis/
   RabbitMQ to the service compose, and never bypass the reuse-if-healthy gate — Go and Laravel services share
   this one infra set by platform contract.
9. Validate targeted → contract/API/gen gates → full/race/static/vuln → real-infra truth tiers → render/smoke as
   risk requires. While runners are unassigned, report `local_ci_smoke_passed; runner_contract_pending` — never
   claim remote CI green. Update the registry row to `active` once contracttest passes.

## Datastore-free services

A service with no Postgres and/or no RabbitMQ is first-class: compose `configkit.WithoutPostgres()` /
`WithoutRabbitMQ()` only when the surface truly does not exist, pass the matching `contracttest.DocSurfaces`, and
never invent placeholder DSNs or set a disabled-lane key. The released scaffold has no `--without-pg`/`--without-mq`
flags yet — prune composition deliberately, keep the generated core contracts, or file a scaffold change request.

## What a consumer session must never do

- Edit any kit-repo file except its own `docs/CONSUMERS.md` row.
- Copy kit source into the service, even "temporarily"; hand-edit generated files instead of regenerating.
- Re-declare or re-prefix kit-owned metric names, env keys, error codes, or envelope shapes locally.
- Suppress, skip, or weaken `contracttest` to make a build or upgrade pass.
- Hand-write permission names/bitmap ids, edit a `Code generated by alaa-permission-catalog. DO NOT EDIT.` file,
  or define a local route posture.
- Declare service-local sibling infrastructure (own Postgres/Redis/RabbitMQ containers) instead of the canonical
  shared-infra identity.
- Ship a `KIT-WRAP` without a same-day change request or baseline proposal on file.
