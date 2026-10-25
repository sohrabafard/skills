# Workflow Plan - Test execution ownership

- Plan kind: execution
- Approved design: `docs/_agent_plans/20261025-test-execution-ownership-design.md`
- Task ID: `test-execution-ownership`
- Mode: delegated
- Profile: resumable
- Task store: beads
- Task binding: AGENTS.md#beads
- Task hierarchy: phase-task-subtask
- Review boundary: final
- Final phase: Phase 1
- Commit authority: not granted
- Status: complete
- Created: `2026-10-25`
- Parent plan: not created
- Prompt pack: none
- Checkpoint: `docs/agents/20261025-test-execution-ownership-state.md`
- Machine state: none
- Base branch and commit: main, 183f5c5a19daaa0c31c5aa41ce8ce2868181aa34
- Work branch: main
- Worktree: current checkout; no new worktree

## Summary and Outcome

Implement the approved design. The initial tree contains only user-owned staged/unstaged `docs/design/separate.md`; preserve both states. Shared policy lives in testing-strategy, runtime coordination stays mirrored, workspace recovery lives in workflow.

## Scope

- In scope: approved design's policy migration, resources/timing, runners, consumers, workflow and proof.
- Out of scope: non-test recommendations, installation, commit, publication, user plan edits.
- Constraints: no new skill; no automatic worktree; one writer per file/shared resource; English authored artifacts; no deletion.
- Approved scope addition (2026-10-26): minimally repair existing repository-tooling-capability-check structure, OpenAI metadata and both index entries to clear preexisting mandatory-gate failures; preserve its logic and existing document languages.
- Necessary integration repair: update the single Laravel-upgrade runtime-owner pointer broken by concurrent completed issue alaa-3g4w; preserve all upgrade logic and shell examples. The full requested fleet gate exposed the stale reference.

## Handoff Package

- Confirmed facts: Source references, runner equivalence and checker coupling inspected; `bd where` matches the repository binding; the exposed role definitions are model-neutral.
- Open assumptions: Live agent compliance remains unproven. Current validation runs in WSL; Windows runner compatibility receives source/contract review. Native Windows probes were the lead's inference from cross-platform runner compatibility, not a user requirement. The user asked for that decision's source, not a blanket platform prohibition. No further native Windows attempt is planned after the bounded environment retry.
- Ruled out: Copying policy into role definitions; weakening gates to accept missing rules; automatic worktrees or task-store replacement.
- Read first on resume: this plan; its approved design; `docs/agents/20261025-test-execution-ownership-state.md`; bound Beads issues.
- Environment notes: WSL Bash; prefix-authorized Beads escalation is needed outside the working tree; no Hindsight tools exposed, so prior-memory recall was unavailable and current repository sources were used.
- Traps: Do not change `docs/design/separate.md`; renderer-owned wrappers and manifests are regenerated only after source edits settle. Policy transfers use the recorded HEAD source, because concurrent consumer rewrites can replace the live source with a pointer before transfer finishes.
- Concurrent work: foreign issue alaa-3g4w completed runtime-ops WSL changes and its index entries. Preserve that skill, its retired Windows reference and artifacts/runtime-ops-wsl. Our resource pointer respects its declared runtime scope; final root-gate input fingerprints include the foreign changes without claiming their authorship/review.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | dispatch and phase gates | always | block delegation |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | policy and validation design | always | block dependent work |
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | state and ownership changes | always | block dependent work |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | instruction edits | always | block dependent work |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | retrieval and returns | always | report gap |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | evidence selection | always | block dependent source claims |
| beads | .agents/skills/beads/SKILL.md | issue operations | always | block tracking-dependent work |
| alaa-bash-shell | skills/sohrab/alaa-bash-shell/SKILL.md | shell runner changes | shell lane | block shell work |
| alaa-repo-docs | skills/sohrab/alaa-repo-docs/SKILL.md | final report and navigation | documentation lane | block documentation completion |

## Ordered Work

### Phase 1 - Transfer, validate and review

- Status: complete
- Phase issue: alaa-xw5h
- Depends on: none
- Reasoning and selection reason: Settled ownership migration with interacting instruction, compatibility and checker changes; one integration/review barrier.
- Settled/open decisions and invariants: Approved design; no unresolved product decision. Preserve the four pre-existing doctrines and runtime-specific mechanics.
- Risk and required observers: Independent verifier, correctness reviewer and instruction reviewer; release review for moved runner packaging. Test strategy checks the discriminating negative scenarios before implementation.
- Owned scope: testing-strategy, both orchestrators, workflow and this artifact family.
- Excluded from this phase: user-owned design input, vendor, installed copies and non-test extractions.
- Required skills: alaa-codex-orchestrator, alaa-testing-strategy, alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing, beads
- Work:
  - Task issue: alaa-xw5h.1 [skills: inherit]
    - Subtask issue: alaa-xw5h.1.1 [skills: alaa-testing-strategy, alaa-prompting-guide, alaa-bash-shell, alaa-low-noise, beads]
    - Subtask issue: alaa-xw5h.1.2 [skills: inherit]
    - Subtask issue: alaa-xw5h.1.3 [skills: inherit]
    - Subtask issue: alaa-xw5h.1.4 [skills: alaa-prompting-guide, alaa-low-noise, beads]
    - Subtask issue: alaa-xw5h.1.5 [skills: alaa-prompting-guide, alaa-low-noise, beads]
  - Task issue: alaa-xw5h.2 [skills: inherit]
    - Subtask issue: alaa-xw5h.2.1 [skills: inherit]
    - Subtask issue: alaa-xw5h.2.2 [skills: alaa-repo-docs, alaa-low-noise, beads]
- Acceptance criteria: Approved design Acceptance Criteria plus all negative scenarios from the user's plan; independent judgments of actual artifacts.
- Validation commands: root scripts validate_sohrab_skill_pack.py, check_skill_index.py, check_fleet_references.py, check_lifecycle_contract.py; both orchestrator scripts/validate_pack.py; changed contract checkers with --self-test; shared execution checker and runner probes; renderer --check and grants as covered by aggregates; workflow artifact validator.
- Collection/repair/retest barrier and evidence owner: Independent verifier collects the frozen candidate's command list once; one combined scoped repair then required list retest; evidence under artifacts/test-execution-ownership and this phase.
- Evidence observed: All 19 recorded commands passed, including the six required gates: artifacts/test-execution-ownership/verification-4/report.md. Documentation links/grades and unchanged-source proof passed: artifacts/test-execution-ownership/docs/evidence.md. Earlier findings and their repair evidence remain archived in this task directory.
- Review status: APPROVED
- Review evidence: artifacts/test-execution-ownership/correctness-approval.md and instruction-review.md; packaging source findings cleared in release-review.md, with its final-gate condition met by verification-4. Installation and live Windows/agent behavior remain outside proven local acceptance.
- Snapshot: HEAD 183f5c5a19daaa0c31c5aa41ce8ce2868181aa34; owned-path snapshot 284 files SHA-256 9f25664ba53311cd8fe16a7a8b608835ca5ff07316881edb24bb23963d5dea86; broader tested inputs 2260 files SHA-256 847f3c801966d478b1b7c71339f5a701daa48959d42f7145ddd0446423f187c8. Manifests/method: artifacts/test-execution-ownership/verification-4/.
- Final curation: no admitted candidates. The full engagement's platform-scope, rule-ownership, evidence-validity and guard-preservation decisions are recoverable from their updated canonical owners and tests. A second memory explanation would duplicate those owners; one-off retries remain task evidence. No memory publication or further repository promotion is required.
- Final report and proposal-only follow-ups: artifacts/test-execution-ownership/report.md. No commit, installation, publication or remote synchronization was requested or performed.
- Completion-artifact validation and source-reuse proof: artifacts/test-execution-ownership/finalization/report.md. During finalization HEAD advanced externally to 17d0572b77ee97167be7e454759ee065d670b358: its 14 changed paths match the previously identified alaa-3g4w runtime-ops scope, and shared-index changes affect only that skill's entries. All 284/2260 tested file contents stayed identical; this task's source changes and the protected user document remain uncommitted. No commit was performed by this task.

## Task Allocation

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Canonical policy and runner migration; interacting semantic exceptions | alaa-implementer-high | balanced | gpt-6.1-sol | high | Prompting-guide 90-model-selection coordinated files row, 2026-10-09; Luna bounded-exact fit fails because multiple execution/authority exceptions must be reconciled | explicit model/effort, fork none | neutral installed role; observed identity unknown |
| Mirrored consumers/workflow; coupled loading and role authority | alaa-implementer-high | balanced | gpt-6.1-sol | high | Same coordinated-files row; mechanical decomposition loses policy/authority boundaries | explicit model/effort, fork none | neutral installed role; observed identity unknown |
| Contract gates and negative fixtures; changed cross-file ownership | alaa-implementer-high | balanced | gpt-6.1-sol | high | Same coordinated-files row; checker semantics and false-green paths require coupled judgment | explicit model/effort, fork none | neutral installed role; observed identity unknown |
| Test matrix / independent instruction and correctness review | applicable read-only role | balanced | gpt-6.1-sol | medium | Research decisions/fact verification row; cross-owner contradictory text requires judgment beyond bounded retrieval | explicit model/effort, fork none | neutral available roles; no live behavior claim |
| Exact command verification / documentation / release inspection | applicable role | balanced | gpt-6.1-sol | medium | Owner-normalized default; command/evidence reconciliation with cross-gate state | explicit model/effort, fork none | runtime identity/enforcement unobservable remains unknown |
| Existing tooling-skill packaging and exact stale-pointer repair; named files, fixed content and cheap structural oracle | alaa-implementer-low | balanced | gpt-6.1-sol | low | Bounded semantic lane: existing exclusion sentence, standard metadata/index form, exact owner-router substitution; no policy redesign | explicit model/effort, fork none | observed identity unknown |

Allocation uses current exposed tool support and neutral installed roles; official model-selection and subagent pages refreshed on 2026-10-25. No cost or quality improvement claim or calibration experiment.

## Delegation

- Lead actor: codex:01a1747c:lead. The lead owns plan/checkpoints and integration evidence only.
- Owner lane: testing-strategy except new checker; both orchestrators' two legacy runner scripts. Actor codex:01a1747c:owner.
- Consumer lane: both orchestrators' Markdown/TOML/YAML source contracts and workflow Markdown/templates; no Python, runners or generated outputs. Actor codex:01a1747c:consumers.
- Checker lane: both orchestrators' Python validation code; testing-strategy execution checker/runner tests; workflow Python only for required generated-loading seams. Actor codex:01a1747c:checks.
- Disjoint writes and shared-resource conflicts: named file ownership; renderer deferred until source lanes stop; no shared test-runtime mutation.
- Integration barriers: owner/consumer lanes use fixed new reference names from the design; checkers consume their finished content before final proof. All writers stop before integrated verification.
- Consolidated checks: six requested gates; aggregate children cited only with proven identical coverage; self-tests only for changed checkers. No heavy concurrency.
- Reusable evidence: scoped files, versions, environment and flags/cwd plus observer must match.
- Phase collection, repair/retest and review barriers: whole candidate after implementation; final-only independent review; source artifacts are not live-agent evidence.
- Return: changed paths, focused evidence, unresolved findings and next step, at most 20 lines; no transcripts.

## Current Position

- Position owner: `docs/agents/20261025-test-execution-ownership-state.md`
The checkpoint owns blockers and next action; this plan does not duplicate its cursor.
