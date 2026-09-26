# Release coverage decision record

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
| 16 | No-environment validation catches confinement | `50-validation-and-testing.md`; existing confinement red fixture remains strict |
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
| 38 | HTTP source encoding removed | `80-version-and-upgrade-deltas.md`; `assets/fixtures/v0.58/` green/red encoding pair |
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
| 55 | URI authority templates rejected at build | Same owner; `assets/fixtures/v0.58/` red authority fixture |
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
Only the local configuration regressions and stable-release resolver receive new
fixtures. Their runtime versus offline proof is stated in
`50-validation-and-testing.md`; documentation coverage is not execution coverage.
