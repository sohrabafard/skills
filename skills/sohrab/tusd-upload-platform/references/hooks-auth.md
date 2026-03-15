# Hooks and Authorization

## Core Rule

Use hooks for policy decisions and lifecycle signals, but use the gateway for request-by-request ownership enforcement.

That split keeps blocking hooks small and reliable while still protecting `PATCH`, `HEAD`, and `DELETE` in security-sensitive systems.

## Recommended Responsibilities by Hook

| Hook | Blocking | Use it for | Do not use it for |
|---|---|---|---|
| `pre-create` | Yes | authenticate actor, authorize upload intent, validate metadata, enforce size and target rules, set custom ID/metadata | long database workflows, remote uploads, virus scanning, transcoding |
| `post-create` | No | register upload creation, audit logging, analytics, bookkeeping | any action that must complete before upload starts |
| `post-receive` | No | periodic ownership/resource checks, stopping uploads when business state changed, progress telemetry | primary authorization model, expensive external work |
| `pre-finish` | Yes | add a small response hint, return an app URL, attach a request-scoped header | long processing, relay upload, anything that must be retryable later |
| `post-finish` | No | enqueue durable jobs, publish events, start relay workflow | doing the full relay inline, volatile work without durable retries |
| `pre-terminate` | Yes | reject termination if policy forbids it | heavy cleanup |
| `post-terminate` | No | cleanup bookkeeping and alerts | anything that must block deletion |

## The Secure Authorization Pattern

### Step 1: Authorize upload creation

In `pre-create`:

- validate the caller identity from `Authorization`, `Cookie`, or signed app metadata,
- validate tenant, project, upload purpose, and target backend,
- validate declared size and metadata,
- persist or confirm an application upload record,
- add normalized metadata needed by later hooks and workers.

### Step 2: Bind upload ID to ownership in your application

Store at least:

- `upload_id`
- `owner_subject`
- `tenant_id`
- `target_type`
- `status`
- `declared_size`
- `filename`
- `requested_content_type`
- `correlation_id`
- timestamps for creation and last activity

Use `assets/schemas/upload-record.schema.json` as a starting point.

### Step 3: Enforce ownership on every request at the gateway

For `PATCH`, `HEAD`, and `DELETE`:

- authenticate the caller at the gateway,
- extract the tus upload ID from the URL,
- look up the upload record,
- confirm the caller is allowed to touch that upload,
- forward the request only if allowed.

This is the correct place to compensate for the fact that stock tusd does not guarantee the same actor resumes the upload.

## Why hooks alone are not enough for ownership enforcement

`pre-create` protects the initial `POST`, but later requests use the upload URL. That makes the upload URL effectively a capability. This may be acceptable for low-risk systems, but not for high-security multi-tenant platforms. When the user’s requirements mention security sensitivity, ownership, or explicit permission checks, add gateway-side verification for every request.

## Hook Transport Guidance

### Default: HTTP hooks

Use HTTP hooks when you need:

- one central hook service,
- shared application state,
- language flexibility,
- easy mTLS, auth, and observability integration.

Forward request headers that matter operationally, for example:

- `Authorization`
- `Cookie`
- `X-Request-Id`
- `X-Correlation-Id`
- tenant headers if they are part of your trust model

### gRPC hooks

Use gRPC hooks only when the platform already operates gRPC well and wants stricter contracts or lower overhead.

### File hooks

Keep file hooks for local development, demos, or intentionally simple single-instance setups.

## Idempotency Rules

Design all hook side effects to tolerate retries and duplicates.

### Mandatory idempotency points

- `pre-create`: safe to run again for the same business request.
- `post-create`: safe to record "already created" without duplicate business artifacts.
- `post-finish`: safe to enqueue the same relay job key more than once.
- `post-terminate`: safe to run cleanup on already-cleaned state.

## Queue and Outbox Pattern

Use this pattern whenever `post-finish` should trigger further work:

1. `post-finish` receives the event.
2. Hook service writes a durable outbox row or queue message keyed by upload ID.
3. Hook service returns success quickly.
4. Worker consumes the job and performs relay, moderation, scanning, notification, or publication.
5. Worker updates the upload record state.

This is the safest pattern because hook-triggered work may be concurrent, may arrive out of order for different event types, and must not depend on the client connection still being alive.

## Use `pre-finish` Carefully

Use `pre-finish` only for small, fast response decoration, for example:

- an application asset URL,
- an internal upload record ID,
- a state token telling the client to poll your app.

Never make `pre-finish` the only place where the final asset URL exists. Persist the same information in your application database because the client may miss that one response.

## Upstream Relay Pattern

When relaying to another tusd / provider upload server:

- stage the client upload on your side first,
- create a durable relay job in `post-finish`,
- upload from the worker using your service-owned credentials,
- store provider URL / asset ID in your DB,
- only then tell the application the asset is ready.

Do not inject your provider token into browser uploads. Do not proxy raw provider tokens through the browser. Do not assume the provider will ever offer the hooks you need.

## Example Hook Responses

### Reject unauthorized upload in `pre-create`

```json
{
  "HTTPResponse": {
    "StatusCode": 403,
    "Body": "{\"message\":\"upload not allowed\"}",
    "Header": {
      "Content-Type": "application/json"
    }
  },
  "RejectUpload": true
}
```

### Stop an upload in `post-receive`

```json
{
  "HTTPResponse": {
    "StatusCode": 409,
    "Body": "{\"message\":\"upload permission was revoked\"}",
    "Header": {
      "Content-Type": "application/json"
    }
  },
  "StopUpload": true
}
```

### Attach an app URL in `pre-finish`

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

If JavaScript must read custom headers, remember to expose them through CORS.

## Anti-Patterns

Avoid these suggestions unless the user explicitly insists and understands the risk:

- authenticate only in `pre-create` for a security-sensitive public upload plane,
- do database transactions or large cross-service work in blocking hooks,
- relay staged files to upstream synchronously inside `post-finish`,
- depend on `post-create` occurring before `post-finish`,
- use metadata alone as a trust boundary when gateway auth can be enforced,
- expose raw tusd URLs as long-term application asset URLs.
