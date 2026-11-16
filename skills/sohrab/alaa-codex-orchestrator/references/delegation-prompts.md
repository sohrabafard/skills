# Delegation Prompt Templates

Use the smallest applicable template. Replace placeholders with concrete repository facts, and with absolute script paths where required.

## Common dispatch envelope

```xml
<goal><one-sentence outcome></goal>
<context><established anchors (file:line, contracts, settled decisions), prior lane outcomes, cited discovery artifacts and preserved behavior; the child re-derives none of them></context>
<scope>
  <owned>files/modules or read-only questions</owned>
  <excluded>explicit exclusions</excluded>
</scope>
<acceptance_criteria><numbered: observable behavior -> proving command or selector -> expected result, or review-only: reason></acceptance_criteria>
<constraints><safety, compatibility, resource, and user constraints></constraints>
<authority>what the agent may and may not change or execute</authority>
<cadence><canonical whole-engagement plan address (Beads root or Markdown path), declared phase|final review boundary, final phase, current phase/task/subtask, pending review/commit and supplied task-owner acceptance authority></cadence>
<task_controls><role authority identity; explicit model AND effort after owner normalization; actual task scope/complexity; priority/reason; admission/evidence; verified invocation surface and effective controls; availability or affected-lane blocker></task_controls>
<beads_identity><literal unique child actor; binding reference; issue IDs; ownership action claim|retain|authorized transfer|none, or not Beads-bound></beads_identity>
<skills><exact names, sources, activation conditions, and absence actions from the plan's phase/task bindings></skills>
<progress>report meaningful progress under the active host contract; use bounded invocations per package or target</progress>
<return>the shape of the return and its line bound; findings, verdicts, counts, and artifact paths only, never transcripts, full diffs, or raw logs</return>
<output>use the agent's native output contract</output>
```

Every dispatch, in every role template below, carries `<task_controls>` and `<return>`. `<task_controls>` records the pair that `routing-matrix.md` selects and `model-effort-policy.md` normalizes and verifies; prose in the envelope sets no runtime control.

Before you send a dispatch, read the invocation back. It must carry a model parameter and an effort parameter that realize the pair in `<task_controls>`: the effort value equals the recorded effort, and the model value is the identifier or alias that `model-effort-policy.md` maps to the recorded model. Correct a missing or different parameter before you send. The only exception is an exact verified compatibility realization under step 4 of `model-effort-policy.md` *Before every dispatch*, which names both parameters for this runtime. For an implementation or fix dispatch, also confirm that `<task_controls>` records the admission predicates of the selected route.

For a Beads-bound dispatch, resolve `<beads_identity>` through `alaa-workflow references/task-tracking.md` section `Agent identity and ownership`. Pass its literal actor, binding, issue IDs, ownership action and the global `bd` flag it requires: `--sandbox` on each `bd` command that can write, unless the user authorized Dolt sync, and `--readonly` for a read-only lane. Read-only gates use action `none` unless separately authorized to mutate issue state.

For the `<return>` shape, length bound and context rationale, read `alaa-low-noise references/workflow-integration.md` section `Delegated lanes`. Workflow owns persistence; `verification-and-gates.md` owns the inherited cadence carried in `<cadence>`.

Put /alaa-testing-strategy in the `<skills>` of a lane that designs implementation or verification, so the child loads it and reads its `references/100-test-execution.md` before planning or executing checks. Resolve `<skills>` through `alaa-workflow references/companion-routing.md`, and copy the lane's resolved entries into the dispatch, because a child cannot inherit the parent's context. Apply that reference's Mandatory Ponytail binding, including its user opt-out, before every new dispatch or continuation.

Every dispatch that can run long carries `<progress>` with the active host's reporting requirements. Do not infer a universal watchdog timeout or require narration between every command. `SKILL.md` owns interrupted-lane recovery.

## Role templates

Combine the common envelope with the smallest complete template from the routed child. When you dispatch:

- `alaa-ent-specialist`, use the mode-specific contract in `alaa-ent-go-orm-db references/85-specialist-delegation.md`;
- a planner variant, spec analyst, explorer or researcher, read [Discovery and acceptance](./delegation-prompts/10-discovery.md);
- a test strategist or architecture critic, read [Design and test strategy](./delegation-prompts/20-design.md);
- an implementation lane or a collected verification repair, read [Implementation](./delegation-prompts/30-implementation.md);
- a verifier or failure analyst, read [Verification and failure analysis](./delegation-prompts/40-verification.md);
- a correctness, instruction or adversarial reviewer, or a finding refuter, read [Correctness and instruction review](./delegation-prompts/50-correctness-review.md);
- a boundary review or specialist after a prior review round, add `<refuted_findings>` per `alaa-workflow references/review-mode.md` `## Finding triage`;
- an API contract reviewer, security reviewer or migration guardian, read [Contract and security review](./delegation-prompts/60-contract-review.md);
- a dependency auditor or release guardian, read [Dependency and release review](./delegation-prompts/70-release-review.md);
- an accessibility reviewer or browser QA agent, read [Interface review](./delegation-prompts/80-interface-review.md);
- a performance profiler or observability reviewer, read [Operability evidence](./delegation-prompts/90-completion/10-operability-evidence.md);
- a fix or documenter after review, read [Review follow-up](./delegation-prompts/90-completion/20-review-followup.md).
