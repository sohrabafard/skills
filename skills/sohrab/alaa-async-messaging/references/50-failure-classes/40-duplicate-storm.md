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
`alaa-reliability-sla references/60-idempotency.md` — `/alaa-reliability-sla`.
