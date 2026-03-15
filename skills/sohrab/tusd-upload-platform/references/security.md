# Security Hardening

## Security Baseline

For any public or multi-tenant upload plane, assume:

- the client is untrusted,
- metadata is untrusted,
- upload URLs are sensitive,
- object-store paths and provider URLs are sensitive application state,
- hook endpoints are part of the control plane and must not be left open.

## Safer Defaults

### Authentication and authorization

- Authenticate every client request at the gateway.
- Authorize upload creation in `pre-create`.
- Enforce ownership again at the gateway for `PATCH`, `HEAD`, and `DELETE`.
- Keep provider credentials strictly server-side.

### Transport security

- Prefer TLS termination at a mature reverse proxy or load balancer.
- Use internal TLS or private networking between gateway and tusd if your environment requires it.
- Set `-behind-proxy` when tusd is behind a reverse proxy.

### CORS

- Restrict `-cors-allow-origin` explicitly in production.
- Enable `-cors-allow-credentials` only when the browser truly needs cookies or credentialed requests.
- Expose only the custom headers the client must read.
- If the gateway already handles CORS better, consider `-disable-cors` and own it there.

### Downloads and termination

- Disable downloads unless the upload URL is intentionally also a download URL.
- Disable termination unless the product really supports user cancellation through tus.
- If termination is enabled, protect it with gateway auth and optionally `pre-terminate` policy checks.

## Metadata Handling

Treat upload metadata as user input.

Validate and normalize:

- filename
- content type hints
- tenant or project IDs
- upload purpose
- any provider-specific options

Do not trust client-provided content type as truth. It is a hint, not a guarantee.

## Tenant Isolation

At minimum, isolate by:

- upload record ownership,
- object prefix or path layout,
- retention policy,
- audit trail,
- application-level access control for final asset URLs.

When using local staging, partition paths by tenant or policy domain if that helps cleanup and forensics. Ensure path generation is deterministic and collision-safe.

## Upload IDs and Paths

If you customize upload IDs or local storage paths:

- include a random component such as a UUID,
- do not derive IDs mainly from filenames,
- avoid collisions with tusd sidecar objects such as `.info` and `.part`,
- never let raw user input determine path traversal.

## Hook Service Security

Protect the hook endpoint like control-plane traffic:

- put it on a private network or behind internal auth,
- prefer mTLS or another service-to-service auth layer,
- limit who may call it,
- log every rejection and every policy failure with correlation IDs,
- make the endpoint idempotent and safe for retries.

## Secrets and Credentials

- Store MinIO / S3 credentials in the platform secret manager, not in the client.
- Store upstream provider credentials only in the relay worker or the service that creates upstream uploads.
- Rotate credentials on a schedule.
- Scope credentials narrowly: separate credentials for direct S3 storage vs upstream relay if possible.

## Additional Controls Worth Considering

Depending on the product domain, recommend these as optional layers:

- malware scanning after upload,
- media validation before relay or publication,
- rate limiting at the gateway,
- WAF or abuse controls on public upload endpoints,
- quota checks in `pre-create`,
- retention TTL for unfinished uploads,
- content moderation before final publish.

## Application URLs vs Raw tusd URLs

Prefer application-owned URLs for end-user workflows.

Good pattern:

- tusd handles resumable upload transport,
- your application owns the authoritative asset record,
- users fetch final status and final playback/download links from your application.

That separation reduces coupling and prevents raw upload URLs from becoming long-term product contracts.
