## 3. Poison redelivery loop

**Symptom.** `alaa_queue_retries_total` rising steeply with `alaa_queue_messages_consumed_total` flat; the
same message identifier repeating in the logs; consumer CPU high with no work completing.

**Diagnosis.** Check failure classification, broker version, queue type, effective policy and the actual
return primitive. Compare the message identity and acquired/delivery counts under
`40-dead-letter-and-replay.md`: repeated non-counting returns can loop below a valid delivery limit.
A high application attempt count is not the broker delivery count; confirm the DLX route independently.

**Smallest safe action.** For counted quorum failures, correct the effective delivery-limit/DLX policy
through the authorized operations path and observe terminal disposition. For non-counting returns, repair
the bounded retry/classification path; lowering a limit that never advances cannot stop the loop.
Contain an actively harmful consumer under the incident runbook without purging messages.

**Escalation.** Fix the classification in the handler so a permanent failure rejects without requeue —
`30-consuming-ack-and-prefetch.md` — and add the case to the handler's tests. A loop that was reachable once
is reachable again from a different message body.
