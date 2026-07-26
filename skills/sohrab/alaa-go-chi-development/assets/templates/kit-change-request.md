# Kit Change Request: <one-line title>

<!--
Filename: YYYY-MM-DD-<kebab-slug>.md, using the real authoring date read from the environment, never invented.
One independently decidable topic per file. Fully self-contained: the reader has none of your session context.
Location: references/20-change-request-workflow.md §Location — it depends on the capability cell, not on habit.
Preserve this request forever; decisions are appended and never replace it.
Fill `kit_phase` and `phase_record` from the session-start read (references/05-phase-and-source-truth.md); copy
what the read returned rather than typing a phase name from memory.
-->

```yaml
type: kit-change-request
date: YYYY-MM-DD
requesting_service: <service | platform-audit | kit-owner>
requesting_repo: <path/URL | kit repo>
kit_version_observed: <immutable version/commit from go.mod>
kit_surface: <package + symbol/contract, e.g. httpkit.Bind, outboxkit relay, PG_SCALE_TIER bands>
kind: bug | limitation | extension | breaking-contracttest-after-minor
severity: blocking | high | normal   # blocking = a committed feature cannot ship, incl. a kit minor breaking contracttest
workaround_in_place: none | KIT-WRAP at <file:line, marker date>
status: filed        # filed → under-review → accepted|accepted-amended|rejected|deferred → implemented → shipped
status_updated: YYYY-MM-DD
kit_phase: <phase name exactly as the read returned it>
phase_record: <docs/change-requests/... path the read named>
related: [<other request files, or none>]
```

## 1. Outcome needed

<One precise paragraph: the behaviour you need, not an internal kit patch. E.g. "Bind must optionally expose the
raw body for webhook signature verification while keeping the size cap.">

## 2. Current kit behaviour and reproduction, verified

<What the kit does today at kit_version_observed. Every statement cites a kit file:line or symbol, a test name, or
a command you ran with its output. For a bug: minimal reproduction — input, expected, actual. Mark anything
unverified NEEDS_CONFIRMATION; never guess.>

## 3. Why the requester needs this, grounded

<Cite the architecture-doc section and/or the code path that hits the limitation. If blocking, name the committed
feature that is blocked. Historical consumer context explains an origin; it creates no execution scope.>

## 4. Proposed public contract, not a patch

<The shape you need: signature / behaviour / env key + default / DDL / error code / metric. Precise enough to be
contracttest-able. State explicitly what must stay backward compatible.>

## 5. Risk and operations

<Security and privacy; transaction, idempotency and data consistency; concurrency and resources; observability
and cardinality; migration and rollback; failure behaviour; testability. State n/a explicitly where true.>

## 6. Impact

<Writing anything here is the `consumer-impact-claim` capability — check its cell first. When the cell forbids it,
every registered consumer takes exactly the marker string the active scope record prescribes, with no repository
inspection. When it permits it, give one line per registered consumer from docs/CONSUMERS.md: none |
likely-affected + why | NEEDS_CONFIRMATION. Never claim "breaks nobody" without a basis you can name.>

## 7. Alternatives considered

<Including "do nothing" and "keep the wrap". Why they lose.>

<!-- Kit owner appends "## Kit decision — YYYY-MM-DD" (verdict, classification, consumer_impact, reasoning,
validation_evidence, implementation_status, shipped_in) per references/30-kit-owner-workflow.md. -->
