# Workflow Plan - Pack finalization WSL-only no basic memory beads-first no fixtures

- Plan kind: execution
- Approved design: embedded
- Approval status: approved
- Approval by: sohrab
- Approval on: 2026-11-02
- Approval evidence: /goal prompt of 2026-11-02 in the Claude Code session
- Task ID: `20261102-230000_pack-finalization`
- Mode: `plan`
- Profile: `resumable`
- Task store: `beads`
- Task binding: AGENTS.md#beads
- Task hierarchy: phase-task-subtask
- Review boundary: final
- Final phase: Phase 3
- Commit authority: local commits pre-authorized (main instruction file)
- Status: completed
- Created: `2026-11-02T19:39:42Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20261102-230000_pack-finalization-state.md`
- Machine state: not created
- Base branch and commit: main @ eb0fba92539917975611b32151d2c3fde24beab8
- Work branch: main (local commits only)
- Worktree: none

## Summary and Outcome

- Current repository truth: merge eb0fba92 has the same tree as 6376c2b3; PC1 added only a vendor/skill-temporal-developer squash already present locally. The pack still carries dual-host (Windows/PowerShell) text, a Basic Memory store, local-only task fallback rules that forbid a Beads fallback, and fixture-based checker tests.
- Outcome: see the approved design below (Outcome and Acceptance).
- Strategy: 14 file-disjoint implementation lanes run in parallel under a Workflow, then independent instruction review and root checkers in normal mode, then per-lane local commits by the parent.

## Scope

- In scope: `skills/sohrab/**`, `scripts/**`, root `AGENTS.md`, `README.md`, `contributing.md`, `install-skills*`, `vendor/subtrees.json`, `vendor/basic-memory` (removal by move), live files under `docs/`.
- Out of scope: dated evidence under `outputs/`, `artifacts/`, `test-results/`, `docs/_agent_plans/`; every other vendor subtree; files outside the repository; push, tag, merge, remote sync.
- Constraints and assumptions: no `--self-test` and no fixture is executed in this run; nothing is deleted (move to `_to_delete/`); lanes never touch the Git index.

## Handoff Package

Field semantics are in the skill's `alaa-workflow references/context-continuity.md`.

- Confirmed facts (verified, each with how it was verified): merge eb0fba92 tree equals 6376c2b3 tree (`git rev-parse` of both gives 8a02b659); `~/.claude/skills/alaa-*` are symlinks into this checkout (`ls -la`); alaa-memory-os `ACTIVE_ADAPTER` is hindsight and ships store-basic-memory, store-hindsight, store-local references.
- Open assumptions (believed but unverified, each with what would verify it): user clarification 2026-11-02 narrows the fixture ban to testing, comparing and fixtures of the skills themselves (project tests stay) and adds a standing preference for short ASD-STE100 skill text; Phase 1 lanes were briefed before it, so Phase 2 must (a) remove skill-comparison and skill-eval machinery that lanes kept, (b) confirm no target-repository testing doctrine was removed, (c) run an STE pass over edited controlling text.
- Ruled out (approach, reason, evidence): reverting any part of eb0fba92 (nothing to revert, tree equality above).
- Read first on resume (ordered exact paths): `docs/agents/20261102-230000_pack-finalization-state.md`, `artifacts/pack-finalization-20261102/design.md`, `skills/sohrab/AGENTS.md`.
- Environment notes (command shapes that work here, and ones that look right but fail): run `init_workflow_files.py` without `-I` (it imports a sibling module); use `PYTHONDONTWRITEBYTECODE=1` for every Python call.
- Traps (looks correct, is not): the pack's own instructions tell agents to run `--self-test` after a checker change; every dispatch in this run overrides that and forbids it.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | before designing implementation or verification | always for implementation/verification | block dependent work |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | before editing any skill, rule or AGENTS.md text | every lane that edits controlling text | block dependent work |
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | before integration and closure | Phase 3 | block dependent work |

## Ordered Work

### Phase 1 - Ground and implement

- Status: completed
- Phase issue: alaa-wvja.1
- Depends on: none
- Reasoning and selection reason: the three themes share files, so lanes partition by owning skill and each lane applies all themes to its own paths.
- Settled/open decisions and invariants: design D1-D10; the orchestrator pair stays behaviourally identical.
- Risk and required observers: wording regressions in controlling text; observer is the independent instruction review in Phase 2. No fixture or self-test runs.
- Owned scope: per lane issue description.
- Excluded from this phase: git index changes, commits, push.
- Required skills: alaa-prompting-guide
- Work:
  - Task issue: alaa-wvja.1.1 [skills: inherit]
  - Task issue: alaa-wvja.1.2 [skills: inherit]
  - Task issue: alaa-wvja.1.3 [skills: inherit]
  - Task issue: alaa-wvja.1.4 [skills: inherit]
  - Task issue: alaa-wvja.1.5 [skills: inherit]
  - Task issue: alaa-wvja.1.6 [skills: inherit]
  - Task issue: alaa-wvja.1.7 [skills: inherit]
  - Task issue: alaa-wvja.1.8 [skills: inherit]
  - Task issue: alaa-wvja.1.9 [skills: inherit]
  - Task issue: alaa-wvja.1.10 [skills: inherit]
  - Task issue: alaa-wvja.1.11 [skills: inherit]
  - Task issue: alaa-wvja.1.12 [skills: inherit]
  - Task issue: alaa-wvja.1.13 [skills: inherit]
  - Task issue: alaa-wvja.1.14 [skills: inherit]
- Acceptance criteria: each lane reports changed paths, moved paths, normal-mode checks run, and unverified items; zero live Basic Memory, PowerShell-host or fixture-test text in its scope.
- Validation commands: lane-scoped grep plus the pack validator in normal mode (`python3 scripts/validate_sohrab_skill_pack.py`) read-only; load /alaa-testing-strategy before design or execution.
- Collection/repair/retest barrier and evidence owner: parent collects lane reports; repairs happen in Phase 2; evidence owner is each lane issue.
- Evidence observed: 14 lanes plus cleanup wave reported; all four root checkers exit 0 after the wave; moves confirmed with du -sb by each lane
- Review status: REVIEW_PENDING
- Review evidence: not run (final boundary owns acceptance)
- Commit: 0b462c55ea050edf66ffa712be84816b35c8bdec
- Snapshot: tested content is contained in the commit above

### Phase 2 - Validate and reconcile

- Status: completed
- Phase issue: alaa-wvja.2
- Depends on: Phase 1
- Reasoning and selection reason: independent review of controlling text and the root gates must follow all lanes because ownership rules span skills.
- Settled/open decisions and invariants: reviewers are read-only; findings are fixed by the owning lane scope.
- Risk and required observers: dangling cross-skill references, drift between the orchestrator pair, checker contracts; observers are alaa-instruction-reviewer lanes and the four root checkers.
- Owned scope: whole pack, read-only plus repairs.
- Excluded from this phase: commits, push.
- Required skills: alaa-prompting-guide, alaa-testing-strategy
- Work:
  - Task issue: alaa-wvja.2.1 [skills: inherit]
- Acceptance criteria: the four root checkers and the pack validator exit 0 in normal mode; reviewers return no unresolved finding.
- Validation commands: `python3 scripts/validate_sohrab_skill_pack.py`, `python3 scripts/check_skill_index.py`, `python3 scripts/check_fleet_references.py`, `python3 scripts/check_lifecycle_contract.py` (normal mode only).
- Collection/repair/retest barrier and evidence owner: collect all checker output once, repair, rerun the failing checker only; evidence owner is alaa-wvja.2.1.
- Evidence observed: Four root checkers, alaa-testing-strategy check_execution_contracts.py, both orchestrator validate_pack/check_agent_grants/check_agent_contracts/render_agents --check, install-skills.wsl.sh --dry-run, memory-os sha256sum -c: all exit 0 after two repair waves
- Review status: REVIEW_PENDING
- Review evidence: not run (final boundary owns acceptance)
- Commit: 0b462c55ea050edf66ffa712be84816b35c8bdec
- Snapshot: tested content is contained in the commit above

### Phase 3 - Integrate and close

- Status: completed
- Phase issue: alaa-wvja.3
- Depends on: Phase 2
- Reasoning and selection reason: commits and closure follow accepted review.
- Settled/open decisions and invariants: local commits only, no attribution trailer, no push.
- Risk and required observers: a commit that mixes lanes; observer is `git status` and per-commit diff stat.
- Owned scope: Git index and Beads issue state.
- Excluded from this phase: push, tag, merge, remote sync.
- Required skills: alaa-workflow
- Work:
  - Task issue: alaa-wvja.3.1 [skills: inherit]
- Acceptance criteria: every lane committed as one Conventional Commit; moved files confirmed at original size; tree clean; issues closed with verdict, version and evidence.
- Validation commands: `git status --short`, `ls -la` on each `_to_delete/20261102-*` directory, `bd lint` per closed issue.
- Collection/repair/retest barrier and evidence owner: none beyond the commands above; evidence owner is alaa-wvja.3.1.
- Evidence observed: git status clean; local commits per lane; git log eb0fba92..HEAD
- Review status: APPROVED-WITH-NITS
- Review evidence: Commits on main, tested at 0b462c55
- Commit: 0b462c55ea050edf66ffa712be84816b35c8bdec
- Snapshot: tested content is contained in the commit above

## Task Allocation

Admitted lanes are dispatched by the parent through the Workflow runtime with the session model; no model or effort override is selected here. Role authority: implementation lanes write inside their owned scope; reviewers are read-only.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| alaa-wvja.1.1 to alaa-wvja.1.14, text edits across skills | implementer (general-purpose subagent) | broad coupled wording edits | session model (inherited) | session effort (inherited) | user requested maximum capability on 2026-11-02; no override chosen | Workflow agent() default controls | concurrency capped by the runtime |
| alaa-wvja.2.1 review | read-only reviewer | independent acceptance | session model (inherited) | session effort (inherited) | independent of implementers | Workflow agent() default controls | concurrency capped by the runtime |

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: lanes alaa-wvja.1.1 to alaa-wvja.1.14, each with a disjoint path scope listed in its issue.
- Dependency edges and ready sets: Beads owns issue dependencies and readiness; the plan owns phase barriers and shared-resource conflicts.
- Disjoint writes and shared-resource conflicts: scopes are partitioned by owning skill; shared cross-skill statements are edited only by the lane that owns the stated rule; `_to_delete/` receives per-lane subdirectories.
- Integration barriers and parallel/serialized rationale: Phase 1 lanes run in parallel; Phase 2 starts after all lane reports; Phase 3 is serial.
- Consolidated tasks/checks and preserved outcome/evidence mappings: each lane keeps its own acceptance; root checkers run once in Phase 2.
- Phase collection, repair/retest and review barriers, owners and resume evidence: parent collects at the Phase 1 barrier; the final review boundary is Phase 3.
- Reusable evidence and invalidation conditions: a lane report stays valid until another lane edits a file it cites.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner records the validated snapshot and handles any explicitly authorized commit.
- Before execution, the Beads workspace, project, nodes, parent-child relations and blocking edges were verified with `bd where`, `bd show` and `bd dep tree` on 2026-11-02.

## Execution Position

- Position owner: `docs/agents/20261102-230000_pack-finalization-state.md` (current phase/task/subtask, blockers, next action).

## Approved Design

Approved in this session; the text after the start marker is the approved design, copied verbatim. Keep this section last and never edit that text; a material change returns Approval status to pending.

<!-- approved-design:start -->

## Outcome

The first-party pack in `skills/sohrab/` and the checkers in `scripts/` describe exactly one host (WSL Linux, Bash), exactly two memory modes (`local` and `hindsight`), one task authority policy (Beads whenever reachable, `local` plan tasks only when it is not), and no fixture-based test surface. One new skill maps legacy Windows paths to their WSL locations.

## Merge decision (already verified)

Commit `eb0fba92` is a merge whose tree equals the tree of `6376c2b3` (`git rev-parse` of both trees agree). PC1 contributed only a squash of `vendor/skill-temporal-developer` whose tree equals the one already merged on this machine. Nothing is kept or reverted from it.

## Decisions

| # | Decision | Reason |
|---|---|---|
| D1 | WSL is the only host. Delete dual-mode (PowerShell / Git Bash / Windows path) instructions; keep Windows text only where Windows is the subject of the skill's domain (a target platform, not the agent host). | The user migrated; other PCs migrate before use. |
| D2 | One new skill, `alaa-legacy-path-map`, owns old-Windows-path to WSL-path translation for project documents and Hindsight recall. It is the single allowed holder of legacy machine paths. | Documents and Hindsight may still advertise old paths. |
| D3 | Memory modes are `local` and `hindsight`. `store-basic-memory.md`, every Basic Memory command, hook, checker branch, README row and the `vendor/basic-memory` subtree are removed. | The user stops using Basic Memory. |
| D4 | Beads is the task authority whenever `bd` is installed and `bd where` resolves the bound workspace. Otherwise the plan runs `Task store: local`. Once Beads is reachable, every new task in any family, including a previously local one, is registered in Beads. Existing open local tasks may be migrated; a task lives in exactly one store. Beads capabilities are used to the extent the installed `bd` help verifies. | The user's rule 3. Replaces "missing binding blocks, no silent local fallback". |
| D5 | Fixture tests are removed from the project: every `--self-test` mode, every `scripts/fixtures`, `test/fixtures`, `*/scripts/fixtures`, red/green corpora, and every instruction to run them. The validation pack is the root checkers in normal mode plus each skill's own normal-mode validator. Nothing in this run executes a fixture test or `--self-test`. | The user's explicit prohibition. |
| D6 | A fixture-named path that a skill uses at runtime as an asset (a template, a sample consumed by a shipped tool in normal mode) is not a fixture test and stays. | Removing it would break shipped behaviour. |
| D7 | The Crockford Base32 cross-implementation conformance harness stays unmodified and unrun. | `skills/sohrab/AGENTS.md` requires one for multi-implementation wire formats; it is a differential corpus, not a fixture test of a checker. Reported to the user as a retained decision. |
| D8 | Nothing is deleted. Removed files move with `mv` into `_to_delete/20261102-<reason>/` at the repository root; size is confirmed with `ls -la`. Lanes do not touch the Git index; the parent stages and commits. | Repository rule; avoids index lock contention between parallel lanes. |
| D9 | Dated evidence under `outputs/`, `artifacts/`, `test-results/` and `docs/_agent_plans/` is history. It is not rewritten. | Evidence records what happened then. |
| D10 | `~/.claude/rules/*` and other files outside the repository are reported, not edited. | Outside the working tree. |

## Scope lanes (file-disjoint)

Each lane owns the listed paths for all four themes. A lane edits only its own paths, never runs `--self-test` or a fixture, never commits, and reports changed paths, moved paths, checks run and unverified items.

## Acceptance

- The four root checkers and the pack validator exit 0 in normal mode.
- No live file under `skills/sohrab/`, `scripts/`, root docs or `install-skills*` mentions Basic Memory, PowerShell as a host option, or a fixture test.
- `vendor/subtrees.json` and generated doc blocks list no Basic Memory source.
- `alaa-legacy-path-map` is registered in both indexes and passes the validator.
- `alaa-workflow` and both orchestrators state the same Beads-first policy.
- Every moved file is confirmed at its original size under `_to_delete/`.
