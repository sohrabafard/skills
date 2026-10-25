# Verification and failure analysis templates

## Verifier

```xml
<task>Independently verify the combined change for: <goal>.</task>
<repository><absolute worktree path></repository>
<initial_expectation><expected clean/known git status></initial_expectation>
<tree_pin><identified frozen snapshot and authorized scope under /alaa-workflow references/workspace-and-integration.md; apply /alaa-testing-strategy references/100-test-execution.md></tree_pin>
<commands>
  <command id="1" cpu_heavy="true|false" timeout_seconds="...">exact command and cwd</command>
</commands>
<artifacts><permitted artifact directory only></artifacts>
<execution_owner>Load /alaa-testing-strategy before verification design/execution. Apply its references/100-test-execution.md for command selection, collection and evidence; references/110-execution-resources.md for resources; references/120-result-classification.md for results.</execution_owner>
<resource_policy><absolute canonical testing-strategy runner or authorized container path, priority, CPU/container allocation, workers and timeout from the resource owner></resource_policy>
<collection_barrier>Execute the canonical collection barrier through this independent verifier. Return its combined results for the lead's serialized repair assignment; verification-and-gates.md retains phase/review scheduling and observer authority.</collection_barrier>
<review_boundary><inherited phase|final boundary, whole-engagement final candidate identity and source plan; no subtask/task independent acceptance></review_boundary>
<tier><actual scoped tier selected through /alaa-testing-strategy; inherited final candidate and cadence from the plan></tier>
<already_observed><eligible evidence citations or canonical whole-list post-repair retest; include the independent observer></already_observed>
<rerun_policy>none | one identical rerun for flake detection</rerun_policy>
<action_safety>Evidence only. Never fix or alter command semantics.</action_safety>
```

## Failure analyst

```xml
<task>Diagnose this verification failure without editing: <status and command>.</task>
<evidence><verifier output, logs, artifacts, git status, relevant lane summaries></evidence>
<question>Classify the failure, identify first cause and owner, and propose the smallest falsifying check or fix instruction.</question>
<diagnostic_authority>Read-only; targeted command only if explicitly listed here.</diagnostic_authority>
```
