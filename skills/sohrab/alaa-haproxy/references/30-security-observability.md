# Alaa HAProxy Security and Observability Checklist

## Security

- Run as a non-root user when binding only high ports inside containers or pods.
- Keep admin sockets on local unix sockets with tight permissions.
- Never expose the Runtime API directly through a Service or public listener.
- Keep TLS private keys, ticket keys, maps with secrets, and ACME state out of git.
- Be explicit about where TLS is terminated and where it is re-established.
- Use `strict-sni` intentionally in multi-tenant frontends.
- Validate backend certificates when HAProxy talks TLS to upstream services.
- Use PROXY protocol only when both sides explicitly support it.
- Audit deprecated `3.3` features before rollout so warnings do not hide real risk.

## Logging

- Use a stable log format that includes:
  - request ID
  - client address or trusted forwarded address
  - frontend and backend name
  - server name
  - status code
  - timing fields
- Add `%[term_events]` for richer incident forensics.
- Avoid logging secrets, full Authorization headers, or certificate details that are not needed.

## Metrics

- Track frontend and backend traffic, retries, errors, queue depth, and saturation.
- Keep scrape endpoints cluster-private when possible.
- On `3.3`, decide whether persistent stats across reloads are worth the experimental feature tradeoff.

## Traces and runtime inspection

- Use `show info`, `show stat`, `show errors`, and `show events` as the first triage layer.
- Use `trace ssl` or `trace acme` only for bounded investigations.
- Turn off heavy tracing after the incident.

## Reload and drain safety

- Test graceful reload under live traffic.
- Test preStop or shutdown behavior in Kubernetes before production.
- Ensure readiness fails before the pod fully exits so traffic drains cleanly.

## Cross-service integration checks

- upstream service discovery source verified
- backend health endpoint reflects real readiness
- request ID reaches application logs
- mTLS trust chain matches the upstream certificates
- monitoring stack can scrape metrics after every rollout
