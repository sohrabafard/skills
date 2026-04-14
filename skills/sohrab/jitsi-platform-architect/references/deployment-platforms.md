# Deployment Platforms

## Table of contents

- Deployment selection rule
- Quick platform matrix
- Debian or VM-based installs
- Docker Compose
- Docker Swarm
- Kubernetes with Helm
- OpenShift under restricted access
- Rootless and single-namespace constraints
- Cluster-team handoff checklist

## Deployment selection rule

Choose the platform that matches the network and privilege reality, not the one that looks nicest on a diagram.

For Jitsi, the media path decides much of the deployment fit. A deployment that cannot cleanly expose JVB UDP and TURN is not production-ready no matter how elegant the web plane looks.

## Quick platform matrix

| Platform | Fit | Strengths | Main cautions |
| --- | --- | --- | --- |
| Debian or VM-based install | Best for serious self-hosted ops when root access is available | Closest to official ops model, flexible multi-bridge layouts | Requires infra ownership and classic host operations |
| Docker Compose | Best for labs, pilots, controlled small production, and fast proof-of-concept work | Official path, simple packaging, JWT and add-on support | Single-node bias, weaker HA story, manual hardening needed |
| Docker Swarm | Only when the organization already runs Swarm well | Familiar for Swarm-native teams | UDP and placement complexity, not the main official recommendation |
| Kubernetes via community Helm | Good when the cluster and network team can support JVB/TURN needs | Declarative ops, separate component scaling | Community-supported charts, exposure details matter a lot |
| OpenShift restricted namespace | Often only partial fit for the full media stack | Useful for web/control plane and platform-side APIs | UDP exposure, SCC, rootless, and Jibri constraints can block full in-cluster design |

## Debian or VM-based installs

This is often the cleanest route for production Jitsi when the organization can manage VMs or bare metal.

Why it fits well:

- aligns closely with official handbook thinking
- straightforward separation of web, signaling, JVB, TURN, and Jibri roles
- easier control over UDP, host networking, and bridge placement
- less abstraction hiding real-time networking details

Prefer this path when:

- the product needs multiple JVBs
- infra can manage TLS, DNS, and host-level firewalling
- you need predictable public IP and UDP behavior
- you need a strong path toward high availability

## Docker Compose

Use Compose when speed and packaging simplicity matter more than platform abstraction.

Good uses:

- proof of concept
- product integration development
- internal pilot
- controlled production with modest concurrency and clear limits

Practical guidance:

- use the official Docker self-hosting guide and release bundle
- keep `.env` values explicit and version-controlled through your secure config process
- use the provided password-generation workflow rather than ad hoc secrets
- use the custom config files for deployment-level defaults
- set advertised IPs correctly when hosts are behind NAT
- prefer a dedicated subdomain; do not design around subdirectory hosting

Do not present a single Compose node as a credible 99.99% solution for a critical SLA.

## Docker Swarm

Be conservative with Swarm recommendations.

It can work when:

- the organization already operates Swarm well
- node placement and public exposure are tightly controlled
- the team understands that media traffic is not ordinary stateless web traffic

Main cautions:

- JVB UDP exposure and placement need deliberate design
- rolling updates can disrupt media if bridge identity and placement are not handled well
- support material is thinner than for the core handbook and Docker quick-start path

Default recommendation: do not choose Swarm just because it is “more clustered” than Compose.

## Kubernetes with Helm

Kubernetes can be a good fit only when the cluster team can satisfy Jitsi’s network realities.

### Packaging stance

- core Jitsi documentation is not centered on Kubernetes as the primary official ops path
- the practical Helm path is community-supported through `jitsi-contrib/jitsi-helm`
- treat the chart as useful, but not equivalent to first-party product support

### What Kubernetes does well

- declarative config and rollout control
- separate scaling of web, control, coturn, and worker components
- integration with cluster observability and secret tooling

### What makes Kubernetes hard for Jitsi

- JVB needs public UDP reachability
- TURN also needs correct public exposure
- L7 ingress or OpenShift Routes solve the web plane, not the media plane
- some exposure modes constrain how many JVB replicas are actually valid behind one public path

### Practical guidance for JVB exposure

Be explicit about the chosen exposure mode and its consequences.

- LoadBalancer or NodePort behind one public UDP endpoint often means only one JVB replica can really work on that path
- multiple JVBs usually need direct node-level exposure patterns such as `hostPort` plus known node IPs, or another infrastructure design that preserves packet affinity
- `hostNetwork` is usually the most invasive option and should not be your casual default

### OCTO and chart caution

The Helm chart can support JVB scaling patterns involving OCTO, but do not treat that as a simple checkbox. Current community guidance describes parts of this area as under-tested and limited in topology assumptions.

## OpenShift under restricted access

This is where many teams over-promise.

If the app team has only one namespace, only container-level access, and no cluster-admin or node-level control, do not assume full Jitsi media-plane success inside the cluster.

### Hard questions to answer first

- Can the cluster team expose public UDP for JVB?
- Can the cluster team expose TURN correctly?
- Are `hostPort`, `LoadBalancer`, or direct node IP patterns allowed?
- Which Security Context Constraints or pod-security settings apply?
- Can the environment satisfy Chrome and shared-memory needs for Jibri?
- Can you pin or isolate nodes for latency-sensitive media workloads?

### What usually still fits in OpenShift

- platform APIs that mint Jitsi JWTs
- room lifecycle services
- analytics collectors
- web app shells or host applications
- in some environments, the Jitsi web and signaling layer

### What often needs a separate environment

- JVB fleet
- TURN relay layer
- Jibri recording workers

### Default recommendation for restricted OpenShift

If the cluster is locked down, propose a hybrid topology first:

- keep platform control-plane services in OpenShift if desired
- place JVB, TURN, and often Jibri on VM or infra-managed hosts with explicit public networking
- connect the platform to Jitsi through JWT and room orchestration APIs

This is usually more honest and more stable than forcing every Jitsi component into a namespace that cannot expose the right network paths.

## Rootless and single-namespace constraints

Be very careful with the phrase “rootless support.”

For Jitsi, rootless or highly restricted execution may still collide with:

- public UDP exposure needs
- low-level networking expectations
- Chrome and shared memory behavior for Jibri
- audio loopback and media device assumptions in recording workers
- host or node visibility needed for multi-JVB patterns

When the team lacks cluster command access, the deliverable should be:

- manifests or Helm values only where realistic
- a dependency and blocker checklist for the cluster team
- a fallback topology when the cluster cannot satisfy media-plane requirements

Do not pretend the app team can implement missing cluster-level capabilities from inside a namespace.

## Cluster-team handoff checklist

When the answer involves Kubernetes or OpenShift, include a handoff list like this:

- public DNS and TLS ownership
- public UDP exposure model for JVB
- TURN exposure model and certificates
- whether multiple JVBs are actually supported by the chosen exposure model
- required SCC or pod-security allowances
- persistent storage needs for artifacts if recording runs in-cluster
- node placement or anti-affinity expectations
- monitoring endpoints and log shipping path
- rollout and rollback ownership
- upgrade testing responsibility
