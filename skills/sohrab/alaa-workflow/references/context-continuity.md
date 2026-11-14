# Context Continuity

This file owns the question "will the work survive losing the conversation?" Everything else in this skill is ordering and artifact hygiene; this is the part that decides whether a long task can be picked up again.

## The four ways context is lost

Long work loses context in four ways, and only one of them is dramatic enough that anyone plans for it.

**Compaction.** The session hits its context limit and older turns are summarized away. The agent continues in the same conversation and often does not announce it. What survives is a compressed summary; what disappears is the detail — the exact error text, the path that was tried and abandoned, the reason a decision went the way it did.

**A new session.** The user comes back tomorrow, or a run is resumed after an interruption. The agent starts with nothing but the repository and whatever files exist in it.

**A different agent.** A subagent takes a lane, or the work moves between runtimes, or a fresh agent inherits an unfinished task. It has no memory of the conversation at all and no way to ask.

**A subagent boundary.** Every dispatch is a one-way context wall. The child sees only its dispatch text; the parent sees only the child's return. Anything the parent knew and did not write down never reaches the child.

Treat all four as the same problem. The design target is a task any competent agent can resume from the canonical task and workflow owners and the available source and evidence, without conversation history. The cold-start test below checks this recovery goal.

## Two different things get lost, and they need different homes

**Position** is where the work currently stands: which phase is finished, what the last verification actually returned, what is blocking right now, what the next executable action is. Position changes constantly and is cheap to write.

**Knowledge** is what the work learned along the way: which approach was tried and abandoned and why, which facts are verified versus still assumed, which command shape actually works in this environment, which plausible-looking path is a trap. Knowledge accumulates slowly, is expensive to rediscover, and is the first thing compaction destroys — precisely because it lives in the middle of the conversation rather than at the end.

Most workflow tooling records position and forgets knowledge. That is why a resumed task so often repeats a failed experiment: the agent knows where it is, but not what the last agent already ruled out.

For admitted Markdown families, the artifacts divide the work as follows:

| Artifact | Owns | Answers |
|---|---|---|
| Plan | Destination and route | Where are we going, and in what order |
| Checkpoint | Position | Where are we right now |
| Handoff package | Knowledge | What has this work already learned |

The handoff package is a section inside the plan rather than a separate file, because knowledge is only useful next to the route it belongs to, and because a fourth file is a fourth thing to keep honest.

For a Beads-native plan, root notes own aggregate position and the root description holds the six-field handoff. Issue-only work keeps its compact plan, position, results and knowledge in its issue, without a separate checkpoint or handoff package. See `references/task-tracking.md` for the fields and local fallback.

## Status and position

In Beads, use the native issue status. The root notes name the exact IDs of the current phase, task and subtask (or `none`), the last verified evidence address, blockers, the next action, touched surfaces, and any pending review or commit. For concurrent lanes, the parent keeps the aggregate cursor and links to the leaf notes for each lane's live position. A task or subtask cursor names its actual ancestry. Clear finished cursors before you advance.

In Markdown, the plan header owns the overall status. The checkpoint and the JSON state project it. Every checkpoint names its exact `Plan`, status, last verified evidence address, blockers, next action, touched surfaces and update time. A plan that has a checkpoint links to it instead of copying the position. Outage reconciliation follows `references/task-tracking.md`.

A design checkpoint uses `Current position` to name the current design question, decision or approval step. It has no phase, task or subtask cursor. Its in-plan handoff uses the six fields below for verified ideas, assumptions, rejected algorithms and continuation evidence. Design validation evidence belongs to that design plan; the checkpoint references it.

For execution, the checkpoint position also names the current phase. A direct profile keeps its cursor in its only plan file. The execution plan contains the outcome and scope, the phase design and barriers, phase acceptance, integrated-review evidence, skill associations and the handoff package. Task results follow `references/task-tracking.md` `## Acceptance and evidence by level`.

The JSON and mapped issue-cursor rules below apply only to Markdown execution. The JSON state contains the schema version, task identity, status, plan path, the current phase, task and subtask cursor, next actions, blockers, last validation and update time.

Optional schema-2 JSON is a compact consumer snapshot with no task table and no graph. Derive its position fields from the checkpoint when one exists, and otherwise from the direct-plan cursor. Never edit those fields independently. Copy `current_phase` exactly. Project each blocker scalar and each next-action scalar into one whole, trimmed array entry. Project an empty array when the scalar is empty or a none sentinel. Trim outer whitespace and outer code wrapping, and never split the scalar at punctuation. Before execution or completion, reconcile torn updates from the canonical owners. For marked families, companion references must resolve to this exact plan; sharing its basename is not enough.

Task state belongs to the authority selected through `references/task-tracking.md`; neither a checkpoint nor JSON becomes an offline issue register.

For a `phase-task-subtask` family the cursor also records `Current task` and `Current subtask` as exact mapped issue IDs, or `none` before selection and after completion. Executing a task leaf selects its task ID and leaves `Current subtask: none`. A selected subtask requires its actual task and phase; a selected task requires its actual phase. Clear finished cursors before moving phases. Schema-3 JSON adds `current_task` and `current_subtask` and derives them exactly from the checkpoint (or direct cursor); schema-2 snapshots remain valid for existing families. Keep the inherited review boundary, any pending review or commit, and the next safe leaf recoverable through the plan and cursor, without copying issue state.

## The handoff package

Six fields. Each exists because a real resume fails without it.

**Confirmed facts.** Things verified by inspection or execution, each with how it was verified. "The session table has no index on `user_id` — checked with `\d sessions`." A fact without its verification method decays into an assumption the moment someone doubts it.

**Open assumptions.** Things currently believed but not verified, each with what would verify it. Keeping these explicitly separate from confirmed facts is the single highest-value line in the package, because a resumed agent that cannot tell the two apart will either re-verify everything or trust something it should not.

**Ruled out.** Approaches tried and abandoned, each with the reason and the evidence. This is what stops a fresh agent from spending an hour rediscovering that the obvious approach does not work. Record the reason, not just the outcome: "rejected — the ORM strips the CTE" is reusable, "did not work" is not.

**Read first on resume.** An ordered, minimal list of exact paths a resuming agent must read before touching anything. Not every file the task touches; the two or three whose content is load-bearing for the remaining work.

**Environment notes.** Command shapes that actually work here, and ones that look right but fail. Exact invocations, not descriptions. This is the knowledge that is most annoying to rediscover and least likely to be in any documentation.

**Traps.** Anything that looks correct and is not. A test that passes for the wrong reason, a config that is overridden elsewhere, a name that appears twice with different meanings.

Keep all six fields present in an admitted handoff package. Write a field when you learn something that belongs in it, not on a schedule. An empty field stays empty; do not pad it.

## Task resume and phase resume

For design, use the kind-aware resume protocol below; this section covers execution and issue-only work.

Task resume reads the issue's notes, comments, acceptance and relations. Phase resume reads the native phase and root, or the Markdown plan and checkpoint, through the protocol below. The task supplies its state. The plan supplies phase and engagement context.

Before resuming Beads mutations or transferring a task to another agent or device, apply `references/task-tracking.md` `## Agent identity and ownership` to recover identity and verify ownership.

Task-specific learned knowledge goes to its comments for native or issue-only work, or to the Markdown plan handoff. The native root handoff links to task-specific findings when needed. Issue notes hold position only.

## Cross-PC handoff record

A handoff to another PC records the responsible device, Git and applicable Dolt sync state, and whether the recipient can access the code and evidence. Record it in the task notes or the native root notes, or in the Markdown checkpoint or direct cursor. A sync record grants no sync authority.

## When to write

Write only at these moments, including the additional long-conversation trigger below. Writing continuously is a tax, and writing only at the end risks losing detail.

1. **Material task progress, or a phase completes or fails.** Update the selected task authority and the affected canonical workflow fields, then derive the admitted snapshots. This is the routine case and it is cheap.
2. **A decision, blocker or scope change.** Update the affected workflow owners and snapshots. If a decision closed off an alternative, add that alternative to *ruled out*.
3. **A validation runs.** Record design evidence at the design plan. Record execution evidence at its level owner in `references/task-tracking.md` `## Acceptance and evidence by level`. When a checkpoint is admitted, point its last verified result to that evidence. `references/workspace-and-integration.md` owns tested identity, write isolation, and reuse; without attributable inputs, a result cannot be cited on resume.
4. **Something is learned that would be expensive to rediscover.** Record it immediately at its owner under `## Task resume and phase resume`.
5. **Before handing off, and before any long autonomous stretch.** Bring the selected task and workflow owners and the admitted snapshots current, then verify them with the cold-start test.

One more trigger is easy to miss: **when the conversation is getting long.** Do not wait for a compaction warning. If the work has run for many turns, or has just finished an expensive investigation, write the knowledge down while it is still verbatim. After compaction the same information is available only as a summary of a summary.

## The cold-start test

Before handoff, and periodically during long work, apply one question to the canonical tasks, workflow artifacts and their linked source and evidence:

> Could a competent agent with no conversation history read these owners and take the next action correctly, without re-deriving expensive knowledge or repeating ruled-out work?

If the answer is no, repair its canonical home: stale position in the cursor, unclear task readiness in the selected task store, coarse phase design in the plan, rejected approaches in *ruled out*, and unverified beliefs in *open assumptions* rather than *confirmed facts*.

The next action names its owned scope, its satisfied prerequisites, any unresolved decision or blocker, the exact command or edit target, and the expected result. The plan identifies reusable evidence, invalidation conditions and the progress paths of interrupted lanes. Repair gaps in existing fields; add no resume artifact or fresh agent solely for this test.

This test is worth running mentally before any long unattended stretch, because that is exactly when nobody is watching to catch the gap.

## The resume protocol

Resolve the family and kind through `references/artifact-lifecycle.md`, then its task authority through `references/task-tracking.md`. Verify the binding before reading issue state.

For a native plan, read the root by its `beads:<root-id>` address, its notes and handoff, then the selected phase, task and subtask with their comments, evidence and relations. Verify registration and ancestry. Reconcile pending outage records, ownership, readiness and phase barriers before dependent work. Read the exact resume sources and skill bindings before editing. Issue-only work reads its issue, linked evidence and applicable bindings.

For Markdown, read applicable owners in this order:

1. **The current bound issue**, when Beads is selected, for actual task state, notes, comments and prerequisites; fresh hook guidance is no substitute for this read. For a `local` family, retest Beads availability under `references/task-tracking.md` before the next new task.
2. **The plan**, when admitted, for destination, scope, acceptance and validation; a design also requires its decisions and open questions, while execution reads ordered phases and any tasks owned by an existing local family.
3. **The handoff package** inside the plan, for verified facts, assumptions, rejected approaches and traps before touching code. Issue-only work reads the issue's notes and comments instead.
4. **The checkpoint**, when admitted, for position, last verified result, blockers and next action; direct work reads the plan cursor. After any restart, compaction or agent handoff, when it holds a `Pending Beads reconciliation` list and Beads is available, register each entry in Beads and clear the list before other work.
5. **The files named in "read first on resume."**
6. **JSON state**, only for a consumer that needs it; reconcile it with canonical owners rather than trusting it independently.

Before overlapping writes after interruption or replacement, apply `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery`; compaction leaves a living writer's ownership in place. Then verify position against reality: check `git status`, the diff, the availability of sources and deliverables, and the attributable evidence against the cursor's touched surfaces. Reconcile stale task, phase and status snapshots before acting, and record what was stale. `references/workspace-and-integration.md` owns evidence reuse: unchanged attributable proof survives a new session or PC, while affected proof does not. A remembered result or another PC's inaccessible source is insufficient.

Before the next execution task, resolve and load its phase bindings and task overrides through `references/companion-routing.md`. Recheck mapped availability when the runtime or installed catalog changed; historical mappings do not prove current availability.

On execution resume, add explicit phase and task skill bindings to older active execution plans before continuing. Completed archives remain readable; reactivation requires those bindings before the next task. This does not migrate task-store authority, which `references/task-tracking.md` owns.

## After compaction, specifically

Compaction is the one case where the agent continues in the same conversation and may not realise anything was lost. Two rules.

**Repeat the resume protocol.** Read every applicable task and workflow owner above. Do not continue from what a summary says they contained: it keeps the shape and drops the specifics.

**Trust reconciled canonical owners over recollection.** After compaction, verify snapshots against actual state through the resume protocol. Record a discrepancy in the admitted cursor or issue notes; do not trust a remembered detail over reconciled task and workflow evidence.

Do not surface raw context-budget numbers to the model as a way of managing this; that tends to produce premature stopping rather than better prioritisation. Where a model needs reassurance to keep going on a long run, state it plainly instead — that ample context remains, and that it should not stop, summarise, or suggest a new session on account of context limits.

## Delegation is a context boundary

A dispatch is a one-way wall. The child cannot ask, and the parent cannot see what the child saw.

Write dispatches assuming zero shared context: the outcome, the owned scope, the exclusions, the acceptance criteria, the verification commands, and any handoff-package facts that bear on this lane. Copy the relevant facts into the dispatch rather than pointing at a conversation the child never had.

Require the child to return a compact structured result rather than a narrative, and record its evidence in the parent's artifacts. A finding that exists only inside a subagent's return has already been lost — the parent's context will compact too.

A long-running or restart-sensitive lane records done items, remaining items and last evidence address after each item. Name the owner in the dispatch: leaf notes for native work, or the admitted lane-local progress path for Markdown. After interruption, reconcile the record, files and attributable evidence through `references/workspace-and-integration.md`. Preserve valid completed work and dispatch only the remainder.

Keep the parent responsible for synthesis. Children return findings and artifact paths; the parent decides what those mean and writes the outcome down.

## What not to write

The failure mode opposite to losing context is drowning in it. These do not belong in any workflow artifact:

- **Raw logs and full command output.** Record the command, the outcome, and the one line that mattered.
- Secondary snapshots must not duplicate scope, acceptance, phase definitions, or task state owned by the plan or selected task store; reference the canonical owner instead.
- **A transcript of what happened.** The artifacts describe state, not history. "Phase 2 complete, tests pass" is state; three paragraphs about how Phase 2 went is history.
- **Speculation recorded as fact.** If it is not verified, it belongs in *open assumptions* with what would verify it.
- **Secrets, tokens, credentials, or private data**, in any artifact, ever.

## Caveats

Compaction behavior, context window sizes, and whether a runtime signals compaction to the agent are all runtime- and model-specific and change between versions. The rules here are written to hold regardless, but re-check `/alaa-prompting-guide` and its runtime references before depending on any specific harness behavior.
