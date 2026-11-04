# Release coverage decision record

## 0.59.0 through 0.61.0 refresh

The [0.59.0](https://raw.githubusercontent.com/vectordotdev/vector/v0.59.0/website/cue/reference/releases/0.59.0.cue),
[0.60.0](https://raw.githubusercontent.com/vectordotdev/vector/v0.60.0/website/cue/reference/releases/0.60.0.cue)
and [0.61.0](https://raw.githubusercontent.com/vectordotdev/vector/v0.61.0/website/cue/reference/releases/0.61.0.cue)
tagged notes cover this interval, including VRL 0.36.0, 0.37.0 and 0.38.0.
Read the migration decisions in `80-version-and-upgrade-deltas.md` before applying
these component-specific additions. These are released-source findings.

| Release | Relevant delta and owning guidance |
| --- | --- |
| 0.59.0 | Secret resolution in strict validation, malformed endpoints, more sink checks without environment, ambiguous test outputs, zero-rate blackhole rejection, and generated optional enum schema fixes. Keep the strict gate in `50-validation-and-testing.md`. |
| 0.59.0 | HTTP-prefix confinement fix and bearer auth on `http_server`, `heroku_logs` and `websocket_server`. Review TLS and credential sourcing in `85-security-and-secrets.md`. HTTP sources add `keepalive.tcp_keepalive`. OTLP source adds `max_concurrent_requests` and `request_timeout_secs`; test overload and producer behavior before setting them. |
| 0.59.0 | Native decode/disk record rejection and old buffer reporter retirement. See `30-buffers-acks-and-backpressure.md` and `60-internal-monitoring.md`. File and Kubernetes unread-byte metrics supplement EOF evidence. |
| 0.59.0 | Migrate deprecated counters to `memory_enrichment_table_failed_insertions_total`, `memory_enrichment_table_failed_reads_total`, `memory_enrichment_table_ttl_expirations_total`, `process_runtime_total` and `aggregate_failed_updates_total`. Also review Linux `memory_oom_kill_events_total` and Prometheus label exposition fixes. |
| 0.59.0 | JetStream resumes closed pull streams with backoff. File fingerprinting retries too-short files. gRPC decompression and TCP ack/TLS failures give more context. GELF caps incomplete message bytes and adds a configurable message-count cap. Lua metrics with invalid tag values now discard instead of panicking. These do not establish an Ala delivery guarantee. |
| 0.59.0 | Optional surfaces: Azure append blobs, Prometheus scrape headers, Loki custom healthcheck URI, event-time aggregation, Datadog span links/events and payload/truncation controls. Inspect tagged component docs before adoption. |
| 0.60.0 | Disk file-ID wrap and stale reload selection fixes. Sample limits per-group state with `max_state_bytes` (128 MiB by default), evicting least recently used groups. Internal log discards, optional sample/throttle discard groups, and Prometheus remote-write counter typing affect observation. See `60-internal-monitoring.md`. |
| 0.60.0 | Migrate OTLP source `use_otlp_decoding` to `decoding.codec: otlp` and check `decoding.signal_types`. Recheck native OTLP log event names and Kubernetes namespace annotations and label metadata. Source/sink task logs now report the underlying error. |
| 0.60.0 | Recheck package migration if using Debian conffiles or Kafka GSSAPI in the official Linux GNU package. Avro adds Date and TimeMillis codec support. These do not change the examples here. |
| 0.61.0 | Explicit relay schemes and proxy credentials/SNI. Unregistered services on `vector` and `opentelemetry` now return gRPC `UNIMPLEMENTED` without a component-error increment. Recheck top/tap connectivity and trust on the target build. |
| 0.61.0 | Disk lifecycle and decoder oversize-error signals. MQTT graceful shutdown drains queued messages and pending QoS exchanges before disconnect when possible. Redis list shutdown gives an in-flight pop up to five seconds to finish and forward its result. GCP Pub/Sub reset reconnect and TLS/proxy changes are provider-specific. |
| 0.61.0 | OpenSearch sink and Datadog Agent v3 metrics intake are optional. Recheck the trust chain after CA changes in distroless images, bundled Mozilla roots and the Databricks sink. |
| VRL | Compile array-element checks and nanosecond conversion on the chosen version. Review HTTPS certificate verification, `range`, and other stdlib changes in `20-vrl-transforms.md` and the tagged notes. |

No configuration changes are driven here by internal performance work, dev tools,
playground UI, platform packaging outside the target, or unrelated component
fixes. The shipped examples exercise the basic remap and ClickHouse config
surfaces. Provider integration, real TLS, chart rendering and upgrades,
buffer reload/drain, metric emission, backpressure, retry, and delivery require
their own checks on the actual target. The release ledger establishes no change
to the skill's default interpolation posture, health endpoint contract,
acknowledgement boundary, retry bounds, or ClickHouse schema policy.

## 0.58.0 historical coverage

Verified 2026-09-26. The canonical version/support ledger is
`80-version-and-upgrade-deltas.md`. This record covers the entire stable delta
after the skill's baseline: one product release, including its bundled VRL
changelog. Earlier migration guidance remains reachable; no consumer upgrade is
performed or required by this record.

Sources: [full tagged release source](https://raw.githubusercontent.com/vectordotdev/vector/v0.58.0/website/cue/reference/releases/0.58.0.cue),
[rendered release](https://vector.dev/releases/0.58.0/),
[tagged upgrade guide](https://raw.githubusercontent.com/vectordotdev/vector/v0.58.0/website/content/en/highlights/2026-08-26-0-58-0-upgrade-guide.md).
Rows follow the tagged changelog's order: 59 product entries and three VRL entries.
An owner below means the topic instruction or capability table adopts the delta;
it does not mean local runtime proof.

| # | Released delta | Owning reference / test or omission decision |
| --- | --- | --- |
| 1 | AWS connector HTTP metrics | `60-internal-monitoring.md`: inspect per-component request series |
| 2 | STS AssumeRole honors FIPS endpoint setting | `85-security-and-secrets.md`: authenticated egress regression cases |
| 3 | JSON/YAML explicit null loading fixed | `50-validation-and-testing.md`: changed parser cases |
| 4 | Azure Blob tags and metadata options | `82-capability-surface.md`: optional component additions |
| 5 | Redis channel reconnect/resubscribe with backoff and recovery metrics | `65-troubleshooting.md`: recovery regressions |
| 6 | Exporter expiration can be disabled | `82-capability-surface.md`: cardinality/memory caveat |
| 7 | Metric sink disk-buffer deadlock and zero-expiration panic fixed | `30-buffers-acks-and-backpressure.md`: recovery matrix |
| 8 | OTLP legacy trace decoding no longer adds timestamp | `82-capability-surface.md`: payload shape compatibility |
| 9 | Memory enrichment cuckoo filter | `82-capability-surface.md`: false positives exclude exact decisions |
| 10 | Memory enrichment bloom filter | Same owner and restriction as row 9 |
| 11 | Datadog Agent LLMObs input/output | `82-capability-surface.md`: optional component additions |
| 12 | Delimited frame truncation option | `82-capability-surface.md`: explicit loss choice, default drop preserved |
| 13 | Kubernetes merged-line truncation | Same owner; file-level oversize still drops |
| 14 | MQTT configured ALPN honored | `85-security-and-secrets.md`: authenticated egress regression cases |
| 15 | Untagged-enum generated schema fixed | `50-validation-and-testing.md`: schema versus binary evidence |
| 16 | No-environment validation catches confinement | `50-validation-and-testing.md`; the strict gate remains required |
| 17 | Hyphenated secret backend names resolve | `85-security-and-secrets.md`: retain portable non-hyphenated example |
| 18 | dnstap `httpProtocol` restored | `82-capability-surface.md`: payload shape compatibility |
| 19 | Loki label/metadata values no longer confined | `85-security-and-secrets.md`: exact field exceptions, keys/tenant remain confined |
| 20 | CloudWatch stream name no longer confined | Same owner; group name remains confined |
| 21 | Reduce NaN sum returns error instead of panic | `20-vrl-transforms.md`: arithmetic failure cases |
| 22 | Invalid Sematext token template returns config error | `50-validation-and-testing.md`: negative config cases |
| 23 | Custom auth VRL enrichment covers HTTP source family | `82-capability-surface.md`: namespace and non-overwrite caveat |
| 24 | S3 Requester Pays opt-in | `82-capability-surface.md`: optional component additions; no billing activation |
| 25 | S3 KMS template uses configured timezone | `85-security-and-secrets.md`: key-selection regression |
| 26 | Azure large account-key upload signing fix | Same owner: multipart/signing regression |
| 27 | Azure Monitor Logs removed | `80-version-and-upgrade-deltas.md`: full resource/config migration |
| 28 | Two legacy buffer gauges removed | `60-internal-monitoring.md`: compatibility query cutover |
| 29 | GELF pending limits and timeout cleanup fixed | `50-validation-and-testing.md`: boundary/malformed input matrix |
| 30 | GELF one-byte trace-log panic fixed | Same owner |
| 31 | Config errors include field path | Same owner; diagnostic matching avoids full-message pinning |
| 32 | Datadog V2 metric resource tags retained | `82-capability-surface.md`: payload shape compatibility |
| 33 | Disk crash recovery usage accounting fixed | `30-buffers-acks-and-backpressure.md`: recovery matrix |
| 34 | Oversized disk record drops instead of process teardown | Same owner: acknowledgement/loss caveat; `60-internal-monitoring.md` drop metrics |
| 35 | Disk writer progress notification ordering fixed | `30-buffers-acks-and-backpressure.md`: recovery matrix |
| 36 | Integer histogram upper limits deserialize | `82-capability-surface.md`: payload shape compatibility |
| 37 | GCP Stackdriver label templates unconfined | `85-security-and-secrets.md`: field-qualified exception |
| 38 | HTTP source encoding removed | `80-version-and-upgrade-deltas.md` |
| 39 | Influx logs namespace removed | `80-version-and-upgrade-deltas.md`: preserve effective measurement |
| 40 | Influx API version selector | `82-capability-surface.md`: optional now, future requirement unversioned |
| 41 | Kafka application-payload decompression | `82-capability-surface.md`: before framing, distinct from broker compression |
| 42 | Kubernetes path metadata fallback | Same owner: directory ID is not Pod UID |
| 43 | Explicit graceful component shutdown logs | `60-internal-monitoring.md`: diagnostic addition, no durability inference |
| 44 | LogDNA alias removed | `80-version-and-upgrade-deltas.md`: Mezmo migration |
| 45 | Logstash compressed-frame OOM and partial-frame loss fixed | `85-security-and-secrets.md`: hostile framing cases |
| 46 | Logstash declared frame size bounded | Same owner: decompressed-size limit retained |
| 47 | Automatic metric tag scalar/array shape | `82-capability-surface.md`: Lua exception |
| 48 | OTLP native metric serialization | Same owner: four documented metric kinds only |
| 49 | Deeply nested events rejected before buffer/send | `30-buffers-acks-and-backpressure.md`: drop/overflow distinction, no overflow authorization |
| 50 | HTTP proxy credentials no longer leak to origin auth | `85-security-and-secrets.md`: proxy/origin separation |
| 51 | Confinement-disabled gauge persists | `60-internal-monitoring.md`: older-version absence is not safety |
| 52 | Sink endpoint validation and scheme default | `80-version-and-upgrade-deltas.md`; affected components below |
| 53 | Optional source TLS handshake timeout | `85-security-and-secrets.md`: unset default still permits held slots |
| 54 | TLS server name applies to hostname verification | Same owner: proxy certificate host remains separate |
| 55 | URI authority templates rejected at build | Same owner |
| 56 | Non-numeric URI port gives validation error | `50-validation-and-testing.md`: changed parser cases |
| 57 | Split varint frame decoder corrected | Same owner: split-read regression case |
| 58 | WebHDFS scheme-less endpoint becomes HTTPS | `80-version-and-upgrade-deltas.md`: explicit scheme migration |
| 59 | Databricks Zerobus OTel v2 compatibility | `82-capability-surface.md`: optional component additions |
| VRL-1 | AWS VPC Flow Log fields v7-v11 | `20-vrl-transforms.md`: fixture selection by producer format |
| VRL-2 | `round` float result type corrected | Same owner: type assertions |
| VRL-3 | NaN-producing float arithmetic errors | Same owner: handled failure cases |

Row 52 affects `appsignal`, `azure_logs_ingestion`, `datadog_events`,
`datadog_logs`, `datadog_metrics`, `datadog_traces`, `elasticsearch`,
`gcp_cloud_storage`, `gcp_pubsub`, `gcp_stackdriver_logs`,
`gcp_stackdriver_metrics`, `honeycomb`, `humio`, `influxdb`, `loki`,
`prometheus_remote_write`, `sematext`, `splunk_hec`, and `webhdfs`.

**Deliberately omitted artifacts:** no runnable provider example for each optional
sink (credentials/resources and consumer versions are unknown); no crash, disk-full,
network, timing or throughput harness (runtime unavailable and no live workload
authorized); no claimed exactness or benchmark improvement from upstream fixes.
The table maps those changes to selection/migration/testing instructions instead.
Runtime versus offline proof is stated in `50-validation-and-testing.md`;
documentation coverage is not execution coverage.
