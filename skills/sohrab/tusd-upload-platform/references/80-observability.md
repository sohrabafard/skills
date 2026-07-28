# Observability

Signal **names and values** — event names, log field names, metric families, `OTEL_*` defaults, Ala timeout and retry numbers — belong to `/alaa-services-contract` (`$alaa-services-contract`). **Requirement levels, gates and reasons** belong to `/alaa-observability-soc` (`$alaa-observability-soc`). This file states only what is specific to an upload plane: what to record about an upload, what must never be recorded, and what a signal has to tell you that a request-response service's signals do not.

## What makes an upload plane different

An upload is long-lived, resumable, and spans more hops than one request. Three consequences:

- **A per-request view is not enough.** One upload is many requests across a variable span of time, so the unit of analysis is the upload, joined by its identifier, not the request.
- **Success at the transfer layer is not success for the user.** The signal that matters is time from upload start to asset readiness, which crosses the transfer layer, the control plane and the workers.
- **Cardinality is dangerous here.** An upload identifier, a tenant identifier or a filename in a metric label multiplies series by traffic. Put them in logs and traces; never in a label.

## Never record

Upload URLs, object keys, bucket names, filenames, raw `Upload-Metadata`, `Authorization` headers, cookies, trusted internal header values, storage or provider credentials, signed internal URLs, file contents, manifest contents, and full archive listings. This applies to logs, metric labels, trace attributes, error reporters and client analytics alike.

Join on the application upload identifier, the request id and the trace id. All three are safe and all three are sufficient.

## What to record, by component

**Transfer layer.** Structured, one line per decision rather than per byte: the upload identifier, the method, the status, the offset before and after, the bytes accepted, and the tenant only where the platform's field policy permits it.

**Front door.** Method, normalised route, status, upstream status, bytes in and out, request and upstream duration, client-IP chain, request id, and the authorization outcome where the front door owns it. Front-door logs are where buffering mistakes, timeout mistakes and abuse first become visible, before the transfer layer sees anything at all.

**Control plane and workers.** The lifecycle event, the upload and asset identifiers, the decision and its reason code, the job identifier, the attempt number, the failure code, and the correlation identifiers. This is where most upload-plane failures actually live.

**Browser.** Plan-creation failures, resume attempts, pause and cancel actions, terminal errors, and expiry or permission failures. Never raw progress into an error reporter.

## Metrics an upload plane needs

Names come from `/alaa-services-contract` (`$alaa-services-contract`). The **quantities** are:

- requests by method and status on upload paths;
- bytes accepted;
- uploads created, finished, terminated;
- hook or callback invocations and failures **by hook**, because a single aggregate hides the one that fails open;
- object-store request duration and error rate;
- part-upload concurrency demand against its limit;
- temp and staging disk utilisation;
- queue depth, oldest-item age, and time to drain for downstream work;
- count of uploads eligible for reclamation and count reclaimed per reaper run;
- count of temporary objects older than the expected finalization window;
- upload-plan creation latency and failure rate;
- time from upload start to asset readiness, as a distribution.

**Two of these exist because of failures this skill has seen and nothing else will surface them:** the reaper's eligible-versus-reclaimed pair, which is the only way a stalled reaper becomes visible before the disk fills; and the aged-temporary-object count, which is the only way a permanent two-copy leak becomes visible before the bill arrives.

## Alerting

Alert on a symptom a human can act on, with a threshold set from a measured baseline. Every threshold shipped in `assets/prometheus/tusd-alert-rules.yml` is a variable for exactly that reason.

| Class | Alert on |
|---|---|
| Availability | sustained growth in 5xx on upload paths; the transfer layer unreachable from the front door; the hook endpoint unreachable |
| Control plane | any growth in hook or callback failures; plan-creation failure rate above baseline; creation rejections above baseline, which is usually a client release or an attack |
| Capacity | temp and staging disk against the thresholds in `35-storage-lifecycle.md`; part-upload concurrency at its limit; object-store latency |
| Retention | reaper eligible count growing across consecutive runs; aged temporary objects above the expected window |
| Product | uploads created but not reaching readiness within the stated budget; downstream backlog oldest-item age; growth in client-observed terminal failures |

## Correlation

One identifier travels the whole path: client to control plane, control plane to client in the plan, client to front door, front door to transfer layer, transfer layer to hook or callback, hook to the durable row, worker to any provider call. Where the platform uses `X-Request-Id` and `traceparent`, reuse both; validate them on arrival, generate them when absent, and echo them on every response.

**Propagate the identifier into the creation-time gate specifically.** That call decides whether the upload happens at all, and an incident that starts there is otherwise unlinkable to the client that caused it.

## Declaring is not wiring

A catalog of events with required and forbidden fields is a contract, not an implementation. A service whose event sink is never populated emits nothing and looks, from the catalog, fully instrumented — which is the state the Ala service is in today, recorded in `15-ala-service.md`. `55-tests.md` names the test that catches it: assert every declared event is emitted by non-test code.

The same applies to metrics. A metrics endpoint that returns hardcoded zeros scrapes cleanly, satisfies a health check, and tells you nothing. Assert that at least one counter moves when work happens.

## SLOs

Split the plane into three measured promises so that a failure in one is not hidden by the others:

1. **Transport** — the plane accepts, resumes and completes client uploads.
2. **Control plane** — plan creation, authorization, hooks and enqueueing behave correctly.
3. **Post-upload** — relay, extraction, moderation or publication finishes within its budget.

A single uptime number hides a plane that accepts every byte and never makes a single asset ready.
