# Lane LA ledger — Workstream 1, advisor pointers, root Beads block

One row per changed, added or removed rule. "W1.n" is Workstream 1 item n of `plan.md`. "I1", "I2" and
"I3" are the fixed interface texts. "sources" is `sources.md` Q4 and its lead decisions. No checker
clause was reworded or deleted: no bound sentence changed. Paths are relative to
`skills/sohrab/alaa-workflow/` unless they start at the repository root.

## `references/task-tracking.md`

| Section | Old rule | New rule | Plan item |
|---|---|---|---|
| `## Select before tracking-dependent work` | new | An authorized task that writes or refreshes a binding block starts from `assets/beads-binding-template.md` | W1.6 |
| `## Select before tracking-dependent work` | Hook guidance and `bd prime` never state the task state | Same, plus: their unfiltered output never widens the project scope (moved from the old block) | W1.6 |
| `## Agent identity and ownership` | Actor built from host IDs or an opaque ID | Same, plus: the run ID is the session identifier the host exposes, so one session derives one actor after a compaction | I3 |
| `## Agent identity and ownership` | A child dispatch carries the actor, binding reference, issue IDs and ownership action; a read-only lane has `none` | A child dispatch carries the actor, binding reference, the leaf's issue ID and the action; a write lane has `claim` and claims its leaf with its own actor; a read-only lane keeps `none`; the lead keeps one `Lane: <leaf id> <actor>` line per live leaf in the root `notes` | W1.3 |
| `## Agent identity and ownership` | Claim authorized unassigned work, then read back | Same, read back once; plus: never claim an in-progress issue that another actor holds, whatever its lease | W1.2 |
| `## Agent identity and ownership` | Never force a claim or take over an issue automatically | Never force a claim; never take another actor's issue except through the transfer or the takeover | W1.4, sources |
| `## Agent identity and ownership` | Read the lease expiry from `bd show`; never hard-code a TTL; run `bd heartbeat` while the claim outlives the TTL; after a failed heartbeat stop, ping, re-read | removed. Send no heartbeat and read no lease TTL, with the reason and its date (v1.3.2 source read on 2026-11-17) and a recheck-after-upgrade duty | W1.2, sources |
| `## Agent identity and ownership` | A lease is local to one node: across PCs the status and assignee carry ownership | The status and assignee carry ownership, on one node and across PCs | W1.2 |
| `## Agent identity and ownership` | After a failed heartbeat: when another actor holds the issue, stop, report and wait for the user | Kept as a stop condition on the guard path: when the re-read after a guard mismatch or an uncertain write shows another holder, stop writing, report and wait for the user | W1.2 |
| `## Agent identity and ownership` | Transfer by the authorized transferring agent | Same, plus: for a stopped lane the lead is the transferring agent and updates the `Lane:` line | W1.3 |
| `## Agent identity and ownership` | new | Takeover of your own earlier claim: three conditions (the work is given to this session; `bd show` names the earlier actor with `in_progress`; stopped-writer recovery proved the writer stopped), then one guarded transfer, one read-back, continue from the last checkpoint block. A failed condition means leave and report. After a compaction: same actor, no transfer | W1.4 as changed by sources (replaces the `bd reclaim` step) |
| `## Agent identity and ownership` | Before close: read the issue, verify assignee and status; after acceptance and `bd lint`, close, then read back the closure and the assignee | After acceptance: `bd lint`, then close; the command result confirms it. Read the issue first only after a resume, an outage or a transfer. The read-back after close is removed | W1.2 |
| `## Agent identity and ownership` | new | The lead closes a write lane's leaf with the lead's actor after the lane returned, the assignee matches the `Lane:` line and the diff is reconciled; the lead then removes the `Lane:` line; a lane never closes its leaf | W1.3 |
| `## Agent identity and ownership` | Dated verification line (2026-11-02, 2026-10-18) | Kept verbatim, plus the 2026-11-17 source line for the guarded transfer | W1.2 |
| `## Beads-native execution plan` | Register the ordered phase milestones under the root; each phase has at least one task | Size the plan: one bounded task is one issue; several tasks are a root with leaves directly under it; a phase milestone only where a recorded barrier separates two task groups; each phase still has at least one task | W1.1 |
| `## Beads-native execution plan` | new | In a plan with no phase, the root takes the place of the phase in every rule of this skill that names a native phase | W1.1 |
| `## Beads-native execution plan` | Task description states the owned scope and its exclusions | Each leaf states its owned paths; two leaves that can be ready together never own one file; add a blocking edge when they must change one file | W1.1 |
| `## Beads-native execution plan` | Root `description` holds the exact `Final phase` issue ID and the six-field handoff | `Final phase` is the ID of the last phase, or of the root when the plan has no phase; the handoff leaves the description | W1.1, W1.4 |
| `## Beads-native execution plan` | Root `notes`: the aggregate cursor, last evidence address, blockers, next action | Root `notes`: the engagement checkpoint block with the `Lane:` lines; root comments: engagement-wide tagged knowledge | I1, I2 |
| `## Beads-native execution plan` | Task: results go in comments and the close reason | Task: `notes` hold the leaf checkpoint block; comments hold task-local tagged knowledge and results; the phase ID is stated where a phase exists | I1, I2, W1.1 |
| `## Beads-native execution plan` | new | A dispatched write lane claims its leaf and appends a checkpoint block before it returns or stops; the lead keeps the root block, reconciles the diff and closes; a rejected leaf stays unclosed and gets a follow-up with a `discovered-from` edge | W1.3 |
| `## Beads-native execution plan` | Nested invocation: own node and cursor; the parent holds the aggregate position | Own node and checkpoint block; the parent holds the engagement position | I1 |
| `## Beads-native execution plan` | Check graph integrity through the capability table, and the hierarchy with `bd children <root-id>`; then the ready query | Two checks: `bd dep cycles` reports no cycle, and the same ready query. `bd children` and `bd graph check` are no longer required | W1.2 |
| `## Beads-native execution plan` | Mark `registered` when the graph checks pass and the records are complete | Same with "both checks", plus the reason: other agents claim from `bd ready` | W1.2 |
| `## Issue fields` | `notes`: position, blockers, next step | Same content, as the checkpoint block | I1 |
| `## Issue fields` | Comments: events, and learned knowledge and curation outcomes when no plan exists | Comments: tagged knowledge for every Beads work, events, and curation outcomes when no plan exists | I2 |
| `## Beads capabilities in use` | Three-column table with nine `Not adopted` rows | Two-column table of adopted commands plus one last row that rejects every other command and flag. The last row keeps the named classes: force flags, close without acceptance, undesignated claim or close, `bd heartbeat`, commands owned elsewhere, and the full remote, setup, destructive and external list with its explicit-authorization rule | W1.5 |
| `## Beads capabilities in use` | `bd heartbeat` adopted | Not adopted: no rule reads the lease that it renews | W1.2, sources |
| `## Beads capabilities in use` | `bd dep cycles`, `bd graph check`, `bd swarm validate`: run them after an edge change | Run `bd dep cycles`; the other two are optional | W1.2 |
| `## Beads capabilities in use` | Read-only row | Same, plus `bd orphans` (moved from the removed row), and: `bd show <id>` and `bd list --assignee` are the resume read | I3 |
| `## Beads capabilities in use` | Ownership row without `--assignee` | `--assignee` named, because the transfer and the takeover use it | sources |
| `## Beads capabilities in use` | `bd close --suggest-next` row | `bd close` named with it, pointing to the ownership and close-reason sections | W1.5 |
| `## Beads capabilities in use` | Events in `bd comments add`, position in `--append-notes` | Knowledge and events in `bd comments add`; the checkpoint block in `--append-notes`; `--notes` replaces the field | I1, I2 |
| `## Beads capabilities in use` | new in this file (was in the root block) | Batch `bd` writes in one script only with `--actor` on every command, `set -euo pipefail`, each result printed, stop at the first failure, read back afterwards; no per-command environment override | W1.6 |
| `## Beads capabilities in use` | Per-row reasons for `--graph`, `--file`, `bd batch`, `bd q`, `bd swarm create`, the `timer`, `gh:*` and `bead` gate types, wisps, `bond`, `squash`, `burn`, `bd preflight`, `bd merge-slot`, `bd set-state`, `bd audit`, `bd provenance`, `bd events`, `bd todo`, `bd edit`, `bd create-form` | removed; the last row rejects them without a reason of their own | W1.5 |
| `## Beads capabilities in use` | Dated lines 2026-11-02, 2026-11-14, 2026-10-13 and both 2026-11-02 observations | Kept; one 2026-11-17 line added | W1.5 |
| `## Ready tasks and workflow gates` | new in this file (was in the root block) | Report a sync as complete only after you observed its result | W1.6 |

## `references/context-continuity.md`

| Section | Old rule | New rule | Plan item |
|---|---|---|---|
| `## Position and knowledge` | Native plan: position in root `notes`, knowledge as the six-field handoff in the root description. Issue-only: notes and comments | Position is the checkpoint block in the root and leaf `notes`; knowledge is tagged comments on the root and the leaf. Issue-only work uses the same two | W1.4 |
| `## Status and position` | Root notes name the phase, task and subtask IDs, evidence address, blockers, next action, touched surfaces, pending review or commit | The five-line checkpoint block I1, appended by the claim holder; the last block is current; `--notes` may drop old blocks; a pending review or commit goes in the root `Next` line | I1 |
| `## Status and position` | The parent keeps the aggregate cursor and links to each lane's leaf notes | The root block carries one `Lane: <leaf id> <actor>` line per live leaf | I1 |
| `## Status and position` | A task or subtask cursor names its actual ancestry; clear a finished cursor before you advance | removed for Beads: the native parent relation gives the ancestry, and an appended block supersedes the earlier one | I1 |
| `## Status and position` | new | The `Lane:` lines are part of the root block; only the lines of the last block are live. The lead drops a closed leaf, or changes an actor, by appending a new root block | I1, W1.3 |
| `## Status and position` | new | Append a block at each write event that moves the position; a dispatched write lane appends one before it returns or stops | W1.3 |
| `## The handoff package` | Six fields | Same six fields, now stated as the definition of knowledge for every medium, each with its comment tag; "keep all six present" is scoped to the Markdown package | W1.4 |
| `## Task resume and phase resume` | new | Resume commands I3 with their trigger (session start, after a compaction, when you cannot name your position); the actor rule; the `Lane:` fallback; where position and knowledge are; the pointer to the takeover | I3, W1.4 |
| `## Task resume and phase resume` | new, beyond I3 as fixed | A new session has a new actor, so its list is empty: on an empty list, as for an unknown actor, list again without `--assignee` and take the issue that the user, the dispatch or the handoff names | I3, W1.4 |
| `## Task resume and phase resume` | new in this file (was in the root block: resolve an ambiguous active task before implementation) | When more than one issue can be yours and neither the user nor a `Lane:` line decides it, ask before any write | W1.6 |
| `## Task resume and phase resume` | Learned knowledge goes to issue comments; the native root handoff links to task findings | Knowledge comments I2: seven tags, root or leaf placement, nothing rewritten. The root handoff link is removed | I2 |
| `## Cross-PC handoff record` | Record it in the task notes or the native root notes | Same, plus: append a current checkpoint block after it, so that the last block stays the position | I1 |
| `## The cold-start test` | Repair stale position in the cursor | In the checkpoint block or the cursor | I1 |
| `## The resume protocol` | Native plan: read the root with its notes and handoff, then the phase, task and subtask | Run the resume commands; read the root with its checkpoint block and tagged comments, then the phase where one exists, the task and the subtask | W1.4, W1.1 |
| `## After compaction, specifically` | new | Under Beads, list your work with the same actor; your claims are still yours, so run no transfer | W1.4 |
| `## Delegation is a context boundary` | Progress record owner for native work: leaf notes | The checkpoint block in the leaf notes | I1 |

## Other workflow files

| File | Old rule | New rule | Plan item |
|---|---|---|---|
| `SKILL.md` Start step 5 | Load `/alaa-low-noise` and the narrowest domain skill | Load `/alaa-low-noise` in the session that leads the work; the companion table states when a dispatch names it | W1.7 |
| `references/companion-routing.md` *Core companions* | `/alaa-low-noise` owns context and print volume | Same, loaded by the leading session; a lane takes its output rule from its agent definition; name the skill in a dispatch only for a discovery-heavy or log-heavy lane | W1.7 |
| `references/phase-prompts.md` *Roles* | new | For a Claude target, apply the advisor section of the prompting guide before the prompt ships (pointer only) | Workstream 3, consumer side |
| `assets/phase-prompts-template.md` header | new | The same pointer; no token and no bound sentence changed | Workstream 3, consumer side |
| `assets/beads-binding-template.md` | new file | The binding block with `__PROJECT__`, the use notes, and the allow-list entries as information for the owner | W1.6 |

## Root `AGENTS.md` Beads block

1,220 words before, 449 after, both marker lines counted. Every rule of the old block has a row.

| Old block rule | Disposition |
|---|---|
| Label, expected workspace, precedence, grants no authority, Codex `$name` reading | Kept |
| Beads is the task authority when available; otherwise no `bd` command except the test, no replacement database, select the store by the owner section | Kept |
| A task lives in exactly one store | In owner: `task-tracking.md` `## Select before tracking-dependent work` |
| Read `.agents/skills/beads/SKILL.md` at start; report when it is missing | Removed from the block (W1.6). The same owner section states when the upstream skill is used |
| `bd where`, expected workspace, `bd ping`; never initialize another database or change the connection | Kept, with the trigger "before other `bd` commands". "Recheck after a workspace or connection change" is removed from the block (W1.6) |
| Reuse hook-injected `bd prime` context | In owner: capability table |
| Load the ownership section before mutations; stop the mutation when it cannot be loaded; keep the actor in the dispatch | Kept as a pointer and as the stop "if it cannot load, run no `bd` write"; the actor rule is in the owner section |
| Resume: read the active issue and its plan; check worktree, scope, ownership, blockers | Replaced by the resume commands I3 with their trigger; the checks are in `context-continuity.md` `## The resume protocol` |
| A summary or `bd prime` cannot replace task-state recovery | Kept |
| Resolve an ambiguous active task before implementation | Moved to `context-continuity.md` `## Task resume and phase resume` |
| Pass the required global flags; batch-script rule; no per-command environment override | Write form kept in the block, now with `--actor` after the subcommand, as the owner section writes it (the old Quick Reference put `--actor` before it); the rest moved to the capability table |
| Label filter on `ready`, `list`, `blocked`; label new issues | Kept |
| Unfiltered hook output does not expand scope | Moved to `task-tracking.md` `## Select before tracking-dependent work` |
| Verify the label before a change; never relabel into scope; other-project writes need authorization | Kept. "Other-project dependency reads are allowed" is removed: no rule forbids a read |
| Search before create; a follow-up authorizes no implementation; `discovered-from` | Kept |
| Claim before implementation; a failed or conflicting claim establishes no ownership | Kept |
| Update status, blockers and dependencies when reality changes | Kept as the checkpoint rule; edges are in `task-tracking.md` `## Record task prerequisites` |
| Close only after acceptance and checks; never for a handoff or a compaction; close reason | Kept |
| Verify mutations; never report unsaved state as saved | Kept, with the pointer to `## Outage and uncertain writes` |
| `spec-id` form; `beads:<root-id>` for a native plan; types `decision` and `spike` | In owner: `## Issue fields`, capability table |
| `bd lint` before close or handoff; `bd stale`; `bd ready --explain` | `bd lint` kept; all three in the capability table |
| Persist at progress, blocker, decision or validation changes; refresh before handoff or compaction | Kept as the checkpoint rule; events in `context-continuity.md` `## When to write` |
| Notes hold position only; knowledge and device handoff by the two continuity sections | Kept |
| Session-end report list | Removed from the block (W1.6): the checkpoint block holds the same items, and the runtime output contract owns the final report |
| Report synchronization complete only when verified | Moved to `task-tracking.md` `## Ready tasks and workflow gates` |
| Beads owns tracked state; no parallel TODO list; no import of existing checklists | In owner: `task-tracking.md` `## One task authority`, `## Migrating a local family` |
| `alaa-workflow` owns planning and evidence structure | Kept as the evidence pointer |
| Durable knowledge and `bd remember` through `/alaa-memory-os` | Kept as a pointer; the reminder rules are in that skill |
| Local commits pre-authorized, one Conventional Commit per topic or lane | Kept. "Worktree lanes branch from the latest commit" is in `workspace-and-integration.md` `## Record the tested state` |
| Push, tag, merge into another branch, history rewrite, Git or Dolt remote sync need explicit authorization; report a pending action | Kept |
| `bd` commands on the expected workspace are this repository's own task tracking; the rule grants no authority | Kept |
| Quick Reference command list | Removed (W1.6): the resume commands and the write form stay; each command is in its owner section |

## Repair after the main review

One row per rule changed by the repair of `review-main.md`. "F n" is finding n; "D n" is a lead decision of the repair dispatch. No checker clause was reworded or deleted: no bound sentence changed.

| File and section | Old rule | New rule | Finding or decision |
|---|---|---|---|
| `references/task-tracking.md` `## Agent identity and ownership` | Use the host's session identifier as the run ID, so that the same session derives the same actor after a compaction | When the host exposes a session identifier, use it as the run ID; no claim that it survives a compaction | F 3, F 7, D12 |
| same | The lead keeps one `Lane:` line per live leaf in the current root block | The lead appends a root block with one `Lane:` line per live leaf before it dispatches a write lane and again after each lane returns or merges | F 4, D8 |
| same | An agent keeps its actor through compaction and resume; a replacement gets a new actor | Paragraph "Actor after a compaction": derive the actor from the session identifier when exposed, else read `Lead:` or `Lane:` from the last root block; never build a new actor for a session that holds claims; only a new session or a replacement gets a new actor and never writes with an actor read from Beads | F 3, F 7, F 40, D12 |
| same | Never take another actor's issue except through the transfer or the takeover | The lead's release of a rejected leaf is the third exception | D13 |
| same | `## Beads capabilities in use` rejects the force flags and limits `bd reclaim` | It rejects the force flags and `bd reclaim` | F 1, F 31, D5 |
| same, Transfer | new | A stopped lane that never claimed its leaf gets no transfer: the replacement is dispatched with `claim` | F 4 |
| same, Takeover | The guards refuse the transfer when the holder changed, and the transfer needs no force flag and no lease. After a compaction the session keeps its actor and runs no transfer | "The transfer needs no force flag." The guard fact stays in the capability row and the dated source line; the compaction rule is in the actor paragraph and in `context-continuity.md` `## After compaction, specifically` | F 40, F 41, D5 |
| same, Takeover | new | After a root takeover, append a root block whose `Lead:` line names the new actor | D12 |
| same, Reject | In `## Beads-native execution plan`: a rejected leaf stays unclosed and the repair is a follow-up with a `discovered-from` edge | The leaf stays unclosed; the lead records the rejection as a comment, then continues the same lane, or releases the leaf with a guarded `bd unclaim` when the lane has stopped; a follow-up is for new work only. Source and the untested non-holder release are stated | F 5, D13 |
| `references/task-tracking.md` `## Beads-native execution plan` | Paragraph "A dispatched write lane owns its leaf ..." restated the claim, the lane checkpoint, the `Lane:` lines and the lead close | Removed: each rule stays in its owner (`## Agent identity and ownership`; `context-continuity.md` `## Status and position`) | F 38 |
| same, root `notes` row | The block with one `Lane: <leaf id> <actor>` line per live leaf | The block with its `Lead:` and `Lane:` lines; the line format has one owner | D12, F 38 |
| same | new | An agent claims the root or a leaf, never a phase milestone | D9 |
| same | new | When the user changes an authority that a root field records, the lead changes the field through a guarded update, not only the notes | D9 |
| `references/task-tracking.md` `## Beads capabilities in use` | The last row rejects every command and flag that no other row names | The intro sentence is removed; a command is used as its row states, with the flags that this skill and the binding block write for it; the last row rejects every other command and each flag it names | F 2, F 13, F 41 |
| same, read-only row | `bd show <id>` prints five fields and `bd list --assignee` lists one actor's issues: the resume read. `bd show --long` shows the lease | Both commands are the resume read, by pointer to `context-continuity.md` `## Task resume and phase resume`; the lease sentence is removed | F 1, F 41, D5 |
| same | Row `bd reclaim`: allowed inside stopped-writer recovery on an expired lease | Removed. `bd reclaim` is in the reject class "Takes or clears another actor's claim"; the guarded transfer replaces it | F 1, F 31, D5 |
| `references/task-tracking.md` `## Outage and uncertain writes` | For a native plan or issue-only work, keep the pending list in the session or an authorized evidence-only artifact | Use an authorized evidence-only artifact; when none exists, ask the user for one and report the full list in each progress update | F 10 |
| `references/context-continuity.md` `## Status and position` | Root block: the block plus one `Lane:` line per live leaf | The root block starts with `Lead: <actor>`; pointer to the owner of the append times | D12, D8 |
| `references/context-continuity.md` `## Task resume and phase resume` | The run part of the actor is the session identifier, so the same session derives the same actor after a compaction | Removed; after a compaction the agent recovers its actor under `task-tracking.md` `## Agent identity and ownership` before any write | F 7, F 40, D12 |
| same | Continue from the `Next` line | Before any write, compare `Touched` with `git status` and the diff and apply stopped-writer recovery under `## The resume protocol`; then continue from the `Next` line | F 6, F 15 |
| same, knowledge comments | The paragraph listed the seven tags with their qualifiers | Each item starts with its field's tag from `## The handoff package` or with `decision:`; the reason clause of "Rewrite nothing" is kept | F 39 |
| Root `AGENTS.md` block and `assets/beads-binding-template.md` | Availability test runs first | It runs first and again after a workspace or connection change | F 16, D6 |
| same, Resume | new | Before you continue, check worktree state against the block's `Touched` line, scope, ownership and blockers | F 6, F 15, D6 |
| same, Work | Other-project writes need the user's authorization | They need the user's explicit authorization for that scope | F 11, F 35, D6 |
| same, Work | Write as `bd --sandbox <subcommand> --actor "<actor>"`. Guards and takeover: `## Agent identity and ownership` | Before any `bd` write, claim, resume or transfer, load `## Agent identity and ownership`; the block's existing sentence stops the write when a section cannot load | F 12, D6 |
| same, Work | Append a checkpoint block when the position changes and before you stop | Also add each learned item as a tagged comment when you learn it, by pointer to `context-continuity.md` `## Task resume and phase resume` | F 8, F 14, D6 |
| same | Write as `bd --sandbox <subcommand> --actor "<actor>"` | The same rule ("Every write takes `--sandbox` before the subcommand and `--actor` after it") heads five write forms: create, claim, checkpoint, comment, close | D6 |
| `assets/beads-binding-template.md` allow-list note | `bd unclaim` and `bd reclaim` are rare, so a prompt is a useful check | Only `bd unclaim` is named | F 1, D5 |

## Second repair round

One row per rule changed after the verification of the first repair. A row here supersedes the row of the table above that names the same rule. No checker clause was reworded or deleted: no bound sentence changed.

| File and section | Old rule | New rule | Finding or decision |
|---|---|---|---|
| `references/task-tracking.md` `## Agent identity and ownership`, actor paragraph | Derive the actor from the session identifier when the host exposes one; otherwise read it from the last root block | One condition: when the IDs that the host still exposes cannot rebuild the whole actor, read it from the last root block (`Lead:` or `Lane:`). The last two sentences are merged, so that "never writes with an actor that it read from Beads" names only the new session or the replacement | F 3, D12 |
| same, Reject | When the lane has stopped, the lead releases the leaf with a guarded `bd unclaim` | When the lane has stopped, the lead moves the leaf to the replacement lane under Transfer. Only when no replacement follows, the lead releases it with the guarded `bd unclaim` and reads it back. A refused release blocks dependent work and is never forced | D13 narrowed by D5 |
| `references/task-tracking.md` `## Beads capabilities in use`, guard row | A guard mismatch exits 13 and writes nothing | A guard mismatch writes nothing and exits 13 on `bd update`, 1 on `bd unclaim` (installed `bd unclaim --help`, bd 1.3.2, read 2026-11-17) | D13 |
| same, last row | Class "Takes or clears another actor's claim" | Class "Takes or clears another actor's claim without its guard"; the command list is unchanged | D5, D13 |
| `references/context-continuity.md` `## Task resume and phase resume`, knowledge comments | "Rewrite nothing: correct an earlier comment with a new one, so that writers never overwrite each other" | The reason clause is removed | F 39 |
| `references/context-continuity.md` `## After compaction, specifically` | Under Beads, list your work with the same actor as before | Recover your actor under `task-tracking.md` `## Agent identity and ownership` and list your work with it | D12 |
| `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery` | After a compaction, recover the same actor (no route to the rule) | The same sentence, plus a pointer to `task-tracking.md` `## Agent identity and ownership` for the actor recovery. The bound clause `recover the same actor and reconcile its active process before continuing` is unchanged | F 7, D12 |
| Root `AGENTS.md` block and `assets/beads-binding-template.md`, create form | `--description "<goal, scope, output>"` | `--description "<goal, scope, output, plan link>"` | D6 |

## Lead edits after the second verification

| File | Old rule | New rule | Reason | Checker clause |
|---|---|---|---|---|
| references/task-tracking.md | The first root checkpoint block came before the first write-lane dispatch | The lead appends it right after it claims the root; the block holds the `Lead:` line and the `Lane:` lines | Verifier: a lead that compacts before any dispatch had no block to read its actor from | none |
| references/task-tracking.md | new | Work with no root reads its actor as the assignee of the in-progress issue that the user or the handoff gave the session | Verifier: single-issue work has no root block | none |
| references/task-tracking.md | The heartbeat reason said that only `bd reclaim` reads the lease | Clause removed | sources.md Q4 names a second caller, and decision D5 removes lease pointers | none |
| references/task-tracking.md | Release of a rejected leaf had no proof step | The lead applies stopped-writer recovery first; the source line states that the help text expects `--force` for a non-holder | Verifier, decision D13 | none |
| references/task-tracking.md | "because a compaction erases the session" | "because a compaction can drop it from the session" | Contradicted context-continuity.md | none |
| references/task-tracking.md | "The transfer needs no force flag." | removed | Finding 41: the guard row and the command already say it | none |
