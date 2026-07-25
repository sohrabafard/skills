# Telemetry Pipeline

Load when the task touches Collector or Vector topology, config, processor placement, buffering, resilience, or the
choice of collection agent.

Endpoints, DNS names, ports, env variable names, processor names, and their default settings belong to
`/alaa-services-contract` (`$alaa-services-contract` in Codex), `references/21-…`. This file owns the topology decision,
the placement gates, and the load behaviour of the telemetry plane.

Scope boundary: this file covers concurrency and load for the telemetry plane only. Product-traffic load behaviour —
connection pools, lock contention, backpressure, load shedding, circuit breaking — belongs to `/alaa-reliability-sla`
(`$alaa-reliability-sla`).

## The default topology, and the one exception

**Default:** every Alaa service emits OTLP only to a Vector sidecar running beside it, one per pod or replica over
loopback, and that sidecar forwards to the horizontally scaled central OpenTelemetry Collector gateway, which exports to
SigNoz and to the SOC branch.

The application never holds the central Collector's address, because an application that knows the gateway address
acquires a hard dependency on gateway availability at exactly the moment the gateway is the thing failing. Its only
responsibility is to fire OTLP at loopback and forget.

**The one exception, with its condition:** a service emits OTLP directly to the central gateway only when its runtime
cannot host a co-located process — a managed platform that forbids sidecars, or a single-binary deployment with no
process supervisor. In that case export must still satisfy layer 1 below, and the missing local buffer is recorded in
the readiness evidence with the reason.

There is no third topology. A service does not build its own agent tier, and it does not fan out to vendor backends
directly — fan-out in application code puts backend credentials, retry logic, and vendor coupling into every repository
that must later be changed one repository at a time.

Deployment shapes for the sidecar:

- Kubernetes or OpenShift: a sidecar container in the same pod, sharing the network namespace; the application targets
  loopback on the contract's OTLP port.
- Docker Swarm or Compose: a co-located Vector service on the shared network. A Vector binary baked into the application
  image means two processes in one container and requires a real process supervisor; treat that as a deliberate exception
  with an owner, not a shortcut.

## Why the sidecar tier exists

- It decouples the application from backend location and availability entirely.
- Each replica owns its own buffer, so a slow or restarting central Collector cannot back-pressure the request hot path.
- It scales with the workload: a new pod brings its own agent, with no shared contention between pods.
- It gives one natural per-application place to pre-filter and shape data, including SOC pre-filtering.

Rules: the sidecar buffers to disk and forwards with retry, so a central outage is absorbed locally rather than dropped.
Heavy trace processing — tail sampling above all — belongs at the central Collector, because the sidecar sees only one
replica's spans and cannot make a whole-trace decision.

## The central Collector must never become the bottleneck

Every service and every sidecar forwards into the central Collector, so treat "the Collector is not a point of
congestion" as a first-class design rule and defend it on four layers. These four are this skill's own, because they are
the telemetry plane's load behaviour.

1. Application export is asynchronous, batched, fail-open, and bounded by short timeouts. A slow Collector never slows a
   request.
2. The per-application sidecar buffers locally, so the application never feels central back-pressure at all.
3. The central Collector runs horizontally scaled behind a load balancer, with memory limiting, batching, sending
   queues, and retry configured, plus tail sampling to bound trace volume.
4. The Collector's own self-telemetry — exporter queue size, send failures, dropped records, memory pressure, disk usage
   — is collected and alerted, because a Collector dropping data silently reports the fleet as healthy.

The Collector is a deployed, sized runtime component in the per-customer deploy artifacts, not a build step. Review its
capacity when onboarding a high-traffic customer, before the traffic arrives.

## Processor placement and config gates

Placement is not a style question. A batching processor placed before a filter batches data that is about to be dropped,
paying full cost for it; a memory limiter placed after an allocating processor cannot prevent the exhaustion it exists to
prevent.

Gates:

- Any Collector or Vector config change runs that component's own validation command, and the result is recorded in the
  change. An unvalidated config does not reach a customer environment, because the failure mode is a Collector that
  refuses to start and takes fleet-wide telemetry with it.
- Placement follows the contract's processor-placement order. Where the contract is silent, place limiting before
  anything that allocates and batching after everything that drops.
- OTLP receivers, debug endpoints, and health extensions are not exposed on public interfaces, and a bind to all
  interfaces is an explicit decision with a stated reason, not a default.

## Per-hop resilience validation

Validate each network hop separately; a pipeline that works end to end under healthy conditions tells you nothing about
which hop fails first.

| Hop | What to prove |
|---|---|
| application to local endpoint | short timeouts, bounded memory, fail-open on refusal, no synchronous dependency on backend availability |
| sidecar to central Collector | queue size, retry policy, disk buffer where loss is unacceptable, TLS, authentication, self-telemetry visible |
| central Collector to SigNoz, Sentry, or SOC | bounded fan-out, one isolated exporter queue per destination, explicit retry, drop, and dead-letter behaviour, alerting on export failure |

A SOC or SIEM branch failing must not block the SigNoz path or application traffic: give it its own exporter and queue,
and state its loss and replay behaviour. Persistent queues improve resilience but are not a message broker; where the
loss profile is genuinely unacceptable, say so and choose a broker rather than tuning a queue upward.

## Choosing the collection agent

| Tier | Tool | Why |
|---|---|---|
| central gateway | OpenTelemetry Collector, contrib distribution | CNCF reference implementation, the widest receiver and exporter set, and the only one of the three with real trace processing including tail sampling |
| edge sidecar, log shaping, SOC egress | Vector | low memory and CPU per replica, strong transform language, already deployed in the fleet's gateway and ingest paths |
| — | Grafana Alloy | only for a Grafana-native stack; the platform standardises on SigNoz, so Alloy adds a second ecosystem for no gain |

Default: central is the OpenTelemetry Collector, edge is Vector, Alloy is not used unless a customer mandates Grafana.
This choice is version-sensitive; re-check `90-source-map.md` before restating it for an unusual constraint.

A Vector that converts syslog into OTLP and ships it to the Collector is a telemetry-ingest adapter, not a SOC sink. SOC
egress is always its own explicit branch — see `70-soc-evidence.md`.
