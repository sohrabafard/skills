---
name: alaa-services-contract
description: "Normative shared-surface contract for Ala backend services and the `@alaa/*` frontend packages: response and error envelopes, health and readiness shapes, trusted gateway headers, public identifiers, event and code names, permission and authorization catalogs, broker and metric registries, request deadlines, and the shared runtime and CI baseline. Use when a change must look identical across the fleet, or when touching @alaa/sdk, Page Kit, UI Kit, app-shell, or widgets. Do not use for feature work inside one service that changes no shared surface. Route generic Docker, Kubernetes, HAProxy, Laravel, or Go engineering to /alaa-docker-production, /caas-arvan-kuber, /alaa-haproxy, /alaa-laravel-architecture, /alaa-golang; observability gates and alerts to /alaa-observability-soc; reliability doctrine to /alaa-reliability-sla; security verdicts to /alaa-security-review; pure UI design to /alaa-frontend-developer."
---

# Alaa Services Contract

You are enforcing one fixed contract across a growing fleet of Ala microservices. It is normative, not
advisory: agents in different repositories must produce the same envelopes, header names, event names,
failure behaviour, and runtime shape, because a fleet aligned service-by-service to each agent's own
judgment cannot be debugged. Exact detail lives in `references/`; this file routes.

## Hard contract rule

- Enforce the contract exactly. Never restate an exact output as an optional recommendation, and never
  invent a local variant of a surface this skill already defines.
- When a repository deviates, converge it. Reporting the blocker replaces converging in exactly three
  cases and no others: (1) convergence would change a surface a live external consumer already depends on
  and no deprecation window has been opened for it under `references/22-failure-load-and-deprecation-contract.md`;
  (2) the repo's own `AGENTS.md` or a repo-owned contract document states the opposite rule, so the owner
  must settle which wins; (3) convergence requires an edit in a second repository outside the current
  task's scope. In those three, stop at the boundary, state the conflicting rule and both file paths, and
  change nothing else. In every other case, converge.
- When this skill replaces a header, field, event, code, route, or helper, remove the old implementation in
  the same change. Anything a consumer can observe goes through the deprecation procedure in
  `references/22-failure-load-and-deprecation-contract.md` first.
- While the provisional backend role freeze is active, authorize with catalog-owned permission bits from
  trusted `X-Access` plus the contract-defined OpenFGA decision. Add no role resolvers, role-derived
  policies, role-to-permission maps, or role-dependent behaviour; roles may be retained only as
  non-authoritative observability metadata. `references/28-backend-permission-authorization-and-role-freeze.md`
  owns the freeze and its activation gate.
- Logs, traces, metrics, and exception evidence are part of done for every long-lived Ala service.
- Keep reference paths relative to this skill folder and repository paths repo-relative, so the skill works
  on any machine.

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read `references/00-topic-map.md` and pick the service mode.
3. Select the repository role: frontend-facing backend behind the gateway, internal backend, auth-boundary
   service, or authz-runtime / control-plane service.
4. Read the smallest reference file that owns the rule you need, not the largest one that mentions it.
5. Load the companion skills that file names, before implementing outside this skill's ownership.
6. Apply the change.
7. Run the checklists in `references/40-apply-checklist-and-anti-patterns.md`.
8. Update docs, Postman artifacts, and tests for every contract surface you touched, in the same change.

## Trigger to file

Short form, keyed on the concern. Step 2 above loads `references/00-topic-map.md`, which carries the full
identifier-level trigger vocabulary per mode; each reference file names its own companion skills.

| Task touches | File |
|---|---|
| Health, readiness, service identity, route families | `10-core-service-contract.md` |
| Deployment mode, shared infra, registry, CI baseline, fast tests | `15-deployment-and-runtime-contract.md` |
| Correlation headers, log fields, event and code names, request middleware | `20-operational-and-observability-contract.md` |
| OTLP exporter env, Prometheus scraping, per-service telemetry reality | `21-alaa-platform-observability-directive.md` |
| A timeout, retry, idempotency key, pool bound, request deadline, load-shedding decision, or deprecating any contract surface | `22-failure-load-and-deprecation-contract.md` |
| An exchange, queue, or routing-key name, or whether a message is an event or a command | `23-queue-and-exchange-registry.md` |
| A metric name, its type, its labels, or registering a new one | `24-metric-registry.md` |
| Gateway prefixes, route ownership, internal hops, public vs private identifiers, internal mTLS status | `25-end-to-end-flow-and-boundaries.md` |
| Request-time per-resource authorization and its OpenFGA wire contract | `26-request-time-authorization-openfga.md` |
| Sending work to the `notification` service | `27-notification-service-contract.md` |
| Backend authorization decisions, roles, and access levels | `28-backend-permission-authorization-and-role-freeze.md` |
| Laravel trusted ingress, the public `project_id` boundary, the `/api/*` success envelope | `30-trusted-ingress-and-laravel-contract.md` |
| TOTP enrollment and forced route-level step-up | `32-auth-totp-and-step-up-contract.md` |
| Permission catalogs, bitmap ids, generated permission configs, drift checks | `35-permission-catalog-and-service-configs.md` |
| Frontend or host code consuming the `@alaa/*` SDK | `60-frontend-sdk-consumption-contract.md` |
| Page Kit, UI Kit, app-shell, widgets | `65-frontend-page-kit-and-widgets-contract.md` |
| Which standard, framework doc, or platform doc outranks which | `90-source-map.md` |
| Which services follow a rule today, and what a named service must change to follow it | `95-fleet-conformance.md` |

`references/50-laravel-copy-baselines.md` holds copy-oriented Laravel class and helper shapes. Read it only
after the file that owns the rule, because it carries shapes, not decisions.

## Companion skills

Invoke a companion as `/alaa-trust-gateway-auth` in Claude Code and `$alaa-trust-gateway-auth` in Codex.
Every skill named anywhere in this pack takes both forms; reference files write the `$` form and it means
the same skill in either runtime. Each reference file names the companions its own concern needs. These
load on a concern no reference file keys on:

- `alaa-php-clean-code` — before implementing or refactoring any PHP.
- `alaa-crockford-base32-codecs` — shared Crockford Base32 or UUIDv7 helper assets across runtimes.
- `alaa-docs-farsi` — when docs, Postman artifacts, or runbooks change.
- `alaa-frontend-doc-annotations`, `alaa-quasar-app-vite-v3` — the documentation pass on a new public
  frontend surface, and exact Quasar component or SSR shapes.
- `alaa-keyset-pagination` — before writing or reviewing a paginated list query: the ordering tuple, the
  index, the continuation predicate, the signed cursor, and the hard cases. This skill keeps the wire shape.
- `alaa-prompting-guide` — every model, effort, prompt, skill, or agent-definition question. This skill
  names no model anywhere.

## What this skill does not own

This skill owns **names, values, shapes, and wire behaviour**. It does not own the requirement levels,
verdicts, or doctrine attached to them. Where a rule here and a rule in one of these skills disagree, the
skill named below wins for its half, and the weaker statement here is deleted rather than kept as a second
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
- **`alaa-docker-production`**, **`caas-arvan-kuber`**, **`alaa-haproxy`**, and **`alaa-gitlab-ci-cd`** own
  the mechanics of containers, clusters, proxies, and pipelines. This skill keeps the Ala fleet policy.
- **`alaa-async-messaging`** and **`alaa-laravel-job-rabbitmq`** own broker prefetch, acknowledgement
  mechanics, DLQ handling, and consumer tuning. This skill keeps the exchange, queues, routing keys, and
  envelope.
- **`alaa-data-layer`** owns pool mechanics inside a driver and persistence invariants. This skill keeps the
  pool bounds and the acquire timeout.
- **`/alaa-minio-object-storage`** (`$alaa-minio-object-storage`) owns the object store as a platform component: the
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
- **`alaa-prompting-guide`** owns model and effort selection.

## When not to use

- Feature work inside one service that changes no shared surface: no envelope, header, event, code, route
  family, permission, queue, metric name, or package boundary.
- Visual or design polish with no package-boundary, SDK-consumption, trust-boundary, or observability
  contract in scope. Use `$alaa-frontend-developer`, and `$alaa-ui-ux-design-system` for design-system work.
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
