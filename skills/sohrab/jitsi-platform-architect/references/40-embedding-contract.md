# Embedding Contract

Read this when embedding the meeting in a Vue, Quasar or Vite application, when choosing between the IFrame API and
`lib-jitsi-meet`, or when a meeting breaks under server-side rendering or a service worker.

This file owns the Jitsi side of the boundary: which integration surface to use, the embed lifecycle Jitsi
requires, what may and may not be overridden at embed time, and the caching rules that are specific to Jitsi
assets. It does not own component structure, store shape, boot-file convention, TypeScript style or permission
user experience — those belong to `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) and
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`). Every upstream IFrame API name below has a row in
`references/90-source-map.md`.

## Choose the integration surface first

**Default to the IFrame API.** It costs far less to maintain than a fork, gives immediate access to a mature
meeting experience, and supports runtime feature toggles and event hooks, so upgrades are a version bump rather
than a re-implementation.

Use a lower-level `lib-jitsi-meet` integration only when the product needs bespoke conference chrome, media layout,
or direct control the IFrame API does not expose — and state the maintenance cost when you propose it.

**Recording constrains this choice, so decide it before the frontend is built.** Jibri is built around a full
Jitsi Meet browser session. A product that replaces that surface entirely makes recording substantially harder, and
for online classes recording is often a graded artifact rather than a convenience. Raise it at the architecture
decision, not after the custom UI exists.

Reconsider the IFrame API when the product requires a visual language that replaces most native meeting chrome,
deep media layout control beyond the supported commands, cross-room orchestration inside your own canvas, or
moderation flows that diverge heavily from the built-in ones.

## The embed lifecycle Jitsi requires

Four obligations, each with the failure it prevents:

1. **Inject `external_api.js` at most once per page.** A second script tag produces a second global and an
   unpredictable constructor. Resolve the injection from a module-level promise so concurrent mounts share it.
2. **Construct the API only after the component is mounted and the container element exists.** Constructing against
   a null parent node fails silently in some paths and renders an empty meeting shell in others.
3. **Call `dispose()` on unmount and on route change, not on unmount alone.** A route change that keeps the
   component alive leaves a live conference behind, and the participant appears in two places.
4. **Guard the window between the awaited join fetch and the constructor.** The user can leave the route while the
   token request is in flight; constructing after that attaches a conference to a detached element that nothing
   will ever dispose.

## Lifecycle snippet — the Jitsi contract only

This shows the contract, not the component. Structure, typing conventions and store wiring belong to the two
frontend skills named above.

```ts
let api: JitsiMeetExternalAPI | null = null
let disposed = false
const controller = new AbortController()

function teardown() {
  disposed = true
  controller.abort()
  api?.dispose()
  api = null
}

onMounted(async () => {
  const join = await fetchJoin(controller.signal)      // rejects on non-2xx; the route renders that failure
  if (disposed || !containerRef.value) { return }      // unmounted while the token request was in flight
  await loadExternalApiOnce(`https://${join.domain}/external_api.js`)
  if (disposed || !containerRef.value) { return }      // and again while the script was loading
  api = new window.JitsiMeetExternalAPI(join.domain, {
    roomName: join.roomName, jwt: join.jwt, parentNode: containerRef.value,
  })
})

onBeforeUnmount(teardown)
onBeforeRouteLeave(teardown)
```

Four things this snippet is asserting, all of which the retired version of this file got wrong and none of which
may be reintroduced: the API handle is typed from the deployment's own declaration rather than `any`, so a renamed
method fails the build instead of failing in a lesson; the join response is typed rather than an untyped `fetch`
result; the join request has an error branch, because a join that cannot be authorized must render a failure and
not an empty meeting frame; and the fetch is abortable and both awaits are guarded, because the unmount race is the
defect that produces a conference nobody can leave.

**Reconnect.** `fetchJoin` is also what a reconnect calls. Never reuse the token the component joined with — the
reason is in `references/10-architecture-and-jwt-trust.md`, and the symptom it prevents is class 4 in
`references/20-failure-classes.md`.

## Server-side rendering

**Never instantiate Jitsi during a server render.**

- Do not touch `window`, `document` or the external API global on the server.
- Render a placeholder shell during the server render; mount the real meeting only in a client lifecycle. In
  Quasar, `QNoSsr` or an equivalent client-only wrapper is the mechanism.
- Load `external_api.js` only in the browser.
- Fetch join data after hydration, and mount the meeting only once the token and room identifier are present.
- **Never embed a join token in server-rendered HTML.** Server-rendered markup is cacheable, loggable and
  shareable, and a token in it survives in places nobody is watching. Issue the token from the client, close to
  the actual join.

## Progressive web apps

Treat the meeting route as network-sensitive, not offline-first.

- Never serve `external_api.js` from a service-worker cache without a revalidation rule. A stale copy pins the
  embed to an API surface the deployment has already moved past, and the failure appears as a missing method on
  one device and nowhere else.
- Exclude the meeting bootstrap document and every websocket-sensitive path from precaching, because a cached
  bootstrap points at a signalling endpoint that may have changed.
- Do not rely on cached meeting state for an active session; there is no useful offline state for a live
  conference.
- Handle background throttling and visibility changes explicitly, and expect a reconnect after the application
  resumes on mobile. Every one of those reconnects is a fresh join and a fresh token.
- Keep analytics heartbeats resilient to gaps and retries — `references/50-events-recording-governance.md`.

## The three configuration layers

Use the lightest layer that resolves the request.

**Layer 1 — deployment configuration.** Server-side configuration files hold defaults that apply across tenants and
rooms: feature defaults, branding, analytics defaults, and any restriction that must not be bypassed by an embed
caller. Anything security-relevant lives here, because this is the only layer the browser cannot reach.

**Layer 2 — embed-time overrides.** Constructor options carry room-specific and product-specific behaviour:
`configOverwrite`, `interfaceConfigOverwrite`, `jwt`, `userInfo`, `lang`, `iceServers` where the platform
deliberately overrides ICE behaviour, `buttonsWithNotifyClick` and `participantMenuButtonsWithNotifyClick` where
the host application intercepts toolbar or participant actions, and `useHostPageLocalStorage` where embed
persistence must follow the host page.

**Layer 3 — runtime commands.** Use these only for dynamic behaviour after mount; `overwriteConfig` is the main
one, and it applies only to what the running version supports.

## What cannot be overridden at embed time

- Host and moderator semantics are not reliably settable through `configOverwrite`. Privilege comes from the
  minted token, and a design that grants it from the embed will appear to work in development against an
  unsecured deployment and fail once token authentication is on.
- Security-relevant settings stay in the deployment configuration, by definition: an embed-time override is a
  value the browser supplied.
- Lobby, visitor and moderator behaviour are deployment and authentication concerns first and user-interface
  concerns second. Decide them in `references/10-architecture-and-jwt-trust.md`, then reflect them in the embed.

## Rules that hold across the boundary

- The host application remains the system of record for navigation, attendance, analytics and post-session state.
- Mirror only product-relevant meeting state into the application store. Mirroring every internal state couples the
  product to Jitsi's internals and breaks on upgrade.
- Never trust an embed-time role hint that is not backed by the server-minted token.
- Keep billing, attendance and lifecycle actions in platform UI outside the meeting frame, so they are not gated by
  a conference being reachable.
