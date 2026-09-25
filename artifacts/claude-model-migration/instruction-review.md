# Independent instruction-contract review

- Agent: claude_instruction, temporary alaa-instruction-reviewer, requested/configured GPT-6 Astra/high; observed identity unknown.
- Verdict: CHANGES-REQUESTED.
- Source: the frozen 482-file candidate, manifest SHA-256 `f93a0f4c937d19e1403e898489de74b76a2872d8a225276eafa0ed9661a8961c`.

## Finding

Major, `skills/sohrab/alaa-prompting-guide/references/90-model-selection.md:20`: replacing the baseline runtime-neutral "Default down when pinning" and "When uncertain, stay lower" rule with "Diagnose before escalation" changes GPT selection behavior, removes the old higher-tier judgment constraint, and conflicts with the plan's GPT-preservation boundary. Required correction: retain baseline Codex behavior and scope the new procedure to Claude. This is a semantic scope correction, not behavior-equivalent compression.

Lead decision: accept the finding; do not authorize a GPT behavior change. Aggregate security/release findings before final fix cycle 2, then restore Codex behavior and request focused independent re-review.

## Focused correction verdict

The reviewer APPROVED the supplied final item 5: the complete baseline rule is explicitly Codex-only, and the newer diagnostic rule explicitly Claude-Code-only. No remaining instruction-text finding. The first focused re-review performed no additional inspection before interruption and truthfully reported the correction unverified. A materially different bounded retry reviewed the actual text read by the lead against the reviewer's earlier baseline evidence. Direct fix-cycle-2 filesystem bytes and unchanged surrounding content were not independently inspected by that reviewer; the independent verifier owns that final binding. This limitation is not a claim that direct filesystem review occurred.

Repair evidence is in `policy/fix-cycle-2/`; final byte/delta verification is recorded separately under `verification/final/`.

The independent verifier completed that binding: Codex and Claude bodies match their respective baseline/pre-fix texts after label removal; replacing item 5 reconstructs the entire pre-correction file with line endings normalized only. Exactly that one file differs in the 482-file manifest. Both affected source gates exited 0. Final manifest SHA-256: `9ac7145a6048d35118ba78f2d80d32ab2280a27b1b2181533815ef8d32a767e5`. The major is resolved by independent instruction judgment plus independent disk/delta proof.

## Evidence and limits

Reviewer inspected instruction deltas for invocation, effort, selection, subagent authoring, runtime resolution, catalog/policy and rule-writer metadata; new model/evaluation references; plan and compression records. Independent gates, unknown identity, fallback disclosure, historical separation and replacement-only output were preserved. Schema/checker internals and live/external evidence were outside this lens. Body preservation relies on the separate independent correctness review. No source edits or live runs occurred. A long silent review was interrupted and resumed from its existing transcript; the reviewer reported no stuck operation or lost evidence.
