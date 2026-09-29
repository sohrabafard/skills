# Dead-lettering and the replay procedure

Read this before declaring a dead-letter route, when deciding what happens to a message a handler cannot
process, and before replaying anything from a dead-letter queue. It owns the dead-letter topology, the
classification that decides where a failed message goes, and the fleet's replay procedure.


Use this index to reach the needed queue-declaration, failure-routing, broker-version, or replay procedure. The original section anchors remain below.

## Topology

Use [Topology](./40-dead-letter-and-replay/10-topology.md) when declaring live, retry, and dead-letter queues and exchanges.

## Broker-version gate for the retry bound

Use [Broker-version gate for the retry bound](./40-dead-letter-and-replay/20-broker-version-gate.md) when checking whether a RabbitMQ 4.3 return path advances quorum delivery count.

## Classification — three kinds of failure, three destinations

Use [Classification — three kinds of failure, three destinations](./40-dead-letter-and-replay/30-failure-classification.md) when choosing the terminal route for transient, permanent, or tenant-scoped failure.

## The replay procedure

Use [The replay procedure](./40-dead-letter-and-replay/40-replay-procedure.md) before moving any message from a DLQ back onto its live queue.

## Unreplayable messages

Use [Unreplayable messages](./40-dead-letter-and-replay/50-unreplayable-messages.md) when a DLQ message may no longer represent work owed.
