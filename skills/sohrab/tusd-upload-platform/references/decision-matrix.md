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

## Reverse Proxy Selection

| Situation | Default choice | Why | Caveat |
|---|---|---|---|
| Existing platform already standardizes on Nginx or Nginx Ingress and the team uses `auth_request`, familiar config snippets, or ingress annotations | Nginx | Lowest adoption friction and easy reuse of existing ingress or auth conventions | Still requires buffering to stay off and timeouts to be reviewed explicitly |
| Existing platform uses HAProxy or wants LB-centric stickiness, canarying, connection policies, or richer load-balancer ownership | HAProxy | Strong fit for load-balancer-centric operations and stickiness strategies for multiple stock tusd instances | Requires careful timeout, ACL, and header forwarding review |
| One stock tusd instance behind one reverse proxy | Follow existing platform standard | Either Nginx or HAProxy is fine if forwarding and buffering rules are correct | Do not over-optimize proxy choice if there is no multi-node need |
| Multiple stock tusd instances sharing storage | Proxy with explicit stickiness support that the platform already operates well | Stickiness is usually simpler than jumping straight to custom distributed locking | Stickiness is an operational mitigation, not a full distributed lock design |

## Hook Transport Selection

| Hook transport | Default use | Strengths | Avoid when |
|---|---|---|---|
| HTTP hooks | Default production choice | Centralized state, language-agnostic, easy to scale, easy to secure behind internal auth or mTLS | You need ultra-low latency and already have a mature gRPC platform |
| gRPC hooks | Advanced production choice | Lower per-call overhead, strong contracts, good fit for existing gRPC estates | The org does not already operate gRPC well |
| File hooks | Local dev or simple single-instance setups | Simple and easy to understand | You need shared state, clustering, or low hook overhead |
| Plugin hooks | Specialized Go-heavy single-instance setups | Lower local overhead than file hooks | You need one central hook process across many tusd instances |

## Authorization Pattern Selection

| Requirement | Recommended pattern |
|---|---|
| Check whether a user may start an upload | `pre-create` hook + app-side upload record creation |
| Ensure only the allowed actor may resume or terminate an upload | Authenticated gateway check on every request + upload record lookup by upload ID |
| Abort uploads if business state changes mid-transfer | Enable `post-receive` and stop uploads when the resource or permission is no longer valid |
| Keep upstream provider credentials out of the browser | Stage locally first, then relay asynchronously from a worker |

## Browser Client Pattern Selection

| Situation | Default choice | Why | Caveat |
|---|---|---|---|
| Vue.js + Quasar + Vite app with SSR enabled | Client-only boot file plus browser-only upload composable | Prevents `window`, `File`, and local storage usage on the server | Do not import browser upload helpers into server-only modules |
| PWA mode enabled | Exclude tus endpoints from service-worker precache and runtime caching | Prevents the service worker from interfering with `PATCH`, `HEAD`, and `DELETE` upload traffic | Do not rely on generic offline caching patterns for resumable uploads |
| High-security environment | App-issued short-lived upload session plus strict gateway auth on every request | Keeps auth and ownership in the application trust boundary | Resuming across browser sessions may need tighter policy or storage hygiene |
| Standard browser app with resumability requirement | `tus-js-client` with resume lookup and bounded retries | Best fit for tusd, resumable uploads, and standard browser support | Tune retry, storage, and termination behavior deliberately instead of relying on defaults alone |

## Operational Defaults

Unless the user explicitly requests something else, recommend these defaults:

- one upload-session creation call from the app before the browser starts tus traffic,
- stable `X-Correlation-Id` per upload plus per-request IDs,
- `removeFingerprintOnSuccess=true` on the browser client,
- disable termination unless the product clearly exposes cancel/delete via tus,
- explicit service-worker exclusions for upload origins and paths,
- proxy-side protection for `/metrics` and any debug endpoints,
- sticky sessions before custom distributed locking when scaling stock tusd.
