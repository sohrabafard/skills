# Troubleshooting by failure class

Each class below is symptom, then the command or metric that **discriminates**
between causes, then the smallest retry, then when to escalate. A list of nouns to
"inspect" is not a diagnosis, so every branch here names something you run.

The live inspector is `vector top`. Note that Vector's observability API moved from
GraphQL to gRPC in 0.55.0: `vector top` and `vector tap` were updated with it, but
anything else that queried `/graphql` was not. `GET /health` is unchanged.

```bash
vector top --url http://127.0.0.1:8686/   # live component throughput and errors
vector tap out_clickhouse                 # sample events entering a component
```

`vector top` needs the `api` block enabled (`api.enabled: true`); if it cannot
connect, that is the finding.

---

## Class 1 — the sink reports healthy but nothing arrives

**Discriminate on where the event count stops.** In `vector top`, read
`component_sent_events_total` for each component along the path:

- **Zero at the source** → the source is not matching. For `file`, check `include`
  globs and that the process can read the paths; checkpoints live under `data_dir`,
  so a stale checkpoint makes an already-read file look empty.
- **Non-zero at the source, zero after a transform** → the transform is dropping.
  A `remap` that aborts discards the event. Check
  `component_discarded_events_total` and `component_errors_total` on that transform,
  then reproduce with `vector vrl -i sample.json -o '<program>'`.
- **Non-zero into the sink, zero out** → delivery, not routing. Go to class 2.

**Smallest retry:** `vector tap <transform>` to see the actual event shape at that
point. Most "no data" incidents are a field name that differs from the assumption.

**Escalate** when the events reach the sink and the destination still shows nothing:
that is a destination-side question, and for a fleet-owned ClickHouse table it
belongs to `/clickhouse-performance-schema-ops`
(`$clickhouse-performance-schema-ops`).

---

## Class 2 — the pipeline stalls, and latency climbs upstream

This is `when_full: block` doing what it is configured to do.

**Discriminate on buffer fullness versus sink errors:**

- `buffer_size_events` / `buffer_size_bytes` rising to `buffer_max_size_events` /
  `buffer_max_size_bytes` → the buffer is full and the sink cannot drain it.
- `component_errors_total` on the sink rising at the same time → the sink is
  failing and retrying. With the default `retry_attempts` of `i64::MAX` it retries
  effectively forever, so there is no terminal error to find in the logs. This is
  the most common cause of a stall that "logs nothing".
- Buffer full, no sink errors → the destination is accepting data slower than it
  arrives. Increase `batch.max_bytes` before increasing concurrency: fewer, larger
  inserts are cheaper for ClickHouse than more, smaller ones.

**Smallest retry:** set `request.retry_attempts` to a finite value so the failure
becomes visible, and confirm the destination is reachable from the Vector host.

**The real decision:** if this path carries product telemetry, `block` is the
defect. The fleet requires fail-open for product traffic, which means
`drop_newest`. See `30-buffers-acks-and-backpressure.md`.

---

## Class 3 — Vector exited on its own

**Discriminate on the exit message, which names the cause:**

- `no storage space` or any I/O error during a disk-buffer flush → **this is
  designed behaviour.** Vector forcefully stops itself when it cannot guarantee a
  disk-buffer write, because it can no longer know what reached disk. Check free
  bytes on the `data_dir` volume, not buffer utilisation — another process
  consuming the same volume produces this too.
- Exit at startup complaining the disk buffers exceed the volume → the sum of every
  `max_size` is larger than the disk. Vector checks this at startup deliberately.
- Startup exit with unhealthy sinks and `--require-healthy` set → the flag is doing
  its job; the sink is genuinely unhealthy.

**Smallest retry:** free space and restart. Vector recovers the uncorrupted portion
of the disk buffer on restart.

**Escalate to capacity planning**, not to a config change, when free space is
adequate and this recurs: the volume is sized for the wrong outage duration. The
arithmetic is in `30-buffers-acks-and-backpressure.md`.

---

## Class 4 — data loss or duplication

**Discriminate on which one, because the causes are opposite:**

- **Loss, buffer was memory** → expected on any restart or crash; memory buffers
  are not durable. Also expected under burst with `drop_newest`, which fills the
  500-event default buffer instantly and drops the remainder even when Vector looks
  idle.
- **Loss, acks enabled, source cannot acknowledge** → run `vector validate
  --deny-warnings`. If the source does not support acknowledgements, Vector says so
  at validate time: *"Silent data loss could occur."* The durability was never real.
- **Loss with `skip_unknown_fields` set** → fields the table does not declare are
  discarded server-side with no error. The rows arrive; the columns do not.
- **Duplication across several sinks in a fanout** → the worst-status rule. One
  failing sink marks the event failed, so it is re-sent to the sinks that already
  succeeded. The fix is topology, not retry tuning: stop sharing an acknowledging
  source between a critical sink and an unreliable one.
- **Duplication into one sink** → a retry after a partial success. At-least-once
  delivery means the destination must tolerate duplicates; for ClickHouse that is a
  deduplicating engine or a query-time strategy, owned by
  `/clickhouse-performance-schema-ops` (`$clickhouse-performance-schema-ops`).

---

## Class 5 — high CPU or memory

**Discriminate with the per-component CPU metric**, which is opt-in: set
`measure_cpu_usage: true` on the transform or sink and read
`component_cpu_usage_ns_total`. Without it you are guessing which component is hot.

- One transform dominating CPU → VRL cost per event. `parse_json` and regex work
  are the usual candidates; a dynamic `parse_regex` pattern is worse than a fixed
  one.
- Memory growing with no CPU spike → in-memory buffers. Memory buffers consume
  memory proportional to `max_events` multiplied by event size, per sink. Sum them.
- Both climbing under burst → the source is bursty and the batch settings serialise
  the work. Check `component_received_events_total` for the burst shape before
  changing anything.

**Escalate** when the per-event cost itself is the problem rather than its
distribution: a stated throughput bound is `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`).

---

## Class 6 — it worked before the upgrade

Check these three first; each silently changes behaviour rather than failing loudly:

1. **`${VAR}` in the config, on 0.57.0 or later.** Interpolation is off by default.
   Credentials become literal strings, validation still passes, authentication
   fails at runtime.
2. **A templated `table`, `database`, object key, file path or header, on 0.57.0.**
   Confinement now requires a literal prefix and rejects the config at startup.
3. **Dashboards using pre-0.53.0 buffer metric names.** Renamed, with the old
   gauges kept for a transition period — so a dashboard can look fine and be
   reading a deprecated name that is about to disappear.

Full deltas and re-derivation commands: `80-version-and-upgrade-deltas.md`.

---

## Field notes, promoted or corrected

These were previously filed as non-normative community hypotheses. Their status now:

| Note | Status |
| --- | --- |
| "Disk buffer is not magic — it can stall under capacity conditions" | **Corrected and promoted.** It does not stall: Vector **forcefully stops itself**. Documented upstream, stated as a rule in `30-buffers-acks-and-backpressure.md`. |
| "An experimental sink in a fanout can still affect production flow" | **Confirmed, with the mechanism.** The worst-status acknowledgement rule is why. See class 4. |
| "Acknowledgements reduce throughput" | **Confirmed.** The source cannot advance until the slowest sink confirms. |
| "Auth failures plus acknowledgements can be dangerous" | **Confirmed and made specific.** Auth failure means the sink never acknowledges, so the buffer fills and `when_full` decides. See class 2. |
| "Quote hyphenated field names in VRL tests" | **Confirmed.** In `20-vrl-transforms.md`. |
| "Arrow stream can be faster, watch schema caveats" | **Confirmed and qualified.** It is beta. See `40-clickhouse-sink.md`. |

Community posts and issue threads remain troubleshooting-only: they may generate a
hypothesis, never a rule. A rule needs the upstream documentation or an observed
runtime result, recorded with the command that reproduces it. Sources:
`90-source-map.md`.
