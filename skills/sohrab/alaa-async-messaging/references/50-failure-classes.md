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

**Symptom.** `alaa_queue_messages_published_total` flat, `alaa_dependency_request_failures_total` rising on
the broker, consumers logging connection failures and restarting. `alaa_outbox_depth` climbing while the
service continues to answer requests normally.

**Diagnosis.** Separate an unreachable broker from a failing publisher: an unreachable broker fails every
service on the vhost at once, so check whether another service's publish counter also went flat. If only one
service is affected, it is credentials, topology, or that service's network path — not the broker.

**Smallest safe action.** None on the broker. The outbox is absorbing the outage by design: the request path
is unaffected and the facts are durable. Confirm the outbox is in fact filling, since that is the evidence
the design is working; a flat outbox depth during a broker outage means facts are being dropped instead.

**Escalation.** If publishes are being made outside a transaction with no outbox row, that route is losing
facts for the whole outage — this is a code defect, not an incident action. Broker cluster recovery is
`/caas-arvan-kuber` (`$caas-arvan-kuber`).

## 2. Consumer stuck with growing unacknowledged count

**Symptom.** Unacknowledged count high and stable or rising; `alaa_queue_backlog` rising;
`alaa_queue_messages_consumed_total` flat or nearly flat; consumer processes alive and not restarting.

**Diagnosis.** The consumer holds deliveries it is not completing. Distinguish three causes before acting: a
handler blocked on a dependency, which shows a rising
`alaa_dependency_request_duration_seconds` for that dependency; a handler deadlocked on the database, which
shows `alaa_db_lock_wait_seconds` rising; and a prefetch so high that the consumer has pulled the working
set into memory, which shows `alaa_worker_memory_bytes` rising with a flat consumed counter.

**Smallest safe action.** Restart one consumer instance, not the fleet. Its unacknowledged messages return
to the queue and are redelivered to healthy instances; if the backlog then moves, the cause is local to that
process, and if it does not, the cause is the dependency.

**Escalation.** Lower prefetch and redeploy when the third cause is confirmed. Recompute the count from the
measured p99 — `30-consuming-ack-and-prefetch.md` — rather than halving it by feel.

## 3. Poison redelivery loop

**Symptom.** `alaa_queue_retries_total` rising steeply with `alaa_queue_messages_consumed_total` flat; the
same message identifier repeating in the logs; consumer CPU high with no work completing.

**Diagnosis.** A permanent failure is being treated as transient. Confirm it by reading one failing
message's delivery count: a count far above the delivery limit means the limit is unset or the handler is
requeuing explicitly, which is the defect. A count at the limit means the mechanism is working and the
message is on its way to the DLQ.

**Smallest safe action.** Set or lower the queue's delivery limit so the message dead-letters, and let it.
Do not stop the consumer: stopping it leaves the message at the queue head to loop again on restart.

**Escalation.** Fix the classification in the handler so a permanent failure rejects without requeue —
`30-consuming-ack-and-prefetch.md` — and add the case to the handler's tests. A loop that was reachable once
is reachable again from a different message body.

## 4. Duplicate storm

**Symptom.** Business effects appearing more than once: two notifications, two charges, two rows.
`alaa_queue_retries_total` elevated. The receipt table's duplicate counter is flat, which is the tell.

**Diagnosis.** A flat duplicate counter with real duplicates means deduplication is not running: either no
receipt row is written, or the key is derived from message content and differs between the copies, or the
receipt is in a different store from the effect and the two disagreed. Read one duplicated pair and compare
their idempotency keys — if the keys differ, the key derivation is the defect, not the broker.

**Smallest safe action.** Stop the consumer for the affected queue. Every further delivery produces another
duplicate, and messages wait safely in a durable queue while a consumer does not.

**Escalation.** Add the uniqueness constraint in the same store as the effect, and prove it with the
redelivery test before restarting the consumer. Doctrine:
`alaa-reliability-sla references/60-idempotency.md` — `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## 5. Outbox stalled, or a claimed row orphaned

**Symptom.** Consumers stop seeing a class of event while the writing endpoint keeps returning success.
`alaa_outbox_depth` and `alaa_outbox_oldest_age_seconds` climbing; `alaa_outbox_published_total` flat.

**Diagnosis.** Separate three cases before touching a row. Depth up with published up is throughput, not a
stall. Depth up with published flat and no relay process running is a dead relay. Depth up with published
flat and a relay running means a row is claimed by nothing: check whether the oldest row's claim is older
than the claim expiry and no live worker holds it.

**Smallest safe action.** Return orphaned rows to the claimable state and let the normal relay take them.
Never publish a row by hand — a hand publish bypasses the confirm and the counter, so the next operator sees
the same flat graph — and never delete a row, because a consumer redelivery is safe and a deleted row is a
lost fact.

**Escalation.** A recurrence means the claim lifetime is shorter than a publish attempt. The claim mechanism
is `/alaa-data-layer` (`$alaa-data-layer`); the relay's own absent timeout, attempt cap, backoff and
quarantine are recorded in `20-publishing-and-the-outbox.md` and are a kit change request, not a local
reimplementation.

## 6. Dead-letter queue filling

**Symptom.** `alaa_queue_dead_letter_total` rising; DLQ depth growing; the live queue draining normally.

**Diagnosis.** Group the dead-lettered messages by tenant first, then by error code. One tenant producing
nearly all of them is a tenant-scoped failure and is not a consumer defect; one error code across many
tenants is a code or contract defect; a spread across both usually means an upstream producer changed its
message shape. Read the death record on one message for the original queue and reason.

**Smallest safe action.** Nothing to the DLQ. It is holding messages exactly as designed, and every action
taken before the cause is known reduces the evidence available.

**Escalation.** Fix the cause, deploy it, then follow the replay procedure in `40-dead-letter-and-replay.md`
in full, including the single-message proof before any batch.

## 7. A replay produced duplicates

**Symptom.** Duplicate business effects appearing immediately after a replay, with the duplicate counter
still flat.

**Diagnosis.** The replay re-published messages with new identifiers, or the effects had already been
produced by another path — a manual operation or a reconciliation job — that wrote no receipt row. Check one
duplicated effect: a receipt row from the original delivery with a different key on the replayed message
proves the identifier was regenerated.

**Smallest safe action.** Stop the replay. Do not replay the remainder while identifiers are being
regenerated, because every remaining message will duplicate too.

**Escalation.** Reconcile the duplicated effects deliberately, one class at a time, before resuming.
Preserve the original identifier and idempotency key on any subsequent replay, and record the count
replayed, as `40-dead-letter-and-replay.md` requires.

## 8. Publish-confirm timeout

**Symptom.** Publishes reported as failing while messages nevertheless arrive at consumers; publish latency
at the timeout boundary; the outbox republishing rows that consumers have already handled.

**Diagnosis.** This is the ambiguous outcome: the timeout says nothing about whether the broker persisted
the message. A connect refusal and a timeout are different events and must not share a code path — the
refusal proves non-delivery, the timeout proves nothing. Confirm by comparing the consumer's received count
against the publisher's confirmed count over the same window; consumer higher than publisher is the
signature.

**Smallest safe action.** Nothing. The republished messages are the correct behaviour of an unconfirmed
publish, and the consumer's deduplication is the component that makes it safe. Verify that deduplication is
actually working — a flat duplicate counter here means class 4, not this class.

**Escalation.** If the confirm timeout is shorter than the broker's real p99 confirm latency, every publish
under load is ambiguous, and the resulting republishes multiply the load that caused it. The timeout value
is `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`; whether `mqkit` exposes
a publish timeout at all was **not verified this session** and must be checked against kit source before
anyone changes one.
