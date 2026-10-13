# Design gates

Date: 2026-10-13. Source baseline: `1207d2e8c17d74ea77920ea9cb285b6c73554c7d`.

## Architecture

The independent architecture critic required compatibility cutover/rollback, a second ownership candidate and explicit JSON cursor derivation. The parent accepted all three and recorded the decisions in the plan before writer dispatch. Marked families require compatible consumers; rollback freezes them. The single task owner wins over editable mirrors. JSON cursor fields derive from the canonical checkpoint/direct-plan cursor. Offline gates prove no live binding/readiness.

## Test strategy

The independent test strategist required an explicit marked-family predicate and scalar-to-array snapshot projection. The parent settled both in the plan: either metadata header marks the family; exactly one of each is mandatory; all profiles enforce the new contract. Array projections retain one whole trimmed scalar or an empty array for a none sentinel. Companion identity uses resolved paths, not basenames.

The discriminating matrix is: malformed/duplicate task IDs, absent/cyclic prerequisite edges, completed tasks with incomplete prerequisites; unresolved executing work despite a planning header; mixed task stores including numbered local tasks; duplicate/missing issue mappings and skills; invalid CLI/collision no-write behavior; independently stale plan/checkpoint/JSON and same-basename wrong-family paths; completed unmarked-history compatibility; local/Beads across every profile. Start from valid fixtures, mutate one property and assert the specific diagnostic and repaired control. Use real templates/files, isolated fixed-time fixtures and bounded sequential tests. A mock no-subprocess/network guard proves only helper isolation.

Independent source scenarios cover external hubs, mere CLI presence, wrong hub, outage, rollback, cold resume, PC2 lacking PC1 source, shared resources, closed issues with failed phase gates and uncertain writes. They are not live runtime tests.

## Parent verdict

Design blockers resolved in the plan. Implementation may begin. Source implementation, focused tests and independent final gates are still pending. Both advisors were read-only; no live Beads operations or source edits occurred in their lanes.
