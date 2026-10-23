<!-- BEGIN ALAA BEADS BINDING -->

## Beads

Project label: `repo:__PROJECT__`

Expected workspace: `/home/sohrab/project/alaa-task-hub/.beads`

User, repository, and orchestrator constraints govern. This binding overrides conflicting upstream Beads skill or hook guidance and grants no additional authority.

Under Codex, read each `/name` skill reference in this block as `$name`.

### Start and resume

Before planning or executing tracked work, and after compaction or session restart:

1. Read `.agents/skills/beads/SKILL.md` unless its full instructions remain in context; hook output is not a substitute. If missing, report it and stop Beads-dependent work.
2. Before issuing other Beads commands, run `bd where` with the configured `BEADS_DIR` and verify the expected workspace. Recheck after workspace or connection changes. On failure or mismatch, stop Beads operations and report it; do not initialize another database or silently change the connection.
3. Reuse current hook-injected `bd prime` context; run it manually only if missing or stale.
4. Before Beads mutations, claims, ownership comparisons, resume or transfer, load `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`. It owns actor allocation, explicit mutation identity, guarded updates, transfer and closure coordination; its actor rules override actorless upstream examples. If unavailable, stop dependent work. Keep the assigned actor in the existing dispatch or admitted handoff.
5. When resuming, read the active issue and linked plan/checkpoint/handoff. Check worktree state, scope, ownership, and blockers before continuing. A conversation summary or `bd prime` cannot replace task-state recovery. Resolve an ambiguous active task before implementation.

Run each `bd` command separately; do not chain commands or add per-command environment overrides.

### Scope and issue lifecycle

- Filter work selection (`ready`, `list`, `blocked`) by the project label using `--label`. Unfiltered hook output does not expand scope. Add this label to new project issues.
- Before changing an existing issue, use `bd show` to verify its label and relevance to the authorized task. Never relabel it merely to bring it into scope. Other-project dependency reads are allowed; creating or changing other-project work requires explicit user authorization for that scope.
- Search before creating. Reuse a matching issue or create one for new actionable work and discovered follow-ups. Recording a follow-up does not authorize its implementation.
- Claim before implementation through `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`, and verify its readback. A failed or conflicting claim does not establish ownership.
- Update status and blockers/dependencies when reality changes. Creating, claiming, and recording progress may precede completion. Keep incomplete or blocked work unclosed. Close only after acceptance criteria and required checks pass; handoff or compaction alone never justifies closure. Close reason: `/alaa-workflow` `references/task-tracking.md` `## Close reason` (verdict, reviewed version, evidence address).
- Verify mutations succeeded. On failure, report the command, error, and pending update; never report unsaved state as saved.

### Issue conventions

Semantics: `/alaa-workflow` `references/task-tracking.md` `## Beads capabilities in use`.

- `--spec-id "<repo-name>:<repo-relative plan path>"` when a plan exists; `<repo-name>` is the project label suffix after `repo:`.
- Type `decision` for a decision other tasks cite; `spike` for a time-boxed investigation.
- Create each follow-up with `--deps "discovered-from:<origin-id>"` (provenance only, not a blocker).
- Ownership-sensitive mutations follow `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`; guard mechanics and exit 13 follow its `## Beads capabilities in use`.
- Run `bd lint <id>` before close or handoff (a finding blocks close or handoff, per `## Beads capabilities in use`), `bd stale` at handoff or resume review, `bd ready --explain` when readiness is unexpected.

### Continuity and handoff

- At meaningful progress, blocker, decision, or validation changes, update issue state and persist what is needed to resume. Refresh it before handoff or planned compaction; do not wait for a compaction warning.
- Issue `notes` hold position, blockers, and next step only. Learned knowledge goes to the `alaa-workflow` plan's handoff package, else issue comments (`/alaa-workflow` `references/context-continuity.md` `## Task resume and phase resume`). Record a device handoff per its `## Cross-PC handoff record`.
- At session end, report issue IDs/status, changed files, validation results and unrun checks, blockers, next action, and pending commit/push/sync. Report synchronization complete only when verified.

### Ownership and authority

- Beads owns newly tracked issue state and dependencies; do not add parallel durable TODO lists. Existing plans/checkpoints retain authority until explicitly migrated; do not import or duplicate their checklists during setup.
- `alaa-workflow` and repository rules own planning, validation, completion criteria, and handoff structure. Task evidence follows `/alaa-workflow` `references/task-tracking.md` `## Acceptance and evidence by level`.
- Route durable knowledge through `/alaa-memory-os`. `bd remember` only for a short reminder shared across the whole hub, with source, scope, and maintainer; write it without separate approval. Never put task status, evidence, lessons, or new rules in it; leaving it empty is correct. Owner: `/alaa-memory-os` `## Beads hub reminders and issue notes`. Keep issue descriptions and dependency explanations with their issues.
- Git commits, pushes, and Dolt remote sync require explicit user authorization; a profile, hook, or skill grants none. Report unauthorized pending actions instead of executing them.

### Quick Reference

Replace `<project-label>` and `<id>` with verified values and `<actor>` with this agent's literal assigned actor from `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`. Its ownership checks, transfer and close coordination apply before these examples. Replace other placeholders with actual values. Run each command separately; all binding rules apply.

```bash
bd ready --label "<project-label>"
bd list --status=in_progress --label "<project-label>"
bd ready --explain --label "<project-label>"
bd blocked --label "<project-label>"
bd --actor "<actor>" create "<title>" --description "<goal, scope, output, plan link>" --acceptance "<criterion or exact plan reference>" --labels "<project-label>" --type <type>
# add when a plan exists:  --spec-id "<repo-name>:<repo-relative plan path>"
# add for a follow-up:     --deps "discovered-from:<origin-id>"
bd show <id>
bd --actor "<actor>" update <id> --claim
bd show <id>
bd --actor "<actor>" update <id> --if-assignee "<actor>" --if-status in_progress --append-notes "<position, blockers, next step>"
bd show <id>
bd lint <id>
bd stale --label "<project-label>"
bd show <id>
bd --actor "<actor>" close <id> --reason "<verdict>; <commit | HEAD+scoped sha256>; <evidence address>"
bd show <id>
bd prime
```

<!-- END ALAA BEADS BINDING -->
