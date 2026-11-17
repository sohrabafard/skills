<!-- BEGIN ALAA BEADS BINDING -->

## Beads

Project label: `repo:__PROJECT__`

Expected workspace: `__BEADS_WORKSPACE__`

User, repository and orchestrator constraints govern. This binding overrides conflicting upstream Beads skill or hook guidance and grants no authority. Under Codex, read each `/name` as `$name`. A `##` name is a section of `/alaa-workflow` `references/task-tracking.md`, unless a file is named; if it cannot load, run no `bd` write.

**Availability.** First, and again after a workspace or connection change, run `bd where` and verify the expected workspace, then `bd ping`. If both pass, Beads is the task authority. Otherwise report the failure, run no other `bd` command, initialize no database and change no connection, and select the store under `## Select before tracking-dependent work`.

**Resume.** Run these at session start, after a compaction, and whenever you cannot name your position:

```bash
bd list --status=in_progress --label "repo:__PROJECT__" --assignee "<actor>"
bd show <id>   # root, then leaf
```

If the list is empty or your actor is unknown, omit `--assignee`; the user or the root's `Lane:` lines name your issue. Position is the last checkpoint block in `notes`; knowledge is tagged comments. No summary or `bd prime` replaces this read. Before you continue, check worktree state against the block's `Touched` line, scope, ownership and blockers. Owner: `/alaa-workflow` `references/context-continuity.md` `## Task resume and phase resume`; another PC: its `## Cross-PC handoff record`.

**Work.**

- Pass `--label "repo:__PROJECT__"` to `ready`, `list` and `blocked`, and label each new issue. Verify an issue's label before you change it; never relabel one into scope. Other-project writes need the user's explicit authorization for that scope.
- Search before you create. A follow-up takes `--deps "discovered-from:<origin-id>"` and authorizes no implementation.
- Before any `bd` write, claim, resume or transfer, load `## Agent identity and ownership`: it states your distinct `<actor>`, the guards and the takeover.
- Claim before you work, then read the issue back; a failed claim or guard mismatch gives no ownership.
- Append a checkpoint block when the position changes and before you stop. Add each learned item as a tagged comment when you learn it (`/alaa-workflow` `references/context-continuity.md` `## Task resume and phase resume`).
- Close only after acceptance, the required checks and `bd lint <id>` pass, never for a handoff or a compaction. Reason: `## Close reason`.
- Commands: `## Beads capabilities in use`. Fields: `## Issue fields`. Evidence: `## Acceptance and evidence by level`. Failed write: `## Outage and uncertain writes`; never report unsaved state as saved.

Every write takes `--sandbox` before the subcommand and `--actor "<actor>"` after it:

```bash
bd --sandbox create "<title>" --description "<goal, scope, output, plan link>" --acceptance "<criterion>" --labels "repo:__PROJECT__" --actor "<actor>"
bd --sandbox update <id> --claim --actor "<actor>"
bd --sandbox update <id> --if-assignee "<actor>" --append-notes "<checkpoint block>" --actor "<actor>"
bd --sandbox comments add <id> "<tag>: <item>" --actor "<actor>"
bd --sandbox close <id> --reason "<verdict>; <tested version>; <evidence address>" --actor "<actor>"
```

**Authority.**

- Local commits on the current work branch are pre-authorized: one Conventional Commit per finished, validated topic or lane.
- Push, tag, merge into another branch, history rewrite and remote sync (Git or Dolt) need explicit user authorization; a profile, hook or skill grants none. Report a pending unauthorized action.
- `bd` commands that read or write the expected workspace are this repository's own task tracking, not changes outside this repository, even when a task or goal forbids such changes. This classification grants no authority.
- Durable knowledge and `bd remember`: `/alaa-memory-os`.

<!-- END ALAA BEADS BINDING -->

## Use of this template

This file is the canonical text of the Beads binding block. It is information for the owner of a repository; no script renders it.

- Copy the text from the `BEGIN` marker to the `END` marker into the repository's main instruction file. Replace each `__PROJECT__` with the repository's project name and `__BEADS_WORKSPACE__` with the path that `bd where` must report for the bound hub. Keep both markers, so that a later refresh replaces only this block.
- The workspace line of a binding block is the one place where a machine path is allowed. This template holds a placeholder, because a template states no machine path.
- Writing the block into a repository needs that repository's own authorization.

## Allow-list entries for these commands

The block and its owner sections run the commands below. A repository that wants them to run without a permission prompt lists them in its own allow-list. The entries below use the Claude Code form of `<repo>/.claude/settings.json` `permissions.allow`; a Codex repository states the same commands in its own rules file. Each entry must match the flag order that the block writes: `--sandbox` before the subcommand and `--actor` after it. This list is information only: this skill changes no settings file, and an allow-list entry grants no authority that the block withholds.

Read commands:

```text
Bash(bd where *)
Bash(bd ping *)
Bash(bd list *)
Bash(bd show *)
Bash(bd ready *)
Bash(bd blocked *)
Bash(bd search *)
Bash(bd lint *)
Bash(bd stale *)
Bash(bd dep cycles *)
Bash(bd prime *)
```

Write commands:

```text
Bash(bd --sandbox create *)
Bash(bd --sandbox update *)
Bash(bd --sandbox close *)
Bash(bd --sandbox comments add *)
Bash(bd --sandbox dep add *)
```

`bd unclaim` changes who holds an issue and is rare, so a permission prompt for it is a useful check. No entry is needed for `bd heartbeat`: no rule uses it.

As read on 2026-11-17, the allow-list of the skills repository had `create`, `update` and `close` only in the other flag order (`bd --sandbox --actor * <subcommand> *`), and no entry for `comments add`, `dep add`, `search` or `dep cycles`.
