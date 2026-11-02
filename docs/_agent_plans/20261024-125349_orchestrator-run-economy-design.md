# Design Plan - Orchestrator run economy and failure clarity

- Plan kind: design
- Task ID: `20261024-125349_orchestrator-run-economy-design`
- Profile: resumable
- Task store: local
- Status: completed
- Created: `2026-10-24T12:53:49Z`
- Checkpoint: `docs/agents/20261024-125349_orchestrator-run-economy-design-state.md`
- Approval status: approved
- Approval by: user (sohrabafard)
- Approval on: 2026-10-24
- Approval evidence: In the session of 2026-10-24 the user replied "the plan is approved" to plan version 2 delivered in chat, then selected "execute in this session" when asked for the next step. Commit was not granted.

## Summary and Outcome

- Current repository truth: Both orchestrators already collect before repair, keep going past independent failures, allow one minimal early repair, batch fixes into one serialized lane, and route only ambiguous failures to the analyst (`alaa-cc-orchestrator references/verification-and-gates.md` Gate economics). Users still observe three costs: tiny lanes that multiply round trips, failure reports that do not locate the failing case, and repair lanes that rediscover context. Causes found in current text: "smallest practical disjoint lanes" (verification-and-gates `Before any dispatch` step 3); the lead may not edit while implementers are viable, which conflicts with keeping small work inline (`SKILL.md` lead contract versus Dispatch discipline); no rule maps several same-owner subtasks to one dispatch; verifier output is per command with only an error excerpt; a selector that matches zero cases can pass; acceptance criteria need not name their proving check; the implementer template carries two overlapping control blocks; the batch repair lane starts without context; retest scope depends on the agent's judgment of changed inputs; repeated harness failures have no rule.
- Outcome: The orchestrators make agents finish work in fewer, larger, clearer dispatches, locate every failing case, repair with preserved context, and retest the recorded check list once, while independent verification, review, specialist gates and Beads tracking still run.

## Scope

- In scope: `alaa-cc-orchestrator` and `alaa-codex-orchestrator` (SKILL.md, references, delegation prompts, agent sources for verifier and implementers, renderer outputs, contract checker), and `alaa-testing-strategy`.
- Out of scope: `alaa-workflow` hierarchy schema, other skills, `vendor/`, installed agent copies, global configuration, commit, push, installation, publication.
- Constraints and assumptions: The two orchestrators change together and differ only in runtime mechanics and delegation polarity. Each rule has one owning file; existing rules are cited, not restated. No new agent roles, no per-failure diagnostic stage, no before/after measurement. Structural checks prove text, not live behavior.

## Proposed Design

1. Lane sizing and dispatch unit (owner: verification-and-gates `Before any dispatch`; SKILL.md Dispatch discipline). Draw the fewest lanes that keep write scopes disjoint and buy real parallelism. Split only for disjoint parallel write scope, a different owning skill or authority, a different task model/effort, or work exceeding one agent's context. Sequential work in one scope is one lane. The dispatch unit is the lane, not the subtask: same-owner subtasks of one task run in one dispatch, and that agent runs task acceptance at its end. Beads hierarchy is unchanged.
2. Lead inline edits (owner: SKILL.md lead contract and execution profile). The lead may make a mechanical local edit with known scope, no design decision, finishable in a few tool calls. A lead-authored diff disqualifies `lean`; Stage D review is then dispatched. Heavy verification stays with the verifier.
3. Task clarity (owner: delegation-prompts envelope and implementation template). Every acceptance criterion states the observable behavior, its proving command or selector, and the expected result, or records a review-only reason. `<context>` carries discovered anchors (file:line, contracts, settled decisions) and cites explorer artifacts. Merge `<role_selection>` into `<task_controls>` without dropping a required field. Confirm the implementer output contract returns changed decisions and contracts for the next lane; add only if absent.
4. Per-case failure report (owner: verifier agent source in each runtime). For each failing case: command and case identity, stage (setup, execution, assertion, cleanup), first causal error with file:line, expected versus observed, classification, dependent cases blocked, cleanup state, artifact path. Per command: passed, failed, blocked, not-run counts. Group cases sharing a first causal error. Prefer the runner's machine-readable output. Unknown cause stays unknown.
5. Readiness and dependency (owner: Gate economics step 1). The recorded check list adds reporter format and declared case dependencies. For a new, changed or harness-history command, one dry selection confirms the selector selects the expected cases. A selector selecting zero cases is `TEST-INFRA-FAILURE`, never `PASS`. A case dependent on a failed precondition is `SKIPPED` naming its blocker.
6. Context-preserving batch repair (owner: Gate economics step 2; routing-matrix Failure routing; collected repair template). One serialized repair lane remains. When one existing implementer's still-valid assignment and context cover most failures, continue that agent through the runtime's continuation mechanism instead of a fresh dispatch; dispatch fresh only when context is invalid or Implementation routing selects another profile.
7. Full check-list retest (reuse owner: `alaa-testing-strategy` SKILL.md result validity; consumers: Gate economics, Stage C). After batch repair, rerun the entire recorded check list on a frozen snapshot, because agent judgment of invalidation is unreliable and one full rerun costs less than another cycle. Proven new impact extends the list; nothing outside it reruns. The final exhaustive rule is unchanged.
8. Repeated harness failure (owner: failure-taxonomy Diagnostic sequence). The same `TEST-INFRA-FAILURE` or `ENVIRONMENT-BLOCKED` with the same first error recurring does not earn another full run; its owner examines the smallest reproduction within the existing retry budget while safe independent checks continue.
9. Test design and incremental migration (owner: `alaa-testing-strategy`). Inventory the topic's existing tests before writing one and reuse sufficient tests. One case failing does not stop independent cases; declare real dependencies. A case may hold several assertions proving one behavior. Cleanup failure maps to `CONTAMINATED` and stops dependent execution. Migration is limited to topics the task touches; wider migration is a separate Beads follow-up. Failure alone never justifies deletion, except the quarantine deadline in `references/50-flake.md`.
10. Not restated: collect before repair, keep-going, early-repair exception, analyst only for ambiguity, hermetic tests and topic selectors, deletion after independent review, two fix-review cycles, clear owners never bypass collection.

## Decisions

| Date | Owner | Decision | Reason |
|---|---|---|---|
| 2026-10-24 | user | Main cycle: record check list, collect, batch repair, rerun the same list, independent review | Stated in the original plan and kept |
| 2026-10-24 | user | No added agents, no per-failure diagnostic stage, no before/after measurement | Stated in the original plan |
| 2026-10-24 | user | Rerun the full recorded check list after batch repair, replacing failed-and-invalidated reruns at that step | Agent invalidation judgment is unreliable |
| 2026-10-24 | user | Adopt v2 additions: lane sizing, lead inline edits, criterion-to-check mapping, per-case failure report, zero-selection rule, context-preserving repair | Approved plan version 2 |
| 2026-10-24 | user | Execute in this session; commit not granted | Answer to the next-step question |

## Open Questions

None blocking. Verify at execution start: the full implementer output contract, `check_agent_contracts.py` coverage, and the VERSION/CHANGELOG convention of each pack.

## Acceptance Criteria

1. One independent case failing does not stop other independent cases.
2. A failed precondition marks its dependent case `SKIPPED` naming the blocker.
3. A selector that selects zero cases never reports `PASS`.
4. The first failure report locates each failing case well enough to route repair without a rerun.
5. Failures are batched before repair under one repair owner; continuation is used when context is valid.
6. After repair the full recorded check list reruns, and nothing outside it.
7. A repeated harness failure leads to a bounded reproduction, not another full run.
8. Test deletion keeps required coverage and has independent acceptance; the quarantine exception is explicit.
9. Sequential same-scope work is one lane; same-owner subtasks share one dispatch.
10. The lead may make a mechanical edit; afterwards `lean` is disallowed.
11. Every acceptance criterion names a proving check or a review-only reason.
12. Both runtimes reach identical decisions; their texts differ only on runtime mechanics.
13. No new rule is stated in two owners, except the mirrored orchestrator pair.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): Current rule locations listed under Current repository truth were read on 2026-10-24 in this session. The two verification-and-gates files differ only at lines 37, 98-99, 106 and 110 (diff with names normalized).
- Open assumptions (believed but unverified, each with what would verify it): Implementer output contract may already return handoff facts (read its agent source).
- Ruled out (approach, reason, evidence): Changing the Beads phase-task-subtask schema; mapping dispatch to lanes achieves the same with no workflow change.
- Read first on resume (ordered exact paths): this plan; `skills/sohrab/AGENTS.md`; `skills/sohrab/alaa-cc-orchestrator/references/verification-and-gates.md`; `skills/sohrab/alaa-testing-strategy/SKILL.md`.
- Environment notes (command shapes that work here, and ones that look right but fail): Run checkers with `python3` from the repository root under WSL.
- Traps (looks correct, is not): Restating an existing Gate economics rule while adding the delta.

## Design Position

- Position owner: `docs/agents/20261024-125349_orchestrator-run-economy-design-state.md`

Date and attribute decisions with reasons. Record actual approval in all four fields; never infer it from implementation intent. Complete only after attributable dated approval. Keep position in the checkpoint and knowledge in the handoff package. This design authorizes no execution, issue registration or external effect.
