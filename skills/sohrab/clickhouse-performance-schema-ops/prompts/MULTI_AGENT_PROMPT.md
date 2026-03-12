
# ClickHouse multi-agent prompt

Spawn specialist agents in parallel, then consolidate:

1. Schema agent
   - choose engine, types, ORDER BY, PRIMARY KEY, PARTITION BY, TTL
2. Ingest agent
   - choose insert strategy, batching, async_insert, dedup, retry semantics
3. Query agent
   - review expensive queries, join patterns, FINAL usage, explain pruning gaps
4. Ops agent
   - inspect parts, merges, mutations, disk pressure, replication, background activity
5. Community-risk agent
   - scan current docs/issues/community guidance for edge cases and version-sensitive gotchas

Return one consolidated plan with:
- final DDL
- ingest path
- optimization plan
- diagnostics/runbook
- explicit risks
