# Scaling, Stability, and Security

## Table of contents

- First principles
- Capacity domains
- Network and TURN guidance
- Multi-bridge guidance
- Recording scale
- Stability and observability
- Security checklist
- SLA realism
- Phased topology guidance

## First principles

The first scale limit is usually the media layer, not the web frontend.

Scale Jitsi primarily by:

- adding more JVB capacity
- separating TURN and recording capacity
- reducing single points of failure in the control plane
- measuring real media behavior under load

Do not design around one giant all-in-one node for serious concurrency.

## Capacity domains

Treat these as separate sizing and failure domains. The handbook sizing examples are useful only as starting points, not promises. For example, official sample topologies commonly start around a few vCPU and roughly 8 GB RAM for control-plane nodes and about 4 to 8 vCPU with around 8 GB RAM for JVB nodes, but real capacity depends on codec mix, dominant view behavior, recording, TURN relay rate, geography, and network quality.

### 1. Web and signaling

- web frontend
- Prosody
- Jicofo
- token mint and join APIs

### 2. Media plane

- JVB fleet
- bridge websockets where used
- public UDP paths
- TURN relays

### 3. Recording plane

- Jibri workers
- storage upload path
- post-processing and replay publishing

### 4. Analytics and control plane

- watch-time collector
- room lifecycle APIs
- webhook dispatcher

Sizing must be per domain. Do not infer media capacity from web CPU usage.

## Network and TURN guidance

TURN is not an optional afterthought for production.

Plan for users behind:

- restrictive corporate firewalls
- symmetric NAT
- mobile networks
- UDP-hostile paths

Practical rules:

- expose TURN deliberately and monitor relay usage
- plan for relay traffic cost and regional placement
- keep public and private endpoint intent clear
- use bridge websockets correctly when the deployment expects them
- avoid outdated nginx multiplexing assumptions that break websocket paths

If two participants work but larger calls fail or remote networks break badly, suspect UDP, advertised IPs, TURN, or bridge exposure before chasing UI bugs.

## Multi-bridge guidance

Horizontal scale means more videobridges, but only if the network design truly supports them.

Recommended reasoning steps:

1. confirm how each JVB becomes internet-reachable
2. confirm how participants are distributed across bridges
3. confirm how bridge health and overload are observed
4. confirm whether the chosen platform can really support more than one active JVB on the public path

A topology diagram is not enough. The packet path has to work.

## Recording scale

Recording is its own resource domain and should be treated as such.

Important rules:

- one Jibri normally handles one active recording or stream at a time
- isolate Jibri from critical bridge capacity
- queue or reject recording requests when worker capacity is exhausted
- test long sessions, browser crashes, and storage failures

If every session must be recorded, recording is a first-class subsystem, not a side feature.

## Stability and observability

A serious Jitsi deployment must be observable across the whole stack.

### Control plane signals

- join authorization latency and failures
- token mint failures
- room-reservation failures if used
- Prosody and Jicofo health
- frontend join funnel and prejoin drop-off

### Media plane signals

- JVB health endpoints
- bridge participant counts
- conference distribution across bridges
- packet loss and bitrate trends
- websocket and TURN pressure
- regional or ISP-specific connectivity failures

### Recording plane signals

- worker availability
- queue depth
- start failure rate
- completion rate
- artifact upload latency

### Business-plane signals

- actual join confirmations
- watch-time heartbeats
- orphaned session cleanup rate
- webhook delivery failures

Use media stats for operations and capacity planning. Use your own normalized event model for business truth.

## Security checklist

Use this baseline unless the task explicitly requires a different tradeoff.

### Identity and tokens

- short-lived room-scoped JWTs only
- issuer and audience restrictions
- room binding by default
- separate signing material from platform access-token secrets
- no browser-generated trusted role claims

### Gateway and headers

- sanitize all trusted `x-*` headers at the edge
- let only the gateway or backend write trusted identity data
- never treat raw browser headers as platform identity

### Network exposure

- keep JVB private REST and Colibri control endpoints off the public internet
- understand the split between public client-facing HTTP or websocket paths and private bridge health or control interfaces
- expose only the endpoints required for clients and approved ops tooling
- document which ports are public, internal, and admin-only

### Feature surface

- disable unused features
- define explicit recording policy
- enable E2EE only when its tradeoffs fit the product
- minimize analytics PII
- pin versions and rehearse upgrades in a staging environment

## SLA realism

A 99.99% target allows only about 4.38 minutes of downtime per 30-day month.

That target is not credible with:

- one host
- one JVB
- one TURN node
- one namespace with cluster dependencies outside your control
- one recording worker with no queue or fallback

A credible path toward that SLA needs at least:

- redundant web and signaling instances where packaging allows it
- multiple JVBs with a network model that truly supports them
- TURN redundancy
- safe rollouts and rollbacks
- synthetic join tests and alerting
- clear incident ownership across app and infra teams
- failure isolation between media, recording, and analytics planes

Be explicit when a proposed design is good enough for pilot or normal production but not for a 99.99% contractual commitment.

## Phased topology guidance

### Pilot

Use when the goal is product integration and early validation.

- one web or signaling node or simple Docker deployment
- one JVB
- one TURN service if external users are involved
- recording optional and tightly limited
- basic join and heartbeat analytics

### Early production

Use when the service is real but concurrency is still controlled.

- separated web or signaling and media roles
- at least one standby or redundant control-plane story
- dedicated TURN planning
- separate Jibri workers if recording exists
- baseline observability and synthetic join testing

### High-concurrency critical path

Use when the product is security-sensitive, high-volume, and availability-critical.

- multiple JVBs with proven public reachability and distribution
- redundant TURN
- isolated recording worker pool with queueing
- rehearsed upgrade and rollback path
- region-aware capacity and traffic planning
- formal load testing under realistic network conditions
- explicit residual-risk statement for anything that still depends on a single external team or single public entry point
