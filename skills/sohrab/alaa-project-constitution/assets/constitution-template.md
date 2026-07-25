<!--
TEMPLATE-ONLY: PROJECT CONSTITUTION GENERATION CONTRACT

This template is self-contained by design. It travels to repositories that do not have the
authoring skill installed, so every rule an agent needs is stated here. Read it in full.

PURPOSE
Create or update one repository constitution that states what this service owes. The final
document is law - not authoring telemetry, a tutorial, an evidence report, or a description of
agent runtimes.

CANONICAL PATHS
- This file is the generation contract wherever it is read from - the authoring skill's bundled
  assets, or a copy an owner placed in a repository. A repository is not required to hold a copy,
  and a missing copy never blocks generation.
- Output: ./CONSTITUTION.md at the repository root.
- Keep exactly one correctly spelled active constitution.
- Where a second constitution template is also present, generate from the one named for this run
  and report every contradiction between the two to the owner instead of merging them silently.

OPERATING MODES
- CREATE: no prior constitution exists.
- UPDATE: treat the existing constitution as the durable prior-decision record, preserve its
  semantic intent, and apply only supported normative deltas. Do not regenerate from scratch or
  ask the owner to repeat information already retained there.
- AUDIT: report drift without editing.

THE FACT/OBLIGATION SEAM - READ THIS BEFORE ANY OTHER RULE
Two claim classes run through this workflow. The anti-fabrication rules apply to exactly one of
them, and blending them makes a constitution either dishonest or useless.

- A REPOSITORY FACT is a statement about this repository: what it currently runs, which
  endpoints, jobs, queues, or tables exist, which limits are configured, which contracts are in
  force, which dates and approvals were recorded. Never invent a fact about this repository.
  Inspect it, or record it as unknown. Never infer one from a dependency name, a convention, or
  a plausible default.
- A DOMAIN OBLIGATION is a statement about what a service of this kind owes. Prescribing that a
  browser client holds a Largest Contentful Paint budget, or that a queue consumer is
  idempotent, is a standard being applied - not a fact being invented. The archetype layer below
  authorises these, and they are written whether or not the code implements them yet.

Keep four claim labels distinct in working state, and never write a prescription in the voice of
an observation:
- OBSERVED repository truth, carrying an inspected path.
- INHERITED rules from still-valid prior governance.
- INFERRED_CANDIDATE obligations prescribed by a matched archetype or the quality bar. This is a
  first-class route to binding law, not a holding pen for material that gets pruned. What it may
  never do is assert current behaviour: where the current state is unknown or non-conformant,
  the rule is written and a non-blocking factual TODO records the gap.
- OWNER_DECIDED choices the owner made in this run or a prior one.

These labels are working state. They never appear in CONSTITUTION.md.

EVIDENCE WORKFLOW
1. Inspect instructions and Git status; preserve unrelated work.
2. In UPDATE mode, read the complete existing constitution before this template.
3. Read this template completely.
4. Build a prior-decision map from the existing constitution: preserved principles, open TODOs
   and proposals, exceptions, canonical sources, status and version, and missing provenance.
5. Inventory executable truth, canonical contracts and governance, architecture, tests, CI,
   generators, runbooks, consumers, security boundaries, and upstream contracts.
6. Match the project archetypes below from observable signals. Do this before module
   classification. A project matches as many archetypes as its signals support.
7. Infer the project's intent, owned outcomes, critical journeys, load-bearing qualities, and
   plausible failure modes from current user context, prior governance, and repository truth.
8. Carry every matched archetype's mandatory obligations forward as INFERRED_CANDIDATE, then
   walk the cross-cutting quality bar over every owned journey and high-risk surface.
9. Verify the current value of every obligation's metric from primary sources.
10. Build the evidence ledger, source-role map, module classification, candidate dispositions,
    decision gaps, ratification evidence, and binding state as internal working data.
11. Ask only essential unresolved owner decisions. A deferred answer makes a new or already
    non-binding result DRAFT/NON_BINDING and prevents new bindings. During an update to an
    existing BINDING constitution, preserve that baseline and its adapters unchanged unless the
    owner explicitly approves replacing it with a draft.
12. Write binding rules from matched-archetype obligations, repository evidence, still-valid
    prior governance, or explicit owner decisions. Never invent a fact about this repository -
    what it runs, which endpoints or jobs exist, which limits are configured, which contracts
    are in force, which dates or approvals were recorded. Domain obligations are a different
    class and the archetype layer authorises them.
13. Keep research-derived implementation ideas outside CONSTITUTION.md unless an obligation
    requires them, they become a durable owner decision, or they are delegated to a named
    canonical source.
14. Perform two writing passes, then the final constitutional compression pass.
15. Bind AGENTS.md and CLAUDE.md externally, only after BINDING is authorized.
16. Validate the final document and the bindings, then report authoring evidence in the agent's
    final response - not inside CONSTITUTION.md.

PROJECT ARCHETYPE LAYER
An obligation listed under a matched archetype is mandatory whether or not the current code
implements it. A missing implementation is a gap for the constitution to govern, never evidence
that the obligation does not apply. A project with no service worker still owes a stated
service-worker or no-service-worker decision; a project with no performance budget still owes a
budget. Drop an obligation only on positive evidence that the surface is outside owned scope,
recorded with the evidence path. "The code does not do this yet" is never that evidence.

State which metric and that a budget is required. Never write a threshold, score, percentile,
or version gate from memory: fetch the current value from its primary source at authoring time
and record the value with its source URL and verification date.

- BROWSER WEB CLIENT. Signals: a browser framework or bundler manifest, index.html, router
  config, component trees, SSR/SSG framework config, a web app manifest, a service-worker file,
  browser test config.
  Mandatory obligations:
  (a) A Core Web Vitals budget naming Largest Contentful Paint, Interaction to Next Paint, and
      Cumulative Layout Shift, each with its percentile, its device and network class, and the
      named routes it governs. A budget with no percentile or no named route is not a budget.
  (b) Both measurement sources named - which tool produces the lab number, which produces the
      field number, and which one the budget is enforced against.
  (c) Lighthouse category budgets for each category the project owns - Performance,
      Accessibility, Best Practices, SEO - with the exact command or CI job that produces them
      and whether a score below budget fails the build or files a ticket.
  (d) SEO obligations matched to the rendering strategy actually in use, because a rule written
      for the wrong strategy is inert. Server-rendered: every indexable route returns its
      primary content, title, meta description, and canonical link in the initial HTML response
      at a stated status code, and a soft 404 returning 200 with an empty shell is a defect.
      Prerendered or static: which routes are prerendered, what a request for a route absent
      from the build manifest receives, and the rebuild trigger with its maximum staleness.
      Client-rendered: what a crawler executing no JavaScript receives for every indexable
      route and which mechanism provides it, plus the rule that indexable content never depends
      on a user interaction. All strategies: one canonical URL per indexable resource; a stated
      rule for trailing slashes, query-parameter variants, and locale variants; a named owner
      for the robots policy and sitemap; and non-production environments not indexable, with
      the mechanism named.
  (e) Metadata and structured data: a named owner per indexable route type for title, meta
      description, canonical link, social-preview fields, and hreflang where locales exist, plus
      the structured-data types emitted and the validator that gates them.
  (f) Generative-engine visibility: the policy for AI and answer-engine crawlers stated by name
      in the robots policy, and load-bearing facts present as text in the response body rather
      than only inside an image, a canvas, or a payload arriving after hydration. Whether to
      permit those crawlers is an owner decision; having no position is not an option.
  (g) Service worker lifecycle and update strategy: registration scope; which routes and asset
      classes may be served from cache and which always go to the network; the cache versioning
      scheme; what happens to previous-version caches on activation; how a user on an old
      worker receives a new release, including whether it applies on next navigation or
      immediately and how in-flight work is protected; and the removal path, so shipping a
      build that drops the worker does not pin users to a stale cache permanently. Where a
      service worker is out of scope, state that as a decision with its reason.
  (h) Failed responses are never cached. A response enters a client-side store - service worker
      cache, an application-controlled HTTP cache directive, an in-memory query cache, or a
      persistent browser store - only when it is a success. Non-success statuses, network
      failures, timeouts, aborted requests, and partial or truncated bodies are never stored and
      never served to a later read as though they had succeeded. Negative caching, where wanted,
      is a separate short-lived cache with its own key namespace and maximum age, so a
      dependency failing during a deploy cannot become the value a user sees all session.
  (i) Offline and degraded-network behaviour per critical journey: what the user sees and can do
      with no network, with a slow network, and on a mid-request failure; which journeys must
      complete offline, which show a stated degraded state, and which may block; and the client
      retry policy, with the rule that a non-idempotent write is never retried without an
      idempotency key.
  (j) Cache invalidation strategy per client-side cache: its key, what invalidates it, its
      maximum age, how a stale entry is detected, how a deploy invalidates asset and data
      caches, and for user-scoped data a key that includes the owning identity plus a sign-out
      that clears every store holding it.
  (k) Accessibility: the conformance standard, version, target level, and the routes and
      components in scope; the automated gate and its command; plus keyboard reachability for
      every interactive control, a visible focus indicator, an accessible name for every
      control, and a stated announcement for each asynchronous state change.
- PUBLIC HTTP API SERVICE. Signals: externally reachable route registration, an API description
  document, a published SDK, third-party auth middleware, rate-limit config, a version prefix.
  Mandatory: a versioning and compatibility rule with a support window; one error envelope with
  a status mapping and no internal exception text in a client body; authentication and
  authorization per route class, denying a new route until its class is declared; bounded
  request bodies and page sizes with a stated rejection; rate limiting with its keying identity
  and overload shed behaviour; idempotency keys for unsafe methods with a stated honour window
  and replay result; per-dependency timeouts and bounded retries under a total deadline smaller
  than the caller's; a propagated correlation identifier; paginated collections with a maximum
  page size; and a deprecation and sunset path with minimum notice.
- INTERNAL SERVICE-TO-SERVICE API. Signals: service discovery or mesh config, mTLS material,
  cluster-local hostnames, RPC or protobuf definitions, shared DTO packages.
  Mandatory: an explicit trust boundary with the rule that network reachability is never
  authorization; a wire-format schema evolution rule with its CI compatibility check;
  per-dependency timeout, retry, and circuit-breaking policy whose retry budget cannot amplify a
  downstream failure; inbound deadline propagation to every outbound call; bounded concurrency
  per caller with a stated response at the bound; a partial-failure contract naming which
  callers may proceed degraded and on what content; and one named owner per contract with the
  consumer change-request path.
- ASYNCHRONOUS WORKER / QUEUE CONSUMER. Signals: broker config, queue/topic/exchange
  declarations, consumer or job classes, dead-letter tooling, outbox or inbox tables, prefetch
  and heartbeat settings.
  Mandatory: stated delivery semantics, assuming at-least-once unless the pinned broker's
  documentation proves otherwise; idempotent handlers with a stated deduplication identity and
  retention window; bounded retries with backoff and jitter and a named terminal destination,
  never silent discard; a poison-message rule removing a deterministically failing message from
  the hot path within a stated attempt count; ordering stated as required per key or explicitly
  not guaranteed; lease handling and a maximum handler duration; a named backlog lag signal with
  its alert condition and drain plan; side-effect safety through an idempotency key or a
  compensating action; and graceful shutdown within a stated drain window.
- SCHEDULED JOB. Signals: crontab entries, a CronJob resource, framework scheduler
  registrations, interval annotations, a scheduler service in compose or chart values.
  Mandatory: an overlap rule per job, either a named lock or explicit overlap safety; a
  missed-run rule for a scheduler outage window; restart safety with its checkpoint or
  transactional boundary; bounded work per run with maximum batch and duration and the behaviour
  at each bound; explicit timezone and daylight-saving semantics for any locally scheduled job;
  and run observability emitting start, end, outcome, and processed count, with an alert when
  the job has not succeeded within a stated window.
- ADMIN OR BACK-OFFICE PANEL. Signals: routes behind an elevated role, staff-only guards, CRUD
  over production entities, bulk-action or export endpoints, impersonation features.
  Mandatory: authorization per action and per record defaulting to deny, with the rule that
  hiding a control is never authorization; an audit trail of actor, action, target, the change,
  timestamp, and correlation identifier in a store the actor cannot edit, with a stated
  retention; destructive-action protection with a confirmation requirement, a maximum record
  count per operation, and a recovery path; impersonation scope, maximum duration, dual-identity
  audit, and forbidden actions; field-level read control with masking and audited exports; and
  the panel's network exposure and authentication factors stated explicitly.
- MOBILE BFF. Signals: endpoints shaped for one client, per-call upstream aggregation,
  client-version headers or minimum-version gates, push registration, per-platform payloads.
  Mandatory: a minimum supported client version with the server's behaviour for older clients, a
  support window, and no contract break while a version remains supported; a forced-update path
  and its delivery mechanism; a maximum response size and composition rather than proxying; a
  partial-upstream-failure contract naming absent sections and their representation; offline and
  resumption rules where a token-refresh failure does not destroy unsent user work;
  at-least-once push with a deduplication key and never as the only delivery path for a state
  change; and payload variants per device class.
- REAL-TIME / STREAMING. Signals: WebSocket or SSE endpoints, heartbeat and reconnect logic,
  presence tracking, pub/sub fan-out, media or licence endpoints, sticky-session config.
  Mandatory: authentication at connect and re-authentication on credential expiry, so a
  connection never outlives the authorization that opened it; bounded reconnect with backoff and
  jitter, a resume cursor, and a stated rule for what was missed while disconnected; heartbeat
  and dead-peer detection intervals on both ends; fan-out bounds per node and per identity with
  a shed behaviour; backpressure as a bounded buffer, a prioritised drop policy, or
  disconnection; per-channel delivery and ordering guarantees; and what a client experiences on
  node loss, with the location of session state.
- DATA OR REPORTING PIPELINE. Signals: ETL or ELT job definitions, warehouse or analytics
  schemas, materialised views or projections, report generators, change-data-capture config,
  orchestrator DAG or model definitions.
  Mandatory: lineage naming upstream sources and the transformation owner, with the rule that a
  report never becomes the authority for a fact the operational store owns; reproducibility from
  inputs plus a stated watermark and late-arrival window; idempotent reload with its key and
  write strategy; a per-dataset freshness contract with its measuring signal and alert
  condition; in-pipeline correctness assertions that stop publication rather than publish a
  partial dataset; a backfill procedure with a blast-radius bound and consumer notification;
  retention, deletion, and personal-data propagation to every derived copy; and a cost bound for
  the largest job with the behaviour when exceeded.

WHEN ARCHETYPES INTERACT
Resolve overlapping obligations explicitly rather than writing both rules. A browser client plus
its own API share one idempotency decision. A worker plus a pipeline must agree on the
deduplication identity and the reload key, or a replay double-counts. An admin panel plus any
personal-data surface govern read control and retention together. A real-time surface plus a
mobile BFF share one credential-rotation contract. Record each resolved overlap once, in the
principle that owns the surface, and cite it from the other.

CROSS-CUTTING QUALITY BAR
Every service in scope is production, security-sensitive, high-concurrency, and carries an
availability target above 99.99%. For every owned journey and high-risk surface, walk all ten
and either produce a dispositioned candidate or record an exclusion with its evidence path:
correctness and testability, including tests that would fail against a plausible broken
implementation; failure behaviour, including timeouts, bounded retries, idempotency, partial
failure, degraded dependencies, and recovery objectives; security, including trust boundaries,
authentication and authorization, untrusted input, secrets, and tenant isolation; observability,
where every new failure mode is diagnosable in production without a code change; concurrency and
load, including pools, contention, N+1 access, cache semantics, backpressure, and load shedding;
clean code, SOLID, and design patterns applied where they earn their place; algorithm and
data-structure choice with stated complexity budgets; configurability with safe defaults and
boundary validation, failing fast on a missing required setting; speed of development and
debuggability, naming the commands that test, run, and reproduce; and documentation of what
shipped, how it is operated, and how it fails.

Two standing preferences cut across all ten. Prefer official framework, platform, and standard
capabilities and wrap them rather than reimplementing them, because a wrapper survives an
upgrade and a reimplementation becomes the reason an upgrade is impossible. And prefer
uniformity across services over local optimality, recording any deliberate deviation with its
reason so the next agent inherits a decision rather than an accident.

MANDATORY LIVE RESEARCH
Research is mandatory for every obligation a matched archetype makes mandatory, and for every
claim whose current value is version-sensitive. Run it after the intent model and archetype
match are written, so each query names a surface and a failure mode rather than a topic.

Prefer, in order: current standards, specifications, and regulator or security-body guidance;
official framework, database, browser, platform, protocol, and vendor documentation for the
pinned version; maintained upstream repositories, reference implementations, and primary
research; then reputable engineering articles only where no primary source answers the question.
Record source URL, verification date, applicability, and limitation for every value used.

Where live verification is unavailable, write the rule with the metric named and carry the value
as a non-blocking factual TODO. State the obligation and defer only the number: a named metric
with a pending value governs behaviour, while a dropped rule governs nothing. Never present an
unverified value as current, and never copy a volatile value from memory - no metric threshold,
category score, framework version, browser support level, security-standard version, retention
period, price, or token limit.

INTENT AND RISK DISCOVERY
- Write an internal intent statement covering users and consumers, the owned outcome, critical
  user and system journeys, runtime and data surfaces, trust boundaries, and load-bearing
  qualities. Owner-supplied material such as an RFP or specification is intent evidence and
  outranks inference about goals; it does not establish repository facts.
- Existing CONSTITUTION.md preserves only context that survived refinement. Never claim to
  recover a prior chat message or discarded rationale; ask only where missing provenance changes
  the policy outcome.
- Use relevant counterfactuals - peak load, concurrent writes, duplicate delivery, dependency
  outage, restart, stale cache, network interruption, partial rollout, expired identity, storage
  pressure, rollback - to turn each obligation into a rule an agent can satisfy or violate on a
  named surface. Counterfactuals establish which obligations apply; they never establish what
  the repository currently does.
- A practice becomes constitutional law by one of two routes and no other: a matched archetype
  or the quality bar makes it mandatory, or repository evidence, still-valid prior governance,
  or an explicit owner decision requires it. A practice with neither route is reported outside
  CONSTITUTION.md rather than promoted because it is widely recommended.
- Disposition every candidate as exactly one of REQUIRED_BY_ARCHETYPE, REQUIRED_BY_EVIDENCE,
  OWNER_DECISION_REQUIRED, DELEGATE_TO_CANONICAL_SOURCE, NON_CONSTITUTIONAL_FOLLOW_UP,
  NOT_APPLICABLE, or UNKNOWN. NOT_APPLICABLE requires an evidence path; absence of an
  implementation is never that evidence.
- Keep the result free of generic best-practice catalogs. Every retained rule names an
  observable condition on a named surface.

INTERACTIVE OWNER DECISIONS
- Inspect evidence and complete archetype, intent, and risk discovery before asking anything.
- Ask only a decision that materially changes project promises, authority, security or privacy
  posture, data lifecycle, compatibility, cost, validation, exceptions, status, or ratification
  and cannot be resolved from current evidence, a matched archetype, or still-valid prior
  governance.
- Never ask whether a matched archetype's obligation applies. Ask which option satisfies it when
  credible alternatives change a durable promise, and write the obligation without asking.
- Ask at most three questions per batch. Normally stop after two batches; where essential gaps
  remain, record structured blocking TODOs and leave a DRAFT instead of extending the interview.
- Use two or three mutually exclusive options. Put one evidence-backed recommendation first,
  explain its project-specific reason and trade-off, and include a Decide later option.
- Where evidence cannot support a recommendation, recommend Decide later honestly.
- Pause for the owner's answer; never select an option on the owner's behalf. A deferred or
  unanswered decision leaves a new or non-binding result DRAFT and unbound. For an existing
  BINDING baseline, preserve the canonical file, version, status, and adapters unchanged and
  report the proposed delta outside it unless the owner explicitly chose replacement.

FINAL DOCUMENT IS LAW, NOT AUTHORING TELEMETRY
The final CONSTITUTION.md contains only durable rules that materially guide project decisions.
It never contains:
- a Constitution Metadata table;
- a Sync Impact Report or hidden generation report;
- evidence ledgers, confidence tables, claim labels, module classifications, or inventories;
- validation transcripts, command matrices, or pass/fail reports;
- AGENTS.md/CLAUDE.md binding instructions, import syntax, adapter status, or context budgets;
- owner-decision state, finalization outcome, template path, generation mode, or prompt data;
- amendment history ceremony, finalization narrative, or tutorial-style step lists.

Keep binding mechanics in AGENTS.md and CLAUDE.md, and keep generation and validation details in
the agent's final response. A constitution may reference canonical files by path, but it never
describes how an agent loads those files.

FINAL CONSTITUTIONAL COMPRESSION PASS
After the evidence-backed rewrite:
1. Reopen and reread the entire CONSTITUTION.md as if it will be injected into every coding task
   forever.
2. Delete any sentence that does not change a project decision, prevent a concrete failure, name
   a durable authority boundary, or define amendment or exception control.
3. Merge repeated rules and remove explanatory history, examples, workflow narration, and facts
   already owned by a canonical source.
4. Prefer one strong sentence over a table where the table adds no decision value.
5. Verify that no prescribed obligation is phrased as an observation of current behaviour.
6. Verify the document reads as a constitution, not a policy-generation artifact.

Compression removes words, never obligations. A prescribed obligation compresses to one sentence
naming its observable condition and its canonical owner; it is never deleted for brevity.

AUTHORITY AND STATUS
- Higher-precedence instructions remain controlling.
- Canonical ownership, current authority, approval, and ratification are distinct facts.
- CREATE or UPDATE permission is not ratification unless the launcher or the owner explicitly
  says so.
- BINDING requires complete essential decisions and ratification evidence in the working record;
  the final document records status only in the footer.
- DRAFT and NEEDS_REVIEW remain non-binding and are never newly imported or activated.
- SUPERSEDED is inactive and points runtime bindings to its successor.

UNKNOWN AND PROPOSAL RULES
- Missing evidence is not proof of absence.
- Record each unresolved item on a single physical line, in exactly this shape:
  TODO(<stable-id>): <decision>; reason: <gap>; owner: <role or UNKNOWN>; blocking: yes|no.
- A deferred owner decision is blocking: yes. An unverified number or unknown current state
  behind an obligation that is otherwise written is blocking: no - it records a factual gap and
  does not prevent ratification, because the rule already governs.
- Unapproved policy uses one physical line:
  PROPOSAL(<stable-id>): <candidate rule>; evidence/rationale: <why>; approval required from:
  <role or UNKNOWN>.
- A BINDING constitution contains no blocking TODO.

CONSTITUTION SHAPE
- Prefer THIN_CHARTER where mature canonical sources own technical and operational detail.
- Use FULL_CHARTER only where the repository lacks an adequate constitutional corpus.
- A thin charter still carries every matched archetype's obligations, as one sentence each naming
  the observable condition and the canonical source that owns the detail. Thinness comes from
  delegating detail, never from dropping an obligation.
- Conditional modules shape the principles; they never become a module inventory in the final
  document.
- A thin charter normally remains below 12 KiB and 160 physical lines. Smaller is better while
  authority and safeguards remain complete.

MODULE DETECTION CHECKLIST
Retention follows the matched archetypes, not the presence of existing code. Mark INCLUDE where a
matched archetype makes the module's subject mandatory, or repository evidence shows the project
owns that behaviour, or the owner placed it in scope. Mark EXCLUDE only on positive evidence that
the subject is outside owned scope with no matched archetype requiring it. Mark UNKNOWN where
inspection cannot establish ownership, and retain a reasoned TODO rather than deleting silently or
inventing a rule. An archetype-mandated but unimplemented subject is INCLUDE.
- MONOREPO_PACKAGES_SDK_CLI
- UPSTREAM_KIT_FRAMEWORK_CONTRACTS
- API_CONTRACTS
- GO_CHI
- LARAVEL_PHP_OCTANE
- FRONTEND_WEB_SSR_PWA
- GATEWAY_PROXY_TRUST
- DATA_MIGRATIONS
- REDIS_CACHE_LOCKS
- ASYNC_JOBS_EVENTS
- REALTIME_STREAMING
- INTEGRATIONS_WEBHOOKS
- MEDIA_FILES
- SEARCH_INDEXING
- INFRA_CI_RUNTIME
- OBSERVABILITY_SOC
- DOCS_GENERATED_AGENT_GUIDANCE

UPSTREAM KIT AND FRAMEWORK CONSUMERS
Never copy an upstream editable contract into a consumer and rewrite it locally; that creates an
unversioned fork. Record the upstream owner and contract location, the exact version pin from the
manifest or lockfile, the inherited versus consumer-owned boundary, the conformance tests, the
upgrade and change-request workflow, and how agents reach the upstream contract when its
repository is unavailable. A local generated snapshot is permitted only where the upstream owns
that delivery model, and it stays reproducible, read-only, stamped with upstream identity and
version, and drift-checked against the pin. Where the kit already satisfies an archetype
obligation, name the obligation and cite the kit contract as its owner; where the kit is silent,
the consumer owns that rule locally. Inheritance narrows what the consumer writes, never what the
service owes.

CROSS-CUTTING COVERAGE GATE
Before writing, verify that every matched archetype's mandatory obligations have a disposition and
every NOT_APPLICABLE carries an evidence path; that each owned journey and high-risk surface was
walked against all ten quality-bar obligations; that every prescribed obligation carrying a number
has a fetched value with source and date or a non-blocking factual TODO in its place; that no
prescribed obligation is phrased as an observation; that external sources did not overwrite
repository truth or prior ratified governance; and that content for stacks and domains the project
does not own was removed. These working classifications never appear as a checklist, matrix, or
research report in CONSTITUTION.md.

MINIMUM FINAL STRUCTURE
- One H1: the project constitution title.
- A short purpose and effect paragraph.
- Authority and Scope.
- Core Principles, consolidated around the project's actual archetypes and risks.
- Canonical Sources, as a compact closed delegation list where needed.
- Change Governance.
- Amendments and Exceptions.
- Unresolved Decisions only where a DRAFT or NEEDS_REVIEW has blocking decisions.
- Exactly one footer line for version, status, and dates.

No other section is mandatory merely because the authoring workflow used it.
END TEMPLATE-ONLY GENERATION CONTRACT
-->

# {{PROJECT_NAME}} Constitution

{{PURPOSE_AND_BINDING_EFFECT}}

## Authority and Scope

{{GOVERNED_SCOPE_AUTHORITY_PRECEDENCE_AND_CONFLICT_RULE}}

## Core Principles

### {{PRINCIPLE_NUMBER_AND_NAME}}

{{PROJECT_SPECIFIC_DURABLE_RULES_WITH_OBSERVABLE_CONDITIONS}}

### {{ARCHETYPE_OBLIGATION_PRINCIPLE_NUMBER_AND_NAME}}

{{ARCHETYPE_PRESCRIBED_OBLIGATIONS_WITH_METRIC_BUDGET_AND_VERIFIED_SOURCE}}

## Canonical Sources

- `{{SOURCE_PATH_OR_VERSIONED_REFERENCE}}` owns {{CANONICAL_TOPIC}}.

{{SOURCE_PRECEDENCE_AND_DRIFT_RULE}}

## Change Governance

{{RISK_COMPATIBILITY_CONSUMER_IMPACT_AND_COMPLETION_RULES}}

## Amendments and Exceptions

{{VERSIONING_AMENDMENT_EXCEPTION_AND_REVIEW_RULES}}

{{UNRESOLVED_DECISIONS_SECTION_OR_OMIT}}

**Version**: {{SEMVER}} | **Status**: {{STATUS}} | **Ratified**: {{DATE_OR_NOT_RATIFIED}} | **Last Amended**: {{DATE}} | **Last Evidence Review**: {{DATE}}
