# Version and Branch

## The branch table

Read on 2026-07-29 from `https://docs.haproxy.org/` (branch labels) and `https://www.haproxy.org/`
(latest patch and end-of-life dates). Re-derive both with the commands in `SOURCES.md`.

| Branch | Label | Latest patch, read 2026-07-29 | End of life |
|---|---|---|---|
| 3.5 | DEV | not for production | — |
| **3.4** | **LTS** | **3.4.2, released 2026-07-03** (branch opened 2026-06-03) | 2031-Q2 |
| 3.3 | no label (stable) | 3.3.12 | **2027-Q1** |
| 3.2 | LTS | 3.2.21 | 2030-Q2 |
| 3.0 | LTS | 3.0.25 | 2029-Q2 |
| 2.8 | LTS, critical fixes only | 2.8.26 | 2028-Q2 |
| 2.6 | LTS, critical fixes only | 2.6.31 | 2027-Q2 |
| 3.1 and below, except the rows above | EOL | — | passed |

## Which branch to target

- **A new deployment targets 3.4.** It is the current LTS and it is supported to 2031-Q2.
- **An estate on 3.2 may stay on 3.2.** It is a supported LTS until 2030-Q2. Staying is a
  decision about change velocity, not about correctness, and it is legitimate. Move to 3.4 when
  the estate needs a feature 3.2 does not have, or when 2030 is close enough to plan for.
- **An estate on 3.3 moves to 3.4.** 3.3 is not an LTS and its security support ends 2027-Q1.
  There is no version of "stay here" that survives past that date.
- **An estate on 3.1 or below is already unsupported.** Move to 3.4.

The `-3.3` suffix on four example files means "requires 3.3 or later". Those four features -
backend HTTP/3, `shm-stats-file`, `sni-auto`, `ktls` - shipped in 3.3 under those directive names
and still work under those names on 3.4, confirmed by running `haproxy -c -f` on a 3.4.0 build on
2026-07-29. One thing did change: **`shm-stats-file` is no longer experimental on 3.4**, so a
config that still carries `expose-experimental-directives` for it alone now warns

```
Option 'expose-experimental-directives' is set in the global section but is no longer used.
```

while **`ktls` is still experimental on 3.4** and removing the gate there is a fatal error. Neither
fact is discoverable from the release notes; both come from the binary. `15-persistent-stats-3.3.cfg`
puts the gate behind `.if !version_atleast(3.4)` for this reason and `17-ktls-3.3.cfg` does not.

## Confirming a directive exists before using it

A directive that exists in one branch may not exist in the branch that will run the config, and
the config file gives no hint either way. Two checks, in order:

1. `haproxy -vv` on the binary that will run it. It prints a `Feature list` of `+NAME`/`-NAME`
   tokens - `+QUIC`, `+KTLS`, `+PROMEX`, `+ZLIB`, `-LUA` and so on - and the TLS library it was
   built against. That list, not a document, is what says whether this build has QUIC, kTLS, Lua,
   tracing or the Prometheus exporter. `haproxy -v` alone also prints the branch's own support
   status, for example "long-term supported branch - will stop receiving fixes around Q2 2031",
   which is the fastest single check that a binary is on a branch worth deploying.
2. `haproxy -c -f <cfg>` on that same binary. This answers "does this directive exist in this
   branch, spelled this way, in this section". An unknown keyword is a fatal error naming the
   line and the section, so the check is conclusive.

**When the directive is absent**, the replacement is one of three things and never "leave it out
and hope": use the documented predecessor named in the branch manual for the branch you run; put
the whole block behind `.if version_atleast(<branch>)` so a mixed estate loads what it can (see
`20-core-config-and-timeouts.md`); or upgrade the binary. Choosing silently to omit the directive
is what turns a missing security control into a config that starts.

On 3.3 and later, `haproxy -vq`, `haproxy -vqs` and `haproxy -vqb` print the version, the status
and the branch as bare strings, which is what a script should parse instead of the `-v` banner.

## 3.2 to 3.3: deprecations and breaking changes

Confirmed 2026-07-29 against `https://www.haproxy.com/blog/announcing-haproxy-3-3`.

Breaking - these fail startup or change behaviour after an upgrade:

- The minimum Linux kernel rises to **4.17**.
- The `program` section is **removed** (deprecated in 3.1).
- Duplicate names across `frontend`, `backend`, `listen`, `defaults` and `log-forward` are now
  errors, as are duplicate `server` names within a backend. This makes naming every `defaults`
  section cheap: a collision is caught at startup rather than resolved silently.
- `http-send-name-header` may no longer overwrite `connection`, `content-length`, `host` or
  `transfer-encoding`.
- Multiple match types after `-m` in an ACL are no longer allowed.
- Email alerts now require the Lua implementation to be enabled. Lua work in HAProxy is owned by
  `/alaa-haproxy-lua` (`$alaa-haproxy-lua`).
- `no-quic` is renamed `tune.quic.listen`.
- **The default load-balancing algorithm becomes `random`** when `balance` is absent. Every
  backend in this skill's examples states `balance` explicitly for this reason.
- **`mode http` backends default to `option abortonclose`**, which changes what happens to an
  in-flight request when the client disconnects.

Deprecated - these warn now and will be removed:

- the `master-worker` global directive, replaced by the `-W` or `-Ws` command-line argument
- `tune.quic.frontend.*`, replaced by `tune.quic.fe.*`
- `dispatch` and `option transparent`

## 3.3 to 3.4

Confirmed 2026-07-29 against `https://www.haproxy.com/blog/announcing-haproxy-3-4`.

Breaking: the stats page no longer shows the HAProxy version; re-enable with `stats show-version`
if a tool parses it.

Deprecated: `compression-direction`, and OpenTracing, which is removed in 3.5. The replacement for
OpenTracing is the native OpenTelemetry integration added in 3.4; whether tracing is required at
all is decided by `/alaa-observability-soc` (`$alaa-observability-soc`).

Added, in case a task needs one of them: backends that can be added and removed at runtime without
a reload; QMux, experimental QUIC over TCP for networks that block UDP; JWE decryption and AES-CBC
at the proxy; ACME DNS-PERSIST-01, External Account Binding and IP addresses in SANs; extended
HTTP/1 glitch detection; `http-request set-timeout` extended to connect, queue and tarpit;
reusable health-check sections; `tune.bufsize.large` and `tune.bufsize.small`; `cpu-affinity` and
`threads-per-core`.

## Upgrading

The upgrade is a config change and a binary change, and the config change comes first:

1. Run `haproxy -c -f <cfg>` **on the new binary** before the new binary runs anything. Every
   breaking change above surfaces here.
2. Fix what it reports. A warning about a deprecated directive is a fix due before the branch
   after next, not a fix due today; an alert is due now.
3. `scripts/check_examples.py --haproxy <path-to-new-binary>` if the estate copied from these
   examples, so the same check runs over every config at once.
4. Roll the binary. Rollback is the previous image tag; the config must remain loadable by both
   binaries for the duration of the rollout, which means no directive that exists in only one of
   them unless it is behind `.if version_atleast(...)`.

Do not share one config fragment across two branches when it uses a deprecated or experimental
directive. Keep one branch-aware config per estate.
