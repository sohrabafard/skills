# Failure Modes

Nine classes. Each gives the symptom as observed, the diagnosis that separates it from its neighbours, the smallest safe retry, and the escalation point. Read the class that matches the symptom; do not read the file end to end during an incident.

Retry legality and backoff shape are `/alaa-reliability-sla` (`$alaa-reliability-sla`). This file says only *whether* retrying this particular thing is safe and *what* to retry.

## 1 — Upload stalls partway and never resumes

**Symptom.** Progress stops at a repeatable percentage, or at a repeatable elapsed time. `PATCH` ends without a status the client can classify.

**Diagnosis.** A repeatable *percentage* points at a size limit: a body cap on some hop, or the object store's part ceiling. A repeatable *elapsed time* points at a timeout: a client timeout, a connect or read timeout on a proxy, or an idle timeout on a load balancer. Ask the client for the bytes transferred at failure and compare it against every body cap on the path. Then issue a `HEAD` and compare the offset to what the client believed.

**Smallest safe retry.** `HEAD`, then `PATCH` from the returned offset. Resume is the designed recovery and re-uploading from zero discards work that the server already holds.

**Escalate when.** The offset does not advance across two clean attempts, or `HEAD` returns an offset lower than a previously acknowledged one — that is data loss in the store, not a transport problem.

## 2 — Resume returns the wrong upload

**Symptom.** After a project switch, an account switch or a logout, resuming attaches to an upload the user did not start, or a file's progress appears against the wrong item.

**Diagnosis.** The client's stored fingerprint was matched by file identity alone rather than against the current upload's application identifier. Confirm by clearing local storage and repeating: if the fault vanishes, it is client-side matching.

**Smallest safe retry.** None. Clear the stored fingerprint and start a new upload. Retrying reproduces the fault.

**Escalate when.** The wrong upload belonged to a different tenant. That is a data-exposure event, not a bug: it means the per-method ownership check in `40-authorization.md` is absent or is passing on a stale identity.

## 3 — Offline reported as permanent failure

**Symptom.** Losing connectivity mid-upload leaves a terminal error in the UI, and reconnecting does not resume.

**Diagnosis.** The client set a paused state and then declined to retry, which made the transport emit its terminal error path, which overwrote the state. Look for a status assignment inside the retry decision followed by another assignment in the error handler.

**Smallest safe retry.** Resume from `HEAD` once connectivity returns; the server state is intact.

**Escalate when.** The server's stored offset is behind what the client acknowledged.

## 4 — Authorization succeeds at creation and fails afterwards

**Symptom.** Creation returns success; the first `PATCH` or `HEAD` returns 401 or 403.

**Diagnosis.** Separate three causes. An expired token means the client refreshed nothing between the plan and the transfer. A missing trusted header means the front door forwarded the creation path and not the transfer path — check whether both paths traverse the same rule. A permission denial on a *stored* target service that differs from the client's means the caller changed target mid-flight, which is the control working.

**Smallest safe retry.** Refresh the credential through the normal flow, then resume. Never retry a 401 or 403 blindly; a retry loop against an authorization failure is indistinguishable from an attack in the logs.

**Escalate when.** The same caller alternates between success and denial on identical requests — that is a stale or partially propagated permission set, and it belongs to `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).

## 5 — Bytes exist with no control-plane record

**Symptom.** Object storage holds objects whose identifiers appear in no application row. Storage grows faster than the record count.

**Diagnosis.** A creation-time recording call failed and its error was discarded. Confirm by counting objects under the transfer layer's prefix against rows in the ownership table for the same window. A silent post-hook produces exactly this and emits nothing.

**Smallest safe retry.** Reconcile forward: for each orphan, look up the intent by the identifier embedded in the key. Never delete on the strength of a missing row alone, because a row that is merely late looks identical to one that never existed.

**Escalate when.** The orphan count grows monotonically. That is the silent-discard defect, not a transient one, and it needs the code change in `45-hooks.md`.

## 6 — Transfer completes, the asset never becomes usable

**Symptom.** The client sees success from the transfer layer. The application record stays in its initial state forever, and completion is refused.

**Diagnosis.** The completion-time recording call failed silently, so the state transition never happened even though the bytes are whole. Distinguish from a downstream processing failure by reading the record's state: stuck at the *initial* state means the completion sync was lost; stuck at *processing* means a worker is the problem, class 7.

**Smallest safe retry.** Re-derive the state from the transfer layer's offset and the declared size, and apply the transition. This is idempotent and is the correct manual repair.

**Escalate when.** It recurs. A client cannot recover from this on its own and will retry forever against a plane that returns success.

## 7 — Downstream work never drains

**Symptom.** Records sit in a queued or processing state. Queue depth or outbox backlog grows. No error appears in the transfer layer's logs, because the fault is not there.

**Diagnosis.** Separate three: no worker is running; workers run and fail on every item, which is a poison message; workers run and are simply outpaced. The claim mechanism tells you which — with lease-based claiming, a stuck item whose lease keeps expiring and being reclaimed is a poison message, whereas a growing set of never-claimed items is a capacity problem.

**Smallest safe retry.** Reclaim after lease expiry, which a lease-based claim design does on its own. For a poison message, move it aside and continue; do not let one item hold the lane.

**Escalate when.** The backlog's oldest item exceeds the product's stated latency for readiness. Broker, DLQ and replay behaviour belong to `/alaa-async-messaging` (`$alaa-async-messaging`).

## 8 — Local disk fills

**Symptom.** Concurrent uploads fail together. Writes fail with no space. The object store is healthy and has plenty of room.

**Diagnosis.** S3 mode buffers parts locally, roughly 1 GiB per in-flight upload at upstream defaults, and "streams to object storage" hides it. Multiply current concurrency by `MaxBufferedParts × PreferredPartSize` and compare with the volume. A staging plane has the second cause too: successfully relayed files that cleanup never removed.

**Smallest safe retry.** None while the disk is full. Stop accepting **new** creations and let in-flight uploads drain; retrying a `PATCH` into a full disk destroys work already done.

**Escalate when.** Utilisation returns after cleanup runs. That is a retention gap, not a capacity gap, and `35-storage-lifecycle.md` has the rule it is missing.

## 9 — Deploy or restart truncates uploads

**Symptom.** Uploads fail in a burst that coincides exactly with a rollout. Failures cluster on large files.

**Diagnosis.** The graceful-shutdown budget is shorter than a legitimate long `PATCH`, or the orchestrator's termination grace period is shorter than the shutdown budget, so the process is killed while draining. Compare three numbers: the longest legitimate `PATCH`, the shutdown budget, and the termination grace period. They must be in ascending order.

**Smallest safe retry.** Resume from `HEAD`; a clean graceful shutdown truncates the request and preserves the offset.

**Escalate when.** The offset after a restart is lower than the client's last acknowledged offset, which means the shutdown was not clean.

## The ambiguous outcome, which cuts across all nine

A timeout after the request bytes were written tells you nothing about whether the work happened. A connection refusal and a timeout are different events and must not share a code path: the first is safe to retry, the second is not, unless the operation is idempotent by construction.

For an upload plane this has one concrete consequence. A `PATCH` that times out may have been fully applied, so the client must not resend the same chunk blindly — it must `HEAD` first and resume from the server's offset. A creation call that times out may have created the upload, so the retry must carry the same idempotency key and be recognised, or the plane accumulates duplicate uploads that each hold storage. Mechanics are `/alaa-reliability-sla` (`$alaa-reliability-sla`); the obligation is stated here because an upload plane is where it costs bytes.
