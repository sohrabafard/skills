# Debug, Upgrade, Migrate, and Review

Phase gate: use this mode on an existing service only while consumer work is active per
[05-phase-and-source-truth](05-phase-and-source-truth.md). During `KIT_FIRST_STABILIZATION`, apply the same method
to the kit and its generated fixtures only; do not open consumer repos.

## Diagnose before changing

1. Read the repo instructions, the pin (`go.mod`), generated file headers, current config, route inventory,
   migrations, and the failing command/test. Reproduce the smallest failing path.
2. Classify the fault boundary: service domain bug, incorrect kit usage, generated drift, kit defect, config/deploy,
   infrastructure, or host/tooling/network friction. Keep these separate in the report.
3. Compare behavior against the **pinned** kit version, not the working kit checkout. A missing command or symbol on
   an old pin is a release/upgrade issue, not a cache or tooling issue.
4. A temporary local `replace` is allowed only for deliberate diagnosis; never commit it. Never copy kit code to
   "unblock".
5. Diagnose only unless the request authorizes fixes. For authorized fixes, make the smallest complete change and
   re-run the originally failing path. A kit defect found here becomes a change request (references/20), not a local
   patch.

## Generated and Tier-2 drift

- Read generated file headers and run the generator matching the service pin. A binary/pin mismatch must fail — that
  failure is the diagnosis, not an obstacle.
- Regenerate through `alaa-go-chi gen`, the scaffold, or the API-contract generators; never patch generated output
  by hand, and never copy generated files from another service.
- Validate `ops/ops.yaml`, route bindings, migrations, docs, OpenAPI/fixtures/Postman, and the drift gate
  (`make tier2-drift`) together.

## Upgrading the kit pin

1. Read the kit `CHANGELOG.md`, the decision records, the `CONTRACTS.md` delta, and any deprecations between the old
   and new pins.
2. Inventory affected imports, env keys, error/metric names, generated artifacts, migration sources, and deploy jobs.
3. Pin the immutable released version; regenerate everything generated with that version; remove temporary replaces.
4. Adapt call sites without local compatibility forks. Delete every `KIT-WRAP` whose underlying request shipped in
   this version.
5. A red `contracttest` after an upgrade means either the service relied on something outside the contract (fix the
   service) or the kit broke a contract in a minor — file a change request with `severity: blocking`; minors must
   never break.
6. Run targeted behavior tests, contract/API/gen drift gates, full/race/static checks, infra truth tiers,
   deploy-render, and local CI gates proportionally. Update the registry row (`kit_version`, `contracttest`,
   `updated`) from verified results.

## Migrating an existing service onto the kit

Migration is a behavior-preserving refactor, so it is stricter than greenfield:

1. **Inventory first.** Produce a timestamped adoption inventory in the migrating repo
   (`docs/kit-adoption/YYYY-MM-DD-<service>-kit-adoption-inventory.md`): every hand-rolled platform surface → the
   kit package that replaces it; domain behavior → its preserved owner; no kit equivalent → a change request or
   baseline proposal, never a local improvisation.
2. Register the service with status `migrating`.
3. Replace surface by surface, one reviewable change each, in this order: boot config/lifecycle → HTTP/envelopes/
   trust → readiness/observability → Postgres lanes/migrations → messaging/outbox/jobs/seeders → API/gen/deploy/CI.
   After each surface, the service's own tests plus `contracttest` (for surfaces already migrated) must pass.
4. Use expand-contract database changes, durable idempotency, and run-twice proof. Never switch DDL to the pooled
   lane.
5. Never mix a behavior change into a migration change; report old-service bugs separately. Preserve external
   behavior unless a canonical contract change was explicitly approved.

## Review priorities

Report correctness/security/data-loss/race/idempotency/contract/governance defects first. Each finding includes
path:line/symbol, risk, the P1–P13 principle or contract section, and the smallest fix. Re-run review after
authorized fixes until no actionable findings remain. Never equate green unit tests with SLA readiness — name the
missing load, saturation, HA/failover, chaos, live telemetry, real CI, and SLO evidence explicitly.
