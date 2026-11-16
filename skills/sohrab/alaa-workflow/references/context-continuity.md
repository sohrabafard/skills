# Context Continuity

Design target: any competent agent can resume the task from the canonical task and workflow owners and the available source and evidence, with no conversation history. Compaction, a new session, a different agent and a subagent dispatch each lose that history, and compaction is often unannounced.

## Position and knowledge

**Position** is where the work stands: finished phases, the last verification result, blockers and the next executable action. **Knowledge** is what the work learned. Record both, because a resumed task that has only position repeats experiments that the last agent already ruled out.

| Plan medium | Position | Knowledge |
|---|---|---|
| Markdown family | Checkpoint; the plan cursor under the `direct` profile | Handoff package, a section inside the plan and never a separate file |
| Beads-native plan | Root `notes` | Six-field handoff in the root description |
| Issue-only work | Issue `notes` | Issue comments |

`references/task-tracking.md` owns the issue fields and the local fallback.

## Status and position

In Beads, use the native issue status. The root notes name the exact IDs of the current phase, task and subtask (or `none`), the last verified evidence address, blockers, the next action, touched surfaces, and any pending review or commit. For concurrent lanes, the parent keeps the aggregate cursor and links to each lane's leaf notes. A task or subtask cursor names its actual ancestry. Clear a finished cursor before you advance.

In Markdown, the plan header owns the overall status, and the checkpoint and the JSON state project it. Every checkpoint names its exact `Plan`, status, last verified evidence address, blockers, next action, touched surfaces and update time. An execution checkpoint also names the current phase. A plan that has a checkpoint links to it and never copies the position. A `direct` profile keeps its cursor in its only plan file.

A design checkpoint uses `Current position` to name the current design question, decision or approval step. It has no phase, task or subtask cursor. Design validation evidence belongs to the design plan; the checkpoint references it.

These rules apply only to Markdown execution:

- The JSON state holds the schema version, task identity, status, plan path, the phase, task and subtask cursor, next actions, blockers, last validation and update time. It is a consumer snapshot with no task table and no graph.
- Derive its position fields from the checkpoint, or from the direct-plan cursor when no checkpoint exists. Never edit them independently. Copy `current_phase` exactly. Project each blocker scalar and each next-action scalar as one whole array entry, with outer whitespace and outer code wrapping trimmed; never split a scalar at punctuation. An empty scalar or a none sentinel projects an empty array.
- Before execution or completion, reconcile torn updates from the canonical owners. In a marked family, a companion reference must resolve to this exact plan; a shared basename is not enough.
- A `phase-task-subtask` family also records `Current task` and `Current subtask` as exact mapped issue IDs, or `none` before selection and after completion. A task leaf selects its task ID and leaves `Current subtask: none`. A selected subtask requires its actual task and phase; a selected task requires its actual phase. Schema-3 JSON adds `current_task` and `current_subtask`, derived exactly from the cursor. Schema-2 snapshots stay valid for existing families.
- Keep the inherited review boundary, any pending review or commit, and the next safe leaf recoverable through the plan and the cursor, without a copy of issue state. Neither a checkpoint nor JSON becomes an offline issue register.

## The handoff package

| Field | Holds |
|---|---|
| Confirmed facts | Facts verified by inspection or execution, each with how it was verified. A fact without its method decays into an assumption |
| Open assumptions | Unverified beliefs, each with what would verify it. Never mix them with confirmed facts |
| Ruled out | Approaches tried and abandoned, each with the reason and the evidence. "Rejected: the ORM strips the CTE" is reusable; "did not work" is not |
| Read first on resume | An ordered list of the two or three exact paths that the remaining work depends on |
| Environment notes | Exact invocations that work here, and ones that look right but fail |
| Traps | Anything that looks correct and is not: a test that passes for the wrong reason, a config overridden elsewhere, a name with two meanings |

Keep all six fields present in an admitted handoff package. Write a field when you learn something that belongs in it, not on a schedule. Leave an empty field empty.

## Task resume and phase resume

This section covers execution and issue-only work. Design uses the resume protocol below.

Task resume reads the issue's notes, comments, acceptance and relations. Phase resume reads the native phase and root, or the Markdown plan and checkpoint, through the resume protocol.

Before you resume Beads mutations or transfer a task to another agent or device, apply `references/task-tracking.md` `## Agent identity and ownership`.

Learned knowledge about a task goes to its issue comments for native or issue-only work, and to the plan handoff for Markdown. The native root handoff links to task findings when needed. Issue notes hold position only.

## Cross-PC handoff record

A handoff to another PC records the responsible device, the Git sync state, the Dolt sync state where it applies, and whether the recipient can reach the code and the evidence. Record it in the task notes or the native root notes, or in the Markdown checkpoint or direct cursor. A sync record grants no sync authority.

## When to write

Write at these events, not continuously and not only at the end:

1. **Material task progress, or a phase completes or fails.** Update the task authority and the affected workflow fields, then derive the admitted snapshots.
2. **A decision, blocker or scope change.** Update the affected owners. Add an alternative that the decision closed to *Ruled out*.
3. **A validation runs.** Record design evidence at the design plan, and execution evidence at its level owner in `references/task-tracking.md` `## Acceptance and evidence by level`, with the tested identity from `references/workspace-and-integration.md`. Point an admitted checkpoint's last verified result at that evidence.
4. **You learn something that is expensive to rediscover.** Record it at once at its owner under `## Task resume and phase resume`.
5. **Before a handoff or a long autonomous stretch.** Bring the owners and the admitted snapshots current, then apply the cold-start test.
6. **The conversation is long, or an expensive investigation just ended.** Write the knowledge down while it is still verbatim. Do not wait for a compaction warning.

## The cold-start test

Before a handoff, and before a long unattended stretch, ask one question of the canonical tasks, the workflow artifacts and their linked source and evidence:

> Could a competent agent with no conversation history read these owners and take the next action correctly, without re-deriving expensive knowledge or repeating ruled-out work?

If the answer is no, repair the canonical home: stale position in the cursor, unclear readiness in the task store, coarse phase design in the plan, a rejected approach in *Ruled out*, an unverified belief in *Open assumptions*.

The next action names its owned scope, its satisfied prerequisites, any open decision or blocker, the exact command or edit target, and the expected result. The plan identifies reusable evidence, its invalidation conditions and the progress paths of interrupted lanes. Repair gaps in existing fields. Add no resume artifact and no fresh agent for this test.

## The resume protocol

Resolve the family and kind through `references/artifact-lifecycle.md`, then the task authority through `references/task-tracking.md`. Verify the binding before you read issue state.

For a native plan, read the root by its `beads:<root-id>` address with its notes and handoff, then the selected phase, task and subtask with their comments, evidence, relations and skill bindings. Verify registration and ancestry. Reconcile pending outage records, ownership, readiness and phase barriers before dependent work. Issue-only work reads its issue, the linked evidence and its bindings.

For Markdown, read the owners that apply, in this order:

1. **The bound issue**, when Beads is selected: task state, notes, comments and prerequisites. Hook guidance is no substitute for this read.
2. **The plan**: destination, scope, acceptance and validation. A design adds its decisions and open questions. Execution adds the ordered phases and any local tasks.
3. **The handoff package**, before you touch code.
4. **The checkpoint**, or the plan cursor for direct work: position, last verified result, blockers and next action. When it holds a `Pending Beads reconciliation` list and Beads is available, register each entry in Beads and clear the list before other work.
5. **The files in *Read first on resume*.**
6. **JSON state**, only for a consumer that needs it. Reconcile it with the canonical owners.

Before overlapping writes after an interruption or a replacement, apply `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery`; compaction leaves a living writer's ownership in place. Then verify the position against reality: compare `git status`, the diff, the available sources and deliverables, and the attributable evidence with the cursor's touched surfaces. Reconcile stale snapshots before you act. Unchanged attributable proof survives a new session or PC; a remembered result, or source on another PC that you cannot reach, proves nothing.

Before the next execution task, load its phase bindings and task overrides through `references/companion-routing.md`. Recheck mapped availability when the runtime or the installed catalog changed. An older active execution plan gets explicit phase and task skill bindings before it continues. A completed archive stays readable and needs those bindings only on reactivation.

## After compaction, specifically

After compaction you continue in the same conversation and may not notice the loss.

- Repeat the resume protocol and read each applicable owner again. A summary keeps the shape and drops the specifics, so trust the reconciled owners over your recollection.
- Never show a model raw context-budget numbers, because they cause premature stopping. When a model needs reassurance on a long run, state plainly that ample context remains and that it must not stop, summarise or suggest a new session because of context limits.

## Delegation is a context boundary

A dispatch is a one-way wall: the child sees only its dispatch text and cannot ask, and the parent sees only the child's return.

- Write each dispatch for zero shared context: the outcome, the owned scope, the exclusions, the acceptance criteria, the verification commands and the handoff-package facts that bear on the lane. Copy those facts in; never point at a conversation that the child never had.
- Set the return shape under /alaa-low-noise `references/workflow-integration.md` *Delegated lanes*. Record the return's evidence in the parent's artifacts, because a finding that lives only in a return is lost when the parent compacts.
- A long-running or restart-sensitive lane records done items, remaining items and the last evidence address after each item. Name that record's owner in the dispatch: leaf notes for native work, or the admitted lane-local progress path for Markdown. After an interruption, reconcile the record, the files and the attributable evidence through `references/workspace-and-integration.md`. Keep valid completed work and dispatch only the remainder.

## What not to write

Keep these out of every workflow artifact:

- **Raw logs and full command output.** Record the command, the outcome and the one line that mattered.
- **Content that another owner holds.** A snapshot references the scope, acceptance, phase definitions and task state of the plan or the task store; it never copies them.
- **History.** Record state: "Phase 2 complete, tests pass", not how Phase 2 went.
- **Speculation as fact.** An unverified belief goes in *Open assumptions* with what would verify it.
- **Secrets, tokens, credentials or private data.**

## Caveats

Compaction behavior, context window sizes and compaction signalling differ by runtime, model and version. Before you depend on a specific harness behavior, check `/alaa-prompting-guide` and its runtime references.
