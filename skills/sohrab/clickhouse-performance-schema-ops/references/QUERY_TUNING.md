
# Query tuning workflow

## First pass
- identify the true bottleneck: too much data read, expensive joins, FINAL semantics, bad grouping, or poor data layout
- compare rows/bytes read to rows returned
- inspect `system.query_log`

## Questions to answer
- Is the filter aligned with ORDER BY / primary index?
- Would a materialized column or skip index help?
- Is a materialized view better than repeatedly computing the same aggregation?
- Is the join pattern appropriate for ClickHouse?
- Is `FINAL` being used for correctness or accidentally everywhere?

## Rules
- push selective filtering as early as possible
- minimize joins; precompute/denormalize when economically justified
- add skip indexes only after types and primary layout are already reasonable
- use projections for alternate single-table access paths, not as a universal hammer
