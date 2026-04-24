# Source Map

Use this file when tusd guidance depends on current protocol, server, client, security, proxy, or release behavior.

## Source Priority

Prefer sources in this order:

1. The tus protocol specification and official tus organization docs:
   - Protocol: https://tus.io/protocols/resumable-upload
   - Implementations: https://tus.io/implementations
2. Official tusd documentation and release notes:
   - Configuration: https://tus.github.io/tusd/getting-started/configuration/
   - Hooks: https://tus.github.io/tusd/advanced-topics/hooks/
   - Storage backends: https://tus.github.io/tusd/storage-backends/
   - GitHub releases: https://github.com/tus/tusd/releases
3. Official tus-js-client docs and releases:
   - Repository: https://github.com/tus/tus-js-client
   - Releases: https://github.com/tus/tus-js-client/releases
4. Official docs for the selected proxy and storage target: Nginx, HAProxy, S3 provider, MinIO, Kubernetes, or cloud load balancer docs.
5. Community issues, StackOverflow answers, and blog posts only as troubleshooting leads.

## Current Release Snapshot

Checked on 2026-04-24:

- `tus/tusd` latest GitHub release: `v2.9.2`, published 2026-03-11.
- `tus/tus-js-client` latest stable GitHub release observed in official releases: `v4.3.1`; a `v5.0.0-pre2` prerelease exists and must not be assumed stable without explicit approval.

Refresh this snapshot before version-sensitive work.

## Freshness Triggers

Re-check official sources before asserting:

- current tusd flags, hook payload fields, hook ordering guarantees, CORS behavior, metrics paths, or S3 options
- whether a storage backend, lock implementation, plugin path, or hook transport is officially supported
- whether a browser client option is available in the installed `tus-js-client` version, especially retry, resume, storage, parallel upload, and hook callback behavior
- proxy behavior for buffering, streaming request bodies, timeouts, sticky routing, or forwarded headers
- security guidance around upload URLs, frontend URL storage, termination, downloads, CORS, auth headers, or multi-tenant ownership checks

## Community Troubleshooting Boundary

Use community material to identify symptoms such as proxy buffering, missing `HEAD`, stale offsets, or S3 multipart cleanup gaps. Confirm the final recommendation through official docs, repo-local config, and a focused upload/resume test.

## Small Anti-Pattern

Anti-pattern: relying on `pre-create` as the only authorization gate.

Better path: make the application issue an upload session, protect `POST`, `PATCH`, `HEAD`, and `DELETE` at the gateway or reverse proxy, and use hooks for validation and lifecycle automation instead of as the only trust boundary.
