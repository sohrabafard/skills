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
