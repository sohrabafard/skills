---
name: alaa-system-design
description: "Pre-implementation design method for a service, subsystem, or class set: bounding the subsystem, extend-versus-new-service decisions, contracts derived before code, data ownership, two compared candidates, and one reviewable design record. Use when asked to design, plan, architect, or scope new work, and before dispatching implementation when a change alters an interface another component calls, moves which component writes a piece of data, changes a consistency, ordering, or caching property, adds or removes a dependency, or creates a new deployable unit. Do not use for implementing a design already decided, for reviewing written code, or for a change touching no interface, no data owner, and no failure path; implement that directly. Route project policy to /alaa-project-constitution; envelopes, headers, and trust boundaries to /alaa-services-contract; timeout, retry, and shedding doctrine to /alaa-reliability-sla."
---

# Alaa System Design

Decide the shape of a subsystem before implementation. Record the decision, so the next agent inherits it instead of re-deriving it.

The deliverable is one design record. Write it on `assets/design-record-template.md`, in that template's section order. Then two agents that design the same subsystem from the same evidence produce recognisably the same record. A fleet whose designs differ on every run cannot be reviewed, debugged, or extended by anyone who did not write them.

A **component** is anything with its own state and its own interface: a service, a module inside a service, a worker, or a shared package. The procedure is identical at every scale. Write cross-skill references as `/name`.

## When a design pass is required

Run a design pass before implementation when the change meets any one of these six conditions:

1. it adds, removes, or changes the shape of an interface another component calls — a route, an emitted or consumed event, a job payload, a shared DTO, or a published client;
2. it changes which component writes a piece of data, or adds a second stored copy of data that already has an owner;
3. it changes a consistency, ordering, idempotency, concurrency, or caching property of an existing path;
4. it adds a dependency between two components that did not depend on each other, or removes one that exists;
5. it creates a new deployable unit, or moves a capability from one deployable unit to another;
6. it changes what a caller sees when a dependency is slow, unavailable, or returning errors.

Implement a change that meets none of the six directly, and review it as code. The gate is these six conditions, not the size, cost, or importance of the change. Every agent judges size and importance differently. All six conditions are readable from the diff and the ticket.

**A design pass that produces no decision was not needed.** When the boundary, ownership, and consistency sections all read "unchanged" and only one real candidate exists, do these steps: close the record with status `not-required`; name which of the six conditions misfired; implement directly. Recording the misfire keeps the trigger list honest. Closing the record silently means the same misfire fires again next month.

Both errors cost. A skipped pass puts the decision into whichever function is written first, and the next service to integrate copies it from the code, so the defect becomes a precedent. An unnecessary pass spends the review attention the next real design needs, and its all-"unchanged" record teaches readers to skim records, including the one that mattered.

## What this skill consumes

`/alaa-project-constitution` builds the project-intent model, matches the project's archetypes, and walks every owned surface against the archetype counterfactuals and the ten quality-bar obligations. It then stops deliberately. It forbids an implementation or a number as the answer to any question it raises, because a policy with one design embedded in it outlives that design.

This skill answers those questions under three rules. The rules keep one obligation list from becoming two.

1. Read `CONSTITUTION.md` and the archetype identifiers it matched. When the repository has none, invoke that skill to match archetypes. Do not match them here.
2. Carry every counterfactual its discovery raised against a surface this design touches into the record section that owns it. Cite the archetype identifier. Answer it with a decision. `references/60-design-record.md` maps each counterfactual class to its section.
3. Never copy the constitution's rows into the record. Never re-derive its archetype match here. Two copies of one obligation list drift, and the copy inside a design record is the one nobody updates.

The traffic runs both ways. An answer that states what every service in the estate owes is a constitutional amendment, not a line in one record. Route it back and say so, because an estate-wide rule buried in one subsystem's record binds nobody.

## The procedure

Walk all seven steps in order. Step N decides section N of the template. The **Output** block below fixes what each step reports. Write a step whose subject does not apply as one line that names why, with the evidence that puts it out of scope. Never omit a step, because a missing section and a decided-not-applicable section look identical to a reviewer, and only one of them was thought about. Read only the references whose condition the task meets. Loading the whole tree means the step was not scoped.

### Step 1 — Frame

State the outcome the subsystem owns before you name any component. Name the trigger condition that fired. A design framed as "build X" cannot be compared against an alternative, because every alternative that is not X is off-topic by construction. A design framed as the outcome can.

### Step 2 — Bound the subsystem

Every component you may change within this change's release is inside the design. A component you cannot change without another team's release is a dependency. It enters the design as a contract you consume, never as code you plan to modify.

> **Extend by default.** Add a new capability to the component that already owns the data it reads and writes. Create a new deployable service only when the capability meets **at least two** of these five conditions, and record which two in the design record:
>
> 1. **Different data owner** — it owns state no existing service owns, and no existing service's owned state sits on its write path.
> 2. **Different failure domain** — a named journey must keep completing while the candidate host service is down, or the host service must keep serving while the capability is down.
> 3. **Different scaling axis** — its load moves with an input that does not move the host service's load, by a stated factor, so the two cannot share a replica count.
> 4. **Different trust or compliance boundary** — it holds data or credentials the host service is not permitted to hold, under a rule the repository or `/alaa-security-review` can name.
> 5. **Different runtime or lifecycle** — it needs a runtime, dependency, or release cadence the host service cannot adopt without changing its own.
>
> Build a capability that meets one condition or none inside the existing service, as a module with its own internal boundary. One condition is not enough. Every new service costs a deployment unit, a contract, a set of failure modes, an on-call surface, and one more place where the fleet's behaviour can diverge. That cost is paid continuously. A module boundary almost always gives the benefit of a single condition at no cost.

Read `references/10-boundary-and-seam.md` when deciding what is inside the design, when finding the seam, when testing whether a boundary is real, when the plan requires an edit inside a dependency, when asking what evidence settles one of the five conditions, or when merging two services back.

### Step 3 — Derive the contract

**Decide the contract in the record before implementation. Write its contract files in the first implementation lane, before the code that satisfies them.** Commit timing follows Review and readiness below. An implementation lane that has to invent a field name, a status code, or an error class was dispatched too early. Whatever it invents becomes the contract by default. Enumerate every interface into and out of the subsystem. Fix the data shape on each. Derive the error surface each caller must handle.

Satisfy the platform invariants `/alaa-services-contract` owns, and cite them. Never restate one in the record.

Read `references/20-contract-first.md` when enumerating interfaces, fixing data shapes, or deciding an error surface, and before committing any contract change.

### Step 4 — Settle data ownership and consistency

**Exactly one component writes each datum.** When two components want to write it, decide in the record which case holds: one is the owner and the other writes through it, or they are two different data that share a name. Shared write access has no owner to ask when the values disagree, so whichever write landed last settles the disagreement.

**A second copy of data is a cache when deleting it at any moment loses nothing.** The system then converges to the same answer by re-reading the owner. **The record states a cache's maximum age and its invalidation trigger.** **A second copy is a fork when deletion loses information, or when anything writes to it that does not also write to the owner.** A fork carries a named reconciliation path and a rule for which copy wins. An unlabelled second copy becomes a fork silently, on the first write that reaches only one of them.

This step owns only who may write and what a stale read is allowed to cause. `/alaa-data-layer` owns the mechanics that enforce it.

Read `references/30-data-and-consistency.md` when a datum's owner is unclear, when a read may be stale, when a second copy is proposed, or when two write paths can interleave.

### Step 5 — Classify every dependency before the design is finished

**A design with an unclassified dependency is unfinished. Classify each dependency during design, not during implementation.** A classification left to implementation is made by whoever writes the call site, one call site at a time. That is how two services come to behave differently against the same dependency.

This step owns only this: the classification and the assumed load exist before the record is reviewable. `/alaa-reliability-sla` owns the gate-versus-contributor rule behind the classification.

Read `references/40-failure-and-load-inputs.md` when building the dependency table, when a classification is disputed, or when the design states no load assumption yet.

### Step 6 — Compare at least two candidates

**A single-candidate design is a decision that was never made.** A reviewer holding one candidate can only accept or reject the whole proposal. Two candidates make the actual choice visible and arguable.

Two candidates are distinct only when they differ on a boundary, a data owner, or a consistency choice. Two proposals that differ in library, naming, or file layout are one candidate.

**Record each rejected candidate as one line: the candidate, the axis it lost on, and the condition that would make it win.** The condition stops the same debate from reopening. When someone proposes the candidate again, the record answers in a minute instead of a meeting.

Read `references/50-alternatives-and-tradeoffs.md` when only one candidate exists, when candidates must be compared, or when recording a rejection.

### Step 7 — State rollout and reversal

Name the state of the system while old and new versions run together. In a fleet, the system occupies that state on every deploy, so it is not an edge case. State reversal in terms of what has accumulated: what a rollback does to data already written in the new shape, and whether the change is reversible at all. A change that becomes irreversible after its first write is the sentence a reviewer weighs hardest. Where the change alters a surface a consumer can observe, the deprecation procedure in `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md` governs. Cite it rather than inventing a window.

## Authority and side effects

A design pass writes exactly one file: the design record, plus the pointer files a multi-repository design requires. It changes no application code, no schema, no configuration, and no contract file. Those belong to implementation under Review and readiness below. A design that edited the code it proposes cannot be rejected, and a proposal that cannot be rejected is not a design pass.

## The design record

The record lives in the repository of the component that owns the data, at `docs/design/<NNNN>-<slug>.md`. Keep it to two screens. A long record is less likely to be read, and an unread record governs nothing.

Read `references/60-design-record.md` when creating, numbering, superseding, or judging a record, when a record will not fit two screens, and when the design spans more than one repository.

## Review and readiness

Complete the design decisions before implementation. Under /alaa-cc-orchestrator or /alaa-codex-orchestrator, inherit the plan cadence and the exact phase, task and subtask cursor through that orchestrator's `references/verification-and-gates.md` section `Review boundary and execution cadence`. That section owns review and commit timing. A decision-complete draft may guide implementation pending that boundary. It is not reviewed acceptance. Return missing or inconsistent cadence to the plan owner before dependent dispatch.

Standalone, without an orchestrator, review the record before you dispatch implementation. An unreviewed record remains `draft` in either mode. Only independent judgment with blocking findings resolved earns `reviewed`.

Read `references/70-review-and-readiness.md` when reviewing a record, when deciding whether a finding blocks, and when handing a record to an implementation lane.

## When NOT to use

- The design is already decided and recorded. Implement it; re-deriving it is not review.
- The task is reviewing code that already exists.
- The change touches no interface another component calls, moves no data owner, alters no consistency, ordering, or caching property, adds and removes no dependency, and creates no deployable unit.
- The question is project policy, a platform invariant, or a failure-doctrine rule. `references/80-ownership-boundaries.md` names each owner.

## Stop conditions

Finish design authoring when every section carries a decision or evidenced non-applicability. Under orchestration, return the record with review and commit pending until the inherited boundary. Resolve blocking findings in the record before reviewed acceptance. Standalone success requires those findings resolved and status `reviewed`.

Stop and report a blocked state when any of these holds:

- a dependency cannot be classified as gate or contributor from the code and the repository's documentation;
- a datum needs two writers and no owner can be named without a decision that belongs to the user;
- the extend-or-create decision turns on a trust or compliance rule the repository does not state, which goes to `/alaa-security-review` and then to the user;
- no second candidate can be constructed even from the do-nothing generator in `references/50-alternatives-and-tradeoffs.md`, which means the problem is not yet stated as a design problem;
- the design would change a surface a live external consumer depends on, with no deprecation window open under `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md`.

## Output

Return this, in this order, for every design pass:

```text
Outcome: design ready | design authored, review pending | design blocked | not required
Record: path, status, and the trigger condition that fired
Scope: components inside, dependencies outside with owners, seam and its test results
Boundary decision: extend <component> | new service, with the conditions met
Contract: interfaces added or changed, shape paths, pending commit if any
Data: each datum -> owning component; each second copy -> cache | fork with its rule
Dependencies: each -> classification, caller-visible failure, assumed load, source of bounds
Candidates: winner with the axis it won on; each rejected with its axis and reviving condition
Rollout: ship order, mixed-version behaviour, reversal, irreversibility if any
Constitution: counterfactuals answered; amendments routed back
Open questions: each with the decision it blocks, or "blocks nothing"
```

## What this skill does not own

This skill owns the **method**: what must be decided, in what order, and what makes the result reviewable. It names no model and states no numeric threshold. Where a rule here and a rule in an owning skill disagree, the owning skill wins for its half, and this skill drops its weaker statement instead of keeping it as a second opinion. When a question is project policy, a contract value, failure doctrine, a security verdict, observability, data mechanics, messaging, dispatch, plan state, proof, complexity, language idiom or prompting, read `references/80-ownership-boundaries.md`; it names the owner of each.
