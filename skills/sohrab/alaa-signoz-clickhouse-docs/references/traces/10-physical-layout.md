# Trace physical layout

Read the [signal prerequisites](../clickhouse-traces-reference.md) before this topic.

Historical layout read on 2026-07-30, rechecked against the released collector in
`../90-versions.md` on 2026-09-26, for `signoz_index_v3`:

```
PartitionBy: toDate(timestamp)
OrderBy:     (ts_bucket_start, resource_fingerprint, has_error, name, timestamp)
TTL:         toDateTime(timestamp) + toIntervalSecond(1296000)          -- 15 days
```

and for `traces_v3_resource`:

```
PartitionBy: toDate(seen_at_ts_bucket_start)
OrderBy:     (labels, fingerprint, seen_at_ts_bucket_start)
TTL:         toDateTime(seen_at_ts_bucket_start) + INTERVAL 1296000 SECOND + INTERVAL 1800 SECOND DELETE
```

Re-derive with the target `COLLECTOR_TAG` selected through `../90-versions.md`:

```bash
curl -s https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/COLLECTOR_TAG/cmd/signozschemamigrator/schema_migrator/traces_migrations.go \
  | grep -n 'OrderBy\|PartitionBy\|TTL:'
```

Four things follow, and they are the reason behind rules this skill used to assert bare:

1. **`ts_bucket_start` is the first key column**, so a query without a `ts_bucket_start` predicate
   cannot use the primary index at all and reads every part in the date partition. This is why the
   bucket predicate is not optional, and it is a stronger reason than "SigNoz stores 30-minute
   buckets".
2. **`resource_fingerprint` is second**, so filtering resources through the CTE plus `GLOBAL IN`
   turns a resource-attribute filter into a primary-key range. It is also why adding the CTE when
   the query filters no resource attribute makes the query slower rather than safer: an unfiltered
   fingerprint set widens the key range instead of narrowing it.
3. **`has_error` and `name` are third and fourth**, so filtering or grouping on `has_error` or `name`
   is index-supported. Filtering on `http_method`, `duration_nano`, `status_code` or a map key is
   not — those are read from the rows the key range already selected. Order the predicates that way.
4. **The resource table's TTL is the index table's TTL plus exactly 1800 seconds.** That margin is
   the same 1800 the bucket predicate uses, and it is what keeps a resource row alive long enough to
   join a span at the oldest edge of the retention window. It is a designed safety margin, not a
   coincidence.

`python3 scripts/check-signoz-schema.py --dsn URL` asserts that the sorting key still begins
`ts_bucket_start, resource_fingerprint`. If that assertion fails, every rule above needs rewriting
before any query does.
