# Schema fixtures for check-signoz-schema.py

Committed so the checker's assertions are shown to fail before it is trusted to report clean.

- `green/` — every table and column this skill claims, plus columns the real tables carry that
  this skill does not claim. Exit `0`. It proves two things: no false positive on a correct
  install, and no false positive on a superset, which every real install is.
- `red-missing-column/` — the traces span table with `ts_bucket_start` deleted. Exit `1`, naming
  that column. This is the stale-skill signal: it is what a SigNoz upgrade that renamed the
  bucket column would look like.
- `red-sorting-key/` — every column present, but `sorting-keys.tsv` reports a key that no longer
  begins `ts_bucket_start, resource_fingerprint`. Exit `1`. Every performance rule in
  `references/clickhouse-traces-reference.md` rests on that prefix, so a silent change to it must
  be loud here.

Each `<db>.<table>.tsv` is `DESCRIBE TABLE` output reduced to its first two fields, which is what
`--describe-dir` reads. Capture a real one with:

```
clickhouse-client --query "DESCRIBE TABLE signoz_traces.distributed_signoz_index_v3 FORMAT TabSeparated" > signoz_traces.distributed_signoz_index_v3.tsv
clickhouse-client --query "SELECT concat(database,'.',name), sorting_key FROM system.tables WHERE database LIKE 'signoz%' FORMAT TabSeparated" > sorting-keys.tsv
```
