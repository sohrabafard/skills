---
name: alaa-system-design
description: "Pre-implementation design method for a service, subsystem, or class set: bounding the subsystem, extend-versus-new-service decisions, contracts derived before code, data ownership and consistency, dependency classification, two compared candidates, and one reviewable design record. Use when asked to design, plan, architect, or scope new work, and before dispatching implementation when a change alters an interface another component calls, moves which component writes a piece of data, changes a consistency, ordering, concurrency or caching property, adds or removes a dependency, or creates a new deployable unit. Do not use for implementing a design already decided, for reviewing code after it is written, or for a change touching no interface, no data owner and no failure path — implement that directly. Route project policy to /alaa-project-constitution, envelopes, headers, identifiers and trust boundaries to /alaa-services-contract, timeout, retry and shedding doctrine to /alaa-reliability-sla, model and effort to /alaa-prompting-guide."
---

# Alaa System Design

Decide the shape of a subsystem before it is implemented, and record the decision so the next agent inherits it instead of re-deriving it. This skill is the method: what is inside the design, where the seam runs, what the contract is, who owns each datum, what happens when each dependency fails, which alternative was rejected and why, and what makes the design ready to build.

The deliverable is one design record with a fixed section order. Two agents designing the same subsystem from the same evidence produce recognisably the same record, because the procedure below fixes what must be decided and `assets/design-record-template.md` fixes where each decision goes. A fleet whose designs come out differently every run cannot be reviewed, debugged, or extended by anyone who did not write them.

This skill owns no platform value and no failure doctrine; each has a named owner under **What this skill does not own**, and a number restated here drifts without either file changing. A **component** here is anything with its own state and its own interface — a service, a module inside a service, a worker, or a shared package — and the procedure is identical at every scale. Companion skills are written `/name` for Claude Code and `$name` for Codex; both forms name the same skill.

## When a design pass is required

Run a design pass before implementation when the change meets any one of these six conditions:

1. it adds, removes, or changes the shape of an interface another component calls — a route, an emitted or consumed event, a job payload, a shared DTO, or a published client;
2. it changes which component writes a piece of data, or adds a second stored copy of data that already has an owner;
3. it changes a consistency, ordering, idempotency, concurrency, or caching property of an existing path;
4. it adds a dependency between two components that did not depend on each other, or removes one that exists;
5. it creates a new deployable unit, or moves a capability from one deployable unit to another;
6. it changes what a caller sees when a dependency is slow, unavailable, or returning errors.

A change meeting none of the six is implemented directly and reviewed as code. The gate is these six conditions rather than the size, cost, or importance of the change, because size and importance are judged differently by every agent while all six of these are readable from the diff and the ticket.

**A design pass that produces no decision was not needed.** When the boundary, ownership, and consistency sections all read "unchanged" and only one real candidate exists, close the record with status `not-required`, name which of the six conditions misfired, and implement directly. Recording the misfire is what keeps the trigger list honest; closing the record silently means the same misfire fires again next month.

Both errors cost. **Skipping a required pass** relocates the decision into whichever function is written first, where the next service to integrate finds it by reading code — and in a fleet that decision is then copied by the next service that looks like this one, so one skipped pass sets a precedent rather than causing an isolated defect. **Running a pass on a change meeting none of the six** spends the review attention the next real design needs and produces a record whose sections all read "unchanged", which teaches readers to skim records, including the one that mattered.

## What this skill consumes

`/alaa-project-constitution` (`$alaa-project-constitution`) builds the project-intent model — users and consumers, the owned outcome, the critical journeys, the runtime and data surfaces, the trust boundaries, the load-bearing qualities — matches the project's archetypes, and walks every owned surface against the archetype counterfactuals and the ten quality-bar obligations. It then stops deliberately: it raises the questions and forbids answering them with an implementation or a number, because a constitution states policy, and a policy with one design embedded in it outlives that design.

This skill answers them. Read `CONSTITUTION.md` and the archetype identifiers it matched; when the repository has none, invoke that skill to match archetypes rather than matching them here. Then carry every counterfactual its discovery raised against a surface this design touches — peak load, dependency outage, process restart, duplicate delivery, concurrent writes, stale cache, network interruption, partial rollout, expired credentials, storage exhaustion, rollback — into the record section that owns it, cite the archetype identifier, and answer it with a decision; `references/60-design-record.md` maps each counterfactual class to its section. Never copy the constitution's rows into the record and never re-derive its archetype match here, because two copies of one obligation list drift and the copy inside a design record is the one nobody updates. The traffic runs both ways: an answer stating what every service in the estate owes is a constitutional amendment rather than a line in one record, so route it back and say so — an estate-wide rule buried in one subsystem's record binds nobody.

## The procedure

Walk all seven steps in order. Each names the record section it fills and the reference that owns its detail. A step whose subject does not apply is written as one line naming why, with the evidence that puts it out of scope — never omitted, because a missing section and a decided-not-applicable section look identical to a reviewer and only one of them was thought about.

### Step 1 — Frame

Produce: the problem in two sentences, the trigger condition that fired, the journeys affected, and the archetype rows and counterfactuals carried in from the constitution.

State the outcome the subsystem owns before naming any component. A design framed as "build X" cannot be compared against an alternative, because every alternative that is not X is off-topic by construction; a design framed as the outcome can.

### Step 2 — Bound the subsystem

Produce: the components inside this design, the dependencies outside it with their owners, where the seam runs, and the extend-or-create decision.

Inside the design is every component you may change within this change's release. A component you cannot change without another team's release is a dependency and enters the design as a contract you consume, never as code you plan to modify. When the plan requires an edit inside a dependency, that is either a second design or a contract change: split it and name which.

> **Extend by default.** A new capability is added to the component that already owns the data it reads and writes. Create a new deployable service only when the capability meets **at least two** of these five conditions, and record which two in the design record:
>
> 1. **Different data owner** — it owns state no existing service owns, and no existing service's owned state sits on its write path.
> 2. **Different failure domain** — a named journey must keep completing while the candidate host service is down, or the host service must keep serving while the capability is down.
> 3. **Different scaling axis** — its load moves with an input that does not move the host service's load, by a stated factor, so the two cannot share a replica count.
> 4. **Different trust or compliance boundary** — it holds data or credentials the host service is not permitted to hold, under a rule the repository or `/alaa-security-review` can name.
> 5. **Different runtime or lifecycle** — it needs a runtime, dependency, or release cadence the host service cannot adopt without changing its own.
>
> A capability meeting one condition or none is built inside the existing service as a module with its own internal boundary. One condition is not enough because every new service costs a deployment unit, a contract, a set of failure modes, an on-call surface, and one more place where the fleet's behaviour can diverge — a cost paid continuously — while the benefit of a single condition is almost always available from a module boundary at no cost.

Detail: `references/10-boundary-and-seam.md`.

### Step 3 — Derive the contract

Produce: every interface into and out of the subsystem, the data shape on each, and the error surface each caller must handle.

**The contract is decided in the record and committed as the first implementation lane, before the code that satisfies it.** "Before" is checkable: the commit that adds the route, the consumer, or the handler is not the commit that first states its shape. An implementation lane that has to invent a field name, a status code, or an error class was dispatched too early, and whatever it invents becomes the contract by default.

`/alaa-services-contract` (`$alaa-services-contract`) owns the platform invariants every Ala design satisfies — response envelopes, correlation and trusted gateway headers, the public identifier boundary, the trust boundary, event and code names, and the deprecation procedure for changing any of them. Satisfy them and cite them; do not restate them in the record.

Detail: `references/20-contract-first.md`.

### Step 4 — Settle data ownership and consistency

Produce: every piece of data the design touches with exactly one owning component, the read path and write path for each critical journey, the consistency each interaction needs, and every second copy labelled.

**Exactly one component writes each datum.** When two want to, either one is the owner and the other writes through it, or they are two different data sharing a name — decide which, in the record. Shared write access has no owner to ask when the values disagree, so the disagreement is settled by whichever write landed last.

**A second copy of data is a cache when deleting it at any moment loses nothing** — the system converges to the same answer by re-reading the owner — **and the record states its maximum age and its invalidation trigger. It is a fork when deletion loses information, or when anything writes to it that does not also write to the owner.** A fork carries a named reconciliation path and a rule for which copy wins; an unlabelled second copy becomes a fork silently, on the first write that reaches only one of them.

`/alaa-data-layer` (`$alaa-data-layer`) owns the mechanics — schema, constraints, indexes, isolation, pooling, projections, Redis behaviour. This step owns which component may write, and what a stale read is allowed to cause.

Detail: `references/30-data-and-consistency.md`.

### Step 5 — Classify every dependency before the design is finished

Produce: one row per dependency carrying its classification, what the caller sees when it fails, the load the design assumes for it, and where its bounds come from.

**A design with an unclassified dependency is unfinished, and this classification happens during design rather than during implementation.** A reviewer holding an unclassified dependency cannot tell whether its failure is an outage or a degradation, so cannot judge the design against the journey; and a classification left to implementation is made by whoever writes the call site, one call site at a time, which is how two services come to behave differently against the same dependency.

`/alaa-reliability-sla` (`$alaa-reliability-sla`) owns the doctrine — the gate-versus-contributor discrimination rule, deadlines, retries, breakers, bulkheads, shedding, degradation, idempotency, and the evidence each mechanism demands. `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md` owns the Ala values. This step owns only that the classification and the assumed load exist before the record is reviewable.

Detail: `references/40-failure-and-load-inputs.md`.

### Step 6 — Compare at least two candidates

Produce: two or more distinct candidates, the winner with the axis it won on, and each rejected candidate with the axis it lost on and the condition that would make it win.

**A single-candidate design is a decision that was never made**, because a reviewer holding one candidate can only accept or reject the whole proposal, and rejecting the whole proposal is expensive enough that it rarely happens. Two candidates make the actual choice visible and arguable.

Two candidates are distinct only when they differ on a boundary, a data owner, or a consistency choice; two proposals differing in library, naming, or file layout are one candidate.

**Record each rejected candidate as one line: the candidate, the axis it lost on, and the condition that would make it win.** The condition is what stops the same debate reopening in six months — when someone proposes it again, the record answers either "the condition has not changed" or "it has, so revisit this", and both answers take a minute instead of a meeting.

Detail: `references/50-alternatives-and-tradeoffs.md`.

### Step 7 — State rollout and reversal

Produce: the order in which the parts ship, what the system does between the first deploy and the last, and what undoes the change.

Name the state of the system while old and new versions run together, because in a fleet that is a state the system occupies on every deploy rather than an edge case. Where the change alters a surface a consumer can observe, the deprecation procedure in `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md` governs; cite it rather than inventing a window. State reversal in terms of what has accumulated — what a rollback does to data already written in the new shape, and whether the change is reversible at all — because a change that becomes irreversible after its first write is the sentence a reviewer weighs hardest.

## Authority and side effects

A design pass writes exactly one file: the design record, plus a one-line pointer file in each other repository when the design spans repositories. It changes no application code, no schema, no configuration, and no contract file; those are the first implementation lane, dispatched after the record is reviewed. A design that edited the code it proposes cannot be rejected, and a proposal that cannot be rejected is not a design pass.

## The design record

The record lives in the repository of the component that owns the data, at `docs/design/<NNNN>-<slug>.md`. Copy `assets/design-record-template.md` and keep its section order, because the fixed order is what makes two records comparable and a missing decision visible. Keep it to two screens: anything longer is either a specification, which belongs in the contract files the record points at, or a discussion, which belongs in the rejected-candidate lines.

Detail — status lifecycle, superseding, the reviewable-versus-decorative test, and multi-repository designs: `references/60-design-record.md`.

## Review and readiness

A design is reviewed before any implementation lane is dispatched. Under `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) that review runs as the `alaa-architecture-critic` role, already gated on contract, boundary, consistency, concurrency, and caching changes; this skill is the standard that role reviews against, and the verdict vocabulary is that role's. A human reviewer applies the same checks and reaches the same verdicts.

Detail — what a reviewer checks per step, which findings block, what the reviewer must not do, and what an implementation lane may decide alone versus escalate back: `references/70-review-and-readiness.md`.

## Stop conditions

Stop successfully when every section of the record carries either a decision or a stated non-applicability with its evidence; the reviewer's blocking findings are resolved in the record rather than deferred into implementation; and the record's status reads `reviewed`.

Stop and report a blocked state when: a dependency cannot be classified as gate or contributor from the code and the repository's documentation; a datum needs two writers and no owner can be named without a decision that belongs to the user; the extend-or-create decision turns on a trust or compliance rule the repository does not state, which goes to `/alaa-security-review` and then to the user; no second candidate can be constructed even from the do-nothing generator in `references/50-alternatives-and-tradeoffs.md`, which means the problem is not yet stated as a design problem; or the design would change a surface a live external consumer depends on with no deprecation window open under `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md`.

## Output

Return this, in this order, for every design pass:

```text
Outcome: design ready | design blocked | not required
Record: path, status, and the trigger condition that fired
Scope: components inside, dependencies outside with owners, seam and its test results
Boundary decision: extend <component> | new service, with the conditions met
Contract: interfaces added or changed, and where each shape is committed
Data: each datum -> owning component; each second copy -> cache | fork with its rule
Dependencies: each -> classification, caller-visible failure, assumed load, source of bounds
Candidates: winner with the axis it won on; each rejected with its axis and reviving condition
Rollout: ship order, mixed-version behaviour, reversal, irreversibility if any
Constitution: counterfactuals answered; amendments routed back
Open questions: each with the decision it blocks, or "blocks nothing"
```

## Reference routing

Read only the files whose condition the task meets. Loading the whole tree means the step was not scoped.

- `references/10-boundary-and-seam.md` — when deciding what is inside the design, where the seam runs, whether a proposed service boundary is real, or whether two services should merge back.
- `references/20-contract-first.md` — when enumerating interfaces, fixing data shapes, or deciding an error surface, and before committing any contract change.
- `references/30-data-and-consistency.md` — when a datum's owner is unclear, a read may be stale, a second copy is proposed, or two write paths can interleave.
- `references/40-failure-and-load-inputs.md` — when building the dependency table, when a classification is disputed, or when the design states no load assumption yet.
- `references/50-alternatives-and-tradeoffs.md` — when only one candidate exists, when candidates must be compared, or when recording a rejection.
- `references/60-design-record.md` — when creating, superseding, or judging a record, and when the design spans more than one repository.
- `references/70-review-and-readiness.md` — when reviewing a record, when deciding whether a finding blocks, and when handing a reviewed record to an implementation lane.

## What this skill does not own

This skill owns the **method**: what must be decided, in what order, and what makes the result reviewable. Where a rule here and a rule below disagree, the skill named below wins for its half and the weaker statement here is deleted rather than kept as a second opinion.

| Not owned here | Owner |
|---|---|
| Project policy, archetype obligations, the ten quality-bar obligations, and the intent model and counterfactuals consumed above | `/alaa-project-constitution` — `$alaa-project-constitution` |
| Envelopes, correlation and trusted gateway headers, the public identifier boundary, the trust boundary, event, code and permission names, and the deprecation procedure | `/alaa-services-contract` — `$alaa-services-contract` |
| Every Ala timeout, retry, pool, acquire-wait, and shed value, with the wire behaviour carrying it | `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md` |
| Failure doctrine: gate-versus-contributor discrimination, deadlines, retries, breakers, bulkheads, admission and shedding, degradation, idempotency, error budgets, and their evidence | `/alaa-reliability-sla` — `$alaa-reliability-sla` |
| Trust-boundary review, authn and authz decisions, tenant isolation, fail-closed doctrine, every security verdict | `/alaa-security-review` — `$alaa-security-review` |
| Signal selection, instrumentation requirement levels, cardinality and sampling budgets, alerting, retention, SOC evidence | `/alaa-observability-soc` — `$alaa-observability-soc` |
| Schema, constraints, indexes, migrations, isolation semantics, pooling mechanics, projections, Redis behaviour | `/alaa-data-layer` — `$alaa-data-layer` |
| Broker prefetch, acknowledgement, consumer concurrency, dead-letter mechanics | `/alaa-async-messaging` — `$alaa-async-messaging` |
| Dispatching, gating, and reconciling the implementation lanes a reviewed design produces, and the `alaa-architecture-critic` verdict vocabulary | `/alaa-cc-orchestrator` — `$alaa-codex-orchestrator` |
| Plan files, resumable state, and phase prompt packs for a design spanning sessions | `/alaa-workflow` — `$alaa-workflow` |
| Language idiom, patterns, and refactoring inside a component | the per-language clean-code skills, named per stack |
| Model selection, effort selection, prompting, and skill or agent authoring | `/alaa-prompting-guide` — `$alaa-prompting-guide` |

This skill names no model and states no numeric threshold.

## Anti-patterns

- running a design pass on a change that meets none of the six trigger conditions, and closing it as complete rather than as `not-required`;
- creating a new service on one condition, or because the capability "feels separate";
- drawing a boundary around a noun — an entity, a table, a page — rather than around a set of data with one writer;
- writing the handler first and deriving the contract from what it happened to return, or documenting the success shape and leaving the error surface to whoever writes the first catch block;
- a second copy of data introduced "for performance" with no label, no maximum age, and no invalidation trigger;
- a dependency table completed after implementation, when every call site has already chosen its own failure behaviour;
- a second candidate constructed to lose, or one that is the winner under different names;
- recording the winner and dropping the rejected candidates, so the same debate reopens with no record of its last outcome;
- restating a value from `/alaa-services-contract` or a doctrine from `/alaa-reliability-sla` in the record instead of citing it, which produces a second copy that drifts;
- deferring an interface shape, a data owner, or a consistency choice to "we will decide in implementation", which is the design pass declining to be a design pass.
