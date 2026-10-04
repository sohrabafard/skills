# Goal and workflow repair

This folder records the source assessment and repair of goal composition and resumable workflow planning across five first-party skills.

## What changed

- Claude goal conditions use plain completion text, separate from the skill-led kickoff. The documented cap is 4,000 characters; 600 is an authoring target, not a vendor limit.
- `alaa-workflow` saves a plan and checkpoint for actionable execution plans and authorized long execution. Explicit plan-only, read-only, chat-only, and native Plan Mode boundaries remain in force.
- Each phase and task maps to its skill source, load point, condition, and action when that skill is missing.

The [prompt composition reference](../../skills/sohrab/alaa-prompting-guide/references/06-invocation-and-composition.md) owns kickoff and goal separation. The [Claude Code runtime reference](../../skills/sohrab/alaa-prompting-guide/references/41-claude-code-runtime-features.md) owns the Desktop Code composer evidence and its limits. The [workflow skill](../../skills/sohrab/alaa-workflow/SKILL.md) routes plan and checkpoint behavior; [companion routing](../../skills/sohrab/alaa-workflow/references/companion-routing.md) owns skill bindings.

## Evidence and navigation

- [Source evidence](source-evidence.md) records official documentation and the user-reported Desktop rejection. No live Desktop command was reproduced.
- [Execution plan](docs/_agent_plans/20261004-000000_goal-and-workflow-skill-repair.md) and [checkpoint](docs/agents/20261004-000000_goal-and-workflow-skill-repair-state.md) carry scope, completion evidence, and resume state.
- [Recorded verification](final-verification.json) contains ten passing affected-tier gates: 74 workflow tests, 16 goal fixtures plus boundaries, two 31-case contract self-tests, and pack/index/reference/lifecycle checks. Nine unchanged gate results are carried forward; the corrected workflow suite was rerun. The earlier 71-test result is superseded.
- [Documentation grades](documentation-grades.json) classifies every changed Markdown file in this work family.

This folder documents the repaired skill behavior; it does not certify an installed skill-pack update or Desktop runtime acceptance.

## Review and closure

The independent instruction reviewer and correctness reviewer both returned APPROVED. Review repairs closed historical-status bypasses, unphased task omissions, invalid skill identities, unrelated state correlation, and numbered-reference false positives. Invocation and diagnostic wording findings are also closed.

The final source snapshot covers 535 inputs at HEAD `360a78c584d4c606c205797f8feebed4c14d6314`; hashes matched before and after verification. Structural checks retain non-blocking body-length warnings and two informational target-path notices. The source changes are uncommitted; recovery depends on preserving this working tree and evidence family.

Final curation retained no separate memory candidates: the reusable corrections already belong to the edited canonical skills and regression tests. No memory was written.

Run accounting: nine agents across seven roles. The final source gate set contains ten commands, with eleven executions including the superseded workflow run; nine results were carried forward after the final correction. Branch span is unavailable because no commit was authorized.
