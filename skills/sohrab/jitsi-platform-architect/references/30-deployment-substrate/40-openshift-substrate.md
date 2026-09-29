Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

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
