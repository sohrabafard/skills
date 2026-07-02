# Alaa Observed Patterns and Antipatterns (project-proven, mandatory)

This reference exists because these exact failures shipped repeatedly in the Alaa clean-island codebase and each
one had to be found and fixed by hand, page by page. Every pattern here is MANDATORY where its trigger applies;
every antipattern is a blocking review finding. Load this file whenever you write or review view mappers, flow
composables, stores, SDK adapters, or design-system components in an Alaa-style repo.

Format: **Trigger → Do → Don't → Why it shipped broken before.**

---

## 1) PRVM — Provenance-Resolved View-Model (the "Repository of rendered values")

**Trigger:** any mapper that turns a domain model / DTO into props a component renders, in a codebase with a
declared data-source policy (e.g. sources `api / derived / api-untyped / mock`).

A backend Repository centralizes "where data comes from" so callers cannot get it wrong. The frontend equivalent:
one framework-free resolver owns the field-value priority chain, and every view mapper builds every designed field
through it. In Alaa this is `src/new/model/_resolve.ts`:

```ts
// DO — the chain is declarative, the mock terminal is REQUIRED by the type:
durationLabel: resolveFieldValue({ mock: DURATION_PLACEHOLDER }),           // no backend yet
rating: resolveFieldValue({
  api: ratingAverage === null ? undefined : { score: ratingAverage, count },
  mock: RATING_PLACEHOLDER,
}),
// Design-omitted variant (e.g. no progress bar on non-enrolled cards) is the
// ONLY sanctioned way to render nothing — expressed by passing no placeholder:
progress: resolveOptionalFieldValue({
  apiUntyped: model.progressPercent,
  ...(model.enrolled ? { mock: PROGRESS_PLACEHOLDER } : {}),
}),
```

```ts
// DON'T — "honest omission": hand-rolled conditional spreads that blank the
// designed UI whenever the upstream value is missing:
...(ratingAverage !== null ? { rating: { ... } } : {}),   // ANTIPATTERN
summaryItems: [],                                          // ANTIPATTERN (designed chips blanked)
// durationLabel intentionally omitted: no backend field    // ANTIPATTERN comment
```

**Why it shipped broken:** the rule said "declare every field" but the VALUE fallback was left to each mapper;
three pages independently re-invented omission ("never fabricate") and live rows degraded the designed layout.
Honesty belongs in the source manifest and the dev provenance marker — never in a hole in the UI. If the repo has
no resolver yet, create one (framework-free, unit-tested, `0`/`false` are real values; `null`/`undefined`/blank
string/`NaN`/empty array fall through).

**Discipline pair:** whenever a task proves a field's true source differs from its manifest, flip manifest+mapper
in the same change or record an explicit follow-up — never leave the declared source lying.

## 2) No shadow adapters over a reactive SDK layer

**Trigger:** a Pinia store or flow composable calling `sdk.*` transport methods.

- **Do:** consume the SDK's Vue adapter composables (per-action pending/error, abort, scope disposal, redaction
  live there once); the store keeps durable session/collection state only; the flow owns journey policy; front the
  adapter with a narrow host-local seam interface that tests can inject.
- **Don't:** wrap `sdk.*` with your own `pending`/`error` refs, status enums (`requestingOtp`, …), retry loops, or
  error redaction inside a store or flow. That is a second, divergent lifecycle implementation.
- **Why:** the first auth flow shipped exactly this and had to be re-layered wholesale.

## 3) God composable → orchestrator + focused units (numeric budgets)

**Trigger:** a `useX` growing past ~400 lines or returning filters AND drafts AND transport verbs AND sync.

- **Do:** split along the standard seams — pure policy/classification → standalone pure modules; view/filter/
  selection state → one `useX`; drafts/dialog state → one `useX`; transport verbs → one `useX` receiving the
  others' narrow surfaces; one thin orchestrator composes them and exposes the page's stable public surface
  (behavior pinned by the untouched page-level spec).
- **Don't:** keep growing one file "because the tests pass", or split by arbitrary line count instead of by
  responsibility.
- **Why:** a 1200-line moderation flow shipped as one file; the split produced 8 cohesive modules with zero
  behavior change.

## 4) Entity cards navigate; intents carry the native event

**Trigger:** a presentational card/row rendering an entity whose id is available.

- **Do:** give the card a real `href` (semantics, middle-click, SEO) AND emit the intent with the native
  `MouseEvent` (`select: [id, event]`) so the host can `preventDefault()` a plain left-click and route client-side
  while modifier/middle clicks keep native behavior. Add the pressable affordance (CSS-only transition, reduced-
  motion safe) in the design-system component, not per page.
- **Don't:** ship a dead card ("we'll wire navigation later"), emit id-only events that force full page reloads
  through raw anchors, or hijack modifier clicks.
- **Why:** cards shipped without hrefs and an action button that did nothing; linking had to be retrofitted with
  an additive emit-signature change.

## 5) Merge writes: presence-detection, never truthiness

**Trigger:** merging a server DTO over existing local/optimistic state.

- **Do:** decide per field with raw-presence checks (`dto.like_count !== undefined && !== null`) so a legitimate
  `0`/`false`/empty overwrites stale local data, while an omitted field keeps the local value.
- **Don't:** `merged.likeCount = dto.likeCount || existing.likeCount` — truthiness fallbacks silently discard
  legitimate zeros.
- **Why:** a live `like_count: 0` was being ignored in the moderation store sync until review caught it.

## 6) Failure classification before optimistic fallback

**Trigger:** live-first writes with a local optimistic fallback.

- **Do:** classify caught (redacted) failures with a pure, unit-tested policy module: definitive backend denials
  (non-transient 4xx, auth/validation codes, never `retryable`) surface a message and SKIP the local mutation;
  transport/5xx/timeout failures keep the optimistic local apply with honest wording. In bulk loops, denied ids
  stay selected and are reported separately.
- **Don't:** collapse every rejection into `catch { applyLocally() }` — a 403 must never look like success.

## 7) Host route policy stays in a tiny sync composable

**Trigger:** UI state that must mirror the URL (accordion deep links, tabs, wizards).

- **Do:** one small `useXRouteSync` composable: deep link → state (applied immediately AND re-applied after any
  state reset such as a mock→live swap), state → URL via `router.replace` (no reload); inject narrow
  `Pick<Route,'params'>`/`Pick<Router,'replace'>` surfaces so tests need no router.
- **Don't:** scatter `router.replace` calls through the page, or trust Vue Router's `:param?` to make a STATIC
  path segment optional — `course/:courseId/set/:setId?` still requires the literal `set/`; use a second route
  record on the same lazy component instead (same component object ⇒ no remount).

## 8) Design-system components: emits are contracts, additions are additive

**Trigger:** changing a published presentational component.

- **Do:** extend emit payloads additively (extra trailing args), keep props-in/events-out (no store/SDK/router in
  the package), document the change in the package guide in the SAME commit, and rebuild the package before
  browser-checking the consumer (hosts consume `dist`).
- **Don't:** put host policy (navigation, fetching, permission checks) inside the component, or "fix" a reusable
  component's behavior from a host page's SCSS.

## 9) Post-teardown guards cover EVERY exposed surface

**Trigger:** a composable exposing async controllers (actions AND reads).

- **Do:** make every exposed `execute`/`refresh` reject-fail-closed after scope disposal and every `reset`/`abort`
  a no-op; test it (`scope.stop()` then call).
- **Don't:** guard the actions and forget the read controller — a retained `flags.refresh()` after unmount was
  still hitting the SDK.

## 10) Locked product law beats local cleverness

**Trigger:** any rule file the maintainer marked as user-locked (UX law, source policy).

- **Do:** apply it verbatim; if you cannot, stop and report. Remove code that contradicts it (e.g. a
  "first accordion starts expanded" flag when the law says all closed) including its tests and manifest entries.
- **Don't:** reinterpret, soften, or extend a locked file without the maintainer's explicit instruction.
