Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

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
