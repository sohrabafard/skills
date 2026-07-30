# The ClickHouse sink

Verified against Vector `0.57.0` on 2026-07-30. Re-derive every default in this file
with `vector generate 'demo_logs//clickhouse'`, which prints what the installed
binary applies rather than what the docs describe.

## The three-way boundary

`clickhouse-performance-schema-ops` owns what a ClickHouse table must be — engine,
sorting key, partitioning, TTL, compression — for tables the fleet controls.
`alaa-signoz-clickhouse-docs` owns how a SigNoz-owned table is queried, and states
that those tables are vendor-owned and read-only to the fleet.
`vector-rust-observability-pipelines` owns what the pipeline writes into a
ClickHouse table and how it behaves when that table is unreachable, and decides no
schema.

Route accordingly: `/clickhouse-performance-schema-ops`
(`$clickhouse-performance-schema-ops`) for DDL, `ORDER BY`, part counts, merges and
retention; `/alaa-signoz-clickhouse-docs` (`$alaa-signoz-clickhouse-docs`) for
SigNoz-managed tables and their query surface. The counterparty has already written
its half: *"that skill owns what the pipeline writes, this one owns what the table
must be."*

Two seams, as rules:

1. **Writing into a SigNoz-managed table.** SigNoz's schema is the contract. The
   VRL in this pipeline produces exactly the columns SigNoz declares. A missing
   column is a schema-change request filed against SigNoz, never a workaround with
   `skip_unknown_fields`.
2. **Writing into a fleet-owned table.** The ingest-pipeline repository owns the
   DDL per `/clickhouse-performance-schema-ops`. The part-count and latency budget
   is that repository's rule; the `batch` and `buffer` settings that satisfy it are
   this skill's. When a sink produces too many parts, the fix is here — larger
   `batch.max_bytes` or a longer `batch.timeout_secs`, fewer and bigger inserts —
   not a schema change there.

**Tenancy.** All tenants report into one shared SigNoz, and everyone with access to
it is authorised to see every tenant's telemetry, because seeing it is how they fix
it. Sensitive projects get a separate SigNoz address selected by an environment
variable. **A tenant predicate is therefore not required on a SigNoz query**, and
`clickhouse-performance-schema-ops`'s mandatory-tenant-predicate rule does not
transfer to SigNoz-owned tables. This is stated rather than omitted so that an
agent who finds both rules can tell which one applies.

## Required and optional

`endpoint` and `table` are required. `database` is optional and defaults to the
server's default database. Everything else below has a default, and the default is
the value you get by saying nothing.

## Defaults, and what to set instead

| Option | Default (0.57.0) | Set it when |
| --- | --- | --- |
| `format` | `json_each_row` | Leave it unless you have measured a reason. Full enum: `json_each_row`, `json_as_object`, `json_as_string`, `arrow_stream`. |
| `compression` | see the note below | Always set it explicitly. |
| `date_time_best_effort` | `false` | Timestamps arrive as RFC3339/ISO8601 text. Sets `date_time_input_format=best_effort` server-side. |
| `skip_unknown_fields` | unset | Almost never — see below. |
| `insert_random_shard` | `false` | Writing to a distributed table and you want inserts spread without a sharding key. |
| `batch.max_bytes` | `10000000` | Tuning part counts. Larger batches mean fewer, bigger parts. |
| `batch.timeout_secs` | `1` | Trading ingest latency for fewer parts. |
| `healthcheck.enabled` | `true` | Leave enabled. |
| `request.timeout_secs` | `60` | |
| `request.retry_attempts` | `9223372036854775807` | **Always.** The default retries effectively forever, so a dead sink never becomes a terminal error. |
| `request.retry_initial_backoff_secs` | `1` | |
| `request.retry_max_duration_secs` | `30` | Ceiling on the backoff interval, not total retry time. |
| `request.concurrency` | `adaptive` | Pin it only when the destination has a hard concurrency limit that adaptive discovery keeps overshooting. |
| `acknowledgements.enabled` | `false` | The path is audit-grade and the source can acknowledge. |
| `dangerously_allow_unconfined_template_resolution` | `false` | Never, without a written security decision. |

**`compression` has a genuine upstream disagreement.** `vector generate` on 0.57.0
emits `compression: none`, while the component reference documents the default as
`gzip`. Because the two sources disagree, **set `compression` explicitly** and do
not rely on either answer. Supported values are `none` and `gzip`. Setting it
explicitly is the rule regardless of which default is correct, so the ambiguity
cannot change your pipeline's behaviour on an upgrade.

`request.adaptive_concurrency` sub-defaults, for the rare case they need tuning:
`initial_concurrency: 1`, `max_concurrency_limit: 200`, `decrease_ratio: 0.9`,
`ewma_alpha: 0.4`, `rtt_deviation_scale: 2.5`.

## `skip_unknown_fields` loses data silently

It sets `input_format_skip_unknown_fields` on the server, so a field the table does
not declare is **discarded without an error**. The insert succeeds, the row lands,
and the field is gone. That is an observability outage that hides itself.

Use it only when both are true: the destination schema is owned by someone else and
can change without notice, and losing an undeclared field is preferable to failing
the insert. Otherwise leave it off and let the insert fail loudly, then reconcile
the schema through the owner named in the boundary above.

## Templated `table` and `database` are confined as of 0.57.0

A templated identifier must carry a literal prefix. Observed on 0.57.0:

```
table: "{{ tenant }}"        -> exit 78, rejected before startup
table: "logs_{{ tenant }}"   -> exit 0
```

The rejection message names the fix: *"Add a static prefix to your template, or set
`dangerously_allow_unconfined_template_resolution: true` to opt out."* Take the
prefix, not the opt-out. Confinement is the mitigation for injection through a
routing field, and disabling it sets
`vector_security_confinement_disabled{component_type=...}` to `1` — a signal
someone will eventually have to explain.

`vector validate --no-environment` does **not** catch this. See
`50-validation-and-testing.md` for the flag set that does.

**Minimum version for a templated identifier is 0.57.0**, which is where the
ClickHouse SQL-injection fix landed: `database` and `table` are now passed as query
parameters with the `Identifier` type rather than escaped client-side. On an
earlier version a templated identifier is an injection surface with no confinement
to bound it. Details in `80-version-and-upgrade-deltas.md`.

## Arrow stream is beta

`batch_encoding.codec = "arrow_stream"` exists and is marked **beta** upstream;
`format: arrow_stream` is the other route to the same encoding. Neither is a
default choice.

Adopt it only when all of these hold: the schema is stable and tightly controlled,
you have measured a throughput or CPU problem that batching did not solve, and you
have validated the destination's behaviour in staging with production-shaped data.
Keep `format: json_each_row` reachable as a one-line rollback, because an encoding
problem under load is not the moment to design a fallback.

## Authentication

`auth.strategy` accepts `basic`, `bearer`, `aws`, and `custom`. Credentials come
from a `secret:` backend referenced as `SECRET[backend.key]`, never from `${VAR}`
interpolation — on 0.57.0 that interpolation is off by default and a
`${CLICKHOUSE_PASSWORD}` literal passes validation and then fails authentication at
runtime. The full rule is in `85-security-and-secrets.md`.

Set `tls.verify_certificate: true` explicitly. Trust-boundary review for a new
external destination belongs to `/alaa-security-review` (`$alaa-security-review`).

## When ClickHouse is unreachable

The full chain — retry, backoff, buffer fill, `when_full`, and the disk-full hard
stop — is in `30-buffers-acks-and-backpressure.md`. It is one file rather than two
because the sink's retry behaviour and the buffer's `when_full` value are a single
decision with two halves.
