# Sources and Freshness

Read this before stating any fact that can change: a version, a default, a release behaviour, a package's status, or a
kit capability.

## When to re-verify

**Rule:** go to the primary source, in this session, before you state any of the following:

- a Go release version, a release date, or a behaviour introduced or removed by a release;
- a package's current major version, its licence, its maintenance status, or a CVE affecting it;
- a framework's current API or its default behaviour;
- a capability of the `alaa-go-chi` kit;
- current guidance from a model or tooling vendor.

**Forbidden:** answering any of those from memory, and prefixing a remembered fact with "as of my knowledge". **Rule:**
either cite the source you read in this session and the date, or say the fact is unverified and name where it would be
checked.

## Kit facts

**Rule:** every claim about `alaa-go-chi` is read from the kit repository — the specific `.go` file, `CONTRACTS.md`,
`GOVERNANCE.md`, `docs/RUNBOOK.md`, `docs/CONSUMERS.md`, or a file under `docs/change-requests/` — and cited by that
path. Governance and phase questions go to `/alaa-go-chi-development` (`$alaa-go-chi-development`).

**Forbidden:** treating a decision record, a change request, a roadmap line, or a design-goal sentence as evidence
that a capability exists in the kit. **Rule:** ratification is not implementation; find the code, name the file.

## Official Go

| Source | Use it for |
|---|---|
| `https://go.dev/doc/devel/release` | the current stable release, supported releases, dates, security notes |
| `https://go.dev/ref/spec` | an exact language, generics, or type-system detail |
| `https://go.dev/doc/modules/layout` | official module and package layout |
| `https://pkg.go.dev` | versions, symbols, examples, importers, licences, CVEs for a published path — queried by `godig` |
| `https://pkg.go.dev/golang.org/x/tools/gopls` | gopls capabilities, MCP tools, code actions, settings |
| `https://oraios.github.io/serena/01-about/020_programming-languages.html` | Serena Go support and its `gopls` prerequisite |
| `https://oraios.github.io/serena/02-usage/050_configuration.html` | Serena Go backend settings forwarded to `gopls` |
| `https://pkg.go.dev/testing` | tests, benchmarks, examples, fuzzing, helpers, cleanup, subtests |
| `https://go.dev/doc/security/fuzz/` | fuzzing rules, seed corpus, deterministic targets |

The release notes for the version `70-modern-go-baseline.md` was written against are named inside that file, with the
date they were read.

## HTTP frameworks

| Source | Use it for |
|---|---|
| `https://github.com/go-chi/chi` · `https://pkg.go.dev/github.com/go-chi/chi/v5` | chi routing and current API |
| `https://pkg.go.dev/github.com/go-chi/chi/v5/middleware` | request id, recovery, timeout, throttle behaviour |
| `https://pkg.go.dev/github.com/go-chi/cors` | CORS middleware behaviour and mounting constraints |
| `https://docs.gofiber.io/` | Fiber; load `/alaa-golang-fiber` (`$alaa-golang-fiber`) for any Fiber task |

## Packages in this stack

`https://pkg.go.dev/github.com/jackc/pgx/v5` · `https://docs.sqlc.dev/` · `https://github.com/pressly/goose` ·
`https://atlasgo.io/docs` · `https://pkg.go.dev/github.com/redis/go-redis/v9` ·
`https://clickhouse.com/docs/integrations/go` · `https://pkg.go.dev/github.com/rabbitmq/amqp091-go` ·
`https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo` · `https://golang.testcontainers.org/`

## Observability and security

`https://opentelemetry.io/docs/languages/go/` ·
`https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp` ·
`https://pkg.go.dev/github.com/prometheus/client_golang/prometheus` ·
`https://pkg.go.dev/github.com/coreos/go-oidc/v3/oidc` · `https://pkg.go.dev/github.com/golang-jwt/jwt/v5`

## Model, effort, and runtime guidance

**Rule:** this skill names no model, no effort level, and no runtime capability. Every such question, and every
vendor source that would answer it, belongs to `/alaa-prompting-guide` (`$alaa-prompting-guide`) and its
`references/50-effort-and-thinking.md`.

## Which source wins

**Rule:** when two sources disagree, take the higher one and record the disagreement:

1. The repository you are working in — its code, tests, generators, and generated artifacts.
2. The kit repository's `CONSTITUTION.md`, `GOVERNANCE.md`, `CONTRACTS.md`, and current source.
3. Official Go documentation.
4. Official documentation for the package or framework in question.
5. The installed `golang-*` skills.
6. The house companion skills.
7. This skill.

**Forbidden:** resolving a disagreement by editing a skill so it agrees. **Rule:** follow the higher source, do the
work, and report the disagreement with both file names in your final message.
