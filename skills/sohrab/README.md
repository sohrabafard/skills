# Sohrab Skills

This pack is a public installable skill set for production-oriented coding agents.

Invoke any skill named here with `/name` in Claude Code and `$name` in Codex; both forms name the same skill.

The current pack mixes two patterns on purpose:

- routing-first umbrella skills where one entrypoint owns a full surface
- explicit generator/validator pairs where the narrow artifact workflow is still useful

## Pack design rules

- a Codex agent can load only a skill that ships `agents/openai.yaml`, and all 69 of the 69 skill folders here do, verified with `python scripts\check_skill_index.py`
- no skill states a model name; model, effort, and runtime-capability questions route to `/alaa-prompting-guide` (`$alaa-prompting-guide`)
- mature surfaces prefer one routing-first owner instead of many tiny near-duplicates
- companion skills stay explicit where ownership boundaries still matter
- `AGENTS.md` here owns how a skill is written and structured; this file does not repeat it

### Path notation in a citation

A path written in a skill points either at a file that ships with that skill or at a file in the repository an agent is working on, and an unmarked path does not say which. Two markers do, and `python scripts\check_fleet_references.py` reads them:

- `$SKILL_DIR/<path>` — a file bundled inside the citing skill. The checker resolves it, and a missing file is a finding.
- `<repo>/<path>` — a path in the target repository. The checker never resolves it, because this repository cannot know what is there.

Mark the path whenever you write or edit a citation. An unmarked path that resolves nowhere is reported as informational and never fails a run, so the fleet can be converted one skill at a time and no intermediate state breaks the gate. `alaa-postman-collections` already uses both markers.

The durable home for this convention is `skills/sohrab/AGENTS.md`, beside the rule that a cross-skill reference names its owning skill; it is stated here because that file was outside the scope of the change that added the markers.

## Core precedence rules

When two skills state the same rule, `AGENTS.md` names the owner and the side that points. It owns those boundaries; the rules below do not repeat them.

### 1. Arvan-first platform policy

If an infrastructure, Kubernetes, Helm, or deployment task targets ArvanCloud CaaS, the pack-level source of truth is `caas-arvan-kuber`. If generic infra advice conflicts with Arvan constraints, Arvan-first wins unless the user explicitly approves an override.

### 2. Gateway trust policy

If a service lives behind the Ala gateway, the trust-boundary source of truth is `alaa-trust-gateway-auth`: JWT-derived identity, trusted header rules, tenant and project boundary propagation, downstream service trust decisions, and auth-service route and error-contract guidance.

### 3. Frontend family policy

For the standard Vue 3 + Quasar + Vite app family, start with `alaa-frontend-developer`. Apply `alaa-vue-typescript-clean-code` as the quality baseline whenever coding, review, or refactor touches Vue SFCs, composables, Pinia stores, frontend TypeScript, or package-grade Vue APIs. Then route to the smallest companion skill that owns the next decision:

- build, deployment, Docker, CI, artifact, public-path, CDN, or proxy concerns: `alaa-frontend-devops`
- documentation-only JSDoc or inline-comment work: `alaa-frontend-doc-annotations`
- workspace package, `packages/*`, peer dependency, or asset-emission issues: `alaa-mono-package`
- Quasar CLI, `quasar.config`, mode-specific, or Quasar upgrade details: `alaa-quasar-app-vite-v3`
- component library, design tokens, or visual governance: `alaa-ui-ux-design-system`

### 4. PHP / Laravel coding baseline

For PHP / Laravel work, the default coding baseline is `alaa-php-clean-code`. Use it together with the smallest relevant companion skills: `alaa-laravel-architecture`, `alaa-data-layer`, `alaa-async-messaging`, `alaa-laravel-job-rabbitmq`, `alaa-octane-performance`, `alaa-security-review`, `alaa-observability-soc`, `alaa-cicd-laravel-postgres`, `alaa-repo-docs`, `alaa-mongodb-patterns`, `alaa-trust-gateway-auth`, `alaa-workflow`.

## Before assuming a service already conforms

`alaa-services-contract/references/95-fleet-conformance.md` records, for the date at its top, which of seven Ala components satisfy which contract rules and what each one that does not must change. Read it before planning a migration, sequencing a fleet change, or writing any sentence that assumes a named service already conforms. It states no rule: the numbered reference file beside each row wins, and where the snapshot and the repository in front of you disagree, the repository is right.

## Pack-local vs system-level dependencies

Everything under `## Current skill map` ships with the `sohrab` pack and is the portable public install surface. The three below are system-level helpers: referenceable, not pack-local, not replaced by anything in the pack.

- `/openai-docs` (`$openai-docs`) — official OpenAI and Codex guidance, citations, prompt updates, CLI or app behavior
- `/playwright` (`$playwright`) — explicit browser automation, navigation, or browser-based QA
- `/playwright-interactive` (`$playwright-interactive`) — persistent browser debugging loops when the task needs interactive browser work

## Default workflows

These sequences route to owners; they do not restate what an owner decides. Three decisions come before the sequence they sit in, in all three workflows:

- **Design before implementation.** When a change meets any condition in the trigger list owned by `/alaa-system-design` (`$alaa-system-design`), run that pass before writing code; read the list there rather than judging by the size of the change.
- **Test design.** Test layer, double choice, and the proof level a claim has reached are decided by `/alaa-testing-strategy` (`$alaa-testing-strategy`).
- **Failure and load behaviour.** Doctrine is `/alaa-reliability-sla` (`$alaa-reliability-sla`); the Ala values those mechanisms are set to are `/alaa-services-contract` (`$alaa-services-contract`).

### Frontend workflow

1. Start with `alaa-frontend-developer`, then apply `alaa-vue-typescript-clean-code`.
2. Route to the companion skill named in precedence rule 3 as soon as the task crosses that boundary.
3. Pair with `alaa-quasar-app-vite-v3` when Quasar-specific behavior or config is part of the root cause.
4. Keep pure visual art direction outside this pack unless a separate design skill is available in the session.
5. Use `$playwright` or `$playwright-interactive` only when browser work is explicitly needed.

### PHP / Laravel workflow

1. Inspect the repository and existing conventions.
2. Use `alaa-workflow` for non-trivial, multi-file, risky, or long tasks.
3. Read `alaa-trust-gateway-auth` first when trusted headers, tenant derivation, or gateway auth semantics are involved.
4. Use `alaa-permission-generator` when adding or changing catalog-owned coarse permissions or `config/permissions.php`.
5. Apply `alaa-php-clean-code` as the default coding baseline.
6. Pull in specialist skills only where the task actually enters their scope.
7. Keep docs, tests, and operational notes aligned before treating the work as done: `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns aligned for tests, `/alaa-services-contract` (`$alaa-services-contract`) for contract artifacts, `/alaa-observability-soc` (`$alaa-observability-soc`) for operational notes.

### Infra and delivery workflow

1. Start with the routing-first owner when one exists: `alaa-k8s-helm`, `alaa-gitlab-ci-cd`, `alaa-bash-shell`, `alaa-makefile`, `alaa-docker-production`.
2. Apply platform policy from `caas-arvan-kuber`, `alaa-haproxy`, or service-specific companion skills as needed.
3. Use explicit generator/validator pairs only on surfaces that still keep that split.
4. Keep operator-facing notes and rollback expectations aligned with the final output.

## Current skill map

Every folder in this directory appears exactly once between the markers below, and every name between them is a folder. `python scripts\check_skill_index.py` asserts both directions and fails when either is false, which is what makes this sentence checkable rather than aspirational. `README.fa.md` carries the same names with a one-line purpose for each; its membership matches this map exactly, and its group boundaries do not — it splits doctrine and multi-agent routing into nine sections where this file uses eight.

<!-- skill-map:start -->

### Core Ala architecture and policy

- `alaa-project-constitution` — authors and governs a repository's `CONSTITUTION.md` and its thin `AGENTS.md`/`CLAUDE.md` bindings, matching the repository's project archetypes and prescribing the obligations a service of that kind owes, including ones the code does not implement yet.
- `alaa-services-contract` — the normative shared-surface contract for Ala backend services and `@alaa/*` packages: response and error envelopes, health/readiness shapes, trusted gateway headers, public identifiers, event and code names, permission catalogs, broker and metric registries, and deadlines.
- `alaa-reliability-sla` — language-independent reliability doctrine for services under a 99.99%+ SLA: deadlines and timeouts, retries with jittered backoff, circuit breakers, bulkheads, load shedding, graceful degradation, idempotency, error budgets, and the fault injection that proves each mechanism fired.
- `alaa-security-review` — the security review gate for production multi-tenant services: trust boundaries, authn/authz, tenant isolation, injection, XSS, SSRF, uploads and secrets, and fail-closed behaviour, emitted as a per-item PASS/FAIL/N-A verdict with a remediation plan.
- `alaa-observability-soc` — observability and SOC signal architecture: which signal a question needs, what requirement level binds, and which gate blocks a ship, across traces, metrics, logs, profiles, cardinality/sampling budgets, burn-rate alerting, and SOC/SIEM egress.
- `alaa-controlled-ops` — ownership boundary and release governance for the `alaa/controlled-ops` Composer package and the services that adopt it: package-owned versus adopter-owned behaviour, Satis publishing, tag moves, and canonical-hash verification.
- `service-runtime-kit-governance` — ownership and debug governance for `service-runtime-kit`-generated local Docker Compose/Swarm runtime in Laravel or PHP repositories: which layer owns a runtime fix, generated-file boundaries, and version pinning.
- `alaa-system-design` — the pre-implementation design method for a service, subsystem, or class set: bounding the subsystem, contracts derived before code, data ownership, compared candidates, and one reviewable design record.
- `alaa-testing-strategy` — test design doctrine for services that must not fail: which layer a behaviour belongs at, when to fake, stub, or use the real dependency, the six proof levels, and telling a flaky test from an intermittent product defect.
- `alaa-algorithms-data-structures` — complexity budgets and structure choice for service code: the bound an operation must hold as input grows, choosing a structure from the access pattern, and catching the N+1 family before a growing path ships with no stated bound.
- `alaa-code-intelligence-routing` — deterministic evidence routing across CodeGraph, Serena, Laravel Boost, native/domain owners, and repository proof; prevents duplicate retrieval and requires same-worktree validation.
- `alaa-keyset-pagination` — cursor/keyset pagination design: deterministic ordering, matching index, cursor integrity and context binding, limits, and the offset exception.
- `alaa-input-normalization` — folding Persian, Arabic and every other non-ASCII decimal digit to ASCII at both input boundaries, under one contract with four implementations and a conformance harness.
- `alaa-prompting-guide` — the sole owner of model, effort, and runtime-capability questions: writing, reviewing, repairing, and compressing prompts, skills, subagent definitions, and `AGENTS.md`/`CLAUDE.md` files for the current model roster. Owns the behavior-preserving compression contract every instruction artifact is edited under, and installs the `alaa-rule-writer` wording specialist on activation.
- `alaa-low-noise` — context economy and output discipline for non-trivial agent work in Claude Code and Codex: bounding what enters the context window and what gets printed during broad discovery, large diffs, long logs, or delegated subagent lanes.
- `alaa-workflow` — adaptive workflow control for long-running, multi-phase, resumable, or handoff-sensitive repository work: an ordered plan, durable continuation across compaction, machine-readable state, and generated agent prompts.

### Multi-agent orchestration and cross-session memory

- `alaa-cc-orchestrator` — production-grade multi-agent coding orchestration for Claude Code: installs the pack's managed agent roster, plans first, sizes the pipeline to that plan, and routes work through scoped implementation, verification, review, and specialist gates.
- `alaa-codex-orchestrator` — the same production-grade multi-agent orchestration model as `alaa-cc-orchestrator`, built for Codex: managed agent TOMLs, plan-first sizing, and scoped implementation, verification, and review gates.
- `alaa-codex-runtime-ops` — Codex runtime and harness recovery on Windows: sandbox setup failures, Git Bash/MSYS signal-pipe and `CreateFileMapping` errors, Docker named-pipe denial, locked session files, and exact-command escalation decisions.
- `alaa-memory-os` — a store-agnostic memory operating model: what is worth recording, in what note shape, and with what recall budget. Basic Memory and Hindsight each get one adapter reference and neither is the subject.
- `alaa-extract-agent-lessons` — an intermediate and final curation gate that extracts evidence-backed decision interfaces, judgment rubrics, and durable knowledge cards, keeps active candidates in `alaa-workflow`, and publishes only authorized durable knowledge through `alaa-memory-os`.

### PHP / Laravel and service engineering

- `alaa-php-clean-code` — PHP 8.5 and Laravel 13 code craft for Octane-safe services: naming, SOLID, pattern and smell diagnosis, repository-first persistence, cache-decorator caching, size budgets, and refactor blast radius.
- `alaa-laravel-architecture` — the Laravel layer map and legal call graph for Ala services (Controller → Service → Repository → DB): where the cache seam, error envelope, and domain events are produced, and a gate for layer violations and public-id leaks.
- `alaa-octane-performance` — Octane runtime safety and hot-path performance for Laravel services with long-lived workers: what must never survive between requests, the reset mechanism, worker lifecycle, and the leak regression test.
- `alaa-laravel-job-rabbitmq` — Laravel queued jobs on RabbitMQ through `vladimir-yuldashev/laravel-queue-rabbitmq`: the `queue:work` versus `rabbitmq:consume` decision, ack/nack policy, delivery limits and the crash-loop hazard, and eight named failure classes.
- `alaa-laravel-public-api-contract-pack` — builds and audits a Laravel service's public API contract pack from executable repository truth: route inventory, versioning, per-route retry semantics, OpenAPI/Postman/SDK docs, and a gate that blocks an unresolved deprecation date.
- `alaa-laravel-upgrade-all-packages` — the Composer/npm dependency-upgrade sweep for a Laravel service: restore point and test baseline first, then outdated/audit state, severity-based advisory triage, blocked-bump capture, and a revertible change.
- `alaa-cicd-laravel-postgres` — release gates for Laravel services on Postgres: which checks are gates versus advisory, the migration up-down-up reversibility gate, per-worker test-database isolation, and Postgres production-version parity.
- `alaa-permission-generator` — registers, generates, applies, and validates Alaa coarse permissions through `alaa-permission-catalog`: permission keys and bitmap ids, Laravel/Go/TypeScript consumers, the auth seed, and trusted `X-Access` bitmap decoding.

### Go

- `alaa-golang` — the front door and router for Go work on the Ala platform: the HTTP framework decision (the `alaa-go-chi` kit on chi is the default), deadline propagation, request-decoding limits, repository/cache boundaries, and TDD — load this before any other Go skill.
- `alaa-golang-clean-code-principles` — the mandatory kit-era Go clean-code baseline for services on `alaa-go-chi`: thirteen P1-P13 principles (trust boundary, errors as domain values, one transaction/one truth, idempotency, and more), each with a wrong/right example and a named proof.
- `alaa-golang-fiber` — Fiber v3 work in Ala Go systems, for a repo that already imports Fiber or holds a recorded Fiber exception: app config, `fiber.Ctx` lifetime, middleware order, error mapping, and the v2-to-v3 migration.
- `alaa-go-chi-development` — governance contract for the shared `alaa-go-chi` kit and the services built on it: kit-owner intake, change and release; consumer bootstrap, diagnosis, upgrade and migration; and the phase-aware execution-scope gate read from the kit repository.

The 46 `golang-*` skills these four route into are upstream subtrees under the repository-root `vendor/`: not pack-local, never edited in place.

### Data and storage

- `alaa-data-layer` — Postgres-truth data-layer policy for the Ala fleet: which store owns a fact, tenant-scoped schema/index design, migrations that never lock a live table, query/pool tuning, and Redis run as a cache the request survives losing.
- `alaa-mongodb-patterns` — MongoDB mechanism for the Ala fleet: document/collection shape, tenant-scoped compound indexes, TTL and retention, idempotent upserts and bulk writes, read/write concern, and primary-election read behaviour.
- `alaa-partitioned-table-fk-audit` — audits a PostgreSQL repository for foreign keys that reference a partitioned table through an incomplete key (SQLSTATE 42830), and ships a tested detector plus a durable regression test.
- `alaa-crockford-base32-codecs` — a lowercase Crockford Base32 and UUIDv7 codec bundle with four byte-identical implementations (PHP, JavaScript, bash, HAProxy Lua) and a harness proving they still agree; not a source of secrets or key material.
- `clickhouse-performance-schema-ops` — ClickHouse schema, ingest, query, and operations policy for the Ala fleet: `CREATE TABLE`/`ORDER BY`/`PARTITION BY` choices, merge-backlog and part-count control, and materialized view versus projection versus TTL versus partition-drop decisions.
- `alaa-minio-object-storage` — object-storage platform policy for the Ala fleet's MinIO and S3-compatible buckets: bucket/key design, tenant scoping, lifecycle and multipart-abort rules, versioning, presigned URLs, and the failure classes of an unreachable store.
- `alaa-arvan-object-storage` — ArvanCloud Object Storage differences layer over the shared S3/MinIO platform policy: regional endpoints, virtual-hosted addressing, the account-level key model, the S3 compatibility matrix, and the 400 MB part ceiling.

### Frontend and frontend delivery

- `alaa-frontend-developer` — the frontend engineering policy and routing hub for the Vue 3 + Quasar + Vite app family: SSR/hydration determinism, SSR auth and session posture, PWA/service-worker policy, and the Lighthouse/Core Web Vitals playbook — start here, then route to the smallest companion skill.
- `alaa-vue-typescript-clean-code` — the mandatory Vue 3, Quasar, Vite and TypeScript clean-code contract: script-setup typing, composable/Pinia shape, SOLID and code-smell repair, TypeScript depth, and hard size budgets — apply before changing any `.vue` or `.ts` file.
- `alaa-quasar-app-vite-v3` — the version-aware control plane for Quasar CLI on `@quasar/app-vite` v3 (plus v2 maintenance and the v2-to-v3 migration): `quasar.config`, boot/routing, platform modes, service workers, and accessibility/performance budgets.
- `alaa-ui-ux-design-system` — UI/UX design decisions for Vue/Quasar apps: design tokens, theming, dark mode, typography, RTL and Persian typography, motion, component states, and accessibility patterns.
- `alaa-frontend-devops` — CI and pipeline gates for a frontend repository: the build artifact contract, public path and asset base, cache policy, build provenance, and what may be compiled into a client bundle.
- `alaa-frontend-doc-annotations` — a documentation-only pass over frontend code — JSDoc and inline comments on Vue/Quasar/Vite files — in a diff whose build output is byte-identical before and after; never used when the change alters behaviour.
- `alaa-mono-package` — workspace package engineering under `packages/*`: exports maps and public entrypoints, peer dependencies, package CSS/asset emission, build order, and how the root app consumes an internal package.
- `alaa-indexeddb-browser-storage` — the browser's own storage substrate for the Ala fleet: IndexedDB semantics, origin quota, eviction, schema upgrade branching, multi-tab/service-worker concurrency, and which data classes may land on a device.
- `alaa-shaka-player` — the complete Shaka Player capability atlas: lifecycle, DASH/HLS, adaptive bitrate, DRM, offline download, the error taxonomy, and the Vue plus Quasar binding.

### Containers, CI/CD, Kubernetes, and platform delivery

- `alaa-docker-production` — Dockerfiles, Compose/Swarm stack files, build secrets, attestation, healthchecks, and resource-limit keys for a production-shaped image and runtime file; decides no gate itself — gate policy belongs to `alaa-frontend-devops`.
- `alaa-k8s-helm` — the unified Kubernetes, Helm, OpenShift, and `kubectl`/`oc` skill: generating, validating, and debugging charts and manifests, version- and access-aware, namespace-safe by default, with a live gate register before any change.
- `alaa-gitlab-ci-cd` — generates, validates, reviews, and debugs GitLab CI/CD pipelines, reusable components, runner configs, and container-build workflows; owns how a gate is expressed on a runner, never whether a check should block.
- `alaa-haproxy` — HAProxy configuration, tuning, troubleshooting, and upgrade work: turning routing, TLS, caching, rate-limiting, and drain decisions into directives, proved with `haproxy -c -f`.
- `alaa-haproxy-lua` — Lua running inside an HAProxy process: execution model, failure visibility at the edge, and testing outside HAProxy. `alaa-haproxy` owns the configuration directives.
- `caas-arvan-kuber` — Arvan CaaS platform facts for Kubernetes/Helm workloads that diverge from stock Kubernetes: the namespace-scoped API surface, alias-versus-canonical RBAC identity, requests-equal-limits admission parity, and undocumented exposure annotations.
- `alaa-bash-shell` — the full Bash and POSIX shell lifecycle: generating, refactoring, validating, and debugging `.sh`/`.bash` scripts, with a mandatory `-h`/`--help` contract and ShellCheck/shfmt/checkbashisms/Bats workflows.
- `alaa-makefile` — generates, validates, refactors, modernizes, and debugs GNU Make and `.mk` build files: phony targets, variable design, recursive make, shell-safety in recipes, and mbake/checkmake/unmake validation.
- `ansible-generator` — generates production-ready Ansible playbooks, roles, task files, and inventories with FQCN-correct modules and idempotent tasks, then hands the result to `ansible-validator`.
- `ansible-validator` — validates, lints, security-audits, and dry-runs existing Ansible playbooks, roles, and inventories with ansible-lint, yamllint, check mode, Checkov, and Molecule, reporting a verdict with remediation citations.

### Messaging, integration, and trust

- `alaa-async-messaging` — RabbitMQ message-plane architecture for the Ala fleet: the seam between a database commit and a published message, the transactional outbox, publisher confirms, prefetch/concurrency, dead-letter topology, and the DLQ replay procedure.
- `alaa-trust-gateway-auth` — trust-boundary authority for the Ala gateway: who may assert a trusted request header, JWT verification order, compact-claim projection into `X-Project-Id`/`X-User-Id`/`X-Access` headers, TOTP step-up, and fail-closed cases at that boundary.
- `alaa-bale-provider` — the Bale Safir messaging-provider contract for Alaa services: `send_message`/`upload_file` wire shapes, phone normalisation, the `request_id` idempotency key, Safir error codes, and failure classes.
- `alaa-sms-provider-mediana` — the Mediana/IPPanel Edge SMS provider contract for Alaa services: wire shapes, canonical recipient rendering, webservice/pattern sends, voice OTP, and timeout/ambiguous-send handling.
- `tusd-upload-platform` — the resumable-upload platform skill covering the tusd server/library, tus-js-client, and the Ala tusd service: size caps, retention/reaper policy, hook failure posture, per-method authorization, and upload incident triage.
- `jitsi-platform-architect` — self-hosted Jitsi Meet/Videobridge as an Ala subsystem for online classes: the join-token trust domain, room-name entropy, guest-domain lockdown, recording governance, and live-conference failure classes; Jitsi is planned here, not yet deployed.

### Observability, documentation, and knowledge

- `alaa-signoz-clickhouse-docs` — SigNoz ClickHouse SQL for dashboard panels over OpenTelemetry logs/traces/metrics: the vendor-owned `signoz_*` tables, sorting keys, bucket-filter and resource-CTE idioms, rollup selection, and missing-span diagnosis.
- `vector-rust-observability-pipelines` — production Vector pipelines: topology and per-path delivery contracts, VRL transforms, buffering and end-to-end acknowledgements, backpressure, sink retry/batching, and destination-unreachable behaviour.
- `alaa-postman-collections` — creates, updates, synchronizes, and validates Postman Collection v2.1 collections and environments so every request carries success and error examples, a token-capturing post-response script, and tests that fail against a broken implementation.
- `alaa-repo-docs` — repository-level documentation: onboarding, architecture, API summaries, data, errors, events, observability, and internal navigation. It preserves each existing document's language, creates localized companions only when explicitly requested, and keeps one canonical home per topic with relative links from other documents.

<!-- skill-map:end -->

## Consolidated or removed from this pack

These names appeared in earlier versions of the map and have no folder here, re-checked 2026-07-30. Do not re-add one before its folder exists on disk. A rename is listed here too, old name first, so a stale pointer resolves to its replacement.

- `dockerfile-*` — replaced by `alaa-docker-production`; `makefile-generator`, `makefile-validator` — replaced by `alaa-makefile`
- `azure-pipelines-*`, `github-actions-*`, `jenkinsfile-*` — `alaa-gitlab-ci-cd` is the only CI surface this pack ships
- `terraform-*`, `terragrunt-*` — infrastructure targets route through `caas-arvan-kuber` and `alaa-k8s-helm`
- `alaa-basic-memory-os` — renamed to `alaa-memory-os`, because the model is store-agnostic and Basic Memory is one adapter
- `promql-*`, `logql-generator`, `loki-config-generator`, `fluentbit-*` — `alaa-observability-soc` owns signal and gate decisions; `alaa-signoz-clickhouse-docs` and `vector-rust-observability-pipelines` own the query and pipeline surfaces

## Definition of done

Work in this pack is considered ready when:

- the smallest correct skill is easy to discover from `SKILL.md`
- detailed guidance is preserved in one-hop `references/` or `docs/` files
- `agents/openai.yaml` exists and matches the current skill intent
- stale donor skill names are removed from active routing docs
- `python scripts\check_skill_index.py` reports no index finding and no `agents/openai.yaml` gap
- examples, checklists, and anti-patterns are preserved in simple English
- system-level helpers are clearly separated from pack-local skills

## Practical note

When a generic best practice conflicts with the Ala gateway trust model, Arvan platform rules, or the frontend artifact contract, document the reason for the deviation instead of hiding it.
