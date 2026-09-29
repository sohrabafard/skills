# The replay procedure

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
4. **The messages are still meaningful under the business owner's validity and cancellation contract.**
   Caller HTTP expiry does not decide this. A message invalid under that contract, whose entity is gone,
   or whose effect already happened by compensation is not replayed. See "unreplayable" below.

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
