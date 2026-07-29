# Sources and Freshness

A version written into a file goes stale silently. Every pinned value in this skill is listed
below with **the one command or URL that re-derives it**, so an agent can check rather than trust.

## When to re-check

Re-check before answering any question about branch status, a release date, a directive's
availability, TLS or QUIC behaviour, a container image tag, or an upgrade path — and whenever the
user asks for current or latest behaviour.

## Pinned values and how to re-derive each one

Read date for every row: **2026-07-29**.

| Pinned value | Where it is written | Re-derive with |
|---|---|---|
| 3.4 is the current LTS; 3.3 carries no label; 3.2 and 3.0 are LTS; 3.1 and below are EOL | `10-version-and-branch.md` branch table | open `https://docs.haproxy.org/` and read the labels beside each branch in the index |
| 3.4.2 released 2026-07-03; 3.3.12; 3.2.21; 3.0.25; 2.8.26; 2.6.31 | `10-version-and-branch.md` branch table | `https://www.haproxy.org/` front-page table, or list `https://www.haproxy.org/download/<branch>/src/` and take the highest tarball |
| 3.3 end of life 2027-Q1; 3.4 to 2031-Q2; 3.2 to 2030-Q2 | `10-version-and-branch.md` branch table | the end-of-life column on `https://www.haproxy.org/` |
| the 3.2 to 3.3 deprecation and breaking-change list | `10-version-and-branch.md` | `https://www.haproxy.com/blog/announcing-haproxy-3-3` |
| the 3.3 to 3.4 deprecation and breaking-change list | `10-version-and-branch.md` | `https://www.haproxy.com/blog/announcing-haproxy-3-4` |
| which TLS stacks give full QUIC; what `limited-quic` costs | `30-quic-http3.md` | `https://www.haproxy.com/blog/state-of-ssl-stacks`, then `haproxy -vv` on the actual binary |
| the compression filter is `comp-res`/`comp-req` from 3.4 | `50-caching-routing-and-rewrites.md` | `https://www.haproxy.com/documentation/haproxy-configuration-tutorials/performance/compression/` |
| cache section keywords and their limits (4095 MB total, object at most half) | `50-caching-routing-and-rewrites.md` | `https://www.haproxy.com/blog/accelerate-your-apis-by-using-the-haproxy-cache`, then section 6 of `https://docs.haproxy.org/3.4/configuration.html` |
| the Prometheus exporter is built in; `extra-counters` is a scrape parameter added in 3.0 | `60-observability-and-runtime.md` | `https://www.haproxy.com/documentation/haproxy-configuration-tutorials/alerts-and-monitoring/prometheus/` |
| `show peers` output marks a peer `(remote,active)` or `(local,inactive)` | `40-rate-limiting-and-peers.md` | `https://www.haproxy.com/documentation/haproxy-runtime-api/reference/show-peers/`, then run it against a live socket |
| official image tags: `3.4.1`, `3.4`, `latest`, `lts` — and `lts` now resolves to 3.4, not 3.2 | `examples/kubernetes/haproxy-deployment.yaml`, both Helm values files | `https://hub.docker.com/_/haproxy/` supported-tags list, or `docker run --rm haproxy:lts haproxy -v` |
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

## What was verified in this session

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
