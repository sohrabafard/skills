---
name: alaa-system-design
description: "Pre-implementation design method for a service, subsystem, or class set: bounding the subsystem, extend-versus-new-service decisions, contracts derived before code, data ownership, two compared candidates, and one reviewable design record. Use when asked to design, plan, architect, or scope new work, and before dispatching implementation when a change alters an interface another component calls, moves which component writes a piece of data, changes a consistency, ordering, or caching property, adds or removes a dependency, or creates a new deployable unit. Do not use for implementing a design already decided, for reviewing written code, or for a change touching no interface, no data owner, and no failure path; implement that directly. Route project policy to /alaa-project-constitution; envelopes, headers, and trust boundaries to /alaa-services-contract; timeout, retry, and shedding doctrine to /alaa-reliability-sla."
---

# Alaa System Design

Decide the shape of a subsystem before it is implemented, and record the decision so the next agent inherits it instead of re-deriving it.

The deliverable is one design record written on `assets/design-record-template.md`, in that template's section order, so that two agents designing the same subsystem from the same evidence produce recognisably the same record. A fleet whose designs come out differently every run cannot be reviewed, debugged, or extended by anyone who did not write them.

A **component** here is anything with its own state and its own interface — a service, a module inside a service, a worker, or a shared package — and the procedure is identical at every scale. Companion skills are written `/name` for Claude Code and `$name` for Codex; both forms name the same skill.

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

Both errors cost. A skipped pass relocates the decision into whichever function is written first, where the next service to integrate reads it out of the code and copies it, so one skipped pass sets a precedent rather than causing an isolated defect. An unnecessary pass spends the review attention the next real design needs and produces an all-"unchanged" record, which teaches readers to skim records, including the one that mattered.

## What this skill consumes

`/alaa-project-constitution` (`$alaa-project-constitution`) builds the project-intent model, matches the project's archetypes, and walks every owned surface against the archetype counterfactuals and the ten quality-bar obligations — then stops deliberately, forbidding an implementation or a number as the answer to any question it raises, because a policy with one design embedded in it outlives that design.

This skill answers those questions, under three rules that keep one obligation list from becoming two. First, read `CONSTITUTION.md` and the archetype identifiers it matched; when the repository has none, invoke that skill to match archetypes rather than matching them here. Second, carry every counterfactual its discovery raised against a surface this design touches into the record section that owns it, cite the archetype identifier, and answer it with a decision — `references/60-design-record.md` maps each counterfactual class to its section. Third, never copy the constitution's rows into the record and never re-derive its archetype match here, because two copies of one obligation list drift and the copy inside a design record is the one nobody updates. The traffic runs both ways: an answer stating what every service in the estate owes is a constitutional amendment rather than a line in one record, so route it back and say so — an estate-wide rule buried in one subsystem's record binds nobody.

## The procedure

Walk all seven steps in order; step N decides section N of the template, and the **Output** block below fixes what each step reports. A step whose subject does not apply is written as one line naming why, with the evidence that puts it out of scope — never omitted, because a missing section and a decided-not-applicable section look identical to a reviewer and only one of them was thought about. Read only the references whose condition the task meets, because loading the whole tree means the step was not scoped.

### Step 1 — Frame

State the outcome the subsystem owns before naming any component, and name the trigger condition that fired. A design framed as "build X" cannot be compared against an alternative, because every alternative that is not X is off-topic by construction; a design framed as the outcome can.

### Step 2 — Bound the subsystem

Inside the design is every component you may change within this change's release. A component you cannot change without another team's release is a dependency and enters the design as a contract you consume, never as code you plan to modify.

> **Extend by default.** A new capability is added to the component that already owns the data it reads and writes. Create a new deployable service only when the capability meets **at least two** of these five conditions, and record which two in the design record:
>
> 1. **Different data owner** — it owns state no existing service owns, and no existing service's owned state sits on its write path.
> 2. **Different failure domain** — a named journey must keep completing while the candidate host service is down, or the host service must keep serving while the capability is down.
> 3. **Different scaling axis** — its load moves with an input that does not move the host service's load, by a stated factor, so the two cannot share a replica count.
> 4. **Different trust or compliance boundary** — it holds data or credentials the host service is not permitted to hold, under a rule the repository or `/alaa-security-review` can name.
> 5. **Different runtime or lifecycle** — it needs a runtime, dependency, or release cadence the host service cannot adopt without changing its own.
>
> A capability meeting one condition or none is built inside the existing service as a module with its own internal boundary. One condition is not enough because every new service costs a deployment unit, a contract, a set of failure modes, an on-call surface, and one more place where the fleet's behaviour can diverge — a cost paid continuously — while the benefit of a single condition is almost always available from a module boundary at no cost.

Read `references/10-boundary-and-seam.md` when deciding what is inside the design, when finding the seam, when testing whether a boundary is real, when the plan requires an edit inside a dependency, when asking what evidence settles one of the five conditions, or when merging two services back.

### Step 3 — Derive the contract

**The contract is decided in the record and committed as the first implementation lane, before the code that satisfies it.** An implementation lane that has to invent a field name, a status code, or an error class was dispatched too early, and whatever it invents becomes the contract by default. Enumerate every interface into and out of the subsystem, fix the data shape on each, and derive the error surface each caller must handle.

Satisfy the platform invariants `/alaa-services-contract` (`$alaa-services-contract`) owns and cite them; never restate one in the record.

Read `references/20-contract-first.md` when enumerating interfaces, fixing data shapes, or deciding an error surface, and before committing any contract change.

### Step 4 — Settle data ownership and consistency

**Exactly one component writes each datum.** When two want to, either one is the owner and the other writes through it, or they are two different data sharing a name — decide which, in the record. Shared write access has no owner to ask when the values disagree, so the disagreement is settled by whichever write landed last.

**A second copy of data is a cache when deleting it at any moment loses nothing** — the system converges to the same answer by re-reading the owner — **and the record states its maximum age and its invalidation trigger. It is a fork when deletion loses information, or when anything writes to it that does not also write to the owner.** A fork carries a named reconciliation path and a rule for which copy wins; an unlabelled second copy becomes a fork silently, on the first write that reaches only one of them.

This step owns only who may write and what a stale read is allowed to cause; `/alaa-data-layer` (`$alaa-data-layer`) owns the mechanics that enforce it.

Read `references/30-data-and-consistency.md` when a datum's owner is unclear, when a read may be stale, when a second copy is proposed, or when two write paths can interleave.

### Step 5 — Classify every dependency before the design is finished

**A design with an unclassified dependency is unfinished, and this classification happens during design rather than during implementation.** A classification left to implementation is made by whoever writes the call site, one call site at a time, which is how two services come to behave differently against the same dependency.

This step owns only that the classification and the assumed load exist before the record is reviewable; the gate-versus-contributor rule behind the classification is `/alaa-reliability-sla`'s (`$alaa-reliability-sla`).

Read `references/40-failure-and-load-inputs.md` when building the dependency table, when a classification is disputed, or when the design states no load assumption yet.

### Step 6 — Compare at least two candidates

**A single-candidate design is a decision that was never made**, because a reviewer holding one candidate can only accept or reject the whole proposal; two candidates make the actual choice visible and arguable.

Two candidates are distinct only when they differ on a boundary, a data owner, or a consistency choice; two proposals differing in library, naming, or file layout are one candidate.

**Record each rejected candidate as one line: the candidate, the axis it lost on, and the condition that would make it win.** The condition is what stops the same debate reopening: when someone proposes the candidate again, the record answers in a minute instead of a meeting.

Read `references/50-alternatives-and-tradeoffs.md` when only one candidate exists, when candidates must be compared, or when recording a rejection.

### Step 7 — State rollout and reversal

Name the state of the system while old and new versions run together, because in a fleet that is a state the system occupies on every deploy rather than an edge case. State reversal in terms of what has accumulated — what a rollback does to data already written in the new shape, and whether the change is reversible at all — because a change that becomes irreversible after its first write is the sentence a reviewer weighs hardest. Where the change alters a surface a consumer can observe, the deprecation procedure in `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md` governs; cite it rather than inventing a window.

## Authority and side effects

A design pass writes exactly one file: the design record, plus the pointer files a multi-repository design requires. It changes no application code, no schema, no configuration, and no contract file; those are the first implementation lane, dispatched after the record is reviewed. A design that edited the code it proposes cannot be rejected, and a proposal that cannot be rejected is not a design pass.

## The design record

The record lives in the repository of the component that owns the data, at `docs/design/<NNNN>-<slug>.md`. Keep it to two screens; a long record is less likely to be read, and an unread record governs nothing.

Read `references/60-design-record.md` when creating, numbering, superseding, or judging a record, when a record will not fit two screens, and when the design spans more than one repository.

## Review and readiness

A design is reviewed before any implementation lane is dispatched, and a record nobody has reviewed is a draft whatever its status line says.

Read `references/70-review-and-readiness.md` when reviewing a record, when deciding whether a finding blocks, and when handing a reviewed record to an implementation lane.

## When NOT to use

- The design is already decided and recorded. Implement it; re-deriving it is not review.
- The task is reviewing code that already exists.
- The change touches no interface another component calls, moves no data owner, alters no consistency,
  ordering, or caching property, adds and removes no dependency, and creates no deployable unit.
- The question is project policy, a platform invariant, or a failure-doctrine rule. The routing table
  below names each owner.

## Stop conditions

Stop successfully when every section of the record carries either a decision or a stated non-applicability with its evidence; the reviewer's blocking findings are resolved in the record rather than deferred into implementation; and the record's status reads `reviewed`.

Stop and report a blocked state when: a dependency cannot be classified as gate or contributor from the code and the repository's documentation; a datum needs two writers and no owner can be named without a decision that belongs to the user; the extend-or-create decision turns on a trust or compliance rule the repository does not state, which goes to `/alaa-security-review` (`$alaa-security-review`) and then to the user; no second candidate can be constructed even from the do-nothing generator in `references/50-alternatives-and-tradeoffs.md`, which means the problem is not yet stated as a design problem; or the design would change a surface a live external consumer depends on with no deprecation window open under `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md`.

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

## What this skill does not own

This skill owns the **method**: what must be decided, in what order, and what makes the result reviewable. It names no model and states no numeric threshold. Where a rule here and a rule below disagree, the skill named below wins for its half and the weaker statement here is deleted rather than kept as a second opinion.

| Not owned here | Owner |
|---|---|
| Project policy, archetype and quality-bar obligations, and the intent model and counterfactuals consumed above | `/alaa-project-constitution` — `$alaa-project-constitution` |
| Envelopes, correlation and trusted gateway headers, the public identifier boundary, the trust boundary, event, code and permission names, and the deprecation procedure | `/alaa-services-contract` — `$alaa-services-contract` |
| Every Ala timeout, retry, pool, acquire-wait, and shed value, with the wire behaviour carrying it | `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md` |
| Failure doctrine: gate-versus-contributor discrimination, deadlines, retries, breakers, bulkheads, admission and shedding, degradation, idempotency, error budgets, and their evidence | `/alaa-reliability-sla` — `$alaa-reliability-sla` |
| Trust-boundary review, authn and authz decisions, tenant isolation, fail-closed doctrine, every security verdict | `/alaa-security-review` — `$alaa-security-review` |
| Signal selection, instrumentation requirement levels, cardinality and sampling budgets, alerting, retention, SOC evidence | `/alaa-observability-soc` — `$alaa-observability-soc` |
| Schema, constraints, indexes, migrations, isolation semantics, pooling mechanics, projections, Redis behaviour | `/alaa-data-layer` — `$alaa-data-layer` |
| Broker prefetch, acknowledgement, consumer concurrency, dead-letter mechanics | `/alaa-async-messaging` — `$alaa-async-messaging` |
| Dispatching and gating the implementation lanes a reviewed design produces, and the `alaa-architecture-critic` role that runs this review with its verdict vocabulary | `/alaa-cc-orchestrator` — `$alaa-codex-orchestrator` |
| Plan files, resumable state, and phase prompt packs for a design spanning sessions | `/alaa-workflow` — `$alaa-workflow` |
| What proves a design's behaviour: the layer a behaviour is tested at, whether a double is honest, the six proof levels, and what evidence a review accepts | `/alaa-testing-strategy` — `$alaa-testing-strategy` |
| The complexity budget on a path this design creates, the real bound on a growing input dimension, structure choice from the access pattern, and the N+1 family | `/alaa-algorithms-data-structures` — `$alaa-algorithms-data-structures` |
| Language idiom, patterns, and refactoring inside a component | the per-language clean-code skills, named per stack |
| Model selection, effort selection, prompting, and skill or agent authoring | `/alaa-prompting-guide` — `$alaa-prompting-guide` |
