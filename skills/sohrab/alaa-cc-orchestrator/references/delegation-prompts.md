# Delegation Prompt Templates

Use the smallest applicable template. Replace placeholders with concrete repository facts and absolute script paths where required.

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
<cadence><whole-engagement plan, declared phase|final review boundary, final phase, current phase/task/subtask, pending review/commit and supplied task-owner acceptance authority></cadence>
<task_controls><role authority identity; explicit model AND effort after owner normalization; actual task scope/complexity; priority/reason; admission/evidence; verified invocation surface and effective controls; availability or affected-lane blocker></task_controls>
<beads_identity><literal unique child actor; binding reference; issue IDs; ownership action claim|retain|authorized transfer|none, or not Beads-bound></beads_identity>
<skills><exact names, sources, activation conditions, and absence actions from the plan's phase/task bindings></skills>
<progress>report meaningful progress under the active host contract; use bounded invocations per package or target</progress>
<return>the shape of the return and its line bound; findings, verdicts, counts, and artifact paths only, never transcripts, full diffs, or raw logs</return>
<output>use the agent's native output contract</output>
```

Every dispatch carries `<task_controls>` and `<return>`. Normalize omitted controls through `model-effort-policy.md` before recording and invoking the pair. Resolve task controls through `routing-matrix.md` and verify the actual invocation through `model-effort-policy.md`; this envelope records the choice and cannot set runtime controls by prose. Every role template below inherits this requirement.

For Beads-bound dispatches, resolve `<beads_identity>` through `alaa-workflow references/task-tracking.md` section `Agent identity and ownership`; pass its literal actor, binding, issue IDs and ownership action. Read-only gates use action `none` unless separately authorized to mutate issue state.

For the `<return>` shape, length bound and context rationale, read `alaa-low-noise references/workflow-integration.md` section `Delegated lanes`. Workflow owns persistence; `verification-and-gates.md` owns the inherited cadence carried in `<cadence>`.

Before designing implementation or verification, include /alaa-testing-strategy in `<skills>` and load it; read its `references/100-test-execution.md` before planning or executing checks. Resolve `<skills>` through `alaa-workflow references/companion-routing.md`; copy the lane's resolved entries into the dispatch because a child cannot inherit the parent's context.

Every dispatch that can run long carries `<progress>` with the active host's reporting requirements. Do not infer a universal watchdog timeout or require narration between every command. Follow `SKILL.md` for interrupted-lane recovery.

## Role templates

Combine the common envelope with the smallest applicable complete template from the routed child.

- When dispatching a planner variant, spec analyst, explorer, or researcher, read [Discovery and acceptance](./delegation-prompts/10-discovery.md) for acceptance, repository-mapping, or research template.
- When dispatching a test strategist or architecture critic, read [Design and test strategy](./delegation-prompts/20-design.md) for matrix-design or architecture-review template.
- When dispatching an implementation lane, read [Implementation](./delegation-prompts/30-implementation.md) for implementation or collected verification repair and escalation instructions.
- When dispatching a verifier or failure analyst, read [Verification and failure analysis](./delegation-prompts/40-verification.md) for evidence-run or failure-diagnosis template.
- When dispatching a correctness, instruction, or adversarial reviewer, read [Correctness and instruction review](./delegation-prompts/50-correctness-review.md) for selected review template and its boundary.
- When dispatching an API contract reviewer, security reviewer, or migration guardian, read [Contract and security review](./delegation-prompts/60-contract-review.md) for compatibility, trust-boundary, or migration template.
- When dispatching a dependency auditor or release guardian, read [Dependency and release review](./delegation-prompts/70-release-review.md) for supply-chain or release-readiness template.
- When dispatching an accessibility reviewer or browser QA agent, read [Interface review](./delegation-prompts/80-interface-review.md) for accessibility or browser-scenario template.
- When dispatching a performance profiler or observability reviewer, read [Operability evidence](./delegation-prompts/90-completion/10-operability-evidence.md) for measurement or diagnosability template.
- When dispatching a fix cycle or documenter after review, read [Review follow-up](./delegation-prompts/90-completion/20-review-followup.md) for finding-repair or verified-documentation template.
