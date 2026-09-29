## Performance budgets to assert

Measured on the lowest-capability lane in `assets/browser-test-matrix.yaml`; a feature may state its own.

```text
database open on application boot: < 100 ms p75, < 500 ms p95
route-level cached read:           < 50 ms p75
migration without progress UI:     < 2 s, or ship progress and a retry
outbox flush batch:                outboxBatchSize, default 25
```

The complexity bound behind each is in `50-transactions-performance-and-query-patterns.md`. A measured
number that meets its budget on a small store and states no bound will stop meeting it as the store grows.
