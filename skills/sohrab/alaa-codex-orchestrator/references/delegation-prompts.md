# Delegation Prompt Templates

Use the smallest applicable template. Replace placeholders with concrete repository facts and absolute script paths where required.

## Common dispatch envelope

```xml
<goal><one-sentence outcome></goal>
<context><relevant repository facts, prior lane outcomes, and preserved behavior></context>
<scope>
  <owned>files/modules or read-only questions</owned>
  <excluded>explicit exclusions</excluded>
</scope>
<acceptance_criteria><numbered checkable criteria></acceptance_criteria>
<constraints><safety, compatibility, resource, and user constraints></constraints>
<authority>what the agent may and may not change or execute</authority>
<skills><exact names, sources, activation conditions, and absence actions from the plan's phase/task bindings></skills>
<progress>report meaningful progress under the active host contract; use bounded invocations per package or target</progress>
<return>the shape of the return and its line bound; findings, verdicts, counts, and artifact paths only, never transcripts, full diffs, or raw logs</return>
<output>use the agent's native output contract</output>
```

Every dispatch carries the `<return>` field. An unbounded child return is the most common way a parent's context is flooded, and the parent pays that cost on every remaining turn of the goal, not only on the turn the return arrives.

Resolve `<skills>` through `alaa-workflow references/companion-routing.md`; copy the lane's resolved entries into the dispatch because a child cannot inherit the parent's context.

Every dispatch that can run long carries `<progress>` with the active host's reporting requirements. Do not infer a universal watchdog timeout or require narration between every command. Follow `SKILL.md` for interrupted-lane recovery.

## Role templates

Combine the common envelope with the smallest applicable complete template from the routed child.

- When dispatching a spec analyst, explorer, or researcher, read [Discovery and acceptance](./delegation-prompts/10-discovery.md) for acceptance, repository-mapping, or research template.
- When dispatching a test strategist or architecture critic, read [Design and test strategy](./delegation-prompts/20-design.md) for matrix-design or architecture-review template.
- When dispatching an implementation lane, read [Implementation](./delegation-prompts/30-implementation.md) for lane template and escalation instructions.
- When dispatching a verifier or failure analyst, read [Verification and failure analysis](./delegation-prompts/40-verification.md) for evidence-run or failure-diagnosis template.
- When dispatching a correctness, instruction, or adversarial reviewer, read [Correctness and instruction review](./delegation-prompts/50-correctness-review.md) for selected review template and its boundary.
- When dispatching an API contract reviewer, security reviewer, or migration guardian, read [Contract and security review](./delegation-prompts/60-contract-review.md) for compatibility, trust-boundary, or migration template.
- When dispatching a dependency auditor or release guardian, read [Dependency and release review](./delegation-prompts/70-release-review.md) for supply-chain or release-readiness template.
- When dispatching an accessibility reviewer or browser QA agent, read [Interface review](./delegation-prompts/80-interface-review.md) for accessibility or browser-scenario template.
- When dispatching a performance profiler or observability reviewer, read [Operability evidence](./delegation-prompts/90-completion/10-operability-evidence.md) for measurement or diagnosability template.
- When dispatching a fix cycle or documenter after review, read [Review follow-up](./delegation-prompts/90-completion/20-review-followup.md) for finding-repair or verified-documentation template.
