# Debug, Upgrade, Migrate, and Review

**Capability required: `consumer-repo-read`, plus `consumer-repo-write` for any fix.** Look up both cells for the
active phase in the matrix in [05-phase-and-source-truth](05-phase-and-source-truth.md) before you open anything.
When a cell blocks you, apply the same method to the kit and its generated fixtures instead, and say that is what
you did.

## Diagnose before changing

1. Read the repository instructions, the pin in `go.mod`, generated file headers, current config, route
   inventory, migrations, and the failing command or test. Reproduce the smallest failing path.
2. Classify the fault boundary and keep the classes separate in the report: service domain bug, incorrect kit
   usage, generated drift, kit defect, config or deploy, infrastructure, or host/tooling/network friction.
3. Compare behaviour against the **pinned** kit version, not against a working kit checkout. A missing command or
   symbol on an old pin is a release or upgrade issue, not a cache or tooling issue.
4. A temporary local `replace` is allowed for deliberate diagnosis and is never committed. Never copy kit code to
   unblock.
5. Diagnose only, unless the request authorizes fixes. For an authorized fix, make the smallest complete change
   and re-run the originally failing path. A kit defect found here becomes a change request (`20-`), never a
   local patch.

## Generated and Tier-2 drift

- Read the generated file headers and run the generator matching the service's pin. A binary-versus-pin mismatch
  must fail; that failure is the diagnosis.
- Regenerate through `alaa-go-chi gen`, the scaffold, or the API-contract generators. Never patch generated
  output by hand and never copy a generated file from another service.
- Validate `ops/ops.yaml`, route bindings, migrations, docs, OpenAPI, fixtures, Postman, and the drift gate
  (`make tier2-drift`) together.

## Upgrading the kit pin

1. Read `CHANGELOG.md`, the decision records named in `12-`, the `CONTRACTS.md` delta, and any deprecations
   between the old and new pins.
2. Inventory the affected imports, env keys, error and metric names, generated artifacts, migration sources, and
   deploy jobs.
3. Pin the immutable released version, regenerate everything generated with that version, and remove temporary
   replaces. Resolve every `.kitnew` file `alaa-go-chi upgrade` emitted; an unresolved `.kitnew` is an unfinished
   upgrade.
4. Adapt call sites without local compatibility forks, and delete every `KIT-WRAP` whose underlying request
   shipped in this version — the wrap's full contract is in `10-`.
5. A red `contracttest` after an upgrade means one of two things: the service relied on something outside the
   contract, which the service fixes; or the kit broke a contract in a minor, which is a change request with
   `severity: blocking`. Minors never break.
6. Run targeted behaviour tests, then the contract, API and generator drift gates, then full/race/static checks,
   then real-infrastructure gates, then deploy-render and local CI, in proportion to what changed. Update the
   registry row's `kit_version`, `contracttest`, and `updated` fields from verified results only.

## Migrating an existing service onto the kit

Migration is a behaviour-preserving refactor, so it is stricter than greenfield.

1. **Inventory first.** Produce a timestamped adoption inventory in the migrating repository at
   `docs/kit-adoption/YYYY-MM-DD-<service>-kit-adoption-inventory.md`: every hand-rolled platform surface mapped
   to the kit package that replaces it; every piece of domain behaviour mapped to its preserved owner; and every
   surface with no kit equivalent mapped to a change request or baseline proposal, never to a local improvisation.
2. Register the service with status `migrating`.
3. Replace surface by surface, one reviewable change each, in this order: boot config and lifecycle → HTTP,
   envelopes and trust → readiness and observability → Postgres lanes and migrations → messaging, outbox, jobs
   and seeders → API, generation, deploy and CI. After each surface, the service's own tests plus `contracttest`
   for the surfaces already migrated must pass.
4. Use expand-contract database changes, durable idempotency, and run-twice proof. Never move DDL to the pooled
   lane.
5. Never mix a behaviour change into a migration change. Report bugs found in the old service separately, and
   preserve external behaviour unless a canonical contract change was explicitly approved.

## Review priorities

Report correctness, security, data-loss, race, idempotency, contract, and governance defects first. Every finding
carries its `path:line` or symbol, the risk, the P-number or `CONTRACTS.md` section it violates, and the smallest
fix. Re-run the review after authorized fixes until no actionable finding remains. Green unit tests are level 2
and nothing more: name the proof level reached and the evidence still missing, using the vocabulary in `05-`.
