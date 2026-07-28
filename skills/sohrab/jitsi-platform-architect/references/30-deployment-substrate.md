# Deployment Substrate

Read this when choosing or defending a substrate for Jitsi, when exposing JVB or TURN, or when handing a
requirement to a cluster team.

This file owns what the media plane demands of a substrate. It does not own substrate mechanics: chart values,
manifests, rollout strategy and namespace policy belong to `/alaa-k8s-helm` (`$alaa-k8s-helm`) and, on Arvan, to
`/caas-arvan-kuber` (`$caas-arvan-kuber`); image hardening, Compose and Swarm delivery belong to
`/alaa-docker-production` (`$alaa-docker-production`); edge termination, TLS and websocket proxying belong to
`/alaa-haproxy` (`$alaa-haproxy`). Every upstream packaging and support-tier claim below has a row in
`references/90-source-map.md`.

## The selection rule

Choose the substrate that matches the network and privilege reality, not the one that looks best on a diagram. For
Jitsi the media path decides most of the fit: **a substrate that cannot cleanly expose JVB UDP and TURN is not
production-ready regardless of how good the web plane looks on it.**

Ask these four questions before writing any manifest, and record the answers in the deliverable:

1. How does each videobridge become reachable from the public internet, by address and by port?
2. How are participants distributed across bridges, and what happens to that distribution when one bridge leaves?
3. How are bridge health and overload observed, and by whom?
4. Can this substrate really run more than one active bridge on the public path?

A topology diagram is not an answer to any of them. The packet path has to work.

## Platform matrix

| Substrate | Fit | Strengths | Main cautions |
|---|---|---|---|
| Debian or VM install | best for serious self-hosted operation with root access | closest to the official operations model, flexible multi-bridge layouts | needs infrastructure ownership and classic host operations |
| Docker Compose | labs, pilots, controlled small production | official path, simple packaging, token support | single-node bias, weak availability story, manual hardening |
| Docker Swarm | only where the organisation already runs Swarm well | familiar to Swarm-native teams | UDP and placement complexity, thin support material |
| Kubernetes via community Helm | good where the cluster and network team can meet the media needs | declarative operation, per-component scaling | community-supported chart, exposure details decide everything |
| OpenShift, restricted namespace | usually a partial fit | fine for the web and control plane and platform APIs | UDP exposure, security context constraints, rootless and Jibri limits can block the media plane |

## Debian or VM installs

This is often the cleanest route to production Jitsi where the organisation can run virtual machines or bare metal:
it aligns with the upstream operations model, separates web, signalling, bridge, TURN and recording roles without
abstraction, and gives direct control over UDP, host networking and bridge placement.

Choose it when the product needs multiple bridges, when infrastructure can manage TLS, DNS and host firewalling,
or when predictable public addressing matters.

## Docker Compose

Use Compose when packaging simplicity matters more than platform abstraction: proof of concept, integration
development, internal pilot, and controlled production with a stated concurrency limit.

- Use the official self-hosting bundle and its documented password-generation workflow rather than ad hoc secrets.
- Keep environment values explicit and version-controlled through the secure configuration process; the signing
  key is not one of them — see `references/10-architecture-and-jwt-trust.md`.
- Set advertised addresses correctly when hosts sit behind NAT, because a wrong advertised address produces exactly
  the symptom in class 6 of `references/20-failure-classes.md`.
- Use a dedicated subdomain. Do not design around subdirectory hosting.

**Do not present a single Compose node as a credible answer to a high-availability commitment.** One node carrying
a timetable means one restart cancels the school day.

## Docker Swarm

Be conservative. Swarm can work where the organisation already operates it well, where node placement and public
exposure are tightly controlled, and where the team understands that media traffic is not ordinary stateless web
traffic. Bridge UDP exposure and placement need deliberate design, and rolling updates disrupt media when bridge
identity and placement are not handled explicitly.

Do not choose Swarm because it looks more clustered than Compose. Choose it because the organisation already runs
it, or do not choose it.

## Kubernetes with Helm

Kubernetes fits only when the cluster team can satisfy the media realities. The practical chart path is
community-supported, which is a different support tier from the core handbook — treat it as useful, not as
first-party product support.

What Kubernetes does well here: declarative configuration and rollout control, independent scaling of web,
control, TURN and worker components, and integration with cluster observability and secret tooling.

What makes it hard: the bridge needs public UDP reachability, TURN needs correct public exposure, and L7 ingress or
routes solve the web plane while leaving the media plane untouched.

### Exposure modes and their consequences

Be explicit about the chosen mode and state its consequence in the deliverable.

- A single LoadBalancer or NodePort in front of one public UDP endpoint usually means **only one bridge replica
  really works on that path**, whatever the replica count says.
- Multiple bridges usually need node-level exposure — `hostPort` with known node addresses, or another design that
  preserves packet affinity to the bridge that owns the conference.
- `hostNetwork` is the most invasive option available and is not a casual default.

Bridge-scaling patterns involving OCTO exist in the chart, and community guidance has described parts of that area
as under-tested with narrow topology assumptions. Verify against the release before promising it —
`references/90-source-map.md`.

## OpenShift under restricted access

This is where designs over-promise most often. When the application team has one namespace, container-level access
and no cluster-admin or node-level control, do not assume the full media plane can run in the cluster.

Answer these before proposing an in-cluster media plane:

- Can the cluster team expose public UDP for the bridges?
- Can the cluster team expose TURN correctly, with certificates?
- Are `hostPort`, LoadBalancer or direct node-address patterns permitted?
- Which security context constraints or pod-security settings apply?
- Can the environment satisfy the browser and shared-memory needs of a recording worker?
- Can nodes be pinned or isolated for latency-sensitive media?

What usually still fits inside a restricted namespace: the token mint endpoint, room-lifecycle services, analytics
collectors, the host application, and in some environments the Jitsi web and signalling layer.

What usually needs somewhere else: the bridge fleet, the TURN layer, and the recording workers.

**Default recommendation for a locked-down cluster: propose a hybrid topology.** Keep the platform control plane in
the cluster, place bridges, TURN and usually recording on hosts with explicit public networking, and connect the
two through the token and room-lifecycle APIs. That is more honest and more stable than forcing every component
into a namespace that cannot expose the right network paths.

## Rootless and single-namespace constraints

Treat the phrase "rootless support" as a claim to verify, not a property to assume. Restricted execution can still
collide with public UDP exposure, low-level networking expectations, the browser and shared-memory behaviour of
recording workers, audio loopback and media-device assumptions, and the node visibility that multi-bridge patterns
need.

When the team has no cluster-level command, the deliverable is: manifests or chart values only where they are
realistic, a dependency and blocker list addressed to the cluster team, and a fallback topology for the case where
the cluster cannot meet the media requirements. Do not write a plan that requires the application team to
implement a cluster capability it cannot reach.

## Cluster-team handoff checklist

Include this list whenever the answer involves Kubernetes or OpenShift, with a named owner against each line:

- public DNS and TLS ownership
- the public UDP exposure model for the bridges
- the TURN exposure model and its certificates
- whether multiple bridges are actually supported by the chosen exposure model
- required security context constraint or pod-security allowances
- persistent storage for recording artifacts if recording runs in-cluster
- node placement and anti-affinity expectations
- monitoring endpoints and the log shipping path
- rollout and rollback ownership
- upgrade testing responsibility

## What a school timetable adds

Capacity for a class platform is knowable before the term starts, because the timetable is written before the term
starts. The substrate must therefore allow **planned** capacity addition ahead of a known peak, not only reactive
scaling after saturation — see `references/60-scale-and-capacity.md`. A substrate whose only scaling story is
autoscaling on observed load will add a bridge several minutes after every class in the period has already failed
to join.
