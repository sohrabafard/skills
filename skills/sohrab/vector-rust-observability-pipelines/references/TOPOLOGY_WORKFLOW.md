
# Topology workflow

## Start with the graph
Write the pipeline as contracts:
- source -> transform(s) -> sink(s)

For each edge define:
- input schema
- output schema
- backpressure behavior
- retry behavior
- whether acknowledgements matter
- what metrics prove it is healthy

## Deployment shapes
### Edge agent
Good when:
- local logs/metrics need buffering near the producer
- network links to the backend can flap

### Aggregator
Good when:
- you need centralized transforms, routing, and isolation from vendor sinks
- you want a single control plane for routing policies

### Unified
Good for small or medium deployments, but be explicit about blast radius.

## Fanout caution
One pipeline feeding multiple sinks can inherit the strictest durability / blockage behavior in surprising ways.
Separate critical and experimental paths when the risk matters.
