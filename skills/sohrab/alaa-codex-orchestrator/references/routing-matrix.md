# Routing Matrix

Spawn only agents that materially reduce uncertainty or enforce a required authority boundary. The catalog is a menu: a typical goal fires one to three roles beyond its implementation lanes. One agent per lane, never several for the same lane, and never a subagent whose job is to double-check another subagent.

## Always or normally required

- Non-trivial repository change: at least one implementer.
- Combined changed state: `alaa-verifier`.
- Ship-quality judgment: `alaa-reviewer`.
- Behavior, API, configuration, or operations changed: `alaa-documenter`, after review.

## Specification and evidence agents

### Spawn `alaa-spec-analyst` when

- the request uses quality language that is not yet checkable ("make it robust", "clean this up", "improve performance");
- two competent readers would define "done" differently;
- a contract is implied but never stated;
- the goal bundles several outcomes that need separating before lanes can be drawn.

Skip it when the request already names the change, the files, and the observable result. This is the cheapest correctness lever in the pipeline — a complete specification up front raises first-pass correctness at every tier — but it is wasted on a concrete request.

### Spawn `alaa-explorer` when

- the owner module or execution path is unclear;
- the task crosses unfamiliar packages or services;
- tests and local conventions are not known;
- the main thread would otherwise guess file scope.

Do not spawn when the relevant paths and contracts are already established in current context.

### Spawn `alaa-researcher` when

- an external API, library, or tool version controls correctness;
- official docs or standards are needed;
- sources disagree or current behavior may have changed;
- the task asks for an evidence-based comparison.

### Spawn `alaa-test-strategist` when

- acceptance criteria are easy to satisfy superficially;
- legacy behavior has weak coverage;
- concurrency, retry, idempotency, migration, security, or failure-mode testing matters;
- test layer selection and flake control need design.

## Implementation routing

Use `alaa-implementer` — Terra at `high` — by default. Escalation is earned by decision density, not surface sensitivity: a lane that mechanically applies an already-ratified decision, an amended contract value, or a precise spec stays on the default implementer regardless of the surface it touches — the reviewer and specialist gates already provide Sol-tier scrutiny there.

Dispatch `alaa-implementer-sol` — Sol at `high` — only when the lane itself must make non-obvious design decisions and at least one of these applies. Record which one in the dispatch and again in the final agent roster:

- public API, event, or data contract changes;
- service boundaries or architecture decisions;
- concurrency, races, locking, distributed ordering, idempotency;
- auth or trust boundary, or cryptographic correctness;
- schema or data migration coupled to application logic;
- **authoring or rewriting an artifact whose deliverable is judgment itself** — a skill, a prompt, an agent definition, an `AGENTS.md`, an architecture document, or a standard other agents will follow. This criterion exists because the others describe software surfaces, and a lane can be judgment-dense without touching any of them. Writing a skill is not mechanical application of a ratified decision: deciding what belongs in the body versus a reference, which rules to merge or delete, and whether the result meets its own bar is the entire work. Judge the density, not the file extension;
- complex backwards compatibility or rollout;
- multiple plausible designs with materially different failure behavior.

When uncertain, do not escalate: dispatch the default implementer and let the review gate decide. One justified re-dispatch after evidence is cheaper than habitual escalation.

Three ceiling rules keep exactly one escalation axis open. **Terra's ceiling is `high`** — never raise a Terra lane's effort above `high` as a substitute for escalating, because above that ceiling the correct move is a different variant, not a bigger thinking budget. **Luna's ceiling is `medium`** — a Luna lane that needs to reason its way past `medium` has been mis-scoped, and the fix is a better dispatch or a different agent. **`max` is never a pin** — it exists only as a named per-invocation retry after a documented failure at `xhigh`.

Name the lane's matching clean-code skill in the dispatch when one is installed: `$alaa-php-clean-code`, `$alaa-vue-typescript-clean-code`, or `$alaa-golang-clean-code-principles`, alongside `$alaa-services-contract` and `$alaa-trust-gateway-auth` in Ala-style repositories.

## Specialist gates

### Architecture critic

Trigger before implementation for cross-cutting design: public contracts, service boundaries, consistency models, concurrency, caching semantics, distributed workflows. Skip for a local bug fix whose contract and ownership are established.

### API contract reviewer

Trigger when a public HTTP or RPC endpoint, event or message schema, shared DTO, SDK surface, or persisted serialization format changes shape. Prefer to trigger it in Phase A, before code exists, so the deprecation path and consumer impact are decided rather than discovered. Trigger it in Phase D instead when the contract change emerged during implementation. Skip when the change is internal to one module and no consumer outside it can observe the difference.

Distinct from the architecture critic, which judges whether the design is sound; this gate judges whether the transition is safe for existing consumers.

### Security reviewer

Trigger for authentication or authorization, tokens and sessions, secrets, untrusted inputs, upload and download, query or command construction, serialization, webhooks, payments, cryptography, tenant isolation, or privileged operations.

### Migration guardian

Trigger for DDL, constraints, defaults, nullability, index creation, data backfills, format transforms, cleanup or deletion, compatibility windows, or production data movement.

### Dependency auditor

Trigger when a dependency is added, upgraded, removed, or replaced, when a lockfile changes outside a scoped upgrade lane, or when a transitive tree shifts materially. Covers known vulnerabilities, license compatibility, maintenance signals, transitive blast radius, and lockfile integrity.

Distinct from the release guardian, which asks whether the change deploys and operates cleanly; this gate asks whether the dependency itself is safe to depend on.

### Accessibility reviewer

Trigger for new or changed user-visible interface: components, forms, dialogs, navigation, tables, and any flow a user completes with a keyboard or a screen reader. Covers semantics and landmarks, keyboard reachability and focus order, focus management across route and dialog transitions, visible focus indication, labelling and error association, contrast, motion preferences, and right-to-left layout correctness where the product ships an RTL locale.

Distinct from browser QA, which gathers functional evidence that a flow works; this gate judges whether the interface is usable by people who do not drive it with a mouse or read it visually.

### Browser QA

Trigger for user-visible browser behavior. Require an exact URL, environment, and scenario. Preserve `--browser chromium` and existing profile settings.

### Performance profiler

Trigger only when there is a measurable question, a comparable baseline, and a budget. Do not use as generic optimization advice.

### Observability reviewer

Trigger for async jobs, queues, retries, external service calls, failure and degraded paths, production critical flows, or new operational states.

### Release guardian

Trigger for CI/CD, Docker or container, package, lock, or version, configuration and environment, feature flags, deployment order, health checks, startup and shutdown, release notes, or rollback changes.

### Adversarial reviewer

Trigger only when the change is irreversible or has high blast radius — production data movement, auth or tenancy boundaries, a public contract break, deployment topology — or when `alaa-reviewer` and a specialist return conflicting verdicts that repository evidence does not settle.

It runs after the reviewer and any specialist gates, against the same complete change, with a deliberately different lens: attack the design's assumptions, look for the failure the correctness review would not think to look for, and state the strongest reason not to ship. It is the pack's only `xhigh` pin, and that budget is spent on breadth of attack rather than on depth of fix. Its output is a report to the user, not another fix cycle. Routing its findings back into implementation restarts a loop that has no natural end, because a fresh adversarial pass always finds something.

Never trigger it on a routine change. A second opinion on work that already passed its gates is cost without a decision attached.

## Failure routing

- Clear test failure owned by one lane: return to that implementer.
- Ambiguous, cross-lane, flaky, timeout, environment, or contamination failure: `alaa-failure-analyst` first.
- Security, migration, or architecture blocker: route the fix through `alaa-implementer-sol`.
- Contract-compatibility blocker: route the fix through the owning implementer with the contract reviewer's finding verbatim.
- Browser-only reproducible defect: browser QA provides evidence; the owning implementer fixes.
- Test infrastructure defect: create an explicit infrastructure implementation lane; the verifier never fixes it.
