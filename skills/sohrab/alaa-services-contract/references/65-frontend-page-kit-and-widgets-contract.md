# Frontend Page Kit And Widgets Contract

Use this file when building or consuming Page Kit, UI Kit, app-shell, or any widget in the clean-island package
families: defining a new widget or page package, wiring a widget into a host, deciding what a widget may own, or
reviewing a change that touches `@alaa/page-*`, `@alaa/widgets-*`, `@alaa/forms`, `@alaa/crud`, `@alaa/model`,
`@alaa/sanitize-html`, or `@alaa/app-shell`.

This file owns the *consumption and boundary* contract for the widget/page layer. It is the visual-layer companion to
`60-frontend-sdk-consumption-contract.md` (which owns how the host talks to backend services). Read both when a widget
needs data: the widget never fetches it, the host fetches it through the SDK and passes it in.

It exists to keep widgets reusable and safe. A widget that reaches for the store, the SDK, the token, or a trusted
header stops being a widget and becomes a hidden piece of the host — untestable, unportable, and a trust-boundary risk.

## Package families (one mental model)

- **Page Kit** (`@alaa/page-*`, `@alaa/widgets-*`) — the page-builder and widget system: schema, renderer, and the
  widget catalog.
- **UI Kit** (`@alaa/forms`, `@alaa/crud`) — the clean-island form and CRUD building blocks.
- **app-shell** (`@alaa/app-shell`) — the per-layout application shell.
- **support** (`@alaa/model`, `@alaa/sanitize-html`, and similar) — focused single-responsibility packages that widgets
  depend on instead of duplicating heavy logic.

These are isolated package lanes. They are not wired into the production app until a maintainer explicitly approves that
migration phase (see "Island isolation" below).

## Abstraction-first / contract-first

- Define the public contract first — the props in, the events out, and the public types — then build the implementation
  behind it. The contract is the deliverable; the internals are replaceable.
- A package/widget exposes a stable, minimal public surface and hides its internals. Consumers depend only on the public
  `dist`/entry exports, never on internal `src/*`.
- Cross-cutting or dependency-heavy logic becomes a focused single-responsibility package (the "extract, don't
  duplicate" rule), not a grab-bag `utils`. Pair with `$alaa-mono-package`.

## The three-layer rule

Data flows in exactly one direction, through three layers:

- **presentation** (widget / component) → **flow composable** → **store** → **SDK**

Rules:

- Widgets are **props-in / events-out**. They receive data through props and report intent through events. They render;
  they do not fetch.
- Widgets own **no host singletons** — no store, no SDK instance, no auth token, no trusted-header generator, no router.
  The host owns data and wiring; the widget owns presentation.
- The flow composable orchestrates; the store holds state; the SDK talks to services (under
  `60-frontend-sdk-consumption-contract.md`). A widget never calls the SDK, APIGateway, or a service route directly.

## Widget contract

- Inputs are explicit, typed props with documented shapes; outputs are explicit, typed events. No implicit globals.
- A widget is deterministic for a given set of props (important for SSR — see below).
- A widget does not read or write browser storage, tokens, or cookies. If it needs identity-derived data, the host
  passes it in as a prop.
- Keep widgets small and focused; prefer composing several small widgets over one large component.

## Consumption boundary (package hygiene)

- Consume sibling packages through their public `dist`/entry exports and `link:../<package-name>` dependencies. Never
  import a sibling's `src/*`.
- Keep `vue` and `quasar` as peer dependencies; do not bundle a second copy.
- Preserve the asset contract: package CSS/assets must reach `dist/ssr/client/assets` through the bundling graph
  (import CSS from the package entry). Pair with `$alaa-mono-package` for boundary, dedupe, and asset rules.

## Island isolation and migration gating

- Do not wire these packages into legacy production `src/*`, `src-ssr/*`, `src-pwa/*`, Quasar boot, the router,
  Vuex/Pinia, the service worker, root scripts, or legacy packages unless the task explicitly approves that migration.
- Host consumption goes through the sanctioned clean-island host lane (`src/new/` behind a `/new/` prefix), feature by
  feature, with explicit per-phase approval. The lane is additive and reversible.

## Security in widgets

- A widget never sends trusted gateway headers and never holds a token — those concerns live in the host + SDK
  (`60-frontend-sdk-consumption-contract.md`). A widget that needs them is mis-scoped.
- Raw/untrusted HTML renders only through the sanctioned sanitizer (`@alaa/sanitize-html` / DOMPurify) at the trust
  boundary. A single bypass of that one raw-HTML path is stored XSS — never hand-roll a regex sanitizer. Pair with
  `$alaa-security-review` for any raw-HTML or dangerouslySet-style path.

## SSR safety

- No browser-only APIs (`window`, `document`, `localStorage`, observers) during SSR render; guard with `onMounted` or a
  `typeof window` check.
- Deterministic render: no `Date.now()`, `Math.random()`, or locale/time-dependent output in the SSR path (it causes
  hydration mismatches).
- Clean up observers, listeners, timers, and abort controllers in `onBeforeUnmount`.

## Documentation requirement

- Every public prop, emit, component, composable, and exported type carries doc comments (TSDoc for `.ts`, JSDoc
  otherwise) with typed params/returns. The public contract is the documented surface. Pair with
  `$alaa-frontend-doc-annotations`.

## Anti-patterns (do not do these)

- A widget that imports the store, the SDK, the router, or a token directly.
- A widget that fetches its own data or calls a service route instead of receiving data via props.
- Importing a sibling package's `src/*` instead of its public `dist`/entry.
- Bundling `vue`/`quasar` into a package, or shipping assets outside the bundling graph so they miss
  `dist/ssr/client/assets`.
- Rendering untrusted HTML without the sanctioned sanitizer.
- Wiring an island package into legacy `src/*`/boot/router/store/SW without explicit migration approval.

## Apply checklist

- Public contract (props/events/types) defined and documented before internals.
- Widget is props-in / events-out, owns no host singletons, fetches no data.
- Data flows presentation → flow composable → store → SDK; no direct SDK/service calls from the widget.
- Sibling consumption is `dist`/entry + `link:`; `vue`/`quasar` are peers; assets reach `dist/ssr/client/assets`.
- No trusted headers/tokens in widgets; raw HTML only via the sanctioned sanitizer.
- SSR-safe and deterministic; no island wiring into legacy lanes without approval.

## Companion routing

- `$alaa-mono-package` — mandatory for any package boundary, exports, dedupe, asset, or extraction decision.
- `$alaa-frontend-developer` — the three-layer architecture and SSR component patterns.
- `$alaa-quasar-app-vite-v3` — exact Quasar component/SSR shapes and the app-vite build posture.
- `$alaa-security-review` — mandatory for raw-HTML/sanitization and any trust-boundary-adjacent widget path.
- `$alaa-frontend-doc-annotations` — documentation pass for the widget/package public surface.
- For data a widget needs, route through `60-frontend-sdk-consumption-contract.md` (host fetches, widget receives props).

For package internals and the package-family map, read `packages/developer_guide.md` and the package's own
`developer_guide.md`; do not encode package internals here.
