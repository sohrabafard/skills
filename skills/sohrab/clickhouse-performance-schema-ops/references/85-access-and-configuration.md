# Client lanes, access, and where every value lives

## Three client lanes

| Lane | Client | Protocol and address | Identity |
| --- | --- | --- | --- |
| ingest | Vector `clickhouse` sink in `wa` | HTTP, `CLICKHOUSE_ENDPOINT`, default `http://shared-clickhouse:8123` (`<repo>/docs/DECISIONS.md` section 10) | the writer role |
| Go read | `alaa-go-chi` `chkit` | native protocol, `CLICKHOUSE_ADDR` as `host:port` with no scheme | the read role |
| PHP read | no fleet kit exists | HTTP | a read role of its own |

The two protocols use different ports, and a swapped value fails like a network fault.
`CLICKHOUSE_USER` and `CLICKHOUSE_PASSWORD` exist on more than one lane and hold a different role on
each. Never assume one value serves two lanes.

## The Go read lane

`alaa-go-chi` `configkit/keys.go` defines the only ClickHouse environment keys. No `CH_*` prefix
exists.

| Key | Meaning | Default |
| --- | --- | --- |
| `CLICKHOUSE_ADDR` | `host:port` of the native-protocol listener | none; blank means the lane is absent |
| `CLICKHOUSE_DATABASE` | database the read session opens | `default` |
| `CLICKHOUSE_USER` | read role | `default` |
| `CLICKHOUSE_PASSWORD` | that role's password | none |
| `CLICKHOUSE_DIAL_TIMEOUT` | connection-establishment bound | `5s` |

- `configkit` resolves the lane and `chkit.ConfigFrom` projects it. A consumer that reads
  `os.Getenv("CLICKHOUSE_ADDR")` has forked the lane; take the value from the resolved config.
- Bind values through the `args ...any` of `Query` and `QueryRow`.
- The kit connects with `github.com/ClickHouse/clickhouse-go/v2`. `github.com/ClickHouse/ch-go` is
  an indirect dependency and no second option. `/alaa-golang`
  `references/40-production-ready-package-catalog.md` makes it conditional on a profiled ingest
  bottleneck; do not introduce it without that profile.
- A change to `chkit` behaviour is a change to the kit: `/alaa-go-chi-development`. A consumer that
  needs a behaviour the kit lacks files the request there and never forks the client.

## The PHP read lane

No fleet kit pins this lane, and ClickHouse maintains no PHP client: its third-party client page
says it "does not maintain the libraries listed below and hasn't done any extensive testing". The
choice of a PHP library is therefore a dependency decision for the owner; ask before you add one.
Whatever the library, the lane must meet these rules:

- **The server enforces the limits, because no kit does.** The PHP read role gets a settings profile
  that sets `readonly`, `max_execution_time` and `max_result_rows` with constraints the client
  cannot loosen, and a `SELECT`-only grant on the rollup database. The owner of shared-instance
  accounts provisions the role and the profile (`/alaa-services-contract`
  `references/15-deployment-and-runtime-contract.md`). Do not ship a PHP reader on a role without
  that profile.
- **Bind every value** with a `{name:Type}` placeholder and its `param_name` request parameter.
- **Send credentials in the `X-ClickHouse-User` and `X-ClickHouse-Key` headers,** never in the URL;
  the official text warns that URL parameters are logged by proxies.
- **An HTTP 200 does not prove success.** The server can fail after it sent the status line and then
  writes the exception into the body. `wait_end_of_query=1` delays the status until the query ends,
  but only while the result fits `http_response_buffer_size`. So also treat a body that carries the
  exception marker named by the `X-ClickHouse-Exception-Tag` response header as a failure.
- **Send no `session_id`.** A session runs one query at a time, and long-lived workers share it.
- **Set the client timeout above `max_execution_time`,** and add no client retry
  (`70-failure-and-degradation.md`).
- Worker and connection lifetime under Octane: `/alaa-octane-performance`. Where the reader class
  sits in the layer map: `/alaa-laravel-architecture`.

Propose the registration of the lane's environment keys in `/alaa-services-contract` before the
first PHP reader ships; do not invent key names in one service.

## Where every other knob lives

| Knob | Lives in | Changed by |
| --- | --- | --- |
| call deadline, pool bounds (`MaxOpenConns`, `MaxIdleConns`, `ConnMaxLifetime`) | `chkit.Config` in the consumer's wiring | the consumer service |
| `max_execution_time`, `max_result_rows` on the Go lane | `chkit.Config.Settings` | the consumer service |
| `readonly=2` on the Go lane | `chkit` internals | **nobody**; it is a kit invariant |
| readiness severity | the consumer's `ReadyCheck` call | the consumer service, with the test in `70-failure-and-degradation.md` |
| batch size, flush interval, buffer, retries | the ingest topology's sink block | the ingest-pipeline repository |
| `index_granularity`, engine, keys, codecs, TTL, deduplication window | the DDL | the ingest-pipeline repository |
| users, roles, profiles, quorum on a writer identity, server and merge-tree settings | the server configuration | the infrastructure operator; no consumer can set them |

A value in none of these rows that this skill does not state is a platform value. Take it from
`/alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`, and request
registration there when it is missing.

## Grants: the part no repository here can verify

`chkit` documents the intended posture: a production role that is `SELECT`-only on the rollup
database, plus the `readonly=2` pin. Only the pin is enforced by code you can read. Whether the role
is `SELECT`-only is a property of the deployment's user and grant definitions.

Do not assert it and do not assume it. The artifact that settles it is the output of
`SHOW GRANTS FOR <the configured user>` on the target ClickHouse, or the grant statements in the
repository that provisions the shared instance. When a task depends on the answer, ask for one of
the two and record which one you received. An unverified grant treated as a control is how a read
lane runs as `default` with full rights.

Two more properties need the same evidence: that the writer role and each read role are distinct
roles, and that a read role cannot see a database other than the one it queries.

## Credentials

Credentials reach the runtime from a secret, never from a file in the repository. The ingest side
takes them from the shared secret the chart names (`<repo>/docs/DECISIONS.md` section 10), and a
consumer takes them from its lane key. After an exposure the only remedy is rotation, and rotation
of a shared instance's credential affects every service on it; say so in the change request.

Threat classes, fail-closed doctrine, and when a change needs a security review:
`/alaa-security-review`; tenant isolation in its `references/40-authorization-and-tenancy.md`.

### The schema client

Run DDL with the native client under the operator-approved address, TLS policy and migration
identity. Pass `--user` and `--host` as arguments. Supply the password through a process-scoped,
secret-backed `CLICKHOUSE_PASSWORD` with shell tracing off, and keep it out of arguments, connection
strings and logs. Validate that the required secrets exist before you connect. Never pass
`--ignore-error` in a schema gate, so that failed SQL stops the run. Audit the client configuration
and arguments for a password that overrides the environment. Prove the effective identity with a
wrong-password failure and with `SELECT currentUser()`.
