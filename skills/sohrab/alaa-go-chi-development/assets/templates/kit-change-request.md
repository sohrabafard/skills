# Kit Change Request: <one-line title>

<!--
Filename: YYYY-MM-DD-<kebab-slug>.md  (authoring date, real date from the environment)
Location: <consumer-repo>/docs/kit-change-requests/
          (design-phase or audit-originated: <kit-repo>/docs/change-requests/ directly)
One file per feature/bug. Fully self-contained: the reader has none of your session context.
-->

```yaml
type: kit-change-request
date: YYYY-MM-DD
requesting_service: <news | notif | entitlement-api | tusd | ...>
requesting_repo: <repo path/URL>
kit_version_observed: <version from go.mod, or commit>
kit_surface: <package + symbol/contract, e.g. httpkit.Bind, outboxkit relay, PG_SCALE_TIER bands>
kind: bug | limitation | extension | breaking-contracttest-after-minor
severity: blocking | high | normal
workaround_in_place: none | KIT-WRAP at <file:line, marker date>
status: filed         # lifecycle: filed → under-review → accepted|accepted-amended|rejected|deferred → implemented
status_updated: YYYY-MM-DD HH:MM   # when status last changed (real date/time from the environment); every status change updates this
```

## 1. What we need (the ask, in one paragraph)

<The outcome, not the implementation. E.g. "Bind must optionally expose the raw body to the handler for
webhook signature verification while keeping the size cap.">

## 2. Current kit behavior (verified, with evidence)

<What the kit does today. Every statement cites kit file:line/symbol, a test name, or a command you ran and its
output. Mark anything unverified as NEEDS_CONFIRMATION — do not guess.>

## 3. Why the consumer needs this (grounded in our contract)

<Cite your architecture doc section and/or the code path that hits the limitation. If it's a bug: minimal
reproduction — input, expected, actual. If severity is blocking: which committed feature is blocked.>

## 4. Proposed contract (not a patch)

<The shape you need: signature / behavior / env key + default / DDL / error code / metric. Precise enough to be
contracttest-able. Explicitly note what must stay backward compatible.>

## 5. Blast radius, as far as we can see

<Per registered consumer (from docs/CONSUMERS.md): none | likely-affected + why | unknown. Never claim "breaks
nobody" without basis. Note idempotency / security / observability implications, or state n/a.>

## 6. Alternatives we considered

<Including "do nothing" and "keep the wrap". Why they lose.>

<!-- Kit owner appends "## Kit decision — YYYY-MM-DD" here after intake; see the skill's 30-kit-owner-workflow. -->
