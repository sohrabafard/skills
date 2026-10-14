# Reusable-Context Curation

Three skills meet here and the boundary is settled. `alaa-extract-agent-lessons` owns admission and the reusable shapes — what qualifies as a decision interface, a judgment rubric, or a knowledge card. `alaa-memory-os` owns durable publication. This workflow owns when curation runs, where a candidate is parked while the engagement is still open, and what happens to the plan when the final gate changes something.

## The intermediate scan

At a completed or failed phase, or a material decision boundary, invoke `/alaa-extract-agent-lessons` only when that boundary produced one of these:

- an explicit user or team judgment;
- an accepted tradeoff;
- a verified surprise;
- a costly detour;
- a validation-driven method change;
- a coordination bottleneck;
- non-obvious reusable knowledge.

A boundary that produced none of them waits for the final gate. Scanning every boundary spends context on nothing and trains the run to skip the scan that mattered.

When a plan is admitted, park each admitted candidate in its matching handoff-package field; for issue-only work, use canonical issue notes. `references/context-continuity.md` owns these locations and field semantics. Record judgments as confirmed facts about who chose what and why, never as universal facts: a preference recorded as law will be applied unchanged in another repository, where it may be wrong and its origin lost. Do not duplicate candidates between owners; link the canonical record.

Do not publish active plan, checkpoint, or validation state to memory. That is position, it is stale within the hour, and a memory store has no way to learn that it went stale.

## The final gate

Run the full-engagement gate before completion, once implementation, validation, review, and documentation evidence are stable — and run it even when the expected result is empty, because a gate that runs only when something is expected has stopped being a gate.

1. Reconcile the intermediate candidates against the final evidence.
2. Consume /alaa-extract-agent-lessons admission/routing and route authorized durable publication through
   /alaa-memory-os; memory owns storage authority and search-before-create, not this timing reference.
3. Record the outcome — persisted, deferred, rejected, or no admitted candidates — once in the admitted plan's final-phase evidence, with a reference from its checkpoint when admitted, or in canonical issue notes for issue-only work. Do not create artifacts outside admission or copy the outcome into another editable owner.

## When the gate reopens the pipeline

A `pipeline reopen required` verdict means the gate changed something described by already-closed evidence. Reopen the owning phase, or the issue-only task when no plan is admitted; perform the authorized repository promotion, rerun every affected validation, review, documentation, and documentation-check gate, then rerun final curation.

Never close a plan or issue-only task against evidence changed by the curation gate. Closing against superseded evidence reports a state never observed, which readers trust.
