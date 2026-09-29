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
