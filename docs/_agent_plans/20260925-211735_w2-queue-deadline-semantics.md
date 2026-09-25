# Workflow Plan - W2 queue deadline and durable acceptance semantics

- Task ID: `20260925-211735_w2-queue-deadline-semantics`
- Mode: `execute`
- Profile: `resumable`
- Status: completed
- Created: `2026-09-25T21:17:35Z`
- Parent plan: not created
- Prompt pack: `docs/_agent_plans/20260925-211735_w2-queue-deadline-semantics__phase-prompts.md`
- Checkpoint: `docs/agents/20260925-211735_w2-queue-deadline-semantics-state.md`
- Machine state: not created
- Base branch and commit: main, ba278f4ed6962e7f20251e55784129c550aa1b85
- Work branch: `main`; retain the current checkout under the workspace owner because scope ownership is clear and integration is not requested. No branch or commit created.
- Worktree: repository root, no isolated checkout.

## Summary and Outcome

The user explicitly approved W2 after its purpose was explained: clarify skill guidance, not change actual services or queues. Traceability: audit F03 in artifacts/skill-modernization-audit-20260925/audit.md. The user submitted the execution prompt in the current chat, authorizing the scoped local implementation and independent gates below; no repeat audit or approval is required.

Current source inspection confirms a contradiction: reliability SKILL.md applies expiry/drop bounds to every queue and derives wait from the originator deadline, while references/40-admission-and-shedding.md allows work to be persisted, receipted and completed asynchronously. references/10-deadlines-and-timeouts.md also uses broad cancellation wording. The correction must scope these statements consistently, rather than patching one sentence and leaving contradictory examples.

## Scope and selection

Approved: alaa-reliability-sla body and directly affected references; read-only consistency review of alaa-async-messaging and alaa-services-contract. Conditional write permission to those two dependencies covers only demonstrated W2 contradictions and necessary owner pointers; record file/line evidence before a write. Shared contract edits must be serialized through the same lane.

Explicitly deferred: service-runtime-kit-governance, alaa-permission-generator; all other audit findings, including router cleanup, version refresh and model changes. The normalization/Arvan task is separate; do not infer its outcome or reopen it.

No application/kit/consumer code, broker settings, cluster access, public envelope/header changes, numeric defaults, TTL/retention values, new event names, new metrics, migrations, vendor, installed copies, global configuration, root instructions/indexes or agent policy changes. If a new product contract or consumer migration is required, stop that affected decision and ask; conditional dependency edits do not authorize it.

Lead-only writes: this workflow family and artifacts/w2-queue-deadline-semantics/ for evidence. No memory publication selected. No commit, merge, push, tag, installation, deployment, publication, destructive cleanup or benchmark authority. Preserve dirty files; never reset, stash or stage another task's changes.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): planning intake tracked status was clean on main at the recorded HEAD. Targeted native reads confirmed the blanket queue/caller-deadline wording and durable-acceptance exception. Async messaging already owns outbox, publisher confirms, acknowledgement after business effect/receipt transaction, replay and DLQ mechanics; services-contract owns concrete names and values.
- Open assumptions (believed but unverified, each with what would verify it): no consumer runtime or failing production queue was inspected. No business expiry or cancellation policy is selected. Role availability is observed; effective MCP restriction and runtime model identity are unknown. Source facts were checked at the unchanged planning HEAD.
- Ruled out (approach, reason, evidence): carrying the expired HTTP deadline unchanged into accepted async work recreates the bug; removing all bounds creates unbounded work; inventing a universal TTL/retention period exceeds scope; treating a timeout as proof no effect happened breaks idempotency; assuming the client received the receipt confuses transport with durable ownership.
- Read first on resume (ordered exact paths): this plan and checkpoint; applicable AGENTS.md; skills/sohrab/alaa-reliability-sla/SKILL.md and its full references; skills/sohrab/alaa-async-messaging/SKILL.md; skills/sohrab/alaa-services-contract/references/22-failure-load-and-deprecation-contract.md, then only their triggered references. Read complete skill contracts before editing them under repository rules.
- Environment notes (command shapes that work here, and ones that look right but fail): use PowerShell BelowNormal and python -B from repository root; no heavy benchmark or live service is needed for this instruction correction. Official RabbitMQ TTL documentation distinguishes message expiry mechanics from application policy; do not infer business obligations from broker defaults.
- Traps (looks correct, is not): application acceptance receipt is not consumer acknowledgement or publisher confirm. A processing-attempt timeout is not whole-job invalidation. An expired business validity deadline is not an instruction to silently delete accepted work. Cancellation can be cooperative/ambiguous; do not promise rollback or exactly-once from prose.

## Acceptance criteria and preserved capability

1. Waiting synchronous work retains inherited deadline, bounded resources, prompt cancellation and early admission/shedding; security gates still fail closed.
2. Durable responsibility begins at the actual persisted acceptance/ownership boundary, not when the caller reads a receipt. HTTP disconnect/deadline alone cannot discard or cancel accepted work.
3. Attempt timeouts, retry budgets and concurrency remain bounded. Job validity, business cancellation and terminal disposition are explicit owner decisions. Do not introduce infinite retry, unlimited retention, or guaranteed eventual success.
4. Before acceptance, overload rejects rather than falsely acknowledging work. After acceptance, capacity pressure or caller disappearance cannot authorize silent loss.
5. Broker message TTL, queue expiry, application validity and retention are differentiated where relevant, without changing broker behavior or inventing new platform numbers. Existing async owner handles DLQ/replay/ack mechanics.
6. Expired or cancelled work follows the existing explicit business outcome/reconciliation contract; if none exists, report the missing decision instead of choosing deletion or indefinite execution.
7. Unknown acceptance and crash/redelivery preserve identity/idempotency and effect-before-ack rules. No conflation of a lost response with an uncommitted effect.
8. Every related rule/example in the selected scope agrees. Preserve domain depth, triggers, exceptions, ownership, safety, required proof and completion conditions.
9. Only approved source and necessary workflow/evidence paths change. English files, no machine paths. This is intentional semantic clarification, not claimed behavior-preserving compression; compress wording only after ratifying the clarified meaning.
10. Independent reviewers judge the actual final snapshot. Source/static scenario evidence must never be labelled broker or consumer runtime proof.

## Ordered Work

### Phase 1 - Revalidate and pressure-test the semantic boundary

- Status: completed
- Depends on: none
- Owned scope: lead workflow/evidence; read-only architecture critic and test strategist.
- Excluded from this phase: implementation, numeric/product policy decisions.
- Work:
  - [x] Verify root, branch, HEAD, dirty state, installed role contracts and target sources.
  - [x] Map every affected deadline/cancellation/drop rule and its owner; collect exact dependency contradictions.
  - [x] Use the architecture critic for the accepted-work ownership boundary and test strategist for the scenario matrix; freeze the bounded interpretation in this plan.
- Acceptance criteria: the existing accepted-work guarantee, required bounds and owner decisions are unambiguous; unresolved business choices block only their dependent statements.
- Validation commands: git status --short; git rev-parse HEAD; bounded native source/diff inspection.
- Evidence observed: intake matches baseline; architecture SOUND-WITH-CONDITIONS and scenario design pass-with-actions. Conditions are the exact four dependency-file qualifications recorded before edits in artifacts/w2-queue-deadline-semantics/execution-evidence.md. Adopt its nine-case matrix; no unresolved product choice is selected. Role bytes match source, with stale version metadata and unknown MCP enforcement recorded. Profile: standard; one writer, independent verifier and correctness/instruction reviews, plus applicable observability lens.
- Snapshot: HEAD ba278f4ed6962e7f20251e55784129c550aa1b85; SHA-256 ae25149398f21dac3b4609f81558bc6ae2b576c1ad9b554bd254e7d388ede305; paths skills/sohrab/alaa-reliability-sla, skills/sohrab/alaa-async-messaging, skills/sohrab/alaa-services-contract; intake-manifest.json in the task artifact directory contains sorted path/content hashes, and this digest hashes that JSON file. No skill source changed in Phase 1.

### Phase 2 - Correct doctrine and necessary dependent wording

- Status: completed
- Depends on: Phase 1
- Owned scope: one implementation lane, primary alaa-reliability-sla; proven conditional dependency files serialized.
- Excluded from this phase: all unselected surfaces and actual service/broker behavior.
- Work:
  - [x] Correct body, cancellation/deadline, admission/drop and affected verification examples under the approved boundary.
  - [x] Change dependency wording only where the recorded contradiction requires it; otherwise return explicit no-change evidence.
  - [x] Apply draft-then-compress with a preservation checklist and focused scenario checks.
- Acceptance criteria: all ten acceptance criteria hold in source; parent reconciles actual diff.
- Validation commands: focused source/scenario checks and applicable native gates below.
- Evidence observed: one writer changed ten source files, inspected its full diff, applied draft-then-compress, and evaluated all nine cases. Scoped git diff --check exited 0 with line-ending notices only. Lead reconciled actual diff and conditional dependency scope. Independent approvals and the single pointer fix are recorded in Phase 3.
- Snapshot: HEAD ba278f4ed6962e7f20251e55784129c550aa1b85; SHA-256 f900a3da29f1009ad14c12ec78c1182955d4a88c7172867a2c48fe99fede2937; paths skills/sohrab, scripts, AGENTS.md, CLAUDE.md; reviewed-initial-manifest.json preserves the initially reviewed 1805-input snapshot. Final source identity is in Phase 3.

### Phase 3 - Independently verify and review

- Status: completed
- Depends on: Phase 2
- Owned scope: independent verifier and correctness/instruction reviewers; lead owns workflow reconciliation.
- Excluded from this phase: reviewer fixes or unrelated cleanup.
- Work:
  - [x] Hold writes; run the affected integrated native checks on one identified snapshot.
  - [x] Independently evaluate scenario outcomes, ownership, exceptions, failure handling and source/quality proof boundaries.
  - [x] Reconcile findings in bounded cycles; document the resulting guidance within selected skills, record documentation grade through its owner.
  - [x] Update checkpoint and report lifecycle states with unrun runtime evidence explicit.
- Acceptance criteria: no unresolved blocker/major findings; required gates pass or affected work reports a precise blocker.
- Validation commands: Validation Matrix.
- Evidence observed: independent source gates PASS; correctness APPROVED with nine scenarios PASS; instruction APPROVED after one pointer-only fix cycle; observability PASS-WITH-GAPS limited to unassessed runtime adoption. Four affected native commands reran successfully after the pointer fix; unchanged index and agent-authority inputs retain their previous PASS. All nine changed Markdown links pass. Documentation owner classified source contracts EXEMPT-ATOMIC and workflow/YAML/JSON as exempt artifacts; no separate guide needed. Exact commands, final artifact checks, role roster and proof limits are in artifacts/w2-queue-deadline-semantics/execution-evidence.md. Final curation admitted no extra candidate and performed no memory publication.
- Snapshot: HEAD ba278f4ed6962e7f20251e55784129c550aa1b85; SHA-256 2611c58dc90a261588c4a01f420eaf6bde8c2ba92e05888b135bf1d07ab471b5; paths skills/sohrab, scripts, AGENTS.md, CLAUDE.md; tested-manifest.json contains 1805 path/content hashes and observation time. No commit; source writes remain held.

## Validation Matrix

Scenario review must state expected disposition and rule/source for each case, plus the incorrect interpretation it rejects:
- Synchronous request expires before admission or during a cancellable dependency wait: no stale retry; resources released.
- Work durably accepted, receipt sent, caller disconnects: accepted responsibility survives.
- Durable acceptance commits but response/receipt is lost: outcome is reconciled by identity; no blind duplicate side effect.
- Admission/storage fails before durable acceptance: no false accepted response.
- Durable processing attempt times out while job remains valid: bounded retry/reconciliation according to existing policy, not discard due to original HTTP deadline.
- Business validity expires or explicit cancellation occurs: apply the owner-defined observable terminal outcome; do not invent one if absent.
- Crash after effect commit before broker ack: existing idempotency/redelivery behavior remains.
- Queue/buffer saturation before versus after acceptance: preserve bounds without silently losing accepted work.
- Missing expiry policy: expose missing business decision; do not infer zero TTL, infinite retries or universal deletion.

These are static instruction/contract evaluations with independent judgment, not live model benchmarks. Use focused fixtures only when they detect a real failure mode; keyword-presence tests alone cannot prove semantics.

Native source gates from repository root:
- python -B scripts/validate_sohrab_skill_pack.py
- python -B scripts/check_skill_index.py
- python -B scripts/check_fleet_references.py
- python -B scripts/check_lifecycle_contract.py
- git diff --check
- python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260925-211735_w2-queue-deadline-semantics.md

Run selected skills' own applicable validators if present and relevant; confirm invocation before execution. Exit 2 is unavailable proof, never pass. Inspect source-versus-corpus contradictions rather than adding decorative tests. No consumer or live broker test is implied by a prose change. If the change needs that proof, report the dependency and seek separate authorization rather than claiming it.

## Delegation, resource and review policy

One owned writer because the doctrine and dependent wording share a semantic contract; do not split conflicting interpretations across writers. Use alaa-implementer-sol for the instruction-contract judgment lane under canonical policy, with the escalation criterion recorded: substantial shared behavioral-contract clarification. Read-only architecture critic and test strategist may work on independently defined questions; serialize acceptance before implementation.

Use standard orchestration with independent verifier, one correctness reviewer and instruction reviewer. Add API-contract review only if selected dependent edits actually alter a public/persisted contract; such expansion may require a user decision before writing. Do not dispatch an entire specialist catalog. No lane approves itself. No model or effort remapping is approved; dated execution profiles are in the prompt pack.

The lead alone changes shared workflow/evidence indexes. BelowNormal shell priority; at most two read-only preparation lanes and one writer; one CPU-heavy command at a time. No benchmark or live model comparison. Claimed quality/speed/cost improvement remains unmeasured. A future authorized model comparison would hold tasks/context/tools constant, vary one factor, reject safety/quality failures before comparing cost.

## Stop conditions and recovery

At most one cause-specific repair and one materially different retry per failed operation; at most two review/fix cycles. Preserve failure evidence; do not weaken gates or confuse environment failure with source defects.

Stop only affected work on overlapping dirty changes, missing required role or evidence, unresolved business semantics, necessary unapproved surface, unstable snapshot, or unavailable mandatory proof. Continue disjoint safe work. Preserve local edits and a concrete next action; no reset, destructive cleanup, global repair or installer fallback.

## Blockers and Next Action

- Blockers: none for the reviewed local instruction correction. Runtime model identity and per-role enforcement remain unknown; stale installation metadata and unattributed index movement are preserved in task evidence. No business lifecycle policy or runtime behavior is claimed proven.
- Next action: stop after final workflow/artifact validation. No commit, integration, installation or live-service action is authorized. Keep every other audit item deferred.

## Completion lifecycle

- IMPLEMENTED: proven by focused source checks on the recorded uncommitted content snapshot; local recovery risk remains until an authorized commit exists.
- MERGE_CANDIDATE: proven by affected native gates and independent correctness/instruction review; this verdict grants no merge authority.
- RELEASE_CANDIDATE: not requested.
- PUBLISHED: not requested; no external immutable publication performed.
