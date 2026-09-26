# Log body search and version gates

Read the [signal prerequisites](../clickhouse-logs-reference.md) before this topic.

## Released query behavior

Read `../90-versions.md` for the release gates: Query Builder `search()` and JSON body response
changes do not make `search()` a raw ClickHouse function. Inspect the stored body type and
version-specific extraction expression. Older installs retain the raw `body` path; keep its
bounded scan and label any index assumption unverified. A JSON path's existence does not
prove that historical rows populate it. The release's JSON parsing default is not permission
to expose customer text in a panel.

## Searching the body

`logs_v2` carries three body columns, and the difference between them decides whether a text search
scans or skips:

- `body` — the raw text. **No index.** A `LIKE '%needle%'` over `body` reads every row in range.
- `body_v2` — a ClickHouse `JSON` column with one typed path, `message String`, and
  `MaxDynamicPaths: 0`. It carries four skipping indexes: `ngrambf_v1(4, 15000, 3, 0)` and
  `tokenbf_v1(10000, 2, 0)` over its full-text expression, and the same pair over its paths
  expression.
- `body_promoted` — a `JSON` column holding paths promoted out of the record.

So: **express a body search against `body_v2` so the bloom-filter indexes can skip granules, and
keep `body` for display.** The ngram index is built at n=4, so a substring shorter than four
characters cannot use it and degrades to a full scan — search for a longer fragment, or a whole
token so the token index applies.

Confirm these columns exist first: they arrive with a SigNoz upgrade, an install behind it has only
`body`, and `scripts/check-signoz-schema.py` reports which are present.
