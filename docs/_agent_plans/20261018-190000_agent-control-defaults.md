# Workflow Plan - Explicit dispatch controls and per-agent Beads ownership

- Task ID: `20261018-190000_agent-control-defaults`
- Mode: `execute`
- Profile: `resumable`
- Task store: `beads`
- Task binding: AGENTS.md#beads
- Task hierarchy: phase-task-subtask
- Review boundary: final
- Final phase: Phase 2
- Commit authority: explicit user grant: completed binding commits and remaining skills and task artifacts on main, including staged-content refresh and whitespace repair. Push and installation remain excluded.
- Status: completed
- Created: `2026-10-18T19:03:26Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20261018-190000_agent-control-defaults-state.md`
- Machine state: not created
- Base branch and commit: main, `4c2a5bd66f18338f128423e2fbaf038a724efb1b`
- Work branch: main
- Worktree: current repository checkout

## Summary and Outcome

- Current repository truth: clean starting tree; neutral role definitions require explicit dispatch controls but provide no omission recovery; Beads defaults to the shared Git username.
- Outcome: both orchestrators explicitly supply supported model and effort on every dispatch, normalize omissions through one mirrored owner, and accept those defaults in role contracts. Workflow owns distinct per-agent Beads identity.
- Strategy: two core implementation lanes, four Luna binding batches, one final integrated verification/review boundary. Binding commits are complete; the authorized follow-up commits remaining skills and task artifacts on main. No installation or push.

## Scope

- In scope: both orchestrators, necessary prompting-guide compatibility, workflow actor ownership, validation, and uniform bindings in the 17 Beads-enabled repositories inventoried below.
- Out of scope: content outside repository Beads binding blocks, installed configuration, vendor, unrelated policies, paid model calibration.
- Constraints and assumptions: preserve supplied controls, capability validation, role authority, cheapest-fit allocation when choices exist, test/review cadence and existing local-plan exception. A missing field takes only its owning default; an unsupported resultant pair still blocks.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): bd where resolves the bound hub; repo:skills open/in_progress search found no matching work. bd 1.3.1 help names --actor, BEADS_ACTOR and Git fallback; claim uses actor; close exposes no atomic assignee guard. Official Codex model/subagent pages read by model_controls confirm gpt-6.1-sol and medium.
- Open assumptions (believed but unverified, each with what would verify it): installed activation and actual serving identity are outside source proof.
- Ruled out (approach, reason, evidence): role pins and capability-registry defaults would duplicate task allocation ownership; weakening the post-normalization control validator would allow incomplete dispatches.
- Read first on resume (ordered exact paths): this plan; linked checkpoint; skills/sohrab/alaa-workflow/references/task-tracking.md; each orchestrator references/model-effort-policy.md.
- Environment notes (command shapes that work here, and ones that look right but fail): run bd commands separately without environment overrides; use explicit --actor for mutations. Shared-hub writes need scoped escalation. Use python -B to avoid new caches.
- Traps (looks correct, is not): Git username identifies the user rather than each concurrent agent. Configured controls do not prove serving identity. A source default is not installed activation.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | Tracking and continuity | always | Stop dependent work |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | Every instruction edit and allocation | always | Stop dependent work |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | Dispatch and final gates | always | Stop dependent work |
| alaa-cc-orchestrator | skills/sohrab/alaa-cc-orchestrator/SKILL.md | Mirrored model changes | model lane | Stop model lane |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | Broad reads and lane returns | always | Bound output manually |
| beads | .agents/skills/beads/SKILL.md | Beads work | always | Stop tracking-dependent work |

## Ordered Work

### Phase 1 - Repair and verify agent controls

- Status: completed
- Phase issue: alaa-ugv
- Depends on: none
- Reasoning and selection reason: bounded cross-runtime instruction changes with two independent domain owners; one final acceptance boundary avoids redundant review.
- Settled/open decisions and invariants: mirrored model-effort-policy files own omission defaults; task-tracking owns actor rule. Preserve explicit fields and reject unsupported controls. Default values never become role pins. No AGENTS.md edits.
- Risk and required observers: incomplete dispatch and mistaken ownership; final independent verifier and instruction reviewer inspect combined candidate and negative scenarios.
- Owned scope: the four named skills and artifacts/agent-control-defaults-20261018.
- Excluded from this phase: installations, commits, pushes, unrelated configuration and vendor.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-low-noise, beads
- Work:
  - Task issue: alaa-ugv.1 [skills: inherit]
    - Subtask issue: alaa-ugv.1.1 [skills: inherit]
  - Task issue: alaa-ugv.2 [skills: inherit]
    - Subtask issue: alaa-ugv.2.1 [skills: inherit]
- Acceptance criteria: both original defects corrected in their single owners, mirrored runtime behavior preserved; official Codex mapping verified or visibly marked unresolved if verification fails; no omitted controls at execution; each actor distinct and stable with truthful ownership checks; exact binding proposal delivered; every applicable named checker exits 0; final independent review resolved.
- Validation commands: each changed skill's check_agent_contracts.py, check_agent_grants.py, validate_pack.py, check_claude_model_policy.py, check_codex_model_policy.py and validate_workflow_files.py as applicable; add --self-test only for changed checkers; root skill/citation gates and git diff --check.
- Evidence observed: focused implementation/checker evidence in artifacts/agent-control-defaults-20261018/model-report.md and actor-report.md; combined final proof: artifacts/agent-control-defaults-20261018/verification.md.
- Review status: REVIEW_PENDING
- Review evidence: Phase 2 owns final independent acceptance of the combined candidate; no separate Phase 1 review.
- Snapshot: HEAD 56e5c80c3b9895949226bfddc52f77050d66337c; SHA256 ffd345672ed4df903b3fa8e1378cd3c841ee305e7f53e791aa3f1661f26cf68c; paths artifacts/agent-control-defaults-20261018/verification-source-sha256.json (90 source files, sorted relative path + NUL + raw bytes + NUL).

### Phase 2 - Uniform bindings and final acceptance

- Status: completed
- Phase issue: alaa-sd7
- Depends on: none
- Reasoning and selection reason: exact common-block replacement across finite independent repositories; all template decisions settled in the workflow owner before dispatch.
- Settled/open decisions and invariants: use artifacts/agent-control-defaults-20261018/binding-template.md verbatim except __PROJECT__; shared hub remains unchanged. The hub repository replaces its generic generated Beads block and adopts the same project-scoped binding. Preserve runtime imports and all surrounding bytes.
- Risk and required observers: accidental unrelated commit or ownership drift; independent final instruction review and verifier compare every block, outside-block bytes and final commit paths. Review is final-only across both phases.
- Owned scope: binding blocks in skills, alaa-task-hub, octane-base, ci-image, wa, tusd, gateway, alaa-go-chi, authz-sidecar, entitlement-projector, authz-openfga, auth, deploy, client, content, entitlement-api, comment-service.
- Excluded from this phase: application edits, skill commits, installs, push, history rewrite and unrelated staged files.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-low-noise, beads
- Work:
  - Task issue: alaa-sd7.1 [skills: inherit]
    - Subtask issue: alaa-sd7.1.1 [skills: inherit]
  - Task issue: alaa-sd7.2 [skills: inherit]
    - Subtask issue: alaa-sd7.2.1 [skills: inherit]
  - Task issue: alaa-sd7.3 [skills: inherit]
    - Subtask issue: alaa-sd7.3.1 [skills: inherit]
  - Task issue: alaa-sd7.4 [skills: inherit]
    - Subtask issue: alaa-sd7.4.1 [skills: inherit]
- Acceptance criteria: every physical binding copy in all 17 repositories equals the common template after label substitution; preserve imports and symlinks and record physical/logical counts in the receipts. Only binding blocks changed; final combined gates pass; one binding-only Conventional Commit per repository on its original branch, with SHA and preserved unrelated state recorded.
- Validation commands: native per-repository diff checks; exact template and surrounding-byte comparisons; Phase 1 integrated checkers; post-commit git show path/diff/parent validation.
- Evidence observed: inventory inspected 66 immediate project directories; 16 standard-bound projects plus shared hub. Luna batch receipts and combined verification passed; binding-commit-manifest.json is the reviewed commit input.
- Review status: APPROVED
- Review evidence: artifacts/agent-control-defaults-20261018/review.md; both independent final reviews APPROVED after targeted repairs; verification.md records passing gates.
- Snapshot: HEAD 56e5c80c3b9895949226bfddc52f77050d66337c; SHA256 657b7c5b73dd6edd5eddfb148b1aa95ebe1d0e1478605cd40d16474dca2ba8c8; paths artifacts/agent-control-defaults-20261018/binding-commit-manifest.json (25 files, sorted project/relative path + NUL + bytes + NUL); all 17 committed identities in commits.md.

## Task Allocation

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Two source investigations | alaa-researcher | balanced, official and CLI reconciliation | gpt-6.1-sol | medium | Current source reconciliation; cross-runtime choices exceed mechanical fit; 2026-10-18 official model and subagent pages | explicit model and reasoning_effort, fork_turns=none | Available host schema; serving identity unknown |
| Mirrored model contracts and prompting compatibility | alaa-implementer | balanced, coupled controls and projection ownership | gpt-6.1-sol | medium | Local behavioral change needs coordinated contract judgment; cheaper mechanical branch fails settled exact-transformation fit | explicit model and reasoning_effort, fork_turns=none | Available; no loaded role pins observed in dispatch contract |
| Workflow actor ownership | alaa-implementer | balanced, claim/update/resume consistency | gpt-6.1-sol | medium | Cross-agent ownership semantics need reconciliation, beyond mechanical exact transformation | explicit model and reasoning_effort, fork_turns=none | Available; serving identity unknown |
| Final native verification | alaa-verifier | balanced, bounded command execution | gpt-6-luna | medium | Finite exact commands and output contract; no unresolved design | explicit model and reasoning_effort, fork_turns=none | Available in host; source evidence only |
| Final combined instruction judgment | alaa-instruction-reviewer | balanced, owner/default/identity interactions | gpt-6.1-sol | medium | Independent authority and coupled contracts, no frontier need | explicit model and reasoning_effort, fork_turns=none | Available; no installation proof |
| Final Python checker correctness | alaa-reviewer | balanced, two bounded checker diffs and negative fixtures | gpt-6.1-sol | medium | Independent correctness gate for executable changes; distinct from instruction semantics | explicit model and reasoning_effort, fork_turns=none | Available; source proof only |
| Four binding batches, exact block replacement | alaa-implementer-luna | explicit user Luna request; mechanical finite scopes | gpt-6-luna | medium | Settled template, 17 named repositories, no semantic discretion, exact parity and outside-block oracle | explicit model and reasoning_effort, fork_turns=none | Available host, four slots; stop overlapping changes |

## Delegation

- Model lane owns both orchestrators and necessary prompting-guide edits. Actor lane owns workflow and the binding proposal. Parent owns this plan/checkpoint and integrated evidence. Luna batch A owns skills/hub/octane-base/ci-image/wa; B owns tusd/gateway/alaa-go-chi/authz-sidecar; C owns entitlement-projector/authz-openfga/auth/deploy; D owns client/content/entitlement-api/comment-service.
- Both lanes draft then compress; every agent preserves other work. Actor dispatch fields are integrated by the model lane after the workflow owner names their contract.
- Beads owns task state and dependencies. Phase/task nodes belong to the lead; leaf assignees belong to their implementing agents. Leaf claims precede writes.
- No blocking edge joins independent leaves. Phase 2 consumes the ratified available actor/template contract, not unfinished model work; both phases share final acceptance. Shared artifact writes are disjoint; final validation freezes all product scopes.
- One integrated checker run covers unchanged combined inputs. A changed checker receives its self-test; changed inputs invalidate only affected evidence.
- The integration parent makes authorized binding-only commits after the final boundary. Luna workers prepare and verify their disjoint batches, then close their own leaves from the verified commit receipts; no worker commit authority is inferred.
- Review occurs only at the final boundary, after both lanes finish. Fixes return to the owning lane and require affected retests; never weaken checks.
- Curation at final acceptance records only task-relevant source lessons in this handoff. No memory publication is authorized.

## Execution Position

- Position owner: `docs/agents/20261018-190000_agent-control-defaults-state.md` (position, blockers and next action).

## Authorized follow-up

The user authorized identical Beads bindings in every Beads-enabled project under the project parent directory, with binding-only commits on each current branch and many Luna subagents, then reaffirmed identical bindings. This supersedes the earlier AGENTS/commit prohibition only for those blocks. That initial grant excluded skill commits, installation and push; the later grant below authorizes the remaining source and artifact commit only. The shared hub has generic upstream setup rather than a marked Alaa block; replacing that block makes its repository-specific work follow the same contract without changing database routing.

## Final gate and curation

Both independent reviews returned APPROVED after two scoped repairs. All required native gates passed on the frozen source candidate; aggregate child coverage and initial failures remain explicit in verification.md. Binding audit proves exact common blocks and outside-byte preservation for 25 physical files, seven preserved symlinks and two Git-clean imports across 17 repositories. The skills import has pre-existing CRLF while its Git blob has LF; canonical clean hashes match, and its working copy is preserved. The parent completed all 17 user-authorized binding-only commits; commits.md records verified SHAs, branches, paths and preserved state. At the binding-only boundary, 90 core source files remained uncommitted and matched the independently verified manifest. The follow-up below includes them in the source commit.

Curation: the model and ownership lessons are already encoded in their source owners; no additional reusable-memory candidate is admitted and no memory publication is authorized. Remaining evidence is task-local.

## Source and artifact commit follow-up

The user authorized committing all remaining skills and task artifacts on the current branch after refreshing staged versions and repairing whitespace. This supersedes the earlier source-commit exclusion; implementation scope and final-only review cadence are unchanged. The 90 source files match the reviewed manifest. Only artifact portability, text formatting and completion records changed during commit preparation. Reuse unchanged source evidence; check the refreshed index, source hashes and workflow metadata before committing.
