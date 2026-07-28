# Scale and Capacity

Read this when sizing any component, when planning for a timetable join spike, or when stating an availability
target.

Availability doctrine, retry budgets, degradation posture and breaker shape belong to `/alaa-reliability-sla`
(`$alaa-reliability-sla`). Concrete platform values and every telemetry name belong to `/alaa-services-contract`
(`$alaa-services-contract`). This file states what to size, against what, and why the class timetable changes the
answer.

## First principle

The first scale limit is the media layer, not the web frontend. Scale by adding bridge capacity, by separating
TURN and recording capacity from it, by removing single points of failure from the control plane, and by measuring
real media behaviour under load. Do not design a single all-in-one node for serious concurrency, and do not infer
media capacity from web CPU usage — they move independently, and the second is a poor proxy that reads healthy
while the first saturates.

## The four capacity domains

Size each separately. A number derived in one domain says nothing about another.

**1. Web and signalling** — the web frontend, Prosody, Jicofo, and the token mint and join APIs. Sized by *join
rate*, not by concurrency.

**2. Media** — the bridge fleet, bridge websockets where used, public UDP paths, and TURN relays. Sized by
concurrent streams, which depends on codec mix, dominant-speaker behaviour, screen sharing and network quality.

**3. Recording** — Jibri workers, the upload path, and post-processing. Sized by concurrent recordings, and
normally one active recording per worker.

**4. Analytics and control** — the watch-time collector, room lifecycle APIs, and the event dispatcher. Sized by
heartbeat rate, which is participants divided by the heartbeat interval.

Published sizing examples are starting points, never promises. Upstream examples have started around a few virtual
CPUs and roughly 8 GB of memory for control-plane nodes and about 4 to 8 virtual CPUs with around 8 GB for bridge
nodes; that figure carries a row in `references/90-source-map.md` and was not verifiable when this file was
written. Real capacity depends on codec mix, view behaviour, recording, relay rate, geography and network quality.

## What a school timetable does to all four

This is the single largest difference between sizing a class platform and sizing a generic conferencing service,
and getting it wrong understates the control plane by an order of magnitude.

**Demand is deterministic and spiky, not diurnal and smooth.** Every class in a period starts within the same two
or three minutes. At the top of the period, the entire period's enrolled concurrency arrives as a join burst, and
the mint endpoint, Prosody and Jicofo all absorb it simultaneously while the bridges see a step change in load
rather than a ramp.

The consequences are concrete:

- **Size the mint endpoint and the signalling plane on the top-of-period join burst; size the bridges on steady
  concurrency.** Sizing everything on average concurrency understates the control plane by roughly the ratio of the
  period length to the join window — a 50-minute period with a 3-minute join window is a factor of about 16.
- **Compute the peak before the term, not after it.** The roster and the timetable are both written in advance, so
  peak concurrency and peak join rate are arithmetic, not discovery. State the number in the deliverable together
  with the timetable it came from and the date that timetable was read.
- **Reconnect storms are correlated.** One school's network event reconnects a whole class at once, and each
  reconnect is a fresh mint plus a fresh join — the same two components that are already at their peak.
- **The between-period gap is the only cheap maintenance window.** Use it for drains, restarts and upgrades —
  class 7 in `references/20-failure-classes.md`.
- **A bridge failure at the top of a period costs a whole period**, because there is no spare capacity absorbing it
  and every affected class rejoins at once.

**Admission control at the mint endpoint would bound the burst, and it does not exist on this platform.** The
service kit provides no rate limiting, circuit breaking, backpressure, load shedding, in-flight cap or ingress
request deadline; the kit's own `AGENTS.md` names rate limits and breakers as a design goal rather than a shipped
capability. Either build a bounded in-flight cap in the mint service and state its value, or state the accepted
risk with the number of joins per minute it is accepted at. Do not write a plan that assumes the kit will shed the
load.

## TURN

TURN is a required component for a class platform, not an afterthought, because school and corporate networks are
the normal case rather than the exception. Plan for restrictive firewalls, symmetric NAT, mobile networks and
UDP-hostile paths.

- Expose TURN deliberately and monitor relay usage; relay traffic is a real and regional cost.
- Keep public and private endpoint intent explicit and documented.
- Use bridge websockets as the deployment expects, and avoid outdated proxy multiplexing patterns that break
  websocket paths.
- When two-party calls work and larger ones fail, or when one network fails badly, suspect UDP, advertised
  addresses, TURN or bridge exposure before looking at the interface — class 6 in
  `references/20-failure-classes.md`.

## Multi-bridge

Horizontal scale means more bridges, and only where the network design genuinely supports them. Confirm all four
before claiming multi-bridge capability:

1. how each bridge becomes reachable from the internet;
2. how participants are distributed across bridges;
3. how bridge health and overload are observed;
4. whether the chosen substrate really supports more than one active bridge on the public path —
   `references/30-deployment-substrate.md`.

## Recording capacity

- One worker normally handles one active recording or stream at a time, so concurrent recordings is a headcount
  question with a linear answer.
- Isolate recording workers from bridge capacity. A recording worker competing with a bridge for CPU degrades every
  conference on that host, not just the recorded one.
- Queue or reject recording requests when worker capacity is exhausted, and decide which of the two before the
  first class rather than during it. See the admission-control gap above.
- Test long sessions, browser crashes and storage failures before the first recorded class, because all three
  appear only at duration.
- If every class must be recorded, recording is a first-class subsystem with its own capacity plan, not a side
  feature.

## What to observe

Group the signals by plane, because an alert that cannot be attributed to a plane cannot be acted on. Names and
required levels belong to the two owners named at the top of this file.

- **Control plane:** join authorization latency and failures, token mint failures and mint latency at the burst,
  Prosody and Jicofo health, and the join funnel including prejoin drop-off.
- **Media plane:** bridge health, participant counts per bridge, conference distribution across bridges, packet
  loss and bitrate trends, websocket and TURN pressure, and regional or provider-specific connectivity failures.
- **Recording plane:** worker availability, queue depth, start failure rate, completion rate, and artifact upload
  latency.
- **Business plane:** confirmed joins, watch-time heartbeats, orphaned session cleanup rate, and downstream
  delivery failures.

Use media statistics for operations and capacity planning. Use your own normalized event model for business truth —
`references/50-events-recording-governance.md`.

**A synthetic join, running continuously against a dedicated room, is the only check that proves the whole path
works.** Every component-level health check in this list can pass while nobody can join; class 2 in
`references/20-failure-classes.md` is exactly that scenario.

## Availability realism

A 99.99% target allows about 4.38 minutes of downtime in a 30-day month. That target is not credible with one
host, one bridge, one TURN node, one namespace whose dependencies are outside your control, or one recording
worker with no queue.

A credible path needs redundant web and signalling instances where the packaging allows it, multiple bridges on a
network model that really supports them, TURN redundancy, rehearsed rollout and rollback, continuous synthetic
join testing, clear incident ownership across the application and infrastructure teams, and failure isolation
between the media, recording and analytics planes.

**Say plainly when a design is adequate for a pilot or ordinary production but not for a contractual 99.99%
commitment.** For a class platform, state the target in terms the school understands as well: minutes of lost
teaching per term is the number a head teacher will hold you to, and it is not the same shape as a percentage.

## Phased topology

**Pilot** — product integration and early validation: one web or signalling node or a simple container deployment,
one bridge, one TURN service where external users are involved, recording optional and tightly limited, basic join
and heartbeat analytics.

**Early production** — real service, controlled concurrency: separated web/signalling and media roles, a stated
redundancy story for the control plane, dedicated TURN planning, separate recording workers where recording
exists, baseline observability and synthetic join testing.

**High-concurrency critical path** — security-sensitive, timetable-driven, availability-critical: multiple bridges
with proven public reachability and distribution, redundant TURN, an isolated recording worker pool with queueing,
a rehearsed upgrade and rollback path, region-aware capacity planning, formal load testing that reproduces the
top-of-period burst rather than a smooth ramp, and an explicit residual-risk statement for everything still
depending on a single external team or a single public entry point.
