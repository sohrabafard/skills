# SigNoz Query Validation Checklists

Use this before finalizing ClickHouse SQL or docs-grounded guidance for a sensitive production system.

## 1. Surface check

- Query Builder/search syntax if the user is working in an Explorer.
- ClickHouse SQL only for dashboards or ClickHouse-backed alert surfaces.
- If the user asks for “the right docs page”, return docs first and do not invent SQL.

## 2. Signal/table check

- Logs: logs v2 table family.
- Traces: signoz index v3 table family.
- Metrics: `signoz_metrics` samples/time-series table family.
- Do not join across signal families unless the join key, time window, and purpose are explicit.

## 3. Time-bounds check

- Every query has a bounded time filter.
- Logs/traces include the bucket filter when the reference requires it.
- Metrics use millisecond macros and sample table `unix_milli` filters.
- Time windows are not accidentally widened by resource CTEs or fingerprint prefilters.

## 4. Output-shape check

- Timeseries returns `ts`, `value`.
- Value widget returns one numeric column named `value`.
- Table panels have labeled columns, deterministic ordering, and `LIMIT` where appropriate.

## 5. Safety and privacy check

- No secrets, credentials, raw payloads, emails, phones, national IDs, tokens, cookies, session IDs, or raw JWTs in example filters/output.
- No high-cardinality grouping unless the user explicitly needs a forensic table and the data is safe.
- Query examples use placeholders, not real customer identifiers.
- No destructive SQL, mutations, table drops, or database configuration changes.

## 6. Performance check

- Uses distributed tables expected by SigNoz.
- Filters by time before expensive map/JSON access when possible.
- Uses indexed/pre-extracted columns when available.
- Uses resource/fingerprint CTEs only when they reduce the scan.
- Includes `LIMIT` for exploratory/table queries.
- Avoids unbounded `LIKE '%...%'` over large log bodies without a narrow time range.

## 7. Schema uncertainty check

Before finalizing, state uncertainty or request schema inspection when:

- table names or macros are version-sensitive
- the user’s existing query references unknown columns
- metrics histogram or exponential histogram internals are involved
- SigNoz docs and live schema disagree
- a query will be pasted into a production alert/dashboard

## 8. Final answer template

```text
Surface: Dashboard ClickHouse | Alert ClickHouse | Query Builder | Docs lookup
Signal: logs | traces | metrics
Assumptions: ...
SQL/filter/formula: ...
Validation notes:
- time bounds: ...
- schema/table family: ...
- privacy/cardinality: ...
- unresolved uncertainty: ...
```
