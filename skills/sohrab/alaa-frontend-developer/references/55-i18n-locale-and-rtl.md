# Locale-Deterministic Rendering

`20-vue-js-ssr-patterns.md` prohibits implicit locale and timezone formatting in SSR-rendered output.
This file is the positive replacement: what to do instead.

**Scope.** Only the determinism half is here. RTL layout, logical properties, icon mirroring, directional
motion, LTR islands inside RTL text, Persian typography and digit rendering all belong to
`/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/05-rtl-and-persian.md`. Folding
non-ASCII digits at an input boundary is `/alaa-input-normalization` (`$alaa-input-normalization`) and
`22-input-validation-and-normalization.md`.

## Why this is a correctness rule, not a polish rule

The server formats with the server's locale and the server's timezone. The browser formats with the
user's. When the same value is formatted on both sides, the two strings differ, hydration reports a
mismatch, and the fix applied under time pressure is usually to move the value client-only — which moves
it out of the server HTML and costs LCP. The defect looks like a formatting bug, hydrates like a
determinism bug, and lands as a performance regression.

## The rule

**Every formatting call states its locale and its timezone explicitly.** Neither is ever read from the
ambient environment on a render path.

```ts
// wrong on an SSR path: both locale and timezone are ambient
value.toLocaleDateString()
new Intl.NumberFormat().format(value)

// right: explicit, and identical on both sides of hydration
new Intl.DateTimeFormat(locale, { timeZone, dateStyle: 'medium' }).format(value)
new Intl.NumberFormat(locale, { maximumFractionDigits: 2 }).format(value)
```

- `locale` and `timeZone` are resolved **once per request**, on the server, from the request context, and
  passed into the render — not read per component and not read from `Intl.DateTimeFormat().resolvedOptions()`
  during a render.
- They are request-scoped values. Do not cache a formatter in a module-level singleton keyed by nothing;
  that is per-request state in a module scope, prohibited by `10-contract-and-boundaries.md`.
- Where a repo has one canonical locale, it is still stated explicitly at the call site. An implicit
  default that happens to be correct today becomes a defect the first time the app runs anywhere else.

## Timestamps on the wire

Send and receive an absolute instant with an offset or in UTC. Do not send a pre-formatted local string
and do not send a naive local datetime — the receiver cannot recover the instant, and the round trip
silently shifts the value. Format at the edge of rendering, never in the store and never in the API layer.
The wire representation itself is `/alaa-services-contract` (`$alaa-services-contract`)
`references/10-core-service-contract.md`.

## Relative time

"3 minutes ago" computed during an SSR render is stale before it paints and differs from the client's
recomputation, which is a guaranteed hydration mismatch. Render the absolute formatted instant on the
server, and upgrade it to a relative string after mount.

## Calendars and sorting

- A calendar system is part of the locale, not an afterthought: a Gregorian date and a Jalali date for the
  same instant are different strings, and picking the calendar at the render site rather than from the
  resolved locale produces two different answers in one page.
- Sorting user-visible strings uses `Intl.Collator` with the stated locale, not a code-unit comparison.
  The order a code-unit sort produces is wrong in every language with accents or non-Latin script, and
  it is silently wrong.

## Message catalogues

A translated string is data, not markup: a catalogue value is rendered as text. If a message needs
emphasis or a link, it is composed from parts in the template, never interpolated as HTML —
`25-frontend-security.md`.

## Verification

Render the affected route twice with two different `TZ` values and two locales and compare the server
HTML; run the hydration assertion from `05-proof-and-tests.md`. A formatting test that runs only in the
developer's timezone proves nothing.
