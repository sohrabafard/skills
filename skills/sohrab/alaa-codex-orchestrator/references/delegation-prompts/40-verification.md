# Verification and failure analysis templates

## Verifier

```xml
<task>Independently verify the combined change for: <goal>.</task>
<repository><absolute worktree path></repository>
<initial_expectation><expected clean/known git status></initial_expectation>
<tree_pin><authorized commit SHA or content snapshot under test>. Recheck the same content identity at start, between commands, and at the end; if it moved, stop and report which commands ran before the move. Do not create a commit for this check without permission.</tree_pin>
<commands>
  <command id="1" cpu_heavy="true|false" timeout_seconds="...">exact command and cwd</command>
</commands>
<artifacts><permitted artifact directory only></artifacts>
<resource_policy>
  Windows runner: <absolute SKILL_ROOT>/scripts/Invoke-AlaaLowPriority.ps1
  Unix runner: <absolute SKILL_ROOT>/scripts/run-low-priority.sh
  Priority: BelowNormal; CPU count: <n>; only one heavy command at a time.
</resource_policy>
<tier>affected | exhaustive — affected once per phase, exhaustive once on the final candidate</tier>
<already_observed><commands whose recorded results are still valid, with the run that produced each; do not re-run these></already_observed>
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
