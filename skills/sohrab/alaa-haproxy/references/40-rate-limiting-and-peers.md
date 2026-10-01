# Rate Limiting, Stick Tables and Peers

When choosing a limiter key, read [Identity and trust](40-rate-limiting-and-peers/10-key-and-trust.md) for direct, PROXY-protocol and forwarded-header topologies and reachability obligations.
When sizing or inspecting a table, read [Table capacity](40-rate-limiting-and-peers/20-table-capacity.md) for entry count, expiry, saturation and real-key inspection.
When reasoning about cluster enforcement, read [Replication and partitions](40-rate-limiting-and-peers/30-replication-and-partitions.md) for non-atomic counters, bounded partition arithmetic and degraded-enforcement owners.
Before enabling peers, read [Peer preconditions](40-rate-limiting-and-peers/40-peer-preconditions.md) for local identity, compatible schema and authenticated transport.

The worked pattern is `examples/haproxy/12-peers-global-rate-limit.cfg`; its illustrative thresholds require the trust and partition assumptions above.
