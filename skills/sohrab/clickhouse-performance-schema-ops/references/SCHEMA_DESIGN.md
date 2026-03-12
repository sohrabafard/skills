
# Schema design

## Base rules
- Choose types first. Shrink types before chasing exotic tuning.
- Prefer non-nullable columns when business semantics allow it.
- Use `LowCardinality(String)` for repeated dimensions when cardinality and workload justify it.
- Design ORDER BY for pruning and compression, not just for aesthetics.
- Keep PARTITION BY low-cardinality and operationally useful.

## ORDER BY guide
Ask:
1. Which predicates are most common?
2. Which predicates exclude the largest ranges?
3. Which dimensions are correlated with other columns and help compression?
4. Which high-cardinality columns only matter as a late tie-breaker?

Common patterns:
- observability logs: `(service, severity, toStartOfHour(ts), ts)` or similar patterns only if they fit access
- metrics/time-series: dimension prefixes + timestamp
- product analytics: stable dimensions used in filters before raw IDs or timestamps

## Primary key guide
- Usually equal to ORDER BY.
- Can be a prefix of ORDER BY when you want the full physical sort for compression but a smaller sparse index in memory.

## Partitioning guide
Use partitions for:
- retention windows
- tiering / storage movement
- operational drop ranges
Avoid:
- high-cardinality partition keys
- partitioning as a substitute for ORDER BY
- one-partition-per-user/session/tenant unless the workload truly demands it
