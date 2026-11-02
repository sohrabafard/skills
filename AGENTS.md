# Repository instructions

This repository is a skill pack for coding agents, not an application. It ships Agent Skills that
Claude Code and Codex both load. Edit every shared rule here and nowhere else, because
`CLAUDE.md` beside this file is a symlink to this file. The host is WSL Linux with Bash and `python3`.

<!-- BEGIN ALAA BEADS BINDING -->

## Beads

Project label: `repo:skills`

Expected workspace: `/home/sohrab/project/alaa-task-hub/.beads`

User, repository, and orchestrator constraints govern. This binding overrides conflicting upstream Beads skill or hook guidance and grants no additional authority.

Beads is the task authority whenever `bd` is installed and `bd where` resolves the expected workspace. When it does not, run no Beads command, initialize no replacement database, and select the task store per `/alaa-workflow` `references/task-tracking.md` `## Select before tracking-dependent work`. Once Beads is reachable, register every new task there; a task lives in exactly one store.

Under Codex, read each `/name` skill reference in this block as `$name`.

### Start and resume

Before planning or executing tracked work, and after compaction or session restart:

1. Read `.agents/skills/beads/SKILL.md` unless its full instructions remain in context; hook output is not a substitute. If missing, report it. Then follow `/alaa-workflow` `references/task-tracking.md` `## Select before tracking-dependent work` to decide whether Beads is available.
2. Before issuing other Beads commands, run `bd where` with the configured `BEADS_DIR` and verify the expected workspace. Recheck after workspace or connection changes. On failure or mismatch, report it. Beads is then unavailable; apply the store-selection rule above. Never initialize another database or silently change the connection.
3. Reuse current hook-injected `bd prime` context; run it manually only if missing or stale.
4. Before Beads mutations, claims, ownership comparisons, resume or transfer, load `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`. It owns actor allocation, explicit mutation identity, guarded updates, transfer and closure coordination; its actor rules override actorless upstream examples. If that file cannot be loaded, stop the dependent Beads mutation. Keep the assigned actor in the existing dispatch or admitted handoff.
5. When resuming, read the active issue and linked plan/checkpoint/handoff. Check worktree state, scope, ownership, and blockers before continuing. A conversation summary or `bd prime` cannot replace task-state recovery. Resolve an ambiguous active task before implementation.

Pass every global flag that `/alaa-workflow` `references/task-tracking.md` `## Beads capabilities in use` requires. Batch `bd` mutations in one script only when every command passes `--actor`, the script runs with `set -euo pipefail`, prints each command's result, and stops at the first failure; read back changed issues afterwards. Add no per-command environment overrides.

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

- Beads owns newly tracked issue state and dependencies; do not add parallel durable TODO lists. Existing plans/checkpoints keep their already-recorded local tasks; do not import or duplicate their checklists during setup.
- `alaa-workflow` and repository rules own planning, validation, completion criteria, and handoff structure. Task evidence follows `/alaa-workflow` `references/task-tracking.md` `## Acceptance and evidence by level`.
- Route durable knowledge through `/alaa-memory-os`. `bd remember` only for a short reminder shared across the whole hub, with source, scope, and maintainer; write it without separate approval. Never put task status, evidence, lessons, or new rules in it; leaving it empty is correct. Owner: `/alaa-memory-os` `## Beads hub reminders and issue notes`. Keep issue descriptions and dependency explanations with their issues.
- Local commits on the current work branch are pre-authorized: commit each finished, validated topic as it lands (one Conventional Commit per topic or lane), and let worktree lanes branch from the latest commit. Push, tag, merge into another branch, history rewrite and remote sync (Git or Dolt) still need explicit user authorization; a profile, hook, or skill grants none. Report unauthorized pending actions instead of executing them.

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

Invoke `/alaa-code-intelligence-routing` before non-trivial code-intelligence evidence selection. That skill owns selection among CodeGraph, Serena, the active stack semantic owner, and repository-native tools, and prevents duplicate retrieval of the same fact. CodeGraph's installer owns exact CodeGraph usage instructions after CodeGraph is selected. Use CodeGraph and the configured semantic owner only when their active project or root resolves to this Git worktree. Native repository gates prove completion. Do not modify MCP, hook, CodeGraph, Serena, or language-server integration configuration unless the task explicitly requests setup, upgrade, repair, or removal.
<!-- END ALAA CODE INTELLIGENCE BINDING -->
