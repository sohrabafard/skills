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
- the lead would otherwise guess file scope.

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

Use `alaa-implementer` by default. Escalation is earned by decision density, not surface sensitivity: a lane that mechanically applies an already-ratified decision, an amended contract value, or a precise spec stays on the default implementer regardless of the surface it touches — the reviewer and specialist gates already provide Opus-tier scrutiny there.

Dispatch `alaa-implementer-opus` only when the lane itself must make non-obvious design decisions and at least one of these applies. Record which one in the dispatch:

- public API, event, or data contract changes;
- service boundaries or architecture decisions;
- concurrency, races, locking, distributed ordering, idempotency;
- auth or trust boundary, or cryptographic correctness;
- schema or data migration coupled to application logic;
- complex backwards compatibility or rollout;
- multiple plausible designs with materially different failure behavior;
- **authoring or rewriting an artifact whose deliverable is judgment itself** — a skill, a prompt, an agent definition, an `AGENTS.md` or `CLAUDE.md`, an architecture document, or a standard other agents will follow.

That last criterion exists because the preceding six describe software surfaces, and a lane can be judgment-dense without touching any of them. Writing a skill is not mechanical application of a ratified decision: deciding what belongs in the body versus a reference, which rules to merge or delete, and whether the result actually meets its own bar is the entire work.

The wording carries as much of that weight as the structure. In these artifacts the prose *is* the executable logic — there is no compiler underneath to enforce what a sentence failed to say — so an ambiguous phrasing, a preference verb where a constraint was meant, or a rule with no stated scope becomes wrong behavior on every future run. Drafting that text is the judgment, not the write-up of it.

A lane like this reads as "no named criterion applies" against a purely software-shaped list, and would then be dispatched to the default implementer — contradicting the decision-density rule the list is supposed to serve. Judge the density, not the file extension.

When uncertain, do not escalate: dispatch the default implementer and let the review gate decide. One justified re-dispatch after evidence is cheaper than habitual escalation.

Never raise a Sonnet lane's effort above `high` as a substitute for escalating. Above that ceiling, the correct move is a different model, not a bigger thinking budget.

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

It runs after the reviewer and any specialist gates, against the same complete change, with a deliberately different lens: attack the design's assumptions, look for the failure the correctness review would not think to look for, and state the strongest reason not to ship. Its output is a report to the user, not another fix cycle. Routing its findings back into implementation restarts a loop that has no natural end, because a fresh adversarial pass always finds something.

Never trigger it on a routine change. A second opinion on work that already passed its gates is cost without a decision attached.

## Failure routing

- Clear test failure owned by one lane: return to that implementer.
- Ambiguous, cross-lane, flaky, timeout, environment, or contamination failure: `alaa-failure-analyst` first.
- Security, migration, or architecture blocker: route the fix through `alaa-implementer-opus`.
- Contract-compatibility blocker: route the fix through the owning implementer with the contract reviewer's finding verbatim.
- Browser-only reproducible defect: browser QA provides evidence; the owning implementer fixes.
- Test infrastructure defect: create an explicit infrastructure implementation lane; the verifier never fixes it.
