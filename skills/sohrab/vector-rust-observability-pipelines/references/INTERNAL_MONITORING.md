
# Internal monitoring

Vector can observe itself.

## Wire these sources
- `internal_logs`
- `internal_metrics`

## Watch for
- dropped events
- retries
- backpressure
- buffer utilization
- sink errors
- healthcheck failures
- CPU/memory trends
- restart loops / startup stalls

## 0.53+ migration checks
- Metric renames:
  - `buffer_max_size` -> `buffer_max_size_bytes`
  - `buffer_size` -> `buffer_size_bytes`
- Histogram change:
  - `buffer_byte_size` bucket model changed (10 -> 26 buckets), so historical alert thresholds may need retuning.
- If dashboards/alerts depend on old internal metric names, migrate them before rollout.
- During upgrade windows, compare both pipeline health and internal metrics trend deltas to avoid false positives from renamed/rebucketed signals.

## Startup policy
If the deployment must fail fast when sinks are unhealthy, use `--require-healthy`.
Otherwise, document that Vector may start and retry while unhealthy sinks recover.
