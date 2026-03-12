
# Operations and diagnostics

## System tables to inspect first
- `system.query_log`
- `system.query_thread_log`
- `system.parts`
- `system.part_log`
- `system.mutations`
- `system.projections`
- `system.replicas` (if replicated)
- `system.tables`, `system.columns`, `system.settings` as needed

## Common playbooks
### Merge pressure / too many parts
- inspect part counts per table and per partition
- inspect insert rate and batch size
- reduce small inserts or enable async inserts
- avoid brute-force `OPTIMIZE FINAL`

### Mutation backlog
- inspect `system.mutations`
- verify whether the workload should be using Replacing/Collapsing patterns instead
- kill pathological mutations only with a clear runbook

### Slow queries
- inspect query log
- quantify read amplification
- align layout and filters
- consider MVs / projections only after proving the base layout is insufficient
