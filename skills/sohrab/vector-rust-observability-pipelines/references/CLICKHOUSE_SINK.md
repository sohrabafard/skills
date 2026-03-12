
# ClickHouse sink

## Core options to decide deliberately
- `endpoint`
- `database`
- `table`
- `auth`
- `tls`
- `compression`
- `batch.max_bytes`
- `batch.max_events`
- `batch.timeout_secs`
- `buffer.type`
- `buffer.when_full`
- `acknowledgements.enabled`

## Schema alignment
Choose between:
- row-wise JSON formats for simplicity
- Arrow stream batch encoding for higher-performance binary transfer when the schema and current version support it cleanly

## 0.53+ pragmatic guidance
- Keep `format: json_each_row` as the safest default for heterogeneous payloads and frequent schema evolution.
- Consider `batch_encoding.codec = "arrow_stream"` only when:
  - schema is stable and tightly controlled,
  - you need higher throughput/lower CPU for large batches,
  - you have validated target ClickHouse behavior in staging with production-like data.
- Always keep a rollback path to JSON format for fast incident recovery.

## Timestamp handling
If timestamps arrive as RFC3339/ISO8601 strings, consider `date_time_best_effort`.

## Schema drift
`skip_unknown_fields` can help tolerate extra fields, but it should be an intentional choice, not an accident.
