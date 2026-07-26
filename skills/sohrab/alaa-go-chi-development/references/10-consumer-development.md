# Consumer Development — Building a Service on the Kit

**Capability required: `consumer-repo-write` (which implies `consumer-repo-read`).** Look up the cell for the
active phase in the matrix in [05-phase-and-source-truth](05-phase-and-source-truth.md) before the first step.
`forbidden` means stop and say which row stopped you. `evidence-required` means satisfy both of that value's
conditions first, then proceed. When the cell blocks you but the task still needs demonstrating, demonstrate it
against a kit-local scaffold fixture and treat any consumer named in the request as kit-improvement input.

Your service owns only its domain; everything platform-shaped comes from the kit. The inventory of kit-owned
surfaces — what to import rather than write — is in
[12-kit-capability-map](12-kit-capability-map.md). This file is how you stay inside that line and what to do when
the line pinches.

## Before writing code

1. Load `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) and `/alaa-golang`
   (`$alaa-golang`), plus the companion skills the touched surfaces require per the routing table in `12-`.
2. Read the service's architecture document and the `CONTRACTS.md` sections your task touches. Source outranks
   both.
3. Pin an immutable released `git.alaatv.com/vk/alaa-go-chi` version in `go.mod`. Never commit a local `replace`;
   a `replace` added for debugging is removed before the task is reported done.
4. Check `docs/CONSUMERS.md` in the kit repo. No row for your service means register it per
   [50-consumer-registry](50-consumer-registry.md) — the only kit-repo write a consumer agent ever makes.
5. Install the kit's canonical `AGENTS.md`/`CLAUDE.md` pair from `docs/consumer-templates/`, substituting the
   service name, rather than writing your own. They must name this skill and both Go skills as mandatory.

## The decision tree for every new piece of logic

```
Is this behaviour already in the kit? (check 12- and current source)
├─ yes → import it. If its API does not fit, do NOT copy or patch:
│   ├─ the gap is in the API shape, not the behaviour → thin local adapter, no
│   │   behaviour fork, marked `// KIT-WRAP(<date>): <reason>`, with the change
│   │   request filed the SAME DAY.
│   └─ the behaviour itself is wrong or missing → file a kit change request (20-)
│       and wait, unless a dated commitment would otherwise be missed — in which
│       case wrap as above, same day, and say in the request that a wrap is live.
├─ no, and a second service would need this behaviour unchanged → baseline
│   proposal FIRST (20-). "A second service would need it" is met when a registered
│   service's architecture document or code already contains the same shape, or a
│   contract owned by /alaa-services-contract ($alaa-services-contract) names it.
└─ no, and the behaviour encodes a rule true only of this service's domain →
    implement it here, in the layer P5 dictates, per the clean-code skill.
```

**The self-test that catches most violations:** would a second service have to change this code's *behaviour* —
not its types, names, or wiring — before it could use it? If no, it belongs in the kit. The `rediskit` precedent
shows the split: the generic Redis transport, cache adapter, invalidator and readiness check were identical
across services and became kit-owned, while each service's domain cache shapes stayed local. Abstract the shared
mechanics; keep the domain policy. Keeping something local on purpose is fine — record the one-paragraph
justification in the service's `docs/DECISIONS.md`.

## The `KIT-WRAP` contract

A wrap is the only sanctioned interim form of kit-shaped code in a consumer, and it is defined entirely here.

- It is an adapter over a kit symbol. It never re-implements the kit behaviour and never diverges from it.
- It carries the marker `// KIT-WRAP(<YYYY-MM-DD>): <reason>` at its declaration, with the real authoring date.
- A change request or baseline proposal for it is filed the same day. A wrap with no filed document is a silent
  fork and the highest-severity finding an audit can raise.
- It lives at most two kit releases. On the second release after its marker date, either the request has shipped
  and the wrap is deleted, or the wrap is a governance violation to escalate.
- On every kit upgrade, delete each wrap whose underlying request shipped in that version.

## Build flow for a new service

1. Generate with `alaa-go-chi new service <name> --parent-dir <dir>`; never hand-copy another service's tree. The
   flags, including `--without-postgres` and `--without-rabbitmq`, are in `12-`. Generated policy, docs, deploy,
   API-contract, hook, and CI surfaces are part of the contract: keep them, fill the TODOs, and replace the
   placeholder routes with thin handlers over domain use cases.
2. Register the service with status `bootstrapping`. Wire only the subcommands it actually uses
   (`serve|consume|dispatch|relay|migrate|seed|topology|ops`).
3. Choose capabilities from `12-`, verifying every symbol against current kit source before use.
4. Define the canonical domain, API, event, and data contracts before implementation, and assign every route
   exactly one posture. Declare permissions through `/alaa-permission-generator` (`$alaa-permission-generator`),
   which generates `internal/authz/permissions_gen.go` and syncs the `auth` seed; wire that generated map into
   the `servicePermissions` seam, replacing the generated `trustkit.DenyAllPermissions` placeholder. Never
   hand-write a permission name or bitmap id, and re-run the generator in both catalog consumers whenever
   permissions change.
5. Keep `domain <- application <- infrastructure`. Handlers parse, invoke one use case, and render.
6. Commit authoritative state and any outbox, audit, receipt, or idempotency record that must agree with it in
   one transaction. Bound, cancel, and own every worker and goroutine, with defined retry, DLQ, terminal, replay,
   and shutdown semantics.
7. Wire low-cardinality logs, metrics, traces, and required/degraded readiness. Never emit secrets, PII, or raw
   payloads.
8. Keep route truth, OpenAPI, fixtures, Postman, extraction chains, docs, deploy roles, and CI synchronized via
   `make api-contract`. For local infrastructure, attach to the one canonical shared-infra instance through the
   generated wrappers and `deploy/shared-infra/compose.yaml`; never add a service-owned Postgres, Redis, or
   RabbitMQ to the service compose, and never bypass the reuse-if-healthy gate. Go and Laravel services share one
   infra set by platform contract — the Laravel side is `/service-runtime-kit-governance`
   (`$service-runtime-kit-governance`).
9. Validate targeted behaviour first, then the contract, API and generator gates, then full/race/static/vuln,
   then real-infrastructure gates, then render and smoke, in proportion to risk. Report each with an outcome word
   from `05-` and name the proof level reached. Update the registry row to `active` once `contracttest` passes.

## Datastore-free services

A service with no Postgres and/or no RabbitMQ is first-class. Generate it with `--without-postgres` and/or
`--without-rabbitmq`, compose `configkit.WithoutPostgres()` / `WithoutRabbitMQ()` only where the surface truly
does not exist, and pass the matching `contracttest.DocSurfaces`. Never invent a placeholder DSN and never set a
key belonging to a disabled lane.

## What a consumer session must never do

- Edit any kit-repo file except its own `docs/CONSUMERS.md` row.
- Copy kit source into the service, even temporarily, or hand-edit a generated file instead of regenerating it.
- Re-declare or re-prefix a kit-owned metric name, env key, error code, or envelope shape locally.
- Suppress, skip, or weaken `contracttest` to make a build or an upgrade pass.
- Hand-write a permission name or bitmap id, edit a file marked
  `Code generated by alaa-permission-catalog. DO NOT EDIT.`, or define a local route posture.
- Declare service-local sibling infrastructure instead of the canonical shared-infra identity.
- Ship a `KIT-WRAP` without a same-day change request or baseline proposal on file.
