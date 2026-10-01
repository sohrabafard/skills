# Bounded coverage and gap matrix

Audit 2026-10-01, compatibility target 3.4.6. Paths are relative to this reference
directory; examples are relative to the skill root. C/M denote the official 3.4
configuration/management manuals and R the 3.4 release announcement; exact source
URLs, release-source identity and proof limits are in `SOURCES.md`.
This matrix records scope and gaps; the topic map owns routing instructions.

| Practical topic | Owner and existing material | Verified gap -> correction | Source | Validation / remaining proof |
|---|---|---|---|---|
| Structure and defaults scope | `20-core-config-and-timeouts/10-defaults-association.md`, defaults checker | Existing positional-association checks retained; add shared healthcheck example | C sections 2, 4, 12.9 | defaults checker and real parser; concatenation still needs rendered-config check |
| ACLs, fetches, converters, maps and rewrites | `20-core-config-and-timeouts/40-maps-and-preprocessor.md`, `50-caching-routing-and-rewrites.md` | Sample phase/type/failure guidance absent -> add phase and normalization decisions | C sections 2, 7 | parser plus missing/duplicate header, map miss, Unicode/encoding and response-phase tests |
| HTTP headers and trust | `25-tls-and-mtls.md`, examples 11/18; `/alaa-trust-gateway-auth` and `/alaa-services-contract` | No central directive decision -> route trust input/duplicate/header replacement through native samples guidance | C HTTP actions and sample fetches | spoofed headers, direct listener access, trusted hop test; no contract names invented |
| H1/H2/H3 and tunnels | timeout guide, `30-quic-http3.md` | H1 glitches, H2 fairness, QUIC elasticity absent -> `15-capabilities-3.4.md`; correct stock OpenSSL blanket statement | C tuning, R; tagged source | parser/build gate plus negotiated protocol, overload and tunnel timeout runtime tests |
| TLS/certificates/mTLS | `25-tls-and-mtls.md`, examples 07/19 | ACME prerequisites and certificate compression absent -> capability reference | C TLS/ACME, R | chain/name/revocation/rotation, issuance and handshake-byte tests; issuer policy stays external |
| JWT/JWE/crypto | TLS reference; `/alaa-trust-gateway-auth` | Decrypt/error/allowlist/build guidance absent -> capability reference | C converters/JWT globals, R; 3.4.4 changelog | malformed/wrong-key/algorithm/tag/claim vectors; no security-free sample identity |
| Discovery/DNS | example 06, symptom guide | No standalone resolver decision -> native samples/discovery additions | C section 5.3 | DNS startup, empty/truncated answer, churn and recovery; parser cannot establish reachability |
| Balancing, affinity, queues/retries/timeouts/reuse | core guides, examples 08/09 | Per-request budgets and shared pools absent; misleading retry universals -> correct mechanics and route replay decision | C proxy/server options, R | example 21, budgets after switching, saturation/reuse/idempotency tests |
| Stick tables/peers/rate limiting | `40-rate-limiting-and-peers.md`, examples 04/12 | Exact partition multiplier and size identity overclaimed -> bound arithmetic and compatibility claims | C section 11, M show peers | partition/reconnect/saturation tests; hard quota routes to `/alaa-system-design` |
| Cache/compression | `50-caching-routing-and-rewrites.md`, example 20 | ZLIB-only prerequisite false; filter ordering missing -> alternative build tokens and explicit ordered filters; removed filter-sequence documented | C section 9, 3.4.5 changelog | checker regression, parser and decompress/cache byte test; policy stays `/alaa-frontend-devops` |
| Health checks | baseline examples, symptom guide | Reusable sections absent -> capability guide and example 21 | C section 12.9, R, 3.4.1 changelog | parser and positive/negative application readiness; readiness policy owner retained |
| Runtime API | `60-observability-and-runtime.md` | Backend lifecycle absent -> `65-dynamic-backends.md` | M commands, R, 3.4.3/4 changelog | create/publish/select/unpublish/drain/delete/reload tests; admin socket access controlled |
| Reload/drain/rollback | `70-delivery-and-drain.md` | Dynamic state loss and entrypoint signal claim insufficient -> route dynamic recovery; correct official entrypoint behavior | M, official Docker entrypoint | reload overlap, streams and reconstruction; chart/admission/rollout proof stays external |
| Logs/metrics/tracing/diagnostics | `60-observability-and-runtime.md` | Persistent stats contradiction, PROMEX default and OTEL availability overclaims -> correct; capability guide adds H2 logs/profiling/metric | C/M, R, exporter source | available filter/exposition inspection; OTEL unavailable in observed image, collector runtime gate unrun |
| CPU/buffers/memory/resource limits | capacity guide | Small/large buffers and topology absent -> capability guide | C global tuning, R | target cpuset/quota/FD/RSS/load and reload overlap; no universal tuning values |
| Container/build capabilities | branch/build/gate references, Helm/Kubernetes patterns | Package parser lacks offline container mode -> add real-binary Docker adapter | official image definitions + published tag metadata | `-vv`, parser, no pulls, isolated scratch; no image build/admission/deployment proof |
| Upgrade compatibility | `10-version-and-branch.md`, gate/source ledgers | Announcement treated as patch contract -> maintenance/backport ledger; stats/compression/OpenTracing/pool changes | C/M/R and release CHANGELOG | intended-build examples; historical captures explicitly retained |

Completeness here means a usable mechanical route or named policy owner. Runtime
claims require their scenario's runtime evidence; a matrix row or parser pass is
not proof of workload capacity, HAProxy component availability, gateway readiness
or deployment. Lua execution/API/library behavior belongs to `/alaa-haproxy-lua`.
