# Prefetch

## Prefetch

**Prefetch count multiplied by the p99 handler duration is the unacknowledged window: the amount of work
that redelivers at once when the channel drops.** Derive the count from that product, and state both the
count and the measured p99 in the change.

The procedure:

1. **Measure the handler's p99 duration** from `alaa_queue_message_duration_seconds`. An estimate is not a
   measurement, and handlers are routinely an order of magnitude slower than their authors expect.
2. **Choose the unacknowledged window the fleet can absorb as a single redelivery burst.** This is the real
   input: when a consumer's channel drops, everything unacknowledged is redelivered together.
3. **Set the count to that window divided by the p99 duration**, and never leave it at the library default.
   Package defaults are large — the Laravel RabbitMQ driver's is `1000` — which leaves the window unbounded
   in practice.
4. **Set it lower for an ordered or high-blast-radius queue**, where a redelivery burst is more expensive
   than the throughput the higher count buys.

**Raising prefetch is not a remedy for a slow consumer.** It moves the broker's bounded, durable queue into
the consumer's unbounded, volatile memory, where a restart loses all of it, and it starves other consumers
on the same queue because the broker will not redeliver messages already dispatched.

The specific value for a queue is `alaa-services-contract`'s; the derivation above is this file's. That
every consumer sets one explicitly is required by
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.
