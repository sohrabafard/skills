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
<task_controls><role authority identity; explicit model AND effort after owner normalization; the two fit facts and the fit-table row and column; priority/reason; admission/evidence; verified invocation surface and effective controls></task_controls>
<beads_identity><literal unique child actor; binding reference; issue IDs; ownership action claim|retain|authorized transfer|none, or not Beads-bound></beads_identity>
<skills><exact names, sources, activation conditions, and absence actions from the plan's phase/task bindings></skills>
<progress>report meaningful progress under the active host contract; use bounded invocations per package or target</progress>
<return>the shape of the return and its line bound; findings, verdicts, counts, and artifact paths only, never transcripts, full diffs, or raw logs</return>
<output>use the agent's native output contract</output>
```

Every dispatch, in every role template below, carries `<task_controls>` and `<return>`.

- **`<task_controls>`** records the pair that `routing-matrix.md` selects and `model-effort-policy.md` normalizes. Prose in the envelope sets no runtime control: the invocation itself must carry the model parameter and the effort parameter that realize that pair. Correct a missing or different parameter before you send: a lane inherits the lead's own value for an omitted control, and that is the most common cause of a pair that is too strong. The only exception is an exact verified compatibility realization under step 4 of `model-effort-policy.md` *Before every dispatch*.
- **`<cadence>`** carries the inherited cadence from `verification-and-gates.md` *Review boundary and execution cadence*.
- **`<beads_identity>`**: for a Beads-bound dispatch, resolve it through `alaa-workflow references/task-tracking.md` section `Agent identity and ownership`, and pass the global `bd` flag, `--sandbox` or `--readonly`, that its `## Beads capabilities in use` requires.
  - A write lane gets its own actor and the action `claim` for its leaf. It claims with `bd --sandbox update <id> --claim --actor <actor>` and reads the issue back. Before it returns or stops, it appends its checkpoint with `bd --sandbox update <id> --if-assignee <actor> --append-notes "<block>" --actor <actor>`. The implementation and documenter definitions hold the block and these two commands, because a lane loads no workflow reference.
  - The lane never closes its leaf. The lead closes it after it reconciles the lane's diff, so that a dependent leaf becomes ready only then. The lead keeps one `Lane: <leaf id> <actor>` line for each live leaf in the root's checkpoint block; only the lines of the last block are live.
  - Read-only gates use action `none` unless separately authorized to mutate issue state.
- **`<skills>`**: resolve it through `alaa-workflow references/companion-routing.md` and copy the lane's resolved entries into the dispatch, because a child inherits none of the parent's context. Include /alaa-testing-strategy for a lane that designs implementation or verification. Apply that reference's Mandatory Ponytail binding, including its user opt-out, before every new dispatch or continuation.
- **`<progress>`** carries the active host's reporting requirements when a dispatch can run long. Do not infer a universal watchdog timeout or require narration between every command.
- **`<return>`**: for its shape and length bound, read `alaa-low-noise references/workflow-integration.md` section `Delegated lanes`.

## Role templates

Combine the common envelope with the smallest complete template for the dispatched role:

- `alaa-ent-specialist`: the mode-specific contract in `alaa-ent-go-orm-db references/85-specialist-delegation.md`;
- a planner variant, spec analyst, explorer or researcher: [Discovery and acceptance](./delegation-prompts/10-discovery.md);
- a test strategist or architecture critic: [Design and test strategy](./delegation-prompts/20-design.md);
- an implementation lane or a collected verification repair: [Implementation](./delegation-prompts/30-implementation.md);
- a verifier or failure analyst: [Verification and failure analysis](./delegation-prompts/40-verification.md);
- a correctness, instruction or adversarial reviewer, or a finding refuter: [Correctness and instruction review](./delegation-prompts/50-correctness-review.md);
- a boundary review or specialist after a prior review round: add `<refuted_findings>` per `alaa-workflow references/review-mode.md` `## Finding triage`;
- an API contract reviewer, security reviewer or migration guardian: [Contract and security review](./delegation-prompts/60-contract-review.md);
- a dependency auditor or release guardian: [Dependency and release review](./delegation-prompts/70-release-review.md);
- an accessibility reviewer or browser QA agent: [Interface review](./delegation-prompts/80-interface-review.md);
- a performance profiler or observability reviewer: [Operability evidence](./delegation-prompts/90-completion/10-operability-evidence.md);
- a fix or documenter after review: [Review follow-up](./delegation-prompts/90-completion/20-review-followup.md).
