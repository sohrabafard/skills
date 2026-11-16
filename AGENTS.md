# Repository instructions

This repository is a skill pack for coding agents, not an application. It ships Agent Skills that
Claude Code and Codex both load. Edit every shared rule here and nowhere else, because
`CLAUDE.md` beside this file is a symlink to this file. The host is WSL Linux with Bash and `python3`.

<!-- BEGIN ALAA BEADS BINDING -->

## Beads

Project label: `repo:skills`

Expected workspace: `/home/sohrab/project/alaa-task-hub/.beads`

User, repository and orchestrator constraints govern. This binding overrides conflicting upstream Beads skill or hook guidance and grants no authority. Under Codex, read each `/name` as `$name`. A `##` name is a section of `/alaa-workflow` `references/task-tracking.md`, unless a file is named; if it cannot load, run no `bd` write.

**Availability.** Before other `bd` commands, run `bd where` and verify the expected workspace, then `bd ping`. If both pass, Beads is the task authority for new tasks. Otherwise report the failure, run no other `bd` command, initialize no database and change no connection, and select the store under `## Select before tracking-dependent work`.

**Resume.** Run these at session start, after a compaction, and whenever you cannot name your position:

```bash
bd list --status=in_progress --label "repo:skills" --assignee "<actor>"
bd show <id>   # root, then leaf
```

Without a known actor, omit `--assignee` and find your leaf through the root's `Lane:` lines. Position is the last checkpoint block in `notes`; knowledge is tagged comments. No summary or `bd prime` replaces this read. Owner: `/alaa-workflow` `references/context-continuity.md` `## Task resume and phase resume`; another PC: its `## Cross-PC handoff record`.

**Work.**

- Pass `--label "repo:skills"` to `ready`, `list` and `blocked`, and label each new issue. Verify an issue's label before you change it; never relabel one into scope. Other-project writes need the user's authorization.
- Search before you create. A follow-up takes `--deps "discovered-from:<origin-id>"` and authorizes no implementation.
- Claim before you work, then read the issue back; a failed claim or guard mismatch gives no ownership. Write as `bd --sandbox --actor "<actor>" <subcommand>`, under `## Agent identity and ownership`.
- Append a checkpoint block when the position changes and before you stop or hand off.
- Close only after acceptance, the required checks and `bd lint <id>` pass, never for a handoff or a compaction. Reason: `## Close reason`.
- Commands: `## Beads capabilities in use`. Fields: `## Issue fields`. Evidence: `## Acceptance and evidence by level`. Failed write: `## Outage and uncertain writes`; never report unsaved state as saved.

**Authority.**

- Local commits on the current work branch are pre-authorized: one Conventional Commit per finished, validated topic or lane.
- Push, tag, merge into another branch, history rewrite and remote sync (Git or Dolt) need explicit user authorization; a profile, hook or skill grants none. Report a pending unauthorized action.
- `bd` commands that read or write the expected workspace are this repository's own task tracking, not changes outside this repository, even when a task or goal forbids such changes. This classification grants no authority.
- Durable knowledge and `bd remember`: `/alaa-memory-os`.

<!-- END ALAA BEADS BINDING -->

## Layout

- `skills/sohrab/` — the first-party pack. `skills/sohrab/AGENTS.md` is the binding contract for any
  change inside it. Read that file before editing a skill. Do not restate its rules here.
- `vendor/` — upstream git subtrees, listed in `vendor/subtrees.json`. Off limits: never edit a file
  under it. `skills/sohrab/AGENTS.md` states that rule in full and owns it.
- `skills/.curated/`, `skills/.system/` — third-party skills. Referenceable, not pack-local.
- `scripts/` — this repository's checkers. `install-skills.md` is authoritative for install paths.
- `artifacts/`, `outputs/`, `test-results/` — task artifacts. Put the products of one piece of work in
  one directory, named for its subject, under one of these. Create the directory if absent.

## Upgrade history

Before upgrading first-party skills or their model policy, read [the upgrade evidence index](outputs/README.md).
It lists prior assessments, plans and verification records. Treat those records as dated evidence.
Verify current repository and upstream facts before reusing their conclusions.

## Commands

Run each command from the repository root with `python3`. The first four commands ran in normal mode on 2026-11-02. Each exited `0`. `vendor_subtrees.py refresh-docs` was not part of that run.

- `python3 scripts/validate_sohrab_skill_pack.py` — per-skill structure: frontmatter, description
  budget, the "When NOT to use" heading, `agents/openai.yaml` shape, and reference-path resolution.
- `python3 scripts/check_skill_index.py` — both skill indexes in `skills/sohrab/` against the
  directory, in both directions, plus this file and `CLAUDE.md`.
- `python3 scripts/check_fleet_references.py` — every cross-skill citation in the pack.
- `python3 scripts/check_lifecycle_contract.py` — the four completion-lifecycle states: defined in
  one owning file, named by both orchestrators' final reports, and restated nowhere else.
- `python3 scripts/vendor_subtrees.py refresh-docs` — regenerates the marked blocks in the root
  `README.md` and in `install-skills.md` from `vendor/subtrees.json`.

Every script here shares one exit-code contract: `0` clean, `1` findings, `2` could not run. A
`2` is a failed gate, never a pass.

## Rules

- **Nothing is deleted.** Move a retired file to `_to_delete/<YYYYMMDD>-<reason>/` and confirm with
  `ls -la` that it arrived at its original size. `skills/sohrab/AGENTS.md` owns this rule. This file
  names it because `_to_delete/` is a root-level directory.
- **Keep capability evidence and runtime control mechanics in one owner:** `/alaa-prompting-guide`.
  It owns supported model/effort pairs and checked model-neutral role projections. Runtime
  orchestrators own actual task allocation/admission for every authority role. Workflow records it.
  A role name or metadata default never chooses a task pair.
- **Before writing skill calls or reference routers, read `skills/sohrab/AGENTS.md`.** It owns
  the single `/name` repository form, metadata and generated-prompt exceptions, legacy conversion,
  and router placement.
- **Before shortening or editing any text that will control another agent** — a prompt, a rule, a
  skill, this file, a `CLAUDE.md`, a constitution, or a subagent dispatch — apply the compression
  contract in `skills/sohrab/alaa-prompting-guide/references/60-skill-authoring.md`. It owns what
  may never be cut and the test the rewrite must pass. This file names it because the rule binds work
  anywhere in this repository, including work that never touches `skills/sohrab/`.
- **Write English into every file.** A Persian document is a mirror of an English source, and
  `alaa-repo-docs` owns when one is produced. A reply to the user may be Persian; a file is not.
- **Require an authoritative source for a concrete claim.** Never read a missing result as a
  negative result. Use a named placeholder rather than an invented specific.
- **Never write a path from one machine.** Never put a Windows drive path or an absolute home path in
  a committed file. Write it relative to the repository root. Two exceptions: the `Expected workspace`
  line of the Beads binding, which names the shared hub path, and `alaa-legacy-path-map`, which owns
  legacy Windows-to-WSL path translation.
- **Ask before an action with an effect outside this working tree** — tag, push, merge into another
  branch, history rewrite, publish, deploy, force-push, or credential rotation. Local commits are
  pre-authorized under the Beads binding's commit rule.
- **No emoji in any artifact.** When a request is ambiguous, contradictory, or unsafe, say so, ask
  the smallest question that resolves it, and stop.

<!-- BEGIN ALAA CODE INTELLIGENCE BINDING -->
## Alaa code-intelligence binding

Invoke `/alaa-code-intelligence-routing` before non-trivial code-intelligence evidence selection. That skill owns selection among CodeGraph, Serena, the active stack semantic owner, and repository-native tools, and prevents duplicate retrieval of the same fact. CodeGraph's installer owns exact CodeGraph usage instructions after CodeGraph is selected. Use CodeGraph and the configured semantic owner only when their active project or root resolves to this Git worktree, or under that skill's lane-worktree rule. Native repository gates prove completion. Do not modify MCP, hook, CodeGraph, Serena, or language-server integration configuration unless the task explicitly requests setup, upgrade, repair, or removal.
<!-- END ALAA CODE INTELLIGENCE BINDING -->
