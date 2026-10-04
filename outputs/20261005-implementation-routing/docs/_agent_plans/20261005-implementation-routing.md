# Workflow Plan - Tune implementation-role selection

- Task ID: `20261005-implementation-routing`
- Mode: implementation
- Profile: resumable
- Status: completed
- Created: 2026-10-05
- Checkpoint: `../agents/20261005-implementation-routing-state.md`
- Base branch and commit: `main`, `1c04f0472ee8b09566073cc54861432f94cfcf93`
- Work branch: `codex/tune-implementation-routing`
- Worktree: current repository checkout
- Execution profile: lean; one bounded write lane, parent correctness review, independent instruction specialist and verifier.

## Summary and Outcome

Tune selection of the default versus difficult implementation role using the work still unresolved when dispatched. Preserve model pins, role identifiers, independent gates, permissions and runtime-specific mechanics. The current default is already correct; repair automatic escalation in failure routing, the missing follow-up reassessment rule, and instruction-authoring wording that overstates complexity.

## High-level Algorithm

The inputs are the current lane outcome, ratified design and acceptance criteria, observed failure evidence, and any continuation's remaining work. Repository contracts establish what is already decided; the parent owns role selection; the prompting guide remains the single owner of model and effort pins.

For an initial assignment, material scope change or fix-cycle follow-up, inspect the decisions still open. Implementing an agreed design remains default work even on concurrency, security, migration or instruction surfaces. A difficult assignment must name a concrete unresolved engineering design decision, the routing criterion it meets, and why that decision changes correctness or failure behavior. Domain labels, file counts, importance, uncertainty, prior tier or failure count alone do not qualify. Missing facts, tools or product intent go to their respective owners; they are not design-complexity evidence.

Record a short role reason in the existing lane/dispatch record. Reassess remaining work at follow-up boundaries; routine implementation after design resolution returns to the default role. Preserve evidence, ownership and gates during a handoff, never leave overlapping writers. Continue the current difficult assignment while its same justified decision remains open; do not switch models midway through one command or force churn for ordinary progress updates. Pipeline-profile escalation and lane-role selection remain separate.

Mirror this behavior in the Claude orchestrator using its existing role names. Keep the legacy difficult Codex identifier and central pins. Agent descriptions must not advertise escalation merely from a sensitive surface; agent bodies consume the recorded scope/routing decision and return missing evidence to the parent without self-upgrading. Routing rules live in the matrices; templates carry their evidence rather than duplicate the algorithm.

The output is a small reviewed source diff, scenario evidence and passing existing validators. No statistical model comparison, speed improvement or serving-model identity is inferred from these checks.

## Scope

- In scope: both orchestrator routing matrices, necessary entrypoint pointers, implementation/fix templates, catalog/role wording, versions/changelogs, generated manifest, and task evidence/archive index.
- Out of scope: central model pins and capabilities; agent renames; grants; unrelated skills; installed agent files; commits, push, publication; entitlement projects; new general test infrastructure.
- Constraints: English source, LF/UTF-8 without BOM, preserve user changes. The inspected source scopes were clean.
- Drift resolved by this request: the failure-routing automatic escalation conflicts with decision-density admission. Resolve through the single implementation-routing owner in both runtimes; do not create a memory duplicate.

## Handoff Package

- Confirmed facts: source and installed default role use Sol/high; difficult Codex role uses Astra/high under a compatibility identifier. Verified against source TOMLs and canonical policy. Versions of both packs are 4.2.0.
- Open assumptions: live model identity and comparative performance remain unknown.
- Ruled out: repinning all implementation to Sol removes justified design escalation; renaming roles needlessly breaks compatibility; a scoring framework or new checker would add machinery beyond this correction.
- Read first on resume: this plan, its checkpoint, the two routing matrices, the scoped Git diff.
- Environment notes: native Python is available. Hindsight recall tools are unavailable in this task; repository truth and prior local policy records ground planning.
- Traps: workflow profile non-de-escalation does not mean a difficult implementation role must own every later fix. A source edit does not prove installed agent activation.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| skill-creator | C:/Users/Alaa-AI/.codex/skills/.system/skill-creator/SKILL.md | instruction change | requested update | stop authoring |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | delegation | role lanes | stop dispatch |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | wording and role selection | all changed instructions | stop authoring |
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | workflow artifacts | plan/state | stop artifact writes |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | bounded reads/returns | all lanes | preserve bounded native output |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | evidence selection | config/prose/native gates | stop uncertain routing |
| alaa-memory-os | skills/sohrab/alaa-memory-os/SKILL.md | recall | prior policy | fail open within its budget |

## Ordered Work

### Phase 1 - Ground and implement

- Status: completed
- Depends on: none
- Owned scope: the paired orchestrator source packages; parent owns this workflow.
- Excluded from this phase: installation, pins, renaming, commits, broad benchmarking.
- Required skills: skill-creator, alaa-prompting-guide, alaa-codex-orchestrator, alaa-low-noise
- Work:
  - [x] Inspect source roles, policy ownership and current routing; obtain specification acceptance. [skills: inherit]
  - [x] Implement the algorithm in both runtimes with one source owner per rule. [skills: inherit]
  - [x] Compress the draft without losing behavior; regenerate only required controlled artifacts. [skills: inherit]
- Acceptance criteria: routine and fully specified sensitive work defaults; difficult work has decision-specific evidence; continuation and failure routing reapply the same admission; no gate or authority drift.
- Validation commands: existing per-pack render/check and contract/grant/pack validators; exact invocation recorded after implementation.
- Evidence observed: settled implementation completed; both contract checks, controlled renderer check and focused whitespace check passed. See ../../focused-checks.md.
- Snapshot: HEAD 1c04f0472ee8b09566073cc54861432f94cfcf93; SHA256 b917fc427790a6a8359aabebc9c5c0efbeef9db8c5e57037de5370103ec8bcaf paths ../../source-manifest.json (scoped 21-path/content manifest); uncommitted, no commit authorized.

### Phase 2 - Validate and reconcile

- Status: completed
- Depends on: Phase 1
- Owned scope: read-only source review, validation receipts and parent workflow closure.
- Excluded from this phase: fixes by reviewers, live installs, benchmark/quality claims.
- Required skills: skill-creator, alaa-prompting-guide, alaa-workflow, alaa-low-noise
- Work:
  - [x] Run independent routing scenarios for routine, sensitive-but-specified, complex, environment-blocked and follow-up cases. [skills: inherit]
  - [x] Obtain independent instruction review and parent correctness review. [skills: inherit]
  - [x] Run existing affected native gates and finalize scope/evidence. [skills: inherit]
- Acceptance criteria: observed scenario choices satisfy the acceptance contract, all required gates pass on the frozen diff, and paired runtime behavior agrees.
- Validation commands: check_agent_contracts.py; check_agent_grants.py; validate_pack.py; Codex render_agents.py --check; central pin validators; skill-creator quick_validate.py; relevant root pack/reference/lifecycle checks; workflow validator; git diff --check.
- Evidence observed: ten independent scenarios assessed; instruction review approved after one minor catalog correction; 12 initial native commands and five affected reruns passed. See ../../report.md.
- Snapshot: HEAD 1c04f0472ee8b09566073cc54861432f94cfcf93; SHA256 b917fc427790a6a8359aabebc9c5c0efbeef9db8c5e57037de5370103ec8bcaf paths ../../source-manifest.json (scoped 21-path/content manifest); uncommitted, no commit authorized.

## Delegation

- routing_spec: read-only specification analyst, configured Sol/medium; completed. Full roster and gate receipts are in ../../report.md.
- routing_impl: default implementer, configured Sol/high, one paired-package write scope. Parent has resolved the algorithm; this is bounded application of it, not an open policy-design assignment.
- instruction review: the fixed instruction-review specialist; its profile is separate from implementation routing.
- verifier: read-only native checks and blind scenario execution using the candidate instructions.
- No caller model overrides. Observed serving identities remain unknown.

## Completion, Rollback and Stop Conditions

Complete after source, scenario evidence, independent review and native gates agree. Preserve uncommitted changes and report that installed custom-agent definitions require separately authorized installation. Restore only task-owned edits from the recorded base if the user requests rollback; never reset unrelated work. Stop on unresolved product choices, widened scope, missing required validation or the orchestrator's bounded repair limit. No installation, commit or publication is implied.

## Blockers and Next Action

- Blockers: none for source implementation.
- Next action: none for source work. Installation and commit require separate authorization.