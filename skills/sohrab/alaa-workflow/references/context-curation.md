# Reusable-Context Curation

This workflow decides when curation runs, where a candidate is parked while the engagement is open, and what happens to the plan when the final gate changes something. `alaa-extract-agent-lessons` owns admission and the reusable shapes. `alaa-memory-os` owns durable publication.

The gates below cover execution and issue-only implementation. A design keeps its context through `references/context-continuity.md` and runs no completion curation.

## The intermediate scan

At a completed or failed phase, or at a material decision boundary, invoke `/alaa-extract-agent-lessons` only when that boundary produced one of these:

- an explicit user or team judgment;
- an accepted tradeoff;
- a verified surprise;
- a costly detour;
- a validation-driven method change;
- a coordination bottleneck;
- non-obvious reusable knowledge.

A boundary that produced none of them waits for the final gate.

Park each admitted candidate at its knowledge owner under `references/context-continuity.md`, and link to it from other owners. Record a judgment as a confirmed fact: who chose what, and why.

Never publish active plan, checkpoint or validation state to memory, because position goes stale within the hour and a memory store cannot learn that it did.

## The final gate

Run the full-engagement gate before completion, once the implementation, validation, review and documentation evidence is stable. Run it even when you expect an empty result.

1. Reconcile the intermediate candidates against the final evidence.
2. Take the admission and routing decisions from /alaa-extract-agent-lessons, and route authorized durable publication through /alaa-memory-os.
3. Record the outcome (persisted, deferred, rejected, or no admitted candidates) once, at the final phase's evidence owner, or in the issue's comments for issue-only work.

## When the gate reopens the pipeline

A `pipeline reopen required` verdict means that the gate changed something that already-closed evidence describes. Reopen the owning phase, or the issue-only task when no plan is admitted. Perform the authorized repository promotion, rerun every affected validation, review, documentation and documentation-check gate, then rerun the final curation.

Never close a plan or an issue-only task against evidence that the curation gate changed, because that reports a state nobody observed.
