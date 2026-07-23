# Routing Matrix

Spawn only agents that materially reduce uncertainty or enforce a required authority boundary.

## Always or normally required

- Non-trivial repository change: at least one implementer.
- Combined changed state: `alaa-verifier`.
- Ship-quality judgment: `alaa-reviewer`.
- Behavior/API/config/operations changed: `alaa-documenter` after review.

## Evidence agents

### Spawn `alaa-explorer` when

- the owner module or execution path is unclear;
- the task crosses unfamiliar packages/services;
- tests and local conventions are not known;
- the main thread would otherwise guess file scope.

Do not spawn when the relevant paths and contracts are already established in current context.

### Spawn `alaa-researcher` when

- an external API/library/tool version controls correctness;
- official docs or standards are needed;
- sources disagree or current behavior may have changed;
- the task asks for an evidence-based comparison.

### Spawn `alaa-test-strategist` when

- acceptance criteria are easy to satisfy superficially;
- legacy behavior has weak coverage;
- concurrency, retry, idempotency, migration, security, or failure-mode testing matters;
- test layer selection and flake control need design.

## Implementation routing

Use `alaa-implementer` by default. Escalate the same dispatch to Opus 4.8 at xhigh effort — a per-invocation model override on the alaa-implementer agent — when any of these apply:

- public API/event/data contract changes;
- service boundaries or architecture decisions;
- concurrency, races, locking, distributed ordering, idempotency;
- auth/trust boundary or cryptographic correctness;
- schema/data migration coupled to application logic;
- complex backwards compatibility or rollout;
- multiple plausible designs with materially different failure behavior.

## Specialist gates

### Architecture critic

Trigger before implementation for cross-cutting design. Skip for a local bug fix whose contract and ownership are established.

### Security reviewer

Trigger for authn/authz, tokens/sessions, secrets, untrusted inputs, upload/download, query/command construction, serialization, webhooks, payments, crypto, tenant isolation, or privileged operations.

### Migration guardian

Trigger for DDL, constraints/defaults/nullability, index creation, data backfills, format transforms, cleanup/deletion, compatibility windows, or production data movement.

### Browser QA

Trigger for user-visible browser behavior. Require exact URL/environment/scenario. Preserve `--browser chromium` and existing profile settings.

### Performance profiler

Trigger only when there is a measurable question, comparable baseline, and budget. Do not use as generic optimization advice.

### Observability reviewer

Trigger for async jobs, queues, retries, external service calls, failure/degraded paths, production critical flows, or new operational states.

### Release guardian

Trigger for CI/CD, Docker/container, package/lock/version, config/env, feature flags, deployment order, health checks, startup/shutdown, release notes, or rollback changes.

## Failure routing

- Clear test failure owned by one lane: return to that implementer.
- Ambiguous/cross-lane/flaky/timeout/environment/contamination: `alaa-failure-analyst` first.
- Security/migration/architecture blocker: route the fix through an Opus-escalated implementer dispatch.
- Browser-only reproducible defect: browser QA provides evidence; owning implementer fixes.
- Test infrastructure defect: create an explicit infrastructure implementation lane; verifier never fixes it.
