# Access, grants, and where every value lives

## Environment keys on the consumer read lane

These are the only ClickHouse environment keys `alaa-go-chi` defines
(`configkit/keys.go:51-55`). There is no `CH_*` prefix; a variable named `CH_ADDR` is read by
nothing.

| Key | Meaning | Default |
| --- | --- | --- |
| `CLICKHOUSE_ADDR` | `host:port` of the **native-protocol** listener | none; blank means the lane is absent |
| `CLICKHOUSE_DATABASE` | database the read session opens | `default` |
| `CLICKHOUSE_USER` | read role | `default` |
| `CLICKHOUSE_PASSWORD` | that role's password | none |
| `CLICKHOUSE_DIAL_TIMEOUT` | connection-establishment bound | `5s` |

`chkit` reads no environment itself: `configkit` resolves the lane and `chkit.ConfigFrom` projects
it (`chkit/config.go:63-65`, "the connection components are what configkit already resolved from
the `CLICKHOUSE_*` lane, so chkit never re-reads the environment"). A consumer that reads
`os.Getenv("CLICKHOUSE_ADDR")` directly has forked the lane; take the value from the resolved
config.

A blank `CLICKHOUSE_ADDR` is not a soft failure: `NewClient` returns `ErrNoClickHouseAddr` and the
service fails at boot rather than at the first query (`chkit/doc.go:34-37`).

## The two ClickHouse endpoints are different endpoints

The ingest side and the read side connect over different protocols and different ports, and mixing
the values produces a connection error that reads like a network fault:

| Side | Variable | Protocol and default |
| --- | --- | --- |
| ingest (Vector sink) | `CLICKHOUSE_ENDPOINT` | HTTP, `http://shared-clickhouse:8123` (`<repo>/docs/DECISIONS.md` section 10) |
| consumer read lane (`chkit`) | `CLICKHOUSE_ADDR` | native protocol, `host:port` with no scheme |

The ingest side also reads `CLICKHOUSE_USER` and `CLICKHOUSE_PASSWORD`, so those two names appear
on both sides and may hold different credentials for different roles. Never assume one value serves
both.

## Where every other knob lives

| Knob | Lives in | Changed by |
| --- | --- | --- |
| per-call deadline (`CallTimeout`) | `chkit.Config` in the consumer's wiring | the consumer service |
| pool bounds (`MaxOpenConns`, `MaxIdleConns`, `ConnMaxLifetime`) | `chkit.Config` | the consumer service |
| `max_execution_time`, `max_result_rows` | `chkit.Config.Settings`, sent as session settings | the consumer service |
| `readonly=2` | `chkit` internals | **nobody**; `chkit/config.go:109-110` records it as a kit invariant that "cannot be weakened through Config" |
| readiness severity | the consumer's `ReadyCheck` call | the consumer service, using the test in `70-failure-and-degradation.md` |
| batch size, flush interval, buffer, retries | the ingest topology's sink block | the ingest-pipeline repository |
| `index_granularity`, engine, keys, codecs, TTL | the `SETTINGS` and clauses of the DDL | the ingest-pipeline repository |
| server-level and merge-tree settings | the ClickHouse server configuration | whoever operates the cluster; a consumer cannot set them |

Changing anything in the `chkit` rows above means changing `alaa-go-chi` itself, which is governed:
`/alaa-go-chi-development` (`$alaa-go-chi-development`) owns what may change in the kit, how it is
versioned, and how the change reaches consumers. A consumer that needs a `chkit` behaviour the kit
does not offer files that request there rather than forking the client locally.

A value that appears in none of these rows and that this skill does not state is a platform value:
take it from `/alaa-services-contract` (`$alaa-services-contract`)
`references/22-failure-load-and-deprecation-contract.md`, and request registration there when it is
missing rather than inventing one.

## Grants: the part this skill cannot verify

`chkit/config.go:70-71` states the intended posture: "The production role should be SELECT-only on
the rollup database; chkit additionally pins every session to readonly=2." Two independent controls,
and only one of them is enforced by code you can read.

- **Enforced and provable here.** `readonly=2` is pinned on every session and tested
  (`10-authority-and-change-path.md`). It holds whatever role the deployment supplies.
- **Not verifiable from this repository.** Whether the production role is actually SELECT-only is a
  property of the ClickHouse deployment's user and grant definitions, which live outside both the
  kit and the ingest-pipeline repository. Nothing in either repository can prove or disprove it.

Because it is unverifiable here, do not assert it and do not assume it. The named artifact that
settles it is the output of `SHOW GRANTS FOR <the configured user>` run against the target
ClickHouse, or the grant statements in the infrastructure repository that provisions the shared
instance. When a task depends on the answer, ask for one of those two artifacts and record which
one you received. Treating an unverified grant as a control is how a read lane turns out to be
running as `default` with full rights.

Two further properties that need the same evidence and get the same treatment: whether the ingest
role and the read role are distinct roles, and whether the read role can see databases other than
the one it queries.

## Credentials

Credentials reach the runtime from a secret, never from a file in the repository. On this platform
the ingest side takes them from a shared secret named by the chart
(`<repo>/docs/DECISIONS.md` section 10, default `shared-clickhouse-secrets`), and the consumer takes
from the `CLICKHOUSE_PASSWORD` lane key. A password committed to git outlives the commit that
removed it, so the only remedy after an exposure is rotation, and rotation of a shared instance's
credential affects every service on it — say so in the change request.

Threat classes, fail-closed doctrine, and when a change needs a security review at all:
`/alaa-security-review` (`$alaa-security-review`), with tenant isolation specifically in
`references/40-authorization-and-tenancy.md`.

## Go client choice

The kit connects with `github.com/ClickHouse/clickhouse-go/v2` (`go.mod:6`, imported at
`chkit/config.go:9`). `github.com/ClickHouse/ch-go` is present in the module graph as an **indirect**
dependency (`go.mod:34`) and is imported by no kit code; it is the low-level client that
`clickhouse-go` builds on, not a second supported option. `/alaa-golang` (`$alaa-golang`)
`references/40-production-ready-package-catalog.md` records the same default and makes `ch-go`
conditional on a profiled ingest bottleneck. Do not introduce it without that profile.
