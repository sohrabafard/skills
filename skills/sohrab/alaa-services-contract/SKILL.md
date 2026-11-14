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

Each service owns `docs/PRODUCT_OVERVIEW.fa.md`, a Persian introduction for product and engineering.
Describe its purpose, main concepts and entities with English names in parentheses, important relationships,
and ownership boundaries. Use one or two concise paragraphs where appropriate. Ground the text in current
service sources and update it when concepts change. It is descriptive; source truth and contracts remain authoritative.
Use one additional concise paragraph for important supplementary capabilities and relationships that would
complicate the diagram. Ground it in current service-owned sources.
Append a simple conceptual Mermaid entity-relationship diagram immediately after the Persian overview paragraphs.
Show only key domain entities and relationships needed to understand the service, with source-grounded cardinalities.
Include user interaction and state when needed for understanding; describe other important capabilities in the
supplementary paragraph instead. Include only facts supported by current service-owned sources. Omit the full physical schema.
The diagram helps product and engineering liaisons assess requests and database design against the existing model.
Use a plain `mermaid` fenced code block without custom configuration. End the document there, without explanatory
prose or an examples table below the diagram.
If the file is missing and creation is within authorized scope, delegate it to a subagent: use
`gpt-6.1-terra` at `high` effort in Codex or `opus` at `medium` effort in Claude Code. Respect higher-priority
instructions and available runtime capabilities; report a blocker if the required delegation is unavailable.

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

Each reference names the companions its concern needs. When a concern arises that no reference keys on (PHP code, a shared Crockford Base32 or UUIDv7 helper, a docs, Postman or runbook change, a new public frontend surface or an exact Quasar component or SSR shape, a paginated list query, or a model, effort, prompt, skill or agent-definition question), read *Companion skills* in `references/00-topic-map.md`. It names the skill to load for each.

## What this skill does not own

This skill owns **names, values, shapes, and wire behaviour**. It does not own the requirement levels,
verdicts, or doctrine attached to them. Where a rule here and a rule in the owning skill disagree, the
owning skill wins for its half. Before you decide a requirement level, a gate, a doctrine or a mechanism, read
*Owned by another skill* in `references/00-topic-map.md`. It names each owner and what this skill keeps.

## When not to use

- Feature work inside one service that changes no shared surface: no envelope, header, event, code, route
  family, permission, queue, metric name, or package boundary.
- Visual or design polish with no package-boundary, SDK-consumption, trust-boundary, or observability
  contract in scope. Use `/alaa-frontend-developer`, and `/alaa-ui-ux-design-system` for design-system work.
- Overriding a repository-specific blocker. Report the incompatibility under the three-case rule above.

## Maintenance rules

Before you edit this skill, read *Maintenance rules* in `references/00-topic-map.md`.
