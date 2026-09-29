# Failure classes on the message plane

Read this during a live message-plane incident, and read the matching class before changing anything. Each
class gives the symptom that identifies it, the diagnosis that separates it from the class it resembles, the
smallest action that is safe to take first, and what escalation means when that action does not hold. The
classes are language-neutral; every observable named is registered in
`alaa-services-contract references/24-metric-registry.md`.

Two rules hold across all eight. **Never delete a message or an outbox row to make a graph flat** — the
graph is the only evidence of the defect, and deletion makes the loss permanent. **Never widen a bound
mid-incident** — raising prefetch, batch size or concurrency while a system is failing adds load to the
component that is already failing.

## 1. Broker unreachable

During a total broker outage, read [Broker unreachable](./50-failure-classes/10-broker-unreachable.md) for the cross-service test and outbox evidence.

## 2. Consumer stuck with growing unacknowledged count

When deliveries remain unacknowledged, read [Consumer stuck](./50-failure-classes/20-consumer-stuck.md) for the three diagnosis signals and safe restart step.

## 3. Poison redelivery loop

When the same message loops, read [Poison redelivery loop](./50-failure-classes/30-poison-redelivery-loop.md) for broker-count and terminal-disposition checks.

## 4. Duplicate storm

When side effects duplicate, read [Duplicate storm](./50-failure-classes/40-duplicate-storm.md) for receipt/key comparison and safe containment.

## 5. Outbox stalled, or a claimed row orphaned

When the relay stops publishing or claims go stale, read [Outbox stalled](./50-failure-classes/50-outbox-stalled.md) for distinguishing throughput, dead relay, and orphaned claims.

## 6. Dead-letter queue filling

When the DLQ grows while live traffic drains, read [Dead-letter queue filling](./50-failure-classes/60-dead-letter-queue-filling.md) for tenant/error grouping and the replay gate.

## 7. A replay produced duplicates

When duplicates begin after replay, read [Replay produced duplicates](./50-failure-classes/70-replay-duplicates.md) for identifier and prior-effect diagnosis.

## 8. Publish-confirm timeout

When publishes time out but deliveries still arrive, read [Publish-confirm timeout](./50-failure-classes/80-publish-confirm-timeout.md) for ambiguous outcomes and confirmed-count comparison.
