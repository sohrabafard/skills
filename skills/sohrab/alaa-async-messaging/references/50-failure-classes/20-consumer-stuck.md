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
