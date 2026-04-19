# Enterprise Go Shortlist

Use this file only when the stdlib and `golang-popular-libraries` references do not already cover the package or tool
decision.

Treat every entry here as "consider", not "always use". Confirm maintenance, license, and fit before adding anything.

## RPC and protobuf-heavy services

- `connectrpc.com/connect`
  - Use when one schema should serve Connect, gRPC, and gRPC-Web without inventing a custom bridge on top of
    `net/http`.
- `github.com/grpc-ecosystem/go-grpc-middleware/v2`
  - Use when `grpc-go` interceptor composition for auth, logging, retries, recovery, or metrics is becoming non-trivial.
- `buf`
  - Use when raw `protoc` command lines are getting brittle and you need repeatable lint, breaking-change detection, and
    code generation.
- `buf.build/go/protovalidate`
  - Use for semantic protobuf validation in new schema-driven services instead of reviving older validation stacks by
    default.

## Auth and resilience

- `github.com/coreos/go-oidc/v3/oidc`
  - Conservative default for OIDC ID token verification on top of `golang.org/x/oauth2`.
- `github.com/sony/gobreaker/v2`
  - Use when retries and timeouts alone are not enough and you need a real circuit breaker.
- `github.com/robfig/cron/v3`
  - Use for in-process cron only when an external scheduler or queue is not the better fit. Pair it with explicit job
    ownership, overlap policy, and shutdown handling.

## Kubernetes and platform integration

- `k8s.io/client-go`
  - Use when the service must watch or mutate Kubernetes resources directly.
- `sigs.k8s.io/controller-runtime`
  - Use for real controllers and operators. Prefer it over ad hoc reconcile loops once the service is part of the
    cluster control plane.
- `ko`
  - Use for single-binary Go services when fast container builds and Kubernetes-oriented delivery matter more than a
    hand-written Dockerfile.

## Delivery and release tools

- `goreleaser`
  - Use when manual multi-platform binary releases, archives, checksums, or package publishing are getting noisy.
- `buf` and `ko` are tools, not runtime dependencies.
  - Pin them in tool directives or install steps, not in production code paths.

## Selection rules

- Prefer the standard library first.
- Prefer vendor skill-owned packages when they already cover the decision.
- Ask before adding dependencies.
- Route deep Docker, Kubernetes, OpenShift, CI, or contract policy to `20-sohrab-companions.md` instead of encoding it
  directly into app packages.
