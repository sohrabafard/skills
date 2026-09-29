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


## Release checklist

- [ ] Decision record names the data class and source of truth for every store touched.
- [ ] Every index key path verified against the record type it indexes.
- [ ] Every read's bound stated; no `O(n)` read on a user-facing route.
- [ ] Capability detection implemented and the tier persisted.
- [ ] Quota error path exercised at level 2 and level 4.
- [ ] Cleanup implemented for every refetchable class, with a cap in the budget file.
- [ ] Logout purge indexed, atomic or journalled, verified by a ranged count.
- [ ] Multi-tab upgrade and the service-worker connection both exercised.
- [ ] A WebKit lane completed if the product supports Safari or iOS.
- [ ] Private-mode checked; no offline promise at tier 0 or 1.
- [ ] Older-schema and malformed records rejected on read.
- [ ] Telemetry per failure class, registered and bucketed, with no payload.
- [ ] User-facing copy matches the wording table in `70-cache-and-drafts.md`.

