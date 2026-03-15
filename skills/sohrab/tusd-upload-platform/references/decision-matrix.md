# Decision Matrix

## Default Architecture Choices

| Situation | Default choice | Why | Main caveat |
|---|---|---|---|
| Users upload files that should end up in your own MinIO / S3-compatible storage | Dedicated `tusd-s3` deployment | tusd already supports S3-compatible storage directly and streams to object storage while the user uploads | S3 mode still uses temporary local disk during multipart handling |
| Users upload videos that must end up in another provider's tusd service with your service-owned credentials | Dedicated `tusd-staging` deployment with local disk + async relay worker | Keeps provider credentials server-side, avoids exposing provider tokens, and gives you full authorization hooks | Requires staging storage, relay jobs, and cleanup lifecycle |
| Product needs both of the above | Two separate tusd deployments | Lower operational ambiguity and clearer ownership of config, storage, cleanup, and SLOs | Two services instead of one |
| Product explicitly requires one deployable unit and accepts custom Go code | One custom Go service with multiple tusd handlers | Lets you route to multiple backends programmatically | Higher build, test, and ownership complexity |

## Pick the Platform Shape

### Choose two separate tusd deployments when

- The platform needs both direct S3/MinIO storage and local-staging relay.
- Different upload classes need different lifecycle policies.
- Different security boundaries are required for direct storage vs upstream relay.
- You want the lower-risk, lower-surprise operating model.

### Choose one custom Go service with multiple handlers only when

- The user explicitly wants one binary or one deployable unit.
- The team can maintain custom Go code around tusd, not just CLI flags.
- The team is willing to own routing, tests, and possibly distributed locking.

## Hook Transport Selection

| Hook transport | Default use | Strengths | Avoid when |
|---|---|---|---|
| HTTP hooks | Default production choice | Centralized state, language-agnostic, easy to scale, easy to secure behind internal auth/mTLS | You need ultra-low latency and already have a mature gRPC platform |
| gRPC hooks | Advanced production choice | Lower per-call overhead, strong contracts, good fit for existing gRPC estates | The org does not already operate gRPC well |
| File hooks | Local dev or simple single-instance setups | Simple and easy to understand | You need shared state, clustering, or low hook overhead |
| Plugin hooks | Specialized Go-heavy single-instance setups | Lower local overhead than file hooks | You need one central hook process across many tusd instances |

## Authorization Pattern Selection

| Requirement | Recommended pattern |
|---|---|
| Check whether a user may start an upload | `pre-create` hook + app-side upload record creation |
| Ensure only the allowed actor may resume or terminate an upload | Authenticated gateway check on every request + upload record lookup by upload ID |
| Abort uploads if business state changes mid-transfer | Enable `post-receive` and stop uploads when the resource or permission is gone |
| Return extra metadata or an app URL when upload finishes | Use `pre-finish` for small, fast response decoration, but persist the same data elsewhere too |
| Trigger relay, transcoding, scanning, or notifications | Use `post-finish` only to enqueue durable work |

## Scaling Choice

| Deployment shape | Recommended control |
|---|---|
| Single tusd instance | Built-in local locking is fine |
| Multiple tusd instances behind a load balancer, using stock tusd | Sticky sessions at the load balancer, or do not scale that way |
| Multiple instances and strong correctness across shared storage | Custom Go integration with a distributed locker, or another architecture that guarantees exclusive access |

## Operational Default

When the user describes a security-sensitive, high-concurrency platform similar to a production upload gateway, recommend this baseline unless told otherwise:

1. `tusd-s3` for direct MinIO/S3 uploads.
2. `tusd-staging` for provider-bound video uploads.
3. One central hook service over HTTP hooks.
4. One authenticated gateway in front of both tusd deployments.
5. One durable job system for relay and other post-upload side effects.
6. One shared upload record schema tracking ownership, target, state, and audit fields.
