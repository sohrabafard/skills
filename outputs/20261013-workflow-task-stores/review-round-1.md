# Independent review - round 1

Both reviewers inspected the combined candidate against baseline `1207d2e8c17d74ea77920ea9cb285b6c73554c7d` and returned changes requested. Neither changed source or reran the full suite.

## Correctness

1. Major: a marked local family accepted an issue mapping outside phase sections. The global escaped-mapping scan covered Beads only, allowing mixed task authority and skipped skill checks. Require global local-mode rejection and a regression.
2. Minor: field extraction used whitespace that could cross a newline. Empty blockers/next action absorbed the next field, violating empty-array snapshot projection. Require same-line extraction and independent empty-value cases.
3. Minor: the initializer accepted the local-only `not applicable` sentinel for a Beads binding, producing a family the validator rejected. Require misuse exit 2 before writes and an atomicity regression.

The reviewer reproduced these through bounded read-only Python probes. The owning code lane must add red tests, make cause-specific fixes and record green evidence.

## Instruction contract

Major: small issue-only work was admitted, but unconditional plan validation and plan/checkpoint evidence/curation sinks made completion impossible without unadmitted files. Condition artifact-only gates on admission and use canonical issue notes for issue-only evidence, position, handoff and curation. Preserve all substantive validation, lifecycle, curation and permission gates. The prose lane must draft/compress the correction before closure review.

Other reviewed scenarios supported explicit selection, external hubs, wrong/unavailable hubs, uncertainty, scope authority, old-family stability, compatibility freeze, phase/issue separation, shared-resource/PC2 limits, mandatory resume reads, task-free JSON and memory boundaries. Compression had no additional observed loss.

## Parent disposition

Accepted all four findings. One repair cycle assigned to the two original owners; no scope expansion to other projects or tools. Source manifest `52a1c08d729e316006be574715c0d102a0d40591dd615725f9f20bb4a5046379` is superseded by this repair cycle. Closure review and independent full affected verification remain pending. Live integration/runtime compliance was not assessed.

## Repair and closure evidence

- Code: three new regression methods first reproduced six failing subcases, then the same assertions passed. The independent correctness reviewer returned APPROVED after inspecting repairs, parser callers and red/green evidence and running bounded read-only probes. Full-suite compatibility proof remains required.
- Instructions: issue-only recording/validation correction was drafted, passed through rule-writer and applied with the candidate-admission condition restored by the parent. Required behavior, curation, lifecycle and authority gates remain. Independent instruction reviewer returned APPROVED for this repair and the five mirrored consumer corrections; no findings remain. Source is frozen for full affected verification.
- Direct consumers: parent inspection found universal plan-checkbox mandates and plan-only task dependency consumption in both orchestrator gate references. The plan's related-file allowance covers five mirrored paragraphs in each. A separate draft/compression pass routes these decisions back to workflow; no allocation/resource/permission policy changes. Include them in instruction closure and both orchestrators' source validators.

## Full-suite fixture reconciliation and second closure

The independent full suite found four stale fixtures (verification-round-1.md). The original code owner corrected only test setup and the retired readiness-placeholder expectation. Four focused methods passed; every exit/diagnostic/workspace/snapshot/artifact-count oracle was retained. Independent correctness closure returned APPROVED: reversing exactly the four corrections reproduced the prior frozen test hash, both production-script hashes were unchanged, and the negative snapshot test still failed for its intended diagnostic before passing after evidence was added. No findings remain. New 19-file identity: b67537a006084689f21addcf517fbe6df90aab74a90162c11f625be291f52bc9. Final full-suite verification is required on this identity.
