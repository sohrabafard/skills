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
