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
| `## Status and position` | new | Append a block at each write event that moves the position; a dispatched write lane appends one before it returns or stops | W1.3 |
| `## The handoff package` | Six fields | Same six fields, now stated as the definition of knowledge for every medium, each with its comment tag; "keep all six present" is scoped to the Markdown package | W1.4 |
| `## Task resume and phase resume` | new | Resume commands I3 with their trigger (session start, after a compaction, when you cannot name your position); the actor rule; the `Lane:` fallback; where position and knowledge are; the pointer to the takeover | I3, W1.4 |
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
| Pass the required global flags; batch-script rule; no per-command environment override | Write form kept in the block; the rest moved to the capability table |
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
