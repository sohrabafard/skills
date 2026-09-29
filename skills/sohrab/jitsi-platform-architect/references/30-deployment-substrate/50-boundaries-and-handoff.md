Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

## Rootless and single-namespace constraints

Official containers introduced rootless execution and internal web ports `8000`/`8443` in `stable-11146`
([release notes](https://github.com/jitsi/docker-jitsi-meet/releases/tag/stable-11146), read 2026-09-29).
Check the pinned image, Compose mappings and proxy targets together during an upgrade; old internal ports may
break the web path. This does not establish OpenShift restricted-policy compatibility: verify UID, filesystem,
security context, Jibri browser/shared-memory/device needs, public UDP/TURN reachability and bridge placement
against the target platform. Keep the hybrid fallback until that proof exists.

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
