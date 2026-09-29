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
is `/alaa-data-layer`; the relay's own absent timeout, attempt cap, backoff and
quarantine are recorded in `20-publishing-and-the-outbox.md` and are a kit change request, not a local
reimplementation.
