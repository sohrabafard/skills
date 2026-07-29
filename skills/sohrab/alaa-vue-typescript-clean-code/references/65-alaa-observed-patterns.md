# Alaa observed patterns and antipatterns (project-proven, mandatory)

This file exists because these exact failures shipped in the Alaa clean-island codebase and each one had to
be found and repaired by hand, page by page. Every pattern here is mandatory where its trigger applies, and
every antipattern is a blocking review finding. Read it whenever you write or review a view mapper, a flow
composable, a store, an SDK adapter, or a design-system component in a repo with these surfaces.

Format: **Trigger, Do, Don't, Why it shipped broken.**

---

## 1) PRVM — the provenance-resolved view model

**Trigger:** any mapper turning a domain model or DTO into props a component renders, in a codebase with a
declared data-source policy (sources such as `api / derived / api-untyped / mock`).

A backend repository centralizes "where data comes from" so callers cannot get it wrong. The frontend
equivalent: one framework-free resolver owns the field-value priority chain, and every view mapper builds
every designed field through it. In Alaa this is `src/new/model/_resolve.ts`.

```ts
// DO — the chain is declarative, and the mock terminal is REQUIRED by the type:
durationLabel: resolveFieldValue({ mock: DURATION_PLACEHOLDER }),           // no backend field yet
rating: resolveFieldValue({
  api: ratingAverage === null ? undefined : { score: ratingAverage, count },
  mock: RATING_PLACEHOLDER,
}),
// A design-omitted variant (no progress bar on non-enrolled cards) is the ONLY
// sanctioned way to render nothing, and it is expressed by passing no placeholder:
progress: resolveOptionalFieldValue({
  apiUntyped: model.progressPercent,
  ...(model.enrolled ? { mock: PROGRESS_PLACEHOLDER } : {}),
}),
```

```ts
// DON'T — "honest omission": hand-rolled conditional spreads that blank the designed UI
// whenever the upstream value happens to be missing:
...(ratingAverage !== null ? { rating: { ... } } : {}),   // ANTIPATTERN
summaryItems: [],                                          // ANTIPATTERN (designed chips blanked)
// durationLabel intentionally omitted: no backend field    // ANTIPATTERN comment
```

**Why it shipped broken:** the rule said "declare every field" but the value fallback was left to each
mapper. Three pages independently re-invented omission under the banner "never fabricate", and live rows
degraded the designed layout. Honesty belongs in the source manifest and the development-mode provenance
marker, never in a hole in the UI.

If the repo has no resolver yet, create one: framework-free, unit-tested, `0` and `false` are real values,
and `null`, `undefined`, blank string, `NaN`, and empty array fall through.

**Discipline pair:** when a task proves a field's true source differs from its manifest, flip the manifest
and the mapper in the same change, or record an explicit follow-up. Never leave a declared source lying.

## 2) No shadow adapters over a reactive SDK layer

**Trigger:** a Pinia store or flow composable calling `sdk.*` transport methods.

- **Do:** consume the SDK's Vue adapter composables — per-action pending and error state, abort, and scope
  disposal live there once. The store keeps durable session and collection state only; the flow owns
  journey policy; front the adapter with a narrow host-local seam interface that tests can inject.
- **Don't:** wrap `sdk.*` with your own `pending`/`error` refs, status enums (`requestingOtp`, …), retry
  loops, or error redaction inside a store or a flow. That is a second, divergent lifecycle implementation
  of something that already exists.
- **Why:** the first auth flow shipped exactly this and had to be re-layered wholesale.

Retry behaviour anywhere in this stack is `/alaa-reliability-sla` (`$alaa-reliability-sla`); where it may
live in Vue code is `70-async-and-failure-binding.md`.

## 3) God composable to orchestrator plus focused units

**Trigger:** a `useX` growing past the file budget, or returning filters and drafts and transport verbs and
sync at once.

- **Do:** split along the standard seams and behind the numeric budgets in `SKILL.md`, which owns both.
  Pin behaviour with the untouched page-level spec while you split.
- **Don't:** keep growing one file because the tests still pass, and do not split by arbitrary line count
  instead of by responsibility.
- **Why:** a 1200-line moderation flow shipped as one file. The split produced eight cohesive modules with
  zero behaviour change — which is the evidence that the responsibilities were always separate.

## 4) Entity cards navigate; intents carry the native event

**Trigger:** a presentational card or row rendering an entity whose id is available.

- **Do:** give the card a real `href` — semantics, middle-click, SEO — *and* emit the intent with the
  native `MouseEvent` (`select: [id, event]`), so the host can `preventDefault()` a plain left click and
  route client-side while modifier and middle clicks keep native behaviour. The pressable affordance
  (CSS-only, reduced-motion safe) belongs in the design-system component, not in each page.
- **Don't:** ship a dead card with navigation "to be wired later", emit an id-only event that forces a full
  page reload through a raw anchor, or hijack modifier clicks.
- **Why:** cards shipped without `href`s and with an action button that did nothing; linking had to be
  retrofitted with an additive emit-signature change.

## 5) Merge writes by presence detection, never truthiness

**Trigger:** merging a server DTO over existing local or optimistic state.

- **Do:** decide per field with raw presence checks (`dto.like_count !== undefined && dto.like_count !== null`),
  so a legitimate `0`, `false`, or empty value overwrites stale local data while an omitted field keeps the
  local value.
- **Don't:** `merged.likeCount = dto.likeCount || existing.likeCount`. A truthiness fallback silently
  discards legitimate zeros.
- **Why:** a live `like_count: 0` was being ignored in the moderation store sync until review caught it.

## 6) Failure classification before optimistic fallback

**Trigger:** live-first writes with a local optimistic fallback.

- **Do:** classify caught (redacted) failures in a pure, unit-tested policy module. A definitive backend
  denial surfaces a message and **skips** the local mutation; a transport failure keeps the optimistic
  local apply with honest wording. In bulk loops, denied ids stay selected and are reported separately.
- **Don't:** collapse every rejection into `catch { applyLocally() }`. A 403 must never look like success.
- **Why:** the collapsed form shipped, and a denied action appeared to the user as a completed one.

Which response codes are definitive versus transient is `/alaa-reliability-sla`
(`$alaa-reliability-sla`); that a denial is a security event rather than a transport event is
`/alaa-security-review` (`$alaa-security-review`). This file owns only the rule that the classification
happens **before** the fallback runs, in a module you can test without a network.

## 7) Host route policy stays in a tiny sync composable

**Trigger:** UI state that must mirror the URL — accordion deep links, tabs, wizards.

- **Do:** one small `useXRouteSync` composable. Deep link to state, applied immediately *and* re-applied
  after any state reset such as a mock-to-live swap; state to URL through `router.replace`, with no reload.
  Inject narrow `Pick<Route, 'params'>` and `Pick<Router, 'replace'>` surfaces so tests need no router.
- **Don't:** scatter `router.replace` calls through the page, and do not trust Vue Router's `:param?` to
  make a **static** path segment optional — `course/:courseId/set/:setId?` still requires the literal
  `set/`. Use a second route record pointing at the same lazy component; the same component object means no
  remount.

## 8) Design-system components: emits are contracts, additions are additive

**Trigger:** changing a published presentational component.

- **Do:** extend emit payloads additively, with extra trailing arguments. Keep props-in and events-out — no
  store, SDK, or router inside the package. Document the change in the package guide in the same commit.
- **Don't:** put host policy — navigation, fetching, permission checks — inside the component, and do not
  "fix" a reusable component's behaviour from a host page's SCSS.
- **Why:** a non-additive emit change broke consumers that were not rebuilt.

The `dist` consumption half of this — rebuilding the package before browser-checking a consumer, peer
dependencies, entry points — is `/alaa-mono-package` (`$alaa-mono-package`).

## 9) Post-teardown guards cover every exposed surface

**Trigger:** a composable exposing async controllers — actions *and* reads.

- **Do:** make every exposed `execute` and `refresh` fail closed after scope disposal, and every `reset` and
  `abort` a no-op. Test it: `scope.stop()`, then call.
- **Don't:** guard the actions and forget the read controller.
- **Why:** a retained `flags.refresh()` after unmount was still hitting the SDK.

`70-async-and-failure-binding.md` states this as a standing rule for every composable, not only the ones
that already broke.

## 10) Locked product law beats local cleverness

**Trigger:** any rule file the maintainer marked user-locked — a UX law, a source policy.

- **Do:** apply it verbatim. If you cannot, stop and report. Remove code that contradicts it, including its
  tests and manifest entries — for example a "first accordion starts expanded" flag when the law says all
  closed.
- **Don't:** reinterpret, soften, or extend a locked file without the maintainer's explicit instruction.
