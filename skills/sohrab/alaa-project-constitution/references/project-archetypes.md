# Project Archetypes

Read this reference on every CREATE and UPDATE, before module classification. Repository
inventory establishes what the project *is*; this layer establishes what a project of that
kind *owes*.

**The load-bearing rule of this file:** an obligation listed under a matched archetype is
mandatory whether or not the current code implements it. A missing implementation is a gap
for the constitution to govern, never evidence that the obligation does not apply. A project
with no service worker still owes a stated service-worker or no-service-worker decision; a
project with no performance budget still owes a budget.

## How to read this file

1. Match archetypes from the signal table. A repository matches as many archetypes as its
   signals support — a browser client that ships its own API and consumes a queue matches
   three, and each contributes its full obligation set.
2. Read only the sections for matched archetypes. Skipping an unmatched section is correct;
   skipping a matched one is a defect in the authoring run.
3. Carry every mandatory obligation of every matched archetype into the candidate list as
   `INFERRED_CANDIDATE`, with this file and the matching signal as its provenance.
4. Use the archetype's counterfactuals to turn each obligation into a rule an agent can
   satisfy or violate on a named surface. An obligation written as an abstract noun has not
   been carried across.
5. Drop an obligation only on positive evidence that the surface is outside owned scope,
   recorded with the evidence path. "The code does not do this yet" is not that evidence.
6. Fetch every number. The `Verify live` line in each section names what must come from a
   primary source at authoring time. Record each value with its source URL and verification
   date. This file states which metric and that a budget is required; it never states a value.

The ten cross-cutting obligations that apply to every archetype live in `quality-bar.md` and
are not restated here. Where an archetype names a concrete rule below, that rule is the
specific form of one of those ten.

## Signal table

| Archetype | Signals that identify it |
|---|---|
| Browser web client | `package.json` with a browser framework or bundler; `index.html`; router config; component directories; SSR/SSG framework config; `manifest.webmanifest`; a service-worker file or worker plugin; browser test config |
| Public HTTP API service | Route registration reachable from outside the cluster; an API description document; a published SDK or client package; auth middleware for third-party callers; rate-limit configuration; a versioned path prefix or version header |
| Internal service-to-service API | Service-discovery or mesh configuration; mTLS material; cluster-local hostnames in config; protobuf/gRPC or internal RPC definitions; shared DTO packages; routes bound to internal interfaces only |
| Asynchronous worker / queue consumer | Broker configuration; queue, topic, or exchange declarations; consumer or job classes; dead-letter tooling; outbox or inbox tables; prefetch, concurrency, or heartbeat settings |
| Scheduled job | Crontab entries; a Kubernetes `CronJob`; framework scheduler registrations; interval annotations; a scheduler service in compose or chart values |
| Admin or back-office panel | Routes behind an elevated role; staff-only guards; CRUD scaffolding over production entities; bulk-action or export endpoints; impersonation features |
| Mobile BFF | Endpoints shaped for one client; per-call aggregation of several upstreams; client-version headers or minimum-version gates; push-notification registration; per-platform payload shapes |
| Real-time / streaming | WebSocket or SSE servers and clients; heartbeat and reconnect logic; presence tracking; pub/sub fan-out; media streaming or licence endpoints; sticky-session configuration |
| Data or reporting pipeline | ETL/ELT job definitions; warehouse or analytics schemas; materialised views or projection builders; report generators; change-data-capture configuration; orchestrator DAG or model definitions |

A signal proves the archetype only when the repository owns the behaviour. A dependency name,
a commented-out block, an example directory, or an environment variable that nothing reads
does not establish ownership — record `UNKNOWN` and ask, rather than matching or dismissing.

## Browser web client (SPA, SSR, SSG, PWA)

### Mandatory obligations

1. **Core Web Vitals budget.** The constitution names a budget for Largest Contentful Paint,
   Interaction to Next Paint, and Cumulative Layout Shift. Each budget states its percentile,
   its device and network class, and the named routes it governs. A budget with no percentile
   or no named route is not a budget: a median measured on a developer laptop passes while the
   field fails.
2. **Field and lab measurement, both named.** State which tool produces the lab number and
   which produces the field number, and which of the two the budget is enforced against. A
   lab-only budget cannot detect a regression that appears only on real devices and networks.
3. **Lighthouse category budgets.** State a minimum score for each Lighthouse category the
   project owns — Performance, Accessibility, Best Practices, and SEO — the exact command or
   CI job that produces them, and whether a score below budget fails the build or files a
   ticket. Fetch the current category list and scoring method at authoring time; Lighthouse
   reweights categories between major versions, so a score carried from memory governs the
   wrong thing.
4. **SEO obligations matched to the rendering strategy actually in use.** The strategies differ
   and a rule written for the wrong one is inert.
   - *Server-rendered:* every indexable route returns its primary content, title, meta
     description, and canonical link in the initial HTML response at a stated status code. A
     soft 404 that returns 200 with an empty shell is a defect, and the constitution names the
     correct status for a missing resource.
   - *Prerendered or static:* state which routes are prerendered, what a request for a route
     absent from the build manifest receives, and how a content change reaches the index — the
     rebuild trigger and the maximum staleness it permits.
   - *Client-rendered:* state what a crawler that executes no JavaScript receives for every
     indexable route, and which mechanism provides it — a prerender service, a server-rendered
     route, or an explicit decision that the route is not indexable. Indexable content must not
     depend on a user interaction such as a click, a scroll, or an accepted consent dialog.
   - *All strategies:* one canonical URL per indexable resource; a stated rule for trailing
     slashes, query-parameter variants, and locale variants; a named owner — file path or
     generator — for the robots policy and the sitemap; and a rule that non-production
     environments are not indexable, with the mechanism named rather than assumed.
5. **Metadata and structured data.** Every indexable route type has a named owner for its
   title, meta description, canonical link, social-preview fields, and `hreflang` where
   locales exist. State which structured-data types the project emits, in which serialisation,
   and which validator gates them in CI.
6. **Generative-engine visibility.** State the project's policy for AI and answer-engine
   crawlers by name in the robots policy — allowed, denied, or per-path — because leaving it
   unstated delegates the decision to a default the owner never made. State that facts a
   generative engine must be able to quote are present as text in the response body rather
   than only inside an image, a canvas, or a payload that arrives after hydration. Whether to
   permit these crawlers is an owner decision; having no position is not an option.
7. **Service worker lifecycle and update strategy.** If a service worker is in scope, state its
   registration scope; which routes and asset classes it may serve from cache and which it must
   always fetch from the network; the versioning scheme for its caches; what happens to caches
   from a previous version on activation; and how a user running an old worker receives a new
   release — the update trigger, whether it applies on the next navigation or immediately, and
   how in-flight work is protected when it applies immediately. State the removal path as well:
   shipping a build that drops the worker must not leave existing users pinned to a stale cache
   permanently. If a service worker is out of scope, state that as a decision with its reason,
   so the next agent does not add one silently.
8. **Failed responses are never cached.** A response is written to a client-side store — service
   worker cache, an HTTP cache directive the application controls, an in-memory query cache, or
   a persistent browser store — only when it is a success. Non-success statuses, network
   failures, timeouts, aborted requests, and partial or truncated bodies are never stored and
   never served to a later read as though they had succeeded. If the project wants negative
   caching, it is stated explicitly as a separate short-lived cache with its own key namespace
   and its own maximum age, so a dependency failing for ninety seconds during a deploy cannot
   become the value a user sees for the rest of the session.
9. **Offline and degraded-network behaviour.** For each critical journey, state what the user
   sees and can do when the network is absent, when it is present but slow, and when it fails
   mid-request. Name which journeys must complete offline, which must show a stated degraded
   state, and which may block. State the client retry policy — bounded attempts, backoff, and
   which methods are safe to retry — with the rule that a non-idempotent write is never
   retried without an idempotency key.
10. **Cache invalidation strategy.** For every client-side cache, state its key, what
    invalidates it, its maximum age, and how a stale entry is detected. State how a deploy
    invalidates asset caches and data caches. For user-scoped data, the cache key includes the
    identity it belongs to, and sign-out clears every store holding that identity's data.
11. **Accessibility.** Name the conformance standard, its version, its target level, and the
    routes and components in scope. State the automated gate and its command, plus the checks
    automation cannot make: keyboard reachability for every interactive control, a visible
    focus indicator, an accessible name for every control, and a stated announcement for each
    asynchronous state change.

### Counterfactuals

- A user on a slow connection and a mid-range phone opens the highest-traffic route. Which
  number does the budget govern, and which tool observed it?
- A crawler that executes no JavaScript requests the highest-value route. What does it receive?
- A deploy ships while a user has the application open. Which worker serves the next
  navigation, and which caches survive it?
- The API returns 503 for ninety seconds during that deploy. What is in the caches afterwards,
  and what does the user see on the next read?
- The user goes offline mid-checkout and reconnects two minutes later. Which requests replay,
  and can any of them charge twice?
- A user signs out on a shared device. What remains readable in browser storage and in the
  service-worker caches?
- A screen-reader user submits a form that fails validation. What is announced, and when?

### Verify live

Current Core Web Vitals metric set and their current thresholds; current Lighthouse category
list, weighting, and scoring method; current version and level structure of the accessibility
standard; documented service-worker update and cache-storage semantics for the target
browsers; the robots directives currently honoured by the search and AI crawlers the owner
names.

## Public HTTP API service

### Mandatory obligations

1. **Versioning and compatibility.** State what counts as a breaking change, how a new version
   is introduced, the minimum support window for a released version, and how a consumer is
   notified. Name where the current version is declared.
2. **One error contract.** State a single error envelope shape, the status-code mapping for each
   error class, and the rule that an internal exception message, stack frame, or query text
   never reaches a client body.
3. **Authentication and authorization per route class.** State the classes, what proves identity
   for each, and the rule that a newly added route is denied until its class is declared.
4. **Bounded input at the boundary.** State the maximum request body size, the maximum page
   size, and the rejection response for each. Validation happens at the boundary, before the
   value reaches domain code.
5. **Rate limiting and admission control.** State the identity a limit is keyed on, the response
   when a limit is exceeded including its retry hint, and the behaviour under total overload —
   which requests are shed and in what order.
6. **Idempotency for unsafe methods.** State which endpoints accept an idempotency key, how long
   a key is honoured, and exactly what a replay returns.
7. **Timeouts and bounded retries for every outbound dependency,** with a total request deadline
   smaller than the deadline the caller is expected to apply.
8. **Correlation.** Every request carries a correlation identifier, propagates it to every
   dependency, and emits it in logs. Name the header and the canonical source that owns the
   telemetry field names.
9. **Bounded collections.** Every collection endpoint is paginated with a stated maximum page
   size. No endpoint returns an unbounded list.
10. **Deprecation and sunset.** State how an endpoint or version is marked deprecated, what
    signal consumers receive, and the minimum notice before removal.

### Counterfactuals

A dependency is down for five minutes; a client retries the same POST three times after a
timeout; a consumer is pinned to a version released a year ago; traffic rises tenfold in one
minute; a credential expires mid-session; a field is removed from a response shape; a caller
requests a page size of one million.

### Verify live

Current version of the API description format in use; current versions of the authentication
and token standards the project implements; the framework's documented default timeouts and
body limits, because an unstated default is still a rule.

## Internal service-to-service API

### Mandatory obligations

1. **Explicit trust boundary.** State which callers are trusted, what proves caller identity,
   and the rule that network reachability is never authorization.
2. **Schema evolution rule** for the wire format — additive-only or versioned — and the
   compatibility check that gates it in CI.
3. **Per-dependency timeout, retry, and circuit-breaking policy,** with a retry budget that
   cannot amplify a downstream failure into an outage.
4. **Deadline propagation.** An inbound deadline bounds every outbound call made to serve it.
5. **Bounded concurrency per caller,** and a stated response when the bound is reached.
6. **Partial-failure contract.** State which callers may proceed on a degraded response, what a
   degraded response contains, and which dependency failures make the whole response fail.
7. **One owner per contract,** named, with the change-request path a consumer follows.

### Counterfactuals

A caller retries three times while the callee is already saturated; a producer adds a field
before consumers deploy; a certificate expires; a process inside the network calls with no
credential; a timeout at the leaf cascades to the edge.

### Verify live

Current compatibility rules and default deadline behaviour for the pinned RPC and
serialisation framework versions.

## Asynchronous worker / queue consumer

### Mandatory obligations

1. **Stated delivery semantics.** Assume at-least-once unless the broker's documentation for the
   pinned version proves otherwise, and state the assumption.
2. **Idempotent handlers.** Every handler states its deduplication identity and the retention
   window over which duplicates are recognised.
3. **Bounded retries** with backoff and jitter, and a named terminal destination for an exhausted
   message. Silent discard is never the terminal destination.
4. **Poison-message rule.** A message that fails deterministically leaves the hot path within a
   stated attempt count and is recoverable from the dead-letter destination.
5. **Ordering.** State whether ordering is required per key, and either how it is preserved or
   that it is explicitly not guaranteed.
6. **Lease and visibility handling.** A handler that can outlive its lease either extends it or is
   redesigned; state which, and state the maximum handler duration.
7. **Backlog and lag.** Name the observable lag signal, its alert condition, and the drain plan
   for a backlog that exceeds it.
8. **Side-effect safety.** A handler with an external side effect states either the idempotency
   key that makes replay safe or the compensating action that undoes a partial run.
9. **Graceful shutdown.** In-flight messages are acknowledged or returned to the broker within a
   stated drain window, never dropped.

### Counterfactuals

The same message is delivered twice; the broker restarts mid-handler; the handler crashes after
an external call but before acknowledgement; a consumer deploys while a large backlog is
queued; the dead-letter destination fills; producer and consumer clocks disagree.

### Verify live

The broker's documented redelivery, acknowledgement, prefetch, and quorum semantics for the
version pinned in the manifest.

## Scheduled job

### Mandatory obligations

1. **Overlap rule.** A run that starts while the previous run is still active is either prevented
   by a named lock or explicitly safe to overlap. State which, per job.
2. **Missed-run rule.** State what happens when the scheduler was unavailable for a window — skip,
   run once on recovery, or backfill a stated range.
3. **Restart safety.** A run interrupted halfway is safe to repeat; state the checkpoint or the
   transactional boundary that makes it so.
4. **Bounded work per run.** State a maximum batch size and a maximum duration, and the behaviour
   when either is reached.
5. **Explicit calendar semantics.** State the timezone the schedule is expressed in and the
   behaviour across a daylight-saving transition for any job scheduled in local time.
6. **Run observability.** Every run emits a start, an end, an outcome, and a processed count, and
   a job that has not succeeded within a stated window raises an alert. A silent job is
   indistinguishable from a dead one.

### Counterfactuals

A daylight-saving transition duplicates or skips the scheduled hour; the scheduler is down for
six hours; a run takes longer than its own interval; two replicas both fire; a run succeeds
having processed zero records.

### Verify live

The scheduler's documented behaviour for missed runs, concurrent runs, and timezone handling at
the pinned version.

## Admin or back-office panel

### Mandatory obligations

1. **Authorization per action and per record,** defaulting to deny, with the rule that hiding a
   control in the interface is never authorization.
2. **Audit trail.** Every state-changing action records actor identity, action, target, the change
   itself, timestamp, and correlation identifier, in a store the actor cannot edit. State the
   retention period.
3. **Destructive-action protection.** Bulk and irreversible operations state a confirmation
   requirement, a maximum number of records per operation, and a recovery path.
4. **Impersonation, where present.** State its scope, its maximum duration, that both identities
   appear in the audit record, and the actions impersonation may never perform.
5. **Field-level read control and export discipline.** State which fields each role may read,
   which are masked, and that an export is itself an audited action with a stated destination
   and retention.
6. **Exposure.** State the panel's network exposure and authentication factors explicitly, rather
   than inheriting whatever the public surface uses.

### Counterfactuals

An admin credential is phished; a bulk delete runs against a filter that matched every record;
an export pulls a full customer table; an impersonated session performs a payment; a support
role reads a field it should not see.

### Verify live

Current requirements of the regulations and standards that apply in the project's jurisdiction
for audit retention, personal-data access, and export logging.

## Mobile BFF

### Mandatory obligations

1. **Client-version compatibility.** State the minimum supported application version, how the
   server behaves for an older client, the support window, and the rule that a released
   version's contract is not broken while it remains in support.
2. **Forced-update path.** State what a client below the minimum receives and which mechanism
   delivers it.
3. **Composition discipline.** State a maximum response size and the rule that the BFF composes
   upstream data rather than proxying it, so one screen does not require N client round trips.
4. **Partial upstream failure.** State which sections of a composed response may be absent, how
   absence is represented in the payload, and which upstream failures fail the whole response.
5. **Offline and resumption.** State what the client may cache and for how long, and the rule that
   a token-refresh failure does not destroy unsent user work.
6. **Push and background delivery, where present.** Assume at-least-once, state the deduplication
   key, and state that a notification is never the only delivery path for a state change.
7. **Payload variants per device class,** stated explicitly for images and large responses,
   because bandwidth and battery are product constraints on this archetype.

### Counterfactuals

A third of installs are two versions behind; one of five upstreams is down; the device is on an
unstable mobile connection; a refresh token is revoked mid-session; a push arrives twice; a
screen depends on a service that has just been deprecated.

### Verify live

Current platform requirements for background execution, push delivery, and payload limits on the
target OS versions.

## Real-time / streaming

### Mandatory obligations

1. **Connection lifecycle.** Authenticate at connect and re-authenticate on credential expiry,
   with the rule that a long-lived connection never outlives the authorization that opened it.
2. **Reconnect and resume.** Bounded reconnection with backoff and jitter, a stated resume cursor
   or token, and a stated rule for what the client missed while disconnected — replay from
   cursor, snapshot then delta, or an explicit gap notification.
3. **Heartbeat and dead-peer detection** with stated intervals on both ends.
4. **Fan-out bounds.** State maximum concurrent connections per node and per identity, maximum
   message rate per connection, and the shed behaviour when either is exceeded.
5. **Backpressure.** State what happens when a consumer is slower than the stream — a bounded
   buffer, a drop policy with stated priority, or disconnection.
6. **Per-channel delivery and ordering guarantee,** stated rather than implied.
7. **Node loss and routing.** State what a client experiences when its node dies and where session
   state lives.

### Counterfactuals

Ten thousand clients reconnect simultaneously after a node restart; a token expires during a
two-hour session; a slow mobile consumer cannot keep up; a message is delivered twice; an
intermediate proxy closes an idle connection; playback continues past licence expiry.

### Verify live

Documented idle-timeout and buffering behaviour of every proxy and load balancer in the path;
current licence or DRM requirements where protected media is served.

## Data or reporting pipeline

### Mandatory obligations

1. **Lineage and authority.** For every derived dataset, name the upstream sources and the
   transformation owner, and state that a report never becomes the authority for a fact the
   operational store owns.
2. **Reproducibility.** A run is deterministic given its inputs and a stated watermark. State the
   watermark and the late-arrival window.
3. **Idempotent reload.** A partition or window can be recomputed without duplicating rows. State
   the key and the write strategy that guarantee it.
4. **Freshness contract per dataset.** State the maximum acceptable lag, the signal that measures
   it, and the alert condition.
5. **Correctness assertions in the pipeline** — row counts, referential integrity, and value
   ranges — with the rule that a failed assertion stops publication rather than publishing a
   partial dataset.
6. **Backfill procedure** with a stated blast-radius bound and a stated way consumers are told
   that historical numbers changed.
7. **Retention, deletion, and personal data.** Name which datasets carry personal data, their
   retention period, and how a deletion in the operational store propagates to every derived copy.
8. **Cost bound.** State a bound on scanned data or compute for the largest job, and what happens
   when it is exceeded.

### Counterfactuals

A source row arrives three days late; an upstream schema gains a column; a run is triggered
twice; a deletion request must reach every derived copy; the largest job's cost doubles after a
traffic spike; a published report and the operational store disagree.

### Verify live

Documented transactional-write, late-arrival, and time-travel semantics for the warehouse and
orchestrator versions in use.

## When archetypes interact

Several matched archetypes can produce obligations that touch the same surface. Resolve the
overlap explicitly rather than writing both rules and letting a later agent choose.

- A browser client plus its own public API: the client's offline rule and the API's idempotency
  rule are one decision. State the idempotency key the client sends on replay, in one place, and
  reference it from the other.
- A worker plus a data pipeline: the worker's deduplication identity and the pipeline's reload key
  must agree, or a replay produces double-counted rows.
- An admin panel plus any archetype that stores personal data: the panel's field-level read
  control and the data retention rule are governed together, because an export can outlive the
  retention period it was exported from.
- A real-time surface plus a mobile BFF: the connection's re-authentication rule and the client's
  token-refresh rule are one contract; a mismatch drops sessions silently on credential rotation.

Record each resolved overlap once, in the principle that owns the surface, and cite it from the
other rather than restating it.
