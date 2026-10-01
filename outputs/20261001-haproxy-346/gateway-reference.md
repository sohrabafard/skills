# Gateway integration reference

Inspected read-only on 2026-10-01 at HEAD `94cdfa5cf72ea0a77a7cdc490d34914ecc057008`.
The existing dirty tree is recorded in `gateway-intake.json`; it belongs to the user.

Verified source pointers:

- `docker/Dockerfile`, `.gitlab-ci.yml`, `docker-compose.yml` and `Makefile` use
  `haproxy:3.3.6-alpine3.23@sha256:4f97a2cb7f02fd08402259e74a65ef12fcfa3dff1ef78fddecb5228a17b7f4ad`.
  The Dockerfile identifies this as an OCI index resolved through the internal registry.
  This run inspected that declaration; it did not re-resolve the registry digest.
- The custom Dockerfile copies `haproxy/errors/` and `haproxy/lua/` into the image.
- `haproxy/lua/backend-readiness.lua` uses `os.getenv` and `os.date`;
  `haproxy/lua/authz-sidecar.lua` uses `os.getenv` and `os.time`.
  A Lua-library allowlist that omits `os` needs a redesign and dependency/failure tests.
- `gateway-error-bytes.json` compares raw Git HEAD bytes with checkout bytes for all ten
  custom responses. Every stored body matches Content-Length; every checkout body is one
  byte longer. For `400.http`, the stored/declared body is 101 bytes and checkout is 102.
  The staged `.gitattributes` does not itself establish that current files were renormalized.

Later gateway upgrade prerequisites:

1. Resolve reviewed tag and platform/index digests together across all image owners.
2. Build the custom image with byte-preserved responses and the existing Lua modules.
3. Capture `haproxy -vv`; derive Lua library restrictions from dependencies, not an example.
4. Render both Kubernetes and shared Docker profiles without changing profile-specific ports.
5. Parse with the actual custom image, then run the gateway's documented compatibility and
   public-HTTP behavior gates, including Lua failure, trust-header, health and observability paths.
6. Verify reload/drain/rollback and deployment separately in the target environment.

This run did not render, build, upgrade or deploy the gateway. The byte inspection reproduces
the framing hazard; it does not claim a new full-gateway parser result. Skill-package tests
cannot establish gateway readiness.

Final read-only observation: HEAD remains the intake commit. The dirty-path set
has grown to include chart helpers/deployment/values, the hardening ADR and
ingress/loadbalancer manifests, indicating concurrent work outside this task.
This task performed no gateway writes; an identical gateway tree is not claimed.
The four image declarations and listed Lua `os` dependencies were rechecked and
still match the intake observations. The byte comparison remains evidence of the
intake checkout, not a validation receipt for the concurrent gateway candidate.
