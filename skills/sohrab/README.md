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

- `alaa-project-constitution`
- `alaa-services-contract`
- `alaa-reliability-sla`
- `alaa-security-review`
- `alaa-observability-soc`
- `alaa-controlled-ops`
- `service-runtime-kit-governance`
- `alaa-system-design`
- `alaa-testing-strategy`
- `alaa-algorithms-data-structures`
- `alaa-code-intelligence-routing` — deterministic evidence routing across CodeGraph, Serena, Laravel Boost, native/domain owners, and repository proof; prevents duplicate retrieval and requires same-worktree validation.
- `alaa-keyset-pagination` — cursor/keyset pagination design: deterministic ordering, matching index, cursor integrity and context binding, limits, and the offset exception.
- `alaa-input-normalization` — folding Persian, Arabic and every other non-ASCII decimal digit to ASCII at both input boundaries, under one contract with four implementations and a conformance harness.
- `alaa-prompting-guide`
- `alaa-low-noise`
- `alaa-workflow`

### Multi-agent orchestration and cross-session memory

- `alaa-cc-orchestrator`
- `alaa-codex-orchestrator`
- `alaa-codex-runtime-ops`
- `alaa-memory-os` — a store-agnostic memory operating model: what is worth recording, in what note shape, and with what recall budget. Basic Memory and Hindsight each get one adapter reference and neither is the subject.
- `alaa-extract-agent-lessons` — an intermediate and final curation gate that extracts evidence-backed decision interfaces, judgment rubrics, and durable knowledge cards, keeps active candidates in `alaa-workflow`, and publishes only authorized durable knowledge through `alaa-memory-os`.

### PHP / Laravel and service engineering

- `alaa-php-clean-code`
- `alaa-laravel-architecture`
- `alaa-octane-performance`
- `alaa-laravel-job-rabbitmq`
- `alaa-laravel-public-api-contract-pack`
- `alaa-laravel-upgrade-all-packages`
- `alaa-cicd-laravel-postgres`
- `alaa-permission-generator`

### Go

- `alaa-golang`
- `alaa-golang-clean-code-principles`
- `alaa-golang-fiber`
- `alaa-go-chi-development`

The 46 `golang-*` skills these four route into are upstream subtrees under the repository-root `vendor/`: not pack-local, never edited in place.

### Data and storage

- `alaa-data-layer`
- `alaa-mongodb-patterns`
- `alaa-partitioned-table-fk-audit`
- `alaa-crockford-base32-codecs`
- `clickhouse-performance-schema-ops`
- `alaa-minio-object-storage`
- `alaa-arvan-object-storage`

### Frontend and frontend delivery

- `alaa-frontend-developer`
- `alaa-vue-typescript-clean-code`
- `alaa-quasar-app-vite-v3`
- `alaa-ui-ux-design-system`
- `alaa-frontend-devops`
- `alaa-frontend-doc-annotations`
- `alaa-mono-package`
- `alaa-indexeddb-browser-storage`
- `alaa-shaka-player`

### Containers, CI/CD, Kubernetes, and platform delivery

- `alaa-docker-production`
- `alaa-k8s-helm`
- `alaa-gitlab-ci-cd`
- `alaa-haproxy`
- `alaa-haproxy-lua` — Lua running inside an HAProxy process: execution model, failure visibility at the edge, and testing outside HAProxy. `alaa-haproxy` owns the configuration directives.
- `caas-arvan-kuber`
- `alaa-bash-shell`
- `alaa-makefile`
- `ansible-generator`
- `ansible-validator`

### Messaging, integration, and trust

- `alaa-async-messaging`
- `alaa-trust-gateway-auth`
- `alaa-bale-provider`
- `alaa-sms-provider-mediana`
- `tusd-upload-platform`
- `jitsi-platform-architect`

### Observability, documentation, and knowledge

- `alaa-signoz-clickhouse-docs`
- `vector-rust-observability-pipelines`
- `alaa-postman-collections`
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
