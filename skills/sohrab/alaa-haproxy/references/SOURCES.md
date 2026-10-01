# Sources and Freshness

A version written into a file goes stale silently. Every pinned value in this skill is listed
below with **the one command or URL that re-derives it**, so an agent can check rather than trust.

## When to re-check

Re-check before answering any question about branch status, a release date, a directive's
availability, TLS or QUIC behaviour, a container image tag, or an upgrade path — and whenever the
user asks for current or latest behaviour.

## Pinned values and how to re-derive each one

Historical read date: **2026-07-29**, except release/status and current image
metadata refreshed **2026-10-01**. Runtime captures in the historical section
remain dated evidence, distinct from the new requested-build checks below.

| Pinned value | Where it is written | Re-derive with |
|---|---|---|
| 3.4 is the current LTS; 3.3 carries no label; 3.2 and 3.0 are LTS; 2.8/2.6 receive critical fixes; 3.1 is EOL | `10-version-and-branch.md` branch table | open `https://docs.haproxy.org/` and read the labels beside each branch in the index |
| 3.4.6, 3.3.16, 3.2.25, 3.0.29 and 2.8.30 released 2026-09-28; 2.6.34 released 2026-09-24 | `10-version-and-branch.md` branch table | `https://www.haproxy.org/` front-page table, or list `https://www.haproxy.org/download/<branch>/src/` and take the highest tarball |
| 3.3 end of life 2027-Q1; 3.4 to 2031-Q2; 3.2 to 2030-Q2 | `10-version-and-branch.md` branch table | the end-of-life column on `https://www.haproxy.org/` |
| the 3.2 to 3.3 deprecation and breaking-change list | `10-version-and-branch.md` | `https://www.haproxy.com/blog/announcing-haproxy-3-3` |
| the 3.3 to 3.4 deprecation and breaking-change list | `10-version-and-branch.md` | `https://www.haproxy.com/blog/announcing-haproxy-3-4` |
| which TLS stacks give full QUIC; what `limited-quic` costs | `30-quic-http3.md` | `https://www.haproxy.com/blog/state-of-ssl-stacks`, then `haproxy -vv` on the actual binary |
| the compression filter is `comp-res`/`comp-req` from 3.4 | `50-caching-routing-and-rewrites.md` | `https://www.haproxy.com/documentation/haproxy-configuration-tutorials/performance/compression/` |
| cache section keywords and their limits (4095 MB total, object at most half) | `50-caching-routing-and-rewrites.md` | `https://www.haproxy.com/blog/accelerate-your-apis-by-using-the-haproxy-cache`, then section 6 of `https://docs.haproxy.org/3.4/configuration.html` |
| the Prometheus exporter requires a build with `+PROMEX`; `extra-counters` is a scrape parameter added in 3.0 | `60-observability-and-runtime.md` | `haproxy -vv`, then `https://www.haproxy.com/documentation/haproxy-configuration-tutorials/alerts-and-monitoring/prometheus/` |
| `show peers` output marks a peer `(remote,active)` or `(local,inactive)` | `40-rate-limiting-and-peers.md` | `https://www.haproxy.com/documentation/haproxy-runtime-api/reference/show-peers/`, then run it against a live socket |
| official image tags: `3.4.6`, `3.4.6-alpine3.24`, `3.4`, `latest`, `lts` — and `lts` now resolves to 3.4, not 3.2 | `examples/kubernetes/haproxy-deployment.yaml`, both Helm values files | official-images library metadata and the pinned docker-library definitions below; read `haproxy -vv` on the selected cached image without pulling |
| `idle-ping` is a `bind` and a `server` argument, never a proxy-level directive | `09-connection-reuse.cfg`, `20-core-config-and-timeouts.md` | `haproxy -c -f` a config with a bare `idle-ping` line in a `frontend`; it reports `unknown keyword 'idle-ping' in 'frontend' section` |
| `balance hash` requires a mandatory sample expression | `08-consistent-hash-affinity.cfg` | `haproxy -c -f` a config with a bare `balance hash`; it reports `balance hash requires a sample expression` |
| `localpeer` is a **global** keyword, and `-L` is its command-line equivalent | `40-rate-limiting-and-peers.md`, `12-peers-global-rate-limit.cfg` | `haproxy -c -f` a config with `localpeer` in `global`; then section 3.1 of the branch configuration manual |
| Kubernetes 1.32 reached end of life 2026-02-28; supported today are 1.36, 1.35, 1.34 | this file, as a warning against reintroducing a 1.32 pin | `https://kubernetes.io/releases/patch-releases/` |

The two commands that settle any directive-level question locally, and beat every source above
when they disagree with it:

```
haproxy -vv                 # what this build actually has
haproxy -c -f <cfg>         # what this branch actually accepts, in this section, spelled this way
```

On 3.3 and later, `haproxy -vq`, `-vqs` and `-vqb` print the version, status and branch as bare
strings for a script to parse.

## Official sources, in priority order

1. `https://docs.haproxy.org/` — branch index and labels
2. `https://docs.haproxy.org/3.4/configuration.html` and `.../management.html` — the manual for the
   branch you actually run; substitute the branch number
3. `https://www.haproxy.org/` and `https://www.haproxy.org/download/<branch>/src/` — releases
4. `https://www.haproxy.com/blog/announcing-haproxy-3-4` and `.../announcing-haproxy-3-3` — what
   changed and what broke
5. `https://hub.docker.com/_/haproxy/` — image tags
6. `https://github.com/haproxytech/helm-charts` and
   `https://www.haproxy.com/documentation/kubernetes-ingress/` — ecosystem

Useful background, subordinate to the above:
`https://www.haproxy.com/blog/state-of-ssl-stacks`,
`https://www.haproxy.com/blog/announcing-haproxy-3-2`,
`https://www.haproxy.com/documentation/haproxy-runtime-api/`.

Community posts and issue comments are for concrete troubleshooting only, after the official
manual, the release notes, `haproxy -vv` and `haproxy -c -f` have all been checked.

## Historical runtime evidence (2026-07-29)

On 2026-07-29 the following were confirmed by running **HAProxy 3.4.0**, built from source with
`TARGET=linux-glibc USE_OPENSSL=1 USE_ZLIB=1 USE_PCRE2=1 USE_PROMEX=1 USE_QUIC=1
USE_QUIC_OPENSSL_COMPAT=1` against OpenSSL 3.0.13:

- the binary's own banner reads "long-term supported branch - will stop receiving fixes around
  Q2 2031", which corroborates the 3.4 row of the branch table from the binary rather than the web;
- `shm-stats-file` is **no longer experimental** on 3.4: `expose-experimental-directives` set for
  it alone now warns that the option "is no longer used";
- `ktls` **is still experimental** on 3.4: removing the gate is a fatal error naming the directive;
- backend QUIC is rejected on a `USE_QUIC_OPENSSL_COMPAT` build with "The SSL stack does not
  provide a support for QUIC server", so `limited-quic` is frontend-only;
- without `limited-quic`, a frontend `quic4@` bind on that build is rejected and HAProxy names the
  option in the error;
- the `tune.quic.*` namespace differs again on 3.4 (`tune.quic.fe.stream.data-ratio`,
  `tune.quic.mem.tx-max`), and `haproxy -dKcfg -c -f /dev/null | grep tune.quic` enumerates the
  names the running binary actually has;
- `haproxy -c -f` returns 0 on success and prints nothing, and returns 1 on a fatal config error,
  so a checker must read the exit status rather than match a success string.

The following were confirmed against a second, older binary (2.8.16) as well, which is why they are
stated as branch-independent:
that `balance hash` without an expression is a fatal parse error; that `idle-ping` is rejected as a
proxy-level keyword; that named `defaults` with `from` works on `frontend`, `backend`, `listen` and
on another `defaults`; that a second unnamed `defaults` silently governs the proxies after it;
that `localpeer` belongs in `global`; that a `peers` section accepts `bind ... ssl` with a
`default-server ssl verify required ca-file` line; that `monitor-uri` with `monitor fail if` parses;
that `"${VAR-default}"` expands only when the whole argument is quoted and that an unset variable
with no default is a parse error; that `"${VAR[*]}"` splits on spaces; and that `.alert` inside a
`.if` block makes `haproxy -c -f` fail with the stated message.

## Requested target refresh: 2026-10-01

The live [release table](https://www.haproxy.org/) still lists **3.4.6**, released
2026-09-28, as the latest 3.4 patch; no newer 3.4 patch was observed. The [manual
index](https://docs.haproxy.org/) labels 3.4 LTS. Keep this task's compatibility
target 3.4.6 even when a later execution sees a newer maintenance release.

Inspected [configuration](https://docs.haproxy.org/3.4/configuration.html) and
[management](https://docs.haproxy.org/3.4/management.html) pages identified themselves
as 3.4.6-1. Their moving branch content is corroborated by the official
[3.4.6 release source](https://www.haproxy.org/download/3.4/src/haproxy-3.4.6.tar.gz),
`VERSION=3.4.6`, SHA256
`791e1815f8af6e8b850a227a9a0a190f3d3478c9e8d38a0f51c98b7f4bfe368b`.
This is the stable release corresponding to tag `v3.4.6`; GitHub development-mirror
tag URLs returned unavailable and were not treated as a negative feature result.
The task evidence's `source-manifest.json` records the inspected release files and
hashes. Initial archive inspection used read-only Python `urllib.request` +
`tarfile` in memory; subsequent inspection used the authorized evidence copy.
No upstream source or installed runtime was edited.

| Fact owner / capability | Precise release-source location / current official source |
|---|---|
| Defaults retention and runtime lifecycle | `doc/configuration.txt` `tune.defaults.purge`, `be-unpublished`; `doc/management.txt` lines 1752ff (`add backend`), 2147ff (`del backend`), 2544ff (`publish backend`), 2925ff (`unpublish backend`), `add server`, `wait`, `del server` |
| Per-request timeout extensions | configuration `http-request set-timeout`, `cur_*_timeout`, `be_*_timeout`; 3.4 announcement [dynamic timeouts](https://www.haproxy.com/blog/announcing-haproxy-3-4) |
| Buffers / topology / scheduler | configuration `tune.bufsize.large`, `tune.bufsize.small`, `option use-small-buffers`, `cpu-affinity` (2271ff), `cpu-policy`, `max-threads-per-group`, `tune.sched.low-latency` (5526ff) |
| H1/H2/QUIC overload | configuration `tune.h1.fe.glitches-threshold`, `tune.h1.be.glitches-threshold`, `tune.h2.fe.max-frames-at-once`, `tune.h2.fe.max-rst-at-once`, `tune.h2.fe.max-total-streams` (4586ff), `tune.h2.fe.max-concurrent-streams`, `tune.streams-elasticity` (5726ff) |
| Shared health checks | configuration `healthcheck` (33123ff) and server `healthcheck` (18963ff); `type`, `http-check`, `tcp-check`; changelog 3.4.1 attachment fixes |
| JWE / crypto | configuration `jwt_decrypt_cert` (22143ff), `jwt_decrypt_jwk` (22175ff), `jwt_decrypt_secret` (22226ff), `jwt.decrypt_alg_list`, `jwt.decrypt_enc_list`, `aes_cbc_enc/dec`; default RSA1_5 exclusion, AWS-LC algorithm exclusions and empty-string failure are explicit here |
| ACME / certificate compression | configuration ACME section, `eab-key-id`, `eab-mac-key`, `eab-mac-alg`, challenge values; `tune.ssl.certificate-compression` (5589ff: auto/off, OpenSSL >=3.2.0) |
| Compression and filter order | configuration section 9.2 (30774ff comp-req/res and legacy filter), 9.4 cache; `compression direction` (7255ff); changelog 3.4.5 removal of filter-sequence |
| Pool compatibility | configuration `tune.idle-pool.shared` (on/full/off, default on), deprecated `tune.takeover-other-tg-connections`, server `pool-max-conn`, `pool-low-conn`, `pool-purge-delay` |
| Logging / stats / profiling | configuration `tune.h2.log-errors`, `shm-stats-file`, `set-dumpable`; management `show profiling memory`, `show stat typed`; 3.4 announcement exporter local-updates metric |
| QMux / OpenTelemetry | configuration protocol/address forms and QMux; announcement's QMux experiment and separate experimental component; [component owner](https://github.com/haproxy/haproxy-opentelemetry) for build and filter configuration |

### Introduction, maintenance and backport ledger

The [3.4 changelog](https://www.haproxy.org/download/3.4/src/CHANGELOG) was read
from the 3.4.6 release archive, not inferred from an announcement:

- 3.4.0: dynamic backends, small/large buffers, extended request timeouts, reusable
  healthcheck sections, H1 glitches, crypto/ACME/TLS compression, new pool control,
  experimental QMux and separate experimental OpenTelemetry integration. Shared
  stats graduated during 3.4 development (3.4-dev14, changelog line 441), before
  3.4.0; `shm-stats-file` is not experimentally gated on 3.4.6.
- 3.4.1: healthcheck/default-server and external check fixes.
- 3.4.3: custom timeout initialization when switching backends; dynamic-backend
  deletion/read safety fixes and removal of outdated experimental documentation.
- 3.4.4: `be-unpublished` addition; JWE secret-length and AES-GCM tag checks;
  dynamic backend first-item deletion correction.
- 3.4.5: **filter-sequence reverted** (line 66); parser/HTX, H3, Lua cosocket,
  cache, ACL and other maintenance corrections. Do not ship announcement syntax
  that this requested patch no longer accepts.
- 3.4.6: QUIC RESET_STREAM crash fix (line 7), sink/server corrections and log
  `+utf8`. The [3.3.16 changelog](https://www.haproxy.org/download/3.3/src/CHANGELOG)
  has the same RESET_STREAM fix and `+utf8` addition in its 2026-09-28 entry.
  These are shared maintenance/backport changes, not exclusive 3.4.0 features.
- Already 3.3: backend H3, SNI auto, kTLS, experimental shared stats, default
  random balancing and `jwt_verify_cert`. Low-latency scheduling is older still
  (its introduction appears in the inherited changelog history, line 15633).

### Official image metadata and build receipt

[Published tag metadata](https://raw.githubusercontent.com/docker-library/official-images/master/library/haproxy)
inspected 2026-10-01 maps `3.4.6`/`3.4`/`latest`/`lts` to `3.4`, and
`3.4.6-alpine`/`3.4.6-alpine3.24` to `3.4/alpine`, at docker-library commit
`0b6d0e8c96b3e06b98929b40260f0fe8b7da6e8d`.
The immutable [Alpine Dockerfile](https://github.com/docker-library/haproxy/blob/0b6d0e8c96b3e06b98929b40260f0fe8b7da6e8d/3.4/alpine/Dockerfile)
uses Alpine 3.24, Lua 5.4 and `USE_LUA=1 USE_QUIC=1 USE_PROMEX=1`.
Its `STOPSIGNAL` is SIGUSR1; its entrypoint uses exec and does not remap SIGHUP.
The [Debian variant](https://github.com/docker-library/haproxy/blob/0b6d0e8c96b3e06b98929b40260f0fe8b7da6e8d/3.4/Dockerfile)
has a different OS/library dependency baseline. Tag metadata proves publication,
not a pull, local cache presence or architecture-specific build behavior.

Task readback of cached `haproxy:3.4.6-alpine` (`docker image inspect`,
`docker run --pull never --rm --network none --entrypoint haproxy <image> -vv`):
image ID `sha256:7af8255207ee9964ccb4eec8ce4b7a40b777769665e3ae83897fb01b24d8a43a`,
HAProxy `3.4.6-56332c5`, Alpine 3.24.2, Lua 5.4.8, OpenSSL 3.5.8,
`+QUIC +PROMEX +SLZ -ZLIB`, QMux present. Available filters include cache,
comp-req/res, legacy compression, spoe and trace; **OpenTelemetry absent**.
The `-OT` token denotes OpenTracing, so the filter inventory is the relevant
OpenTelemetry presence test. Lua 5.5 compile support does not change this
image's Lua 5.4 interpreter; `/alaa-haproxy-lua` owns matching language/API tests.
A local image ID is not the published OCI index digest.

### Rule-correction and compression rationale

Deliberate corrections preceded compression: shared stats experimental scope,
PROMEX build dependence, stock-OpenSSL QUIC version dependence, OpenTelemetry's
separate build, actual compression syntax/filter ordering, announcement-versus-
patch scope, entrypoint signals, sample failures and peer arithmetic were corrected
from the sources above. The new capability reference is an atomic decision catalog;
the matrix is an audit table, not a second procedural router. The final documentation
compression pass removes repeated narration and cross-runtime invocation pairs while preserving
triggers, owners, exceptions, prerequisites, source dates and validation obligations.
The routing-first body delegates capability details instead of loading them on
every invocation. Coverage and sources are atomic audit/lookup catalogs; the
capability reference is an atomic decision catalog, while the lifecycle reference
is procedural narrative. Added length covers independently requested capabilities,
build prerequisites and patch-versus-introduction distinctions that had no owner
in the baseline. It does not duplicate fleet policy. Compression retained the
distinct clauses for failure, experimental gating, unavailable components and
parser-versus-runtime proof; it made no new tuning decision.

Static/byte checks establish contract shape and raw body length. HAProxy parsing
establishes intended-build syntax and external path availability. The runtime
harness establishes only its isolated dynamic-backend scenarios. Neither proves
DNS/TLS/ACME issuance, overload capacity, QMux interoperability, OpenTelemetry span
export, live gateway compatibility, rollout, image build or deployment readiness.

### Historical focused gate receipt: first cycle (2026-10-01)

These attempts precede the explicitly authorized additional correction cycle
below. Their failures are preserved as observed history; the final independent
results are recorded at the end of this ledger.

Commands below ran from the repository root with host Python (`-B`,
`PYTHONDONTWRITEBYTECODE=1`). Gate commands are relative to this package:

- `python -B scripts/check_examples.py --structure-only`: exit 0; 21 configs,
  no findings. `python -B scripts/check_defaults_scope.py examples/haproxy`:
  exit 0; 21 configs, no findings. These preceded the final prose/header edits.
- `python -B scripts/check_http_error_bytes.py --self-test`: exit 0; six byte
  fixtures, no failures. All four checker `--help` invocations exited 0.
- Examples `--self-test` could not create its CRLF temporary fixture
  (`PermissionError`). One cause-specific TEMP/TMP relocation and retry had the
  same failure. Defaults-scope `--self-test` also failed creating a temporary
  CRLF fixture. Neither self-test is recorded as passed.

Docker checks used the cached image receipt above, installed host OpenSSL on PATH,
`--pull never`, `--network none`, one CPU, 256 MiB and read-only fixture mounts.
They ran in the approved host context; no image pull or published port occurred.

First parser command:
`python -B scripts/check_examples.py --docker-image haproxy:3.4.6-alpine --allow-skips`.
It attempted 22 targets (21 configs plus effective Kubernetes ConfigMap), skipped
none, and reported six findings: the DNS example and ConfigMap nameserver could
not connect under network isolation; the metrics example and ConfigMap health and
metrics frontends inherited an ignored HTTP log format without a log address;
example 21 placed `set-timeout connect` in a frontend without backend capability.

One cause-specific repair moved example 21 connect/queue actions into its backend,
used fixture-local DNS, and attempted `no option httplog` on health/metrics
frontends. Retry command was identical without `--allow-skips`: exit 1, 22 targets
attempted, 20 clean, two fatal targets. `no option httplog` is unsupported in the
metrics example and effective ConfigMap; these examples were **blocked at that attempt**.
The counter printed as parsed represents attempted targets, not successful parses.
At that attempt, moving `option httplog` to traffic frontends was a proposed,
unvalidated correction. The authorized additional cycle below applied it.

Both lifecycle attempts used
`python -B scripts/check_runtime_3_4.py --docker-image haproxy:3.4.6-alpine`.
First attempt exited 2 on an HTTP 503 from BusyBox wget. The one repair accepted
only wget return code 1 containing `503 Service Unavailable`, within an eight-second
readiness deadline; other operation errors still fail immediately. Retry exited 1
with `FAIL: routed response did not become fallback`. No stage label survived;
first-create unpublished selection is an inference from source and control flow,
not observed stage evidence. The probe lacks `default_backend be_fallback`:
management source lines 2925ff states unpublished backend selection is ignored,
then rules continue. A map default does not apply to an existing `/live` mapping.
At that attempt, adding an explicit fallback was proposed and unvalidated. Containers
were stopped by the harness cleanup; lifecycle success is **not established**.

This candidate was frozen after the one repair/retry. Independent diagnosis and
verification belong to the parent gate. Router/gate-register reconciliation and
final documentation compression were subsequently completed without changing the
failed configs or runtime probe or rerunning gates. Independent acceptance was
open at that point. No DNS, TLS,
ACME, overload, tracing, gateway startup, rollout or deployment proof is claimed.

### Authorized additional correction cycle (2026-10-01)

The user authorized one additional bounded fix/test cycle; the final verifier
owns its single real parser and lifecycle execution. The package lane made no
additional Docker execution. Logging is now selected only on traffic frontends;
the lifecycle fixture has an explicit fallback and stage labels. Pinned release
`src/cli.c` lines 2399-2411 was inspected from the existing authorized archive:
wait replies distinguish `Done.`, expiration, interruption and failure. The
probe asserts those replies with a transport deadline longer than its wait,
observes a real server stream, preserves its full body through maintenance,
then waits for removal. Its controlled Lua origin requires `+LUA`.

Parser environment forwarding is limited to explicitly constructed fixture values;
an unrelated synthetic inherited sentinel must be absent. All Docker invocations
allocate owned names before creation and verify bounded cleanup, including client
timeouts and failed creation. The exact patch matcher rejects `3.4.60` and trailing
junk. Decimal Content-Length comparison avoids integer digit-limit exceptions;
absurd-length and leading-zero fixtures preserve raw-byte behavior.

From repository root, `python -B skills/sohrab/alaa-haproxy/scripts/test_runner_contracts.py`
initially passed eleven synthetic tests; `python -B skills/sohrab/alaa-haproxy/scripts/check_http_error_bytes.py --self-test`
passed eight fixtures. The final verifier receipt in the task evidence archive is authoritative for the corrected candidate. These establish runner contracts and byte classification,
not Docker engine access, real parsing or dynamic lifecycle behavior. Prior scratch
self-test failures remain historical; final independent results follow below.

### Documentation classification and restructuring

Under `/alaa-repo-docs` `references/15-document-size-and-clustering.md`, this file
is **EXEMPT-ATOMIC**, not approved red narrative: it is the complete verification
record for one versioned package refresh decision. Its claim-to-source register,
source identity, dated build, attempt history and proof limitations together
identify what that decision established. Separating qualifiers/history from the
register can make an old observation look current. This classification applies
to this verification payload, not to all source files or integrated guides. The
gate register is separately atomic as one ordered acceptance procedure.

Eligible narrative references 10, 15, 40, 50, 60 and 70 were losslessly clustered
by reader question; their existing paths remain routers and each topic has one
child owner. This relocation is a separately justified structural change, not a
compression shortcut. A subsequent compression pass removes duplicate headings
and shortens routing narration without changing read triggers, obligations,
exceptions, authority, defaults, source dates or proof limits. Version selection
and peer partition guidance remain yellow because splitting their decision flows
would separate branch/default context or enforcement consequences from the choice.

Additional-cycle cheap checks from repository root: examples `--structure-only`
and defaults-scope against `examples/haproxy` each returned exit 0 for 21 configs.
The scoped Markdown link/line-budget command inspected 42 eligible documents:
35 green, seven yellow, no orange/red. Yellow files retain activation/routing,
a complete backend lifecycle, map/preprocessor decision flow, QUIC build context,
branch selection/upgrade context or peer enforcement consequences; splitting those
flows further would detach a prerequisite from its decision. SOURCES and the gate
register are separately classified atomic payloads above, not waived narrative.
No result predicts the final verifier's parser or active-stream lifecycle verdict.

### Pre-verifier cheap review closure (2026-10-01)

Pinned `src/hlua.c` lines 13461-13469 requires an explicit boolean conversion
mode before Lua loading or emits a warning and defaults to the legacy mode.
The controlled fixture now selects `normal` before `lua-load`. Its real `-c`
result is classified with the examples checker's warning classifier; nonzero
parsing and unresolved warnings block lifecycle assertions with the named stage.
A synthetic test covers clean parsing, warnings on stdout/stderr and fatal parsing.
`python -B skills/sohrab/alaa-haproxy/scripts/test_runner_contracts.py` passed
12 tests in one focused run; scoped diff check returned 0. No Docker gate ran.
The three cache/router descriptions were corrected to match their existing child
contents, then compressed without changing child obligations. The final verifier
receipt remains authoritative for real parsing and lifecycle behavior.

### Final independent result and precommit review (2026-10-02 readback)

The archived final verifier receipt at
`<repo>/outputs/20261001-haproxy-346/verification/final-report.md` records all
22 parser targets passing on the frozen candidate and twelve synthetic runner
tests passing. The lifecycle command exited 1 at `active stream prevents
deletion: lifecycle assertion`; the actual CLI reply was not retained. Stream
completion, drained deletion and reload reconstruction were not reached. This
is a failed candidate gate, not an established HAProxy regression or lifecycle pass.

The precommit review corrected retry/build commentary, example inputs and suite
exit-code wording, and retained the wait reply in the assertion failure message
without changing its condition. It ran no tests, parser, checker or runtime command.
The lifecycle cause remains unresolved; the edited runner has no new execution
proof. Earlier receipts apply to their recorded inputs, not this edit. No gateway,
rollout or deployment proof is claimed.
