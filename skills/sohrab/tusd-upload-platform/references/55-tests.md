# Required Tests

Every test below names a behaviour that a plausible-looking implementation gets wrong. A change to an upload plane is not finished until the tests covering the behaviour it touched exist and pass. Layering doctrine — which of these is a unit, an integration or an end-to-end test — is `/alaa-testing-strategy` (`$alaa-testing-strategy`); this file names what must be proven, not where.

## Resume and offset

| Test | What it proves | A broken implementation |
|---|---|---|
| Kill the connection at 40 % of a large upload, then `HEAD`, then `PATCH` from the returned offset and let it complete. Assert the stored object's size equals the declared size. | resume works end to end through every hop, and the front door does not buffer or rewrite the offset | completes with a truncated or doubled object, or `HEAD` returns 0 |
| Restart the transfer process mid-`PATCH` with a graceful signal, then resume. | the shutdown budget exceeds the drain, and the offset survives | the offset regresses, or the upload cannot resume |
| Resume after a project switch with a stored fingerprint from the previous project. | the client matches a stored upload against the current application identifier | resumes the wrong upload — the class 2 fault in `50-failure-modes.md` |
| Go offline mid-upload, then reconnect. Assert the client state is the paused state and not the terminal one, and that resume succeeds. | the offline path does not fall through to the terminal error handler | reports permanent failure while the server holds a resumable upload |

## Authorization

| Test | What it proves | A broken implementation |
|---|---|---|
| Replay another tenant's upload id on `HEAD`, `PATCH` and `DELETE` with otherwise valid context. Assert denial **before any byte is accepted**, and assert the response is identical to the response for a non-existent id. | per-method ownership runs ahead of the transfer handler and the boundary does not confirm existence | accepts bytes then rejects, or returns a distinguishable status |
| Send each trusted header missing in turn. Assert a distinct failure code per header. | context failures are diagnosable individually | one generic failure for six causes |
| Send a client-supplied copy of a trusted header directly to the service, bypassing the gateway. Assert it is not honoured. | stripping actually happens somewhere on the path | the client escalates its own privileges |
| Request a target service the caller lacks the permission bit for, at creation **and** at completion. Assert denial at both. | completion re-checks against the stored target, not the client's | a caller changes target mid-flight |
| Assert no generated permission name contains `extract`, `protocol`, `complete` or `delete`. | a catalog change that would silently alter authorization breaks the build instead | the plane's authorization model changes without a code change |

## Size and metadata

| Test | What it proves | A broken implementation |
|---|---|---|
| Create an upload with `Upload-Length` above the configured cap. Assert rejection at creation, before any byte. | the cap is enforced by the handler and not merely advertised | accepts and fails mid-transfer, or accepts entirely |
| Compare the advertised `Tus-Max-Size` with the configured cap. Assert they are equal. | the plane does not lie to clients | advertises a cap it does not hold |
| Create with `Upload-Length` that disagrees with the declared size in the plan. Assert a distinct conflict status. | declared size is bound to the intent | a client uploads a different file than it declared |
| Send a metadata filename containing `../` and a filename containing non-ASCII bytes. Assert the stored path is unaffected and the upload still succeeds. | metadata never reaches a path segment | path traversal, or a spurious rejection of a legitimate name |
| Send a metadata key outside the allowlist. Assert rejection rather than silent ignoring. | the allowlist is enforced, not decorative | unbounded client-controlled data reaches storage |

## Hooks and failure posture

| Test | What it proves | A broken implementation |
|---|---|---|
| Make the creation-time gate fail — stop the hook endpoint, or force the callback to error. Assert `POST` is denied and no upload exists. | the gate is fail-closed | an unauthorized upload starts because the gate was unreachable |
| Make a recording call fail. Assert the operation still succeeds **and** that a log line and a metric record the loss. | the posture is fail-open and loud, not silent | the divergence is invisible until storage is audited |
| Call the hook endpoint directly without the transfer layer's credential. Assert refusal. | the hook endpoint authenticates its caller | anyone on the network can authorize an upload |
| Send the same completion event twice. Assert one downstream job. | completion is idempotent | duplicated downstream work per retry |
| Drive concurrent uploads through one handler and assert every notification is processed against its own upload. | notification draining has no cross-request leakage | one request's drain consumes another's event |

## Storage and retention

| Test | What it proves | A broken implementation |
|---|---|---|
| Complete an upload and assert the object appears only at completion and under a server-generated key with no client-supplied segment. | key construction is server-owned | client input reaches the key |
| Where finalization copies an object, assert both copies exist during the window and only one after cleanup. | the two-copy window is bounded | storage doubles permanently on cleanup failure |
| Start an upload, abandon it, advance the clock past the retention threshold, run the reaper. Assert the row, the bytes **and** the multipart upload are all gone, and that the reaper's counters moved. | retention covers all three, and a stalled reaper is visible | bytes or multipart state leak invisibly |
| Fill the temp volume past the second threshold. Assert new creations are refused with a retryable status and in-flight uploads still complete. | disk pressure sheds the right load | in-flight work is destroyed under pressure |

## Client

| Test | What it proves |
|---|---|
| Render an SSR page that imports the upload module. Assert no browser global is touched during server render. | the browser boundary holds |
| Register the service worker and run an upload. Assert no upload request is intercepted or cached. | the exclusion list covers every upload route |
| Force a 401 and a 403. Assert no retry loop. | authorization failures are terminal to the client |
| Force a 409 and a 423. Assert bounded retries with jitter and a finite end. | the retry budget is bounded and not synchronised across clients |
| Emit a telemetry event for a failed upload. Assert no URL, key, filename, trusted header value or credential appears in the payload. | redaction runs on the path that actually reports |

## Observability

| Test | What it proves |
|---|---|
| Complete one upload and assert a single trace links the control-plane call, the transfer and the downstream work. | correlation propagates across every hop |
| Assert every metric emitted has bounded label cardinality, with no upload id, no tenant id and no filename in a label. | metrics cannot be exploded by traffic |
| Scrape the metrics endpoint from outside the internal network. Assert refusal. | the endpoint is not public |
| Assert every event the service claims to emit is emitted by non-test code. | the contract is wired, not merely declared |
