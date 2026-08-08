# Monitoring Vector itself

Vector is a dependency of every incident review that reads a log, so it needs the
same treatment as a service. Verified against `0.57.0` on 2026-07-30.

## Wire both self-observation sources

```yaml
sources:
  vector_logs:
    type: internal_logs
  vector_metrics:
    type: internal_metrics
```

Ship them to a destination **that is not the one you are debugging**. Internal
metrics routed only through the failing ClickHouse sink disappear exactly when you
need them, which turns a partial outage into a blind one.

## Who owns which name

- **Vector's own internal metric names** are upstream's and are listed here.
- **Every Ala-side name** — log field names, event and code names, the `alaa_*`
  metric catalog, `OTEL_*` variables and their defaults — belongs to
  `/alaa-services-contract` (`$alaa-services-contract`). Do not invent one here.
- **Whether a signal is required, what gates on it, and why** belongs to
  `/alaa-observability-soc` (`$alaa-observability-soc`).
- **Every Ala threshold and budget value** belongs to `/alaa-services-contract`
  (`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md`.

This file names the Vector metric to watch and the condition that makes it
interesting. It does not set an Ala number.

## The metrics worth an alert, and the condition that matters

| Metric | Watch for | Why it is the discriminating signal |
| --- | --- | --- |
| `component_sent_events_total` | Rate falling to zero on a sink that previously flowed | Distinguishes "nothing is arriving" from "nothing is leaving" when compared against the source's counter |
| `component_received_events_total` | Burst shape at the source | Tells you whether a stall is inbound pressure or outbound failure |
| `component_errors_total` | Any sustained non-zero rate, by `error_type` | The default `retry_attempts` of `i64::MAX` means a failing sink logs no terminal error; this counter is the only evidence |
| `component_discarded_events_total` | Any non-zero value | Events deliberately dropped. On a fail-open path this is expected and must still be graphed, because it is the cost of the policy |
| `buffer_size_events`, `buffer_size_bytes` | Approaching the `max` counterpart | Saturation. The lead indicator for both a stall and a drop |
| `buffer_max_size_events`, `buffer_max_size_bytes` | The denominator | Utilisation is meaningless without it |
| `buffer_discarded_events_total` | Any non-zero value | Drops attributable to the buffer specifically, rather than to a transform |
| `source_buffer_utilization_mean`, `transform_buffer_utilization_mean` | Sustained rise | Moving averages added in 0.53.0; better for alerting than the instantaneous gauges, which are spiky |
| `component_latency_seconds`, `component_latency_mean_seconds` | One transform's latency rising while its input rate is flat | Time an event spends in a single transform **including that transform's buffer**. Histogram and gauge respectively, both added in 0.54.0. Separates a slow VRL program from a downstream stall |
| `source_send_latency_seconds`, `source_send_batch_latency_seconds` | Rise at a source that previously handed off instantly | How long the source takes to hand events on. Added in 0.55.0 — `35-pass-through-and-relay-paths.md` |
| `component_sent_events_total` at a source against `component_received_events_total` at its sinks | A widening gap | The backlog, wherever it is parked. Buffer gauges report only what is inside a buffer; a 0.57.0 run showed 200 out of a source and 2 into the sink with nothing dropped. Do not rely on buffer utilisation alone — `35-pass-through-and-relay-paths.md` |
| `component_cpu_usage_ns_total` | One transform dominating | **Opt-in, and transforms only:** set `measure_cpu_usage: true` on the *transform*. Added 0.57.0. Observed on 0.57.0: on a sink it is rejected — `x unknown field 'measure_cpu_usage', expected one of 'print_interval_secs', 'rate', 'acknowledgements'`, exit 78; on a `remap` transform it loads clean. There is no sink-side equivalent |
| `vector_security_confinement_disabled` | Equal to `1` | A sink is running with routing-template confinement turned off |
| `component_errors_total{error_type="confinement_failed"}` | Any non-zero value | A template rendered outside its confinement base at runtime |
| `vector_started_total`, `vector_stopped_total` | Repeated increments | Restart loop. A disk-buffer volume filling produces exactly this |

**Free disk space on the `data_dir` volume is not a Vector metric and is the most
important thing to alert on when disk buffers are in use.** Vector exits when it
cannot write, so this is a process-liveness dependency. Take it from the node
exporter or the platform, not from Vector.

## Alert on the derivative, not the level

A buffer at 80% is normal during a burst and alarming if it has been climbing for
ten minutes. Two conditions worth encoding:

- `buffer_size_bytes / buffer_max_size_bytes` rising monotonically across a window
  longer than your longest expected burst → the sink is not keeping up.
- `component_discarded_events_total` increasing while
  `component_received_events_total` is flat → dropping without a load increase,
  which means the sink degraded rather than the input growing.

Requirement levels, burn rates and the question of what pages a human belong to
`/alaa-observability-soc` (`$alaa-observability-soc`).

## The 0.53.0 metric migration, stated correctly

The previous version of this file named two renames and gave the **old** name
wrongly in both, so an agent following it grepped for names that never existed,
found nothing, and reported the migration clean. The correct list:

| Current name | Deprecates |
| --- | --- |
| `buffer_max_size_bytes` | `buffer_max_byte_size` |
| `buffer_max_size_events` | `buffer_max_event_size` |
| `buffer_size_bytes` | `buffer_byte_size` |
| `buffer_size_events` | `buffer_events` |

All four are one family. Migrating only the byte-sized pair leaves the event-sized
pair broken.

**The old gauges still exist for a transition period.** So a dashboard can read a
deprecated name indefinitely without erroring, and finding the old name proves
nothing about whether the new one is wired. Search for both, migrate to the new
name, and only then remove the old.

**Internal histogram buckets went from 20 to 26**, across all internal histograms.
Confirmed live on 0.57.0: 26 buckets, smallest upper limit exactly
`0.000244140625` (2⁻¹²), largest finite `4096`, then `inf`. Any alert or VRL program
that indexes buckets positionally must be re-derived; anything using quantiles is
unaffected.

Full detail and re-derivation commands: `80-version-and-upgrade-deltas.md`.

## One metric is emitted twice, with different tags

`http_client_rtt_seconds` is emitted **both** as a global series with no
`component_id` tag **and** once per sink carrying `component_id`,
`component_kind` and `component_type`. Observed live on 0.57.0 with two ClickHouse
sinks: three series, one untagged and one per sink.

Two consequences:

- A filter or allowlist keyed on `component_id` **still matches** the per-sink
  series. It does not silently lose the metric.
- **Do not sum across the family, and do not assume the untagged series aggregates
  the tagged ones.** In the observed run it does not: the untagged series recorded
  two observations, both in the `≤0.00390625` bucket, summing to `0.0064`, while the
  two per-sink series recorded one observation each with sums of `0.0100` and
  `0.0055` — above that bucket. It is measuring different requests. What it measures
  was not determined here, so treat the untagged series as an unidentified third
  signal and select explicitly on the presence or absence of `component_id`.

Verified on `timberio/vector:0.57.0-alpine`, digest
`sha256:19e3526faf4d4b1ed0c28a0d68d4cc3a1e13e437099986a5b7a768707907497c`, build
`0.57.0 (x86_64-unknown-linux-musl 8832452 2026-07-14 20:58:30)`, 2026-08-08,
against a live ClickHouse. Whether other upstream metrics share this dual-emission
shape was not surveyed — check the one you are filtering on before assuming either
way.

## Startup policy

`--require-healthy` is a flag on the **root** `vector` command, not on `validate`:

```bash
vector --require-healthy --config /etc/vector/vector.yaml
```

*"Exit on startup if any sinks fail healthchecks."* Choose deliberately, because the
two options fail in opposite directions:

- **With it:** a rollout will not proceed while a downstream is unhealthy. Correct
  for an audit-grade path, where starting without the destination means losing
  records.
- **Without it:** Vector starts and retries while the sink recovers. Correct for a
  fail-open product-telemetry path, where refusing to start is a worse outcome than
  degraded telemetry.

The choice follows the delivery contract for the path, which is written once in
`10-topology-and-delivery-contract.md` and constrained by
`/alaa-observability-soc` (`$alaa-observability-soc`).
