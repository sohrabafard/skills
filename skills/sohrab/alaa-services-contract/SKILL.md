---
name: alaa-services-contract
description: "Normative contract for Ala backends and `@alaa/*`: response/error envelopes, health/readiness, trusted gateway headers, public IDs, event/code names, permission catalogs, broker/metric registries, deadlines, runtime/CI baseline, delivery-artifact ownership. Use when changes must match fleet-wide; before shared Ala image/chart/CI include/generator; for Ala Runner/executor/job image/ci-image tools/CI Docker daemon/manual image release; for `@alaa/sdk`, Page Kit, UI Kit, app-shell or widgets; or shared infrastructure source/provisioning/recovery. Not for single-service feature work with no shared-surface change. Route Docker/Kubernetes/HAProxy/Laravel/Go to /alaa-docker-production, /alaa-k8s-helm, /alaa-haproxy, /alaa-laravel-architecture, /alaa-golang; observability gates to /alaa-observability-soc; reliability doctrine to /alaa-reliability-sla; security verdicts to /alaa-security-review; UI design to /alaa-frontend-developer."
---

# Alaa Services Contract

You are enforcing one fixed contract across a growing fleet of Ala microservices. It is normative, not
advisory: agents in different repositories must produce the same envelopes, header names, event names,
failure behaviour, and runtime shape, because a fleet aligned service-by-service to each agent's own
judgment cannot be debugged. Exact detail lives in `references/`; this file routes.

## Hard contract rule

- Enforce the contract exactly. Never restate an exact output as an optional recommendation, and never
  invent a local variant of a surface this skill already defines.
- When a repository deviates, converge it. Apart from the gRPC stop condition below, reporting the
  blocker replaces converging only in these three cases: (1) convergence would change a surface a live external consumer already depends on
  and no deprecation window has been opened for it under `references/22-failure-load-and-deprecation-contract.md`;
  (2) the repo's own `AGENTS.md` or a repo-owned contract document states the opposite rule, so the owner
  must settle which wins; (3) convergence requires an edit in a second repository outside the current
  task's scope. In those three, stop at the boundary, state the conflicting rule and both file paths, and
  change nothing else. A CI gap under the [Milestone 1 exception](references/15-deployment-and-runtime-contract.md#gitlab-cicd-baseline-contract) is not a deviation.
- When this skill replaces a header, field, event, code, route, or helper, remove the old implementation in
  the same change. Anything a consumer can observe goes through the deprecation procedure in
  `references/22-failure-load-and-deprecation-contract.md` first.
- The [current gRPC release policy](references/15-deployment-and-runtime-contract.md#grpc-in-the-current-development-release)
  governs when to stop convergence and when to retain a gRPC implementation. The deprecation procedure still applies.
- While the provisional backend role freeze is active, authorize with catalog-owned permission bits from
  trusted `X-Access` plus the contract-defined OpenFGA decision. Add no role resolvers, role-derived
  policies, role-to-permission maps, or role-dependent behaviour; roles may be retained only as
  non-authoritative observability metadata. `references/28-backend-permission-authorization-and-role-freeze.md`
  owns the freeze and its activation gate.
- Logs, traces, metrics, and exception evidence are part of done for every long-lived Ala service.
- Keep reference paths relative to this skill folder and repository paths repo-relative, so the skill works
  on any machine.

## Quick start

1. Read the repo-local `AGENTS.md`. Before touching or surveying another service, read "Paused and retired services" in `references/05-scope-service-modes-and-auth-routing.md`.
2. Read `references/00-topic-map.md` and pick the service mode.
3. Select the repository role: frontend-facing backend behind the gateway, internal backend, auth-boundary
   service, or authz-runtime / control-plane service.
4. Read the smallest reference file that owns the rule you need, not the largest one that mentions it.
   For service env declarations or deploy delivery, read
   [Deploy-time environment contract](references/15-deployment-and-runtime-contract.md#deploy-time-environment-contract).
   For Infra source, bootstrap, provisioning, transport or recovery, follow Mode A++ in the topic map;
   distinguish the shared policy from source support and deployed evidence.
5. Load the companion skills that file names, before implementing outside this skill's ownership.
6. Apply the change.
7. Run the checklists in `references/40-apply-checklist-and-anti-patterns.md`.
8. Update docs, Postman artifacts, and tests for every contract surface you touched, in the same change.

## Companion skills

Write cross-skill calls once as `/name`, per the pack's `AGENTS.md`. Each reference names the companions its concern needs. These
load on a concern no reference file keys on:

- `alaa-php-clean-code` — before implementing or refactoring any PHP.
- `alaa-crockford-base32-codecs` — shared Crockford Base32 or UUIDv7 helper assets across runtimes.
- `alaa-repo-docs` — when docs, Postman artifacts, or runbooks change.
- `alaa-frontend-doc-annotations`, `alaa-quasar-app-vite-v3` — the documentation pass on a new public
  frontend surface, and exact Quasar component or SSR shapes.
- `alaa-keyset-pagination` — before writing or reviewing a paginated list query: the ordering tuple, the
  index, the continuation predicate, the signed cursor, and the hard cases. This skill keeps the wire shape.
- `alaa-prompting-guide` — every model, effort, prompt, skill, or agent-definition question. This skill
  names no model anywhere.

## What this skill does not own

This skill owns **names, values, shapes, and wire behaviour**. It does not own the requirement levels,
verdicts, or doctrine attached to them. Where a rule here and a rule in one of these skills disagree, the
skill named below wins for its half. Maintainers delete the weaker statement here rather than keep it as a second
opinion.

- **`alaa-observability-soc`** owns every observability requirement level, gate, threshold, alert, Collector
  topology and processor placement, metric label allow and deny list, resource-identity policy, exemplar
  requirement level, and Sentry policy. This skill keeps every metric, log field, event, code, and `OTEL_*`
  name together with its default value.
- **`alaa-reliability-sla`** owns timeout, retry, circuit-breaker, backpressure, and error-budget doctrine —
  why a value exists and how to choose it. This skill keeps the Ala values and the wire behaviour in
  `references/22-failure-load-and-deprecation-contract.md`.
- **`alaa-security-review`** owns security review checklists and verdicts, the general fail-closed doctrine,
  and the general rule that allow-side authorization metadata is never an authorization input. This skill
  keeps the exact header names, envelope shapes, and the fail-closed wire contract those rules act on.
- **`service-runtime-kit-governance`** owns which generator variable expresses each runtime value and which
  kit version ships it. This skill keeps the canonical shared-infra names, the host-port table, and the
  reuse-or-fail-fast obligation.
- **`alaa-laravel-architecture`** and **`alaa-php-clean-code`** own PHP and Composer package selection and
  framework idiom. This skill keeps middleware order, class and helper names, and response boundaries.
- **`alaa-docker-production`**, **`alaa-k8s-helm`**, **`alaa-haproxy`**, and **`alaa-gitlab-ci-cd`** own
  the mechanics of containers, clusters and charts, proxies, and pipelines; **`caas-arvan-kuber`** owns Arvan
  CaaS platform facts. This skill keeps the Ala fleet policy.
- **`alaa-async-messaging`** and **`alaa-laravel-job-rabbitmq`** own broker prefetch, acknowledgement
  mechanics, DLQ handling, and consumer tuning. This skill keeps the exchange, queues, routing keys, and
  envelope.
- **`alaa-data-layer`** owns pool mechanics inside a driver and persistence invariants. This skill keeps the
  pool bounds and the acquire timeout.
- **`/alaa-minio-object-storage`** owns the object store as a platform component: the
  bucket, the tenant scope carried inside an object key, lifecycle and retention policy, storage-credential supply and
  rotation, and presigned-URL issuance. Load it when shaping a bucket, writing a lifecycle or retention policy,
  scoping an object key to a tenant, granting or rotating a storage credential, or issuing a presigned URL.
- **`alaa-keyset-pagination`** owns the pagination design method: choosing the traversal mode, the sort
  allowlist, the ordering tuple and its unique final component, the composite index, the row-value
  continuation predicate, the signed cursor's payload and context binding, and the nullable, mutable, and
  backward-traversal cases. This skill keeps the wire shape those decisions produce — `cursor`, `limit`,
  `meta.next_cursor`, `meta.prev_cursor`, the forbidden `meta` keys, and the admin-table offset exception.
- **`alaa-system-design`** owns *when* a contract shape is decided and by what procedure: the rule that the shape is
  settled in a design record and committed before the code that satisfies it, where the boundary the contract sits on
  runs, and which component owns each datum crossing it. This skill keeps the shape itself — the envelope, header,
  event, code, and identifier a decided contract must use. Read it before adding a surface, not while adding one.
- **`alaa-prompting-guide`** owns model/effort capability evidence and runtime mechanics; the runtime orchestrator owns actual task allocation for every authority role.

## When not to use

- Feature work inside one service that changes no shared surface: no envelope, header, event, code, route
  family, permission, queue, metric name, or package boundary.
- Visual or design polish with no package-boundary, SDK-consumption, trust-boundary, or observability
  contract in scope. Use `/alaa-frontend-developer`, and `/alaa-ui-ux-design-system` for design-system work.
- Overriding a repository-specific blocker. Report the incompatibility under the three-case rule above.

## Maintenance rules

- Keep this file routing-first; every exact contract detail lives in `references/`.
- State each rule in exactly one file. When a rule appears twice, delete the weaker statement and leave a
  one-line pointer to the owner.
- Change a route, header, event, code, metric, permission, or queue name only through the deprecation
  procedure in `references/22-failure-load-and-deprecation-contract.md`.
- Never pin a tool, kit, or library version here. Name the skill that owns the version instead, because a
  version pin in a contract file goes stale silently and is then copied forward as authoritative.
- When a change touches a contract owned jointly with a companion skill, update that skill in the same
  effort and record the split in the ownership list above.
- Record conformance in `references/95-fleet-conformance.md`, never in a rule file. When a change makes a
  service conform, or a new rule leaves the fleet behind, update that snapshot in the same effort. It is
  evidence, not contract: it states no rule and overrides none.
