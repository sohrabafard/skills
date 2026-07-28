# Dead-lettering and the replay procedure

Read this before declaring a dead-letter route, when deciding what happens to a message a handler cannot
process, and before replaying anything from a dead-letter queue. It owns the dead-letter topology, the
classification that decides where a failed message goes, and the fleet's replay procedure.

## Topology

**Every queue declares a dead-letter target in the same change that declares the queue.** A queue with no
dead-letter target either redelivers a poison message forever or drops it, and both outcomes look like a
working consumer from outside.

The shapes, with names taken from `alaa-services-contract references/23-queue-and-exchange-registry.md`:

- A live queue's dead-letter queue is `<queue>.dlq`.
- A command family's dead-letter exchange is `<service>.commands.dlx`, of type `direct`.
- A dead-letter routing key is the live routing key with `.failed` appended.
- A delayed-retry queue is `<queue>.retry`, and its dead-letter target is the **live** queue, which is what
  makes the delay work.

**A dead-letter queue declares no dead-letter target of its own.** A DLQ whose failures dead-letter again
produces a chain nobody drains, and the message's origin becomes unrecoverable after the second hop.

**A dead-letter queue has no consumer by default.** Its purpose is to hold messages for a human decision;
attaching a consumer that retries them recreates the loop the DLQ exists to break.

**Every dead-lettered message carries enough context to diagnose it without the original request**: the
original queue and routing key, the correlation or trace identifier, the delivery count, and the failure's
error code. The broker records the reason automatically; the error code has to be put there by the handler,
and its absence is what turns a DLQ into a pile of undiagnosable messages.

## Classification — three kinds of failure, three destinations

Classify by whether a retry could ever succeed, not by how bad the failure looks.

| Class | Test that identifies it | Destination |
|---|---|---|
| **Transient** | The failure is a property of this moment: dependency unreachable, timeout, lock contention, a `502`/`503`/`504` | Redeliver, bounded by the delivery limit. It reaches the DLQ only after the limit is spent |
| **Permanent** | The failure is a property of the message: schema violation, unknown message type, an entity it references was deleted for good | Reject without requeue. It goes to the DLQ on the first failure, because redelivering it cannot change the outcome |
| **Tenant-scoped** | The failure is a property of one tenant or project: a disabled account, a revoked credential, an exhausted quota | Reject without requeue, and record the tenant on the message. Redelivering consumes the fleet's capacity on one tenant's messages and starves every other tenant |

**A handler that cannot classify a failure treats it as transient and lets the delivery limit decide.**
Treating an unknown failure as permanent discards work on the first blip; treating it as transient costs the
delivery limit and then reaches the DLQ anyway, where a human can look at it.

**A tenant-scoped failure is the one that hides in aggregate metrics.** One tenant producing every failure
looks identical, at the queue level, to a broken consumer — which is why `50-failure-classes.md` makes
"group the DLQ by tenant" the first diagnostic step.

## The replay procedure

Replay moves messages from a dead-letter queue back onto their live queue. It is a deliberate operation with
preconditions, and it is the operation most likely to turn one incident into two.

### Preconditions — all four, before any message moves

1. **The cause is fixed and the fix is deployed.** The observable: the fixed code is running in the
   environment being replayed into, confirmed by its deployed version, not by a merged pull request.
2. **The cause is proven gone on one message.** Replay exactly one message and observe it succeed. A replay
   that begins with the whole queue and discovers the fix was incomplete has doubled the DLQ and lost the
   original ordering.
3. **The handler is idempotent, and its redelivery test passes on the deployed version.** Replay is a
   deliberate redelivery, so every duplicate it creates is caught only by that guarantee.
4. **The messages are still meaningful.** A message whose deadline has passed, whose entity is gone, or
   whose effect has already been produced by a compensating action is not replayed. See "unreplayable"
   below.

### The replay

1. **Record the starting count** of the dead-letter queue. Without it there is no way to say afterwards how
   many messages were replayed, and no way to detect a message that arrived during the replay.
2. **Replay in bounded batches, never the whole queue at once.** A DLQ that filled during a several-hour
   outage holds more work than the live fleet processes in that time, so replaying it all makes the consumer
   the next outage.
3. **Watch the live queue's error rate between batches, and stop on the first failure that is not a
   duplicate.** The failure means the cause was not what the fix addressed.
4. **Republish onto the live queue with the original routing key**, stripping the `.failed` suffix, and
   preserve the original message identifier and idempotency key. A new identifier makes the replayed
   message a new message, so the consumer's deduplication cannot protect anything.
5. **Do not drain the DLQ into a file and re-inject it later.** The round trip loses broker headers,
   including the death record that says why the message failed, and that record is the only evidence of the
   original defect.

### After the replay

**Report the starting count, the number replayed, the number that failed again, and the residual DLQ
depth.** A replay reported only as "done" leaves nobody able to tell whether the queue is empty because the
messages succeeded or because they were discarded.

**A message that fails on replay is not replayed a second time without a new cause analysis.** The second
replay of an unchanged message against unchanged code produces the same failure and consumes capacity twice.

## Unreplayable messages

A message in a dead-letter queue is not always work that is owed. These are unreplayable, and each is
handled by naming it rather than by replaying it:

- **Its effect has already happened by another path** — a human ran the operation manually, or a
  reconciliation job produced it. Replaying duplicates an effect that idempotency cannot catch, because the
  other path wrote no receipt.
- **Its deadline has passed.** A one-time password, a session notification, or a time-boxed instruction
  delivered hours late is worse than not delivered, because the recipient cannot tell it is stale.
- **The entity it references is permanently gone.** The replay will fail identically, so it is a way of
  making the same message fail twice.
- **Its body is malformed and the producer's defect is fixed.** The correct output is a new, well-formed
  message from the producer, not a replay of a body no consumer can parse.

**Every unreplayable message is recorded before it is discarded**: its identifier, its tenant, its original
routing key, and the reason it was not replayed. Discarding without that record makes the loss permanent and
undiscoverable, which is the outcome the dead-letter queue existed to prevent.
