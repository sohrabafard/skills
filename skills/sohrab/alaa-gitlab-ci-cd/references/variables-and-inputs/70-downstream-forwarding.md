# Downstream forwarding

Open this guide when controlling variables passed to downstream pipelines. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Downstream pipelines and forwarding

Be explicit about what is forwarded. Do not assume only the variables you care
about are passed. `workflow:rules:variables` become default variables and can
flow downstream unless inheritance is restricted. Where forwarding cannot be
avoided, use names unique enough that a collision in the downstream project is
visible.
