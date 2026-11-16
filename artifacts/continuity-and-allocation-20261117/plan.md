# Continuity, allocation fit, advisor handling and output reach — design

## Context

After the compression work (merged as `d82abfc7`, pack version 7.0.0), the owner asked for four
behaviour changes, to be planned and then executed:

1. Beads use that stays safe when several agents or lanes work on one topic, costs fewer
   commands, and always holds enough position and knowledge for an agent to continue after a
   compaction or in a new session.
2. Orchestrators that choose a model and an effort that fit each lane: not needlessly strong,
   not needlessly weak.
3. `alaa-prompting-guide` handles advisor use whenever it writes a prompt for a Claude model.
4. `alaa-low-noise` makes agents report briefly and keep command output out of the context.

Owner decisions on 2026-11-17: no hook or settings change; no transcript measurement.

Evidence from read-only exploration on 2026-11-17:

| Finding | Source |
|---|---|
| `bd ready` excludes every in-progress issue; three issues whose lease expired on 2026-10-31 are absent from it. `bd reclaim` is the only command that reverts a stale lease, and the pack allows it only inside stopped-writer recovery | `bd ready --help`, `bd reclaim --help`, `bd show --long`, `task-tracking.md` |
| Not established: whether another actor's `--claim` succeeds on an in-progress issue with a stale lease | help text is silent; Phase 0 reads the source |
| `bd show <id>` prints description, design, acceptance, notes and comments in one call; `bd list` filters by `--assignee` | observed; `bd list --help` |
| The six-field handoff sits in the root `description`, so each update rewrites the whole field | `task-tracking.md` native plan table |
| The root `AGENTS.md` Beads block is 1,208 words, always loaded; its only template, in `artifacts/agent-control-defaults-20261018/`, has drifted, and no live checker reads the block | mapping lane |
| Allocation text pushes only toward cheaper pairs, has no rule for effort within a model, no guard against a pair that is too strong, and no feedback after a lane returns | both `references/routing-matrix.md` |
| No agent definition preloads `alaa-low-noise`; none bounds command output; 41 of 70 carry no return-length rule | both packs' `agents/` |
| Advisor prompt rules exist in `41-claude-code-runtime-features.md`, but only a topic-map row routes to them | `alaa-prompting-guide` |
| The project allow-list covers `bd create`, `update`, `close` and read commands, not `comments add`, `reclaim` or `dep add` | `.claude/settings.json` |

Recorded owner decisions that stay: the orchestrator owns allocation for every role; role names
select no pair; no executable pins; no trial ladder; no quotas; the balanced default priority;
old `gpt-6-sol` excluded; the mechanical branch; batch allocation; the omitted-control defaults;
the read-back that every dispatch carries both controls (5.8.0).

## Fixed interface texts

Lanes run in parallel and cannot see this conversation, so these texts are fixed here and saved
to the artifacts directory in Phase 0. A lane may shorten wording, not meaning.

**I1 — Checkpoint.** The claim holder appends this block to the leaf issue's `notes` with
`bd update <id> --if-assignee <actor> --append-notes`. The last block is the current one. The
holder may replace the whole field with `--notes` to drop old blocks.

```text
Position: <what is done>
Next: <the next action: command or edit target, and the expected result>
Blockers: <none | each blocker and who can clear it>
Evidence: <last verified result: command, outcome, commit or artifact path>
Touched: <uncommitted paths, or none>
```

The root `notes` hold the same block for the engagement, plus one line per live leaf:
`Lane: <leaf id> <actor>`.

**I2 — Knowledge comments.** Any actor appends a comment that starts with one tag:
`fact:` (with how it was verified), `assumption:` (with what would verify it), `ruled-out:`
(with the reason), `read-first:` (a path), `env:` (an invocation that works or fails here),
`trap:`, `decision:`. The tags are the six handoff fields plus decisions. Engagement-wide
knowledge goes on the root, task-local knowledge on the leaf. Nothing is rewritten.

**I3 — Resume commands.**
`bd list --status=in_progress --label "<project-label>" --assignee "<actor>"`, then
`bd show <id>` for the root and for the leaf. An agent that cannot name its actor omits
`--assignee` and finds its leaf through the `Lane:` lines of the root. The actor's run part is
the session identifier that the host exposes, so the same session derives the same actor after
a compaction.

**I5 — Output rule** for every agent definition: "Bound each command's output: use a quiet
flag, a filter or `tail`, or redirect to a file and read only the failing slice. Never print a
whole file, log, tree or diff."

## Workstream 1 — Beads: parallel-safe, lighter, resumable

Owner: `alaa-workflow`. Files: `references/task-tracking.md`, `references/context-continuity.md`,
`SKILL.md`, `references/companion-routing.md`, `references/phase-prompts.md` and
`assets/phase-prompts-template.md` (one advisor pointer each), a new
`assets/beads-binding-template.md`, and the Beads block of the root `AGENTS.md`.

1. **Plan shape by size.** One bounded task is one issue. Several tasks are a root epic with
   leaf tasks directly under it. A phase milestone exists only where a real barrier separates
   two groups of tasks. `Final phase` stays as a root field and names the last phase, or the
   root when the plan has no phase. Each leaf states its owned paths; two ready leaves never
   share a file. That rule is what lets several agents work in one checkout without worktrees.
2. **Ownership.** Keep: a distinct actor per agent, `--actor` on every write, claim then one
   read-back, `--if-assignee` and `--if-status` on every update, exit 13 handling, no force
   flag, and "claim only unassigned work, never an in-progress issue, whatever its lease".
   Remove: the heartbeat duty and the TTL read. The removal holds only if Phase 0 confirms from
   the source that no pack-allowed command hands a stale-lease issue to another actor;
   otherwise the heartbeat rule stays and the report says so. Close: `bd lint`, then close; read
   the issue first only after a resume, an outage or a transfer. Keep
   `Registration: draft|registered`, because other agents claim from `bd ready`; its checks
   stay `bd dep cycles` and one ready query.
3. **Write lanes own their leaf; the lead accepts.** A dispatched write lane claims its leaf
   with its own actor and appends checkpoint I1 before it returns or stops. The lead closes the
   leaf after it reconciles the lane's diff, so a dependent leaf becomes ready only then. The
   lead keeps the root checkpoint with its `Lane:` lines. A rejected leaf gets a follow-up task
   with a `discovered-from` edge.
4. **Continuity.** Position is checkpoint I1. Knowledge is comments I2; the root description
   no longer carries the handoff. Keep the six write events, the cold-start test and the rule to
   repeat the resume protocol after compaction. Add the native resume as commands I3, and one
   recipe for a new session that finds its own earlier claim: verify that the earlier writer
   stopped (stopped-writer recovery), `bd reclaim --id <id>`, claim, read back, continue from
   the last checkpoint block.
5. **Capability table.** One table of adopted commands with their rules, and one row that
   rejects every other command, with the remote and destructive class needing explicit
   authorization. Keep each dated verification line.
6. **Binding block.** Rewrite the root `AGENTS.md` Beads block to about a third of its size:
   label, workspace, precedence, the availability test, commands I3 with "run them at session
   start, after a compaction, and whenever you cannot name your position", the label filter,
   search before create, claim before work, close after acceptance, the sync and push limits,
   and one pointer per owner section. Add the same text as
   `alaa-workflow/assets/beads-binding-template.md` with a `__PROJECT__` placeholder and the
   allow-list entries a repository needs. The block is instruction text that survives
   compaction, so it carries the resume trigger that a hook would otherwise carry.
7. **Low-noise binding.** `SKILL.md` Start and `references/companion-routing.md` bind
   `/alaa-low-noise` for the lead session only; lanes get rule I5 from their definition.

Kept verbatim, because other repositories still carry the old block: the headings
`## Select before tracking-dependent work`, `## Agent identity and ownership`,
`## Beads capabilities in use`, `## Close reason`, `## Acceptance and evidence by level`,
`## Issue fields`, `## Outage and uncertain writes`, and in `context-continuity.md`
`## Task resume and phase resume`, `## Cross-PC handoff record`. Each still states what the old
block cites it for, and the old block's `--append-notes` command stays correct under I1. The
Markdown plan family, its templates and both workflow scripts are out of scope.

## Workstream 2 — Allocation that fits the lane

Owner: the orchestrator pair, mirrored. Files in both packs: `references/routing-matrix.md`,
`references/model-effort-policy.md`, `SKILL.md`, `references/delegation-prompts.md`;
`alaa-prompting-guide references/50-effort-and-thinking.md` gains the lowering rule.

1. Replace step 3 "Select the cheapest suitable pair" with "Select the pair that fits". The lead
   records two facts per lane and reads the pair from a fit table:
   - **judgment left to the lane**, which selects the model: none (exact transformation);
     bounded local decisions with a discriminating check; grounded everyday decisions; coupled
     or cross-boundary unresolved decisions; judgment-dense work that no check can catch, or
     hours of autonomous work;
   - **search and length**, which selects the effort: short and fully specified; ordinary;
     long, multi-file, strict, or hard to verify; hardest long-running work with a measured gain.
   Each pack's table names its own models and effort levels and cites the row of
   `alaa-prompting-guide references/90-model-selection.md` that supports each cell. No number
   or default moves out of the prompting guide.
2. State both defects with equal force. Too strong: a frontier model or a high effort on a lane
   whose decisions are settled and whose check discriminates; a raise because of a title, a
   sensitivity label or a second lens. Too weak: a bounded model on a lane that must settle
   coupled decisions; a low or default effort on a long lane that no check can catch; a cheap
   pair chosen while a fit predicate fails.
3. Effort within a model: start at the surface default; raise one level for a long, strict or
   unverifiable lane; lower one level for a short, fully specified or high-volume lane; use the
   two highest levels only with a recorded measured gain.
4. Frontier models stay evidence-gated, as one row of the table: an official row that matches
   the lane, a strong pair that fell short after the dispatch was repaired, or an explicit user
   selection.
5. Feedback for the remaining work, at the existing reassessment points: a lane that returns
   light or incomplete after a specific dispatch raises one step for the rest, effort for a
   search shortfall and model for a judgment shortfall; a lane that finishes trivially on a
   strong pair lowers the pair for the remaining similar lanes. Completed work is not replayed,
   so this is not a trial ladder.
6. The allocation record becomes one line: the pair and the table row that selected it.

Expected pairs, fixed now so the walkthrough tests the table and not the reverse. Claude Code:

| Sample lane | Expected pair |
|---|---|
| Exact rename over many enumerated files, with a cheap check | Haiku 5.5, medium |
| Bounded comparison of sources against four files | Sonnet 5.5, medium |
| Everyday feature with known patterns and explicit acceptance | Sonnet 5.5, medium |
| Refactor across services with unresolved contracts | Opus 5.5, medium; high when it is long |
| Judgment-dense instruction rewrite that no check can catch | Opus 5.5, high; Fable 5.2, high after a strong pair fell short or on owner selection |
| Migration that runs unattended for hours | Fable 5.2, high |
| Second-lens review of a broad change | The pair its scope needs, Opus 5.5 at medium or high; never stronger because it is second |

The Codex table must give, for the same seven lanes, the cells that the official matrix in
`90-model-selection.md` assigns; LB records those cells before it writes the table.

Checker literals in `BOUNDED_REQUIREMENTS` and the allocation tuples follow the text one-to-one,
or are deleted with a ledger row; checker logic does not change.

## Workstream 3 — Advisor in Claude prompts

Owner: `alaa-prompting-guide`. Files: `SKILL.md`, `references/41-claude-code-runtime-features.md`,
`references/06-invocation-and-composition.md`; consumers by pointer only: cc
`references/model-effort-policy.md` and `references/delegation-prompts.md`, and the workflow
prompt files (through Workstream 1).

1. `SKILL.md` decision procedure gains a step: for a Claude target, apply `41` *Prompts for a
   session that may have an advisor* before you ship a prompt, a system prompt or a dispatch.
2. In `41`, turn the nine rules into one table an author applies in a single read. Rows: the
   surface (Claude Code session or subagent; API or SDK system prompt) by the executor model.
   Each cell says exactly what to write, and "write nothing" is a valid cell: the current text
   already says to add no timing block for a Claude Code subagent and no nudge for an Opus
   executor. Above the table, the four things every Claude prompt does whether or not an
   advisor exists: state goal, constraints and acceptance in the prompt text; have the executor
   write a decision in visible text before it acts on it; save the deliverable before the
   completion consultation; never depend on the advisor. The source check in Phase 0 decides
   each cell; no consultation sentence is fixed in this plan. Keep every dated source.
3. `06` kickoff composition points to that step for a goal that will run long on a Claude model.
4. cc `model-effort-policy.md`: when the lead's session has an advisor, the lead consults it
   before it ratifies the plan and before the final report; consultation changes no pair,
   authority or gate. cc `delegation-prompts.md` and the workflow prompt files point to the
   table and state no advisor text of their own. The codex pack records in its changelog that
   it has no equivalent.

## Workstream 4 — Output discipline that reaches agents

Owners: `alaa-low-noise` and the orchestrator pair.

1. Every agent definition in both packs carries rule I5 and the return-length default, through
   the shared blocks and the three contract assets. The 41 definitions that had neither gain
   both. The implementation contract also carries checkpoint I1, because a lane does not load
   workflow references.
2. With I5 in every definition, a dispatch names `/alaa-low-noise` only for a discovery-heavy
   or log-heavy lane. `SKILL.md` "Every dispatch carries `/alaa-low-noise`" changes to that.
3. `alaa-low-noise/SKILL.md`: put the four rules that save the most context first; add a
   default command-output budget as a default with its exception; keep the progress budget;
   keep `## Delegated lanes` in `references/workflow-integration.md` as the owner of the return
   shape.

## Execution

Phase 0, lead.
- Create `work/continuity-and-allocation` in its own worktree.
- Save this plan, the interface texts and both mapping reports to
  `artifacts/continuity-and-allocation-20261117/`.
- Register the Beads plan under the rules that are live now.
- One `alaa-researcher` dispatch (Sonnet 5.5, medium): re-read the Code advisor and Advisor
  tool pages, the Claude and OpenAI model-selection guides, the Codex models and subagents
  pages, and the claim path of the installed Beads version's source; report only differences
  from `41`, `90`, `50` and `12`, the advisor cell per surface and model, and whether any
  command can hand a stale-lease issue to another actor.
- Record which `bd` subcommands the project allow-list covers.

Phase 1, three write lanes in parallel, each in its own worktree fast-forwarded to the
integration branch, each with a ledger of changed and removed rules:

| Lane | Scope | Pair |
|---|---|---|
| LA | Workstream 1, the advisor pointers in the workflow prompt files, the root `AGENTS.md` block, and the checker clauses that bind those files | Fable 5.2, high, by owner selection through approval of this plan |
| LB | Workstreams 2 and 4 in both packs, and the pair side of 1 and 3: `<beads_identity>` default `claim`, I1 and I5 in the contracts and shared blocks, the cadence text that names plan fields, the advisor pointer; checker clauses; `VERSION` 7.1.0; changelog; `render_agents.py --write` | Fable 5.2, high, by owner selection through approval of this plan |
| LC | Workstream 3 in `alaa-prompting-guide`, the lowering rule in `50`, and Workstream 4 item 3 in `alaa-low-noise` | Opus 5.5, medium: bounded edits with settled content |

Phase 2, lead.
- Merge each lane into the integration branch after its gates pass.
- Walk the seven sample lanes through each pack's fit table and compare with the expected
  pairs above. Walk one cold-start resume from Beads content alone, using this engagement's own
  root and one leaf. Record both walkthroughs.
- One `alaa-instruction-reviewer` lane (Opus 5.5, high) over ownership, allocation, the binding
  block and the agent blocks, with the before text supplied as files. Fix blocker and major
  findings; record the rest. No confirmation pass.
- Write the report and its row in `outputs/README.md`. Commit on the integration branch.
- Stop. Report to the owner that the branch is ready.

Phase 3, only on the owner's word: merge into `main` with `git merge --no-ff`, install the
managed agents of both runtimes, compare the Claude files with the 7.1.0 manifest, remove the
worktree and branch, close the Beads tasks.

## Out of scope

Hooks and settings; transcript measurement; the Markdown plan family and both workflow scripts;
checker logic; the role roster; the policy JSON data; other skills; the Beads block of any
other repository; push, tag and remote sync.

## Verification

- All sixteen gates of the previous engagement exit 0 on the final tree: the four root
  checkers; `check_execution_contracts.py`; in each pack `render_agents.py --check`,
  `validate_pack.py`, `check_agent_contracts.py`, `check_agent_grants.py`; the three
  prompting-guide checkers.
- Each heading listed under Workstream 1 as kept returns one `grep -n` hit.
- The fit-table walkthrough gives the expected pairs; the cold-start walkthrough names the next
  action from `bd show` output alone; the review verdict and its dispositions are in the report.
- Not proved by any of this: live agent behaviour. The owner's project tests are the evidence
  for that. What to watch there: the model and effort on each dispatch line of the final
  report; whether a new session resumes from `bd show` alone; the number of `bd` commands per
  task; the size of lane returns and of command output in the terminal.
