# Bale Safir failure classes

Read this when a Safir call failed, when writing the error-handling path for a Safir client, or when
deciding whether a specific failure may be retried.

Each class is **symptom, diagnosis, smallest safe retry, escalation**. The classes are vendor-specific.
Every general rule they depend on is owned elsewhere and routed, never restated:

- Retry legality, the backoff curve, jitter, budgets and circuit breaking: `/alaa-reliability-sla`
  (`$alaa-reliability-sla` in Codex), `references/20-retries.md`.
- Idempotency-key mechanics: the same skill, `references/60-idempotency.md`.
- Ala timeout, budget and pool **values**: `/alaa-services-contract` (`$alaa-services-contract`),
  `references/22-failure-load-and-deprecation-contract.md`.
- Queue, worker, DLQ and redelivery behaviour when the send is dispatched from a broker consumer:
  `/alaa-async-messaging` (`$alaa-async-messaging`).

One rule governs the whole table and belongs to this skill: **`request_id` never changes across retries of
one delivery.** A retry carrying a new `request_id` is a second send, and Safir will deliver it.

## 1. Connect refused, DNS failure, or TLS handshake failure

**Symptom.** The connection never opened. No request bytes were written.

**Diagnosis.** This is proof of non-execution. Safir cannot have delivered a message it never received.
Distinguish it from a timeout at the point where the error is caught: a client that catches one broad
transport exception has already lost the distinction, and the observable consequence is duplicate messages
that appear only when Safir is slow rather than down.

**Smallest safe retry.** Retryable, with or without an idempotency key, under the caller's bounded budget.

**Escalation.** Repeated refusal across attempts is an availability event for the whole channel, not a
per-recipient failure. Fail the delivery to its durable retry path and stop calling; do not walk the
recipient list issuing calls that cannot connect.

## 2. Read timeout after the request was written

**Symptom.** The request was sent in full, and no response arrived before the deadline.

**Diagnosis.** This is the absence of information, not evidence of failure. Safir may have accepted the
message, delivered it, and lost the response. **This is the one rule this skill genuinely owns:** a read
timeout on `send_message` is retryable only with an unchanged `request_id`, because Safir may have
delivered. A retry with a fresh `request_id` sends the message a second time to a user who already has it,
and on an OTP path that means two codes and a support ticket.

**Smallest safe retry.** Retry the identical request body, `request_id` included, under the caller's budget.
Change nothing else: a "corrected" field makes the retry a different request, and the key no longer matches
what Safir stored.

**Escalation.** When the budget is exhausted with no response, the delivery outcome is genuinely unknown.
Record it as unknown rather than as failed. Marking it failed invites a manual resend that duplicates a
message that was delivered; the delivery-state row and the `alaa_dependency_timeouts_total` counter are
what an operator needs to decide.

## 3. HTTP `429`, or error code `3` `RateLimitExceeded`

**Symptom.** Safir refuses the request and names throttling.

**Diagnosis.** The account is sending faster than its allowance. This is a capacity condition, not a defect
in the payload.

**Smallest safe retry.** Retryable with an unchanged `request_id`. Where the response carries a retry hint,
wait exactly the hint: guessing a shorter wait is the amplification the hint exists to prevent. Where there
is no hint, back off under the curve `alaa-reliability-sla references/20-retries.md` defines.

**Escalation.** Sustained throttling is a capacity problem that a retry cannot fix. Reduce concurrency at
the sender, and raise the account limit with Bale. Retrying harder converts a throttle into an outage.

## 4. Error code `2` `InternalServerError`, or any `5xx`

**Symptom.** Safir answers with a server-side failure.

**Diagnosis.** Ambiguous in exactly the way class 2 is ambiguous. The request reached Safir; whether it was
acted on is unknown.

**Smallest safe retry.** Retryable only with an unchanged `request_id`, under the caller's budget.

**Escalation.** A `5xx` rate that does not fall across the budget is a Safir-side incident. Stop the
channel rather than draining the queue against it, and route the channel-down decision through the
notification service's own degradation path.

## 5. Error code `17` `NotBaleUser`

**Symptom.** A per-recipient `ErrorInfo` naming code `17`.

**Diagnosis.** The recipient has no Bale account. The request was correct and Safir processed it; there is
simply nobody to deliver to. This is a deliverability outcome, not a transport failure.

**Smallest safe retry.** None. Retrying is guaranteed to fail identically and costs a call each time.

**Escalation.** Fall back to another channel where the notification's contract defines one, and record the
recipient as unreachable on Bale so the next send does not re-discover it. Where the message is an OTP and
Bale was chosen as the delivery channel, this is a user-visible login failure and the fallback path decides
whether the user can log in at all.

## 6. Error code `20` `PaymentRequired`, and code `21` `MaximumContactLimitReached`

**Symptom.** Safir refuses on an account condition rather than on the request.

**Diagnosis.** Credit is exhausted, or the bot has reached its contact limit. Neither is a property of this
message, and neither changes without a human acting.

**Smallest safe retry.** None. Every retry fails identically until an operator tops up credit or raises the
limit.

**Escalation.** Alert an operator, and hold pending deliveries in their durable state rather than failing
them: the messages are still wanted, and they will send once the account is restored. Also raise it as an
availability event, because an account condition takes the whole channel down for every recipient at once
and looks like a per-message failure in the logs.

## 7. Error codes `4` `InvalidInput` and `8` `InvalidPhone`

**Symptom.** Safir rejects the request as malformed, or rejects the recipient number.

**Diagnosis.** A caller defect. Code `8` is almost always a normalisation defect: a number that reached the
wire as `09123830000`, `+989123830000`, or with Persian digits still in it.

**Smallest safe retry.** None with the same payload. Retrying an invalid request converts a client defect
into provider load.

**Escalation.** Run the raw number through
`python3 scripts/validate_bale_payload.py --normalize '<raw>' --channel bale` and the payload through
`--mode request`. A code `8` in production that the validator does not reproduce means the normaliser and
the send path disagree — find the call site that builds the number without the normaliser.

## 8. `error_data` present alongside `message_id`

**Symptom.** A `200` response carrying both a `message_id` and a non-empty `error_data` array.

**Diagnosis.** A partial result. Some recipients were accepted and some were not, and the transport status
says nothing about which. A client that treats a `200` with a `message_id` as success silently drops every
per-recipient failure in the array.

**Smallest safe retry.** Never retry the whole request. Take the outcome per recipient from `error_data`,
map each entry by its `phone_number`, and apply the class above that matches each `code`. Recipients absent
from `error_data` succeeded.

**Escalation.** Where `error_data` names a recipient that was not in the request, stop and report it rather
than reconciling by position: the mapping is by `phone_number`, and a mismatch means the response does not
correspond to the request that was sent.

## 9. `upload_file` succeeded and `send_message` failed

**Symptom.** A `file_id` was returned, and the send that was to reference it did not complete.

**Diagnosis.** The two steps are independent requests with independent failure modes. The upload is durable
on Safir's side; the failure is entirely in step 2.

**Smallest safe retry.** Retry `send_message` alone, reusing the stored `file_id` and the unchanged
`request_id`, and classify the step-2 failure under classes 1 to 4. Do not re-upload: a second upload
returns a second `file_id`, consumes quota for a file Safir already holds, and orphans the first.

**Escalation.** Where `file_id` was not persisted before step 2, the upload is unrecoverable and the file
must be uploaded again — that is the defect to fix, not the incident to work around. Persisting `file_id`
before the send is what makes step 2 independently retryable at all.
