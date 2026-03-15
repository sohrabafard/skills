# Snippets and Template Guidance

## Recommended CLI Baseline for `tusd-s3`

Adapt this baseline instead of writing flags from scratch:

```bash
tusd \
  -host 0.0.0.0 \
  -port 8080 \
  -base-path /files/ \
  -behind-proxy \
  -disable-download \
  -cors-allow-origin 'https://app.example.com' \
  -hooks-http https://hook-service.internal.example.com/tusd/hooks \
  -hooks-http-forward-headers Authorization,X-Request-Id,X-Correlation-Id \
  -hooks-enabled-events pre-create,post-create,post-receive,pre-finish,post-finish,pre-terminate,post-terminate \
  -progress-hooks-interval 2s \
  -log-format json \
  -metrics-path /metrics \
  -network-timeout 60s \
  -shutdown-timeout 30s \
  -request-completion-timeout 15s \
  -acquire-lock-timeout 20s \
  -s3-bucket uploads \
  -s3-endpoint https://minio.internal.example.com \
  -s3-object-prefix tenant-a/ \
  -s3-part-size 52428800 \
  -s3-min-part-size 5242880 \
  -s3-concurrent-part-uploads 10
```

### Notes

- Add `-disable-termination` unless the product intentionally exposes cancel/delete via tus.
- Add `-cors-allow-credentials` only when browser credentials are actually required.
- Keep a temp volume available even in S3 mode.

## Recommended CLI Baseline for `tusd-staging`

```bash
tusd \
  -host 0.0.0.0 \
  -port 8080 \
  -base-path /files/ \
  -behind-proxy \
  -disable-download \
  -cors-allow-origin 'https://app.example.com' \
  -hooks-http https://hook-service.internal.example.com/tusd/hooks \
  -hooks-http-forward-headers Authorization,X-Request-Id,X-Correlation-Id \
  -hooks-enabled-events pre-create,post-create,post-receive,pre-finish,post-finish,pre-terminate,post-terminate \
  -progress-hooks-interval 2s \
  -log-format json \
  -metrics-path /metrics \
  -network-timeout 60s \
  -shutdown-timeout 30s \
  -request-completion-timeout 15s \
  -acquire-lock-timeout 20s \
  -upload-dir /var/lib/tusd-staging \
  -dir-perms 0750 \
  -file-perms 0640
```

### Notes

- Use a mounted persistent volume for staging.
- Use `ChangeFileInfo.Storage.Path` only for filestore path shaping, not for routing to another backend.
- Keep cleanup jobs and retention policies explicit.

## Gateway Requirements

Whether the gateway is Nginx, HAProxy, Envoy, or app code, preserve these behaviors:

- no request buffering,
- forwarded host and scheme,
- correlation ID propagation,
- optional sticky sessions when scaling stock tusd horizontally,
- auth on every client request,
- separate protection for `/metrics` and any profiling endpoints.

Start from `assets/nginx/tusd-reverse-proxy.conf` when generating a concrete reverse-proxy config.

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
2. auth model
3. hook map
4. storage flow
5. config snippets
6. observability and risks

This sequence keeps the design readable and avoids dumping flags without context.
