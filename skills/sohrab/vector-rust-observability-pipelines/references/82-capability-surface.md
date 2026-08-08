# The capability surface at the pin

`80-version-and-upgrade-deltas.md` records what **breaks** on the way to the pin.
This file records what the pin can **do**. An agent holding only the breaking
changes will not reach for a component that has existed since 0.54.0, and will keep
recommending options 0.57.0 deprecated.

Scope: additions and deprecations across `0.54.0` → `0.57.0`, taken from the four
release pages, the `/highlights/` index, and the `0.55.0` and `0.57.0` upgrade
guides. Every row is version-tagged. **Absence from these tables is absence from
those pages, not evidence a capability does not exist.**

## New components

| Kind | Component | Added | Note |
| --- | --- | --- | --- |
| source | `windows_event_log` | 0.55.0 | Native Windows Event Log API; pull-mode subscriptions, bookmark checkpointing, field filtering |
| sink | `azure_logs_ingestion` | 0.54.0 | The replacement for the deprecated `azure_monitor_logs` |
| sink | `databricks_zerobus` | 0.56.0 | Databricks Unity Catalog via Zerobus; OAuth 2.0, schema fetched from Unity Catalog, protobuf batches |
| transform | `delay` | 0.56.0 | Fixed delay per event, or conditional including via VRL |

No new component is stated on the fetched 0.57.0 pages.

## VRL

| Change | Version |
| --- | --- |
| `parse_yaml` — new, YAML 1.1 | 0.54.0 |
| `encode_csv` — new | 0.55.0 |
| `to_entries` / `from_entries` — jq-compatible behaviour, key/value aliases | 0.55.0 |
| `flatten` — `except` parameter to exclude keys | 0.55.0 |
| String literals — `\u{HEX}` unicode escapes | 0.56.0 |
| `parse_regex` — dynamic, non-literal patterns | 0.56.0, continued in VRL v0.34.0 with 0.57.0 |
| `encode_proto` — scalar coercion, `allow_lossy_string_coercion`, integer and boolean map keys | 0.56.0 |
| Compiler — all unhandled errors reported in one pass; `else` may open a new line after `}` | 0.56.0 |
| `parse_cef` — new `strict` parameter, default `true` | 0.57.0 |
| Panic fix on lines ≥ 65535 bytes in `parse_key_value`, `parse_cef`, `decode_mime_q`, `parse_ruby_hash` | 0.57.0 |

**`parse_cef`'s `strict: true` default is a behaviour change wearing an additive
label.** Input that parsed leniently before can now be rejected. Upstream does not
list it as breaking; treat it as one for any config already parsing CEF.

## New config keys on existing components

| Key | Component | Added |
| --- | --- | --- |
| `request.retry_strategy` | HTTP-based sinks, generally — chooses which response codes retry. **Nests under `request:`**; rejected at a sink's top level, observed on 0.57.0 | 0.56.0 |
| Array, Map and Tuple support under `arrow_stream` | `clickhouse` | 0.54.0 |
| UUID mapped to Arrow `Utf8` | `clickhouse` | 0.55.0 |
| `healthcheck.uri`, custom headers via `request.headers` | `prometheus_remote_write` | 0.54.0 |
| `compression: zstd`, string syntax | `vector` sink | 0.56.0 |
| `routing.endpoints` — `load_balance`, `failover`, `failover_primary`; `keepalive.interval_secs`, `keepalive.timeout_secs` | `vector` sink | 0.57.0 |
| Custom auth strategy writes metadata, enriching the event | `http_server` | 0.56.0 |
| `internal_metrics.include_extended_tags` | `tag_cardinality_limit` | 0.54.0 |
| `exact_fingerprint` mode | `tag_cardinality_limit` | 0.57.0 |
| Opt-in temperature collector | `host_metrics` | 0.57.0 |
| `measure_cpu_usage: true` | **transforms only** — enables the CPU counter below. Observed on 0.57.0: rejected on a sink (`x unknown field 'measure_cpu_usage', expected one of 'print_interval_secs', 'rate', 'acknowledgements'`, exit 78), accepted on a `remap` transform | 0.57.0 |
| `buffer_utilization_ewma_half_life_seconds` **replacing** `buffer_utilization_ewma_alpha` | buffer observability — breaking, see `80-version-and-upgrade-deltas.md` | 0.54.0 |

## CLI

| Flag / variable | Default | Added |
| --- | --- | --- |
| `--dangerously-allow-env-var-interpolation` / `VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION` | off | 0.57.0 |
| `--chunk-size-events` / `VECTOR_CHUNK_SIZE_EVENTS` | `1000` events | 0.57.0 |
| `--max-decompressed-size-bytes` / `VECTOR_MAX_DECOMPRESSED_SIZE_BYTES` | 100 MiB | 0.57.0 |
| `--internal-logs-source-rate-limit` / `VECTOR_INTERNAL_LOGS_SOURCE_RATE_LIMIT` | not stated | 0.57.0 |
| `--raise-fd-limit` / `VECTOR_RAISE_FD_LIMIT` | not stated | 0.57.0 |
| `vector service --stop-timeout` (stop, uninstall) | not stated | 0.55.0 |
| `vector top` / `vector tap` over gRPC — drop the `/graphql` URL suffix | — | 0.55.0 |
| `vector top` scroll, sort and filter keybinds (`?` lists them) | — | 0.54.0 |
| `vector vrl --quiet` / `-q` — suppress the REPL banner. Spelling confirmed on 0.57.0: `vector vrl --help` prints `Usage: vector vrl [OPTIONS] [PROGRAM]` and `-q, --quiet` | — | 0.54.0 |

The last two 0.57.0 flags relevant to a relay topology are treated in
`35-pass-through-and-relay-paths.md`, which owns what they do and do not buy.

## New internal observability

| Metric | Kind | Added |
| --- | --- | --- |
| `component_latency_seconds` | histogram — time an event spends in one transform, including its buffer | 0.54.0 |
| `component_latency_mean_seconds` | gauge, same subject | 0.54.0 |
| `source_send_latency_seconds` | distribution | 0.55.0 |
| `source_send_batch_latency_seconds` | distribution | 0.55.0 |
| `component_cpu_usage_ns_total` | counter, **opt-in** via `measure_cpu_usage: true` on a **transform** | 0.57.0 |
| `component_errors_total{error_type="confinement_failed"}` | counter | 0.57.0 |
| `vector_security_confinement_disabled{component_type}` | gauge, `1` when confinement is off | 0.57.0 |
| `datadog_logs_reserved_attribute_conflicts_total` | counter | 0.57.0 |

Also 0.55.0: the `vector` source added gRPC health checking
(`grpc.health.v1.Health`). Which of these is worth an alert, and on what condition,
is `60-internal-monitoring.md`.

## Unit tests

`expected_event_count` on a test output, for asserting event emission — 0.56.0. The
verified schema key list is in `50-validation-and-testing.md`.

## Stop advertising these

| Deprecated or removed | Version | Use instead |
| --- | --- | --- |
| `azure_monitor_logs` sink | deprecated 0.54.0 | `azure_logs_ingestion`. The 0.54.0 notes give a deadline: migrate before Microsoft ends support for the old Data Collector API, scheduled at the time of writing for September 2026. Paraphrase — re-read the release page before quoting the date |
| Top-level `headers` on the `http` and `opentelemetry` sinks | **removed** 0.55.0 | `request.headers` |
| GraphQL API, `/graphql`, `/playground` | **removed** 0.55.0 | The gRPC API. `api.graphql` and `api.playground` are now rejected at config load — `80-version-and-upgrade-deltas.md` |
| Boolean `compression` on the `vector` sink | deprecated 0.56.0 | String syntax: `gzip`, `zstd`, `none` |
| `series_api_version: v1` on `datadog_metrics` | deprecated 0.56.0 | `v2`, already the default |
| `address` on the `vector` sink | deprecated 0.57.0 | `routing.endpoints` |
| `--disable-env-var-interpolation`, `VECTOR_DISABLE_ENV_VAR_INTERPOLATION` | **removed** 0.57.0 | `--dangerously-allow-env-var-interpolation` — `85-security-and-secrets.md` |

## The one quantified performance figure in the range

`parse_regex` and `parse_regex_all`, **4–13% speedup**, 0.56.0. That is the only
number stated across all four releases. 0.57.0's regex pre-computed capture-group
indices, its `truncate` `suffix` parameter, and its concurrent `parse_regex_all`
improvement carry **no** figure — do not supply one. Two regressions were also
fixed: metric-normalization sink CPU, present since 0.50.0 (0.56.0), and `file` /
`kubernetes_logs` CPU (0.55.0).

## What these sources do not say — and do not infer it

Every page in range fetched successfully, so nothing here is UNFETCHED. Everything
here is UNCONFIRMED in the sense that the pages are silent, which is not the same as
the pages denying it:

- **No release cadence, support window, or LTS statement** appears on the 0.57.0
  release page or its upgrade guide.
- **No 0.56.0 highlight article was located** on the `/highlights/` index; every
  0.56.0 row above comes from the release page alone.
- **No adaptive-concurrency change and no disk-buffer performance change** is stated
  in this range. The Adaptive Request Concurrency and Disk Buffer v2 highlights are
  dated 2020 and 2022, outside it.
- **No source-side never-block or backpressure-decoupling capability** is stated as
  new — `35-pass-through-and-relay-paths.md`.
- **No `http_server` source change** is stated: not `response_code`, `address`,
  decoding, framing, headers, `path_key`, `strict_path`, or acknowledgement
  behaviour. Two targeted passes over 0.57.0 returned nothing. Unstated, not
  unchanged.
- **No `prometheus_exporter` sink change and no internal metric rename** is stated
  in this range.
- **No minimum Rust, glibc, or Alpine version** is stated. 0.56.0 does record that
  RHEL 8, Rocky Linux 8, AlmaLinux 8 and CentOS Stream 8 support was restored after
  being broken in v0.55.0 by an unintended glibc requirement increase — so 0.55.0
  moved a platform floor without documenting it as a breaking change. Paraphrase, not
  a quotation. Check a platform floor against the binary, not against release notes.

Observed rather than read: the `timberio/vector:0.57.0-alpine` tag exists and pulls,
digest `sha256:19e3526faf4d4b1ed0c28a0d68d4cc3a1e13e437099986a5b7a768707907497c`,
build `0.57.0 (x86_64-unknown-linux-musl 8832452 2026-07-14 20:58:30)`, on
2026-08-08. The release pages do not address the `-alpine` tag either way.

All of the above reached this file through a summarising fetch rather than raw page
text. A claim that has to be exact gets re-read at its source: `90-source-map.md`.
