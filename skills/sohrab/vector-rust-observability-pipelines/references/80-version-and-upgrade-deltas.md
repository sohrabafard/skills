# Version pins and upgrade deltas

Every pin below carries the command that re-derives it. A version written in a file
goes stale silently; a re-derivation command beside it does not.

```
PIN vector = 0.61.0
PIN helm-chart = 0.61.0
```

`scripts/check-upstream-version.mjs` reads those two `PIN` lines from this file and
compares them to upstream, so this document and the checker cannot disagree.
Run it with `node scripts/check-upstream-version.mjs`: exit 0 current, 1 drift,
2 could not run.

## Compatibility and evidence ledger (verified 2026-11-04)

| Surface | Evidence and scope |
| --- | --- |
| Latest stable product | [Vector 0.61.0](https://vector.dev/releases/0.61.0/), [published tag](https://github.com/vectordotdev/vector/releases/tag/v0.61.0) at 2026-10-29 16:51:24 UTC |
| Refresh interval | `(0.58.0, 0.61.0]`: 0.59.0, 0.60.0 and 0.61.0. Apply the migration checks below in order. |
| Bundled VRL | [0.38.0](https://github.com/vectordotdev/vrl/releases/tag/v0.38.0), 2026-10-28 |
| Released chart | [vector-0.61.0](https://github.com/vectordotdev/helm-charts/releases/tag/vector-0.61.0), published 2026-10-29 17:12:11 UTC. [Chart.yaml](https://raw.githubusercontent.com/vectordotdev/helm-charts/vector-0.61.0/charts/vector/Chart.yaml) declares appVersion `0.61.0-distroless-libc` and Kubernetes `>=1.28.0-0`. Check source-specific support separately. |
| Compatibility | Older consumer migration notes and dated 0.57.0 measurements still apply in their stated scope. No upstream LTS or support window established. |
| Binary evidence | Cached 0.61.0 Alpine config and unit checks are separate from released-source guidance. Consumer version, deployed chart overrides, delivery, and production behavior require their own evidence. |

The full item-by-item coverage, including VRL and justified omissions, lives in
`81-release-coverage.md`. Read it when auditing refresh completeness. Read
`82-capability-surface.md` when choosing an optional capability.

## Re-deriving the pins

Select the numeric maximum among published, non-draft, non-prerelease `vX.Y.Z`
product releases; exclude `vdev`, nightly and suffixed candidate tags. The checker
walks at most five API pages and returns exit 2 if the inventory is incomplete.

```bash
curl -s 'https://api.github.com/repos/vectordotdev/vector/releases?per_page=100' \
  | jq -r '.[] | select(.draft == false and .prerelease == false) | select(.tag_name | test("^v[0-9]+\\.[0-9]+\\.[0-9]+$")) | "\(.tag_name) \(.published_at)"'
```

The command shows one page only; use the checker for bounded inventory and numeric
ordering. **Do not use `/releases/latest` for this repository.** On 2026-09-26 it
redirected to [vdev-v0.3.24](https://github.com/vectordotdev/vector/releases/tag/vdev-v0.3.24),
the tag of the `vdev` developer tool that lives in the same repository, not a
Vector release. A resolver that trusts it reports the wrong product, and every version
comparison downstream is then wrong in the direction that looks safe.
`scripts/check-upstream-version.mjs` rejects `vdev-*` tags.

Resolve chart releases separately with the `vector-X.Y.Z` pattern and the same
publication filters, then read `Chart.yaml` at that released tag. Neither a raw
Cargo tag probe nor mutable `master`/`develop` proves a stable release. On a fetch
failure, keep proof unavailable; do not guess downward through version numbers.

```bash
curl -fsS https://raw.githubusercontent.com/vectordotdev/helm-charts/vector-0.61.0/charts/vector/Chart.yaml
```

The chart version and the Vector version are separate numbers and have drifted
apart before. Compare `appVersion` against the Vector release pin on every chart
bump: when they differ, a Helm-deployed pipeline runs a different Vector build
from a package-installed one, and a version-sensitive behaviour change lands in
one environment and not the other.

## Release line since the version this skill previously pinned

`0.53.0` 2026-01-27 · `0.54.0` 2026-03-10 · `0.55.0` 2026-04-22 ·
`0.56.0` 2026-06-03 · `0.57.0` 2026-07-14 · `0.58.0` 2026-08-26 ·
`0.59.0` 2026-10-06 · `0.60.0` 2026-10-19 · `0.61.0` 2026-10-29.

This file records what **breaks** across that line. What the pin can **do** — new
components, VRL, config keys, CLI flags, metrics, and the deprecations to stop
recommending — is `82-capability-surface.md`. Read it before concluding Vector
cannot do something.

## Migration from 0.58.0

| Release | Before moving this path |
| --- | --- |
| [0.59.0](https://vector.dev/highlights/2026-10-05-0-59-0-upgrade-guide/) | Nest Avro complex and logical type attributes inside the type object. Old complex schemas fail to load and shorthand logical types can silently become primitives. Require modern Datadog trace payloads. Check receiver support before adopting Datadog metrics series v3, or pin v2. For `kubernetes_logs` migrate off Kubernetes 1.31, regardless of the chart's install constraint. Replace source `http` with `http_server`, sink `greptimedb` with `greptimedb_metrics`, and boolean `vector` sink compression with `gzip` or `none` as appropriate. |
| [0.60.0](https://vector.dev/highlights/2026-10-19-0-60-0-upgrade-guide/) | Replace Datadog metrics series v1 with v3 (default) or v2. Set `version: "1"` or `version: "2"` on InfluxDB log and metric sinks. Remove fields for the other version entirely, including fields set to null. |
| [0.61.0](https://vector.dev/releases/0.61.0/#vector-sink-default-https) | Add an explicit scheme to both `address` and `routing.endpoints` on `vector` sinks. Scheme-less endpoints now select HTTPS. For an intentionally plaintext receiver use `http://`. For a TLS receiver validate its certificate chain and hostname on the target image. |

From 0.59.0, strict validation resolves secret backends and can execute helper
commands. Use `50-validation-and-testing.md` to stage validation safely.
Recompile VRL on each step using `20-vrl-transforms.md`. Check buffer recovery,
drain and rollback with the target version before changing a sink identity or
reusing a data directory. Use `30-buffers-acks-and-backpressure.md` for delivery
and `60-internal-monitoring.md` for loss signals.

## 0.58.0 migration decisions

Source: [released upgrade guide](https://vector.dev/highlights/2026-08-26-0-58-0-upgrade-guide/),
checked against its [tagged source](https://raw.githubusercontent.com/vectordotdev/vector/v0.58.0/website/content/en/highlights/2026-08-26-0-58-0-upgrade-guide.md).

| Affected configuration | Migration before upgrading |
| --- | --- |
| `azure_monitor_logs` | Removed. Move to `azure_logs_ingestion`; obtain Data Collection Endpoint/Rule configuration and map `endpoint`, `dcr_immutable_id`, `stream_name`, `auth`. A sink-type rename alone is insufficient |
| `buffer_byte_size`, `buffer_events` | Removed. Use `buffer_size_bytes`, `buffer_size_events`; monitoring owner: `60-internal-monitoring.md` |
| `http_server` or deprecated `http` source `encoding` | Removed. Replace with `decoding.codec` and `framing.method` using the table below |
| `influxdb_logs.namespace` | Removed. If `measurement` is already set, retain it; otherwise preserve the old name as `measurement: <old-namespace>.vector` |
| `type: logdna` | Removed alias; use `type: mezmo` |
| URI templates within or adjacent to hostname | Rejected at build time. Keep a static host and a literal `/` before dynamic path segments; security owner: `85-security-and-secrets.md` |
| Scheme-less `webhdfs.endpoint` | Now resolves as HTTPS. Specify the intended scheme explicitly; never disable certificate verification to hide a migration failure |

| Removed HTTP encoding | `decoding.codec` | `framing.method` |
| --- | --- | --- |
| `text` | `bytes` | `newline_delimited` |
| `json` | `json` | `bytes` |
| `ndjson` | `json` | `newline_delimited` |
| `binary` | `bytes` | `bytes` |

Sink endpoint validation also rejects empty, host-less and non-HTTP(S) URLs for
the components listed in the full release ledger. Missing schemes resolve as
HTTPS. Keep explicit schemes and hosts; do not extrapolate this component list
to every URI field or infer a new ClickHouse default.

Before upgrading an exactness path, read `30-buffers-acks-and-backpressure.md`:
some invalid records are now dropped while the process survives, and an
oversized disk record can still cause a source acknowledgement. This does not
change the fleet's loss policy or make that path exact. Rollback requires the
previous binary, matching config and dashboard queries; do not assume a changed
buffer on disk is downgrade-compatible without an authorized recovery test.

## The three 0.57.0 changes that change what you must write

### 1. Environment-variable interpolation is disabled by default

Upstream: *"Environment variable interpolation in configuration files is now
disabled by default."* Restore it with `--dangerously-allow-env-var-interpolation`
or `VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true`. The old
`--disable-env-var-interpolation` flag and `VECTOR_DISABLE_ENV_VAR_INTERPOLATION`
were removed.

**This fails open, which is why it gets its own rule.** A config containing
`password: ${CLICKHOUSE_PASSWORD}` still passes `vector validate` with exit 0 on
0.57.0, because any string is a valid password. The sink then authenticates with
the 22-character literal text `${CLICKHOUSE_PASSWORD}`. Nothing in the validation
step reports it. Observed directly on 0.57.0:

```
$ vector validate --no-environment p.yaml    # password: ${CLICKHOUSE_PASSWORD}
√ Loaded ["p.yaml"]
                 Validated
EXIT=0
```

Where the interpolated value must satisfy a format, the same change fails loudly
instead: `endpoint: ${CH_ENDPOINT}` gives `x invalid uri character` and exit 78 —
and it aborts the **whole config load**, so a password interpolated in the same file
never gets used. The breakage is silent only where every interpolated value is
format-unconstrained.

That asymmetry is the whole rule, and `85-security-and-secrets.md` rule 1 states it
once: which shapes of interpolation are safe, the three conditions that make an
environment variable a legitimate credential source, and the deprecation of
placeholders in structural positions.

### 2. Sink routing templates are confined

Upstream: *"Sinks that accept `{{ field }}` references in routing templates now
enforce a confinement boundary: the rendered value must stay within the literal
prefix declared in the template."* Templates with no literal prefix are rejected.
The per-sink opt-out is `dangerously_allow_unconfined_template_resolution: true`,
and setting it raises `vector_security_confinement_disabled` to `1`.
`component_errors_total{error_type="confinement_failed"}` counts runtime failures.

Observed on 0.57.0 for a ClickHouse sink:

```
table: "{{ tenant }}"        -> exit 78: template references event fields (["tenant"])
                                but has no literal string prefix to derive a
                                confinement base from.
table: "logs_{{ tenant }}"   -> exit 0
```

**Rule:** every templated `table`, `database`, object key, file path, or HTTP
header value carries a literal prefix. This is a security control, not a style
preference — it is the fix for injection through a routing field.

**Historical 0.57.0 trap, fixed in 0.58.0:** *"`vector validate
--no-environment` doesn't catch unconfined routing templates."* See
`50-validation-and-testing.md` for the flag set that does catch it.

### 3. ClickHouse SQL injection fixed

Upstream: *"Fixed SQL injection via identifier names in the `clickhouse` sink.
The `database` and `table` config values are now passed as ClickHouse query
parameters with the `Identifier` type (`{database:Identifier}.{table:Identifier}`),
letting the server handle quoting rather than relying on client-side string
escaping."*

**Rule:** `0.57.0` is the minimum version for any pipeline whose ClickHouse
`database` or `table` is templated from event data. On an earlier version, a
templated identifier is an injection surface, and confinement does not exist
there to bound it either.

## 0.55.0 — the observability API moved from GraphQL to gRPC

The API moved from GraphQL to gRPC. This covers `vector top`, `vector tap`, and
anything that talked to `/graphql` or `/playground`.

**The consequence that breaks a config, and it is a hard startup failure.** The
0.55.0 material reports that configs containing `api.graphql` or `api.playground`
are rejected — a paraphrase, because it reached this skill through a summarising
fetch. It needs no quotation: the behaviour is directly observed on 0.57.0.

```
api:
  graphql: false        ->  x unknown field `graphql`, expected `enabled` or `address`
  playground: false         in `api`
                            EXIT=78
```

Setting either to `false` does not help — the field itself is unknown. Delete both.
This is not a tooling note to schedule; a config carrying either key does not start
on 0.55.0 or later.

**`GET /health` on the API port still answers `200 {"ok":true}` on 0.57.0** —
observed on a live 0.57.0 process with the API bound to `0.0.0.0:8687`, on
`timberio/vector:0.57.0-alpine`, digest
`sha256:19e3526faf4d4b1ed0c28a0d68d4cc3a1e13e437099986a5b7a768707907497c`, build
`0.57.0 (x86_64-unknown-linux-musl 8832452 2026-07-14 20:58:30)`, 2026-08-08. An
earlier reading of this had "the `GET /health` endpoint is unchanged" as an upstream
quote; it is not one, it was a summariser's paraphrase. The binary settles it, and
Kubernetes HTTP probes on `GET /health` need no change.

**Rule:** before upgrading past 0.55.0, delete `api.graphql` and `api.playground`,
and re-point anything other than `vector top` and `vector tap` that queries the
Vector API — a dashboard, a scrape job, a custom operator — at the gRPC API.

Also in 0.55.0: the top-level `headers` option was removed from the `http` and
`opentelemetry` sinks, and `azure_logs_ingestion` with Client Secret credentials
now requires `azure_credential_kind` to be set explicitly.

## 0.54.0 and 0.56.0

`0.54.0`: the `datadog_logs` sink defaults to `zstd` compression; set
`compression` explicitly to keep the previous behaviour. `0.56.0`: the
`greptimedb_metrics` and `greptimedb_logs` sinks require GreptimeDB v1.x.
Neither affects a ClickHouse pipeline.

**`0.54.0` also renamed a buffer-observability config key**, which does affect any
pipeline that tuned it: `buffer_utilization_ewma_alpha` was **replaced** by
`buffer_utilization_ewma_half_life_seconds`. Upstream states the
`*buffer_utilization_mean` metrics now use time-weighted averaging, *"more
representative of the actual buffer utilization over time"*, and that the key
replacement is what makes the change breaking. A config still setting the old key
must be migrated; a config that never set it needs no edit, but the metric it reads
is computed differently from 0.54.0 onward, so a threshold derived before that
release needs re-deriving. Those two metrics are the smoothed saturation signal in
`60-internal-monitoring.md`.

## 0.53.0 — the internal buffer metric renames

This is the migration the previous version of this skill stated wrongly. It named
two renames, gave the **old** name incorrectly in both, gave the bucket count
change as 10 to 26, and scoped it to one metric. An agent grepping dashboards for
the names it listed finds nothing, reports the migration clean, and leaves every
real deprecated name in place. The corrected list, verified against the 0.53.0
release notes:

| Current name | Deprecates |
| --- | --- |
| `buffer_max_size_bytes` | `buffer_max_byte_size` |
| `buffer_max_size_events` | `buffer_max_event_size` |
| `buffer_size_bytes` | `buffer_byte_size` |
| `buffer_size_events` | `buffer_events` |

All four are renames of the same family; a migration that handles only the two
byte-sized ones leaves the two event-sized ones broken.

**On the earlier release line the old gauges still exist.** Upstream: *"while keeping the old related gauges
available for a transition period."* That is what makes a safe migration
possible — dashboards can carry both names across one release, and the cutover
does not have to be atomic. It also means a grep that finds the old name proves
nothing about whether the new one is wired. In 0.58.0, `buffer_byte_size` and
`buffer_events` are removed; do not extend the transition promise to that version
or infer removal of the two old maximum-size names from this release note.

**Histogram buckets went 20 to 26, across all internal histograms**, not for one
metric. The smallest bucket is now approximately `0.000244` (2^-12). Upstream
warns that *"if you were manually indexing buckets using VRL, you have to change
your indexes"*. Alert thresholds derived from bucket indexes need re-deriving;
thresholds derived from quantiles do not.

Also added in 0.53.0, and useful for the saturation signal in
`60-internal-monitoring.md`: `source_buffer_utilization_mean` and
`transform_buffer_utilization_mean`, exponentially weighted moving averages of
buffer utilisation alongside the instantaneous gauges.

Re-derive this whole section:

```bash
curl -s https://raw.githubusercontent.com/vectordotdev/vector/master/website/cue/reference/releases/0.53.0.cue
```

## VRL metric helpers

`get_vector_metric`, `find_vector_metrics` and `aggregate_vector_metrics` were
added in 0.53.0 and still exist on 0.57.0. Verified 2026-07-30.
