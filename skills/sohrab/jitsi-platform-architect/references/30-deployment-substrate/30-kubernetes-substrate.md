Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

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
