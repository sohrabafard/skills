# Design Plan - Test execution ownership

- Plan kind: design
- Task ID: `test-execution-ownership-design`
- Profile: resumable
- Task store: local
- Status: complete
- Created: `2026-10-25`
- Checkpoint: `docs/agents/20261025-test-execution-ownership-design-state.md`
- Approval status: approved
- Approval by: user
- Approval on: 2026-10-25
- Approval evidence: The user explicitly said "PLEASE IMPLEMENT THIS PLAN" and reproduced the approved plan in this chat. The user-owned source is `docs/design/separate.md`; its staged and unstaged edits remain untouched.

## Summary and Outcome

Generic test execution currently lives in both orchestrators, including resource runners and result classification. Make alaa-testing-strategy the single owner, reachable without orchestration. Keep role allocation, independence and phase scheduling in the mirrored orchestrators.

## Scope

Testing strategy, both orchestrator consumers and validators, compatibility runners, and workflow shared-file ownership/resume. No new skill, installation, commit, publication, unrelated policy extraction, automatic worktree or journal/locking system.

## Proposed Design

Add testing-strategy references `100-test-execution.md`, `110-execution-resources.md`, and `120-result-classification.md`. Transfer general execution policy, leaving triggered pointers in consumers. Preserve scope tiers, validity/reuse, classify-before-repair and flake behavior. Retain host-neutral runner implementations in testing-strategy; old orchestrator entrypoints forward without changing arguments or results.

Collect independent checks before one batch repair. Preserve the minimal early repair exception for an obstruction blocking all or most checks, then resume collection. Retest the entire recorded list on the repaired frozen snapshot under existing budgets. Orchestrators retain observer independence and implementer continuation/allocation.

Serialize CPU-heavy commands per host for this workflow. Explicitly budget concurrent test/dependency containers within effective host CPU capacity and align worker counts with container allocation. Comparative timing requires an idle host, identical CPU/workload/cache/setup, interleaved before/after samples, timer resolution, raw samples and deviations. Loaded-host flake diagnosis remains valid without a performance claim.

Workflow owns one active writer per file, generated output or shared runtime resource. Before replacing a stopped writer reconcile process/descendant liveness, stable scoped files and existing journal/issue/checkpoint. Unknown ownership blocks only overlapping writes. Resume in the same checkout preserving the diff; compaction does not transfer a live writer's ownership.

## Decisions

| Date | Owner | Decision | Reason |
|---|---|---|---|
| 2026-10-25 | user | Transfer all generic execution policies, not only the original two rules | Direct work needs the same policies |
| 2026-10-25 | user | Permit concurrent disjoint-file writers in one checkout | No automatic new worktree; shared resources still have one owner |
| 2026-10-25 | user | Leave non-test extraction candidates as recommendations | Avoid widening this implementation |
| 2026-10-25 | lead | Keep legacy runner paths as forwarding adapters | Preserve external invocation compatibility |

## Open Questions

None for implementation. Native Windows execution availability remains a verification limit, not a design decision.

## Acceptance Criteria

One canonical rule owner; direct and both runtime loading paths; equivalent runner forwarding; safe shared-file resume; preserved pre-existing test doctrine. Six requested repository/pack gates and applicable contract self-tests, rendering/grant checks, runner validation and independent reviews pass. Static proof never claims live agent compliance.

## Handoff Package

- Confirmed facts: Current source was read. Existing contract checkers assert policy text inside orchestrators, so transfer requires checking new ownership rather than dropping assertions.
- Open assumptions: Native Windows availability must be observed.
- Ruled out: New skill, automatic worktrees, duplicate normative policy, speculative non-test refactors.
- Read first on resume: this design; `docs/_agent_plans/20261025-test-execution-ownership.md`; `skills/sohrab/AGENTS.md`.
- Environment notes: Beads hub binding verified; writes use authorized sandbox escalation, no database initialization or configuration changes.
- Traps: Preserve user-owned `docs/design/separate.md`; generated role wrappers must be rendered from their sources.

## Design Position

- Position owner: `docs/agents/20261025-test-execution-ownership-design-state.md`
