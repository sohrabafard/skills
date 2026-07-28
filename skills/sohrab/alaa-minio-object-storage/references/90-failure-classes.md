# Failure classes

Each entry is symptom, then diagnosis, then the smallest safe retry, then when to stop retrying and escalate.
Retry counts, backoff shape and breaker thresholds are `/alaa-reliability-sla` (`$alaa-reliability-sla`); this file
says only which failures may be retried at all and what each one means.

**The rule that spans every class: an error is never evidence that an object is absent.** Only a successful
response saying so is. Converting a failed check into "not there" is how a retry deletes data.

## 1. Connection refused, or the endpoint name does not resolve

*Diagnosis.* The store is down, the container is not on the network the client is using, or the endpoint host is
wrong. Distinguish them by resolving the name from inside the calling process's network namespace.

*Retry.* Safe and idempotent for any operation. Retry with backoff.

*Escalate* when the endpoint resolves but nothing listens after the store's own health check reports healthy: that
is a network attachment problem, not a store problem.

## 2. `403 SignatureDoesNotMatch`

*Diagnosis.* One of five things, and they are not equally likely: the secret key is wrong; the signature version
the client signs with is not the one the endpoint requires; the region in the signing scope is wrong; the clock
has drifted; or the client canonicalised the request differently from the store — commonly over path-style versus
virtual-host addressing, or over a key containing characters that were escaped differently.

*The signature-version cause deserves naming separately because it is the one that gets misdiagnosed.* A client
signing with v2 against an endpoint that requires v4, or the reverse, fails to authenticate with a valid
credential, and the failure is indistinguishable from a wrong secret key by symptom alone. Two pieces of evidence
separate them: the credential works from a different client against the same endpoint, and the two clients differ
in their signature-version setting. **Check the signature version before rotating a credential**, because
rotating one that was never wrong replaces a five-minute configuration fix with a rotation under incident
pressure and leaves the real cause in place. `70-client-libraries.md` owns the rule and states how each client
sets it; `75-mc-command-line-client.md` states the `mc` flag.

The presented error code differs between implementations for this cause — some stores answer
`SignatureDoesNotMatch` and others answer a request-invalid error naming the signing algorithm they expect — so
match on the cause rather than on the code. *The exact codes each store returns need verification*
`[source: https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html, read: unverified as of
2026-07-27]`.

*Retry.* Pointless. The request will fail identically until the configuration changes. Retrying wastes the incident.

*Escalate* immediately, and check clock skew first because it is the only cause that appears and disappears on its
own.

## 3. `403 AccessDenied`

*Diagnosis.* The credential is valid and the policy does not permit this action on this resource. Read the action
and the resource from the request, not from the policy: the common cause is `s3:ListBucket` requested at bucket
scope while the policy grants only object-scope actions.

*Retry.* Never. An access decision does not change under retry.

*Escalate* to whoever owns the policy, with the exact action and resource ARN.

## 4. `404 NoSuchBucket` versus `404 NoSuchKey`

*Diagnosis.* Two entirely different faults behind one status. `NoSuchBucket` means the bucket name is wrong or the
bucket was never provisioned in this environment; `NoSuchKey` means the key computation disagrees with the key that
was written, or the object was removed.

*Retry.* Neither is retryable. Retrying `NoSuchKey` immediately after a write is the one exception worth a single
short re-check, because a listing may lag; a direct `GET` of a just-written key should not.

*Escalate* `NoSuchBucket` as a provisioning defect. Investigate `NoSuchKey` as a key-construction defect and
compare the computed key against the one recorded in the database row.

## 5. `403 InvalidAccessKeyId`, or an expired-token error

*Diagnosis.* The credential was deleted or rotated out from under the process, or a temporary credential expired
and nothing refreshed it.

*Retry.* Only where the client can refresh the credential. Where the credential is a captured static pair, retrying
is a loop that never succeeds.

*Escalate* to a rotation review — see `30-identity-credentials-and-access.md`.

## 6. `503 SlowDown`, or a `5xx` with no body

*Diagnosis.* The store is shedding load or is genuinely failing. A `SlowDown` is explicit backpressure and must be
respected, not out-waited by parallelism.

*Retry.* Safe with backoff and jitter, and with the concurrency reduced rather than held constant.

*Escalate* when the rate persists past the retry budget, or when it correlates with free capacity falling — a full
volume presents this way.

## 7. A timeout part-way through a `PUT`

*Diagnosis.* The request may have completed at the store after the client gave up. This is the unknown-write case.

*Retry.* Safe **for a single-object `PUT` to a fixed key**, because the key determines the object and a repeat
overwrites with identical bytes. Not safe for `CompleteMultipartUpload`: re-check with `ListMultipartUploads` or a
`HEAD` of the destination key first.

*Escalate* nothing; record the outcome as unknown and let the reconciliation path decide, per `SKILL.md` "When the
store fails".

## 8. `CompleteMultipartUpload` fails, or reports `EntityTooSmall`

*Diagnosis.* A part below the minimum size that was not the last part, a missing part number, or an ETag that does
not match the part the store holds. `EntityTooSmall` is a part-sizing defect, not a transient error
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html, read: unverified as of
2026-07-27]`.

*Retry.* Only after re-listing the parts and confirming what the store actually has. A blind retry of completion
fails identically and leaves the parts allocated.

*Escalate* to part sizing in `50-multipart-capacity-and-cost.md`, and abort the upload so the abort rule does not
have to.

## 9. The store's volume is full

*Diagnosis.* Writes fail with a generic server error while reads keep succeeding. That asymmetry is the signature;
confirm against free capacity rather than against the error text.

*Retry.* Useless until capacity is recovered, and harmful because retries add load to a store already in trouble.

*Escalate* immediately, and look first for incomplete multipart parts and noncurrent versions, which are the two
consumers invisible to an object listing.

## 10. TLS handshake or certificate verification failure

*Diagnosis.* An untrusted or expired certificate, a hostname mismatch caused by virtual-host addressing against a
wildcard certificate, or a plaintext endpoint answering a TLS client.

*Retry.* Never; the outcome is deterministic.

*Escalate* without disabling verification. Disabling it converts a loud, correct failure into a silent credential
disclosure.

## 11. A delete returns success and the object is still readable

*Diagnosis.* Versioning is on, so the delete created a delete marker and the previous version remains. The object
is gone from an unversioned read and present to a versioned one, and it is still billed.

*Retry.* Not applicable; the delete succeeded.

*Escalate* to `20-lifecycle-and-retention.md`: a versioned bucket needs a noncurrent-version expiration rule before
any deletion can be described as removal.

## Reporting a storage failure

Name the class from this list, the operation, the bucket, and the outcome for the object — present, absent, or
unknown. **Never put the object key, the presigned URL or the credential in the report**; carry the database row
identifier instead, per `SKILL.md` rule 4.
