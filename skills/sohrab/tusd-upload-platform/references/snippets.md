# Snippets and Template Guidance

## Contents

- [Recommended CLI Baseline for `tusd-s3`](#recommended-cli-baseline-for-tusd-s3)
- [Recommended CLI Baseline for `tusd-staging`](#recommended-cli-baseline-for-tusd-staging)
- [Gateway Requirements](#gateway-requirements)
- [HAProxy Baseline Notes](#haproxy-baseline-notes)
- [Vue.js + Quasar + Vite Client Baseline](#vuejs--quasar--vite-client-baseline)
- [Hook Service Contract: Fields To Read First](#hook-service-contract-fields-to-read-first)
- [Good Response Strategy](#good-response-strategy)
- [Recommended Output Language When Advising Users](#recommended-output-language-when-advising-users)


## Recommended CLI Baseline for `tusd-s3`

Adapt this baseline instead of writing flags from scratch:

```bash
tusd   -host 0.0.0.0   -port 8080   -base-path /files/   -behind-proxy   -disable-download   -cors-allow-origin 'https://app.example.com'   -hooks-http https://hook-service.internal.example.com/tusd/hooks   -hooks-http-forward-headers X-Project-Id,X-User-Id,X-Access,X-Access-Token-Id,X-Request-Id,traceparent,X-User-Mobile,X-User-Fname,X-User-Lname   -hooks-enabled-events pre-create,post-create,post-receive,pre-finish,post-finish,pre-terminate,post-terminate   -progress-hooks-interval 2s   -log-format json   -metrics-path /metrics   -network-timeout 60s   -shutdown-timeout 30s   -request-completion-timeout 15s   -acquire-lock-timeout 20s   -s3-bucket uploads   -s3-endpoint https://minio.internal.example.com   -s3-object-prefix tenant-a/   -s3-part-size 52428800   -s3-min-part-size 5242880   -s3-concurrent-part-uploads 10
```

### Notes

- Add `-disable-termination` unless the product intentionally exposes cancel or delete via tus.
- Add `-cors-allow-credentials` only when browser credentials are actually required.
- Keep a temp volume available even in S3 mode.

## Recommended CLI Baseline for `tusd-staging`

```bash
tusd   -host 0.0.0.0   -port 8080   -base-path /files/   -behind-proxy   -disable-download   -cors-allow-origin 'https://app.example.com'   -hooks-http https://hook-service.internal.example.com/tusd/hooks   -hooks-http-forward-headers X-Project-Id,X-User-Id,X-Access,X-Access-Token-Id,X-Request-Id,traceparent,X-User-Mobile,X-User-Fname,X-User-Lname   -hooks-enabled-events pre-create,post-create,post-receive,pre-finish,post-finish,pre-terminate,post-terminate   -progress-hooks-interval 2s   -log-format json   -metrics-path /metrics   -network-timeout 60s   -shutdown-timeout 30s   -request-completion-timeout 15s   -acquire-lock-timeout 20s   -upload-dir /var/lib/tusd-staging   -dir-perms 0750   -file-perms 0640
```

### Notes

- Use a mounted persistent volume for staging.
- Use `ChangeFileInfo.Storage.Path` only for filestore path shaping, not for routing to another backend.
- Keep cleanup jobs and retention policies explicit.

## Gateway Requirements

Whether the gateway is Nginx, HAProxy, Envoy, or app code, preserve these behaviors:

- no request buffering,
- forwarded host, scheme, and client IP chain,
- request/trace ID propagation,
- optional sticky sessions when scaling stock tusd horizontally,
- auth on every client request,
- separate protection for `/metrics` and any profiling endpoints.

Start from:

- `assets/nginx/tusd-reverse-proxy.conf` for Nginx-based platforms,
- `assets/haproxy/tusd-reverse-proxy.cfg` for HAProxy-based platforms.

## HAProxy Baseline Notes

When adapting the HAProxy asset:

- keep `option forwardfor`,
- set `X-Forwarded-Proto` and `X-Forwarded-Host`,
- keep `option http-buffer-request` disabled,
- set `timeout client` and `timeout server` high enough for large `PATCH` requests,
- add stickiness if more than one stock tusd instance may serve the same upload.

## Vue.js + Quasar + Vite Client Baseline

Use `assets/client/useTusUpload.ts` as the starting point when the browser needs resumable uploads.

Recommended shape:

1. the app asks the backend for an upload session,
2. the browser starts `tus-js-client` with that session,
3. the client forwards safe auth and request tracing headers while the gateway injects trusted internal headers,
4. the UI exposes pause, resume, cancel, and retry states,
5. terminal failures are reported to Sentry without leaking raw upload URLs.

If SSR is enabled, register the upload boot file as client-only. If PWA is enabled, exclude upload routes from service-worker caching.

## Hook Service Contract: Fields To Read First

From the hook request, the most useful fields are usually:

- `Type`
- `Event.Upload.ID`
- `Event.Upload.Size`
- `Event.Upload.Offset`
- `Event.Upload.MetaData`
- `Event.Upload.Storage`
- `Event.HTTPRequest.Method`
- `Event.HTTPRequest.URI`
- `Event.HTTPRequest.RemoteAddr`
- `Event.HTTPRequest.Header`

## Good Response Strategy

### For `pre-create`

- return 2xx with no body changes when allowed,
- return 4xx-like semantic information through `HTTPResponse` plus `RejectUpload` when denied.

### For `post-receive`

- stop the upload only when the business state really changed or policy was revoked,
- keep the decision fast and deterministic.

### For `pre-finish`

- return tiny response hints such as an app-side upload record URL,
- do not block on downstream publishing.

### For `post-finish`

- write a durable job and return quickly.

## Recommended Output Language When Advising Users

When producing a concrete solution, present it in this order:

1. topology
2. proxy choice
3. auth model
4. hook map
5. client upload flow when relevant
6. storage flow
7. config snippets
8. observability and risks

This sequence keeps the design readable and avoids dumping flags without context.
