# Version pins and upgrade deltas

Every pin below carries the command that re-derives it. A version written in a file
goes stale silently; a re-derivation command beside it does not.

```
PIN vector = 0.57.0
PIN helm-chart = 0.58.0
```

`scripts/check-upstream-version.mjs` reads those two `PIN` lines from this file and
compares them to upstream, so this document and the checker cannot disagree.
Run it with `node scripts/check-upstream-version.mjs`: exit 0 current, 1 drift,
2 could not run.

## Re-deriving the pins

Vector release (verified 2026-07-30: `0.57.0`, released 2026-07-14):

```bash
curl -s 'https://api.github.com/repos/vectordotdev/vector/releases?per_page=100' \
  | jq -r '[.[] | select(.tag_name | test("^v[0-9]+\\.[0-9]+\\.[0-9]+$"))] | .[0] | "\(.tag_name) \(.published_at)"'
```

**Do not use `/releases/latest` for this repository.** It returns `vdev-v0.3.3`,
the tag of the `vdev` developer tool that lives in the same repository, not a
Vector release. A resolver that trusts it reports Vector 0.3.3, and every version
comparison downstream is then wrong in the direction that looks safe.
`scripts/check-upstream-version.mjs --self-test` asserts this trap is rejected,
using the committed fixture `assets/fixtures/upstream-releases.sample.json`.

Helm chart (verified 2026-07-30: chart `0.58.0`, appVersion `0.57.0-distroless-libc`):

```bash
curl -s https://raw.githubusercontent.com/vectordotdev/helm-charts/develop/charts/vector/Chart.yaml
```

The chart version and the Vector version are separate numbers and have drifted
apart before. Compare `appVersion` against the Vector release pin on every chart
bump: when they differ, a Helm-deployed pipeline runs a different Vector build
from a package-installed one, and a version-sensitive behaviour change lands in
one environment and not the other.

## Release line since the version this skill previously pinned

`0.53.0` 2026-01-27 · `0.54.0` 2026-03-10 · `0.55.0` 2026-04-22 ·
`0.56.0` 2026-06-03 · `0.57.0` 2026-07-14.

## The three 0.57.0 changes that change what you must write

### 1. Environment-variable interpolation is disabled by default

Upstream: *"Environment variable interpolation in configuration files is now
disabled by default."* Restore it with `--dangerously-allow-env-var-interpolation`
or `VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true`. The old
`--disable-env-var-interpolation` flag and `VECTOR_DISABLE_ENV_VAR_INTERPOLATION`
were removed.

**This fails open, which is why it gets its own rule.** A config containing
`password: ${CLICKHOUSE_PASSWORD}` still passes `vector validate` with exit 0 on
0.57.0, because any string is a valid password. The sink then authenticates with
the 22-character literal text `${CLICKHOUSE_PASSWORD}`. Nothing in the validation
step reports it. Observed directly on 0.57.0:

```
$ vector validate --no-environment p.yaml    # password: ${CLICKHOUSE_PASSWORD}
√ Loaded ["p.yaml"]
                 Validated
EXIT=0
```

Where the interpolated value must satisfy a format, the same change fails loudly
instead: `endpoint: ${CH_ENDPOINT}` gives `x invalid uri character` and exit 78.
So the breakage is silent exactly where the value is a secret.

**Rule:** do not use `${VAR}` interpolation for credentials in a Vector config.
Use a `secret:` backend and `SECRET[backend.key]` references. The full rule, and
the deprecation of placeholders in structural positions, is in
`85-security-and-secrets.md`.

### 2. Sink routing templates are confined

Upstream: *"Sinks that accept `{{ field }}` references in routing templates now
enforce a confinement boundary: the rendered value must stay within the literal
prefix declared in the template."* Templates with no literal prefix are rejected.
The per-sink opt-out is `dangerously_allow_unconfined_template_resolution: true`,
and setting it raises `vector_security_confinement_disabled` to `1`.
`component_errors_total{error_type="confinement_failed"}` counts runtime failures.

Observed on 0.57.0 for a ClickHouse sink:

```
table: "{{ tenant }}"        -> exit 78: template references event fields (["tenant"])
                                but has no literal string prefix to derive a
                                confinement base from.
table: "logs_{{ tenant }}"   -> exit 0
```

**Rule:** every templated `table`, `database`, object key, file path, or HTTP
header value carries a literal prefix. This is a security control, not a style
preference — it is the fix for injection through a routing field.

**Trap, stated by upstream as a known issue:** *"`vector validate
--no-environment` doesn't catch unconfined routing templates."* See
`50-validation-and-testing.md` for the flag set that does catch it.

### 3. ClickHouse SQL injection fixed

Upstream: *"Fixed SQL injection via identifier names in the `clickhouse` sink.
The `database` and `table` config values are now passed as ClickHouse query
parameters with the `Identifier` type (`{database:Identifier}.{table:Identifier}`),
letting the server handle quoting rather than relying on client-side string
escaping."*

**Rule:** `0.57.0` is the minimum version for any pipeline whose ClickHouse
`database` or `table` is templated from event data. On an earlier version, a
templated identifier is an injection surface, and confinement does not exist
there to bound it either.

## 0.55.0 — the observability API moved from GraphQL to gRPC

Upstream: the API *"has moved from GraphQL to gRPC. This includes `vector top`,
`vector tap`, and anything that talked to `/graphql` or the `/playground`. The
HTTP `GET /health` endpoint is unchanged."*

**Rule:** if anything other than `vector top` and `vector tap` queries the Vector
API — a dashboard, a scrape job, a custom operator — it must be re-pointed at the
gRPC API before upgrading past 0.55.0. Kubernetes HTTP probes on `GET /health`
are unaffected and need no change.

Also in 0.55.0: the top-level `headers` option was removed from the `http` and
`opentelemetry` sinks, and `azure_logs_ingestion` with Client Secret credentials
now requires `azure_credential_kind` to be set explicitly.

## 0.54.0 and 0.56.0

`0.54.0`: the `datadog_logs` sink defaults to `zstd` compression; set
`compression` explicitly to keep the previous behaviour. `0.56.0`: the
`greptimedb_metrics` and `greptimedb_logs` sinks require GreptimeDB v1.x.
Neither affects a ClickHouse pipeline.

## 0.53.0 — the internal buffer metric renames

This is the migration the previous version of this skill stated wrongly. It named
two renames, gave the **old** name incorrectly in both, gave the bucket count
change as 10 to 26, and scoped it to one metric. An agent grepping dashboards for
the names it listed finds nothing, reports the migration clean, and leaves every
real deprecated name in place. The corrected list, verified against the 0.53.0
release notes:

| Current name | Deprecates |
| --- | --- |
| `buffer_max_size_bytes` | `buffer_max_byte_size` |
| `buffer_max_size_events` | `buffer_max_event_size` |
| `buffer_size_bytes` | `buffer_byte_size` |
| `buffer_size_events` | `buffer_events` |

All four are renames of the same family; a migration that handles only the two
byte-sized ones leaves the two event-sized ones broken.

**The old gauges still exist.** Upstream: *"while keeping the old related gauges
available for a transition period."* That is what makes a safe migration
possible — dashboards can carry both names across one release, and the cutover
does not have to be atomic. It also means a grep that finds the old name proves
nothing about whether the new one is wired.

**Histogram buckets went 20 to 26, across all internal histograms**, not for one
metric. The smallest bucket is now approximately `0.000244` (2^-12). Upstream
warns that *"if you were manually indexing buckets using VRL, you have to change
your indexes"*. Alert thresholds derived from bucket indexes need re-deriving;
thresholds derived from quantiles do not.

Also added in 0.53.0, and useful for the saturation signal in
`60-internal-monitoring.md`: `source_buffer_utilization_mean` and
`transform_buffer_utilization_mean`, exponentially weighted moving averages of
buffer utilisation alongside the instantaneous gauges.

Re-derive this whole section:

```bash
curl -s https://raw.githubusercontent.com/vectordotdev/vector/master/website/cue/reference/releases/0.53.0.cue
```

## VRL metric helpers

`get_vector_metric`, `find_vector_metrics` and `aggregate_vector_metrics` were
added in 0.53.0 and still exist on 0.57.0. Verified 2026-07-30.
