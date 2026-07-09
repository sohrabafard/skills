<!--
TEMPLATE-ONLY: PROJECT CONSTITUTION GENERATION CONTRACT

PURPOSE
This is a reusable authoring template, not a pre-written project constitution. Copy it
to a repository root as ./constitution-template.md. An agent creates or updates the
binding ./CONSTITUTION.md from repository evidence and explicit owner decisions.

The visible skeleton intentionally contains placeholders instead of generic policy.
Coverage prompts live in TEMPLATE-ONLY comments and must be removed from the generated
constitution. A prompt, example, model preference, or common best practice is never
binding project policy unless repository evidence or an authorized owner decision makes
it project-specific.

CANONICAL NAMES
- Template: ./constitution-template.md
- Output: ./CONSTITUTION.md
- Correct misspelled constitution filenames; never maintain typo and canonical variants
  as two active policy files.
- {{CONSTITUTION_PATH}} means ./CONSTITUTION.md unless the owner explicitly chooses one
  other correctly spelled path.

OPERATING MODES
- CREATE: no constitution exists. Produce the first project-specific constitution.
- UPDATE: a constitution exists. Read it first and treat the work as evidence
  revalidation plus a focused normative delta. Do not regenerate it from scratch.
- AUDIT: inspect and report drift without editing.

NON-NEGOTIABLE AUTHORING RULES
1. Work from the repository root and obey applicable higher-precedence instructions.
2. In UPDATE mode, read the complete existing constitution before this template.
3. Read this complete template before writing.
4. Read applicable AGENTS.md, CLAUDE.md, named owner sources, and high-signal project
   evidence. Preserve unrelated worktree changes.
5. Use executable repository truth for current behavior. Treat docs, comments, prior
   policy, and memory as claims to verify when verification is practical.
6. Do not infer absence or N/A merely because evidence was not found. Distinguish
   NOT_PRESENT, NOT_INSPECTED, NOT_APPLICABLE, and UNKNOWN.
7. Do not invent routes, services, queues, topics, schemas, environment variables,
   providers, owners, thresholds, dates, domains, commands, SLAs, SLOs, or business rules.
8. Record unresolved facts exactly as:
   TODO(<stable-id>): <what must be confirmed>; reason: <why evidence is insufficient>;
   owner: <role or UNKNOWN>; blocking: <yes|no>.
9. Record suggested but unapproved policy exactly as:
   PROPOSAL(<stable-id>): <candidate rule>; evidence/rationale: <why>;
   approval required from: <role or UNKNOWN>.
10. Retain only conditional modules backed by positive evidence or explicit owner scope.
    Delete irrelevant modules, their validation rows, and their placeholders. UNKNOWN is
    not EXCLUDE; record a TODO when the uncertainty matters.
11. Use MUST/MUST NOT only for objectively testable project invariants. A SHOULD rule
    needs an explicit exception condition. MAY identifies a permitted choice.
12. Remove all TEMPLATE-ONLY comments, authoring prompts, examples, unused rows, and
    unresolved {{PLACEHOLDERS}} from the final document.
13. Do not change application code, dependencies, generated products, deployments,
    shared/production systems, secrets, or Git history while authoring the constitution.

REQUIRED EVIDENCE WORKFLOW
Phase A - Preflight and authority map
- Resolve root, template, output, mode, applicable guidance, allowed edits, and owner
  context. Inspect Git status when available.
- In UPDATE mode, read prior rules, stable IDs, exceptions, ratification metadata,
  amendment history, last evidence review, and documented concerns before anything else.

Phase B - Evidence inventory and classification
- Inventory maintained docs/ADRs, manifests/lockfiles, source roots, routes, schemas,
  migrations, messages, tests, task runners, CI, generated owners, deployment/runtime
  config, security guidance, telemetry, and runbooks.
- Prefer targeted search and bounded reads. Never expose secrets or private production data.
- Build an evidence ledger: claim, source, what it proves, confidence, and freshness.
- Classify every conditional module INCLUDE, EXCLUDE, or UNKNOWN. EXCLUDE needs positive
  evidence of irrelevance or an explicit scope decision.

Phase C - Writing pass 1: evidence-backed draft
- Create/update {{CONSTITUTION_PATH}} as internal draft work.
- In UPDATE mode, start from the existing constitution and apply only supported deltas.
  Preserve valid project-specific policy, stable IDs, history, original ratification date,
  and live exceptions. Do not rewrite unchanged policy for style.
- Fill retained placeholders with concrete, testable, project-specific content.
- Keep one Sync Impact Report as the first HTML comment. Do not report completion yet.

Phase D - Writing pass 2: independent constitutional review
- Reopen and reread the full file from disk as if reviewing another agent's work.
- Compare it with the prior constitution, template, owner input, applicable guidance,
  canonical docs, manifests, CI, generated outputs, and executable truth.
- Remove unsupported specificity and generic filler. Verify every MUST and every command.
- Verify module pruning, TODOs, proposals, exceptions, version/date, authority, bindings,
  maintenance cadence, amendment history, and guidance drift.
- Record meaningful refinements in the Sync Impact Report.

Phase E - Binding and validation
- Ensure root AGENTS.md requires agents to read the constitution.
- Ensure root CLAUDE.md imports @CONSTITUTION.md where supported, or explicitly requires
  it when imports are unavailable. Keep both as thin adapters, not policy copies.
- Run safe document checks. Report remaining uncertainty and drift before finishing.

UPDATE / PERIODIC REVIEW RULES
- An update is a revalidation of current evidence and a normative delta, not a fresh
  generation. Read old policy first and preserve anything still valid.
- Compare repository changes since Last evidence review, plus high-risk surfaces whose
  freshness cannot safely be inferred from a diff.
- Classify each prior rule: PRESERVED, CLARIFIED, ADDED, STRENGTHENED, WEAKENED, REMOVED,
  or UNRESOLVED. WEAKENED/REMOVED rules need explicit rationale and approval.
- Evidence refresh with no normative change updates review metadata/report only and does
  not require a version bump.
- Trigger a review on the filled cadence and on filled events such as stack, ownership,
  contract, trust boundary, data, deployment, validation, or critical-journey changes.

INITIAL VERSION POLICY
- First approved binding constitution: 1.0.0.
- Owner-requested non-binding draft: 0.1.0 with status DRAFT.
- Updates preserve the original ratification date and derive version from normative impact.
- Use the runtime date only when available as evidence; never fabricate history.

FINAL DOCUMENT SHAPE
- The Sync Impact Report is the first block and remains one HTML comment.
- The first visible line is "# <Project Name> Constitution".
- Required universal headings remain; irrelevant conditional modules disappear.
- No TEMPLATE-ONLY content or unexplained placeholder remains.
- The result is self-contained without this template or skill.
END TEMPLATE-ONLY GENERATION CONTRACT
-->

<!--
Sync Impact Report
Mode: {{CREATE_UPDATE_OR_AUDIT}}
Constitution path: {{CONSTITUTION_PATH}}
Version: {{OLD_VERSION_OR_NONE}} -> {{NEW_VERSION}}
Status: {{DRAFT_BINDING_OR_NEEDS_REVIEW}}
Template used: {{TEMPLATE_PATH}}
Prior constitution(s) read: {{PATHS_OR_NONE}}
Owner input used: {{SUMMARY_OR_NONE}}
Evidence inspected:
- {{EVIDENCE_PATH_AND_PURPOSE}}
Evidence review window / delta basis: {{REVIEW_WINDOW_OR_CREATE_BASELINE}}
Project classification: {{PROJECT_TYPE_AND_BOUNDARIES}}
Included conditional modules:
- {{MODULE_ID_AND_EVIDENCE}}
Removed conditional modules:
- {{MODULE_ID_AND_REASON}}
Unknown/deferred modules:
- {{MODULE_ID_AND_TODO}}
Prior-rule disposition summary:
- {{PRESERVED_CLARIFIED_ADDED_STRENGTHENED_WEAKENED_REMOVED_UNRESOLVED}}
Normative changes:
- {{RULE_DELTA_OR_NONE}}
Pass 2 refinements:
- {{REFINEMENT_OR_NONE}}
Binding status:
- AGENTS.md: {{ALIGNED_CHANGED_MISSING_OR_DRIFT}}
- CLAUDE.md: {{ALIGNED_CHANGED_MISSING_OR_DRIFT}}
- README/docs index: {{ALIGNED_CHANGED_NOT_REQUIRED_OR_DRIFT}}
Validation performed:
- {{CHECK_AND_RESULT}}
Open TODOs / proposals / exceptions / conflicts:
- {{ITEM_OR_NONE}}
-->

# {{PROJECT_NAME}} Constitution

## 1. Constitution Metadata

<!-- TEMPLATE-ONLY:
Fill every retained row from evidence. Use a structured TODO when a required fact is
unknown. Do not guess an approver, date, cadence, or repository root.
-->

| Field | Value |
|---|---|
| Status | {{DRAFT_BINDING_NEEDS_REVIEW_OR_SUPERSEDED}} |
| Version | {{SEMVER}} |
| Ratified | {{YYYY_MM_DD_OR_TODO}} |
| Last amended | {{YYYY_MM_DD_OR_TODO}} |
| Last evidence review | {{YYYY_MM_DD_OR_TODO}} |
| Next scheduled review | {{DATE_EVENT_OR_TODO}} |
| Owner / approving role | {{OWNER_ROLE_OR_TODO}} |
| Governed repository root | {{REPOSITORY_ROOT}} |
| Constitution path | {{CONSTITUTION_PATH}} |
| Source template | {{TEMPLATE_PATH}} |
| Supersedes | {{PRIOR_VERSION_OR_NONE}} |

{{STATUS_AND_EFFECT_RULE}}

## 2. Scope, Authority, and Conflict Resolution

<!-- TEMPLATE-ONLY:
Define exact governed and excluded surfaces, agents/people/automation, environments, and
policy authority. Keep platform/runtime precedence intact. Separate instruction priority
from factual evidence priority. State how conflicts and non-compliant implementation are
handled; implementation drift must not silently rewrite policy.
-->

### 2.1 Governed scope

{{GOVERNED_SCOPE}}

### 2.2 Explicit exclusions and ownership boundaries

{{EXCLUSIONS_AND_BOUNDARIES}}

### 2.3 Instruction authority

{{INSTRUCTION_PRECEDENCE}}

### 2.4 Factual source priority and conflict handling

{{FACT_PRIORITY_AND_CONFLICT_RULE}}

## 3. Project Identity and Evidence Map

<!-- TEMPLATE-ONLY:
Describe only verified project facts. Keep evidence paths repository-relative where
possible. A file's existence proves only what was actually inspected. Delete irrelevant
rows and add project-specific rows when useful.
-->

### 3.1 Identity and owned surfaces

| Topic | Evidence-backed value | Canonical evidence |
|---|---|---|
| Purpose and critical users | {{PURPOSE_AND_USERS}} | {{SOURCE}} |
| Critical user/operator journeys | {{CRITICAL_JOURNEYS}} | {{SOURCE}} |
| Criticality and failure impact | {{CRITICALITY}} | {{SOURCE}} |
| Primary stacks and runtimes | {{STACKS_AND_RUNTIMES}} | {{SOURCE}} |
| Owned apps/services/packages | {{OWNED_SURFACES}} | {{SOURCE}} |
| External systems/providers | {{EXTERNAL_DEPENDENCIES}} | {{SOURCE}} |
| Data/messaging/infrastructure ownership | {{TECHNICAL_OWNERSHIP}} | {{SOURCE}} |
| Explicit non-goals | {{NON_GOALS}} | {{SOURCE_OR_OWNER_DECISION}} |

### 3.2 Canonical source registry

| Domain | Canonical source path(s) | What it owns | Freshness/validation rule |
|---|---|---|---|
| {{DOMAIN}} | {{PATHS}} | {{OWNERSHIP}} | {{FRESHNESS_RULE}} |

### 3.3 Evidence ledger

| Claim or decision | Evidence path / command | What it proves | Confidence | Last verified |
|---|---|---|---|---|
| {{CLAIM}} | {{SOURCE}} | {{PROOF_BOUNDARY}} | {{HIGH_MEDIUM_LOW}} | {{DATE}} |

### 3.4 Constitution maintenance contract

<!-- TEMPLATE-ONLY:
Set a realistic evidence-review cadence and event triggers. Include high-risk surfaces
that must always be rechecked even when no obvious file delta exists. Define who approves
normative changes and how unchanged rules are preserved. Never invent a calendar date.
-->

| Maintenance field | Project-specific contract |
|---|---|
| Review cadence | {{REVIEW_CADENCE}} |
| Event-triggered reviews | {{REVIEW_TRIGGERS}} |
| Always-refresh evidence surfaces | {{ALWAYS_REFRESH_SURFACES}} |
| Delta comparison basis | {{DELTA_COMPARISON_METHOD}} |
| Rule disposition method | {{RULE_DISPOSITION_METHOD}} |
| Review owner / approver | {{REVIEW_OWNER_AND_APPROVAL}} |
| Staleness response | {{STALE_CONSTITUTION_RESPONSE}} |

## 4. Normative Language and Unknowns

<!-- TEMPLATE-ONLY:
Define MUST, SHOULD, MAY, TODO, PROPOSAL, EXCEPTION, UNKNOWN, and N/A as used by this
project. Preserve the structured TODO/PROPOSAL/EXCEPTION formats required by the authoring
contract. State that missing evidence is not proof of absence.
-->

{{NORMATIVE_LANGUAGE_AND_UNKNOWN_HANDLING}}

## 5. Universal Principles

<!-- TEMPLATE-ONLY:
Retain all eleven headings. Under each, author only project-specific, testable rules
supported by evidence or explicit owner policy. A heading may contain a structured TODO
or a short evidence-backed N/A rationale, but never generic filler.
-->

### I. Evidence, Freshness, and No Fabrication

<!-- TEMPLATE-ONLY: Cover factual authority, current-source checks, uncertainty, and
prohibition on invented contracts/commands/thresholds where applicable. -->

{{EVIDENCE_FRESHNESS_RULES}}

### II. Ownership, Boundaries, and Dependency Direction

<!-- TEMPLATE-ONLY: Cover source-of-truth owners, layer/service/package/data boundaries,
dependency direction, and cross-boundary access. -->

{{OWNERSHIP_BOUNDARY_RULES}}

### III. Security, Privacy, Identity, and Secrets

<!-- TEMPLATE-ONLY: Derive trust boundaries, authorization/tenancy, sensitive data,
secret handling, logging/redaction, privileged actions, and security validation. -->

{{SECURITY_PRIVACY_RULES}}

### IV. Contracts, Compatibility, and Generated Ownership

<!-- TEMPLATE-ONLY: Identify actual contracts and consumers; cover compatibility,
deprecation/migration, generators, and breaking-change approval only where applicable. -->

{{CONTRACT_COMPATIBILITY_RULES}}

### V. Maintainable Architecture and Clean Code

<!-- TEMPLATE-ONLY: Fill the project's real layering, domain ownership, abstraction,
error, naming, duplication, dependency, and complexity rules. -->

{{ARCHITECTURE_CODE_QUALITY_RULES}}

### VI. Test-Gated Quality and Validation Integrity

<!-- TEMPLATE-ONLY: Name actual test layers, change-to-proof mapping, failure-path proof,
test integrity, coverage policy if evidence-backed, and reporting semantics. -->

{{TEST_VALIDATION_RULES}}

### VII. Reliability, Concurrency, and Failure Behavior

<!-- TEMPLATE-ONLY: For applicable runtimes cover timeouts, cancellation, retries,
idempotency, ordering, backpressure, limits, shutdown, recovery, and degraded modes. -->

{{RELIABILITY_FAILURE_RULES}}

### VIII. Performance and Resource Efficiency

<!-- TEMPLATE-ONLY: Define measured surfaces, representative workloads, metrics, tools,
baselines, budgets, regression policy, and exception process. If no approved numeric
budget exists, use a structured TODO; never invent one. -->

{{PERFORMANCE_RESOURCE_RULES}}

### IX. Observability, Auditability, and Operability

<!-- TEMPLATE-ONLY: Derive actual log/error/metric/trace/health contracts, correlation,
cardinality/redaction, dashboards, alerts, SLOs, runbooks, and incident ownership. -->

{{OBSERVABILITY_OPERABILITY_RULES}}

### X. Accessibility, UX, Localization, and Human Safety

<!-- TEMPLATE-ONLY: Apply only to relevant human-facing surfaces. Cover actual states,
semantics, keyboard/focus, language/direction, responsive behavior, and safety needs. -->

{{ACCESSIBILITY_UX_LOCALIZATION_RULES}}

### XI. Controlled Change, Documentation, and Supply Chain

<!-- TEMPLATE-ONLY: Define scope/reversibility, destructive/external approval, docs/code/
generated synchronization, dependency provenance/license/security, and release hygiene. -->

{{CONTROLLED_CHANGE_SUPPLY_CHAIN_RULES}}

## 6. Change Risk and Required Gates

<!-- TEMPLATE-ONLY:
Create project-specific risk tiers. Do not pre-classify absent domains. Risk is based on
impact, reversibility, blast radius, and uncertainty rather than file count. Name actual
review, proof, and approval owners. Remove unused rows or add justified tiers.
-->

| Risk tier | Project trigger | Required plan/review | Required proof | Approval |
|---|---|---|---|---|
| {{RISK_TIER}} | {{TRIGGER}} | {{PLAN_REVIEW}} | {{PROOF}} | {{APPROVAL}} |

{{RISK_CLASSIFICATION_RULE}}

## 7. Conditional Project Modules

<!-- TEMPLATE-ONLY:
For each module: INCLUDE only with positive evidence or explicit owner scope; EXCLUDE only
with positive irrelevance/scope evidence; UNKNOWN is not EXCLUDE. In the final file,
delete every unused module including this prompt. For retained modules replace every
placeholder with project-specific rules, sources, budgets, exceptions, and real commands.
Subsections inside a retained module may also be deleted when irrelevant.
-->

### Module MONOREPO_PACKAGES_SDK_CLI

<!-- TEMPLATE-ONLY: Consider multiple packages/apps, shared libraries, SDKs, CLIs,
scaffolds, public exports, dependency direction, versioning, builds/dist, generators,
publishing, and consumer proof. -->

- Evidence and owned surfaces: {{MONOREPO_EVIDENCE_AND_SCOPE}}
- Binding rules: {{MONOREPO_RULES}}
- Required validation: {{MONOREPO_VALIDATION}}

### Module API_CONTRACTS

<!-- TEMPLATE-ONLY: Consider owned HTTP/RPC/GraphQL/OpenAPI/Postman/SDK contracts,
route/version/auth, request/response/error/pagination/idempotency, compatibility,
deprecation, consumers, operational endpoints, and contract proof. -->

- Evidence and owned contracts: {{API_EVIDENCE_AND_SCOPE}}
- Binding rules: {{API_CONTRACT_RULES}}
- Required validation: {{API_VALIDATION}}

### Module GO_CHI

<!-- TEMPLATE-ONLY: Retain for evidence-backed Go services/packages; cover real package
layers, router/middleware/errors, context/cancellation, concurrency/shutdown, config,
data/external boundaries, telemetry, benchmarks, and actual Go commands. -->

- Evidence and owned surfaces: {{GO_EVIDENCE_AND_SCOPE}}
- Binding rules: {{GO_RULES}}
- Required validation: {{GO_VALIDATION}}

### Module LARAVEL_PHP_OCTANE

<!-- TEMPLATE-ONLY: Retain for evidence-backed PHP/Laravel. Cover real layering,
policies/auth/tenant boundaries, Eloquent/query/migrations/transactions, queues/events/
scheduler, and long-lived worker reset/state rules only when Octane is present. -->

- Evidence and owned surfaces: {{LARAVEL_EVIDENCE_AND_SCOPE}}
- Binding rules: {{LARAVEL_RULES}}
- Required validation: {{LARAVEL_VALIDATION}}

### Module FRONTEND_WEB_SSR_PWA

<!-- TEMPLATE-ONLY:
Retain for browser UI, browser SDK, Vue/React/Quasar/Nuxt/Next or comparable evidence.
Delete irrelevant SSR, SEO, PWA, media, and browser-storage topics individually.

Derive rules for actual component/state/service boundaries, browser trust, XSS/CSRF/CSP,
tokens/storage/privacy, responsive design, accessibility, keyboard/focus, RTL/i18n,
routing, loading/error/degraded states, SSR/hydration/status, SEO metadata/canonical/
structured data, and PWA cache/update/offline behavior.

Performance coverage must ask, not assume:
- Which routes and critical journeys are measured under which device/network/profile?
- Is Lighthouse/Lighthouse CI configured? What runs, aggregation, and approved thresholds
  exist for performance, accessibility, best practices, and SEO?
- Which LCP, INP, CLS, TTFB or other browser/server metrics have approved sources/budgets?
- Which JS/CSS/image/font/chunk budgets exist?
- Which DOM element-count, maximum-depth, and maximum-children limits exist, how are they
  measured, and what exception process applies?
- Which hydration, long-task, memory, listener, rendering, and interaction budgets exist?
If no approved numeric budget exists, use a structured TODO and retain measured baselines;
do not convert example values or generic recommendations into policy.
-->

- Evidence, owned apps, modes, and browsers: {{FRONTEND_EVIDENCE_AND_SCOPE}}
- Architecture, security, UX, SSR/SEO/PWA rules: {{FRONTEND_RULES}}
- Performance measurement and approved budgets: {{FRONTEND_PERFORMANCE_CONTRACT}}
- Required validation: {{FRONTEND_VALIDATION}}

### Module GATEWAY_PROXY_TRUST

<!-- TEMPLATE-ONLY: Distinguish application-side trusted identity/header/route posture
from proxy/ingress ownership. Cover stripping/spoofing, exposure, TLS/ACL/maps/rewrites,
upstreams/health/reload, timeouts/retry/failover, and telemetry propagation as evidenced. -->

- Evidence and owned boundary: {{GATEWAY_EVIDENCE_AND_SCOPE}}
- Binding rules: {{GATEWAY_RULES}}
- Required validation: {{GATEWAY_VALIDATION}}

### Module DATA_MIGRATIONS

<!-- TEMPLATE-ONLY: Consider owned schemas/migrations/repositories/indexes/backfills/
seeders. Cover source of truth, isolation/privacy/retention, transactions/consistency/
locks, additive rollout/rollback/compatibility, query/index/partition proof, backup/
restore/repair/reconciliation, and actual commands. -->

- Evidence and owned data: {{DATA_EVIDENCE_AND_SCOPE}}
- Binding rules: {{DATA_RULES}}
- Required validation: {{DATA_VALIDATION}}

### Module REDIS_CACHE_LOCKS

<!-- TEMPLATE-ONLY: Consider Redis/cache/session/lock/idempotency/rate-limit evidence.
Cover namespaces/cardinality, TTL/invalidation/staleness/source of truth, locking and
rate-limit correctness, outage/degraded/recovery behavior, and actual validation. -->

- Evidence and owned role: {{REDIS_EVIDENCE_AND_SCOPE}}
- Binding rules: {{REDIS_RULES}}
- Required validation: {{REDIS_VALIDATION}}

### Module ASYNC_JOBS_EVENTS

<!-- TEMPLATE-ONLY: Consider brokers/queues/topics/events/jobs/outbox/inbox/consumers/
schedulers. Cover schemas/compatibility, delivery/idempotency/ordering/dedupe/replay,
retry/backoff/DLQ/poison/reconciliation, transaction boundaries, concurrency/backpressure/
shutdown, observability, and actual proof. -->

- Evidence and owned flows: {{ASYNC_EVIDENCE_AND_SCOPE}}
- Binding rules: {{ASYNC_RULES}}
- Required validation: {{ASYNC_VALIDATION}}

### Module REALTIME_STREAMING

<!-- TEMPLATE-ONLY: Consider WebSocket/SSE/long polling/live collaboration/streaming.
Cover authentication/re-auth, authorization, ordering/resume/duplicates/reconnect/
heartbeat, connection/resource/backpressure limits, degraded/fallback behavior, and proof. -->

- Evidence and owned channels: {{REALTIME_EVIDENCE_AND_SCOPE}}
- Binding rules: {{REALTIME_RULES}}
- Required validation: {{REALTIME_VALIDATION}}

### Module INTEGRATIONS_WEBHOOKS

<!-- TEMPLATE-ONLY: Consider external API/provider/callback/payment/SMS/email/auth/storage
and webhooks. Cover credentials, timeout/retry/circuit/quota, authenticity/replay/
idempotency/ordering, sandbox/contract tests, fallback/reconciliation/exit, and proof. -->

- Evidence and owned integrations: {{INTEGRATION_EVIDENCE_AND_SCOPE}}
- Binding rules: {{INTEGRATION_RULES}}
- Required validation: {{INTEGRATION_VALIDATION}}

### Module MEDIA_FILES

<!-- TEMPLATE-ONLY: Consider upload/download/object storage/documents/images/audio/video/
streaming/transcoding/DRM/signed URLs. Cover validation/scanning, keys/isolation/retention,
authorization/range/cache, playback/license/captions, cleanup/orphans/recovery, and proof. -->

- Evidence and owned media: {{MEDIA_EVIDENCE_AND_SCOPE}}
- Binding rules: {{MEDIA_RULES}}
- Required validation: {{MEDIA_VALIDATION}}

### Module SEARCH_INDEXING

<!-- TEMPLATE-ONLY: Consider search engines, projections, materialized views, indexing,
ranking/autocomplete/read models. Cover source-of-truth relation, schema compatibility,
refresh/rebuild/replay/reconciliation, freshness/relevance/privacy/tenant filtering,
load/performance budgets, and proof. -->

- Evidence and owned indexes: {{SEARCH_EVIDENCE_AND_SCOPE}}
- Binding rules: {{SEARCH_RULES}}
- Required validation: {{SEARCH_VALIDATION}}

### Module INFRA_CI_RUNTIME

<!-- TEMPLATE-ONLY: Consider Docker/Compose/Kubernetes/Helm/Terraform/Ansible/CI/CD,
deployment, runtime config, and scripts. Cover image/build provenance, config/secrets,
resources/probes/scaling/network/storage, CI gates/artifact promotion, rollout/rollback,
shared/production approval and render/dry-run paths. -->

- Evidence and owned environments: {{INFRA_EVIDENCE_AND_SCOPE}}
- Binding rules: {{INFRA_RULES}}
- Required validation: {{INFRA_VALIDATION}}

### Module OBSERVABILITY_SOC

<!-- TEMPLATE-ONLY: Consider telemetry libraries/config, collectors, dashboards, alerts,
SLOs, incidents, SOC/audit logs, and runbooks. Cover stable contracts/correlation,
cardinality/sampling/retention/redaction, ownership, integrity/access, and proof. -->

- Evidence and owned telemetry: {{OBSERVABILITY_EVIDENCE_AND_SCOPE}}
- Binding rules: {{OBSERVABILITY_RULES}}
- Required validation: {{OBSERVABILITY_VALIDATION}}

### Module DOCS_GENERATED_AGENT_GUIDANCE

<!-- TEMPLATE-ONLY: Consider docs/specs/OpenAPI/Postman/code generation/scaffolds/golden
files/templates/runbooks/AGENTS.md/CLAUDE.md/skills. Cover canonical sources, regeneration,
drift detection, links/rendering/indexes, nested guidance, and synchronization proof. -->

- Evidence and owned artifacts: {{DOCS_EVIDENCE_AND_SCOPE}}
- Binding rules: {{DOCS_GENERATED_GUIDANCE_RULES}}
- Required validation: {{DOCS_GENERATED_VALIDATION}}

## 8. Project Validation Matrix

<!-- TEMPLATE-ONLY:
Create only rows required by retained principles/modules and real project commands.
Commands must exist in evidence or be a structured TODO. Map each change class to exact
proof and a blocking rule. Include failure-path and critical-journey proof where relevant.
Never describe a skipped, blocked, or not-run gate as passed.
-->

| Surface / change class | Required command or check | Evidence produced | Blocking condition |
|---|---|---|---|
| {{CHANGE_CLASS}} | {{COMMAND_OR_CHECK}} | {{EVIDENCE}} | {{BLOCKING_RULE}} |

{{BLOCKED_GATE_REPORTING_RULE}}

## 9. Constitution Check for Every Non-Trivial Change

<!-- TEMPLATE-ONLY:
Turn the relevant questions below into a concise project-specific checklist. Cover:
affected principles/modules/risk; inspected truth; owners/consumers; trust/data/privacy;
failure/retry/rollback/recovery/compatibility; performance/accessibility/resource budgets;
telemetry/runbooks; exact validation run; docs/generated/agent-guidance alignment; and
remaining assumptions/TODOs/proposals/exceptions. Remove irrelevant questions.
-->

{{PROJECT_CONSTITUTION_CHECKLIST}}

## 10. Agent Operating Contract

<!-- TEMPLATE-ONLY:
Define evidence-backed before/during/before-completion behavior for agents. Include scope,
worktree preservation, approval boundaries, smallest coherent changes, validation, honest
reporting, long-work state when the repository has an approved mechanism, and real blocker
conditions. Do not prescribe tools or workflows absent from the repository.
-->

### Before work

{{AGENT_BEFORE_WORK_RULES}}

### During work

{{AGENT_DURING_WORK_RULES}}

### Before completion

{{AGENT_COMPLETION_RULES}}

## 11. AGENTS.md and CLAUDE.md Binding

<!-- TEMPLATE-ONLY:
The constitution is canonical project policy; runtime guidance files must be thin adapters,
not duplicate copies. Inspect existing root/nested files and preserve their content.

Fill an AGENTS.md adapter that requires reading the canonical path before planning,
editing, reviewing, or runtime/deployment changes; states its binding scope; requires
conflict/drift disclosure; and points to amendment/exception handling.

For Claude Code, use an exact top-level @CONSTITUTION.md import when supported, plus a
short binding rule. If imports are unavailable, use an explicit read requirement. Record
any higher-precedence or nested guidance conflict rather than silently overwriting it.
-->

### Root AGENTS.md adapter contract

{{AGENTS_BINDING_RULE}}

### Root CLAUDE.md adapter contract

`@CONSTITUTION.md`

{{CLAUDE_BINDING_RULE}}

### Binding status

| Surface | Path | Status | Required action |
|---|---|---|---|
| {{AGENT_RUNTIME}} | {{GUIDANCE_PATH}} | {{STATUS}} | {{ACTION_OR_NONE}} |

{{NESTED_GUIDANCE_RULE}}

## 12. Governance, Amendments, and Exceptions

<!-- TEMPLATE-ONLY:
Fill semantic-version impact rules, evidence-only refresh behavior, amendment authority,
required evidence, and exception constraints. A normative weakening/removal must be
explicit. Exceptions should be narrow, approved, time-bounded, reviewable, and unable to
silently rewrite the underlying rule. Tailor high-risk approval to verified project roles.
-->

### 12.1 Versioning and evidence refresh

{{VERSIONING_AND_EVIDENCE_REFRESH_RULES}}

### 12.2 Amendment process

{{AMENDMENT_PROCESS}}

### 12.3 Exception process

{{EXCEPTION_PROCESS}}

| ID | Rule | Scope | Reason | Risk / mitigation | Owner / approver | Starts | Expires | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| {{EXCEPTION_ID_OR_NONE}} | {{RULE}} | {{SCOPE}} | {{REASON}} | {{MITIGATION}} | {{OWNER}} | {{DATE}} | {{DATE}} | {{PATH}} | {{STATUS}} |

### 12.4 Amendment history

| Version | Date | Status | Summary | Evidence / decision | Approver |
|---|---|---|---|---|---|
| {{VERSION}} | {{DATE}} | {{STATUS}} | {{SUMMARY}} | {{PATH_OR_DECISION}} | {{APPROVER}} |

## 13. Open Decisions and Follow-up

<!-- TEMPLATE-ONLY:
List only live structured TODOs and PROPOSALs. Remove the table if none remain and say
"None" only when the evidence review genuinely resolved all items.
-->

| ID | Type | Question / action | Evidence gap or rationale | Owner | Blocking | Review target | Status |
|---|---|---|---|---|---|---|---|
| {{STABLE_ID_OR_NONE}} | {{TODO_OR_PROPOSAL}} | {{ITEM}} | {{REASON}} | {{OWNER}} | {{YES_NO}} | {{DATE_EVENT_OR_TODO}} | {{STATUS}} |

## 14. Final Ratification

<!-- TEMPLATE-ONLY:
State the exact scope and effect of DRAFT/BINDING/NEEDS_REVIEW. Confirm the governing
version, status, ratification date, last amendment, last evidence review, and approving
role. Do not use ceremonial or generic policy language.
-->

{{RATIFICATION_STATEMENT}}

**Version**: {{SEMVER}} | **Status**: {{STATUS}} | **Ratified**: {{DATE_OR_TODO}} | **Last Amended**: {{DATE_OR_TODO}} | **Last Evidence Review**: {{DATE_OR_TODO}}
