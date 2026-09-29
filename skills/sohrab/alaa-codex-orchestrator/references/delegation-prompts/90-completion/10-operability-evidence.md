# Operability evidence templates

## Performance profiler

```xml
<task>Measure: <metric/question>.</task>
<budget_owner>/alaa-algorithms-data-structures owns the complexity budget this measurement is judged against — the operation, the dimension that grows, the bound, and the input size the bound was measured at. Read it when the declared budget names no growing dimension, or when the finding is that the path has no enforced maximum.</budget_owner>
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
