# Topology and the delivery contract

A Vector config is a set of independent delivery paths that happen to share a
process. Reasoning about it as one config blob is what produces the surprise where
one sink's failure changes another sink's behaviour.

**Where the design question belongs.** Choosing how many Vector tiers a system has,
where the trust boundary sits, and which component owns which responsibility is
subsystem design, and it belongs to `/alaa-system-design` (`$alaa-system-design`).
This file covers what is specific to Vector: how a path's delivery behaviour is
written down, and which Vector mechanisms make paths independent of each other.

## Write the contract per path, before any config

For every source-to-sink path, state these seven things. Each one maps to a
concrete Vector setting, so a contract with a blank is a config decision nobody has
made:

| Contract field | The Vector setting it decides |
| --- | --- |
| Event schema in, and out | The `remap` program, and its unit tests |
| Is this path a gate or a contributor? | `when_full`, and whether acks are enabled |
| Tolerable outage duration | `buffer.max_size` or `max_events`, via the sizing arithmetic |
| Tolerable loss | `when_full: drop_newest` versus a disk buffer |
| Retry ceiling | `request.retry_attempts` — the default is effectively infinite |
| What proves it healthy | The internal metric and threshold you will alert on |
| How it is tested | The `vector test` cases, including the failure classes |

**Gate or contributor is the load-bearing question**, and the fleet has already
answered it for product telemetry: fail open. The rule, the two path types, and the
Vector option that expresses each are in `30-buffers-acks-and-backpressure.md`.
Requirement level is owned by `/alaa-observability-soc`
(`$alaa-observability-soc`); every Ala value is owned by `/alaa-services-contract`
(`$alaa-services-contract`)
`references/22-failure-load-and-deprecation-contract.md`.

## Deployment shapes, and what each one costs

- **Edge agent.** Vector runs beside the producer. Buffers close to the source, so a
  flapping network link to the backend is absorbed locally. Cost: buffer capacity is
  bounded by whatever the node has, and node-local disk buffers do not survive the
  node.
- **Central aggregator.** Producers ship to a Vector tier that owns transforms,
  routing and vendor-sink isolation. Cost: it is a new single point of failure and
  needs its own capacity plan. Benefit: routing policy changes in one place, and
  vendor sinks are isolated from producers.
- **Agent to aggregator.** Both, and the usual production shape: the agent absorbs
  local flap, the aggregator owns policy. Cost: two tiers to operate, and two places
  where buffering must be configured deliberately rather than defaulted.
- **Unified.** One Vector doing everything. Reasonable for small deployments, but
  state the blast radius explicitly: every path shares one process, and a disk-buffer
  volume filling stops all of them at once.

Choosing between these is a design question. Take it to `/alaa-system-design`
(`$alaa-system-design`) when the answer is not obvious from the delivery contracts.

## Fanout is where paths stop being independent

One source feeding several sinks does **not** give you several independent paths.
Two mechanisms couple them:

1. **Acknowledgements use the worst status.** If one sink of three fails, the event
   is marked failed and re-sent — to all three. The two healthy sinks receive
   duplicates because the third is broken.
2. **Backpressure propagates through the shared source.** A sink with
   `when_full: block` stalls the source, which stalls every other sink reading from
   that source. A slow experimental destination becomes a production incident.

**Rule:** a critical path and an unreliable or experimental path do not share an
acknowledging source. Give them separate sources, or accept duplicates and stalls
in the critical path. This is the concrete reason behind the old advice not to "mix
experimental and production sinks casually" — the mechanism is the worst-status rule,
not general caution.

**Rule:** when one destination must not be able to stall another, isolate them into
separate Vector instances or separate sources, not merely separate sinks. Sinks in
one topology share the source's acknowledgement state; that is not something a sink
setting can undo.

## Throughput and batching bounds

Batch sizes, buffer capacity and concurrency are throughput arithmetic, and the
inputs must be measured rather than assumed — `component_received_events_total` for
rate and `component_sent_bytes_total / component_sent_events_total` for event size,
both in `60-internal-monitoring.md`. When a bound has to be *stated* as a function
of a growing input rather than measured at one operating point, that is
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`), which owns
complexity budgets and the method for deriving a bound from the system.

## Ordering of decisions

1. Enumerate the paths. One line each: source, transforms, sink.
2. Write the seven contract fields per path. Stop at any blank.
3. Decide gate or contributor per path, against
   `/alaa-observability-soc` (`$alaa-observability-soc`).
4. Choose the deployment shape that lets each path meet its contract, and the Helm
   role that gives it the storage it needs — `70-helm-chart-operations.md`.
5. Only then write config. Validate it with the flag set in
   `50-validation-and-testing.md`.
