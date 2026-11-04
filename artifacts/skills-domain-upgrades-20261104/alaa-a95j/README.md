# Vector 0.61.0 acceptance evidence

Issue alaa-a95j. Source baseline 4f60ce6f4d43c976c9d3b69d0279643734e6d967.
The candidate source snapshot is identified by `skill.sha256`, relative to the
repository root. Release and migration sources are linked in the skill's
`80-version-and-upgrade-deltas.md` and `81-release-coverage.md`. Read the tagged
release interval as product documentation evidence.

## Artifact and resources

The cached mirror image inspected by exact ID reported a matching RepoDigest
suffix and entrypoint `/usr/local/bin/vector`. Image ID
`sha256:3bb7ed5152910ed51729e256937b1d8a4bf67ff624e9d565e8e5877bffd015c7`.
The executable reported
`vector 0.61.0 (x86_64-unknown-linux-musl 17e017e 2026-10-29 16:03:40.929269968)`.
The Helm tag points to a separately released distroless build.

Run from the skill root unless stated. The included adapter was placed on PATH
as `vector`; set `VECTOR_IMAGE` to the ID, `VECTOR_SKILL` to the absolute skill
root, `VECTOR_STAGE` and `TMPDIR` to the same isolated scratch directory, and
`VECTOR_RUN_LOG` to a writable log path outside the mount. Each Vector invocation
used a disposable container, 4 CPU and 1 GiB caps, a 120 s timeout, `--pull never`,
`--network none`, a read-only skill mount and a writable scratch mount. No ports
or provider services. Host 32 logical CPUs, at least 4 reserved, about 10.7 GiB
available before the runtime slot. The parent serialized runtime work.
Docker reported no remaining containers labeled `alaa.task=alaa-a95j` after
each batch. Logs substitute `<repo>` and `<scratch>` for local paths.

## Selected and executed checks

| Command | Expected and observed selection | Result |
| --- | --- | --- |
| `timeout 120s node scripts/check-upstream-version.mjs` | Two independently selected stable pins, Vector and chart, both 0.61.0 | Exit 0 |
| `timeout 120s node scripts/check-vector-configs.mjs` | Two strict validations, five named transform unit cases, one common VRL invocation. All selected and executed. | Exit 0 initially and after fixing a latent CRLF fixture-path check, with the final file snapshot |
| Direct adapter controls | Seven selected and executed. Strict E651 rejection, a deliberately wrong output assertion, missing secret in strict mode, the same config under weaker validation, explicit plaintext relay config, removed boolean compression, and malformed endpoint scheme | Two expected exits 0, five expected exits 78, each matched its diagnostic |
| `python3 -B scripts/check_fleet_references.py --skill vector-rust-observability-pipelines` from repo root | One skill, 17 Markdown files, 59 citations | Exit 0 |

`vector-processes.log` retains the adapter's concrete CLI arguments and binary
output including case names and exits. `controls.log` includes the explicit
expectations. Negative inputs used scratch copies only: changed the normalize
level expression to `string!(.level) ?? "info"`, changed the first asserted level
from `warn` to `impossible`, pointed the ClickHouse secret file at an absent
path, and changed a strict-clean Vector sink config from `compression: gzip`
to boolean `true` or from `http://127.0.0.1:6000` to an `ftp://` URI. The
relay fixture used `demo_logs`, one `vector` sink, and no connections.

## Boundaries

The shipped ClickHouse example uses a file backend. The checker binds that
example to a synthetic file while preserving strict validation of secret
resolution, ClickHouse component build, and topology. User-supplied configs
keep their backend. The backend may execute or contact a provider on 0.59+.
The failing missing-file control confirms the fixture serves a required
dependency. The weak validation control confirms why it cannot establish the
same contract. CRLF hardening was a static finding in the original passing
candidate. Final replay validates the changed checker on the current checkout.

No live relay handshake, API liveness, database insert, delivery, retry,
backpressure, drain, telemetry emission, Helm render, or distroless execution
was exercised. These candidates require the actual target and are separate from
the shipped fixture's contract. The source upgrade does not establish installed
skill activation or a consumer rollout. Independent review and root gates are
owned by the parent.
