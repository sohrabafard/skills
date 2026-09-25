# Workflow Plan - GPT-6 agent policy migration

- Task ID: `20260925-120000_gpt6-agent-migration`
- Mode: `execute`
- Profile: `resumable`
- Status: completed
- Created: `2026-09-25T09:32:30Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20260925-120000_gpt6-agent-migration-state.md`
- Machine state: not created
- Base branch and commit: `main` at `164d06a8944a87eb77a8b458c505b7efcb82268d`
- Work branch: `codex/gpt6-agent-migration`
- Worktree: none

## Summary and Outcome

- Current repository truth: 21 orchestrator agents and the rule-writer pin the previous GPT family; validators accept that family only. All ten approved baseline gates exited 0 before implementation.
- Outcome: implement the user-approved plan in `p.md`: one GPT-6-first policy owner, explicit candidate pins, truthful runtime evidence, synchronized role contracts, grants, installers, and validation.
- Strategy: standard orchestration; policy and pack lanes write disjoint scopes, then governance writes. Independent review and final integrated checks follow. No installation, commit, merge, publication, or memory-write authority was granted.

## Scope

- In scope: prompting-guide, Codex orchestrator, shared Claude orchestrator behavior, low-noise, directly affected workflow/governance/index/install docs and checkers.
- Out of scope: vendor subtrees, unrelated skills, installed home-directory copies, production systems and external publication.
- Constraints and assumptions: preserve user-owned staged/unstaged `p.md` unchanged (SHA256 `8995E51332EEE0F3F89E9D2BB1A5D40EC6C1F8B2AE5DB03A3FDBBFE4DB59B2FD`). Candidate settings are not benchmark-proven. Native source checks, materialization and real runtime evidence remain distinct.

## Handoff Package

Knowledge that lives only in the current agent's head and disappears on compaction. Fill a field when something is learned, not on a schedule; leave a field empty rather than padding it. Field semantics are in `alaa-workflow references/context-continuity.md`, which is in the skill, not in this repository.

- Confirmed facts (verified, each with how it was verified): native TOML inspection established 22 current GPT pins. Official subagent docs fetched in this task state custom-file pins take precedence over spawn values; current harness locks configured roles. Baseline gate logs are in `artifacts/gpt6-agent-migration/baseline-*.log`.
- Open assumptions (believed but unverified, each with what would verify it): quality and cost of proposed pins need the eight-scenario comparative evaluation; runtime activation needs authorized installation/fresh discovery. The local CLI/account cannot currently run the requested Luna probe, so the full comparative matrix is blocked rather than passed.
- Ruled out (approach, reason, evidence): silent legacy fallback, fixed Luna medium ceiling, overriding fixed custom profiles at dispatch, raw-copy installation, and model identity inferred from prompt literals.
- Read first on resume (ordered exact paths): this plan; `docs/agents/20260925-120000_gpt6-agent-migration-state.md`; user-approved `p.md`; `skills/sohrab/alaa-prompting-guide/assets/codex-model-policy.json`; `artifacts/gpt6-agent-migration/verification-summary.md`.
- Environment notes (command shapes that work here, and ones that look right but fail): PowerShell; use `python -B` and PYTHONDONTWRITEBYTECODE to avoid bytecode. Work-branch creation succeeded after filesystem escalation. Native memory registry is missing and no official Hindsight recall tool is exposed; proceed from current sources without recall. CLI version is 0.147.0. The ephemeral read-only Luna probe first failed on state/IPC permissions; its one exact escalated retry reached the backend and failed with HTTP 400, model unsupported for this ChatGPT account. Logs: `artifacts/gpt6-agent-migration/runtime-probe.log` and `runtime-probe-escalated.log`. This establishes only this CLI/account limitation; do not infer all GPT-6/API/desktop availability.
- Traps (looks correct, is not): the baseline manifest was stale despite baseline validation passing; deterministic rendering and drift fixtures now catch it; plain TOML copies inherit unsafe/unintended MCP configuration; configured identity is not observed runtime identity. Do not commit to manufacture a validation snapshot.

## Ordered Work

### Phase 1 - Baseline and source contracts

- Status: completed
- Depends on: none
- Owned scope: current repository inspection and baseline evidence.
- Excluded from this phase: source mutations and installed files.
- Work:
  - [x] Read the named sources and verify current behavior.
  - [x] Record all ten requested baseline checks and the protected user file.
- Acceptance criteria: previous failures and new regressions are distinguishable; approved model table is available in `p.md`.
- Validation commands: root structure, index, references, lifecycle; both pack validators and grants self-tests; rule-writer gate and self-test.
- Evidence observed: all ten exited 0; logs under `artifacts/gpt6-agent-migration/`.
- Commit: 164d06a8944a87eb77a8b458c505b7efcb82268d
- Baseline identity: existing HEAD contained the inspected source; no new commit was created.

### Phase 2 - Implement disjoint lanes

- Status: completed
- Depends on: Phase 1
- Owned scope: the three lanes recorded below.
- Excluded from this phase: installed agents, vendor files, user p.md, and index changes.
- Work:
  - [x] Establish canonical policy and refresh owner references.
  - [x] Migrate role definitions, render shared reviewer wrappers and manifest, and strengthen checks.
  - [x] Reconcile governance, mirrors, installation docs, and authorized-operation boundaries.
- Acceptance criteria: all approved profile pins match; no second policy owner; shared behavior is mirrored; side effects require actual authority.
- Validation commands: each lane's focused tests, self-tests and deterministic check modes.
- Evidence observed: all three implementation lanes completed; focused validators and independent regression probes passed. Corrective findings are resolved in artifacts/gpt6-agent-migration/verification-summary.md.
- Snapshot: HEAD 164d06a8944a87eb77a8b458c505b7efcb82268d; paths artifacts/gpt6-agent-migration/source-snapshot-manifest.json; SHA256 2e9b5ed0eb60d82ebc35792c9971399d824d10f36044db1ce04977ebaa0a049b; 201 source files; observed 2026-09-25T10:15:52.256190+00:00.

### Phase 3 - Independent review and integrated proof

- Status: completed
- Depends on: Phase 2
- Owned scope: complete changed surface, evidence artifacts, and report.
- Excluded from this phase: unapproved installation, commits and publication.
- Work:
  - [x] Independent correctness/instruction, security-grant and release review; route fixes to owning lanes.
  - [x] Run the final ten gates plus new policy/renderer/behavioral checks on a stable tree.
  - [x] Exercise live grant materialization into fresh scratch without installing; record actual capability blockers.
  - [x] Ship eight comparative evaluation scenarios and record any unexecuted live runs explicitly.
  - [x] Verify p.md and index preservation, reconcile docs/state, and report lifecycle states separately.
- Acceptance criteria: observed source gates pass; remaining live validation is clearly separated, with no fabricated results.
- Validation commands: approved gate set in `p.md`, new checker self-tests/check modes, workflow validator, git diff --check.
- Evidence observed: sixteen final gates exited 0; workflow 45 tests passed; renderer retained fixtures passed; nine negative installer paths passed in each shell; 23 agents materialized against six live servers. Independent review APPROVED. Documentation gate passed after explicit user acceptance of the three pre-existing red-sized documents at exact line counts. The evaluation record contains 32 unrun rows, not fabricated quality results. See artifacts/gpt6-agent-migration/verification-summary.md.
- Snapshot: HEAD 164d06a8944a87eb77a8b458c505b7efcb82268d; paths artifacts/gpt6-agent-migration/source-snapshot-manifest.json; SHA256 2e9b5ed0eb60d82ebc35792c9971399d824d10f36044db1ce04977ebaa0a049b; 201 source files; observed 2026-09-25T10:15:52.256190+00:00.

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership: policy_implementation owns prompting-guide and low-noise; agent_pack_implementation owns both orchestrator packs; governance_implementation owns root/pack governance, indexes, install docs and workflow. At most two implementation writers run concurrently; governance prepares read-only until released.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths. No lane or parent stages or commits without explicit user authority.

## Blockers and Next Action

- Blockers: full live comparative matrix is blocked by the observed CLI/account model rejection. Source implementation and local gates can proceed. No installation, upgrade, credential or global configuration change is authorized.
- Next action: local repository implementation is complete. Live calibration and installed-profile activation require an available, explicitly authorized execution surface; no automatic fallback or installation is authorized.

## Final outcome

- IMPLEMENTED: proven on the scoped content snapshot; uncommitted changes remain a recovery risk.
- MERGE_CANDIDATE: repository migration gates and independent review passed; live calibration is explicitly unrun and makes no quality claim.
- RELEASE_CANDIDATE: not requested.
- PUBLISHED: not requested.
- Curation: repository owners contain the durable policy and regression lessons; no additional memory note admitted or written, and no pipeline reopen required.
- Preservation: p.md content hash and original staged empty blob unchanged. Other new index entries appeared without attribution to lane commands; preserved, not reset.
- Documentation exception: user explicitly accepted install-skills.md at 405 lines, skills/sohrab/README.md at 232, and skills/sohrab/README.fa.md at 226 for this revision. The approved-size link/line gate exited 0.
