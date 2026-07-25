# Evidence and Module Selection

Read this reference after the root template and before writing. Search narrowly, then read the
smallest set of files that can establish ownership, current behaviour, and real validation
commands.

## Evidence priority

1. Safe executable truth: routes, schemas, migrations, manifests, generated output, tests, CI
   definitions, task runners, and reproducible runtime inspection.
2. Maintained canonical contracts, ADRs, architecture and security documents, and runbooks.
3. The existing constitution as prior governance and a durable record of retained owner
   decisions; agent guidance files as instruction evidence.
4. Owner-supplied intent material — an RFP, a specification, a design brief, or reference
   articles. This establishes what the project is *for* and which archetypes to expect. It does
   not establish what the repository currently does.
5. Current standards and official vendor, framework, platform, and regulator documentation as
   the source of obligation values. Authoritative for what a standard currently requires;
   never proof of project behaviour.
6. Comments, task notes, memory, examples, and secondary external guidance.

Absence from a limited search is not evidence of absence. Record `UNKNOWN` when the inspection
surface is incomplete.

Archetype signals are inventoried by `project-archetypes.md` and are not repeated here. Inspect
for those signals first, because the archetype match drives module retention below. Then
inventory the domains in the table that follows, which establish the project's canonical
governance and its validation surface.

## High-signal inventory

| Domain | Common evidence |
|---|---|
| Instructions | `AGENTS.md`, `CLAUDE.md`, `.claude/**`, `.agents/**`, `.codex/**`, rules, skills |
| Identity and governance | `README*`, docs index, architecture documents, ADRs, governance, contracts, runbooks |
| Upstream contracts | consumed kit, framework, SDK, or scaffold pins; vendored contract copies; conformance tests |
| Language and framework | `go.mod`/`go.work`; `composer.json`/`artisan`; `package.json` and lockfiles; per-language source trees |
| Data and cache | migrations, schema, ORM models, repositories, indexes, backfills, recovery scripts, key builders, TTLs, locks |
| Trust boundary | trusted-header middleware, route posture, proxy and ingress configuration, ACLs and maps |
| Integrations and media | provider adapters, webhook verification, payment/SMS/email/storage contracts, upload, storage, transcoding, playback |
| Search and projections | search engine configuration, projections, indexing, rebuild, replay, reconciliation |
| Infra and runtime | Dockerfiles, Compose, Helm and Kubernetes, Terraform and Ansible, CI/CD, deploy scripts, env templates |
| Observability | tracing, metrics, log pipelines, error reporting, dashboards, alerts, health and readiness endpoints |
| Generated artifacts | generators, templates, golden files, codegen, scaffold tests, API description and SDK artifacts |
| Validation | test suites, lint and type configuration, contract tests, CI job definitions, task targets |

For each material claim, capture source path, what the evidence proves, what it does not prove,
freshness, and confidence. Do not read secrets or reproduce private production data.

## Canonical is not ratified

Record two independent dimensions for every governing source:

- ownership classification — `LOCAL_CANONICAL`, `INCORPORATED_BY_REFERENCE`, `UPSTREAM_CANONICAL`,
  `GENERATED`, `ADVISORY`, or `HISTORICAL`, defined in
  `constitutional-corpus-and-upstream-contracts.md`;
- authority status the source itself proves — `active`, `approved`, `ratified`, `pending`,
  `unknown`, or another evidence-backed project term.

Never infer ratification from canonical ownership, file naming, code enforcement, or age. Detect
two sources claiming canonical ownership of the same detail as drift and resolve it before
ratification.

## Module retention follows the archetype

Modules are the template's structural slots. Retention is decided by the archetype match, not by
whether the code already implements the module's subject.

| State | Condition | Effect |
|---|---|---|
| `INCLUDE` | A matched archetype makes the module's subject mandatory, **or** repository evidence shows the project owns that behaviour, **or** the owner placed it in scope | Retain, and write the obligation even where implementation is absent |
| `EXCLUDE` | Positive evidence places the subject outside owned scope, and no matched archetype requires it | Remove the module and record the evidence path |
| `UNKNOWN` | Inspection cannot establish whether the project owns the subject | Retain a reasoned TODO; never delete silently and never invent a rule |

An implemented-but-unmatched subject is still `INCLUDE` — the code proves ownership. An
archetype-mandated but unimplemented subject is `INCLUDE` as well; that is the case the previous
version of this skill got backwards, deleting exactly the sections a project most needed. Do not
classify from filenames alone when executable ownership is unclear.

Archetype-to-module mapping, applied after the match in `project-archetypes.md`:

| Matched archetype | Modules it makes mandatory |
|---|---|
| Browser web client | `FRONTEND_WEB_SSR_PWA`, and `API_CONTRACTS` when the client owns its own API surface |
| Public HTTP API service | `API_CONTRACTS`, `GATEWAY_PROXY_TRUST` |
| Internal service-to-service API | `API_CONTRACTS`, `GATEWAY_PROXY_TRUST` |
| Asynchronous worker / queue consumer | `ASYNC_JOBS_EVENTS` |
| Scheduled job | `ASYNC_JOBS_EVENTS` |
| Admin or back-office panel | `GATEWAY_PROXY_TRUST`, `OBSERVABILITY_SOC` |
| Mobile BFF | `API_CONTRACTS`, `INTEGRATIONS_WEBHOOKS` where push or provider delivery is owned |
| Real-time / streaming | `REALTIME_STREAMING`, and `MEDIA_FILES` where protected media is served |
| Data or reporting pipeline | `DATA_MIGRATIONS`, `SEARCH_INDEXING` where read models or projections are owned |

Modules outside that mapping — `MONOREPO_PACKAGES_SDK_CLI`, `UPSTREAM_KIT_FRAMEWORK_CONTRACTS`,
`GO_CHI`, `LARAVEL_PHP_OCTANE`, `REDIS_CACHE_LOCKS`, `INFRA_CI_RUNTIME`, `OBSERVABILITY_SOC`,
`DOCS_GENERATED_AGENT_GUIDANCE` — are retained on repository evidence of ownership or explicit
owner scope. A dependency name or an unread environment variable does not prove ownership; a
vendored package, an example directory, or a build-time-only tool is the common false positive.

When `UPSTREAM_KIT_FRAMEWORK_CONTRACTS` applies, record the canonical upstream source, the
consumer version pin, the inherited/local ownership split, the upgrade path, and the conformance
test. Never copy the upstream contract into a locally editable consumer file.

## Validation command discovery

Accept a command only when repository truth contains it: manifest scripts, `Makefile`, Taskfile,
Justfile, shipped scripts, CI steps, maintained developer documentation, or a framework-native
command the project already uses. Do not invent a conventional command because it is common for
the stack. If commands disagree, report drift and prefer the executable or CI-owned path after
verification.

Where an archetype mandates a check the repository has no command for, state the obligation and
record a non-blocking factual TODO naming the missing command. Do not fabricate the command, and
do not drop the obligation because no command exists yet.

For a `THIN_CHARTER`, list an exact command once at most, at its canonical owner, and use compact
change-class references instead of repeating command catalogs per module and again in a matrix.

## Evidence ledger minimum

For each binding rule that carries project-specific facts, capture the rule, its canonical path
and section or symbol, what the evidence proves and does not prove, its freshness or last
verification date, confidence (`HIGH`, `MEDIUM`, `LOW`), and any drift or TODO where sources
disagree. For each rule prescribed by an archetype, capture the archetype, the matching signal,
and the fetched value with its source and date.

Every binding rule that delegates to a contract, guidance file, skill, standard, or runbook names
it in the constitution's compact canonical-source list. The working ledger and the source-role
classification stay out of the final document. Never place secrets, raw logs, or personal or
production data in the ledger.
