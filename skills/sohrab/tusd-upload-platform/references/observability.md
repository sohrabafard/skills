# Observability and Operations

## Contents

- [Logging](#logging)
- [Metrics Exposed by tusd](#metrics-exposed-by-tusd)
- [What to Alert On](#what-to-alert-on)
- [Dashboards](#dashboards)
- [Correlation IDs](#correlation-ids)
- [Client Exception Reporting With Sentry](#client-exception-reporting-with-sentry)
- [Profiling](#profiling)
- [SLO Thinking](#slo-thinking)
- [Operational Runbook Defaults](#operational-runbook-defaults)


## Logging

### tusd process

Use structured logs by default:

- `-log-format=json`
- keep `-verbose=true` unless the user has a strong reason not to
- send stdout and stderr to the platform log pipeline and SOC tooling

Capture at least:

- timestamp
- service name
- environment
- instance or pod ID
- request or request/trace ID
- upload ID when present
- tenant or account ID when your gateway adds it safely

### Reverse proxy or gateway

Gateway logs matter as much as tusd logs because they are the first place where request buffering mistakes, auth failures, timeout problems, and client abuse appear.

Capture at least:

- request method
- request path template or normalized route
- HTTP status
- upstream status
- bytes in and out
- request duration
- upstream duration
- client IP or trusted forwarded chain
- request ID and request/trace ID
- auth decision outcome when your gateway owns auth

Send gateway logs to the SOC pipeline with the same correlation model as tusd and hook logs.

### Hook service and relay worker

Logs from hooks and workers matter as much as tusd logs because many control-plane failures happen there, not in tusd itself.

Log these consistently:

- hook type
- upload ID
- policy decision
- relay job ID
- upstream asset or upload ID
- retry count
- failure code
- request/trace ID

### Browser client telemetry

Do not treat the browser as the source of truth, but do capture high-value client signals:

- upload session creation failures
- resume attempts
- pause and cancel actions
- terminal upload errors
- user-visible expiration or permission failures

Do not stream raw progress ticks into Sentry. Prefer app analytics, RUM, or sampled custom telemetry for progress trends.

## Metrics Exposed by tusd

### Core tusd metrics

Expect these built-in metrics:

- `tusd_connections_open`
- `tusd_requests_total{method=...}`
- `tusd_errors_total{status=...,code=...}`
- `tusd_bytes_received`
- `tusd_uploads_created`
- `tusd_uploads_finished`
- `tusd_uploads_terminated`
- `tusd_hook_errors_total{hooktype=...}`
- `tusd_hook_invocations_total{hooktype=...}`

### S3-specific metrics

When using the S3-compatible backend, also expect:

- `tusd_s3_request_duration_ms{operation=...}`
- `tusd_s3_disk_write_duration_ms`
- `tusd_s3_upload_semaphore_demand`
- `tusd_s3_upload_semaphore_limit`

### Additional platform metrics worth adding

The surrounding platform should export its own metrics for:

- upload session creation latency and failure rate
- gateway 401, 403, 409, 410, and 5xx rates on upload paths
- relay queue depth and time-to-drain
- staged-file cleanup backlog
- application upload state lag, for example `uploaded_to_staging` to `ready`
- client-observed terminal failures by product surface

## What to Alert On

Use these as the default alert categories:

### Availability

- sustained 5xx growth from `tusd_errors_total`
- gateway health failures or upstream connection saturation
- inability to reach hook service

### Control plane

- non-zero growth in `tusd_hook_errors_total`
- relay queue lag
- relay failure rate
- outbox backlog
- repeated `pre-create` rejections above baseline
- upload session issuance failures above baseline

### Capacity

- local staging disk usage
- S3 temp disk usage on `tusd-s3`
- object store latency spikes via `tusd_s3_request_duration_ms`
- semaphore saturation when `tusd_s3_upload_semaphore_demand` approaches or exceeds the configured limit
- open connection spikes via `tusd_connections_open`
- gateway connection or backend saturation

### Product health

- uploads created but not reaching `ready` state in your application within expected time
- stale unfinished uploads beyond retention
- relay jobs stuck in `queued` or `relaying`
- increasing browser-side terminal failures with 401, 403, 409, or 410 outcomes

## Dashboards

A useful first dashboard has these panels:

1. requests by method from `tusd_requests_total`
2. errors by status and code from `tusd_errors_total`
3. bytes ingested from `tusd_bytes_received`
4. upload lifecycle counters created / finished / terminated
5. hook invocations and hook errors by type
6. S3 request duration percentiles
7. S3 semaphore demand vs limit
8. local disk usage for staging and temp paths
9. relay queue depth and relay success rate from your worker metrics
10. gateway request duration and upstream duration percentiles for upload paths
11. browser upload session failures and terminal error classes

## Correlation IDs

Propagate one request/trace ID end-to-end:

- client -> app session creation endpoint
- app -> browser response with upload session
- browser -> gateway
- gateway -> tusd
- tusd -> hook service via forwarded headers or request body context
- hook service -> queue or outbox
- worker -> upstream provider calls

If the platform already uses `X-Request-Id`, reuse it. Otherwise add a dedicated `traceparent` plus a per-request ID.

## Client Exception Reporting With Sentry

When the browser uses Sentry:

- tag events with app upload ID, tenant or policy domain when safe, target type, and request/trace ID,
- attach coarse upload context such as size bucket or intended asset type,
- scrub raw upload URLs, Authorization headers, cookies, and provider tokens,
- route events through the platform tunnel endpoint if ad blockers or egress policy matter,
- upload source maps so upload failures are debuggable in production.

## Profiling

Use profiling only on internal or temporary diagnostic paths:

- `-expose-pprof=true` only for controlled access
- keep `-pprof-path` private
- never expose profiling endpoints publicly

## SLO Thinking

For a strict upload-plane SLO, split the service into at least three measured promises:

1. **Transport SLO**: the platform accepts, resumes, and completes client uploads successfully.
2. **Control-plane SLO**: session creation, hooks, auth, and queueing behave correctly.
3. **Post-upload SLO**: the platform finishes relay, publication, moderation, or processing within the expected time budget.

This avoids hiding relay failures or auth regressions inside a single vague uptime number.

## Operational Runbook Defaults

Keep these checks in the runbook:

- Is the gateway forwarding requests without buffering?
- Are tusd metrics still exposed and scraping cleanly?
- Is hook error rate rising?
- Is local temp disk full or close to full?
- Is staging disk full or close to full?
- Are relay jobs draining?
- Are shutdowns graceful, or are uploads being cut off?
- Did a proxy or TLS change alter upload speed or resume behavior?
- Is the browser client still honoring current auth, CORS, and service-worker exclusions?
