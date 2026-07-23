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
<output>use the agent's native output contract</output>
```

## Explorer

```xml
<task>Map the execution path and ownership for: <question>.</task>
<focus>Entry points, symbols, data flow, tests, configuration, repository rules, coupling.</focus>
<action_safety>Strictly read-only. No external research and no proposed design unless options were requested.</action_safety>
```

## Researcher

```xml
<task>Establish the external/version-specific facts needed for: <decision question>.</task>
<versions><versions derived from repository manifests/locks></versions>
<source_priority>Repository evidence, then primary/official sources.</source_priority>
<decision_boundary>Inform the orchestrator; do not decide or edit.</decision_boundary>
```

## Test strategist

```xml
<task>Design the minimal test matrix that proves: <acceptance criteria>.</task>
<failure_models><plausible broken implementations and failure modes to catch></failure_models>
<repository_commands><known test commands and helpers></repository_commands>
<action_safety>Read-only; do not write tests.</action_safety>
```

## Implementer lane

```xml
<task>Implement lane <n>: <bounded outcome>.</task>
<scope><owned files/modules>; exclude <everything else>.</scope>
<acceptance_criteria><numbered criteria></acceptance_criteria>
<dependencies><completed lane contracts or none></dependencies>
<clean_code_skill><matching installed skill or repository baseline></clean_code_skill>
<verification>
  <commands><exact targeted commands></commands>
  <low_priority_runner><absolute path when CPU-heavy></low_priority_runner>
  <resource_limits><priority, CPU count, workers, timeout></resource_limits>
</verification>
<action_safety>No unrelated work, commit, deploy, publish, destructive action, or global configuration change.</action_safety>
```

Use `alaa-implementer-sol` instead of `alaa-implementer` when the routing matrix says to escalate.

## Verifier

```xml
<task>Independently verify the combined change for: <goal>.</task>
<repository><absolute worktree path></repository>
<initial_expectation><expected clean/known git status></initial_expectation>
<commands>
  <command id="1" cpu_heavy="true|false" timeout_seconds="...">exact command and cwd</command>
</commands>
<artifacts><permitted artifact directory only></artifacts>
<resource_policy>
  Windows runner: <absolute SKILL_ROOT>/scripts/Invoke-AlaaLowPriority.ps1
  Unix runner: <absolute SKILL_ROOT>/scripts/run-low-priority.sh
  Priority: BelowNormal; CPU count: <n>; only one heavy command at a time.
</resource_policy>
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

## Reviewer

```xml
<task>Review the complete change for: <goal>.</task>
<plan><lanes and acceptance criteria></plan>
<diff_scope><base/head or touched files></diff_scope>
<verification_evidence><integrated verifier results></verification_evidence>
<stance>Fresh context, read-only, findings-first, no fixes.</stance>
<adversarial>true|false</adversarial>
```

## Architecture critic

```xml
<task>Pressure-test this proposed architecture before implementation: <plan>.</task>
<invariants><required correctness, compatibility, security, and operability invariants></invariants>
<evidence><architecture docs, relevant code paths, external contracts></evidence>
<question>Find blockers, hidden assumptions, simpler alternatives, rollout/rollback conditions.</question>
```

## Security reviewer

```xml
<task>Perform a defensive security review of: <change scope>.</task>
<trust_boundaries><actors, inputs, privileges, sensitive assets></trust_boundaries>
<verification><security tests/evidence already run></verification>
<action_safety>Repository-only, read-only, no external exploitation.</action_safety>
```

## Migration guardian

```xml
<task>Gate this schema/data migration: <change>.</task>
<database><technology/version and deployment model></database>
<rollout><old/new app and schema sequence></rollout>
<data_scale><known scale or explicitly unknown></data_scale>
<question>Check compatibility, locks/load, backfill, validation, rollback/roll-forward, abort thresholds.</question>
```

## Browser QA

```xml
<task>Execute browser QA for: <user-visible behavior>.</task>
<environment><URL, existing server, auth/test data, viewport></environment>
<scenarios><exact steps and expected results></scenarios>
<browser_constraint>Preserve --browser chromium and configured profile. Do not start duplicate services.</browser_constraint>
<artifacts><absolute permitted artifact directory></artifacts>
```

## Performance profiler

```xml
<task>Measure: <metric/question>.</task>
<workload><scenario, data shape, concurrency, warmup></workload>
<baseline_budget><baseline and pass/fail budget></baseline_budget>
<environment><comparable environment facts></environment>
<resource_policy><low-priority runner, CPU count, timeout></resource_policy>
<artifacts><profile/trace output directory></artifacts>
```

## Observability reviewer

```xml
<task>Review production diagnosability for: <change>.</task>
<failure_states><new/changed success, failure, retry, degraded states></failure_states>
<telemetry_stack><repo-observed logs/metrics/traces/alerts conventions></telemetry_stack>
<question>Map states to signals, decisions, alerts, runbooks, privacy/cardinality risks.</question>
```

## Release guardian

```xml
<task>Gate release readiness for: <change>.</task>
<scope><CI, container, config, dependencies, deployment, health, docs as applicable></scope>
<evidence><build/verification/review results></evidence>
<question>Identify conditions, ordered rollout, rollback, manual steps, and unverified prerequisites.</question>
```

## Fix-cycle dispatch

```xml
<task>Resolve reviewer/specialist findings in original lane <n>.</task>
<findings_verbatim><file:line, severity, failure, required fix></findings_verbatim>
<original_scope_and_acceptance>unchanged unless the orchestrator explicitly revises them</original_scope_and_acceptance>
<verification><targeted checks plus affected integrated checks></verification>
<output>For each finding: fixed | disputed with repository evidence; touched files; verification; new risks.</output>
```

## Documenter

```xml
<task>Update documentation for verified shipped change: <goal>.</task>
<change_summary><actual behavior, files, configuration/API/operational changes></change_summary>
<verdicts><review and specialist verdicts></verdicts>
<scope><expected documentation files/sections></scope>
<checks><docs formatter, links, examples, scope check></checks>
<action_safety>Documentation files only; no intended or unverified behavior.</action_safety>
```
