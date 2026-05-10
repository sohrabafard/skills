---
name: alaa-controlled-ops
description: "Use this skill when work involves Ala ControlledOps package or consuming-service adoption: bulk operations, dry-run hashes, approval or rejection lifecycle, execution admission, retry or cancellation helpers, idempotency, service adapters, package release through Satis, route/Postman parity, write-boundary validation, or the `alaa/controlled-ops` repository. Do not use it for generic queue, docs, Postman, or Laravel work that has no ControlledOps surface."
---

# Alaa ControlledOps

## Purpose

Use this skill to keep ControlledOps package and adopter-service work inside the right ownership boundary.

The shared package owns reusable workflow primitives. The consuming service owns HTTP API shape, domain validation, domain writes, migrations, queues, outbox, and public docs.

Keep this top-level file lean. Load only the reference files needed for the current task.

## When to use

- changes inside `D:\Sohrab\Project\alaa-controlled-ops`
- ControlledOps adoption in a service such as `content`
- bulk operation request, dry-run, approval, rejection, execution, retry, cancellation, or fatal-recovery work
- dry-run hash, payload hash, idempotency key, replay, or conflict behavior
- service adapter boundaries, write-boundary tests, route or Postman parity for ControlledOps endpoints
- package release, Satis visibility, Composer lock verification, or package-to-service rollout

## When NOT to use

- generic Laravel architecture work with no ControlledOps package or adopter surface
- generic async, RabbitMQ, Postman, or docs work unless it is tied to ControlledOps behavior
- approval workflow design for a product that is not using the Ala ControlledOps package
- direct domain feature work where ControlledOps contracts, lifecycle, hashes, or package adoption are irrelevant

## Quick start

1. Read the active repo `AGENTS.md`.
2. Classify the target as package work, consuming-service adoption, or cross-repo release/adoption work.
3. Read `references/00-topic-map.md`.
4. Verify current behavior from the active repo before using any historical route counts, permission IDs, package versions, or phase names.
5. For package work, inspect `D:\Sohrab\Project\alaa-controlled-ops` docs, contracts, tests, and `scripts/controlled_ops_verify.php`.
6. For adopter-service work, inspect the consuming service routes, controllers, FormRequests, resources, migrations, jobs, tests, docs, and Postman artifacts first.
7. Pair with `$alaa-services-contract`, `$alaa-trust-gateway-auth`, `$alaa-postman-collections`, `$alaa-docs-farsi`, `$alaa-php-clean-code`, or `$service-runtime-kit-governance` when those surfaces are in scope.

## Non-negotiables

- Package availability does not create service runtime behavior. A service must implement and validate its own routes, requests, resources, locks, transactions, workers, and outbox behavior.
- ControlledOps package code must not write consuming-service domain tables or receive raw upload bodies.
- Dry-run, approval, execution, retry, cancellation, and recovery claims must be backed by current code or committed docs.
- Treat historical session facts as search hints. Verify exact route counts, Postman counts, permission IDs, and package versions against the current repositories.
- Prefer tagged Satis package adoption for service Composer locks. Local path repositories are developer-only overrides unless the user explicitly asks otherwise.

## Reference navigation

- Read `references/10-source-priority-and-boundaries.md` before making contract or ownership claims.
- Read `references/20-package-service-adoption.md` when adopting or releasing the package into a service.
- Read `references/30-lifecycle-idempotency-validation.md` for dry-run hash, approval, replay, conflict, and lifecycle semantics.
- Read `references/40-validation-and-release-gates.md` before closing package or adopter-service work.
- Read `references/90-source-map.md` when version, release, or source freshness matters.

## Maintenance rules

- Keep `SKILL.md` routing-first.
- Put detailed package facts in `references/`, and keep those facts traceable to current repo docs or code.
- Refresh this skill after meaningful changes to `D:\Sohrab\Project\alaa-controlled-ops` adoption or release policy.
