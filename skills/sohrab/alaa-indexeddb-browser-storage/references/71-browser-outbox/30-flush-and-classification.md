# The flush

## The flush

1. **Acquire the Web Lock** `alaa:outbox-flush` with `ifAvailable: true`. Without it, several tabs and the
   service worker flush the same rows — `41-multitab-versionchange-and-locks.md`.
2. **Run the reaper first**, before claiming anything.
3. **Claim a batch** in one short `readwrite` transaction: cursor the scheduling index over
   `['queued', ''] … ['queued', nowIso]`, set `status: 'sending'` and `sendingSince`, stop at
   `outboxBatchSize`. Commit.
4. **Send outside the transaction**, each request carrying its `idempotencyKey` and an `AbortSignal` bound
   to a timeout. A send with no timeout never settles and never reports.
5. **Classify each result** and write the outcome in a short transaction.
6. **Release the lock** and emit the metrics.


## Classification

| Result | Status written | Attempts | Note |
|---|---|---|---|
| 2xx | `sent` | unchanged | record the acknowledgement, then delete or compact |
| network error, timeout, 5xx, 429 | `queued` | `+1` | reschedule per the retry policy |
| 409 or a documented conflict body | `conflict` | unchanged | surface to the user; never retried automatically |
| 401 | `queued`, **attempts unchanged** | unchanged | **pause the whole flush.** The session expired and refresh must run first. Counting a 401 as an attempt burns a valid mutation's budget on an authentication problem. |
| 403 | `abandoned` | unchanged | the server has stated this actor may not do this; retrying cannot change it |
| other 4xx | `abandoned` | unchanged | a malformed request stays malformed |

Classifying 401 and 403 identically is the defect this table exists to prevent: one is transient and one is
permanent, and treating either as the other loses data or loops.
