# Log column access

Read the [signal prerequisites](../clickhouse-logs-reference.md) before this topic.

## Column access

| Instead of | Use | Why |
|---|---|---|
| `attributes_string['method']` | `attribute_string_method` | materialized column, no map lookup per row |
| `attributes_number['response.time']` | `attribute_number_response$$time` | `$$` substitutes `.` in a materialized column name |
| `attributes_bool['is_error']` | `attribute_bool_is_error` | same |

Each materialized column has a companion `attribute_<type>_<key>_exists` of type `Bool`. Test that
rather than `mapContains(attributes_string, 'key')` when the materialized column exists, because the
`_exists` column is a stored value and `mapContains` is a per-row map scan.

A key with no materialized column is still reachable through the map, and
`mapContains(attributes_string, 'container_name')` is the correct existence test there.

Resource attributes read as `resource.service.name::String`. **The `resource` JSON column caps
distinct dynamic paths at 100** (`MaxDynamicPaths: 100` in the schema migrator, identically for
traces). Resource attributes beyond that cap land in the shared dynamic store and are read more
slowly. Do not assume `resource.anything::String` performs like a column on an install with wide
resource attributes; confirm with `DESCRIBE`.

Convert time for display with `fromUnixTimestamp64Nano(timestamp)`, and bucket with
`toStartOfInterval(fromUnixTimestamp64Nano(timestamp), INTERVAL 1 MINUTE) AS ts`.
