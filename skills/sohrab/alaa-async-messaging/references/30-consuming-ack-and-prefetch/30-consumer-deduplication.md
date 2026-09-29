# Consumer-side deduplication

## Consumer-side deduplication

**A consumer writes a receipt row keyed by the message's idempotency key, in the same transaction as its
business effect, and a duplicate is recognised by the uniqueness constraint rejecting that insert.** A
duplicate increments a counter and does nothing else — no second effect, no error, no dead-letter.

- **The key comes from the message envelope, not from the message body's content.** A content-derived key
  cannot distinguish an honest redelivery from a genuine second request with identical content, so it
  suppresses real work.
- **The receipt lives in the same store as the effect.** In two stores they disagree: the receipt commits
  and the effect rolls back, and the redelivery is then refused forever.
- **A `SELECT` before the `INSERT` is not deduplication.** Two concurrent redeliveries both find nothing and
  both proceed; the constraint is the only component in the path that serialises.

Request-side idempotency doctrine — who generates a key, retention, and the in-flight case — is
`alaa-reliability-sla references/60-idempotency.md` — `/alaa-reliability-sla`.
