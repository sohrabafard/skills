# Hooks, Callbacks and Their Failure Posture

A hook is where an upload plane makes a decision or records a fact. This file states, for each one, what it is for, how long it may take, and **what happens when it fails**. An unstated posture is read as fail-open by the next agent to arrive, so every entry below states one.

## The two postures, and the question that picks between them

- **Fail-closed.** The call decides whether a caller may act. When it cannot decide, it denies. Nothing proceeds.
- **Fail-open and loud.** The call only records. Its failure denies nothing, so it must log its own failure and increment a metric, because the operation continues with a gap in the record.

The deciding question is never how important the call is. It is: **what does its failure let through?** A creation gate that fails open lets an unauthorized upload start. A recording call that fails closed rejects an upload that was already authorized and already paid for in bytes. Doctrine is `/alaa-security-review` (`$alaa-security-review`) for the first and `/alaa-reliability-sla` (`$alaa-reliability-sla`) for the second.

**There is no third posture.** "Fail open and silent" is the defect this file exists to prevent: it produces a plane that is wrong and looks healthy.

## Responsibility and posture by hook

Register (a), the tusd binary and the library. `pre-` events are blocking; `post-` events are not.

| Hook | Blocking | Use it for | Never use it for | On failure |
|---|---|---|---|---|
| `pre-create` | yes | authenticate, authorize the intent, validate metadata, enforce the size cap and the target, set the id | database workflows, remote calls, scanning | **fail closed**: deny creation |
| `post-create` | no | register the creation, audit, analytics | anything that must complete before bytes flow | **fail open, loud**: log and count; the record is now missing |
| `post-receive` | no | periodic re-check of the actor's right, progress telemetry, stopping a revoked upload | the primary authorization model, expensive external work | **fail open, loud**: the upload continues under the creation-time decision |
| `pre-finish` | yes | one small response hint | anything that must be retryable, anything long | **fail closed**: the completion response fails; the bytes are still stored |
| `post-finish` | no | write a durable job or outbox row, publish an event | performing the downstream work inline | **fail open, loud**: the client sees success and nothing downstream runs |
| `pre-terminate` | yes | refuse a termination that policy forbids | heavy cleanup | **fail closed**: deny termination |
| `post-terminate` | no | cleanup bookkeeping and alerting | anything that must block deletion | **fail open, loud** |

Two ordering guarantees hold and no others: `pre-create` is first for an upload, and `post-finish` starts after `pre-finish` completes. Never write code that depends on `post-create` being observed before `post-finish`.

## Authenticating the hook endpoint itself

In register (a) the hook endpoint is a control-plane service reachable over the network, and it accepts a payload that decides authorization. It needs its own authentication, and this is a requirement rather than a preference.

1. **The hook endpoint authenticates its caller as the transfer layer.** Choose one named mechanism and name it in the deployment: mutual TLS with a client certificate issued for that purpose, or a shared secret carried in a header that is verified in constant time and rotated on a stated schedule. A private network alone is placement, not authentication.
2. **Forwarding the client's credentials to the hook is a different thing and does not substitute.** `-hooks-http-forward-headers` gives the hook the *client's* context so it can decide about the client; it says nothing about who called the hook.
3. **The endpoint refuses a call it cannot authenticate**, with the same code every time, and logs it.
4. **The endpoint is idempotent**, because the transport retries by default: 3 attempts on a 5xx or a network error, 1 s apart.
5. Bound the work: 15 s transport timeout, 5 KiB response limit. A blocking hook's latency is the client's latency.

## In-process callbacks — the embedded case

An embedded service has no hook transport, so items 1 to 4 above do not apply and the callbacks are ordinary function calls. Three things change, and each is a trap:

- **The failure posture must still be stated per callback**, because now it is expressed as `return err` versus `_ = err`, and the second form is invisible in review.
- **A discarded error is a silent divergence.** The Ala service discards the error from each of its three post-transfer synchronisers and logs nothing. The consequences are concrete: a failure at creation leaves bytes accumulating in object storage with no control-plane row, and a failure at completion returns `204` to a client whose session never leaves `created`, so the asset can never be completed and nothing says why. Both are recorded as service defects in `15-ala-service.md`.
- **Notification channels are not callbacks.** See the notification-channel contract in `25-upstream-library.md`: the handler's send blocks the request, so drain from a long-lived goroutine and read everything from the event rather than from the ambient request.

## Response shapes

Register (a). A hook response may deny creation, stop an upload in progress, or shape the HTTP response the client receives.

Reject a creation:

```json
{
  "HTTPResponse": {
    "StatusCode": 403,
    "Body": "{\"message\":\"upload not allowed\"}",
    "Header": { "Content-Type": "application/json" }
  },
  "RejectUpload": true
}
```

Stop an upload whose permission was revoked mid-transfer:

```json
{
  "HTTPResponse": {
    "StatusCode": 409,
    "Body": "{\"message\":\"upload permission was revoked\"}",
    "Header": { "Content-Type": "application/json" }
  },
  "StopUpload": true
}
```

Attach a hint at completion:

```json
{
  "HTTPResponse": {
    "Header": {
      "Link": "<https://app.example.com/uploads/abc123>; rel=\"related\"",
      "X-App-Upload-Id": "abc123"
    }
  }
}
```

A header the browser must read has to be exposed through CORS, or it is invisible to JavaScript even though it arrived.

**A completion hint is never the only copy of a piece of data.** The client may miss that response — the connection may drop after the server wrote it — so the same information must be readable from the application afterwards.

## Idempotency

Every hook side effect runs more than once eventually: the transport retries, a worker replays, a client repeats a request. Doctrine, including how to derive a key and why it must not come from request content, is `/alaa-reliability-sla` (`$alaa-reliability-sla`). The upload-plane obligations are:

- creation-time authorization is safe to run again for the same business request;
- creation registration records "already created" without producing a second business artifact;
- completion enqueues the same downstream job key more than once without producing duplicate work;
- termination cleanup is safe against already-cleaned state.

## Enqueue, do not perform

Whenever completion must trigger further work, the sequence is fixed:

1. Completion receives the event.
2. The handler writes a durable row keyed by the upload identifier, in the same transaction as the state change where the storage allows it.
3. The handler returns immediately.
4. A worker consumes the row and performs the relay, moderation, scan, notification or publication.
5. The worker updates the record.

This is not a style preference. Hook-triggered work may be concurrent, may arrive out of order across event types, and must not depend on the client's connection still being alive. Anything performed inline in a non-blocking hook is lost when the process restarts, and nothing will tell you it was lost.
