# Workflow Plan - Goal and workflow skill repair

- Task ID: `20261004-000000_goal-and-workflow-skill-repair`
- Mode: execute
- Profile: resumable
- Status: complete
- Created: `2026-10-04T15:35:36Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `../agents/20261004-000000_goal-and-workflow-skill-repair-state.md`
- Machine state: not created
- Base branch and commit: main 360a78c584d4c606c205797f8feebed4c14d6314
- Work branch: main (current checkout; disjoint ownership, no integration requested)
- Worktree: repository root

## Summary and Outcome

- Initial repository truth: goal composition permitted operating instructions inside goal text; workflow template/checker omitted skill mappings; advisory and low-noise rules could suppress durable planning.
- Outcome: short source-verified goals and automatic durable phased execution plans with explicit skills per task.
- Strategy: preserve one owner per rule; repair prompting and workflow first, then align both orchestrators and low-noise. Standard execution profile; independent verification and instruction review.
- Rejected alternatives: longer universal goal manuals (repeat skill contracts); hard-coded unverified runtime limits (stale); blanket artifacts for all advice (exceeds intent); whole model-policy refresh (unrelated).

## Scope

- In scope: the five user-named skill directories, their existing templates/checkers/tests, and this evidence family.
- Out of scope: vendor, installed skills/agents, global config, model pins, commit, merge, publication, installation and live paid model benchmarks.
- Constraints and assumptions: an actionable execution-plan request authorizes plan/checkpoint artifacts, not product execution. Explicit no-file/read-only/chat-only and native Plan Mode restrictions prevail. Reusable phase prompt packs remain opt-in.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): initial scoped worktree clean; base from git rev-parse. Spec lane confirmed missing phase/task skill fields and conflicting artifact admission.
- Open assumptions (believed but unverified, each with what would verify it): user confirmed Desktop Code tab and supplied a composer rejection for embedded mentions, commands, links and formatting; full prompt/version and live reproduction remain unavailable; live Desktop acceptance not tested. Installed role restrictions are known; enforcement/serving identity unknown. Hindsight tools unavailable; repository and local memory supplied context.
- Ruled out (approach, reason, evidence): no model-policy migration; requested defects concern composition and workflow contract. No branch required under current workspace owner for disjoint local writes.
- Read first on resume (ordered exact paths): this plan; its checkpoint; skills/sohrab/AGENTS.md; changed canonical owner references.
- Environment notes (command shapes that work here, and ones that look right but fail): PowerShell 7; python -B prevents pycache. Create output directory before selecting it as command cwd. Scoped git status succeeds; full status reports inaccessible historical _to_delete directories.
- Traps (looks correct, is not): source/static checks do not prove Desktop parser acceptance or model behavior; native Plan Mode is not ordinary planning prose.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-prompting-guide | ../../../../skills/sohrab/alaa-prompting-guide/SKILL.md | writing agent instructions or choosing runtime syntax | always | Stop the dependent decision and report the missing owner. |
| alaa-memory-os | ../../../../skills/sohrab/alaa-memory-os/SKILL.md | planning from prior context | prior-context or long-run trigger holds | Stop the dependent decision and report the missing owner. |
| alaa-code-intelligence-routing | ../../../../skills/sohrab/alaa-code-intelligence-routing/SKILL.md | selecting repository evidence owner | non-trivial evidence retrieval | Stop the dependent decision and report the missing owner. |
| alaa-workflow | ../../../../skills/sohrab/alaa-workflow/SKILL.md | planning, checkpointing and phase transition | always | Stop the dependent decision and report the missing owner. |
| alaa-low-noise | ../../../../skills/sohrab/alaa-low-noise/SKILL.md | retrieval and delegated return shaping | long or delegated work | Stop the dependent decision and report the missing owner. |
| alaa-codex-orchestrator | ../../../../skills/sohrab/alaa-codex-orchestrator/SKILL.md | Codex lane dispatch and independent gates | Codex orchestration | Stop the dependent decision and report the missing owner. |
| alaa-cc-orchestrator | ../../../../skills/sohrab/alaa-cc-orchestrator/SKILL.md | auditing Claude mirrored consumer contract | Claude consumer alignment | Stop the dependent decision and report the missing owner. |
| alaa-testing-strategy | ../../../../skills/sohrab/alaa-testing-strategy/SKILL.md | choosing failure cases and proof strength | checker or behavior validation | Stop the dependent decision and report the missing owner. |
| alaa-codex-runtime-ops | ../../../../skills/sohrab/alaa-codex-runtime-ops/SKILL.md | diagnosing host validation failures | Windows shell or sandbox failure | Stop the dependent decision and report the missing owner. |
| alaa-repo-docs | ../../../../skills/sohrab/alaa-repo-docs/SKILL.md | grading task evidence and checking links | documentation gate | Stop the dependent decision and report the missing owner. |
| alaa-extract-agent-lessons | ../../../../skills/sohrab/alaa-extract-agent-lessons/SKILL.md | final context curation | completion boundary | Stop the dependent decision and report the missing owner. |

## Ordered Work

### Phase 1 - Ground the acceptance contract

- Status: complete
- Depends on: none
- Owned scope: Read-only source and official runtime research
- Excluded from this phase: All product writes
- Required skills: alaa-prompting-guide, alaa-memory-os, alaa-code-intelligence-routing
- Work:
  - [x] P1.1 Inspect source ownership and obtain acceptance criteria [skills: inherit]
- Acceptance criteria: checkable user outcomes, preserved authority and canonical ownership; explicit skill mappings and resumable evidence.
- Validation commands: Official sources, source inspection, acceptance lane
- Evidence observed: Source gaps confirmed by acceptance lane; goal_research verified official sources on 2026-10-04
- Snapshot: none; no files changed

### Phase 2 - Repair canonical owners

- Status: complete
- Depends on: Phase 1
- Owned scope: alaa-workflow and alaa-prompting-guide
- Excluded from this phase: Model policy, installed copies, unrelated skills
- Required skills: alaa-prompting-guide, alaa-workflow, alaa-low-noise
- Work:
  - [x] P2.1 Repair runtime goal composition and durable plan skill routing [skills: inherit]
- Acceptance criteria: checkable user outcomes, preserved authority and canonical ownership; explicit skill mappings and resumable evidence.
- Validation commands: Focused goal contract fixtures and workflow unit tests
- Evidence observed: 74 workflow tests and 16 goal text fixtures plus boundary/exit checks passed. Independent correctness and instruction reviews approved after fixing all reported bypasses and false positives. Commands and timestamps: ../../final-verification.json.
- Snapshot: HEAD 360a78c584d4c606c205797f8feebed4c14d6314; ../../final-source-snapshot.json SHA256 E663B5915FE10D2934C43EB7BC81BC225B59B8E94FC141895903B6B4A68A7C3D; paths skills/sohrab/alaa-workflow, skills/sohrab/alaa-prompting-guide; uncommitted, preserve working tree.

### Phase 3 - Align consumers

- Status: complete
- Depends on: Phase 2
- Owned scope: Both orchestrators and alaa-low-noise
- Excluded from this phase: Canonical workflow machinery and runtime model policy
- Required skills: alaa-prompting-guide, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-low-noise
- Work:
  - [x] P3.1 Align admission, phase/task skills and compressed output without duplicating owners [skills: inherit]
- Acceptance criteria: checkable user outcomes, preserved authority and canonical ownership; explicit skill mappings and resumable evidence.
- Validation commands: Both agent contract checks and parity review
- Evidence observed: both packs and both 31-case contract self-tests passed; mirrored consumer parity and scope checks passed. Independent instruction/correctness reviews approved. Exact affected-tier results: ../../final-verification.json.
- Snapshot: HEAD 360a78c584d4c606c205797f8feebed4c14d6314; ../../final-source-snapshot.json SHA256 E663B5915FE10D2934C43EB7BC81BC225B59B8E94FC141895903B6B4A68A7C3D; paths skills/sohrab/alaa-cc-orchestrator, skills/sohrab/alaa-codex-orchestrator, skills/sohrab/alaa-low-noise; uncommitted, preserve working tree.

### Phase 4 - Verify and review

- Status: complete
- Depends on: Phase 3
- Owned scope: Frozen five-skill candidate and task artifacts
- Excluded from this phase: Install, commit, publish, deployment
- Required skills: alaa-prompting-guide, alaa-workflow, alaa-testing-strategy, alaa-codex-runtime-ops, alaa-repo-docs, alaa-extract-agent-lessons
- Work:
  - [x] P4.1 Run integrated gates and independent instruction/correctness review; record limits [skills: inherit]
- Acceptance criteria: checkable user outcomes, preserved authority and canonical ownership; explicit skill mappings and resumable evidence.
- Validation commands: Native pack, reference, lifecycle, instruction, workflow and goal checks
- Evidence observed: final source gates all passed; 535 source/tool inputs unchanged during verification. Both independent reviews APPROVED, all findings closed. Links in 26 Markdown files passed; narrative documents GREEN (30 and 36 lines); scoped diff check passed. Exact documentation results: ../../documentation-validation.json. Curation: no separate candidates; fixes reside in canonical owners; no memory write.
- Snapshot: HEAD 360a78c584d4c606c205797f8feebed4c14d6314; ../../final-source-snapshot.json SHA256 E663B5915FE10D2934C43EB7BC81BC225B59B8E94FC141895903B6B4A68A7C3D; paths skills/sohrab/alaa-workflow, skills/sohrab/alaa-prompting-guide, skills/sohrab/alaa-cc-orchestrator, skills/sohrab/alaa-codex-orchestrator, skills/sohrab/alaa-low-noise, scripts; uncommitted, preserve working tree.

## Delegation

- Parent owns plan, integration and reporting. At most two concurrent writers, disjoint skill scopes.
- Evidence: acceptance (spec analyst), goal_research (researcher).
- Implementation: workflow owner; prompting owner; consumer alignment serialized after owner contracts.
- Gates: independent verifier, instruction reviewer and correctness reviewer; source checks are not live model evaluations.

## Blockers and Next Action

- Blockers: no local implementation blocker; live Desktop acceptance remains unverified.
- Next action: local repair complete. Installed deployment, live Desktop testing, commit and publication remain outside this request.
