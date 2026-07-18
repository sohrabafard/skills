# Kit Change Request: <one-line title>

<!--
Filename: YYYY-MM-DD-<kebab-slug>.md (real authoring date from the environment, never invented).
One independently decidable topic per file. Fully self-contained: the reader has none of your session context.
Location: active consumer work → <consumer-repo>/docs/kit-change-requests/;
          design-phase, audit-originated, or kit-first-phase → <kit-repo>/docs/change-requests/.
Preserve this request forever; decisions are appended, never replace it.
-->

```yaml
type: kit-change-request
date: YYYY-MM-DD
requesting_service: <service | platform-audit | kit-owner>
requesting_repo: <path/URL | kit repo>
kit_version_observed: <immutable version/commit from go.mod>
kit_surface: <package + symbol/contract, e.g. httpkit.Bind, outboxkit relay, PG_SCALE_TIER bands>
kind: bug | limitation | extension | breaking-contracttest-after-minor
severity: blocking | high | normal   # blocking = committed feature cannot ship (incl. kit minor broke contracttest)
workaround_in_place: none | KIT-WRAP at <file:line, marker date>
status: filed        # filed → under-review → accepted|accepted-amended|rejected|deferred → implemented → shipped
status_updated: YYYY-MM-DD
related: [<other request files, or none>]
```

## 1. Outcome needed

<One precise paragraph: the behavior you need, not an internal kit patch. E.g. "Bind must optionally expose the
raw body for webhook signature verification while keeping the size cap.">

## 2. Current kit behavior and reproduction (verified)

<What the kit does today at kit_version_observed. Every statement cites kit file:line/symbol, a test name, or a
command you ran with its output. Bug: minimal reproduction — input, expected, actual. Mark anything unverified
NEEDS_CONFIRMATION — never guess.>

## 3. Why the requester needs this (grounded)

<Cite the architecture doc section and/or code path that hits the limitation; if blocking, name the committed
feature that is blocked. Historical consumer context creates no execution scope during KIT_FIRST_STABILIZATION.>

## 4. Proposed public contract (not a patch)

<The shape you need: signature / behavior / env key + default / DDL / error code / metric. Precise enough to be
contracttest-able. State explicitly what must stay backward compatible.>

## 5. Risk and operations

<Security/privacy; transaction/idempotency and data consistency; concurrency/resources; observability/cardinality;
migration/rollback; failure behavior; testability. State n/a explicitly where true.>

## 6. Impact (phase-aware)

<During KIT_FIRST_STABILIZATION: every registry row = NOT_ASSESSED_KIT_FIRST, with no repo inspection.
After explicit reactivation: per registered consumer (from docs/CONSUMERS.md): none | likely-affected + why |
NEEDS_CONFIRMATION. Never claim "breaks nobody" without basis.>

## 7. Alternatives considered

<Including "do nothing" and "keep the wrap". Why they lose.>

<!-- Kit owner appends "## Kit decision — YYYY-MM-DD" (verdict, classification, consumer_impact, reasoning,
validation_evidence, implementation_status, shipped_in) per references/30-kit-owner-workflow.md. -->
