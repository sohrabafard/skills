# The reaper — the failure class the server outbox does not have

## The reaper — the failure class the server outbox does not have

**Symptom.** A row sits in `sending` and nothing moves; the queue depth does not fall; no error is logged,
because the context that would have logged it no longer exists.

**Diagnosis.** `sendingSince` is older than `outboxReaperStaleAfterMs` (default **120,000**, which must
exceed `outboxSendTimeoutMs` by a clear margin or the reaper races a live send).

**Action.** Return the row to `queued`, increment `attempts`, reschedule, and set `lastError: 'reaped'`.
This is safe precisely because the request carried an `idempotencyKey`: if the original send did reach the
server, the duplicate is deduped there.

**When.** At the start of every flush before any claim, and on application boot. Never on a timer alone — a
closed device has no timer, and boot is when the orphans are guaranteed visible.
`examples/outbox-reaper.ts` is the implementation.

**Never resolve a stuck row by deleting it.** A deleted row is a user mutation that no longer exists and
nothing will detect its absence.
