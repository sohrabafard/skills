# The Ala watch-time ingest pipeline

`wa` is the fleet's only Vector deployment and its only ClickHouse. It is also the one
Vector path in the fleet where the fail-open telemetry rule does not apply, and the
reason is not a Vector fact — it is what the data is for.

Measured against the `wa` working tree at commit `5bbe3c2` on 2026-07-30. Every number
below has a re-derivation command in the last section. Run the command before repeating
the number anywhere else.

## The ruling, and why it changes the category of the data

The owner ruled on 2026-07-30 that **the counts in `wa_raw` must be exact**. The ruling
is recorded in `<repo>/docs/DECISIONS.md` §29, which calls `wa_raw` a commercial record
rather than an approximate analytics store. Watch-time is therefore **product data, not
telemetry** — and it is that classification, not the fact that Vector is the process
moving it, that decides the pipeline's failure behaviour.

This has to be said out loud here, because the general rule points the other way.
`/alaa-observability-soc` (`$alaa-observability-soc`) binds the fleet to fail-open for
product traffic, and `30-buffers-acks-and-backpressure.md` names the Vector option that
expresses it. An agent arriving at this pipeline holding that rule and nothing else will
set `when_full: drop_newest` on a billing record and will be able to cite a rule for it.
SOC's rule governs telemetry *about* the product. It does not reach a table whose counts
*are* the product.

**Do not decide this by which tool moves the data.** Use the discrimination rule that
`/alaa-reliability-sla` (`$alaa-reliability-sla`) owns at its `SKILL.md:18-30`: when this
dependency cannot answer, does proceeding without it let something through that must not
get through? Answer it per path, and one Vector process answers it twice:

| Path | Can it proceed without the destination? | Class | Direction |
| --- | --- | --- | --- |
| A service's own logs, metrics and traces to SigNoz | Yes — the request already happened, and a lost span costs visibility | Contributor | Fails open. Drop, count the drop, never block the producer. |
| Watch-time events into `wa_raw` under the exactness ruling | No — a success code for an event that was never stored lets an under-count through, and the under-count is billed | Gate | Fails closed. Refuse the event rather than accept one that will not land. |

One pipeline, two answers, decided by what the data is for and not by which tool carries
it. Three boundaries hold around that ruling, and none of them belongs to this file:

- **Whether a signal is required at all, and at which gate:**
  `/alaa-observability-soc` (`$alaa-observability-soc`).
- **Why a fail-open or fail-closed mechanism exists and how to choose its shape:**
  `/alaa-reliability-sla` (`$alaa-reliability-sla`). It states no Ala number.
- **Every Ala value** — tolerable outage duration, retry budget, request deadline:
  `/alaa-services-contract` (`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md`.

This file owns one thing: which Vector option expresses the chosen shape on this
pipeline, and what this pipeline does when ClickHouse is unreachable.

## The topology, as measured

```text
wa_ingest_http           http_server, 0.0.0.0:8686, POST /ingest/v1/events, response_code 202
 └ parse_envelope        remap; aborts the whole batch on a missing X-Project-Id or X-Request-Id
    └ explode_events     remap; `. = unnest!(.events)` — one request becomes N events
       └ normalize_rows  remap; one flat 60-field row per event, plus identifier_format_invalid
          └ route_events route; event_type == "watch_segment" on one leg, != on the other
             ├ clickhouse_watch_segments_raw  ->  wa_raw.watch_segments_raw
             └ clickhouse_events_raw          ->  wa_raw.events_raw

 parse_envelope.dropped  ┐
 explode_events.dropped  ├  log_to_metric counters only. No dead-letter sink. Rule 5.
 normalize_rows.dropped  ┘

 vector_internal_metrics -> select_internal_metrics -> rename_internal_metrics  ┐
 count_normalized_rows, count_rejected_batches, count_rejected_events           ├ prometheus_exporter :9598
                                                                               ┘
 vector_internal_logs + vector_internal_metrics -> console sink on stderr
```

Both ClickHouse sinks carry identical settings, and they are the settings the rest of
this file argues about:

| Setting | Value on both sinks | Where the argument is |
| --- | --- | --- |
| `buffer` | `type: disk`, `max_size: 4294967296`, `when_full: block` | Rules 1 and 2 |
| `acknowledgements.enabled` | `true` on both sinks, absent on the source | Rule 2 |
| `batch` | `max_events: 5000`, `max_bytes: 10485760`, `timeout_secs: 2` | Complexity, below |
| `request` | `concurrency: 4`, `retry_attempts: 20`, `retry_initial_backoff_secs: 1`, `retry_max_duration_secs: 90` | Rule 3 |
| `skip_unknown_fields` | `true`, with its reason in a config comment | Immediately below |
| `format`, `compression` | `json_each_row`, `gzip` — both explicit | Nothing. This is the correct shape. |

4 GiB is sixteen times the 268435488-byte floor that
`30-buffers-acks-and-backpressure.md` records, so it is a chosen size rather than the
smallest legal one. `retry_attempts: 20` is finite, which is also the correct shape:
the Vector default is effectively infinite and never surfaces a dead sink as an error.

`skip_unknown_fields: true` here is the narrow exception `40-clickhouse-sink.md`
describes, not a defect. `normalize_rows` emits one row shape, `route_events` splits that
shape across two tables with different column sets, so each sink is always handed columns
its own table does not declare. **Do not remove it** — ingestion into
`wa_raw.watch_segments_raw` stops on the first event. Its cost stays real: a column added
to the row but not to the table is dropped server-side with no error, so a field-sync
check in CI, not the sink, is what keeps the two in step.

**Two byte-identical copies, enforced.** The config is `<repo>/vector/wa-vector.yaml`,
745 lines, with a byte-identical copy at `<repo>/charts/wa/files/wa-vector.yaml`. A CI job
named `vector_config_sync` runs `cmp -s` over the pair at the lint stage, so every edit
lands in both files in the same commit or the pipeline fails. That job is the reason the
Helm-rendered Vector and the Compose-run Vector cannot silently diverge, and it is a
pattern worth copying wherever a config has to exist twice.

**Where this file's seam begins.** The public edge is `POST /wa/ingest/v1/events` on the
gateway: unauthenticated, matched by a path-prefix ACL, rewritten, and forwarded to
`wa:8686` under the gateway's `timeout server 30s`, with no rate limiting in the rendered
configuration. `/alaa-haproxy` (`$alaa-haproxy`) owns every one of those directives, and
no proxy configuration is written from here. This file's half starts at the TCP
connection: the source's `response_code`, what has actually happened to the event by the
time that code is emitted, and how long the source may hold the request open. The two
halves have to be read together, and rule 2 is where they meet.

**The read side does not touch these tables.** `wa-api` reads only `wa_agg.*` — four
rollup tables behind five materialized views, defined in
`<repo>/clickhouse/ddl/002_agg.sql` — through the shared kit's `chkit` client, whose
`chkit/doc.go:16` forbids request paths from reading raw event tables. The sinks write
only `wa_raw`, the API reads only `wa_agg`, and they share no table. That split is why
rule 3's duplicates are not contained by the sinks alone.

## Five rules, and the pipeline that is their evidence

Every rule below is general and portable. The instance is cited as its evidence, and the
instances are being fixed under separate change requests filed against `wa`. Read the
rule and apply it to the pipeline in front of you; the citation is not a task list.

### 1. A durable buffer on ephemeral storage is not a durable buffer

A disk buffer's guarantee is bounded by the volume beneath it, and the two facts live in
different files — the buffer in the Vector config, the volume in the workload manifest.
State the volume's lifetime beside the buffer's `max_size` and treat them as one decision.
When the volume does not outlive the process, the disk buffer is a throughput smoother,
and it must not be described as durable in the delivery contract, the runbook, or the
alert that watches it.

The loss lands in exactly the scenario the buffer exists for. The sink goes down, the
buffer fills over hours, an operator redeploys to fix the sink, and the redeploy discards
everything the buffer was holding. A buffer that behaves worst under precisely the
condition it was bought for is worse than no buffer, because it also removed the pressure
to build something else.

**In this pipeline.** `data_dir` is `/var/lib/vector`, and
`<repo>/charts/wa/templates/deployment.yaml:117-118` backs that mount with `emptyDir: {}`.
The 4 GiB disk buffer survives a sink outage and does not survive a rollout.
`70-helm-chart-operations.md` records the same trap as it appears in the upstream Vector
chart's `persistence` values; this is a bespoke chart, so the trap arrives with no
`persistence` key to notice it by.

### 2. Acknowledgement is end-to-end or it is nothing

Acknowledgement is a chain from sink back to source. A sink that acknowledges tells the
source the data is durable, and only the source can turn that into something a client
sees. Enabling it on the sinks alone changes no response any client receives: the
durability then exists in the config and not in the contract. Either enable it on the
source and the sinks together, or write in the delivery contract that the success code
means *accepted for parsing* and nothing more — and if the path is a gate, only the first
of those is available.

The honest cost belongs with the rule, because it is what makes this a decision rather
than an oversight. A source that waits for the acknowledgement holds the HTTP request
open until every sink confirms. Silent loss becomes visible backpressure, which is the
right direction, and the ingest endpoint can hang under sustained overload, which is a
genuine new failure mode. It needs a bounded request deadline in front of it and an
alert on buffer utilisation. The mechanism is `30-buffers-acks-and-backpressure.md`;
the deadline value is `/alaa-services-contract` (`$alaa-services-contract`)
`references/22-failure-load-and-deprecation-contract.md`.

**Do not read that cost as the only way the client can be slowed.** Acknowledgements
decide whether the *response* waits for durability; `when_full` decides what a full
sink buffer does, and `block` propagates backpressure toward the source from there.
They are separate settings, and this pipeline sets `block` on both sink buffers
independently of any acknowledgement decision. How far that propagation reaches, and
after how much traffic, is not established — `35-pass-through-and-relay-paths.md`
holds the conditions, the evidence, and the limits of what was measured.

**In this pipeline.** Both sinks set `acknowledgements.enabled: true`. The
`wa_ingest_http` source sets no `acknowledgements` key, and the file has no top-level
block, so `response_code: 202` is returned as soon as the body is decoded. Measured on
0.57.0 with ClickHouse unreachable, that path answered `202` in 3–15 ms across six
consecutive requests — the sinks' acknowledgements reach no client, exactly as the rule
says.

**What was actually run, because the committed config cannot be.** That measurement
used this config with two deviations: `api.graphql` and `api.playground` deleted, and
`VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true` set. Rule 4 below records why
each is required and the exit code without it. The measurement therefore describes the
topology, not the committed file, which does not start on 0.57.0 at all.

Under the exactness ruling this is the sharpest of the five: the client is told the
event was accepted, and a rollout, a drain, or the `emptyDir` of rule 1 can then
discard it with nothing anywhere recording that it was lost.

### 3. At-least-once delivery plus a non-deduplicating table equals duplicate rows

A sink that retries cannot distinguish "the insert failed" from "the insert succeeded and
the reply was lost", so it must retry, and a retry after an unseen success writes the rows
twice. No retry setting removes this; tuning only changes how often it happens.
**Exactness is won or lost at the table, not at the sink.**

ClickHouse's insert deduplication is enabled by default **only** for `Replicated*MergeTree`
engines. A plain `MergeTree` accepts the identical block twice and keeps both copies. A
pipeline whose delivery is at-least-once and whose table is a plain `MergeTree` therefore
has no exactness anywhere in it, whatever the sink config says.

The consequence the pipeline owner has to carry is one step further out: **a rollup built
on a duplicating table inherits the duplicates.** A materialized view fires per insert, so
a duplicated raw insert writes the rollup rows twice, and a deduplication strategy applied
to the raw table later does not retroactively correct rollup rows the view has already
written. Any exactness plan has two parts — stop new duplicates, and rebuild the affected
rollup ranges — and the second part is not optional.

Which engine or table setting delivers exactness is not this skill's decision.
`/clickhouse-performance-schema-ops` (`$clickhouse-performance-schema-ops`) owns engine,
sorting key and table settings, and `65-troubleshooting.md` already routes the
duplication-into-one-sink class there. What this skill owns is the pipeline's obligation:
state the delivery guarantee in the path's delivery contract, and file the exactness
requirement against the table owner rather than assuming a retry count makes it true.

**In this pipeline.** Both raw tables are plain `MergeTree`, with `ReplicatedMergeTree`
templates present but commented out, and no `non_replicated_deduplication_window` set. The
ClickHouse deployment is a single 24.8 node with no Keeper, so the replicated engines are
not reachable without infrastructure this repository neither owns nor can see. Both sinks
retry up to twenty times with a 90-second backoff ceiling at `concurrency: 4`, and `wa_agg`
adds four rollups behind five materialized views reading from those raw tables — so the
rollups sit downstream of the duplication.

### 4. A version pin is a dormant configuration change

A pinned version is not a frozen system. It is a set of upstream defaults you have not
adopted yet, and every release between the pin and current stable can change a default the
config depends on without changing one byte of the config. The change lands the moment the
pin moves. Before bumping a pin, read the release notes for **every** intervening release,
and enumerate the defaults the config relies on rather than the features you intend to use.

The dangerous ones are the defaults that fail open. A default that starts rejecting the
config is discovered at validate time. A default that starts assigning a different meaning
to the same text is discovered in production, or not at all.

**In this pipeline.** Vector is pinned to `0.53.0` in five places while current stable is
`0.57.0`; nothing has been bumped. Two dormant changes are waiting in that gap, and
running the unchanged config on a 0.57.0 binary shows both, in order:

1. `api.graphql: false` and `api.playground: false` are still in the config. 0.55.0
   rejects both at load: `x unknown field 'graphql', expected 'enabled' or 'address'`,
   exit 78. The config does not start.
2. Remove those two keys and the next load failure is the six `${VAR}` sites — endpoint,
   user and password on each of the two sinks. 0.57.0 disables interpolation by default,
   and the config fails with `x invalid uri character in 'sinks.clickhouse_events_raw'`,
   exit 78, **with and without the environment variables set**.

Both observed on `timberio/vector:0.57.0-alpine`, digest
`sha256:19e3526faf4d4b1ed0c28a0d68d4cc3a1e13e437099986a5b7a768707907497c`, 2026-08-08.

**So the bump does not silently authenticate with a literal `${CLICKHOUSE_PASSWORD}` —
it refuses to load.** The interpolated `endpoint` is format-constrained and aborts the
load before any credential is used, which is the tripwire
`85-security-and-secrets.md` rule 1 requires and this config happens to have.

The rule stands and the danger is undiminished: **a version pin is a dormant
configuration change**, and this one is holding two. What the loud failure removes is
the *silent* variant, not the change. CI would not distinguish them anyway: the
`vector_validate` job runs `vector validate --skip-healthchecks` with no
`--deny-warnings` on either copy, and it exports an empty `CLICKHOUSE_PASSWORD` first,
which makes a literal placeholder and a working credential produce the same result.
That is the evidence for the rule `50-validation-and-testing.md` already states — a
validate gate has to be able to see the defect class it is gating, or it reports clean
on the one thing it exists to catch.

### 5. A dropped-events counter is not a dead-letter queue

A counter answers how many events were rejected. It never answers which ones, or what they
contained, so nothing rejected can be re-driven, and a systematic rejection — one client
version emitting one malformed field — is indistinguishable in the metric from background
noise. On a telemetry path that is acceptable hygiene. Under an exactness requirement it is
a silent correctness hole: the total is knowably wrong, and unknowably wrong by how much.

The rule is not "add a dead-letter sink". It is that **an exactness requirement obliges a
recoverable record of every rejection, and where a security policy forbids storing the
rejected payload, that conflict is a decision for the two owners rather than something the
pipeline may leave open.** Name it as an open conflict in the delivery contract, with both
owners, instead of letting a counter stand in for the decision. A resolvable middle usually
exists — a bounded, redacted record carrying the identifiers and the rejection reason but
not the body, or rejecting at the edge before the event is accepted — and choosing between
them is a design decision, not a config change.

**In this pipeline.** Three `.dropped` outputs feed two `log_to_metric` counters,
`alaa_wa_ingest_batches_rejected_total` and `alaa_wa_ingest_events_rejected_total`, and
nothing else. The config states its reason and the reason is a real one: a rejected payload
is unvalidated input arriving on an unauthenticated public path, governed by
`<repo>/docs/contracts/wa/security/pii-logging-rules.md`, and the config instructs that
neither `.dropped` output be wired to a sink. So this is not an oversight. It is an
unresolved conflict between a security policy and an exactness ruling that post-dates it.
Whether unvalidated public input may be stored at all belongs to
`/alaa-security-review` (`$alaa-security-review`); what the exactness requirement demands
belongs to the owner and is recorded in `<repo>/docs/DECISIONS.md`. The pipeline's job is
to name the conflict in its delivery contract, not to settle it.

## Telling these tables apart from SigNoz's

`wa_raw` and `wa_agg` are fleet-owned databases, created by
`<repo>/clickhouse/ddl/001_init.sql` and `<repo>/clickhouse/ddl/002_agg.sql`. They are not
SigNoz's, and the distinction decides which skill answers a question about them.

`/alaa-signoz-clickhouse-docs` (`$alaa-signoz-clickhouse-docs`) owns how a **SigNoz-owned**
table is queried and states that those tables are vendor-owned and read-only to the fleet.
Its rules do not transfer here in either direction. A schema change to `wa_raw` is a change
this repository makes, not a request filed against a vendor. And SigNoz's tenancy posture —
one shared SigNoz, where everyone with access is authorised to see every tenant's telemetry
because seeing it is how they fix it — is a statement about SigNoz's own tables and is not
a licence to omit `project_id` from a `wa_agg` query.

The three-way ClickHouse boundary itself is stated once, in `40-clickhouse-sink.md`, and is
not restated here. What that statement leaves open, this file closes:
`/clickhouse-performance-schema-ops` (`$clickhouse-performance-schema-ops`) `SKILL.md:14-15`
assigns the DDL directory and the Vector topology writing into it to "the ingest-pipeline
repository". **In this fleet that repository is `wa`**, the same repository described above,
holding both `<repo>/clickhouse/ddl/` and `<repo>/vector/wa-vector.yaml`. An agent looking
for the owner of a `wa_raw` column type has now found it.

## The question this file deliberately does not answer

`batch.max_events: 5000` against `batch.timeout_secs: 2`, `retry_attempts: 20` against a
90-second ceiling, and whether a report scans a rollup or the raw table are all questions
about how a cost grows with the input, not about which Vector option exists. State the
bound the path must hold as ingest rate, event size and retention grow, then take it to
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`), which owns
complexity budgets and the method for deriving a bound from the system rather than from one
observed operating point. Measure the inputs first: `60-internal-monitoring.md` names the
metrics that supply them.

## Re-deriving every number in this file

Run these from the root of the `wa` checkout. A number repeated without its command is a
number that has already started going stale.

```bash
git rev-parse --short HEAD                                    # 5bbe3c2, the tree measured here
wc -l vector/wa-vector.yaml                                   # 745
grep -n 'acknowledgements' vector/wa-vector.yaml              # 2 hits, both sinks, none on the source
sed -n '374,435p' vector/wa-vector.yaml | grep -c '^        "'  # 60 flat row fields
grep -n '\${' vector/wa-vector.yaml                           # 6 interpolation sites, all in sinks
grep -rn 'emptyDir' charts/                                   # the volume behind /var/lib/vector
grep -n 'ENGINE = ' clickhouse/ddl/001_init.sql               # 2 live MergeTree, 2 commented Replicated
grep -c 'CREATE MATERIALIZED VIEW IF NOT EXISTS' clickhouse/ddl/002_agg.sql   # 5
grep -n 'clickhouse-server' docker-compose.yml                # ClickHouse 24.8, single node
grep -n 'vector validate' .gitlab-ci.yml                      # 2 calls, neither with --deny-warnings
grep -n 'cmp -s' .gitlab-ci.yml                               # the vector_config_sync byte-identity gate
grep -rn '0\.53\.0' --include='*.yml' --include='*.yaml' .    # 9 hits: 5 pins, 4 comments in the 2 copies
```

The five pin sites are `<repo>/.gitlab-ci.yml`, `<repo>/docker-compose.yml`,
`<repo>/docker-compose.swarm.yml`, `<repo>/charts/wa/values.yaml` and
`<repo>/charts/wa/Chart.yaml`; all five move together or the deployed Vector and the
validated Vector are different binaries.

Current upstream stable is not derived from this repository. Run
`node scripts/check-upstream-version.mjs`, which compares this skill's own pin against
upstream and exits 0 current, 1 drift, 2 could not run; the underlying command and the
`/releases/latest` trap it avoids are in `90-source-map.md`.
